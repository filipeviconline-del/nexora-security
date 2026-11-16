"""Bounded DNSx adapter. Call only after scope authorization in security_chat."""
import json
import re
import shutil
import subprocess
import threading
from datetime import datetime, timezone

_LOCK = threading.Lock()
_DOMAIN = re.compile(r'(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$')

def run_dnsx(host, is_ip, entry):
    if is_ip or not _DOMAIN.fullmatch(host.lower()):
        return {'tool':'dnsx','status':'unavailable','detail':'DNSx requer domínio público válido e autorizado.'}
    if not isinstance(entry, dict) or entry.get('ip') != host:
        return {'tool':'dnsx','status':'unavailable','detail':'Entrada de escopo não corresponde ao domínio.'}
    binary = shutil.which('dnsx')
    if not binary:
        return {'tool':'dnsx','status':'unavailable','detail':'Executável dnsx não encontrado.'}
    if not _LOCK.acquire(blocking=False):
        return {'tool':'dnsx','status':'busy','detail':'Consulta DNSx já em andamento.'}
    try:
        args = [binary,'-a','-aaaa','-cname','-mx','-ns','-j','-silent','-t','2','-rl','2','-retry','1','-timeout','3s','-duc']
        try:
            p = subprocess.run(args, input=host+'\n', text=True, capture_output=True,
                               timeout=30, check=False, stdin=subprocess.PIPE)
        except subprocess.TimeoutExpired:
            return {'tool':'dnsx','status':'timeout','target':host,'detail':'Limite de 30 segundos atingido.'}
        except OSError as exc:
            return {'tool':'dnsx','status':'failed','target':host,'detail':type(exc).__name__}
        records=[]
        errors=[]
        for line in p.stdout.splitlines()[:100]:
            try:
                obj=json.loads(line)
            except json.JSONDecodeError:
                errors.append('Linha não JSON descartada')
                continue
            if not isinstance(obj,dict):
                continue
            name=str(obj.get('host','')).lower().rstrip('.')
            if name != host.lower():
                continue
            safe={'host':name}
            for key in ('a','aaaa','cname','mx','ns','status_code','rcode'):
                if key in obj:
                    safe[key]=obj[key]
            records.append(safe)
        return {'tool':'dnsx','status':'completed' if p.returncode==0 else 'failed',
                'target':host,'executed_at':datetime.now(timezone.utc).isoformat(),
                'command':args,'exit_code':p.returncode,'records':records,
                'count':len(records),'stderr':p.stderr[:1500], 'parse_warnings':errors[:5],
                'notice':'Somente domínio cadastrado. Nenhum subdomínio descoberto recebe autorização automática.'}
    finally:
        _LOCK.release()
