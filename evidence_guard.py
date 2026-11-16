"""Deterministic, read-only evidence extraction. Never executes tools."""
import re

PORT = re.compile(r'^[ \t]*(\d{1,5})/(tcp|udp)[ \t]+(open\|filtered|closed\|filtered|open|closed|filtered|unfiltered)[ \t]+([^\s]+)(?:[ \t]+([^\r\n]*))?$', re.M)

def extract(results):
    results = results if isinstance(results, dict) else {}
    out = {'executed_tools': list(results), 'tool_status': {}, 'ports': [], 'port_counts': {}, 'subdomains': {}, 'limitations': []}
    for tool, data in results.items():
        if not isinstance(data, dict):
            out['tool_status'][tool] = 'unknown'
            continue
        status = str(data.get('status', 'unknown'))
        out['tool_status'][tool] = status
        if status not in ('completed', 'ok', 'success'):
            out['limitations'].append(f'{tool}: status {status}; não interpretar como coleta bem-sucedida.')
        if tool == 'nmap':
            for match in PORT.finditer(str(data.get('stdout') or '')):
                port = int(match.group(1))
                if not 1 <= port <= 65535: continue
                out['ports'].append({'port': port, 'protocol': match.group(2), 'state': match.group(3), 'service': match.group(4), 'details': (match.group(5) or '')[:180]})
            for p in out['ports']:
                out['port_counts'][p['state']] = out['port_counts'].get(p['state'], 0) + 1
            if not out['ports']:
                out['limitations'].append('Nmap: nenhuma linha de porta reconhecida; isso não prova ausência de portas abertas.')
        if tool in ('subfinder', 'amass'):
            names = data.get('subdomains', [])
            if isinstance(names, list):
                out['subdomains'][tool] = [x for x in names[:500] if isinstance(x, str)]
            else:
                out['limitations'].append(f'{tool}: campo subdomains ausente ou inválido.')
    return out
