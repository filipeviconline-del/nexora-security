# Windows 11 com WSL2

Não há instalador .exe nativo. O caminho recomendado é executar o Nexora no Ubuntu dentro do WSL2.

1. Abra PowerShell como Administrador:

```powershell
wsl --install -d Ubuntu
```

2. Reinicie se solicitado, abra Ubuntu e crie usuário e senha.
3. Confirme no PowerShell: `wsl --list --verbose` (versão 2).
4. No terminal **Ubuntu**:

```bash
sudo apt update
sudo apt install -y git
git clone https://github.com/filipeviconline-del/nexora-security.git
cd nexora-security
bash scripts/install-linux.sh
bash scripts/check.sh
bash scripts/start.sh
```

5. No navegador do Windows, acesse `http://localhost:8001/chat`.
6. Opcional: instale [Ollama no Ubuntu](https://ollama.com/download/linux) e execute `bash scripts/install-ollama.sh`.

Se não abrir, teste `curl -I http://127.0.0.1:8001/chat` dentro do Ubuntu. Confira [documentação oficial do WSL](https://learn.microsoft.com/windows/wsl/install).

**Atenção:** os scripts precisam estar publicados antes da instalação. Não exponha portas nem realize testes fora do escopo autorizado.