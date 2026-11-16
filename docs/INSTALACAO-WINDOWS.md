# Instalação do Nexora Security no Windows 11 com WSL2

O Nexora é uma aplicação Linux/Python. **Não há instalador .exe nativo** nesta versão. A opção recomendada no Windows é executar o backend dentro do Ubuntu no WSL2 e acessar o chat pelo navegador do Windows.

> **Estado atual:** os arquivos de código e scripts de instalação ainda não estão integralmente publicados neste repositório. Não prossiga com scripts ausentes.

## 1. Verificar os requisitos

- Windows 11 atualizado, virtualização habilitada no firmware, espaço livre em disco e internet
- Preferencialmente **8 GB de RAM disponíveis** para testes com Ollama 3B; menos RAM pode ficar lento
- PowerShell aberto como **Administrador** somente para a instalação do WSL

## 2. Instalar o Ubuntu no WSL2

No PowerShell (Administrador):

```powershell
wsl --install -d Ubuntu
```

Reinicie o Windows caso seja solicitado. Abra **Ubuntu** no menu Iniciar e defina usuário e senha Linux.

Confira a versão no PowerShell:

```powershell
wsl --list --verbose
```

O Ubuntu deve aparecer com **VERSION 2**. Se necessário, consulte [Instalação oficial do WSL](https://learn.microsoft.com/windows/wsl/install).

## 3. Preparar o Ubuntu

No terminal **Ubuntu**, e não no PowerShell:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y git curl ca-certificates python3 python3-venv python3-pip nmap whatweb dnsutils whois
```

## 4. Baixar o projeto

O repositório é privado: use uma conta GitHub autorizada. Quando o código completo estiver publicado:

```bash
cd ~
git clone https://github.com/filipeviconline-del/nexora-security.git
cd nexora-security
ls -la
```

Se não houver `main.py` e `scripts/install-linux.sh`, pare: o código ainda não foi publicado por completo.

## 5. Instalar o Nexora

```bash
bash scripts/install-linux.sh
bash scripts/check.sh
```

## 6. Instalar e conectar o Ollama

Use o guia completo [CONFIGURAR-OLLAMA.md](CONFIGURAR-OLLAMA.md). A configuração mais simples para esta versão é manter **Ollama e Nexora no mesmo Ubuntu WSL2**, pois o backend chama `127.0.0.1:11434`.

Depois de instalar o Ollama, caso não exista serviço systemd ativo, abra um segundo terminal Ubuntu e execute:

```bash
ollama serve
```

No primeiro terminal:

```bash
ollama pull llama3.2
cd ~/nexora-security
ollama create linuxsec-ai -f Modelfile
bash scripts/start.sh
```

## 7. Abrir no navegador do Windows

Acesse **http://localhost:8001/chat**.

Se não abrir, no Ubuntu teste:

```bash
curl -fsS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8001/chat
curl -fsS http://127.0.0.1:11434/api/tags
```

Se funcionar dentro do WSL mas não no navegador, investigue o encaminhamento de localhost e a configuração de rede do WSL2. Não abra a porta para a internet.

## 8. Diagnóstico

- `wsl: command not found` no PowerShell: confirme atualização e privilégios do Windows.
- Erro de virtualização: habilite a virtualização no BIOS/UEFI e recursos necessários do Windows.
- `ollama: command not found`: instale o Ollama **dentro do Ubuntu WSL2**.
- `model not found`: confira `ollama list` e `OLLAMA_MODEL`.
- Chat não responde: verifique o Ollama na porta 11434 e o FastAPI na 8001.
- Ferramentas de reconhecimento ausentes: verifique `bash scripts/check.sh` e [FERRAMENTAS.md](FERRAMENTAS.md).

## 9. Cuidados

Não execute scanners em ativos sem autorização. Não exponha as portas 8001/11434 publicamente. Evite armazenar código e ambientes virtuais em `/mnt/c` para não prejudicar desempenho e permissões; prefira `~/nexora-security` dentro do Ubuntu.