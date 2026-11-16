# Instalação do Nexora Security — Ubuntu e Debian

> **Guia para a estrutura atual do repositório (`main.py` + pacote `nexora/`).** Não depende de `scripts/install-linux.sh`, `scripts/check.sh` ou `scripts/start.sh`: esses arquivos não fazem parte da instalação aqui documentada. A instalação foi verificada parcialmente no Ubuntu (dependências, importação FastAPI e interface do chat); não há garantia de funcionamento em todas as distribuições.

## 1. Requisitos

- Ubuntu ou Debian atualizado, acesso à internet, Git e Python 3 com suporte a `venv`.
- Recomendados 8 GB de RAM ou mais para usar um modelo local; os requisitos variam conforme o modelo.
- Ollama instalado **na mesma máquina** do FastAPI (API local `127.0.0.1:11434`).
- Ferramentas como Nmap, WhatWeb e utilitários Go são opcionais e dependem da funcionalidade utilizada.

## 2. Instalar dependências do sistema

Execute no terminal Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y git curl ca-certificates python3 python3-venv python3-pip nmap whatweb dnsutils whois
python3 --version
```

Se o sistema não encontrar `python3-venv`, atualize os índices do APT e consulte o pacote `python3.X-venv` correspondente à versão instalada.

## 3. Clonar o código atualizado

```bash
cd ~
git clone https://github.com/filipeviconline-del/nexora-security.git
cd nexora-security
git switch main
ls main.py requirements.txt
ls nexora/api nexora/core nexora/recon nexora/web
```

Se a pasta `~/nexora-security` já existir e for um clone Git sem alterações locais:

```bash
cd ~/nexora-security
git pull --ff-only origin main
```

Não execute `git reset --hard` nem sobrescreva modificações próprias. Se `git pull` falhar, preserve seu trabalho e investigue o conflito.

## 4. Criar ambiente virtual e instalar Python

```bash
cd ~/nexora-security
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip check
```

O `requirements.txt` atual inclui `fastapi`, `uvicorn` e **`dnspython`**. O último é necessário para importar `nexora.recon.dns_recon`. Não instale essas dependências globalmente com `sudo pip`.

## 5. Validar o backend antes de iniciar

```bash
python -m compileall -q main.py nexora
python -c "from main import app; print('NEXORA: IMPORTAÇÃO OK'); print('Rotas:', len(app.routes))"
```

No teste de referência realizado após a reorganização, foram registradas **14 rotas**. A quantidade pode mudar em versões posteriores; o importante é importar sem exceções.

Se aparecer `No module named 'dns'`, execute `python -m pip install -r requirements.txt` novamente **com o ambiente virtual ativo**.

## 6. Instalar e iniciar Ollama

Consulte [CONFIGURAR-OLLAMA.md](CONFIGURAR-OLLAMA.md) para instalação detalhada e alternativas para WSL/VM.

Depois de instalar Ollama da fonte oficial e iniciar o serviço:

```bash
ollama pull llama3.2
ollama list
curl -fsS http://127.0.0.1:11434/api/tags
```

**Importante:** parte do backend ainda usa `linuxsec-ai` como nome de modelo padrão interno, mesmo que a interface exiba **Nexora Security**. Para evitar o erro `model not found`, sempre defina explicitamente `OLLAMA_MODEL=llama3.2` ao iniciar. Não é necessário renomear seu modelo nem alterar o código.

## 7. Iniciar o Nexora

```bash
cd ~/nexora-security
source .venv/bin/activate
export PATH="$HOME/go/bin:$PATH"
export OLLAMA_MODEL=llama3.2
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```

Abra **http://127.0.0.1:8001/chat**. Para parar, pressione `Ctrl+C`.

Para um teste isolado, use a porta `8002` em vez de `8001`. Mantenha `--host 127.0.0.1`: a aplicação ainda não tem autenticação de usuários.

## 8. Testar instalação

Em outro terminal:

```bash
curl -fsS -o /dev/null -w 'Chat HTTP: %{http_code}\n' http://127.0.0.1:8001/chat
curl -fsS -o /dev/null -w 'Dashboard HTTP: %{http_code}\n' http://127.0.0.1:8001/dashboard
curl -fsS http://127.0.0.1:11434/api/tags
```

Abra o chat e faça uma pergunta conceitual usando **Conversar com IA**. O inventário de ferramentas pode ser respondido localmente, portanto não serve sozinho para confirmar a conexão com Ollama.

## 9. Erros comuns

| Erro | Ação |
|---|---|
| `No module named uvicorn` | `source .venv/bin/activate` e `python -m pip install -r requirements.txt` |
| `No module named dns` | Reinstale `requirements.txt`; confirme `dnspython` |
| `Address already in use` | Encerre a instância anterior ou use `--port 8002` |
| `model not found` | `ollama pull llama3.2`; `export OLLAMA_MODEL=llama3.2` |
| `Connection refused` em 11434 | Inicie o serviço Ollama e confira `curl /api/tags` |
| `externally-managed-environment` | Ative `.venv`; não use `sudo pip` |
| Ferramenta externa ausente | Veja [FERRAMENTAS.md](FERRAMENTAS.md); integração pode exigir instalação adicional |

Para investigação detalhada, consulte [Checklist](CHECKLIST-DIAGNOSTICO.md) e [Solução de problemas](SOLUCAO-DE-PROBLEMAS.md).

## 10. Segurança

Use somente alvos autorizados. Não publique `authorized_targets.json`, credenciais, relatórios ou arquivos `.env`. Não exponha FastAPI nem Ollama à internet.
