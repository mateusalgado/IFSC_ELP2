"""Monta o relatorio: RELATORIO.md (+ tabelas/*.md nos marcadores {{nome}}) -> RELATORIO_VISUAL.html (pandoc) -> RELATORIO_MATEUS_SALGADO_PROJETO.pdf (Chrome headless).
Uso (Windows): "C:\\Program Files\\KiCad\\10.0\\bin\\python.exe" build.py [arquivo.md] [saida_base]
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PANDOC = Path.home() / "AppData/Local/Pandoc/pandoc.exe"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
CSS = """
<style>
  @page { size: A4; margin: 1.8cm 1.8cm; }
  * { box-sizing: border-box; }
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.5; color: #1a1a1a; background: #fff; font-size: 10.5pt; margin: 0; max-width: none !important; padding: 0 !important; }
  .container { max-width: 960px; margin: 0 auto; padding: 0 10px; }
  h1 { font-size: 1.6em; font-weight: 600; margin: 0 0 10px 0; }
  h2 { font-size: 1.3em; font-weight: 600; margin-top: 22px; margin-bottom: 8px; padding-bottom: 3px; border-bottom: 1px solid #ccc; break-after: avoid; }
  h3 { font-size: 1.08em; font-weight: 600; margin-top: 16px; margin-bottom: 6px; break-after: avoid; }
  p { margin: 0 0 8px 0; text-align: justify; }
  ul, ol { margin: 0 0 8px 22px; padding: 0; }
  li { margin-bottom: 2px; text-align: justify; }
  table { width: 100%; border-collapse: collapse; margin: 8px 0 12px 0; font-size: 0.8em; }
  tr { break-inside: avoid; }
  th { border-bottom: 1.5px solid #333; padding: 3px 4px; text-align: left; font-weight: 600; background: #f3f3f3; }
  td { padding: 2px 4px; border-bottom: 1px solid #ddd; vertical-align: top; }
  figure { text-align: center; margin: 10px 0 14px 0; break-inside: avoid; }
  figure img { max-width: 92%; max-height: 400px; border: 1px solid #ddd; }
  figcaption { font-size: 0.88em; color: #444; margin-top: 4px; }
  code { font-family: 'Courier New', monospace; font-size: 0.92em; background: #f6f6f6; padding: 0 3px; }
  pre { font-family: 'Courier New', monospace; font-size: 0.85em; border: 1px solid #bbb; background: #fcfcfc; padding: 8px 12px; }
  blockquote { border-left: 3px solid #c33; margin: 8px 0; padding: 4px 12px; background: #fff6f6; }
  .header-info p { margin: 2px 0; }
  sub, sup { font-size: 0.75em; }
  @media print { a { color: inherit; text-decoration: none; } }
</style>
"""


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "RELATORIO.md"
    base = sys.argv[2] if len(sys.argv) > 2 else "RELATORIO_VISUAL"
    md = src.read_text(encoding="utf-8")
    tabdir = src.parent / "tabelas"

    def sub(m):
        p = tabdir / (m.group(1) + ".md")
        return p.read_text(encoding="utf-8") if p.exists() else m.group(0)
    md = re.sub(r"\{\{(\w+)\}\}", sub, md)
    tmp = src.parent / "_relatorio_tmp.md"
    tmp.write_text(md, encoding="utf-8")
    hdr = src.parent / "_css.html"
    hdr.write_text(CSS, encoding="utf-8")
    html = src.parent / (base + ".html")
    subprocess.run([str(PANDOC), str(tmp), "-f", "markdown+pipe_tables+implicit_figures+raw_html", "-t", "html5", "--standalone",
                    "--metadata", "title=Projeto Semestral EPO II 2026-2", "--metadata", "lang=pt-BR", "-H", str(hdr), "-o", str(html)], check=True)
    h = html.read_text(encoding="utf-8")
    h = h.replace("<body>", "<body><div class=\"container\">").replace("</body>", "</div></body>")
    h = re.sub(r"<header id=\"title-block-header\">.*?</header>", "", h, flags=re.S)
    html.write_text(h, encoding="utf-8")
    pdf = src.parent / "RELATORIO_MATEUS_SALGADO_PROJETO.pdf"   # convencao das tarefas (o HTML intermediario continua RELATORIO_VISUAL.html)
    subprocess.run([str(CHROME), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--print-to-pdf=" + str(pdf), "--run-all-compositor-stages-before-draw",
                    "--virtual-time-budget=20000", html.resolve().as_uri()], check=True, capture_output=True)
    tmp.unlink(); hdr.unlink()
    print("ok:", html.name, pdf.name, f"{pdf.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
