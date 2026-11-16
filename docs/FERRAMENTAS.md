# 🧰 Ferramentas de reconhecimento — instalação e uso (Linux e Windows)

Este guia é voltado a **laboratórios próprios e ativos com autorização expressa**. Ele ensina a instalar, verificar e executar exemplos **não intrusivos** das ferramentas que podem apoiar o Nexora Security. A presença de uma ferramenta no computador **não significa** que sua integração ao Nexora já esteja implementada.

> **Status do projeto:** o código-fonte completo do Nexora e os scripts de instalação ainda não foram publicados neste repositório. Os exemplos abaixo são executados **diretamente no terminal**. Para o Windows, prefira **WSL2 com Ubuntu**; os comandos Linux rodam dentro do WSL, não no PowerShell.

## 1. Escolha o ambiente

| Sistema | Caminho recomendado | Observação |
|---|---|---|
| Ubuntu / Debian | Terminal Linux nativo | `apt` + ferramentas Go/Python |
| Kali Linux | Terminal da VM ou instalação nativa | Algumas ferramentas já vêm instaladas; confira antes |
| Windows 11 | [WSL2 com Ubuntu](INSTALACAO-WINDOWS.md) | Mais compatível com ferramentas Linux |
| Windows sem WSL2 | Instalação nativa caso a ferramenta ofereça | Nem todos os recursos ou comandos são equivalentes |

### Preparar Linux ou WSL2

```bash
sudo apt update
sudo apt install -y git curl wget ca-certificates unzip jq python3 python3-pip python3-venv \
  golang-go nmap whois dnsutils
```

Verifique:

```bash
python3 --version
go version
nmap --version
```

