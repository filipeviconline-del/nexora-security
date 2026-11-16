"""LinuxSec Security Chat v5: approved, bounded tool orchestration."""
import ipaddress
import json
import os
import shutil
import subprocess
import urllib.request
from datetime import datetime, timezone
from urllib.parse import urlsplit

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from nexora.api.nmap_engine import LOCK, normalize_host, read_targets, resolve_dns, run_nmap, NmapRequest
from nexora.recon.dns_recon import query_records

router = APIRouter(prefix='/tools/chat', tags=['Security Chat'])

class PlanRequest(BaseModel):
    target: str = Field(min_length=3, max_length=253)
    message: str = Field(default='Analise a superfície de exposição autorizada.', max_length=10000)

class RunRequest(PlanRequest):
    approved: bool = False
    tools: list[str] = Field(default_factory=lambda: ['dns', 'nmap', 'whatweb'], max_length=5)

ALLOWED = {'dns', 'nmap', 'whatweb', 'subfinder', 'amass', 'dnsx', 'dnsx_brute', 'httpx', 'katana', 'gau'}

def scope_entry(target):
    host, is_ip = normalize_host(target)
    with LOCK:
        entry = next((x for x in read_targets() if x['ip'] == host), None)
    if entry is None:
        raise HTTPException(status_code=403, detail='Alvo não cadastrado no escopo autorizado.')
    return host, is_ip, entry

def approved_ip(host, is_ip, entry):
    if is_ip:
        return host
    current = resolve_dns(host)
    if not set(current).issubset(set(entry.get('resolved_ips', []))):
        raise HTTPException(status_code=409, detail='DNS alterado: revise e recadastre o alvo antes de executar.')
    return current[0]

def safe_web_target(host, is_ip, entry):
    # Do not follow redirects; constrain the connection to an approved IP using curl --resolve.
    ip = approved_ip(host, is_ip, entry)
    addr = ipaddress.ip_address(ip)
    if addr.is_link_local or addr.is_multicast or addr.is_unspecified:
        raise HTTPException(status_code=403, detail='Endereço não permitido para verificação web.')
    return ip

@router.post('/plan')
def plan(body: PlanRequest):
    host, is_ip, _ = scope_entry(body.target)
    steps = []
    if not is_ip and (body.message.strip().lower() == 'gau' or 'get all urls' in body.message.lower()):
        steps.append({'tool':'gau','description':'GAU: URLs historicas publicas do hostname cadastrado, sem visitar endpoints'})
        return {'target':host, 'message':body.message, 'steps':steps, 'approval_required':True, 'notice':'Consulta a indices publicos; sem varredura ativa dos endpoints.'}
    if not is_ip and 'katana' in body.message.lower():
        steps.append({'tool':'katana','description':'Crawler de profundidade 1 no host cadastrado, 1 req/s, sem formularios'})
        return {'target':host, 'message':body.message, 'steps':steps, 'approval_required':True, 'notice':'Somente dominio cadastrado. Sem expansao automatica de escopo.'}
    if not is_ip and any(term in body.message.lower() for term in ('httpx', 'http probe', 'http probe')):
        steps.append({'tool':'httpx','description':'HTTPx: verificar HTTP/HTTPS do dominio cadastrado, sem seguir redirecionamentos'})
        return {'target':host, 'message':body.message, 'steps':steps, 'approval_required':True, 'notice':'Somente dominio cadastrado; nao executar automaticamente nos subdominios encontrados.'}
    if not is_ip and any(term in body.message.lower() for term in ('dns brute', 'dnsx brute', 'força bruta dns', 'bruteforce dns')):
        steps.append({'tool':'dnsx_brute','description':'Descoberta DNS por lista limitada de 53 nomes (2 consultas/s)'})
        return {'target':host, 'message':body.message, 'steps':steps, 'approval_required':True, 'notice':'Modo ativo de consultas DNS; execute somente em domínio sob sua administração.'}
    if not is_ip and 'dnsx' in body.message.lower():
        steps.append({'tool':'dnsx','description':'Consultas DNS A, AAAA, CNAME, MX e NS (DNSx)'})
        return {'target':host, 'message':body.message, 'steps':steps, 'approval_required':True, 'notice':'Plano DNSx isolado; exige aprovação.'}
    if not is_ip:
        steps.append({'tool':'subfinder','description':'Enumeração passiva de subdomínios (fontes externas)'})
        steps.append({'tool':'amass','description':'Mapeamento passivo de subdomínios (Amass v5)'})
    if not is_ip:
        steps.append({'tool':'dns','description':'Registros DNS públicos'})
    steps.append({'tool':'nmap','description':'Portas e serviços (top 20)'})
    if not is_ip:
        steps.append({'tool':'whatweb','description':'Identificação de tecnologias HTTP(S), sem redirecionamentos'})
    return {'target':host, 'message':body.message, 'steps':steps, 'approval_required':True,
            'notice':'Plano determinístico; a IA interpreta os resultados, mas não executa comandos livres.'}

