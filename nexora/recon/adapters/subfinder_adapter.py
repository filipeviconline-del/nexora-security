"""Passive Subfinder adapter; only called by explicitly approved Security Chat runs."""
import re
import subprocess
import threading
import time
from datetime import datetime, timezone
from nexora.core.tool_registry import candidates, probe

_LOCK = threading.Lock()
_LAST = {}
COOLDOWN_SECONDS = 60


def run_subfinder(host, is_ip, entry):
    if is_ip:
        return {'status': 'unavailable', 'detail': 'Subfinder exige domínio autorizado.'}
    ready = next((v for v in (probe('subfinder', p, ['-version']) for p in candidates('subfinder')) if v['status'] == 'READY'), None)
    if ready is None:
        return {'status': 'unavailable', 'detail': 'Subfinder não instalado ou não funcional. Consulte /tools/registry.'}
    if not _LOCK.acquire(blocking=False):
        return {'status': 'busy', 'detail': 'Já existe uma enumeração Subfinder em andamento.'}
    try:
        now = time.monotonic()
        if now - _LAST.get(host, -1e9) < COOLDOWN_SECONDS:
            return {'status': 'cooldown', 'detail': 'Aguarde 60 segundos para consultar novamente este domínio.'}
        _LAST[host] = now
        args = [ready['path'], '-d', host, '-silent', '-timeout', '10', '-max-time', '2', '-rl', '2']
        try:
            proc = subprocess.run(args, capture_output=True, text=True, timeout=145, check=False, stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            return {'status': 'timeout', 'detail': 'Enumeração excedeu 145 segundos.'}
        except OSError as exc:
            return {'status': 'failed', 'detail': type(exc).__name__}
        names = set()
        for raw in proc.stdout.splitlines():
            value = raw.strip().lower().rstrip('.')
            if not value.endswith('.' + host) or len(value) > 253:
                continue
            if all(re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', label) for label in value.split('.')):
                names.add(value)
            if len(names) >= 500:
                break
        return {'tool': 'subfinder', 'status': 'completed' if proc.returncode == 0 else 'failed',
                'target': host, 'executed_at': datetime.now(timezone.utc).isoformat(),
                'count': len(names), 'subdomains': sorted(names), 'truncated': len(names) >= 500,
                'exit_code': proc.returncode, 'stderr': proc.stderr[:2000],
                'notice': 'Consulta passiva a fontes externas. Subdomínios descobertos NÃO são automaticamente autorizados para testes ativos.'}
    finally:
        _LOCK.release()
