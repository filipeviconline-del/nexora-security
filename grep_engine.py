"""Pesquisa controlada com grep em evidências fornecidas pelo operador.
Não aceita caminhos de arquivos, shell ou opções de linha de comando arbitrárias.
"""
import shutil
import subprocess
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix='/tools', tags=['Evidence Search'])
MAX_TEXT = 200_000
MAX_MATCHES = 150

class GrepRequest(BaseModel):
    text: str = Field(min_length=1, max_length=MAX_TEXT)
    keywords: list[str] = Field(min_length=1, max_length=10)
    ignore_case: bool = True

@router.post('/grep')
def grep_evidence(body: GrepRequest):
    executable = shutil.which('grep')
    if not executable:
        raise HTTPException(status_code=503, detail='grep não encontrado no sistema.')
    keywords = []
    for raw in body.keywords:
        word = raw.strip()
        if not word or len(word) > 80 or '\x00' in word or '\n' in word or '\r' in word:
            raise HTTPException(status_code=400, detail='Cada palavra-chave deve ter entre 1 e 80 caracteres e ocupar uma linha.')
        if word not in keywords:
            keywords.append(word)
    # -F: pesquisa literal, sem regex; -n: número da linha; -i: sem diferenciar maiúsculas.
    # -- separa opções dos padrões; entrada exclusivamente por stdin.
    command = [executable, '-F', '-n']
    if body.ignore_case:
        command.append('-i')
    for word in keywords:
        command.extend(['-e', word])
    command.extend(['--', '-'])
    try:
        result = subprocess.run(command, input=body.text, capture_output=True,
                                text=True, timeout=5, check=False)
    except subprocess.TimeoutExpired as exc:
        raise HTTPException(status_code=504, detail='Pesquisa excedeu 5 segundos.') from exc
    except OSError as exc:
        raise HTTPException(status_code=500, detail='Falha ao executar grep.') from exc
    if result.returncode not in (0, 1):
        raise HTTPException(status_code=500, detail='grep não conseguiu processar a pesquisa.')
    lines = result.stdout.splitlines()
    matches = []
    for line in lines[:MAX_MATCHES]:
        number, sep, content = line.partition(':')
        if sep and number.isdecimal():
            matches.append({'line': int(number), 'text': content[:1000]})
    return {
        'tool': 'grep', 'source': 'texto fornecido na requisição',
        'keywords': keywords, 'ignore_case': body.ignore_case,
        'total_matches': len(lines), 'truncated': len(lines) > MAX_MATCHES,
        'matches': matches,
        'notice': 'Correspondências textuais não comprovam vulnerabilidades. Não foram lidos arquivos locais.'
    }
