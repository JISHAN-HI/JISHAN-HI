"""Generate self-contained profile SVGs. Python 3.11+, no packages required."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)

def text(x, y, content, size=14, color='#9cacbf', extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extra}>{escape(str(content))}</text>'

def svg(name, height, title, body):
    header = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">Animated DevOps profile artwork for Jishan Mulla. Decorative animations, not live infrastructure status.</desc>
<defs><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M 32 0 L 0 0 0 32" fill="none" stroke="#172536" stroke-width="0.6"/></pattern><linearGradient id="fade"><stop stop-color="#123743"/><stop offset="1" stop-color="#0c1420"/></linearGradient></defs>
<style>text{{font-family:Consolas,'Liberation Mono',monospace}}.reveal{{animation:appear .7s both;animation-delay:var(--d,0s)}}@keyframes appear{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}.trace{{stroke-dasharray:1400;animation:draw 2s ease-out both}}@keyframes draw{{from{{stroke-dashoffset:1400}}to{{stroke-dashoffset:0}}}}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<rect x="1" y="1" width="998" height="{height-2}" rx="18" fill="#0c1420" stroke="#243549"/><rect x="2" y="2" width="996" height="{height-4}" rx="18" fill="url(#grid)"/>
'''
    (OUT/name).write_text(header+body+'</svg>', encoding='utf-8')

body = '<path d="M1 48H999" stroke="#243549"/>'
for i,c in enumerate(['#ff6b78','#e8bb66','#57d6ad']):
    body += f'<circle cx="{26+i*20}" cy="25" r="5" fill="{c}"/>'
body += text(112,30,'jishan@github:~ / infrastructure-terminal',12)
body += text(824,30,'PROFILE / 01',11,'#56dac8')
body += '<rect x="36" y="83" width="212" height="222" rx="16" fill="url(#fade)" stroke="#2c5966"/>'
body += '<path class="trace" d="M61 122V108H83 M202 108H223V130 M61 267V281H83 M201 281H223V260" fill="none" stroke="#59e1cf" stroke-width="2"/>'
body += text(70,222,'JM',94,'#e3f9f5','font-weight="bold" class="reveal"')
body += text(86,258,'&gt;_'.replace('&gt;','>'),20,'#57d6ad')
body += '<g class="reveal" style="--d:.25s">'+text(285,101,'ENGINEERING / OPERATIONS / AUTOMATION',11,'#57d6ad')+text(281,158,'JISHAN MULLA',47,'#eef5ff','font-weight="bold"')+text(285,195,'DevOps Engineer',21,'#6ed7ee')+'</g>'
body += '<g class="reveal" style="--d:.6s">'+text(285,236,'From source code to dependable infrastructure.',16,'#c3cfdd')+text(285,265,'Cloud + on-prem Kubernetes. Repeatable delivery.',14)+text(285,289,'Observe. Diagnose. Automate. Improve.',14)+'</g>'
body += '<path d="M36 332H964" stroke="#243549"/>'
body += text(36,366,'01 / BUILD',12,'#57d6ad')+text(357,366,'02 / OPERATE',12,'#6ed7ee')+text(692,366,'03 / IMPROVE',12,'#c1a5ff')
body += text(36,393,'Pipelines & infrastructure',13)+text(357,393,'Clusters & observability',13)+text(692,393,'Automation & recovery',13)
svg('control-room.svg',426,'Jishan Mulla — DevOps Engineer',body)

body = text(32,38,'DELIVERY PATH',12,'#57d6ad')+text(740,38,'WORKFLOW ILLUSTRATION',11)
body += text(32,73,'Commit to confidence.',25,'#edf5ff','font-weight="bold"')
stages=[('01','SOURCE','Git / GitHub'),('02','BUILD','GitHub Actions'),('03','PACKAGE','Docker'),('04','DEPLOY','Kubernetes'),('05','OBSERVE','Metrics / Logs')]
for i,(number,label,stack) in enumerate(stages):
    x=32+i*191
    if i<4: body+=f'<path d="M{x+173} 143h18" stroke="#57d6ad" stroke-width="2" class="trace"/>'
    body+=f'<g class="reveal" style="--d:{i*.25}s"><rect x="{x}" y="103" width="173" height="113" rx="10" fill="#101e2c" stroke="#2a4659"/>'
    body+=text(x+15,129,number,11,'#57d6ad')+text(x+15,161,label,17,'#edf5ff')+text(x+15,191,stack,11)+'</g>'
body+=text(32,253,'AUTOMATE THE REPETITION. KEEP THE ENGINEERING.',12,'#6ed7ee')
svg('delivery-path.svg',280,'Delivery workflow: source, build, package, deploy, observe',body)

body = text(32,39,'CONTRIBUTION SIGNAL',12,'#57d6ad')
datafile=ROOT/'data/contributions.json'
if datafile.exists():
    import datetime
    data=json.loads(datafile.read_text())
    days=data['days']
    start=datetime.date.fromisoformat(days[0]['date'])
    start-=datetime.timedelta(days=(start.weekday()+1)%7)
    palette=['#172637','#164840','#197361','#32ac87','#65e5b5']
    weeks=max((datetime.date.fromisoformat(d['date'])-start).days//7 for d in days)+1
    step=min(17,920/weeks)
    for d in days:
        delta=(datetime.date.fromisoformat(d['date'])-start).days
        x=40+(delta//7)*step; y=93+(delta%7)*18
        body+=f'<rect class="reveal" style="--d:{min(delta//7*.012, .7):.3f}s" x="{x}" y="{y}" width="{step-3}" height="14" rx="3" fill="{palette[d["level"]]}"><title>{d["date"]}: activity level {d["level"]}</title></rect>'
    body+=text(32,67,'Public GitHub contribution calendar',16,'#edf5ff')
    body+=text(32,252,'Snapshot: '+data['updated']+' UTC',11)
    body+=text(663,252,'LESS',10)
    for i,c in enumerate(palette): body+=f'<rect x="{707+i*20}" y="241" width="14" height="14" rx="3" fill="{c}"/>'
    body+=text(818,252,'MORE',10)
else:
    body+=text(32,99,'Your activity belongs here.',27,'#edf5ff')
    body+=text(32,147,'Awaiting the first GitHub Actions refresh.',15,'#6ed7ee')
    body+=text(32,180,'The workflow will fetch your real public contribution calendar.',13)
    body+=text(32,239,'NO SAMPLE COUNTS / NO INVENTED STATS',11,'#57d6ad')
svg('contributions.svg',280,'GitHub contribution activity for JISHAN-HI',body)
print('Generated three SVG assets.')
