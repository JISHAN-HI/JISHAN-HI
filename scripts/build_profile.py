"""DevOps terminal profile. Standard library only; all SVGs are self-contained."""
from pathlib import Path
from html import escape
import datetime as dt
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
ASSETS.mkdir(exist_ok=True)
INK='#dae5e4'; MUTED='#869a9d'; GREEN='#74e5b5'; BG='#0b1216'

def t(x,y,s,size=13,color=INK,extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {extra}>{escape(str(s))}</text>'

def frame(w,h,title,body,defs=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title><defs>{defs}</defs>
<style>text{{font-family:'DejaVu Sans Mono',Consolas,monospace}}.line{{animation:line .55s ease-out both;animation-delay:var(--d,0s)}}@keyframes line{{from{{opacity:0;transform:translateY(4px)}}to{{opacity:1;transform:translateY(0)}}}}.cell{{animation:cell .5s ease-out both;animation-delay:var(--d,0s)}}@keyframes cell{{from{{opacity:0;transform:translateY(-5px)}}to{{opacity:1;transform:translateY(0)}}}}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}.wipe{{display:none}}}}</style>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="10" fill="{BG}" stroke="#233237"/>
{body}</svg>'''

def save(name,svg):
    (ASSETS/name).write_text(svg,encoding='utf-8')

def bar(w,label):
    return ''.join(f'<circle cx="{18+i*13}" cy="19" r="3.5" fill="{c}"/>' for i,c in enumerate(['#c57878','#cfb478','#74bd99']))+t(68,23,label,10,MUTED)+f'<path d="M1 38H{w-1}" stroke="#233237"/>'

# A character-rendered infrastructure console, not a photo or a fake live monitor.
art=[
'             .-----------------.',
'          .-\'   CLOUD / EDGE    `-.',
'        .\'                       `.',
'        `----._____________.-----\'',
'                  | |',
'          +-------+-+-------+',
'          |                 |',
'     .----+----.       .----+----.',
'     |  [:::]  |       |  [:::]  |',
'     |  [:::]  |       |  [:::]  |',
'     |  [:::]  |       |  [:::]  |',
'     `----+----\'       `----+----\'',
'          |                 |',
'          +--------+--------+',
'                   |',
'          .--------+--------.',
'          |    >_  JISHAN    |',
'          |  build / deploy |',
'          | observe / heal  |',
'          `-----------------\'',
]
body=bar(370,'infra-as-code.sh')
body+=t(22,64,'$ ./render-infrastructure',11,GREEN)
for i,line in enumerate(art):
    y=94+i*13
    body+=t(17,y,line,10.4,INK,'xml:space="preserve"')
    # Opaque covers wipe away one row at a time; text is visible without SMIL.
    body+=f'<rect class="wipe" x="16" y="{y-11}" width="0" height="13" fill="{BG}"><animate attributeName="x" values="16;353" dur=".15s" begin="{.25+i*.1:.2f}s" fill="freeze"/><animate attributeName="width" values="337;0" dur=".15s" begin="{.25+i*.1:.2f}s" fill="freeze"/><set attributeName="width" to="337" begin="0s" end="{.25+i*.1:.2f}s"/></rect>'
body+=t(24,386,'INFRASTRUCTURE IS A CRAFT.',11,GREEN)
body+=t(24,408,'Make it repeatable. Make it observable.',9.5,MUTED)
save('devops-ascii.svg',frame(370,438,'Animated ASCII cloud, servers and DevOps terminal',body))

body=bar(490,'jishan@github: ~')
body+=t(24,72,'jishan@github',21,GREEN,'font-weight="bold"')
body+=t(24,94,'------------------------------',12,MUTED)
rows=[('Name','Jishan Mulla'),('Role','DevOps Engineer'),('Focus','Cloud + on-prem infrastructure'),('Cloud','AWS'),('Runtime','Kubernetes / Docker / Linux'),('Delivery','GitHub Actions / Flux CD'),('IaC','Terraform'),('Observe','Prometheus / Grafana / Loki'),('Approach','Automate. Observe. Improve.')]
for i,(key,value) in enumerate(rows):
    body+=f'<g class="line" style="--d:{.35+i*.16:.2f}s">'+t(24,125+i*27,key,12,GREEN)+t(103,125+i*27,':',12,MUTED)+t(120,125+i*27,value,11.5)+'</g>'
for i,c in enumerate(['#233237','#648b80','#74e5b5','#a9c6b2','#7499b3','#b3a0bf','#d8c28d','#dae5e4']):
    body+=f'<rect x="{24+i*27}" y="376" width="27" height="15" fill="{c}"/>'
body+=t(24,419,'$ less toil; more engineering_',11,MUTED)
save('info-card.svg',frame(490,438,'Jishan Mulla DevOps neofetch information card',body))

data=json.loads((ROOT/'data/contributions.json').read_text())
days=data['days']; start=dt.date.fromisoformat(days[0]['date'])
start-=dt.timedelta(days=(start.weekday()+1)%7)
active=sum(d['level']>0 for d in days)
best=run=0
for d in days:
    run=run+1 if d['level'] else 0
    best=max(best,run)
weeks=(dt.date.fromisoformat(days[-1]['date'])-start).days//7+1
step=min(14.8,790/weeks)
palette=['#17252a','#20483d','#2a785b','#43b984','#83efbc']
body=bar(880,'contributions --last-year')
body+=t(25,69,'A year of shipping, one day at a time.',16,INK)
last_month=None
for d in days:
    date=dt.date.fromisoformat(d['date']); delta=(date-start).days; week,row=divmod(delta,7)
    x=51+week*step; y=112+row*17
    if date.day<=7 and date.month!=last_month and row==0:
        body+=t(x,100,date.strftime('%b'),9,MUTED); last_month=date.month
    body+=f'<rect class="cell" style="--d:{week*.018+row*.026:.3f}s" x="{x:.2f}" y="{y}" width="{step-3:.2f}" height="13" rx="2.5" fill="{palette[d["level"]]}"><title>{date}: activity level {d["level"]}</title></rect>'
for label,row in [('Mon',1),('Wed',3),('Fri',5)]:body+=t(14,122+row*17,label,9,MUTED)
body+='<path d="M25 245H855" stroke="#233237"/>'
body+=t(25,271,f'{active} active days',12,GREEN)+t(225,271,f'{best}-day longest active streak',11,INK)
body+=t(25,295,'Publicly visible activity · '+data['updated']+' UTC',10,MUTED)
body+=t(665,271,'Less',9,MUTED)
for i,c in enumerate(palette):body+=f'<rect x="{697+i*20}" y="261" width="13" height="13" rx="2" fill="{c}"/>'
body+=t(807,271,'More',9,MUTED)
save('contributions.svg',frame(880,318,'Publicly visible GitHub activity for JISHAN-HI',body))

# Content-based image versions avoid keeping an older calendar in README caches.
readme=ROOT/'README.md'
if readme.exists():
    content=readme.read_text(encoding='utf-8')
    for name in ['devops-ascii.svg','info-card.svg','contributions.svg']:
        digest=hashlib.sha256((ASSETS/name).read_bytes()).hexdigest()[:12]
        content=re.sub(r'assets/'+re.escape(name)+r'(?:\?v=[^"\s]*)?',f'assets/{name}?v={digest}',content)
    readme.write_text(content,encoding='utf-8')
print(f'Built terminal profile: {active} active days; longest active streak {best} days.')
