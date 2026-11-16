"""Conservative Katana crawler for one explicitly approved domain."""
import ipaddress
import json
import re
import shutil
import subprocess
from urllib.parse import urlsplit

_HOST = re.compile(r'^(?=.{1,253}$)(?!-)[a-z0-9-]+(?:\.(?!-)[a-z0-9-]+)+$', re.I)

def run_katana(host, is_ip, entry, approved_ip):
    if is_ip or not _HOST.fullmatch(host) or entry.get('ip') != host:
        return {'status':'blocked', 'error':'Apenas dominio cadastrado; IP e subdominios descobertos nao autorizados automaticamente.'}
    binary = shutil.which('katana')
    if not binary:
        return {'status':'missing', 'error':'Katana nao encontrado no PATH; confira ~/go/bin.'}
    try:
        pinned = approved_ip(host, is_ip, entry)
        ip = ipaddress.ip_address(pinned)
        if ip.is_link_local or ip.is_multicast or ip.is_unspecified:
            return {'status':'blocked', 'error':'Endereco nao permitido.'}
    except Exception as exc:
        return {'status':'blocked', 'error':str(exc)[:300]}
    # -fs fqdn prevents out-of-host crawling; -d 1 bounds traversal.
    # No headless, JavaScript crawling, form filling, or authentication.
    cmd = [binary, '-u', 'https://' + host, '-d', '1', '-fs', 'fqdn',
           '-silent', '-jsonl', '-c', '1', '-p', '1', '-rl', '1', '-timeout', '5']
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=65)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {'status':'error', 'error':str(exc)[:300]}
    urls = []
    seen = set()
    for line in proc.stdout.splitlines()[:500]:
        try:
            obj = json.loads(line)
        except (ValueError, TypeError):
            continue
        raw = obj.get('url') or (obj.get('request') or {}).get('endpoint') or ''
        if not isinstance(raw, str):
            continue
        parsed = urlsplit(raw)
        if parsed.scheme not in ('http','https') or parsed.hostname != host:
            continue
        # Avoid embedding credentials, fragments, and query values in reports.
        safe_url = f'{parsed.scheme}://{host}{parsed.path or "/"}'
        if safe_url not in seen:
            seen.add(safe_url)
            urls.append(safe_url)
        if len(urls) >= 100:
            break
    return {'status': 'ok' if proc.returncode == 0 else 'error',
            'tool':'projectdiscovery-katana', 'target':host,
            'approved_ip_at_start':pinned, 'depth':1, 'rate_limit_per_second':1,
            'urls':urls, 'count':len(urls),
            'stderr':proc.stderr[-400:] if proc.returncode else '',
            'notice':'Somente URLs do host cadastrado sao exibidas. A resolucao DNS interna do crawler nao esta fixada no IP aprovado; use em dominio proprio com DNS estavel. Nenhum endpoint descoberto recebe autorizacao adicional.'}
