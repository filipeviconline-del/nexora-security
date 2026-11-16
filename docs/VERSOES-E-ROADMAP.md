# Versões e próximas atualizações — Nexora Security

## Versão atual do repositório

**v0.1.0-alpha — código principal e documentação (pré-lançamento)**

Esta identificação se refere ao estágio de publicação do repositório, **não a uma release estável validada**. Arquivos principais do aplicativo, como `main.py` e `chat_page.py`, já estão publicados. Ainda faltam validação de instalação limpa, scripts auxiliares e testes de integração.

### O que está disponível nesta etapa

- Código-fonte principal do aplicativo, incluindo FastAPI e interface web
- README de apresentação e arquitetura proposta
- Guias de instalação para Ubuntu/Debian, Kali/VirtualBox e Windows/WSL2
- Guia de configuração do Ollama e chat local
- Guia de ferramentas de reconhecimento e laboratório seguro
- Central de documentação, checklist de diagnóstico e solução de problemas
- Recomendações de tratamento de erros e observabilidade

### O que ainda não está concluído no GitHub

- Revisão completa e testes do código-fonte publicado
- Publicação e teste dos scripts de instalação
- Teste de instalação limpa em Kali, Ubuntu e WSL2
- Verificação das integrações reais de ferramentas e do modelo local
- Publicação de release com artefatos e notas de versão

## Planejamento de atualizações

As versões abaixo são **metas planejadas**, não datas prometidas nem funcionalidades já entregues.

| Versão planejada | Objetivo | Situação |
|---|---|---|
| **v0.1.0-alpha** | Código principal e documentação inicial | **Atual — pré-lançamento** |
| **v0.2.0-alpha** | Revisar código publicado, arquivos de exemplo e scripts testáveis | Planejada |
| **v0.3.0-beta** | Validar instalação, chat com Ollama e integrações em laboratório | Planejada |
| **v0.4.0-beta** | Melhorar mensagens de erro, logs, testes e experiência de uso | Planejada |
| **v0.5.0-beta** | Autenticação e licenças offline (proposta, ainda não implementada) | Planejada |
| **v1.0.0** | Primeira versão estável, após validação de segurança e documentação | Planejada |

## Critérios para avançar de versão

- Código e documentação correspondem ao mesmo comportamento real
- Dependências e versões mínimas verificadas
- Instalação limpa reproduzível
- Nenhum segredo ou dado privado publicado
- Testes básicos de chat, erros e ferramentas opcionais
- Escopo autorizado e confirmação humana preservados

## Como acompanhar

Consulte o [README principal](../README.md), o [guia de tratamento de erros](TRATAMENTO-DE-ERROS.md) e os commits do repositório.

A numeração acima é editorial e poderá ser ajustada quando o código completo for auditado. Uma **tag ou GitHub Release** só deve ser criada quando houver uma versão correspondente verificável.
