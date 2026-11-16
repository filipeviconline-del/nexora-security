# Kali Linux no VirtualBox

1. Instale o [VirtualBox](https://www.virtualbox.org/) e baixe o [Kali oficial](https://www.kali.org/get-kali/).
2. Importe a VM e configure, se o computador permitir, 4 vCPUs, 8 GB RAM, disco de 50 GB e rede NAT.
3. Inicie o Kali e crie um snapshot.
4. Abra o terminal:

```bash
sudo apt update
sudo apt install -y git
git clone https://github.com/filipeviconline-del/nexora-security.git
cd nexora-security
bash scripts/install-linux.sh
bash scripts/check.sh
bash scripts/start.sh
```

5. Acesse `http://127.0.0.1:8001/chat` no navegador da VM.
6. Opcional: instale o [Ollama](https://ollama.com/download/linux) e rode `bash scripts/install-ollama.sh`.

**Atenção:** os scripts precisam estar publicados no repositório antes da instalação. Não exponha as portas 8001 ou 11434 na internet. Execute apenas testes autorizados.