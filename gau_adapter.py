"""GAU passive URL-history collection for one explicitly registered domain."""
import ipaddress
import re
import shutil
import subprocess
from urllib.parse import urlsplit

HOST = re.compile(r'^(?=.{1,253}$)[a-z0-9-]+(?:\.[a-z0-9-]+)+$', re.I)

def run_gau(host, is_ip, entry):
    if is_ip or not HOST.fullmatch(host) or entry.get('ip') != host:
        return {'status': 'blocked', 'error': 'Somente dominio explicitamente cadastrado.'}
    binary = shutil.which('gau')
    if not binary:
        return {'status': 'missing', 'error': 'gau nao encontrado no PATH.'}
    # GAU only queries third-party URL indexes; it does not fetch returned URLs.
    cmd = [binary, '--providers', 'wayback,commoncrawl', '--threads', '1',
           '--timeout', '10', '--retries', '1', host]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=55)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {'status': 'error', 'error': str(exc)[:250]}
    found, seen = [], set()
    for line in p.stdout.splitlines()[:3000]:
        url = line.strip()
        try:
            parsed = urlsplit(url)
            if parsed.scheme not in ('http', 'https') or parsed.hostname != host:
                continue
            # Drop credentials, query strings, fragments; avoid sensitive data in AI reports.
            path = parsed.path or '/'
            safe = f'{parsed.scheme}://{host}{path[:300]}'
            if safe not in seen:
                seen.add(safe)
                found.append(safe)
            if len(found) >= 150:
                break
        except ValueError:
            continue
    return {'status': 'ok' if p.returncode == 0 else 'error',
            'tool': 'gau', 'target': host, 'providers': ['wayback', 'commoncrawl'],
            'urls': found, 'count': len(found), 'truncated': len(found) >= 150,
            'stderr': p.stderr[-350:] if p.returncode else '',
            'notice': 'URLs historicas publicas, nao verificadas nem acessadas. Somente hostname cadastrado; subdominios excluidos. Ausencia de URLs nao comprova ausencia de endpoints.'}
