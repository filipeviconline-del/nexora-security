# Instalação do Nexora Security no Windows 11 com WSL2

O Nexora é uma aplicação Python/FastAPI executada em Linux. **Não há instalador `.exe` nativo nesta versão.** A abordagem documentada é Ubuntu no WSL2, com Ollama também dentro do Ubuntu para manter o endereço local `127.0.0.1:11434`.

## 1. Instalar o WSL2

Abra **PowerShell como Administrador**:

```powershell
wsl --install -d Ubuntu
```

Reinicie se solicitado. Abra o aplicativo Ubuntu e crie usuário e senha Linux. No PowerShell, confira:

```powershell
wsl --list --verbose
```

O Ubuntu deve estar na **VERSION 2**. Referência: [Microsoft — Instalar WSL](https://learn.microsoft.com/windows/wsl/install).

## 2. Preparar o Ubuntu no WSL2

Os comandos a seguir são **Bash no terminal Ubuntu**, não PowerShell:

```bash
sudo apt update
sudo apt install -y git curl ca-certificates python3 python3-venv python3-pip nmap whatweb dnsutils whois
```

Trabalhe em `~/nexora-security`, não em `/mnt/c`, para evitar problemas de desempenho e permissões.

## 3. Clonar o código atualizado

```bash
cd ~
git clone https://github.com/filipeviconline-del/nexora-security.git
cd nexora-security
ls main.py requirements.txt
ls nexora/api nexora/core nexora/recon nexora/web
```

Se já houver clone, atualize-o com `git pull --ff-only origin main` sem descartar alterações locais.

## 4. Instalar o ambiente Python

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip check
python -m compileall -q main.py nexora
python -c "from main import app; print('NEXORA: IMPORTAÇÃO OK'); print('Rotas:', len(app.routes))"
```

O arquivo `requirements.txt` inclui `dnspython`, necessário para os módulos de DNS. Não execute `pip` globalmente com `sudo`.

## 5. Configurar Ollama no Ubuntu WSL2

Siga [CONFIGURAR-OLLAMA.md](CONFIGURAR-OLLAMA.md) para instalar Ollama da fonte oficial **dentro do WSL2**.

Se `systemctl` não estiver disponível, abra **outro terminal Ubuntu** e execute:

```bash
ollama serve
```

No terminal principal:

```bash
ollama pull llama3.2
ollama list
curl -fsS http://127.0.0.1:11434/api/tags
```

Não inicie uma segunda instância se o serviço já estiver ativo. A instalação do Ollama somente no Windows pode exigir configuração de rede adicional, não coberta por este caminho simplificado.

## 6. Iniciar o Nexora

```bash
cd ~/nexora-security
source .venv/bin/activate
export PATH="$HOME/go/bin:$PATH"
export OLLAMA_MODEL=llama3.2
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```

Definir `OLLAMA_MODEL` é importante: alguns módulos ainda têm `linuxsec-ai` como modelo padrão interno.

No navegador **do Windows**, abra **http://localhost:8001/chat**. O encaminhamento de localhost do WSL2 geralmente permite esse acesso, mas pode variar conforme a configuração.

## 7. Diagnóstico

No Ubuntu WSL2:

```bash
curl -fsS -o /dev/null -w 'Chat HTTP: %{http_code}\n' http://127.0.0.1:8001/chat
curl -fsS http://127.0.0.1:11434/api/tags
```

- **Erro de virtualização:** verifique os requisitos de virtualização e WSL2 na documentação Microsoft.
- **`No module named dns`:** `source .venv/bin/activate` e `python -m pip install -r requirements.txt`.
- **`model not found`:** `ollama pull llama3.2` e `export OLLAMA_MODEL=llama3.2`.
- **FastAPI funciona no WSL, mas não no Windows:** investigue encaminhamento localhost do WSL2; não exponha o serviço na internet.
- **Porta ocupada:** pare a instância anterior ou use `--port 8002`.
- **Ferramenta externa ausente:** consulte [FERRAMENTAS.md](FERRAMENTAS.md).

Mais detalhes em [Solução de problemas](SOLUCAO-DE-PROBLEMAS.md).

## 8. Segurança

Mantenha FastAPI e Ollama locais. O Nexora ainda não tem autenticação de usuários. Use ferramentas de reconhecimento somente em sistemas autorizados.
