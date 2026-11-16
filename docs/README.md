# Central de documentação — Nexora Security

Bem-vindo à documentação técnica do **Nexora Security**. Use este índice para instalar, operar, diagnosticar e manter seu ambiente.

> **Disponibilidade:** a documentação está publicada, mas o código completo do aplicativo e os scripts citados nos tutoriais ainda precisam ser adicionados ao repositório. Os procedimentos de diagnóstico podem ser utilizados no ambiente local já existente.

## Comece por aqui

| Objetivo | Documento |
|---|---|
| Consultar versão atual e próximas atualizações | **[Versões e roadmap](VERSOES-E-ROADMAP.md)** |
| Instalar no Ubuntu ou Debian | [Instalação Linux](INSTALACAO-LINUX.md) |
| Instalar no Kali / VirtualBox | [Instalação Kali](INSTALACAO-KALI-VM.md) |
| Instalar no Windows 11 / WSL2 | [Instalação Windows](INSTALACAO-WINDOWS.md) |
| Instalar Ollama e configurar o chat | [Configurar Ollama](CONFIGURAR-OLLAMA.md) |
| Instalar e usar ferramentas de reconhecimento | [Ferramentas](FERRAMENTAS.md) |
| Investigar erros e recuperar o ambiente | **[Solução de problemas](SOLUCAO-DE-PROBLEMAS.md)** |
| Fazer verificações rápidas sem alterar o sistema | [Checklist de diagnóstico](CHECKLIST-DIAGNOSTICO.md) |
| Entender a política de erros e logs | [Tratamento de erros](TRATAMENTO-DE-ERROS.md) |

## Ordem sugerida

1. Escolha o guia do seu sistema operacional e instale os pré-requisitos.
2. Verifique Python, ambiente virtual e dependências.
3. Configure Ollama, baixe um modelo e teste a API local.
4. Inicie o FastAPI e abra o chat.
5. Instale as ferramentas opcionais e teste cada uma separadamente.
6. Se algo falhar, comece pelo [checklist](CHECKLIST-DIAGNOSTICO.md) e consulte a [solução de problemas](SOLUCAO-DE-PROBLEMAS.md).

## Convenções

- Comandos em blocos `bash` são para **Linux, Kali ou Ubuntu no WSL2**, salvo indicação em contrário.
- Comandos `powershell` são para **PowerShell do Windows**.
- `127.0.0.1` significa a máquina ou ambiente onde o comando é executado. Em VMs e WSL2, isso exige atenção à rede.
- A porta padrão do Nexora documentada aqui é **8001**; a do Ollama é **11434**.
- Os exemplos de testes de rede usam `127.0.0.1` ou domínios reservados para documentação.
- Os procedimentos não devem ser aplicados a terceiros sem autorização.

## Como registrar um erro

Ao relatar um problema, anote: sistema operacional, versão do Python, comando executado, mensagem exata do erro, porta envolvida, o que era esperado e o que ocorreu. **Remova senhas, tokens, cookies, IPs privados de clientes e outros dados sensíveis antes de compartilhar logs.**

[Voltar ao README principal](../README.md)
