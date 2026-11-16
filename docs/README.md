# Central de documentação — Nexora Security

Documentação do **Nexora Security**, plataforma experimental de apoio à análise de segurança com FastAPI, Ollama e ferramentas de reconhecimento para ambientes autorizados.

> **Estado do projeto:** o código-fonte principal, incluindo `main.py` e `chat_page.py`, está publicado no repositório. A publicação do código **não significa** que exista uma release estável ou instalação limpa validada. Alguns scripts mencionados em versões anteriores da documentação ainda não estão disponíveis.

## 📚 Navegação por assunto

### 01 — Apresentação, versões e condições de uso

| Documento | Conteúdo |
|---|---|
| [README principal](../README.md) | Visão geral, arquitetura, recursos e início rápido |
| [Versões e roadmap](VERSOES-E-ROADMAP.md) | Estado atual, entregas e próximas versões |
| [Licença proprietária](../LICENSE) | Condições de uso e necessidade de autorização |

### 02 — Instalação e configuração

| Documento | Ambiente ou objetivo |
|---|---|
| [Instalação Linux](INSTALACAO-LINUX.md) | Ubuntu e Debian |
| [Instalação Kali](INSTALACAO-KALI-VM.md) | Kali Linux em máquina virtual |
| [Instalação Windows](INSTALACAO-WINDOWS.md) | Windows 11 e WSL2 |
| [Configuração do Ollama](CONFIGURAR-OLLAMA.md) | Modelo local e comunicação com FastAPI |

**Antes de executar comandos de instalação**, confirme se os arquivos e scripts citados realmente existem no repositório. O código principal foi publicado, mas o instalador `scripts/install-linux.sh` ainda não foi confirmado no GitHub.

### 03 — Ferramentas e operação

| Documento | Conteúdo |
|---|---|
| [Ferramentas de reconhecimento](FERRAMENTAS.md) | Dependências, comandos, verificações e laboratórios autorizados |

O uso de qualquer ferramenta deve respeitar o escopo autorizado. Licença de software e autorização de pentest são permissões distintas.

### 04 — Diagnóstico, manutenção e erros

| Documento | Quando usar |
|---|---|
| [Checklist de diagnóstico](CHECKLIST-DIAGNOSTICO.md) | Primeira verificação de ambiente, serviços, portas e dependências |
| [Solução de problemas](SOLUCAO-DE-PROBLEMAS.md) | Sintomas, causas prováveis e correções passo a passo |
| [Tratamento de erros](TRATAMENTO-DE-ERROS.md) | **Proposta técnica** de padronização de erros, logs e observabilidade; não confundir com funcionalidade implementada |

### 05 — Arquitetura e funcionalidades futuras

| Documento | Situação |
|---|---|
| [Arquitetura de autenticação e licenças offline](ARQUITETURA-AUTENTICACAO-LICENCAS.md) | **Planejamento futuro**; não implementado na versão atual |

## 🧭 Sequência recomendada de leitura

1. [README principal](../README.md) e [versões](VERSOES-E-ROADMAP.md) para conhecer o projeto.
2. Guia de instalação correspondente ao seu sistema operacional.
3. [Configuração do Ollama](CONFIGURAR-OLLAMA.md) para testar a IA local.
4. [Ferramentas](FERRAMENTAS.md) para preparar integrações opcionais.
5. [Checklist](CHECKLIST-DIAGNOSTICO.md) e [solução de problemas](SOLUCAO-DE-PROBLEMAS.md) quando houver falhas.
6. Documentos de arquitetura para acompanhar funcionalidades ainda planejadas.

## ⚙️ Convenções técnicas

- Comandos `bash`: Linux, Kali ou Ubuntu no WSL2, salvo indicação contrária.
- Comandos `powershell`: PowerShell do Windows.
- `127.0.0.1`: ambiente local em que o comando é executado; VMs e WSL2 podem exigir ajustes de rede.
- Porta de exemplo do FastAPI: `8001`; porta padrão do Ollama: `11434`.
- Os exemplos de rede devem ser executados somente em laboratórios ou sistemas autorizados.
- Nunca envie `.env`, credenciais, cookies, listas privadas de alvos ou dados de clientes para o repositório.

## 🩺 Como relatar problemas

Informe sistema operacional, versão do Python, comando utilizado, erro exato, comportamento esperado e comportamento observado. Remova segredos e dados sensíveis antes de compartilhar logs.

## 🔗 Links principais

- [Código e página inicial](../README.md)
- [Licença](../LICENSE)
- [Roadmap](VERSOES-E-ROADMAP.md)
- [Diagnóstico](CHECKLIST-DIAGNOSTICO.md)
- [Erros conhecidos](SOLUCAO-DE-PROBLEMAS.md)

---

**Nexora Security** · Documentação em evolução · Uso em escopo autorizado
