"""Consultas DNS passivas, apenas para domínios cadastrados no escopo."""
from datetime import datetime, timezone
import ipaddress
import threading
import time

import dns.exception
import dns.resolver
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from nmap_engine import LOCK, read_targets, normalize_host

router = APIRouter(prefix='/tools', tags=['DNS Recon'])
TYPES = ('A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME')
_QUERY_LOCK = threading.Lock()
_LAST_QUERY = {}

class DNSRequest(BaseModel):
    target: str = Field(min_length=3, max_length=253)

def query_records(domain):
    resolver = dns.resolver.Resolver(configure=True)
    resolver.timeout = 2.0
    resolver.lifetime = 4.0
    output = {}
    for record_type in TYPES:
        try:
            answers = resolver.resolve(domain, record_type, search=False, raise_on_no_answer=False)
            if answers.rrset is None:
                output[record_type] = {'records': [], 'status': 'sem resposta'}
                continue
            records = []
            for record in list(answers)[:30]:
                value = record.to_text()
                if record_type == 'TXT':
                    value = value[:1024]
                records.append(value[:1024])
            output[record_type] = {'records': records, 'ttl': answers.rrset.ttl, 'status': 'ok'}
        except dns.resolver.NXDOMAIN:
            output[record_type] = {'records': [], 'status': 'domínio inexistente'}
        except dns.resolver.NoAnswer:
            output[record_type] = {'records': [], 'status': 'sem resposta'}
        except dns.resolver.NoNameservers:
            output[record_type] = {'records': [], 'status': 'servidor DNS indisponível'}
        except dns.exception.Timeout:
            output[record_type] = {'records': [], 'status': 'tempo esgotado'}
        except dns.exception.DNSException:
            output[record_type] = {'records': [], 'status': 'erro DNS'}
    return output

@router.post('/dns-recon')
def dns_recon(body: DNSRequest):
    domain, is_ip = normalize_host(body.target)
    if is_ip:
        raise HTTPException(status_code=400, detail='Selecione um domínio, não um endereço IP.')
    with LOCK:
        authorized = any(item['ip'] == domain for item in read_targets())
    if not authorized:
        raise HTTPException(status_code=403, detail='Domínio não cadastrado no escopo autorizado.')
    # Limite simples por domínio para evitar consultas repetidas acidentais.
    with _QUERY_LOCK:
        now = time.monotonic()
        if now - _LAST_QUERY.get(domain, -1000) < 15:
            raise HTTPException(status_code=429, detail='Aguarde 15 segundos antes de consultar novamente este domínio.')
        _LAST_QUERY[domain] = now
    return {
        'tool': 'dns-recon',
        'target': domain,
        'queried_at': datetime.now(timezone.utc).isoformat(),
        'records': query_records(domain),
        'notice': 'Consultas DNS públicas; resultados não comprovam vulnerabilidades.'
    }
