"""Bounded passive Amass v5 adapter for explicitly approved Security Chat runs."""
import re
import shutil
import subprocess
import threading
import time
from datetime import datetime, timezone

_LOCK = threading.Lock()
_LAST = {}
COOLDOWN_SECONDS = 60
MAX_RESULTS = 500
DOMAIN_RE = re.compile(r'(?i)^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+$')


def run_amass(host, is_ip, entry):
    if is_ip or not DOMAIN_RE.fullmatch(host) or len(host) > 253:
        return {'tool': 'amass', 'status': 'unavailable', 'detail': 'Amass exige domínio válido cadastrado.'}
    if not isinstance(entry, dict) or entry.get('ip') != host:
        return {'tool': 'amass', 'status': 'denied', 'detail': 'Escopo não confirmado.'}
    binary = shutil.which('amass')
    if not binary:
        return {'tool': 'amass', 'status': 'unavailable', 'detail': 'Amass não encontrado no PATH.'}
    if not _LOCK.acquire(blocking=False):
        return {'tool': 'amass', 'status': 'busy', 'detail': 'Já existe uma enumeração em andamento.'}
    try:
        now = time.monotonic()
        if now - _LAST.get(host, -1e9) < COOLDOWN_SECONDS:
            return {'tool': 'amass', 'status': 'cooldown', 'detail': 'Aguarde 60 segundos.'}
        _LAST[host] = now
        # Passive is the default in Amass v5. No -active, -brute, or scope expansion.
        command = [binary, 'enum', '-d', host, '-rigid', '-norecursive', '-timeout', '2', '-nocolor']
        try:
            proc = subprocess.run(command, capture_output=True, text=True, timeout=145,
                                  check=False, stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            return {'tool': 'amass', 'status': 'timeout', 'detail': 'Tempo máximo de 145 segundos atingido.'}
        except OSError as exc:
            return {'tool': 'amass', 'status': 'failed', 'detail': type(exc).__name__}
        names = set()
        for line in proc.stdout.splitlines():
            candidate = line.strip().lower().rstrip('.')
            if candidate.endswith('.' + host) and len(candidate) <= 253 and DOMAIN_RE.fullmatch(candidate):
                names.add(candidate)
                if len(names) >= MAX_RESULTS:
                    break
        return {
            'tool': 'amass', 'status': 'completed' if proc.returncode == 0 else 'failed',
            'target': host, 'executed_at': datetime.now(timezone.utc).isoformat(),
            'count': len(names), 'subdomains': sorted(names),
            'truncated': len(names) >= MAX_RESULTS, 'exit_code': proc.returncode,
            'stderr': proc.stderr[:2000],
            'stdout_excerpt': proc.stdout[:3000] if not names else '',
            'notice': 'Amass v5 passivo; resultados não autorizam testes ativos nos subdomínios.'
        }
    finally:
        _LOCK.release()
