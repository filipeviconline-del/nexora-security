"""WhatWeb direct, low-impact, only after scope approval by Security Chat."""
from pathlib import Path
import os
import subprocess

from tool_registry import candidates, probe


def run_whatweb(host, entry, approved_ip, safe_web_target):
    # This function must only be called by the approved /tools/chat/run flow.
    safe_web_target(host, False, entry)
    ready = next((item for item in (
        probe('whatweb', path, ['--version']) for path in candidates('whatweb')
    ) if item['status'] == 'READY'), None)
    if not ready:
        return {'status': 'unavailable', 'detail': 'Nenhum executável WhatWeb funcional.'}
    # No user-provided flags, redirects or aggressive plugin levels.
    argv = [ready['path'], '--aggression=1', '--follow-redirect=never',
            '--max-threads=1', f'https://{host}/']
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=35,
                           check=False, stdin=subprocess.DEVNULL,
                           env={**os.environ, 'LC_ALL': 'C.UTF-8'})
        # Check DNS again after scan; fail closed if it changed during execution.
        approved_ip(host, False, entry)
        return {'status': 'completed' if p.returncode == 0 else 'failed',
                'mode': 'WhatWeb real HTTPS (aggression 1, sem redirects)',
                'tool': 'whatweb', 'binary': ready['path'],
                'stdout': p.stdout[:20000], 'stderr': p.stderr[:2000],
                'exit_code': p.returncode,
                'notice': 'A consulta DNS foi validada antes e depois, mas a conexão direta do WhatWeb não fixa o IP: use apenas em laboratórios/alvos com DNS confiável. Resultados não confirmam vulnerabilidades.'}
    except subprocess.TimeoutExpired:
        return {'status': 'timeout', 'detail': 'WhatWeb excedeu 35 segundos.'}
    except OSError as exc:
        return {'status': 'failed', 'detail': type(exc).__name__}
