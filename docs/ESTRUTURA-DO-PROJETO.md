# Estrutura de código do Nexora Security

Os módulos Python estão organizados em `nexora/api/`, `nexora/core/`, `nexora/recon/` e `nexora/web/`.

O arquivo `main.py` permanece na raiz, com o mesmo comando de execução:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```

A reorganização preserva o HTML/JavaScript original e atualiza imports Python. `Modelfile` permanece na raiz. Esta branch deve ser validada antes de integrar à `main`.

```bash
python3 -m compileall -q main.py nexora
python3 -m pip install -r requirements.txt
```

Teste também `/chat`, `/dashboard`, `/analyzer` e `/tools/*` em ambiente de laboratório. Não publique `authorized_targets.json` ou dados privados.
