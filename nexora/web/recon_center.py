"""Recon Center: painel de orquestração para alvos previamente autorizados."""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/recon", response_class=HTMLResponse)
def recon_center():
    return PAGE

PAGE = r'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Recon Center | Nexora Security</title>
<style>
:root{color-scheme:dark;--bg:#0b1220;--panel:#142a3b;--line:#2b4b5c;--cyan:#00d9d0;--green:#35e4a0;--text:#e6f7f7;--muted:#9ab8c4}
*{box-sizing:border-box}body{background:var(--bg);color:var(--text);font:15px system-ui,sans-serif;margin:0}main{max-width:1150px;margin:auto;padding:28px}header{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:center}h1{margin:10px 0;color:var(--cyan)}h2{font-size:18px}a{color:var(--cyan)}p,small{color:var(--muted)}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:20px;margin:18px 0}.tools{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px}.tool{padding:12px;border:1px solid var(--line);border-radius:10px;background:#102333;display:flex;align-items:center;gap:9px}.tool:has(input:disabled){opacity:.45}select,input,button{font:inherit}select{background:#0b1220;color:var(--text);padding:12px;border:1px solid var(--line);border-radius:8px;max-width:100%;width:100%}button{padding:12px 18px;background:var(--green);color:#092021;border:0;border-radius:9px;font-weight:700;cursor:pointer}button:disabled{opacity:.5;cursor:not-allowed}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#081725;padding:14px;border-radius:9px;max-height:550px;overflow:auto}#status{min-height:24px}.results{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}.result{border:1px solid var(--line);border-radius:10px;padding:14px;min-width:0}.result pre{max-height:310px}label{cursor:pointer}.check{display:flex;gap:9px;align-items:flex-start;margin:15px 0}.muted{color:var(--muted)}.error{color:#ffb4b4}details{margin-top:12px}summary{cursor:pointer;color:var(--cyan)}@media(max-width:600px){main{padding:15px}}
</style></head><body><main>
<header><div><small>NEXORA SECURITY / RECON CENTER</small><h1>Reconhecimento integrado</h1></div><nav><a href="/dashboard">Dashboard</a> · <a href="/chat">Chat</a></nav></header>
<p>Selecione um alvo previamente cadastrado, escolha até 5 ferramentas e autorize explicitamente a execução. Nenhuma descoberta amplia o escopo automaticamente.</p>
<section class="panel"><h2>1. Alvo autorizado</h2><select id="target" aria-label="Alvo autorizado"></select><p id="scope"></p><p><a href="/dashboard#targets">Gerenciar alvos autorizados</a></p></section>
<section class="panel"><h2>2. Ferramentas</h2><p>Disponibilidade depende das ferramentas instaladas. Para IPs, apenas Nmap é permitido nesta orquestração.</p><div class="tools" id="tools"></div>
<label class="check"><input type="checkbox" id="approved"> Confirmo que tenho autorização para executar as ferramentas selecionadas neste alvo e nos IPs associados já cadastrados.</label>
<button id="run" disabled>Executar ferramentas selecionadas</button><p id="status" role="status" aria-live="polite"></p></section>
<section class="panel"><h2>3. Relatório consolidado</h2><p id="meta">Aguardando execução.</p><div class="results" id="results"></div><details id="rawBox" hidden><summary>JSON original da execução</summary><pre id="raw"></pre></details></section>
</main><script>
const names={dns:"DNS",nmap:"Nmap",whatweb:"WhatWeb",subfinder:"Subfinder",amass:"Amass",dnsx:"DNSx",dnsx_brute:"DNSx Brute",httpx:"HTTPx",katana:"Katana",gau:"GAU"};
const order=Object.keys(names),$=id=>document.getElementById(id);let targets=[];
async function request(url,options){const response=await fetch(url,options);const data=await response.json();if(!response.ok)throw Error(typeof data.detail==="string"?data.detail:"Erro HTTP "+response.status);return data}
function domain(target){return !!target && !/^[0-9.]+$/.test(target) && !target.includes(":")}
function selection(){return [...document.querySelectorAll('input[data-tool]:checked')].map(x=>x.value)}
function refresh(){const value=$('target').value,hasDomain=domain(value);document.querySelectorAll('input[data-tool]').forEach(el=>{el.disabled=!hasDomain&&el.value!=="nmap";if(el.disabled)el.checked=false});const chosen=selection();$('run').disabled=!value||!$('approved').checked||chosen.length===0||chosen.length>5;$('scope').textContent=hasDomain?'Domínio cadastrado; resolução DNS será revalidada.':'IP cadastrado; somente Nmap disponível.'}
for(const key of order){const label=document.createElement('label');label.className='tool';const input=document.createElement('input');input.type='checkbox';input.value=key;input.dataset.tool='1';input.addEventListener('change',()=>{if(selection().length>5){input.checked=false;$('status').textContent='Selecione no máximo 5 ferramentas.'}refresh()});label.append(input,document.createTextNode(names[key]));$('tools').append(label)}
$('target').addEventListener('change',()=>{$('approved').checked=false;refresh()});$('approved').addEventListener('change',refresh);
async function load(){try{const data=await request('/tools/targets');targets=data.targets||[];for(const t of targets){const o=document.createElement('option');o.value=t.ip;o.textContent=t.label?t.label+' — '+t.ip:t.ip;$('target').append(o)}if(!targets.length)$('status').textContent='Nenhum alvo cadastrado. Cadastre um alvo autorizado no Dashboard.';refresh()}catch(e){$('status').textContent='Não foi possível carregar os alvos: '+e.message}}
function resultCard(name,value){const card=document.createElement('div');card.className='result';const heading=document.createElement('h3');heading.textContent=names[name]||name;const pre=document.createElement('pre');pre.textContent=JSON.stringify(value,null,2);card.append(heading,pre);$('results').append(card)}
$('run').addEventListener('click',async()=>{const tools=selection(),target=$('target').value;if(!target||!$('approved').checked||!tools.length||tools.length>5)return;
$('run').disabled=true;$('status').textContent='Executando as ferramentas autorizadas. Aguarde...';$('results').replaceChildren();$('rawBox').hidden=true;
try{const data=await request('/tools/chat/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target,tools,approved:true,message:'Consolidar evidências de reconhecimento autorizado.'})});
$('meta').textContent='Alvo: '+data.target+' • '+data.executed_at+' • '+Object.keys(data.results||{}).length+' ferramenta(s) no relatório';
for(const [name,value] of Object.entries(data.results||{}))resultCard(name,value);
if(data.ai)resultCard('Análise Ollama',data.ai);
$('raw').textContent=JSON.stringify(data,null,2);$('rawBox').hidden=false;$('status').textContent='Execução concluída. Resultados não comprovam vulnerabilidades.'}
catch(e){$('status').textContent='Falha na execução: '+e.message;$('status').className='error'}finally{refresh()}});
load();
</script></body></html>'''
