import os, re, json, urllib.request
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title='Nexora Security', version='0.1.0')
@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse(url="/chat", status_code=307)
class Analysis(BaseModel):
    request: str = Field(max_length=30000)
    response: str = Field(default='', max_length=60000)
    use_ai: bool = False

RULES = [
 ('Cookie sem HttpOnly', r'(?im)^set-cookie:(?![^\r\n]*httponly)', 'Verifique se cookies de sessão precisam de HttpOnly.'),
 ('Cookie sem Secure', r'(?im)^set-cookie:(?![^\r\n]*;\s*secure(?:;|\s|$))', 'Confirme uso de HTTPS e atributo Secure.'),
 ('Possível ausência de CSP', None, 'Avalie uma política Content-Security-Policy apropriada.'),
 ('Possível ausência de HSTS', None, 'Verifique Strict-Transport-Security em respostas HTTPS.'),
]

def redact(s):
    s = re.sub(r'(?im)^(authorization|cookie|set-cookie|proxy-authorization|x-api-key):[^\r\n]*', r'\1: [REDACTED]', s)
    s = re.sub(r'(?i)(access_token|refresh_token|id_token|client_secret|password|code)=([^&\s]+)', r'\1=[REDACTED]', s)
    return s

@app.get('/analyzer', response_class=HTMLResponse)
def home():
    return '''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Nexora Security</title><style>body{background:#0b1220;color:#e6f7f7;font:16px system-ui;max-width:1000px;margin:30px auto;padding:16px}h1{color:#00d9d0}textarea{width:100%;box-sizing:border-box;background:#142a3b;color:white;border:1px solid #456;padding:12px;border-radius:8px}button{background:#35e4a0;border:0;padding:12px 20px;border-radius:8px;font-weight:bold;cursor:pointer}pre{white-space:pre-wrap;background:#142a3b;padding:16px;border-radius:8px}</style><h1>Nexora Security — Web Pentest Copilot</h1><p>Análise passiva de HTTP para laboratórios autorizados. Remova segredos antes de colar.</p><label>Requisição HTTP</label><textarea id="req" rows="9" placeholder="GET / HTTP/1.1&#10;Host: lab.local"></textarea><p>Resposta HTTP</p><textarea id="res" rows="9" placeholder="HTTP/1.1 200 OK"></textarea><p><label><input id="ai" type="checkbox"> Consultar Ollama local (opcional)</label></p><button onclick="analyze()">Analisar</button><pre id="out">Aguardando análise...</pre><script>async function analyze(){const out=document.getElementById('out');out.textContent='Analisando...';try{const r=await fetch('/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({request:document.getElementById('req').value,response:document.getElementById('res').value,use_ai:document.getElementById('ai').checked})});out.textContent=JSON.stringify(await r.json(),null,2)}catch(e){out.textContent=String(e)}}</script></html>'''

@app.post('/analyze')
def analyze(body: Analysis):
    req, res = redact(body.request), redact(body.response)
    findings=[]
    # Identificação de referências diretas a objetos
    if re.search(
        r'(?i)/(usuarios|users|accounts|profiles)/\d+',
        req
    ):
        findings.append({
            'observacao': 'Referência direta a objeto identificada',
            'categoria': 'Possível IDOR/BOLA',
            'status': 'hipótese não confirmada',
            'recomendacao': (
                'Verificar se o usuário autenticado possui '
                'autorização para acessar este recurso.'
            )
        })
    for name, pattern, advice in RULES:
        if pattern and re.search(pattern, res):
            findings.append({'observacao':name,'recomendacao':advice,'status':'requer validação'})
    headers = res.lower()
    if res and 'content-security-policy:' not in headers:
        findings.append({'observacao':'CSP não observada nesta resposta','status':'requer contexto'})
    if res and 'strict-transport-security:' not in headers:
        findings.append({'observacao':'HSTS não observado nesta resposta','status':'requer contexto HTTPS'})
    result={'achados':findings,'aviso':'Indícios não comprovam vulnerabilidade. Nenhum teste ativo foi executado.'}
    if body.use_ai:
        prompt = ('Você é um tutor de pentest web em laboratório autorizado. Analise somente os dados fornecidos. '
                  'Não afirme exploração confirmada sem evidência. Sugira verificações manuais seguras. '
                  'Não execute comandos. Responda em português.\nRequisição:\n'+req[:12000]+'\nResposta:\n'+res[:16000])
        payload=json.dumps({'model':os.getenv('OLLAMA_MODEL','llama3.2'),'prompt':prompt,'stream':False}).encode()
        try:
            request=urllib.request.Request('http://127.0.0.1:11434/api/generate',data=payload,headers={'Content-Type':'application/json'})
            with urllib.request.urlopen(request,timeout=90) as response:
                result['analise_ia']=json.load(response).get('response','')
        except Exception as exc:
            result['erro_ia']='Ollama indisponível ou modelo não instalado: '+type(exc).__name__
    return result
from nexora.api.nmap_engine import router as nmap_router

app.include_router(nmap_router)
from nexora.web.dashboard import router as dashboard_router

app.include_router(dashboard_router)

# Nexora Security Chat v5 integration
from nexora.api.security_chat import router as security_chat_router
from nexora.web.chat_page import router as chat_page_router
app.include_router(security_chat_router)
app.include_router(chat_page_router)

from nexora.api.grep_engine import router as grep_router
app.include_router(grep_router)

# Nexora Tool Registry v1
from nexora.core.tool_registry import router as registry_router
app.include_router(registry_router)
# Nexora read-only Ollama conversational chat
from nexora.api.chat_assistant import router as chat_assistant_router
app.include_router(chat_assistant_router)
