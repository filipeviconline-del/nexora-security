# Tratamento de erros e observabilidade — Nexora Security

Este documento define **recomendações para o desenvolvimento**. Não significa que o código atual já implemente todos os comportamentos descritos. A implementação deve ser validada após a publicação do backend.

## Objetivos

1. Mostrar mensagens claras sem revelar dados sensíveis.
2. Registrar erros técnicos com contexto suficiente para diagnóstico.
3. Diferenciar falhas de configuração, dependências, rede, validação e execução.
4. Impedir que uma falha em ferramenta opcional derrube o chat inteiro.
5. Permitir reprodução segura e testes automatizados.

## Modelo de resposta de erro recomendado

Exemplo ilustrativo (não é contrato de API já implementado):

```json
{
  "error": {
    "code": "OLLAMA_UNAVAILABLE",
    "message": "Não foi possível conectar ao serviço de IA local.",
    "request_id": "exemplo-123",
    "retryable": true
  }
}
```

- `code`: identificador estável para documentação e testes.
- `message`: orientação curta para o usuário, sem detalhes internos.
- `request_id`: identificador de correlação entre interface e log.
- `retryable`: indica se tentar novamente pode resolver.

## Taxonomia sugerida

| Código interno | HTTP sugerido | Ação do usuário |
|---|---:|---|
| `VALIDATION_ERROR` | 422 | Corrigir campos ou parâmetros |
| `AUTHORIZATION_REQUIRED` | 403 | Confirmar escopo e autorização |
| `TOOL_NOT_INSTALLED` | 424 | Instalar dependência opcional |
| `TOOL_TIMEOUT` | 504 | Reduzir carga e verificar execução |
| `OLLAMA_UNAVAILABLE` | 503 | Iniciar Ollama |
| `MODEL_NOT_FOUND` | 424 | Baixar/configurar modelo |
| `MODEL_TIMEOUT` | 504 | Verificar RAM/CPU e tempo limite |
| `INTERNAL_ERROR` | 500 | Consultar logs com request ID |

Os códigos HTTP são **proposta de design**, não garantia do comportamento atual.

## Padrões de implementação recomendados

### Backend

- Centralizar tratamento de exceções em FastAPI, preservando exceções HTTP previstas.
- Usar `timeout` explícito para chamadas ao Ollama e subprocessos.
- Capturar `FileNotFoundError` para dependências opcionais ausentes.
- Evitar `except Exception: pass`; registrar exceção e retornar erro controlado.
- Limitar tamanho de entrada, saída e logs; nunca registrar prompts confidenciais por padrão.
- Validar escopo antes de iniciar qualquer ferramenta de rede.
- Não montar comandos com concatenação de shell a partir de entrada do usuário; usar argumentos estruturados e `shell=False`.
- Exibir confirmação humana antes de operações que possam gerar tráfego ou alterar estado.

### Interface

- Mostrar estados: `conectando`, `executando`, `concluído`, `falhou`.
- Informar a dependência que falhou (Ollama, modelo, ferramenta, backend).
- Exibir `request_id` copiável em caso de erro.
- Evitar repetição automática de operações de reconhecimento; para chamadas de IA, aplicar tentativas limitadas quando apropriado.
- Não exibir stack traces ou tokens no navegador.

### Logs

Sugestão de campos: timestamp UTC, nível, componente, código do erro, request ID, duração, resultado e versão da aplicação.

**Nunca registrar:** senhas, tokens, cookies, cabeçalhos Authorization, dados privados de clientes, relatórios integrais ou prompts sensíveis.

Aplicar rotação, retenção curta e permissões restritas. A política exata depende do ambiente.

## Plano de testes

| Cenário | Resultado esperado |
|---|---|
| Ollama desligado | Erro claro, sem travar a interface |
| Modelo ausente | Orientação para `ollama list` / `ollama pull` |
| Ferramenta opcional ausente | Chat permanece disponível |
| Timeout de ferramenta | Processo encerrado de modo controlado |
| Porta FastAPI ocupada | Diagnóstico sem matar outros processos |
| Escopo não autorizado | Execução bloqueada |
| Entrada inválida | Resposta 4xx com orientação |
| Erro inesperado | 500 com ID, sem exposição de stack trace |

## Procedimento de incidente

1. **Identificar:** registre horário, operação e código de erro.
2. **Conter:** interrompa somente a operação afetada; não mate processos desconhecidos.
3. **Diagnosticar:** siga [Checklist](CHECKLIST-DIAGNOSTICO.md) e [Solução de problemas](SOLUCAO-DE-PROBLEMAS.md).
4. **Corrigir:** faça uma mudança por vez, preservando backup.
5. **Validar:** repita o teste que falhou e verifique regressões.
6. **Documentar:** registre causa raiz, correção e prevenção.

[Índice da documentação](README.md)
