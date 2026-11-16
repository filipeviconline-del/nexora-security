# Ollama no Nexora Security — instalação, configuração e diagnóstico

Este guia explica como habilitar o botão **Conversar com IA** do Nexora Security em **Kali Linux**, **Ubuntu**, **VirtualBox** e **Windows 11 com WSL2**. O Nexora usa **FastAPI** em `127.0.0.1:8001` e chama a API local do **Ollama** em `127.0.0.1:11434`.

> **Estado atual:** o código principal está publicado na estrutura `nexora/`. A instalação é manual por ambiente virtual; não depende de scripts `scripts/*.sh`. Não exponha as portas 8001/11434 à internet.

## 1. Pré-requisitos

- Kali Linux ou Ubuntu atualizado (no VirtualBox ou computador físico); no Windows 11, Ubuntu instalado no WSL2
- Internet para baixar o modelo, Git e Python 3 com venv
- Recomenda-se 8 GB de RAM para testar o modelo Llama 3.2 3B em CPU; com menos memória pode ficar lento ou falhar
- Projeto Nexora Security clonado, com `main.py`, `nexora/api/chat_assistant.py`, `Modelfile` e `requirements.txt`

### No Kali/Ubuntu

```bash
sudo apt update
sudo apt install -y curl git python3 python3-venv python3-pip
```

### No Windows 11

Abra **PowerShell como Administrador**:

```powershell
wsl --install -d Ubuntu
```

Reinicie se solicitado, crie seu usuário Ubuntu e execute os próximos comandos **dentro do terminal Ubuntu**, não no PowerShell. Confira a versão do WSL:

```powershell
wsl --list --verbose
```

Use WSL2. Se o Ubuntu estiver no WSL1, consulte a documentação da Microsoft antes de continuar.

## 2. Instalar o Ollama

No terminal Linux:

```bash
curl -fsSL https://ollama.com/install.sh -o /tmp/ollama-install.sh
less /tmp/ollama-install.sh
sh /tmp/ollama-install.sh
ollama --version
```

Baixe somente do site oficial e revise o script antes de executar.

### Iniciar o serviço

Em Kali/Ubuntu com systemd:

```bash
sudo systemctl enable --now ollama
systemctl status ollama --no-pager
```

Se `systemctl` não estiver disponível (possível em algumas configurações WSL), abra **outro terminal Linux** e execute:

```bash
ollama serve
```

Mantenha esse terminal aberto. Não inicie duas instâncias do servidor na mesma porta.

Verifique:

```bash
curl -fsS http://127.0.0.1:11434/api/tags
```

Uma resposta JSON com `models` indica que a API responde. Se houver `Connection refused`, o servidor não está ativo ou a porta está diferente.

## 3. Baixar e testar o modelo

```bash
ollama pull llama3.2
ollama list
ollama run llama3.2 "Responda apenas: NEXORA OK"
```

O repositório inclui um `Modelfile`. Se desejar criar um modelo personalizado `nexora-ai`, execute na raiz do projeto:

```bash
cd ~/nexora-security
ollama create nexora-ai -f Modelfile
ollama list
ollama run nexora-ai "Explique o que é reconhecimento passivo."
```

Se a criação do modelo personalizado falhar, mantenha `llama3.2`. Os modelos não são distribuídos junto com o código Git. **Atenção:** alguns módulos ainda têm `linuxsec-ai` como modelo padrão interno, portanto defina `OLLAMA_MODEL` explicitamente para o modelo instalado.

## 4. Preparar o backend FastAPI

No terminal Linux, na pasta do projeto completo:

```bash
cd ~/nexora-security
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -c "from main import app; print('NEXORA: IMPORTAÇÃO OK')"
export PATH="$HOME/go/bin:$PATH"
export OLLAMA_MODEL=llama3.2
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```

Se tiver criado e testado o modelo personalizado, poderá usar `export OLLAMA_MODEL=nexora-ai` no lugar de `llama3.2`.

