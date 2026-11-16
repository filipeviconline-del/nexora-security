# Checklist de diagnóstico — Nexora Security

Este roteiro reúne verificações **somente de leitura**, sem reinstalar ou apagar arquivos. Execute no terminal Linux onde o backend Nexora roda. Em Windows/WSL2, abra o **Ubuntu**.

## 1. Identificar ambiente

```bash
pwd
uname -a
cat /etc/os-release | grep -E '^(NAME|VERSION|PRETTY_NAME)='
python3 --version
command -v python3
```

Confira se você está na pasta correta do projeto. Em instalações antigas, o caminho pode ser diferente do nome do repositório. **Não renomeie diretórios em produção sem atualizar os caminhos usados pelo aplicativo.**

## 2. Verificar arquivos e Python

```bash
ls -la
test -f main.py && echo "main.py: OK" || echo "main.py: AUSENTE"
test -f requirements.txt && echo "requirements.txt: OK" || echo "requirements.txt: AUSENTE"
test -d .venv && echo ".venv: EXISTE" || echo ".venv: AUSENTE"
```

Se `.venv` existir:

```bash
source .venv/bin/activate
python -c "import sys; print(sys.executable)"
python -m pip --version
python -c "import uvicorn; print('uvicorn:', uvicorn.__version__)"
```

Se `uvicorn` não estiver disponível, consulte [ERR-001](SOLUCAO-DE-PROBLEMAS.md#err-001--no-module-named-uvicorn).

## 3. Verificar Ollama e modelos

```bash
command -v ollama || true
ollama --version 2>/dev/null || true
curl --max-time 5 -fsS http://127.0.0.1:11434/api/tags
ollama list
```

A consulta à API deve retornar JSON com a chave `models`. Se falhar, consulte [ERR-003](SOLUCAO-DE-PROBLEMAS.md#err-003--ollama-indisponível-ou-connection-refused).

## 4. Verificar portas e interface

```bash
ss -ltnp | grep -E ':(8001|11434)\b' || true
curl --max-time 5 -sS -o /dev/null -w 'HTTP Nexora: %{http_code}\n' http://127.0.0.1:8001/chat
```

- Código **200** geralmente indica que a página respondeu.
- Código **404** pode indicar rota incorreta.
- Código **405** em teste `HEAD` não significa necessariamente que `GET` falhou; este roteiro usa `GET`.
- Código **000** significa que não foi recebida uma resposta HTTP válida; consulte o erro do `curl`.

## 5. Verificar ferramentas

```bash
export PATH="$HOME/go/bin:$PATH"
for t in nmap whatweb whois dig subfinder amass dnsx httpx katana gau; do
  printf '%-12s %s\n' "$t" "$(command -v "$t" || echo AUSENTE)"
done
```

Uma ferramenta ausente pode ser **opcional**. Não reinstale todo o projeto apenas por isso. Consulte [Ferramentas](FERRAMENTAS.md).

## 6. Verificar recursos

```bash
free -h
df -h /
```

Se a memória ou disco estiverem insuficientes, interrompa tarefas pesadas e libere espaço de maneira controlada. **Não apague logs, modelos ou ambientes virtuais sem backup e confirmação do que está sendo removido.**

## 7. Próximo passo

Procure o sintoma na [tabela de erros](SOLUCAO-DE-PROBLEMAS.md) e aplique **uma correção por vez**. Repita a verificação que falhou antes de tentar outra alteração.

[Índice da documentação](README.md)
