import html as H
F="/home/claude/tools/node_modules/@fontsource/"
def ff(fam,w,name): return f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('file://{F}{name.lower()}/files/{name.lower()}-latin-{w}-normal.woff2') format('woff2');}}"
FONTS="".join(ff('Sora',w,'sora') for w in (400,600,700,800))+"".join(ff('Manrope',w,'manrope') for w in (400,500,600,700,800))
CSS=FONTS+"""
@page{size:A4;margin:16mm 14mm 18mm}
@page land{size:A4 landscape;margin:14mm 14mm 16mm}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Manrope,sans-serif;color:#0A192F;font-size:9.6pt;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body.land{page:land}
.hero{background:#0A192F;color:#FFFFFF;border-radius:10px;padding:16px 22px 17px;position:relative;overflow:hidden;margin-bottom:16px}
.hero:before{content:"";position:absolute;right:-60px;top:-80px;width:260px;height:260px;border-radius:50%;background:radial-gradient(circle,rgba(37,99,235,.45),transparent 65%)}
.hero:after{content:"";position:absolute;left:0;bottom:0;height:4px;width:100%;background:linear-gradient(90deg,#2563EB,#38BDF8 60%,#D4AF37)}
.brand{font-family:Sora;font-weight:800;font-size:8.5pt;letter-spacing:.18em;display:flex;justify-content:space-between;align-items:center;position:relative}
.brand span{color:#38BDF8}.brand i{font-style:normal;font-weight:600;letter-spacing:.12em;color:#64748B;font-size:7pt}
.kick{margin-top:16px;font-size:7.5pt;letter-spacing:.16em;text-transform:uppercase;color:#38BDF8;font-weight:700;position:relative}
.hero h1{font-family:Sora;font-weight:700;font-size:20pt;line-height:1.15;margin:4px 0 6px;position:relative}
.hero p{color:#CBD5E1;font-size:9.4pt;max-width:150mm;position:relative}
.badge{display:inline-block;margin-top:10px;font-size:7pt;font-weight:800;letter-spacing:.14em;text-transform:uppercase;padding:4px 10px;border-radius:99px;border:1px solid #D4AF37;color:#E9CF7A;position:relative}
h2{font-family:Sora;font-weight:700;font-size:12.5pt;color:#0A192F;margin:16px 0 7px;display:flex;align-items:center;gap:8px;break-after:avoid}
h2 b{font-size:8pt;color:#fff;background:#123B66;border-radius:5px;padding:2px 6px}
h3{font-family:Sora;font-weight:600;font-size:10pt;color:#123B66;margin:11px 0 5px;break-after:avoid}
p{margin:0 0 6px}ul.l,ol.l{margin:0 0 7px 15px}ul.l li,ol.l li{margin-bottom:2px}
table{width:100%;border-collapse:collapse;margin:4px 0 10px;font-size:8.3pt;break-inside:auto}
thead{display:table-header-group}tr{break-inside:avoid}
th{background:#123B66;color:#fff;text-align:left;font-weight:700;padding:5px 6px;font-size:7.6pt;letter-spacing:.02em}
td{padding:5px 6px;border-bottom:1px solid #E2E8F0;vertical-align:top}
tbody tr:nth-child(even) td{background:#F1F5F9}
td.c,th.c{text-align:center}
td:empty{height:22px}
.call{border-left:3px solid #2563EB;background:#EFF4FF;padding:8px 11px;border-radius:0 6px 6px 0;margin:7px 0 10px;font-size:8.8pt;break-inside:avoid}
.call.gold{border-color:#D4AF37;background:#FBF5E8}
.call.blue{border-color:#38BDF8;background:#EEF7FD}
.kv{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border:1px solid #E2E8F0;border-radius:6px;overflow:hidden;margin:4px 0 10px}
.kv div{padding:6px 9px;border-right:1px solid #E2E8F0;border-bottom:1px solid #E2E8F0;font-size:8.3pt}
.kv div b{display:block;font-size:6.8pt;letter-spacing:.1em;text-transform:uppercase;color:#64748B}
.kv div span{color:#94A3B8}
.fld{display:grid;grid-template-columns:repeat(2,1fr);gap:7px 14px;margin:4px 0 10px}
.fld.c3{grid-template-columns:repeat(3,1fr)}
.fld div{font-size:7.6pt;color:#475569;border-bottom:1px solid #CBD5E1;padding:12px 0 2px}
.fld div.w{grid-column:1/-1}
.chk{list-style:none;margin:2px 0 9px}
.chk li{padding-left:18px;position:relative;margin-bottom:3px}
.chk li:before{content:"";position:absolute;left:0;top:2px;width:10px;height:10px;border:1.4px solid #123B66;border-radius:2px}
.pill{display:inline-block;padding:1px 7px;border-radius:99px;font-size:7.2pt;font-weight:700;white-space:nowrap}
.p1{background:#DBEAFE;color:#1E40AF}.p2{background:#D9F0FD;color:#0B5A85}.p3{background:#FEF3C7;color:#7A5A00}.p4{background:#FFE4CC;color:#8A3B00}.p5{background:#FDDCDC;color:#8E1B1B}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.card{border:1px solid #E2E8F0;border-radius:8px;padding:10px 12px;break-inside:avoid;margin-bottom:9px}
.card h3{margin-top:0}
.steps{display:grid;gap:7px;margin:5px 0 10px}
.steps>div{display:grid;grid-template-columns:24px 1fr;gap:9px;align-items:start;break-inside:avoid}
.steps>div>em{font-style:normal;width:24px;height:24px;border-radius:50%;background:#2563EB;color:#FFFFFF;font-family:Sora;font-weight:700;font-size:8pt;display:grid;place-items:center}
.steps b{display:block}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:5px 0 10px}
.tiles div{background:#0A192F;color:#FFFFFF;border-radius:8px;padding:7px 11px}
.tiles b{display:block;font-family:Sora;font-size:14pt}
.tiles span{font-size:7.2pt;color:#CBD5E1}
.tiles i{display:block;height:4px;border-radius:3px;margin-top:6px}
.sign{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:26px}
.sign div{border-top:1px solid #475569;padding-top:4px;font-size:7.6pt;color:#475569;text-align:center}
.small{font-size:7.8pt;color:#475569}
.pb{break-before:page}
.gantt td{padding:4px 2px}.gantt td span:not(.pill){display:block;height:9px;margin-top:3px;border-radius:2px;background:#2563EB}
.gantt td span.o{background:#38BDF8}.gantt td span.d{background:#D4AF37}
.end{margin-top:14px;padding-top:8px;border-top:1px solid #E2E8F0;font-size:7.4pt;color:#64748B}
"""
def e(t): return H.escape(t)
def page(title,kicker,sub,body,land=False):
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{e(title)} · HANSLIERY SÁNCHEZ</title><style>{CSS}</style></head><body class="{'land' if land else ''}">
<div class="hero"><div class="brand"><div>HANSLIERY <span>SÁNCHEZ</span></div><i>COMPLIANCE &amp; RISK ADVISORY</i></div>
<div class="kick">{kicker}</div><h1>{title}</h1><p>{sub}</p><span class="badge">Documento modelo · ejemplo de entregable</span></div>
{body}
<div class="end">Documento modelo: los datos de ejemplo son ficticios. Cada entregable final se elabora a la medida de la entidad y no sustituye el criterio del oficial de cumplimiento ni de sus instancias de aprobación. · linkedin.com/in/hansliery-sanchez-figuereo-mlrm-b49ba254 · hansliery89.github.io/hansliery-web</div>
</body></html>"""
def tbl(head,rows,cls="",widths=None):
    th="".join(f'<th{(" style=width:"+widths[i]) if widths and widths[i] else ""}>{h}</th>' for i,h in enumerate(head))
    tr="".join("<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in rows)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'
def h2(n,t): return f"<h2><b>{n}</b>{t}</h2>" if n else f"<h2>{t}</h2>"
def ul(items,cls="l"): return f'<ul class="{cls}">'+"".join(f"<li>{i}</li>" for i in items)+"</ul>"
def ol(items): return '<ol class="l">'+"".join(f"<li>{i}</li>" for i in items)+"</ol>"
def kv(pairs): return '<div class="kv">'+"".join(f"<div><b>{a}</b>{b}</div>" for a,b in pairs)+"</div>"
def fld(items,c3=False): return f'<div class="fld{" c3" if c3 else ""}">'+"".join(f'<div{" class=w" if i.startswith("!") else ""}>{i.lstrip("!")}</div>' for i in items)+"</div>"
def steps(items): return '<div class="steps">'+"".join(f"<div><em>{i+1}</em><div><b>{a}</b>{b}</div></div>" for i,(a,b) in enumerate(items))+"</div>"
def call(t,c=""): return f'<div class="call {c}">{t}</div>'
PR={"Muy bajo":"p1","Bajo":"p2","Medio":"p3","Alto":"p4","Muy alto":"p5","Baja":"p2","Media":"p3","Alta":"p4","Crítica":"p5","Implementado":"p1","Parcial":"p3","No implementado":"p4","Cerrada":"p1","En curso":"p3","Pendiente":"p4","Sin coincidencia":"p1","Falso positivo":"p2","Potencial":"p3","Confirmada":"p5","Fuerte":"p1","Moderado":"p3","Débil":"p4"}
def pill(t): return f'<span class="pill {PR.get(t,"p2")}">{t}</span>'
PH='<span style="color:#94A3B8">[completar]</span>'
