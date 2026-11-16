"""Inventário local, sem rede nem execução de scanners contra alvos."""
from pathlib import Path
import os
import re
import shutil
import subprocess
from fastapi import APIRouter

router = APIRouter(prefix='/tools', tags=['Tool Registry'])

TOOLS = {
    'nmap': ('nmap', ['--version']),
    'whatweb': ('whatweb', ['--version']),
    'subfinder': ('subfinder', ['-version']),
    'amass': ('amass', ['-version']),
    'theHarvester': ('theHarvester', ['-h']),
    'spiderfoot': ('spiderfoot', ['-h']),
    'recon-ng': ('recon-ng', ['-h']),
    'crt.sh': (None, None),
    'dnsx': ('dnsx', ['-version']),
    'httpx': ('httpx', ['-version']),
    'katana': ('katana', ['-version']),
    'gau': ('gau', ['--version']),
}

def candidates(name):
    result = []
    if name == 'whatweb':
        result.append(str(Path.home() / '.local/bin/whatweb-linuxsec'))
    found = shutil.which(name)
    if found:
        result.append(found)
    return list(dict.fromkeys(result))

def probe(name, executable, flags):
    if not executable or not (Path(executable).is_file() and os.access(executable, os.X_OK)):
        return {'name': name, 'status': 'NOT_INSTALLED', 'path': None, 'version': None}
    try:
        p = subprocess.run([executable, *flags], capture_output=True, text=True,
                           timeout=5, check=False, stdin=subprocess.DEVNULL)
        output = (p.stdout + '\n' + p.stderr).strip()
        first = next((line.strip() for line in output.splitlines() if line.strip() and not line.startswith('.$$$')), '')
        # Some CLI tools return 1 for help; only version probes with returncode 0 count as READY.
        good = p.returncode == 0
        return {'name': name, 'status': 'READY' if good else 'BROKEN',
                'path': executable, 'version': first[:180] or None,
                'detail': None if good else f'Exit code {p.returncode}: {output[-250:]}'}
    except subprocess.TimeoutExpired:
        return {'name': name, 'status': 'TIMEOUT', 'path': executable, 'version': None}
    except OSError as exc:
        return {'name': name, 'status': 'BROKEN', 'path': executable,
                'version': None, 'detail': type(exc).__name__}

@router.get('/registry')
def registry():
    items = []
    for name, (binary, flags) in TOOLS.items():
        if name == 'crt.sh':
            items.append({'name': name, 'status': 'EXTERNAL_SERVICE', 'path': None,
                          'version': None, 'detail': 'Serviço web público; conectividade não verificada.'})
            continue
        options = [probe(name, path, flags) for path in candidates(binary)]
        chosen = next((x for x in options if x['status'] == 'READY'), None)
        if not chosen:
            chosen = options[0] if options else {'name': name, 'status': 'NOT_INSTALLED', 'path': None, 'version': None}
        if name == 'whatweb':
            chosen['alternatives'] = [{'path': x['path'], 'status': x['status']} for x in options if x['path'] != chosen['path']]
        items.append(chosen)
    return {'tools': items, 'notice': 'Inventário local de executáveis. READY não comprova integração funcional ao scanner.'}