> Para ferramentas Go, a versão do Go fornecida pelo sistema pode estar desatualizada. Se a instalação falhar por versão mínima, instale uma versão compatível seguindo [go.dev/dl](https://go.dev/dl/), sem misturar binários antigos e novos no PATH.

Adicione binários Go ao PATH na sessão:

```bash
export PATH="$HOME/go/bin:$PATH"
```

Para persistir no Bash:

```bash
grep -qxF 'export PATH="$HOME/go/bin:$PATH"' ~/.bashrc || \
  echo 'export PATH="$HOME/go/bin:$PATH"' >> ~/.bashrc
```

## 2. Ferramentas: o que fazem e como instalar

| Ferramenta | Finalidade | Instalação recomendada |
|---|---|---|
| **Nmap** | Descoberta de portas e serviços em alvos autorizados | `sudo apt install nmap` |
| **WHOIS** | Consultar informações públicas de registro | `sudo apt install whois` |
| **dig / nslookup** | Consultas DNS | `sudo apt install dnsutils` |
| **WhatWeb** | Identificar tecnologias web a partir de respostas HTTP | `sudo apt install whatweb` (quando disponível) |
| **theHarvester** | Agregar informações públicas de fontes configuradas | Preferir pacote do Kali ou [repositório oficial](https://github.com/laramies/theHarvester) |
| **Subfinder** | Enumerar subdomínios por fontes passivas | `go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest` |
| **Amass** | Mapear superfície de ataque / DNS | [OWASP Amass](https://github.com/owasp-amass/amass) — consultar releases e requisitos |
| **dnsx** | Consultas e validação DNS | `go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest` |
| **httpx** (ProjectDiscovery) | Verificar respostas HTTP de hosts em escopo | `go install github.com/projectdiscovery/httpx/cmd/httpx@latest` |
| **Katana** | Rastreamento de páginas web autorizadas | `go install github.com/projectdiscovery/katana/cmd/katana@latest` |
| **gau** | Coletar URLs conhecidas de fontes públicas | `go install github.com/lc/gau/v2/cmd/gau@latest` |
| **crt.sh** | Pesquisa pública de certificados TLS | Site/API em [crt.sh](https://crt.sh/) — **não é comando de terminal por padrão** |
| **Shodan** | Busca em dados indexados de dispositivos | [shodan.io](https://www.shodan.io/) — API/CLI podem exigir conta/chave |
| **Maltego** | Análise visual de relações | [maltego.com](https://www.maltego.com/) — aplicativo com termos/licenças próprios |
| **Google Dorks** | Pesquisa avançada de páginas públicas | Operadores do Google; não requer instalação |

Algumas fontes OSINT exigem chave de API, assinatura, cadastro ou impõem limites. Não inclua chaves no GitHub.

### Instalar ferramentas Go

```bash
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/lc/gau/v2/cmd/gau@latest
```

Verifique os binários:

```bash
for tool in subfinder dnsx httpx katana gau; do
  printf '%-12s ' "$tool"
  command -v "$tool" || echo "não encontrado"
done
```

**Atenção:** existem outros programas chamados `httpx` (por exemplo, o cliente Python). Para evitar confusão, confirme `httpx -version` e a documentação do ProjectDiscovery.

### Windows 11 com WSL2

No **PowerShell como administrador**:

```powershell
wsl --install -d Ubuntu
```

Reinicie se necessário e abra o **Ubuntu** pelo menu Iniciar. Execute nele as seções Linux acima. Não use `sudo apt` no PowerShell.

Se precisar de Nmap nativo no Windows, obtenha o instalador em [nmap.org/download](https://nmap.org/download) e siga as instruções oficiais. Para o Nexora rodando no WSL2, prefira ferramentas instaladas no **mesmo Ubuntu WSL2**.

## 3. Laboratório seguro para aprender

Use como alvo principal `127.0.0.1`, que representa seu próprio computador. Para testar HTTP, crie um servidor local simples:

```bash
mkdir -p ~/nexora-lab-http
printf '<h1>Laboratorio Nexora</h1>\n' > ~/nexora-lab-http/index.html
cd ~/nexora-lab-http
python3 -m http.server 8080 --bind 127.0.0.1
```

Mantenha esse terminal aberto e use **outro terminal** para os exemplos. Acesse `http://127.0.0.1:8080` no navegador da mesma máquina.

## 4. Exemplos de uso por ferramenta

### Nmap — descobrir serviço local

```bash
nmap -sT -p 8080 127.0.0.1
```

Observe a coluna **STATE**. Se aparecer `open`, há um serviço aceitando conexões nessa porta. Se estiver `closed`, confirme se o servidor Python está rodando.

### dig — consulta DNS pública

```bash
dig example.com A +short
dig example.com MX +short
```

`A` retorna endereços IPv4; `MX` retorna servidores de e-mail. `example.com` é domínio reservado para documentação.

### WHOIS — dados de registro

```bash
whois example.com
```

Os dados disponíveis variam conforme o registro e políticas de privacidade. WHOIS não informa vulnerabilidades.

### WhatWeb — tecnologias do servidor HTTP local

```bash
whatweb http://127.0.0.1:8080
```

Mostra indícios de servidor e tecnologia HTTP. Resultados são pistas, não confirmação de vulnerabilidades.

### httpx — resposta HTTP do laboratório

```bash
printf 'http://127.0.0.1:8080\n' | httpx -silent -status-code -title
```

Use o **httpx do ProjectDiscovery**, não o pacote Python de mesmo nome.

### Katana — descobrir links na página local

```bash
katana -u http://127.0.0.1:8080 -d 1 -silent
```

O servidor local de exemplo tem apenas uma página simples, então o resultado pode ser curto.

### Subfinder — subdomínios passivos

```bash
subfinder -d example.com -silent
```

O domínio `example.com` é reservado e provavelmente não retornará subdomínios. Para resultados úteis, use **um domínio próprio ou explicitamente autorizado**, respeitando limites das fontes. Subfinder não substitui autorização para interagir com os hosts descobertos.

### dnsx — resolver DNS

```bash
printf 'example.com\n' | dnsx -a -silent
```

### gau — URLs conhecidas publicamente

```bash
gau example.com
```

O resultado depende das fontes externas. A ausência de saída não é necessariamente erro.

### crt.sh — certificados públicos, sem instalar comando

Abra [crt.sh](https://crt.sh/) e pesquise `example.com`. Opcionalmente, consulte a API:

```bash
curl -fsS 'https://crt.sh/?q=example.com&output=json' | jq '.[0:3]'
```

A API pública pode limitar ou atrasar respostas. `crt.sh -d https://...` não é um comando padrão do Kali: `crt.sh` é principalmente um **site/serviço**.

### theHarvester, Amass, Shodan e Maltego

Estas ferramentas exigem atenção à instalação, às fontes de dados e às condições de uso:

- **theHarvester:** consulte `theHarvester -h` após instalar pelo pacote/repositório oficial; selecione apenas fontes permitidas e domínios autorizados.
- **Amass:** consulte `amass -h` e a [documentação oficial](https://github.com/owasp-amass/amass); prefira modo passivo em estudos introdutórios.
- **Shodan:** faça consultas manuais na interface web; API e CLI dependem de conta e permissões.
- **Maltego:** use o aplicativo gráfico e as transformações disponíveis na sua licença; evite inserir dados sensíveis de terceiros.

## 5. Como usar com o Nexora Security

O Nexora pode organizar informações coletadas por ferramentas instaladas, mas **não é seguro presumir que todas as integrações estão prontas**. Quando o código completo estiver publicado:

1. Instale a ferramenta no **mesmo Linux/WSL2** onde o FastAPI executa.
2. Confirme com `command -v nome-da-ferramenta`.
3. Execute um exemplo local deste guia.
4. Inicie o Nexora e verifique quais adaptadores realmente aparecem na interface.
5. Defina explicitamente o escopo autorizado e revise as solicitações antes de executar.
6. Confira evidências e relatórios manualmente.

Não copie comandos da IA diretamente para um shell sem revisar parâmetros, alvos e possíveis efeitos.

## 6. Checklist de diagnóstico

```bash
echo '--- Ambiente ---'
uname -a
python3 --version
go version
echo '--- Ferramentas ---'
for t in nmap whois dig whatweb subfinder amass dnsx httpx katana gau; do
  printf '%-12s %s\n' "$t" "$(command -v "$t" || echo AUSENTE)"
done
echo '--- IA local (opcional) ---'
curl --max-time 3 -fsS http://127.0.0.1:11434/api/tags || echo 'Ollama indisponível'
```

- **`command not found`**: pacote ausente ou diretório fora do `PATH`.
- **Erro de versão Go**: atualize o Go a partir da fonte oficial.
- **Sem resultados em OSINT**: verifique fonte, conectividade, limites e permissões; nem toda consulta tem resultado.
- **`Connection refused` no laboratório**: servidor HTTP local não está ativo.
- **Ferramenta funciona no terminal, mas não no Nexora**: integração ainda pode não estar implementada; confira os adaptadores do projeto.

## 7. Segurança e privacidade

- Use **somente alvos próprios ou com autorização expressa**; até consultas passivas podem ter limites legais/contratuais.
- Não faça varreduras agressivas, autenticação automatizada ou exploração em serviços de terceiros sem escopo formal.
- Nunca publique `.env`, tokens de Shodan, credenciais, relatórios privados ou dados pessoais.
- Mantenha Ollama (`11434`) e Nexora (`8001`) ligados a `127.0.0.1`.
- Atualize ferramentas pelos canais oficiais e revise mudanças de versão.

## 8. Documentação oficial

- [Nmap](https://nmap.org/book/man.html)
- [ProjectDiscovery](https://docs.projectdiscovery.io/)
- [OWASP Amass](https://github.com/owasp-amass/amass)
- [theHarvester](https://github.com/laramies/theHarvester)
- [gau](https://github.com/lc/gau)
- [Go](https://go.dev/doc/install)
- [WSL2](https://learn.microsoft.com/windows/wsl/install)
- [Ollama e chat Nexora](CONFIGURAR-OLLAMA.md)
