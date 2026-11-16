# Instalação do Nexora Security no Ubuntu / Debian

Este guia é para instalações locais em Ubuntu e Debian. Para Kali no VirtualBox consulte [INSTALACAO-KALI-VM.md](INSTALACAO-KALI-VM.md); para Windows consulte [INSTALACAO-WINDOWS.md](INSTALACAO-WINDOWS.md).

> **Estado atual:** os arquivos de código e scripts de instalação ainda não estão integralmente publicados. Não execute comandos que dependam de arquivos ausentes.

## 1. Requisitos

- Ubuntu/Debian com `apt`, internet, Python 3 e Git
- Recomendados 8 GB de RAM para modelo local 3B em CPU
- Permissão para instalar pacotes com `sudo`

## 2. Atualizar e instalar dependências

```bash
sudo apt update
sudo apt install -y git curl ca-certificates python3 python3-venv python3-pip nmap whatweb dnsutils whois
```

## 3. Clonar repositório

O repositório é privado; autentique-se no GitHub com uma conta autorizada.

```bash
cd ~
git clone https://github.com/filipeviconline-del/nexora-security.git
cd nexora-security
ls -la
```

Confirme `main.py`, `requirements.txt`, `Modelfile` e `scripts/install-linux.sh`. Se faltarem, aguarde a publicação do código.

## 4. Instalação

```bash
bash scripts/install-linux.sh
bash scripts/check.sh
```

O instalador cria o ambiente virtual e instala dependências básicas. Não instala automaticamente todas as ferramentas Go nem o Ollama.

## 5. Configurar IA

Consulte [CONFIGURAR-OLLAMA.md](CONFIGURAR-OLLAMA.md). Após instalar e iniciar o Ollama:

```bash
ollama pull llama3.2
# Opcional: execute somente se o projeto incluir um Modelfile
# ollama create nexora-ai -f Modelfile
ollama list
```

## 6. Iniciar

```bash
bash scripts/start.sh
```

Abra **http://127.0.0.1:8001/chat**. Para parar o servidor use `Ctrl+C`.

## 7. Verificação

Em outro terminal:

```bash
bash scripts/check.sh
curl -fsS http://127.0.0.1:11434/api/tags
curl -fsS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8001/chat
```

## 8. Solução de problemas

- `No module named uvicorn`: ative o venv ou execute novamente `bash scripts/install-linux.sh`.
- `Port 8001 already in use`: encerre a instância antiga antes de iniciar outra.
- Ollama indisponível: `systemctl status ollama`, `ollama list` e guia Ollama.
- Ferramentas ausentes: veja [FERRAMENTAS.md](FERRAMENTAS.md).
- Scripts ausentes no clone: código ainda não publicado integralmente.

## 9. Segurança

Mantenha `--host 127.0.0.1`. Não exponha FastAPI/Ollama na internet, não publique segredos nem execute verificações sem autorização explícita.