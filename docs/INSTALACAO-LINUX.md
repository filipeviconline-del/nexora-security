# Ubuntu e Debian

Pré-requisitos: Linux com apt, Git, Python 3 e acesso à internet.

```bash
sudo apt update
sudo apt install -y git
git clone https://github.com/filipeviconline-del/nexora-security.git
cd nexora-security
bash scripts/install-linux.sh
bash scripts/check.sh
bash scripts/start.sh
```

Abra `http://127.0.0.1:8001/chat`. Para IA local, instale o [Ollama](https://ollama.com/download/linux) e execute `bash scripts/install-ollama.sh`.

**Atenção:** a publicação dos scripts ainda precisa ser concluída. Não execute como root nem exponha as portas do FastAPI/Ollama à internet.