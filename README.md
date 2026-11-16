# Nexora Security

Plataforma experimental de assistência à análise de segurança com **FastAPI**, **Ollama local** e ferramentas de reconhecimento para laboratórios e ativos expressamente autorizados.

> **Status:** protótipo de laboratório. Não está preparado para hospedagem pública ou uso multiusuário.

## Instalação

- [Kali Linux / VirtualBox](docs/INSTALACAO-KALI-VM.md)
- [Windows 11 / WSL2](docs/INSTALACAO-WINDOWS.md)
- [Ubuntu / Debian](docs/INSTALACAO-LINUX.md)
- **[Configurar Ollama e fazer o chat funcionar](docs/CONFIGURAR-OLLAMA.md)**

Após baixar o código completo:

```bash
bash scripts/install-linux.sh
bash scripts/check.sh
bash scripts/start.sh
```

Acesse http://127.0.0.1:8001/chat. Os recursos de IA exigem Ollama e o modelo local configurados.

## Recursos

- Chat de apoio à análise de segurança
- Planejamento e aprovação explícita de verificações
- Integrações com ferramentas de reconhecimento, sujeitas à instalação local
- Relatórios e evidências de análises autorizadas

## Segurança

Não exponha as portas 8001 ou 11434 à internet. Não envie segredos, relatórios, logs ou listas privadas de alvos ao repositório. A descoberta de um host não constitui autorização para testá-lo.

## Estado da publicação

A documentação inicial está sendo preparada. O código completo e os instaladores devem ser conferidos e enviados antes de usar os comandos de instalação.

## Licença

A definir pelo autor.