**Importante:** `OLLAMA_MODEL` é lida pelo backend publicado. Sempre defina a variável na sessão em que inicia o Uvicorn. O endereço local esperado é `http://127.0.0.1:11434`. Definir `OLLAMA_URL` só terá efeito se o backend efetivamente ler essa variável.

Não use `--reload` para disponibilização pública. Não altere o host para `0.0.0.0` sem proteção de rede e autenticação.

## 5. Abrir o chat

- Kali/Ubuntu com navegador: **http://127.0.0.1:8001/chat**
- Windows 11 com Nexora no WSL2: abra **http://localhost:8001/chat** no navegador do Windows
- Ubuntu Server sem navegador: use o navegador de uma sessão local apropriada ou um túnel SSH autenticado; não exponha a porta publicamente

Na interface, use **Conversar com IA** (não **Preparar plano**). Experimente:

> Explique a diferença entre reconhecimento passivo e ativo.

A consulta de inventário de ferramentas pode ser respondida pelo registro local, sem chamar o Ollama; por isso, para testar a IA, faça uma pergunta conceitual.

## 6. Diagnóstico por camadas

Execute **no mesmo ambiente Linux onde o FastAPI roda**:

```bash
# Serviço Ollama
curl -fsS http://127.0.0.1:11434/api/tags

# Modelo escolhido
ollama list

# Teste direto da API de chat
curl -fsS http://127.0.0.1:11434/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"model":"llama3.2","messages":[{"role":"user","content":"Diga OK"}],"stream":false}'

# FastAPI / interface
curl -I http://127.0.0.1:8001/chat
```

O teste de API usa `llama3.2`; altere para `nexora-ai` se esse for o único modelo instalado. Alguns servidores respondem a `HEAD` com 405 mesmo quando `GET` funciona; nesse caso, teste:

```bash
curl -fsS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8001/chat
```

### Problemas frequentes

| Sintoma | Possível causa | Verificação/ação |
|---|---|---|
| `ollama: command not found` | Ollama não instalado ou fora do PATH | `command -v ollama`; reinstale pela fonte oficial |
| `Connection refused` na porta 11434 | Servidor Ollama parado | `systemctl status ollama` ou `ollama serve` |
| `model not found` | Modelo solicitado não existe | `ollama list`; `ollama pull llama3.2` ou `ollama create nexora-ai -f Modelfile` |
| Chat retorna 503 | Backend não consegue conversar com Ollama | Teste `/api/tags` e `/api/chat` na mesma VM/WSL |
| Nexora não abre na porta 8001 | FastAPI parado, porta ocupada ou erro Python | Veja o terminal do Uvicorn; `ss -ltnp | grep 8001` |
| VM muito lenta | CPU/RAM insuficientes para inferência | Aumente recursos se possível; teste um modelo menor |
| Funciona no Linux mas não no navegador Windows | Problema de encaminhamento localhost WSL2 | Teste `curl` dentro do WSL e confira a rede WSL2 |
| Inventário responde mas outras perguntas não | Inventário usa resposta local, Ollama indisponível | Teste uma pergunta conceitual e a API Ollama |

## 7. Boas práticas

- Mantenha Ollama e FastAPI acessíveis somente localmente
- Nunca compartilhe senhas, tokens, relatórios ou listas privadas de alvos
- Use ferramentas de reconhecimento somente em ambientes com autorização explícita
- Para acesso remoto, use VPN e autenticação antes de considerar qualquer exposição do sistema
- O desempenho do modelo local depende de RAM, CPU e eventual GPU disponível

## 8. Referências oficiais

- [Ollama — download Linux](https://ollama.com/download/linux)
- [Ollama — documentação](https://docs.ollama.com/)
- [Microsoft — instalar WSL](https://learn.microsoft.com/windows/wsl/install)
- [Kali Linux — downloads oficiais](https://www.kali.org/get-kali/)
