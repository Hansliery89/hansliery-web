import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from base import page
import docs1,docs2,docs3,docs4
from playwright.sync_api import sync_playwright
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")+"/"; os.makedirs(OUT,exist_ok=True)
ALL={**docs1.D,**docs2.D,**docs3.D,**docs4.D}
FT='<div style="width:100%;font-family:Arial;font-size:7px;color:#7F93AC;padding:0 14mm;display:flex;justify-content:space-between"><span>HANSLIERY SÁNCHEZ · COMPLIANCE &amp; RISK ADVISORY · {t}</span><span>Documento modelo · <span class="pageNumber"></span>/<span class="totalPages"></span></span></div>'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome"); pg=b.new_page()
    for slug,(t,k,s,body,land) in ALL.items():
        h="/tmp/entregables_html/"+slug+".html"; os.makedirs(os.path.dirname(h),exist_ok=True)
        open(h,"w",encoding="utf-8").write(page(t,k,s,body,land))
        pg.goto("file://"+h); pg.evaluate("document.fonts.ready")
        pg.pdf(path=OUT+slug+".pdf",format="A4",landscape=land,print_background=True,prefer_css_page_size=True,display_header_footer=True,header_template="<span></span>",footer_template=FT.format(t=t))
        print(slug,os.path.getsize(OUT+slug+".pdf")//1024,"KB")
    b.close()
