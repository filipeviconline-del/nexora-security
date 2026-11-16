# Solução de problemas — Nexora Security

Este manual contém sintomas, diagnóstico, correções e critérios de validação. **Comece pelo [checklist](CHECKLIST-DIAGNOSTICO.md)**. Os procedimentos consideram a instalação local em Linux, Kali ou Ubuntu/WSL2.

> Não execute comandos destrutivos como `rm -rf`, não altere permissões indiscriminadamente e não exponha serviços na internet para tentar corrigir um problema local.

## Índice rápido

| Código | Sintoma | Área |
|---|---|---|
| [ERR-001](#err-001--no-module-named-uvicorn) | `No module named uvicorn` | Python |
| [ERR-002](#err-002--porta-8001-em-uso) | Porta 8001 ocupada | FastAPI |
| [ERR-003](#err-003--ollama-indisponível-ou-connection-refused) | Ollama não responde | IA |
| [ERR-004](#err-004--modelo-ollama-não-encontrado) | `model not found` | IA |
| [ERR-005](#err-005--chat-abre-mas-a-ia-não-responde) | Chat abre, mas IA falha | Integração |
| [ERR-006](#err-006--ferramenta-não-encontrada) | `command not found` | Ferramentas |
| [ERR-007](#err-007--go-antigo-ou-binário-fora-do-path) | Go incompatível / PATH | Ferramentas |
| [ERR-008](#err-008--windows-wsl2-não-acessa-a-interface) | Windows não abre chat | Rede |
| [ERR-009](#err-009--pip-externally-managed-environment) | `externally-managed-environment` | Python |
| [ERR-010](#err-010--sem-espaço-ou-memória) | Falta de recursos | Sistema |
| [ERR-011](#err-011--falha-de-dns-ou-internet) | Falha de DNS / internet | Rede |
| [ERR-012](#err-012--clone-de-repositório-privado-falha) | `git clone` negado | GitHub |
| [ERR-013](#err-013--virtualbox-rede-ou-mouse) | VM sem rede / mouse | VirtualBox |
| [ERR-014](#err-014--redis-ssl-connect-failed) | Redis TLS falha | Integração opcional |

## ERR-001 — No module named uvicorn

**Sintoma:** `/usr/bin/python3: No module named uvicorn`.

**Causa provável:** execução pelo Python do sistema, ambiente virtual desativado ou dependências não instaladas.

**Diagnóstico:**

```bash
pwd
test -d .venv && echo "venv presente"
python3 -m pip --version
```

**Correção**, na raiz do projeto que contenha `requirements.txt`:

```bash
sudo apt install -y python3-venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn --version
```

**Validação:** `python -m uvicorn --version` mostra a versão. Depois inicie `python -m uvicorn main:app --host 127.0.0.1 --port 8001`. Não instale pacotes globalmente com `sudo pip`.

## ERR-002 — Porta 8001 em uso

**Sintoma:** `Address already in use` ou `[Errno 98]`.

**Diagnóstico:**

```bash
ss -ltnp | grep ':8001'
```

**Correção:** se já existe uma instância válida do Nexora, use-a. Caso precise reiniciar, volte ao terminal onde o Uvicorn foi iniciado e pressione `Ctrl+C`. Não mate processos desconhecidos. Só então inicie novamente.

**Validação:**

```bash
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8001/chat
```

## ERR-003 — Ollama indisponível ou Connection refused

**Sintoma:** `curl: (7) Failed to connect` na porta 11434, erro de conexão no chat ou `503`.

**Diagnóstico:**

```bash
command -v ollama
systemctl status ollama --no-pager 2>/dev/null || true
ss -ltnp | grep ':11434' || true
```

**Correção:** em Linux com systemd, `sudo systemctl start ollama`. Se não houver serviço, abra **outro terminal** e execute `ollama serve`. Não inicie duas instâncias simultâneas.

**Validação:**

```bash
curl -fsS http://127.0.0.1:11434/api/tags
```

## ERR-004 — Modelo Ollama não encontrado

**Sintoma:** `model not found`, `404` na API de chat, ou modelo não listado.

**Diagnóstico:** `ollama list` e confira o valor de `OLLAMA_MODEL`.

**Correção:**

```bash
ollama pull llama3.2
export OLLAMA_MODEL=llama3.2
ollama run llama3.2 "Responda OK"
```

Se usar um modelo personalizado `nexora-ai`, crie-o **somente se houver um Modelfile válido**:

```bash
test -f Modelfile && ollama create nexora-ai -f Modelfile
```

**Validação:** o nome exato aparece em `ollama list`. Reinicie o FastAPI no terminal em que exportou `OLLAMA_MODEL`.

## ERR-005 — Chat abre, mas a IA não responde

**Sintoma:** interface carrega, porém a resposta falha, fica em espera ou retorna erro.

**Diagnóstico em camadas:**

```bash
curl -fsS http://127.0.0.1:11434/api/tags
curl --max-time 120 -fsS http://127.0.0.1:11434/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"model":"llama3.2","messages":[{"role":"user","content":"Responda OK"}],"stream":false}'
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8001/chat
```

**Interpretação:** se a API do Ollama falha, resolva o serviço/modelo antes de investigar o Nexora. Se o Ollama responde, mas o chat não, confira o terminal do Uvicorn e a configuração do modelo. **Não presuma que a variável `OLLAMA_URL` é lida pelo backend sem verificar o código.**

**Validação:** uma pergunta conceitual no botão **Conversar com IA** recebe resposta. A resposta local de inventário de ferramentas não prova que o Ollama está funcionando.

## ERR-006 — Ferramenta não encontrada

**Sintoma:** `nmap: command not found`, `whatweb: command not found` ou `subfinder: command not found`.

**Diagnóstico:** `command -v nmap`, `command -v whatweb`, `command -v subfinder`.

**Correção:** para Nmap e WhatWeb, em distribuições com pacotes disponíveis:

```bash
sudo apt update
sudo apt install -y nmap whatweb
```

Para ferramentas Go, consulte [Ferramentas](FERRAMENTAS.md). **Validação:** `command -v nome` retorna caminho. A ferramenta pode ser opcional e não bloquear o chat.

## ERR-007 — Go antigo ou binário fora do PATH

**Sintoma:** `go: ... requires go >= ...` ou instalação concluída sem encontrar comando.

**Diagnóstico:**

```bash
go version
go env GOPATH
echo "$PATH"
ls -la "$HOME/go/bin" 2>/dev/null || true
```

**Correção:** use a versão compatível disponível em [go.dev/dl](https://go.dev/dl/). Na sessão:

```bash
export PATH="$HOME/go/bin:$PATH"
```

**Validação:** `command -v subfinder` e `subfinder -version`. Evite substituir instalações Go existentes sem identificar a versão ativa.

## ERR-008 — Windows WSL2 não acessa a interface

**Sintoma:** o FastAPI funciona no Ubuntu/WSL2, mas `http://localhost:8001/chat` não abre no Windows.

**Diagnóstico:** no Ubuntu, teste `curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8001/chat`. No PowerShell, execute `wsl --list --verbose`.

**Correção:** confirme WSL2 e que o processo está ativo no Ubuntu. Verifique o encaminhamento localhost do WSL e regras locais de rede. Consulte [guia Windows](INSTALACAO-WINDOWS.md). **Não abra `0.0.0.0` nem libere firewall indiscriminadamente.**

**Validação:** a mesma rota responde no navegador Windows.

## ERR-009 — pip externally-managed-environment

**Sintoma:** `error: externally-managed-environment` ao instalar dependências.

**Causa:** proteção do Python gerenciado pela distribuição.

**Correção:**

```bash
sudo apt install -y python3-venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

**Validação:** `python -c "import uvicorn"` funciona. **Não use `--break-system-packages`** como solução padrão.

## ERR-010 — Sem espaço ou memória

**Sintoma:** download de modelo falha, processo encerra sozinho, `No space left on device` ou travamentos.

**Diagnóstico:**

```bash
free -h
df -h /
```

**Correção:** libere espaço com cuidado, feche aplicativos pesados ou use modelo menor. No VirtualBox, ajuste RAM/CPU conforme capacidade do host.

**Validação:** o download termina e o modelo responde a `ollama run llama3.2 "OK"`.

## ERR-011 — Falha de DNS ou internet

**Sintoma:** `Temporary failure in name resolution`, downloads falham ou ferramentas OSINT não retornam resultados.

**Diagnóstico:**

```bash
getent hosts example.com
curl --max-time 10 -I https://example.com
```

**Correção:** confirme conectividade da VM/WSL2, DNS, proxy corporativo e hora do sistema. Não altere `/etc/resolv.conf` sem conhecer a configuração da distribuição/WSL.

**Validação:** a resolução DNS e uma requisição HTTPS autorizada funcionam.

## ERR-012 — Clone de repositório privado falha

**Sintoma:** `Repository not found`, `Authentication failed` ou `Permission denied (publickey)`.

**Diagnóstico:** confira URL, permissões de leitura e método de autenticação.

**Correção:** autentique-se pelo GitHub CLI (`gh auth login`) ou configure uma chave SSH autorizada. Não coloque tokens na URL nem no histórico do shell.

**Validação:** `git ls-remote https://github.com/filipeviconline-del/nexora-security.git HEAD` responde quando autenticado.

## ERR-013 — VirtualBox: rede ou mouse

**Sintoma:** VM sem internet, cursor capturado, dificuldade para sair da tela cheia ou salvar configurações.

**Diagnóstico:** confira estado da VM, adaptador NAT, integração do mouse, Guest Additions e tecla Host configurada em **Arquivo/Ferramentas > Preferências > Entrada** (os nomes variam por versão).

**Correção:** desligue completamente a VM antes de alterar configurações que exigem máquina desligada. Ajuste a tecla Host para uma combinação disponível no teclado. Para mouse Bluetooth, confira se a integração de ponteiro está habilitada; o periférico físico é gerenciado pelo host.

**Validação:** cursor entra e sai da VM e `getent hosts example.com` resolve o domínio. Não dependa de uma tecla Ctrl direita que seu teclado não possui.

## ERR-014 — Redis: SSL_connect failed

**Sintoma:** `SSL_connect failed: record layer failure` ao usar `redis-cli --tls`.

**Diagnóstico:** confirme com o provedor se o endpoint e a porta exigem TLS, a cadeia de certificados e se a rede permite acesso. Verifique `redis-cli --version`.

**Correção:** use **exatamente** o host, a porta, o modo TLS e as credenciais fornecidos pelo serviço; não desative TLS para contornar erros de certificado. Não copie URLs com senha para tickets ou documentação.

**Validação:** uma conexão autorizada retorna `PONG` para `PING`. Redis é uma integração opcional e não faz parte do requisito mínimo do chat Nexora.

---

## Como escalar um problema

Se a correção não funcionar, registre o erro exato, as versões, o resultado do [checklist](CHECKLIST-DIAGNOSTICO.md) e as alterações já tentadas. Evite repetir instalações ou reiniciar processos indiscriminadamente.

[Índice da documentação](README.md)
