# Instalação do Nexora Security no Kali Linux — VirtualBox

Este guia usa a **estrutura atual** do código no GitHub. Não requer scripts de instalação ausentes. A execução dentro de VM depende dos recursos do computador hospedeiro.

## 1. Preparar a máquina virtual

1. Baixe o VirtualBox no [site oficial](https://www.virtualbox.org/) e a imagem do Kali em [kali.org](https://www.kali.org/get-kali/).
2. Importe a VM e inicie o Kali.
3. Se possível, aloque 4 vCPUs, 8 GB de RAM e 50 GB de disco; modelos de IA podem exigir mais.
4. Use **rede NAT** para o primeiro teste. Não exponha portas do FastAPI ou Ollama.
5. Crie um snapshot antes de instalar novas ferramentas.

## 2. Preparar o Kali

Execute **dentro do terminal da VM**:

```bash
sudo apt update
sudo apt install -y git curl ca-certificates python3 python3-venv python3-pip nmap whatweb dnsutils whois
```

## 3. Clonar o Nexora

```bash
cd ~
git clone https://github.com/filipeviconline-del/nexora-security.git
cd nexora-security
ls main.py requirements.txt
ls nexora/api nexora/core nexora/recon nexora/web
```

Se já tiver um clone sem alterações locais, use `git pull --ff-only origin main` dentro dele.

## 4. Instalar as dependências Python

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip check
python -m compileall -q main.py nexora
python -c "from main import app; print('NEXORA: IMPORTAÇÃO OK'); print('Rotas:', len(app.routes))"
```

O pacote **dnspython** já está declarado no `requirements.txt`. Se `import dns` falhar, confirme que está usando o Python do `.venv`.

## 5. Configurar Ollama na própria VM

Siga [CONFIGURAR-OLLAMA.md](CONFIGURAR-OLLAMA.md) para instalar Ollama da fonte oficial. Depois:

```bash
ollama pull llama3.2
ollama list
curl -fsS http://127.0.0.1:11434/api/tags
```

Se o serviço não estiver ativo, verifique `sudo systemctl status ollama`. Em ambientes sem serviço configurado, use `ollama serve` em um segundo terminal. Não execute dois servidores na mesma porta.

**Atenção:** o modelo padrão de alguns módulos internos ainda é `linuxsec-ai`. O comando de inicialização abaixo define `llama3.2` explicitamente para evitar falhas.

## 6. Iniciar o aplicativo

```bash
cd ~/nexora-security
source .venv/bin/activate
export PATH="$HOME/go/bin:$PATH"
export OLLAMA_MODEL=llama3.2
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```

No navegador **dentro do Kali**, acesse:

- Chat: http://127.0.0.1:8001/chat
- Dashboard: http://127.0.0.1:8001/dashboard

O navegador do computador hospedeiro não acessará automaticamente o `127.0.0.1` da VM: são ambientes diferentes. Para o primeiro teste, use o navegador da VM.

## 7. Verificar e solucionar

Em outro terminal da VM:

```bash
curl -fsS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8001/chat
curl -fsS http://127.0.0.1:11434/api/tags
```

- **Erro `No module named dns`**: ative `.venv` e reinstale `requirements.txt`.
- **Ollama não responde**: confira serviço e `ollama list`.
- **VM lenta**: verifique RAM, CPU e disponibilidade de disco; considere um modelo menor.
- **Mouse/teclado do VirtualBox**: confira integração do ponteiro e Guest Additions conforme versão do VirtualBox.
- **Porta 8001 ocupada**: encerre instância anterior ou use `--port 8002`.

Consulte [Solução de problemas](SOLUCAO-DE-PROBLEMAS.md).

## 8. Segurança

Mantenha rede NAT e `--host 127.0.0.1`. A aplicação não implementa autenticação de usuários nesta versão. Faça reconhecimento apenas em ativos com autorização explícita.