def whatweb(host, entry):
    from nexora.recon.adapters.whatweb_adapter import run_whatweb
    return run_whatweb(host, entry, approved_ip, safe_web_target)


from nexora.core.report_engine import ai_summary

@router.post('/run')
def run(body: RunRequest):
    if not body.approved:
        raise HTTPException(status_code=400,detail='Aprovação explícita necessária.')
    if len(set(body.tools)) != len(body.tools) or not set(body.tools).issubset(ALLOWED):
        raise HTTPException(status_code=400,detail='Ferramentas inválidas ou repetidas.')
    host, is_ip, entry = scope_entry(body.target)
    # Validate before any active action.
    approved_ip(host,is_ip,entry)
    if is_ip and ('dns' in body.tools or 'whatweb' in body.tools or 'subfinder' in body.tools or 'amass' in body.tools or 'dnsx' in body.tools or 'dnsx_brute' in body.tools or 'httpx' in body.tools or 'katana' in body.tools or 'gau' in body.tools):
        raise HTTPException(status_code=400,detail='DNS e inspeção web requerem domínio cadastrado.')
    results = {}
    if 'gau' in body.tools:
        from nexora.recon.adapters.gau_adapter import run_gau
        results['gau'] = run_gau(host, is_ip, entry)
    if 'katana' in body.tools:
        from nexora.recon.adapters.katana_adapter import run_katana
        results['katana'] = run_katana(host, is_ip, entry, approved_ip)
    if 'httpx' in body.tools:
        from nexora.recon.adapters.httpx_adapter import run_httpx
        results['httpx'] = run_httpx(host, is_ip, entry, approved_ip)
    if 'dnsx_brute' in body.tools:
        from nexora.recon.adapters.dnsx_brute_adapter import run_dnsx_brute
        results['dnsx_brute'] = run_dnsx_brute(host, is_ip, entry)
    if 'dnsx' in body.tools:
        from nexora.recon.adapters.dnsx_adapter import run_dnsx
        results['dnsx'] = run_dnsx(host, is_ip, entry)
    if 'subfinder' in body.tools:
        from nexora.recon.adapters.subfinder_adapter import run_subfinder
        results['subfinder'] = run_subfinder(host, is_ip, entry)
    if 'amass' in body.tools:
        from nexora.recon.adapters.amass_adapter import run_amass
        results['amass'] = run_amass(host, is_ip, entry)
    if 'dns' in body.tools:
        results['dns'] = query_records(host)
    if 'nmap' in body.tools:
        results['nmap'] = run_nmap(NmapRequest(target=host))
    if 'whatweb' in body.tools:
        results['whatweb'] = whatweb(host,entry)
    return {'target':host,'executed_at':datetime.now(timezone.utc).isoformat(),
            'results':results,'ai':ai_summary(host,results,body.message),
            'notice':'Somente ações aprovadas; resultados de ferramentas são evidências, não confirmação de vulnerabilidade.'}


class GrepExplainRequest(BaseModel):
    target: str = Field(min_length=3, max_length=253)
    keywords: list[str] = Field(min_length=1, max_length=10)
    matches: list[dict] = Field(default_factory=list, max_length=40)

@router.post('/explain-grep')
def explain_grep(body: GrepExplainRequest):
    host, _, _ = scope_entry(body.target)
    # Results from the client are untrusted; never use them as commands or as proof.
    clean = [{'line': str(m.get('line',''))[:10], 'text': str(m.get('text',''))[:500]}
             for m in body.matches[:40]]
    return ai_summary(host, {'grep_matches': clean, 'keywords': body.keywords},
        'Explique em português as correspondências textuais de forma detalhada, '
        'indicando evidências, incertezas, verificações defensivas e correções pertinentes. '
        'Não afirme que uma correspondência comprova vulnerabilidade.')
