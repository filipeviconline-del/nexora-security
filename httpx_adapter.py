"""Bounded ProjectDiscovery httpx check for a single approved hostname."""
import ipaddress
import json
import re
import shutil
import subprocess
from urllib.parse import urlsplit

_HOST = re.compile(r'^(?=.{1,253}$)(?!-)[a-z0-9-]+(?:\.(?!-)[a-z0-9-]+)+$', re.I)


def run_httpx(host, is_ip, entry, approved_ip):
    if is_ip or not _HOST.fullmatch(host) or entry.get('ip') != host:
        return {'status':'blocked', 'error':'Somente dominio explicitamente cadastrado.'}
    pinned = approved_ip(host, is_ip, entry)
    binary = shutil.which('httpx')
    if not binary:
        return {'status':'missing', 'error':'ProjectDiscovery httpx nao encontrado no PATH.'}
    try:
        version = subprocess.run([binary, '-version'], capture_output=True, text=True, timeout=8)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {'status':'error', 'error':str(exc)[:300]}
    banner = (version.stdout + version.stderr).lower()
    if 'projectdiscovery' not in banner and 'httpx' not in banner:
        return {'status':'blocked','error':'Binario httpx nao identificado; confira instalacao ProjectDiscovery.'}
    # Never enumerate subdomains or follow redirects. Restrict to the exact registered hostname.
    # httpx performs its own DNS lookup: revalidate immediately before execution.
    approved_ip(host, is_ip, entry)
    records = []
    for scheme in ('https', 'http'):
        url = f'{scheme}://{host}'
        cmd = [binary, '-u', url, '-json', '-silent', '-no-color', '-status-code',
               '-title', '-tech-detect', '-timeout', '5', '-retries', '0',
               '-threads', '1', '-rl', '1']
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        except (OSError, subprocess.TimeoutExpired) as exc:
            records.append({'input':url, 'error':str(exc)[:300]})
            continue
        for line in proc.stdout.splitlines()[:10]:
            try:
                item = json.loads(line)
            except (ValueError, TypeError):
                continue
            observed = str(item.get('input') or item.get('url') or '')
            parsed = urlsplit(observed if '://' in observed else 'https://' + observed)
            if parsed.hostname != host:
                continue
            # httpx can report a final URL. Do not treat other hosts as authorized.
            final_url = str(item.get('url') or '')
            final_host = urlsplit(final_url).hostname if final_url else host
            records.append({'input':url, 'url':final_url if final_host == host else None,
                            'status_code':item.get('status_code'),
                            'title':str(item.get('title') or '')[:200],
                            'tech':list(item.get('tech') or [])[:30],
                            'webserver':str(item.get('webserver') or '')[:100],
                            'ip':str(item.get('host') or '')[:100],
                            'redirect_to_external_host': final_host != host})
        if proc.returncode != 0 and not proc.stdout.strip():
            records.append({'input':url, 'error':proc.stderr.strip()[:300]})
    return {'status':'ok' if any('status_code' in r for r in records) else 'no_response',
            'tool':'projectdiscovery-httpx', 'target':host, 'approved_ip':pinned,
            'redirects_followed':False, 'results':records[:12],
            'notice':'Resultados informativos; nao comprovam vulnerabilidades. DNS deve permanecer estavel.'}
