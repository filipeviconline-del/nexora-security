# LINUXSEC_REPORT_V2
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
router = APIRouter()
@router.get('/chat', response_class=HTMLResponse)
def chat():
    return HTML
HTML = r'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Nexora Security | Security Intelligence</title><style>
:root{color-scheme:dark;--bg:#0b1220;--panel:#142a3b;--line:#2b4b5c;--text:#e6f7f7;--muted:#9ab8c4;--green:#35e4a0;--cyan:#00d9d0}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px system-ui}.app{max-width:1100px;margin:auto;padding:18px;min-height:100vh;display:flex;flex-direction:column}header{display:flex;justify-content:space-between;align-items:center;gap:10px;border-bottom:1px solid var(--line);padding-bottom:14px;flex-wrap:wrap}header strong{color:var(--cyan);font-size:22px}.muted{color:var(--muted);font-size:13px}.feed{flex:1;min-height:220px;padding:16px 0}.msg{background:var(--panel);border:1px solid var(--line);padding:16px;border-radius:14px;margin:12px 0;white-space:pre-wrap;overflow-wrap:anywhere}.user{margin-left:14%;background:#183a43}.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin:12px 0}input,textarea,select{background:#081725;color:var(--text);border:1px solid var(--line);border-radius:8px;padding:11px;font:inherit;max-width:100%}textarea{width:100%;min-height:65px;resize:vertical}button{border:0;border-radius:8px;background:var(--green);color:#092021;padding:11px 15px;font-weight:700;cursor:pointer}button.secondary{background:#264b5d;color:var(--text)}button.danger{background:#783b43;color:white}button:disabled{opacity:.5}.row{display:flex;gap:9px;align-items:center;flex-wrap:wrap}.row>*{min-width:0}.grow{flex:1}.composer{position:sticky;bottom:0;background:var(--bg);border-top:1px solid var(--line);padding:14px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#081725;padding:12px;border-radius:8px;max-height:290px;overflow:auto;font-size:12px}.chart{display:grid;gap:10px}.barrow{display:grid;grid-template-columns:110px 1fr 40px;gap:9px;align-items:center}.track{height:16px;background:#091724;border-radius:6px;overflow:hidden}.fill{height:100%;background:var(--cyan)}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.metric{font-size:26px;font-weight:800}.hidden{display:none!important}.status{color:#ffb454}.notice{border-left:3px solid var(--cyan);padding:9px 12px;color:var(--muted)}label{font-size:13px;color:var(--muted)}@media(max-width:640px){.grid{grid-template-columns:1fr 1fr}.barrow{grid-template-columns:90px 1fr 30px}.app{padding:12px}}

/* LinuxSec evidence reader v1 */
.evidence{border:1px solid var(--line);border-radius:14px;padding:16px;margin:12px 0;background:var(--panel)}
.evidence h3{margin:0 0 12px;color:var(--cyan)}.tool-block{border:1px solid var(--line);border-radius:10px;margin:12px 0;overflow:hidden;background:#0d2030}
.tool-head{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:12px;background:#18384a;flex-wrap:wrap}.tool-head strong{font-size:16px}.pill{border-radius:20px;padding:4px 9px;font-size:12px;background:#294a56;color:#e6f7f7}
.fields{padding:12px;display:grid;gap:8px}.field{display:grid;grid-template-columns:minmax(110px,180px) minmax(0,1fr);gap:10px;border-bottom:1px solid #274454;padding-bottom:8px}.field-name{color:var(--muted);overflow-wrap:anywhere}.field-value{white-space:pre-wrap;overflow-wrap:anywhere}
.lines{margin:10px 12px 14px;border:1px solid #294758;border-radius:8px;overflow:auto;max-height:420px;background:#081725}.line{display:grid;grid-template-columns:48px minmax(0,1fr);border-bottom:1px solid #182d3d;font:13px/1.6 ui-monospace,SFMono-Regular,Consolas,monospace}.line-no{color:#7fabb9;text-align:right;padding:4px 10px;border-right:1px solid #294758;user-select:none}.line-text{white-space:pre-wrap;overflow-wrap:anywhere;padding:4px 10px}.section-label{margin:14px 12px 7px;color:var(--cyan);font-weight:700}.evidence details{margin:10px 12px}.evidence summary{cursor:pointer;color:var(--cyan)}.evidence .raw{max-height:260px}.empty-note{padding:10px 12px;color:var(--muted)}
@media(max-width:640px){.field{grid-template-columns:1fr;gap:3px}.evidence{padding:10px}}
/* LinuxSec report v2 */
.ls-report{background:#0e2030;border:1px solid #315468;border-radius:16px;padding:20px;margin:18px 0;box-shadow:0 12px 35px #0003}.ls-report h2{margin:0;color:#e6f7f7}.ls-sub{color:#9ab8c4;margin:6px 0 18px}.ls-metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:15px 0}.ls-stat{background:#142a3b;border:1px solid #2b4b5c;border-radius:10px;padding:14px}.ls-stat b{display:block;font-size:26px;color:#35e4a0}.ls-stat span{color:#b5ccd4;font-size:12px}.ls-tabs{display:flex;flex-wrap:wrap;gap:8px;border-bottom:1px solid #315468;padding-bottom:12px;margin:18px 0}.ls-tabs button{background:#1c3949;color:#e6f7f7;font-weight:600;padding:9px 12px}.ls-tabs button[aria-selected=true]{background:#35e4a0;color:#071d20}.ls-pane[hidden]{display:none}.ls-table{width:100%;border-collapse:collapse;font-size:13px}.ls-table th,.ls-table td{padding:9px;border-bottom:1px solid #294858;text-align:left;overflow-wrap:anywhere}.ls-table th{color:#a7c6d1}.ls-badge{display:inline-block;background:#274b5d;border-radius:20px;padding:3px 8px;font-size:12px}.ls-badge.open{color:#35e4a0}.ls-badge.filtered{color:#ffb454}.ls-warning{border-left:3px solid #ffb454;background:#292b32;padding:12px;margin:12px 0}.ls-ai{white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.65;background:#081725;border:1px solid #294858;border-radius:10px;padding:18px;max-height:750px;overflow:auto}.ls-tools{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}.ls-filter{width:100%;margin:12px 0}.ls-report details{margin:12px 0}.ls-report summary{cursor:pointer;color:#00d9d0}.ls-report pre{max-height:450px}@media(max-width:700px){.ls-metrics{grid-template-columns:repeat(2,minmax(0,1fr))}.ls-report{padding:12px}.ls-table{font-size:12px}}


/* LINUXSEC_CHAT_DESIGN_V1 */
.feed{display:flex;flex-direction:column;gap:16px;padding:24px 0 36px}
.ls-chat-message{max-width:94%;width:fit-content;min-width:min(340px,100%);border:1px solid #2a4a5c;border-radius:18px;background:linear-gradient(155deg,#172d3d,#102333);padding:17px 20px;box-shadow:0 10px 28px #0002;overflow-wrap:anywhere}
.ls-chat-message.is-user{align-self:flex-end;max-width:82%;background:#173b43;border-color:#30686a}
.ls-chat-message.is-assistant{align-self:flex-start}
.ls-chat-message-head{display:flex;align-items:center;gap:9px;margin-bottom:12px;color:#b9d4de;font-size:12px;font-weight:700;letter-spacing:.025em}
.ls-chat-avatar{display:inline-grid;place-items:center;width:27px;height:27px;border-radius:9px;background:#0c5557;color:#a9ffec;font-size:11px}
.is-user .ls-chat-avatar{background:#2d5664;color:white}
.ls-chat-body{line-height:1.65;font-size:14px;color:#e6f7f7}
.ls-chat-paragraph{margin:0 0 12px}.ls-chat-paragraph:last-child{margin-bottom:0}
.ls-chat-heading{margin:14px 0 7px;color:#5cebd7;font-size:14px}
.ls-chat-list{padding-left:22px;margin:8px 0 14px}.ls-chat-list li{margin:5px 0}
.ls-chat-actions{display:flex;justify-content:flex-end;margin-top:12px;border-top:1px solid #315061;padding-top:9px}
.ls-chat-copy{font-size:11px!important;padding:5px 9px!important;border-radius:7px!important;opacity:.8}
.ls-inventory-summary{font-size:13px;color:#a4c8d0;margin:0 0 12px}
.ls-inventory-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}
.ls-inventory-item{background:#0b1d2b;border:1px solid #294859;border-radius:11px;padding:12px;min-width:0}
.ls-inventory-top{display:flex;justify-content:space-between;gap:8px;align-items:center;flex-wrap:wrap}
.ls-inventory-top strong{font-size:14px;color:#f1fcff}
.ls-inventory-state{font-size:10px;font-weight:700;padding:4px 7px;border-radius:20px;background:#334453;color:#c9d7dd}
.ls-inventory-state.ready{background:#123d35;color:#65e5b6}
.ls-inventory-state.missing{background:#443033;color:#ffc1bd}
.ls-inventory-state.internal{background:#273d52;color:#b7dfff}
.ls-inventory-meta{font-size:11px;color:#a3bdc7;margin-top:6px;overflow-wrap:anywhere}
.ls-chat-note{margin-top:15px;padding:11px 13px;background:#102e3b;border-left:3px solid #00d9d0;border-radius:5px;color:#b9d1da;font-size:12px}
@media(max-width:720px){.ls-chat-message,.ls-chat-message.is-user{max-width:100%;width:100%;min-width:0;padding:13px}.ls-inventory-grid{grid-template-columns:1fr}.feed{gap:11px}}


/* NEXORA_REDESIGN_V1 — apresentação apenas; endpoints e handlers originais intactos */
:root{--bg:#090e18;--panel:#111d2b;--line:#253747;--text:#e8f2f7;--muted:#91a7b9;--green:#47ddbc;--cyan:#46e6db;color-scheme:dark}
html{scroll-behavior:smooth}body{background:radial-gradient(ellipse 850px 450px at 88% -8%,#133746 0%,transparent 65%),radial-gradient(ellipse 700px 600px at -18% 52%,#101c35 0%,transparent 65%),#090e18;color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;letter-spacing:.005em}
.app{max-width:1260px;padding:0 32px 32px}.nx-topbar{min-height:92px;border-bottom:1px solid #253443;padding:18px 0;gap:20px}.nx-brand{display:flex;align-items:center;gap:12px;color:inherit;text-decoration:none}.nx-brand-mark{display:grid;place-items:center;width:45px;height:45px;border:1px solid #286c75;border-radius:14px;color:#4be4d8;background:linear-gradient(145deg,#123842,#11212f);font-size:35px;line-height:1;box-shadow:0 0 26px #22ddcf16}.nx-brand strong{display:block;font-size:22px;letter-spacing:.11em;line-height:1.1;color:#f0f8fa}.nx-brand-accent{color:#47e6d8}.nx-brand small{display:block;margin-top:5px;font-size:9px;letter-spacing:.22em;color:#8ea9b9;font-weight:750}.nx-header-right{display:flex;align-items:center;flex-wrap:wrap;gap:9px}.nx-local{font-size:10px;letter-spacing:.12em;color:#b1c6d1;background:#101e2a;border:1px solid #2a3d49;padding:10px 12px;border-radius:100px;white-space:nowrap}.nx-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#4de1b3;box-shadow:0 0 10px #4de1b3;margin-right:7px}.nx-nav{display:flex;align-items:center;gap:7px;margin:17px 0 27px;overflow:auto;scrollbar-width:thin}.nx-nav-item{color:#9db1c2;text-decoration:none;padding:11px 15px;border:1px solid transparent;border-radius:10px;font-size:13px;font-weight:650;white-space:nowrap;transition:.15s}.nx-nav-item:hover{background:#17283a;color:#effafb}.nx-nav-item.nx-current{background:#15333a;color:#69eee0;border-color:#23565d}.nx-hero{min-height:235px;position:relative;overflow:hidden;border:1px solid #2a4551;border-radius:22px;background:linear-gradient(110deg,#142d3c 0%,#10202e 60%,#0d1726 100%);padding:34px 40px;display:flex;align-items:center;box-shadow:0 18px 60px #0003}.nx-hero-copy{z-index:1;max-width:680px}.nx-eyebrow,.nx-section-kicker{font-size:10px;font-weight:800;letter-spacing:.19em;color:#69cfc9}.nx-hero h1{font-size:clamp(26px,3.3vw,43px);letter-spacing:-.045em;line-height:1.15;margin:14px 0 12px;font-weight:760;color:#f3fbfd}.nx-hero h1 em{font-style:normal;color:#4fe1d4}.nx-hero p{color:#b0c3d0;line-height:1.7;margin:0;font-size:14px;max-width:550px}.nx-hero-tags{display:flex;gap:9px;flex-wrap:wrap;margin-top:20px}.nx-hero-tags span{background:#152d3a;border:1px solid #2a4b58;border-radius:7px;color:#a9d4d7;font-size:11px;padding:7px 10px}.nx-hero-art{position:absolute;right:7%;top:50%;width:220px;height:220px;transform:translateY(-50%);opacity:.75}.nx-orbit{position:absolute;border:1px solid #2c8589;border-radius:50%;inset:10px;box-shadow:inset 0 0 28px #1dd5c70b}.nx-orbit-b{inset:40px;border-style:dashed;transform:rotate(30deg)}.nx-orbit-core{position:absolute;inset:65px;display:grid;place-items:center;font-size:76px;color:#55d9d2;text-shadow:0 0 35px #46e6db66}.nx-section-head{display:flex;align-items:end;justify-content:space-between;gap:12px;margin:34px 0 6px}.nx-section-head h2{margin:7px 0 0;font-size:22px;letter-spacing:-.025em}.nx-section-caption{font-size:12px;color:#8fa6b7}.nx-report-anchor{height:0;scroll-margin-top:30px}.feed{gap:14px;min-height:150px;padding:16px 0 25px}.feed>.msg:first-child{border:1px solid #2a4652;background:#112331;color:#bcd2dd;border-radius:16px;line-height:1.75;padding:18px 22px}.ls-chat-message{background:#122330;border-color:#2b4350;box-shadow:0 10px 25px #0002}.ls-chat-message.is-user{background:#18383c;border-color:#316361}.ls-chat-message-head{color:#82d9d2}.ls-chat-avatar{background:#164f51}.ls-chat-body{font-size:14px;line-height:1.8}.ls-chat-heading{color:#60e4d6}.ls-inventory-card{background:#10202c;border-color:#2b4551}.card,.evidence,.ls-report{background:#101d2a;border:1px solid #293d4c;border-radius:17px;box-shadow:0 12px 35px #0002}.ls-report{padding:25px}.ls-stat{background:#142534;border-color:#2b4151}.ls-stat b{color:#58dfc4}.ls-tabs button{background:#1b3040;color:#b7cfda}.ls-tabs button[aria-selected=true]{background:#49ddc8;color:#092329}.ls-ai{background:#0b1724;border-color:#2c4352;line-height:1.8}.composer{z-index:5;bottom:0;border:1px solid #2d4954;border-radius:18px;background:#101e2bed;backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);padding:19px 20px 12px;margin:12px 0 20px;box-shadow:0 -8px 50px #0004}.composer textarea{margin:12px 0 10px;min-height:92px;line-height:1.6;background:#0b1826;border:1px solid #345061;border-radius:12px;padding:15px}.composer textarea:focus,.composer select:focus,input:focus{outline:2px solid #40cbbb88;outline-offset:1px}.composer>.muted,.composer p.muted{font-size:11px;line-height:1.6;margin:12px 0 0}.composer .row{gap:9px}.composer label{font-weight:650}button{background:#4adbc6;color:#092329;border-radius:10px;transition:background .15s,transform .15s;font-weight:750}button:hover:not(:disabled){background:#79eee0;transform:translateY(-1px)}button.secondary{background:#1b3545;color:#d1e5ed;border:1px solid #315164}button.secondary:hover:not(:disabled){background:#27485a}button.danger{background:#743a45;color:white}.status{font-size:12px}.ls-report pre,.lines,pre{background:#0b1622}a:focus-visible,button:focus-visible{outline:2px solid #56e4d7;outline-offset:3px}
@media(max-width:900px){.nx-hero-art{right:-70px;opacity:.3}.nx-hero-copy{max-width:100%}.nx-local{display:none}}
@media(max-width:640px){.app{padding:0 13px 18px}.nx-topbar{padding:15px 0;align-items:flex-start}.nx-header-right{width:100%}.nx-header-right button{flex:1;font-size:11px;padding:10px}.nx-nav{margin:12px 0 19px;gap:3px}.nx-nav-item{padding:10px 11px;font-size:12px}.nx-hero{padding:25px 20px;min-height:215px;border-radius:16px}.nx-hero h1{font-size:27px}.nx-hero p{font-size:12px}.nx-hero-tags{gap:5px}.nx-hero-tags span{font-size:10px}.nx-hero-art{display:none}.nx-section-head{margin-top:25px;align-items:start;flex-direction:column}.nx-section-caption{font-size:11px}.composer{padding:13px;border-radius:14px;bottom:0;margin-bottom:8px}.composer .row button{flex:1;font-size:12px;padding:10px}.composer select{width:100%;flex-basis:100%}.ls-report{padding:13px}.ls-metrics{grid-template-columns:repeat(2,minmax(0,1fr))}.ls-chat-message,.ls-chat-message.is-user{max-width:100%;width:100%;min-width:0}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}button{transition:none}}

</style></head><body><div class="app"><header class="nx-topbar"><a class="nx-brand" href="/chat" aria-label="Nexora Security — início"><span class="nx-brand-mark">◇</span><span><strong>NEXORA<span class="nx-brand-accent">.</span></strong><small>SECURITY INTELLIGENCE</small></span></a><div class="nx-header-right"><span class="nx-local"><span class="nx-dot"></span> AMBIENTE LOCAL</span><button class="secondary" id="targetsToggle">◎ Alvos autorizados</button><button class="secondary" id="httpToggle">↗ Analisador HTTP</button></div></header>
<nav class="nx-nav" aria-label="Navegação principal"><a href="/" class="nx-nav-item">▦ <span>Dashboard</span></a><a href="/chat" class="nx-nav-item nx-current" aria-current="page">✧ <span>Assistente IA</span></a><a href="#nx-workspace" class="nx-nav-item">⌘ <span>Workspace</span></a><a href="#nx-reports" class="nx-nav-item">▤ <span>Relatórios</span></a></nav>
<section class="nx-hero" id="nx-workspace"><div class="nx-hero-copy"><div class="nx-eyebrow"><span class="nx-dot"></span> OPERAÇÕES DE SEGURANÇA · WORKSPACE</div><h1>Inteligência para cada <em>investigação.</em></h1><p>Converse com sua IA local, prepare análises autorizadas e transforme evidências em decisões claras.</p><div class="nx-hero-tags"><span>◈ Ollama local</span><span>◉ Escopo autorizado</span><span>◇ Evidências verificáveis</span></div></div><div class="nx-hero-art" aria-hidden="true"><div class="nx-orbit nx-orbit-a"></div><div class="nx-orbit nx-orbit-b"></div><div class="nx-orbit-core">◇</div></div></section>
<div class="nx-section-head"><div><span class="nx-section-kicker">CENTRO DE COMANDO</span><h2>Assistente de segurança</h2></div><span class="nx-section-caption">Respostas, planos e evidências em um só lugar</span></div><div id="nx-reports" class="nx-report-anchor" aria-hidden="true"></div>
<section id="targetsPanel" class="card hidden"><h3>Alvos autorizados</h3><form id="targetForm" class="row"><input class="grow" id="newTarget" placeholder="IP ou domínio" required maxlength="253"><input id="newLabel" placeholder="Descrição" maxlength="80"><label><input type="checkbox" id="auth" required> Tenho autorização</label><button>Cadastrar</button></form><p id="targetStatus" class="muted"></p><div id="targetList"></div></section>
<section id="httpPanel" class="card hidden"><h3>Analisador HTTP original</h3><iframe title="Analisador HTTP" id="httpFrame" style="width:100%;height:720px;border:0" data-src="/analyzer"></iframe></section>
<div class="feed" id="feed"><div class="msg">Olá! Escolha um alvo cadastrado e descreva a análise desejada. Prepararei um plano e só executarei as verificações após sua aprovação. Você poderá pedir gráficos e pesquisar evidências usando grep: ssh, nginx.</div></div>
<div class="composer"><div class="row"><label for="target">Alvo autorizado</label><select id="target" class="grow"></select><button class="secondary" id="refresh">Atualizar</button></div><textarea id="message" maxlength="10000" placeholder="Analise DNS, portas e serviços deste alvo.">Analise a superfície de exposição, explique os resultados e gere gráficos.</textarea><div class="row"><button class="secondary" id="askAI">Conversar com IA</button><button id="plan">Preparar plano</button><button id="approve" class="hidden">Aprovar e executar</button><button id="charts" class="secondary" disabled>Gerar gráficos</button><span id="status" class="status" role="status"></span></div><p class="muted">Os gráficos usam dados reais coletados; a IA interpreta os achados, mas não inventa medições. As ferramentas dependem de instalação e autorização; resultados descobertos não ampliam o escopo.</p></div></div>
<script>
const $=id=>document.getElementById(id);let currentPlan=null,lastResult=null;function el(tag,cls,txt){const n=document.createElement(tag);if(cls)n.className=cls;if(txt!==undefined)n.textContent=txt;return n}/* LINUXSEC_CHAT_DESIGN_V1 — renderização segura de mensagens */
function lsChatText(parent,text){
 const lines=String(text??'').split(/\r?\n/), fragment=document.createDocumentFragment();let paragraph=null;
 const flush=()=>{if(paragraph){fragment.append(paragraph);paragraph=null}};
 for(const raw of lines){const line=raw.trim();if(!line){flush();continue}
  if(/^#{1,3}\s+/.test(line)){flush();fragment.append(el('h4','ls-chat-heading',line.replace(/^#{1,3}\s+/,'')));continue}
  if(/^[-•]\s+/.test(line)){if(!paragraph||paragraph.tagName!=='UL'){flush();paragraph=el('ul','ls-chat-list')}paragraph.append(el('li','',line.replace(/^[-•]\s+/,'')));continue}
  if(/^\d+[.)]\s+/.test(line)){if(!paragraph||paragraph.tagName!=='OL'){flush();paragraph=el('ol','ls-chat-list')}paragraph.append(el('li','',line.replace(/^\d+[.)]\s+/,'')));continue}
  if(!paragraph||paragraph.tagName!=='P'){flush();paragraph=el('p','ls-chat-paragraph')}
  if(paragraph.childNodes.length)paragraph.append(document.createTextNode(' '));paragraph.append(document.createTextNode(raw));
 }
 flush();parent.append(fragment)
}
function lsChatInventory(parent,text){
 const lines=String(text).split(/\r?\n/), rows=lines.filter(l=>/^\s*-\s*[\w.-]+\s*:/.test(l));
 if(!rows.length)return false;
 const summary=el('div','ls-inventory-summary',rows.length+' ferramentas identificadas no inventário local');parent.append(summary);
 const grid=el('div','ls-inventory-grid');
 for(const line of rows){const m=line.match(/^\s*-\s*([\w.-]+)\s*:\s*(.*)$/);if(!m)continue;const name=m[1],detail=m[2];const card=el('div','ls-inventory-item');const top=el('div','ls-inventory-top');top.append(el('strong','',name));let state='Não verificado',cls='unknown';if(/NOT_INSTALLED/i.test(detail)){state='Não instalado';cls='missing'}else if(/ADAPTER_OR_INTERNAL/i.test(detail)){state='Adaptador';cls='internal'}else if(/EXTERNAL_SERVICE/i.test(detail)){state='Serviço externo';cls='internal'}else if(/READY/i.test(detail)){state='Detectado';cls='ready'}top.append(el('span','ls-inventory-state '+cls,state));card.append(top);
 const integrated=detail.match(/integrado no backend\s*=\s*(sim|não)/i);if(integrated)card.append(el('div','ls-inventory-meta','Backend: '+integrated[1]));
 const version=detail.match(/\|\s*(.+)$/);if(version)card.append(el('div','ls-inventory-meta',version[1].trim().slice(0,160)));
 grid.append(card)}parent.append(grid);
 const rest=lines.filter(l=>!/^\s*-\s*[\w.-]+\s*:/.test(l)).join('\n').trim();if(rest){const note=el('div','ls-chat-note');lsChatText(note,rest);parent.append(note)}return true
}
function bubble(txt,who='assistant'){
 const wrap=el('article','ls-chat-message '+(who==='user'?'is-user':'is-assistant'));
 const head=el('div','ls-chat-message-head');head.append(el('span','ls-chat-avatar',who==='user'?'EU':'AI'));head.append(el('span','ls-chat-speaker',who==='user'?'Você':'LinuxSec AI'));
 const body=el('div','ls-chat-body');if(who!=='user'&&!lsChatInventory(body,txt))lsChatText(body,txt);else if(who==='user')lsChatText(body,txt);
 const actions=el('div','ls-chat-actions');const copy=el('button','secondary ls-chat-copy','Copiar');copy.type='button';copy.onclick=()=>navigator.clipboard.writeText(String(txt)).then(()=>copy.textContent='Copiado!').catch(()=>copy.textContent='Falha ao copiar');actions.append(copy);
 wrap.append(head,body,actions);$('feed').append(wrap);wrap.scrollIntoView({block:'nearest'});return wrap
}async function req(url,method='GET',body){const r=await fetch(url,{method,headers:{'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined});const data=await r.json();if(!r.ok)throw Error(typeof data.detail==='string'?data.detail:'Erro HTTP '+r.status);return data}function busy(value,label){$('plan').disabled=value;$('approve').disabled=value;$('status').textContent=label||''}async function targets(){try{const r=await req('/tools/targets');const old=$('target').value;$('target').replaceChildren();$('targetList').replaceChildren();for(const t of r.targets){const opt=el('option','',t.label?t.label+' — '+t.ip:t.ip);opt.value=t.ip;$('target').append(opt);const line=el('div','row');line.style.padding='7px 0';line.append(el('span','grow',t.ip+(t.resolved_ips?.length?' → '+t.resolved_ips.join(', '):'')));if(t.ip!=='127.0.0.1'){const del=el('button','danger','Remover');del.onclick=async()=>{if(!confirm('Remover '+t.ip+'?'))return;try{await req('/tools/targets/'+encodeURIComponent(t.ip),'DELETE');await targets()}catch(e){$('targetStatus').textContent=e.message}};line.append(del)}$('targetList').append(line)}if([...$('target').options].some(x=>x.value===old))$('target').value=old}catch(e){bubble('Erro ao carregar alvos: '+e.message)}}
$('refresh').onclick=targets;$('targetsToggle').onclick=()=>{$('targetsPanel').classList.toggle('hidden')};$('httpToggle').onclick=()=>{$('httpPanel').classList.toggle('hidden');if(!$('httpPanel').classList.contains('hidden')&&!$('httpFrame').src)$('httpFrame').src=$('httpFrame').dataset.src};$('targetForm').onsubmit=async e=>{e.preventDefault();try{await req('/tools/targets','POST',{ip:$('newTarget').value,label:$('newLabel').value,authorization_confirmed:$('auth').checked});$('targetStatus').textContent='Alvo cadastrado.';$('targetForm').reset();await targets()}catch(err){$('targetStatus').textContent=err.message}};
$('plan').onclick=async()=>{if(await maybeGrepFromChat())return;currentPlan=null;lastResult=null;$('approve').classList.add('hidden');$('charts').disabled=true;const target=$('target').value,message=$('message').value.trim();if(/(?:invent[aá]rio(?:\s+(?:de|das)\s+ferramentas)?|listar\s+(?:as\s+)?ferramentas|quais\s+ferramentas\s+(?:est[aã]o\s+)?(?:instalad[ao]s|dispon[ií]veis)|tool registry)/i.test(message)){bubble(message,'user');busy(true,'Verificando ferramentas locais...');try{const inv=await req('/tools/registry');bubble('Inventário local de ferramentas:\n'+inv.tools.map(t=>t.name+' — '+t.status+(t.version?' — '+t.version:'')+(t.path?' — '+t.path:'')).join('\n')+'\n\n'+inv.notice)}catch(e){bubble('Falha no inventário: '+e.message)}finally{busy(false,'')}return;}if(!target){bubble('Cadastre um alvo primeiro.');return}bubble('Alvo: '+target+'\n'+message,'user');busy(true,'Preparando plano...');try{const p=await req('/tools/chat/plan','POST',{target,message});currentPlan=p;bubble('Plano para '+p.target+':\n'+p.steps.map((s,i)=>(i+1)+'. '+s.tool.toUpperCase()+' — '+s.description).join('\n')+'\n\nAprovação necessária antes da execução.');$('approve').classList.remove('hidden')}catch(e){bubble('Erro: '+e.message)}finally{busy(false,'')}};
// Conversa informativa, sem execução de scanners ou necessidade de alvo.
let lsChatHistory=[];
$('askAI').onclick=async()=>{
 const message=$('message').value.trim();
 if(!message){bubble('Digite uma pergunta para o assistente.');return;}
 bubble(message,'user');$('askAI').disabled=true;$('status').textContent='Consultando assistente...';
 try{
  const answer=await req('/tools/chat/ask','POST',{message,history:lsChatHistory.slice(-6)});
  bubble(answer.text+'\n\nFonte: '+(answer.source==='local_registry'?'inventário local':'Ollama '+answer.model));
  lsChatHistory.push({role:'user',content:message},{role:'assistant',content:answer.text});
  lsChatHistory=lsChatHistory.slice(-8);
 }catch(e){bubble('Erro no assistente: '+e.message)}
 finally{$('askAI').disabled=false;$('status').textContent=''}
};

$('approve').onclick=async()=>{if(!currentPlan)return;if($('target').value!==currentPlan.target||$('message').value.trim()!==currentPlan.message){bubble('Alvo ou pedido alterado: prepare novo plano.');return}busy(true,'Executando; aguarde...');$('approve').classList.add('hidden');try{lastResult=await req('/tools/chat/run','POST',{target:currentPlan.target,message:currentPlan.message,tools:currentPlan.steps.map(s=>s.tool),approved:true});renderReportV2(lastResult);$('charts').disabled=false}catch(e){bubble('Falha: '+e.message)}finally{busy(false,'')}};


// Exibe evidências como texto (textContent), nunca como HTML fornecido pelo scanner.
function addField(parent,key,value){
 const row=el('div','field');row.append(el('div','field-name',key),el('div','field-value',String(value)));
 parent.append(row);
}
function addLines(parent,title,raw){
 const label=el('div','section-label',title);parent.append(label);
 const lines=el('div','lines');const all=String(raw).split(/\r?\n/);
 const limit=300;
 for(let i=0;i<Math.min(all.length,limit);i++){
  const row=el('div','line');row.append(el('span','line-no',String(i+1)),el('span','line-text',all[i]||' '));lines.append(row);
 }
 if(all.length>limit)lines.append(el('div','empty-note','Exibindo as primeiras '+limit+' linhas de '+all.length+'. Consulte o JSON original para o conteúdo retornado.'));
 parent.append(lines);
}
function renderEvidence(results,target){
 const container=el('section','evidence');container.append(el('h3','','Evidências técnicas — '+target));
 container.append(el('p','muted','Dados coletados pelas ferramentas. A interpretação da IA aparece separadamente abaixo.'));
 for(const [tool,data] of Object.entries(results||{})){
  const block=el('section','tool-block');const head=el('div','tool-head');
  head.append(el('strong','',tool.toUpperCase()));
  const status=(data&&typeof data==='object'&&!Array.isArray(data))?(data.status||data.state||'resultado'):'resultado';
  head.append(el('span','pill',String(status)));block.append(head);
  if(data===null||data===undefined){block.append(el('p','empty-note','Sem dados retornados.'));}
  else if(typeof data==='string'){addLines(block,'Saída da ferramenta',data);}
  else if(Array.isArray(data)){
   const fields=el('div','fields');addField(fields,'Itens retornados',data.length);block.append(fields);
   data.forEach((item,i)=>addLines(block,'Item '+(i+1),typeof item==='string'?item:JSON.stringify(item,null,2)));
  }else if(typeof data==='object'){
   const fields=el('div','fields');
   for(const [key,value] of Object.entries(data)){
    if(value===null||value===undefined)continue;
    if(typeof value==='string'&&(key==='stdout'||key==='stderr'||key==='headers'||key==='output'||key==='raw'||value.includes('\n'))){
      addLines(block,key==='stdout'?'Saída do terminal':key==='stderr'?'Mensagens de erro':key==='headers'?'Cabeçalhos HTTP':key,value);
    }else if(typeof value==='object'){
      if(Array.isArray(value)&&value.every(x=>typeof x!=='object'||x===null))addField(fields,key,value.join(', '));
      else addLines(block,key,JSON.stringify(value,null,2));
    }else addField(fields,key,value);
   }
   if(fields.childNodes.length)block.insertBefore(fields,block.children[1]||null);
  }else{const fields=el('div','fields');addField(fields,'Valor',data);block.append(fields);}
  container.append(block);
 }
 const details=el('details');details.append(el('summary','','Ver JSON original completo'));
 const raw=el('pre','raw',JSON.stringify(results,null,2));details.append(raw);
 const copy=el('button','secondary','Copiar JSON');copy.type='button';
 copy.onclick=async()=>{try{await navigator.clipboard.writeText(JSON.stringify(results,null,2));copy.textContent='Copiado!'}catch(_){copy.textContent='Selecione o JSON para copiar'}};
 details.append(copy);container.append(details);
 $('feed').append(container);container.scrollIntoView({block:'end'});
}
function drawCharts(){if(!lastResult)return;const results=lastResult.results;const nmap=results.nmap||{};const rows=[];for(const line of (nmap.stdout||'').split(/\r?\n/)){const m=line.match(/^(\d+)\/(tcp|udp)\s+(open|closed|filtered|open\|filtered|closed\|filtered|unfiltered)\s+(\S+)/);if(m)rows.push({port:m[1],state:m[3],service:m[4]})}const open=rows.filter(x=>x.state==='open').length,closed=rows.filter(x=>x.state==='closed').length,other=rows.length-open-closed;const dns=results.dns||{};const types=['A','AAAA','MX','NS','TXT','CNAME'];const dnsCounts=types.map(t=>({name:t,count:dns[t]?.records?.length||0}));const box=el('div','card');box.append(el('h3','','Gráficos da análise — '+lastResult.target));const summary=el('div','grid');for(const [title,num] of [['Portas abertas',open],['Portas fechadas',closed],['Serviços observados',new Set(rows.filter(x=>x.state==='open').map(x=>x.service)).size]]){const c=el('div','card');c.append(el('div','muted',title),el('div','metric',String(num)));summary.append(c)}box.append(summary);function graph(title,items){const wrap=el('div','card');wrap.append(el('h4','',title));const max=Math.max(1,...items.map(x=>x.count));for(const item of items){const row=el('div','barrow');row.append(el('span','',item.name));const track=el('div','track');const fill=el('div','fill');fill.style.width=(item.count/max*100)+'%';track.append(fill);row.append(track,el('span','',String(item.count)));wrap.append(row)}return wrap}if(results.nmap)box.append(graph('Estados das portas (linhas reconhecidas)',[{name:'Abertas',count:open},{name:'Fechadas',count:closed},{name:'Outras',count:other}]));if(results.dns)box.append(graph('Registros DNS por tipo',dnsCounts));if(!results.nmap&&!results.dns)box.append(el('p','muted','Sem métricas numéricas disponíveis.'));box.append(el('p','notice','Gráficos derivados dos resultados técnicos, não estimativas da IA. O Nmap pode omitir portas fechadas da saída textual.'));$('feed').append(box);box.scrollIntoView({block:'end'})}
async function maybeGrepFromChat(){
 const msg=$('message').value.trim();
 const match=msg.match(/^(?:grep\s*:\s*|(?:pesquise|procure|busque|encontre)\s+(?:por\s+)?(?:as?\s+palavras?\s+)?)(.+)$/i);
 if(!match)return false;
 if(!lastResult){bubble('Execute primeiro uma análise autorizada. A pesquisa utiliza somente as evidências da última execução nesta página.');return true;}
 if($('target').value!==lastResult.target){bubble('O alvo mudou. Faça uma nova análise antes de pesquisar.');return true;}
 const keywords=[...new Set((match[1].match(/"[^"]+"|'[^']+'|[^,;\s]+/g)||[]).map(s=>s.replace(/^["']|["']$/g,'').trim()).filter(Boolean))].slice(0,10);
 if(!keywords.length){bubble('Informe palavras-chave. Exemplo: grep: ssh, nginx');return true;}
 const evidence=JSON.stringify(lastResult.results,null,2).slice(0,190000);
 bubble(msg,'user');busy(true,'Pesquisando nas evidências...');
 try{
  const result=await req('/tools/grep','POST',{text:evidence,keywords,ignore_case:true});
  bubble('Grep nas evidências da última execução: '+result.total_matches+' linha(s) encontrada(s)'+(result.truncated?' (exibição limitada)':'')+'.');
  const pre=el('pre','',result.matches.length?result.matches.map(x=>x.line+': '+x.text).join('\n'):'Nenhuma correspondência.');$('feed').append(pre);
  if(result.matches.length){
   const ai=await req('/tools/chat/explain-grep','POST',{target:lastResult.target,keywords,matches:result.matches.slice(0,40)});
   bubble('Análise da IA sobre as correspondências ('+ai.status+'):\n'+ai.text);
  }
 }catch(e){bubble('Erro na pesquisa: '+e.message)}finally{busy(false,'')}
 return true;
}
 $('charts').onclick=drawCharts;targets();
// LINUXSEC_REPORT_V2: render from tool results; untrusted strings only through textContent.
function lsFacts(result){
 const facts=result.ai?.facts;
 if(facts&&Array.isArray(facts.ports))return facts;
 const results=result.results||{},ports=[],counts={},subdomains={},statuses={};
 for(const [name,data] of Object.entries(results)){
  statuses[name]=data?.status||'unknown';
  if(name==='nmap')for(const line of String(data?.stdout||'').split(/\r?\n/)){
   const m=line.match(/^\s*(\d+)\/(tcp|udp)\s+(open\|filtered|closed\|filtered|open|closed|filtered|unfiltered)\s+(\S+)(?:\s+(.*))?$/);
   if(m){ports.push({port:Number(m[1]),protocol:m[2],state:m[3],service:m[4],details:m[5]||''});counts[m[3]]=(counts[m[3]]||0)+1}
  }
  if(['subfinder','amass'].includes(name))subdomains[name]=Array.isArray(data?.subdomains)?data.subdomains:[];
 }
 return {executed_tools:Object.keys(results),tool_status:statuses,ports,port_counts:counts,subdomains,limitations:[]};
}
function lsNode(tag,cls,text){const x=document.createElement(tag);if(cls)x.className=cls;if(text!==undefined)x.textContent=String(text);return x}
function lsTable(headers,rows){const table=lsNode('table','ls-table'),thead=lsNode('thead'),tr=lsNode('tr');headers.forEach(h=>tr.append(lsNode('th','',h)));thead.append(tr);table.append(thead);const body=lsNode('tbody');rows.forEach(values=>{const row=lsNode('tr');values.forEach(v=>row.append(lsNode('td','',v)));body.append(row)});table.append(body);return table}
function renderReportV2(result){
 const facts=lsFacts(result),tools=facts.executed_tools||[],ports=facts.ports||[],counts=facts.port_counts||{};
 const report=lsNode('section','ls-report');report.append(lsNode('h2','','Relatório técnico — '+result.target),lsNode('p','ls-sub','Evidências verificáveis • '+(result.executed_at||'Horário indisponível')));
 const metrics=lsNode('div','ls-metrics');for(const [label,value] of [['Ferramentas',tools.length],['Abertas',counts.open||0],['Filtradas',counts.filtered||0],['Fechadas',counts.closed||0]]){const card=lsNode('div','ls-stat');card.append(lsNode('b','',value),lsNode('span','',label));metrics.append(card)}report.append(metrics);
 const bar=lsNode('div','ls-tools');for(const t of tools)bar.append(lsNode('span','ls-badge',t.toUpperCase()+' · '+(facts.tool_status?.[t]||'unknown')));report.append(bar);
 const tabs=lsNode('div','ls-tabs'),panes={};
 const addTab=(name,caption)=>{const btn=lsNode('button','',caption);btn.type='button';btn.setAttribute('aria-selected',name==='overview'?'true':'false');tabs.append(btn);const pane=lsNode('div','ls-pane');pane.hidden=name!=='overview';panes[name]=pane;btn.onclick=()=>{[...tabs.children].forEach(b=>b.setAttribute('aria-selected',String(b===btn)));Object.entries(panes).forEach(([key,p])=>p.hidden=key!==name)}};
 addTab('overview','Visão geral');addTab('evidence','Evidências');addTab('ai','Análise Ollama');addTab('raw','JSON original');report.append(tabs);
 const overview=panes.overview;overview.append(lsNode('h3','','Portas identificadas'));
 if(ports.length){const input=lsNode('input','ls-filter');input.placeholder='Filtrar por porta, estado ou serviço';overview.append(input);const tableHost=lsNode('div');overview.append(tableHost);const paint=()=>{const q=input.value.trim().toLowerCase();const rows=ports.filter(p=>[p.port,p.protocol,p.state,p.service,p.details].join(' ').toLowerCase().includes(q)).map(p=>[p.port+'/'+p.protocol,p.state,p.service,p.details||'—']);tableHost.replaceChildren(lsTable(['Porta','Estado','Serviço','Detalhes'],rows))};input.oninput=paint;paint()}
 else overview.append(lsNode('p','muted','Nenhuma linha de porta foi reconhecida nos resultados disponíveis.'));
 const subs=Object.entries(facts.subdomains||{});for(const [tool,names] of subs){overview.append(lsNode('h3','','Subdomínios — '+tool));overview.append(lsNode('p','muted',names.length+' nome(s) reportado(s). Descoberta não amplia autorização.'));if(names.length){const details=lsNode('details'),summary=lsNode('summary','','Mostrar subdomínios');details.append(summary,lsNode('pre','',names.join('\n')));overview.append(details)}}
 const notice=lsNode('div','ls-warning','Porta aberta não comprova vulnerabilidade. “filtered” não significa “closed”. Somente as ferramentas listadas acima foram executadas nesta análise.');overview.append(notice);
 for(const lim of facts.limitations||[])overview.append(lsNode('p','muted',lim));
 const evidence=panes.evidence;evidence.append(lsNode('p','muted','Dados originais por ferramenta, sem interpretação da IA.'));for(const [tool,data] of Object.entries(result.results||{})){const details=lsNode('details'),summary=lsNode('summary','',tool.toUpperCase()+' — '+(data?.status||'resultado'));details.append(summary,lsNode('pre','',JSON.stringify(data,null,2)));evidence.append(details)}
 const ai=panes.ai;ai.append(lsNode('p','muted','Texto gerado pelo modelo. Hipóteses e recomendações não são fatos verificados.'));if(result.ai?.evidence_truncated)ai.append(lsNode('div','ls-warning','O contexto de evidências enviado ao Ollama foi truncado.'));ai.append(lsNode('div','ls-ai',result.ai?.text||'Nenhuma resposta do Ollama.'));
 const raw=panes.raw;raw.append(lsNode('pre','',JSON.stringify(result,null,2)));const copy=lsNode('button','secondary','Copiar relatório JSON');copy.onclick=()=>navigator.clipboard.writeText(JSON.stringify(result,null,2)).then(()=>copy.textContent='Copiado').catch(()=>copy.textContent='Não foi possível copiar');raw.append(copy);
 for(const key of ['overview','evidence','ai','raw'])report.append(panes[key]);$('feed').append(report);report.scrollIntoView({block:'start',behavior:'smooth'});
}

</script></body></html>'''
