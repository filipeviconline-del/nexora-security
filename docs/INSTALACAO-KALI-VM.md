# Instalação do Nexora Security no Kali Linux — VirtualBox

Este guia cobre a criação da VM, instalação do sistema, dependências, execução do Nexora e configuração da IA. **Estado atual:** o repositório contém documentação inicial; o código-fonte e scripts de instalação ainda não foram publicados integralmente. Não execute comandos que dependam de arquivos ausentes.

## 1. Preparar o VirtualBox

1. Baixe o [VirtualBox](https://www.virtualbox.org/) no computador principal.
2. Baixe uma imagem oficial em [Kali Linux Downloads](https://www.kali.org/get-kali/), preferencialmente a imagem pronta para VirtualBox.
3. Importe a VM, defina usuário/senha e inicie o Kali.
4. Se o computador permitir, configure **4 vCPUs, 8 GB RAM e 50 GB de disco**. Para um modelo local 3B, menos RAM pode prejudicar bastante o desempenho.
5. Escolha **rede NAT** para o primeiro teste. Não utilize bridge nem redirecione portas para a internet.
6. Após atualizar o sistema, crie um **snapshot** chamado `kali-limpo`.

## 2. Preparar o Kali

Abra o terminal da VM:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y git curl ca-certificates python3 python3-venv python3-pip unzip nmap whatweb dnsutils whois
python3 --version
git --version
```

## 3. Baixar o Nexora

O repositório está **privado**: faça login no GitHub com sua conta autorizada. Quando o código completo estiver publicado:

```bash
cd ~
git clone https://github.com/filipeviconline-del/nexora-security.git
cd nexora-security
ls -la
```

Confirme a presença de `main.py`, `requirements.txt` e `scripts/install-linux.sh`. Se faltarem, **pare aqui**: a publicação do código ainda não terminou.

## 4. Instalação básica

```bash
bash scripts/install-linux.sh
bash scripts/check.sh
```

O instalador prepara o Python e dependências básicas. Ferramentas Go e Ollama são opcionais e devem ser instalados separadamente.

## 5. Ollama e chat

Siga o guia [CONFIGURAR-OLLAMA.md](CONFIGURAR-OLLAMA.md). Resumo:

```bash
# Depois de instalar e iniciar o Ollama:
ollama pull llama3.2
# Opcional: execute somente se o projeto incluir um Modelfile
# ollama create nexora-ai -f Modelfile
ollama list
```

Inicie o Nexora:

```bash
bash scripts/start.sh
```

Abra na VM: **http://127.0.0.1:8001/chat**. Clique em **Conversar com IA** e faça uma pergunta conceitual para confirmar que a IA responde.

## 6. Testes

Em outro terminal:

```bash
cd ~/nexora-security
bash scripts/check.sh
curl -fsS http://127.0.0.1:11434/api/tags
curl -fsS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8001/chat
```

O primeiro comando verifica o ambiente; o segundo testa o Ollama; o terceiro testa o FastAPI.

## 7. Problemas comuns

- **VM lenta:** reduza outros programas abertos, aumente RAM/CPU ou teste modelo menor.
- **Ollama não responde:** verifique `systemctl status ollama` ou inicie `ollama serve` em terminal separado.
- **Modelo não encontrado:** execute `ollama list` e ajuste `OLLAMA_MODEL`.
- **Git clone solicita autenticação:** o repositório é privado; configure Git Credential Manager, GitHub CLI ou chave SSH.
- **Arquivos/scripts ausentes:** a publicação do código ainda está pendente.
- **Sem acesso do computador principal:** a interface está limitada ao loopback da VM por segurança. Não exponha portas para contornar isso; configure um acesso autenticado, por exemplo túnel SSH, quando necessário.

## 8. Segurança

Execute somente em alvos expressamente autorizados. Mantenha a VM em NAT, a aplicação em `127.0.0.1` e as portas 8001/11434 não expostas. Faça snapshot antes de instalar ferramentas extras.