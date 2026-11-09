"""Monta o relatorio: RELATORIO.md (+ tabelas/*.md nos marcadores {{nome}}) -> RELATORIO_VISUAL.html (pandoc, imagens embutidas)
-> RELATORIO_MATEUS_SALGADO_PROJETO.pdf (Chrome headless).
Uso (Windows): "C:\\Program Files\\KiCad\\10.0\\bin\\python.exe" build.py [arquivo.md] [saida_base]

Pos-processamento do HTML: marcas de origem [C] [S] [CAD] [M] viram etiquetas coloridas; "atende"/"NAO atende" nas tabelas
viram estados verde/vermelho/ambar; o HTML e autossuficiente (imagens em base64), por isso abre em qualquer lugar.
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
  :root { --ink:#111111; --muted:#555b63; --line:#d6d9dd; --soft:#f4f5f7; --accent:#111111; --accent2:#ececee;
          --ok:#1a7f37; --bad:#b42318; --warn:#9a6700; --c:#3a3f45; --s:#1a7f37; --cad:#6f42c1; --m:#c2410c; }
  @page { size: A4; margin: 1.6cm 1.7cm 1.7cm 1.7cm; }
  * { box-sizing: border-box; }
  html, body { background: #fff; }
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.45; color: var(--ink); font-size: 10.2pt; margin: 0; max-width: none !important; padding: 0 !important; }
  .container { max-width: 980px; margin: 0 auto; padding: 0 8px; }
  h1 { font-size: 1.55em; font-weight: 650; margin: 0 0 6px 0; line-height: 1.25; color: var(--accent); }
  h2 { font-size: 1.28em; font-weight: 650; margin: 24px 0 10px 0; padding-bottom: 4px; border-bottom: 2px solid var(--accent); color: var(--ink); break-after: avoid; }
  h2.pb, .pb { break-before: page; }
  h3 { font-size: 1.08em; font-weight: 650; margin: 18px 0 6px 0; color: var(--accent); break-after: avoid; }
  h4 { font-size: 0.98em; font-weight: 650; margin: 12px 0 4px 0; break-after: avoid; }
  p { margin: 0 0 7px 0; text-align: justify; }
  ul, ol { margin: 0 0 8px 20px; padding: 0; }
  li { margin-bottom: 2px; text-align: justify; }
  a { color: var(--ink); }
  /* --- cabecalho --- */
  .titlecard { border: 1px solid var(--line); border-left: 6px solid var(--accent); border-radius: 6px; padding: 12px 16px; margin: 0 0 12px 0; background: var(--soft); }
  .titlecard table.meta { width: auto; min-width: 70%; margin: 6px 0 0 0; font-size: 0.9em; }
  .titlecard table.meta td { border: 0; padding: 1px 14px 1px 0; background: transparent; }
  .titlecard table.meta td:first-child { white-space: nowrap; color: var(--muted); }
  .titlecard p { margin: 2px 0; color: var(--muted); font-size: 0.9em; text-align: left; }
  .kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin: 10px 0 14px 0; }
  .kpi { border: 1px solid var(--line); border-radius: 6px; padding: 7px 10px; background: #fff; break-inside: avoid; }
  .kpi .l { font-size: 0.72em; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); }
  .kpi .v { font-size: 1.12em; font-weight: 650; color: var(--accent); margin-top: 1px; }
  .kpi .d { font-size: 0.78em; color: var(--muted); }
  /* --- etiquetas de origem e estados --- */
  .badge { display: inline-block; font-size: 0.68em; font-weight: 700; letter-spacing: 0.03em; padding: 0 5px; border-radius: 3px; color: #fff; vertical-align: 0.12em; line-height: 1.5; }
  .b-C { background: var(--c); } .b-S { background: var(--s); } .b-CAD { background: var(--cad); } .b-M { background: var(--m); }
  .ok { color: var(--ok); font-weight: 650; } .bad { color: var(--bad); font-weight: 650; } .warn { color: var(--warn); font-weight: 650; }
  .legend { font-size: 0.86em; color: var(--muted); border: 1px dashed var(--line); border-radius: 6px; padding: 6px 10px; margin: 6px 0 10px 0; }
  /* --- memoria de calculo --- */
  .calc { border: 1px solid var(--line); border-radius: 6px; background: #fbfcfd; padding: 8px 12px 6px 12px; margin: 8px 0 12px 0; break-inside: avoid; }
  .calc .t { font-weight: 650; color: var(--accent); font-size: 0.95em; margin-bottom: 4px; }
  .calc .t span { font-weight: 400; color: var(--muted); font-size: 0.9em; margin-left: 6px; }
  .eq { font-family: 'Cambria Math', Cambria, 'Times New Roman', serif; font-size: 1.02em; margin: 3px 0 3px 10px; line-height: 1.5; }
  .eq .res { font-weight: 700; color: var(--accent); }
  .eq .why { font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 0.82em; color: var(--muted); margin-left: 8px; }
  .step { display: grid; grid-template-columns: 1.6em 1fr; gap: 0 6px; margin: 2px 0; }
  .step .n { color: var(--muted); font-size: 0.85em; text-align: right; padding-top: 2px; }
  /* --- caixas --- */
  .note { border-left: 4px solid var(--accent); background: var(--accent2); padding: 6px 12px; margin: 8px 0 10px 0; font-size: 0.95em; break-inside: avoid; }
  .alert { border-left: 4px solid var(--bad); background: #fff5f4; padding: 6px 12px; margin: 8px 0 10px 0; font-size: 0.95em; break-inside: avoid; }
  blockquote { border-left: 4px solid var(--accent); margin: 8px 0; padding: 4px 12px; background: var(--accent2); }
  /* --- tabelas --- */
  table { width: 100%; border-collapse: collapse; margin: 6px 0 12px 0; font-size: 0.8em; }
  tr { break-inside: avoid; }
  th { border-bottom: 1.5px solid var(--accent); padding: 4px 5px; text-align: left; font-weight: 650; background: var(--accent2); vertical-align: bottom; }
  td { padding: 3px 5px; border-bottom: 1px solid var(--line); vertical-align: top; }
  tbody tr:nth-child(even) td { background: #fafbfc; }
  table.spec td:first-child { font-weight: 600; white-space: nowrap; }
  td.num, th.num { text-align: right; white-space: nowrap; }
  caption, .tcap { caption-side: top; text-align: left; font-size: 0.86em; font-weight: 650; color: var(--ink); margin: 6px 0 2px 0; }
  /* --- figuras --- */
  figure { text-align: center; margin: 8px 0 12px 0; break-inside: avoid; }
  figure img { max-width: 94%; max-height: 360px; border: 1px solid var(--line); border-radius: 4px; }
  figcaption { font-size: 0.85em; color: var(--muted); margin-top: 4px; text-align: center; }
  .fig2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; align-items: start; }
  .fig2 figure { margin: 4px 0 8px 0; }
  .fig2 figure img { max-width: 100%; max-height: 300px; }
  .wide figure img { max-width: 100%; max-height: 520px; }
  code { font-family: 'Consolas', 'Courier New', monospace; font-size: 0.9em; background: #f1f3f5; padding: 0 3px; border-radius: 3px; }
  pre { font-family: 'Consolas', 'Courier New', monospace; font-size: 0.85em; border: 1px solid var(--line); background: #fcfcfc; padding: 8px 12px; }
  sub, sup { font-size: 0.74em; line-height: 0; }
  .small { font-size: 0.88em; color: var(--muted); }
  @media print { a { color: inherit; text-decoration: none; } .kpi, .calc, .note, .alert { -webkit-print-color-adjust: exact; print-color-adjust: exact; } th, .badge, tbody tr:nth-child(even) td, .titlecard { -webkit-print-color-adjust: exact; print-color-adjust: exact; } }
</style>
"""


def monta_capa(h):
    """h1 + instituicao + tabela de identificacao -> .titlecard; tabela 'Indicador | Valor | Observacao' -> painel .kpis"""
    m = re.search(r"(<h1[^>]*>.*?</h1>)(\s*<p>.*?</p>)?(\s*<table>.*?</table>)", h, flags=re.S)
    if m:
        tab = re.sub(r"<table>", '<table class="meta">', m.group(3), count=1)
        tab = re.sub(r"<thead>.*?</thead>", "", tab, flags=re.S)
        h = h[:m.start()] + '<div class="titlecard">' + m.group(1) + (m.group(2) or "") + tab + "</div>" + h[m.end():]
    k = re.search(r"<table>\s*<thead>\s*<tr[^>]*>\s*<th[^>]*>Indicador</th>.*?</table>", h, flags=re.S)
    if k:
        corpo = re.search(r"<tbody>(.*?)</tbody>", k.group(0), flags=re.S)
        tiles = []
        for row in re.findall(r"<tr[^>]*>(.*?)</tr>", corpo.group(1) if corpo else "", flags=re.S):
            cels = re.findall(r"<td[^>]*>(.*?)</td>", row, flags=re.S)
            if len(cels) >= 3:
                tiles.append(f'<div class="kpi"><div class="l">{cels[0].strip()}</div><div class="v">{cels[1].strip()}</div><div class="d">{cels[2].strip()}</div></div>')
        h = h[:k.start()] + '<div class="kpis">' + "".join(tiles) + "</div>" + h[k.end():]
        h = re.sub(r"<p><strong>Indicadores do projeto</strong></p>\s*", "", h, count=1)
    return h


def pos_processa(h):
    h = monta_capa(h)
    # etiquetas de origem: [C] [S] [CAD] [M] - so no texto, nunca dentro de tags (alt="..." das figuras)
    partes = re.split(r"(<[^>]+>)", h)
    for i in range(0, len(partes), 2):
        partes[i] = re.sub(r"\[(C|S|CAD|M)\](?!\()", lambda m: f'<span class="badge b-{m.group(1)}">{m.group(1)}</span>', partes[i])
    h = "".join(partes)
    # estados nas tabelas de criterios/aceite
    h = re.sub(r"<td>(NÃO atende[^<]*)</td>", r'<td><span class="bad">\1</span></td>', h)
    h = re.sub(r"<td>(atende com ressalva[^<]*|atende o cálculo[^<]*)</td>", r'<td><span class="warn">\1</span></td>', h)
    h = re.sub(r"<td>(atende(?: a meta)?)</td>", r'<td><span class="ok">\1</span></td>', h)
    # quebra de pagina antes das secoes principais (menos a primeira)
    h = re.sub(r'<h2 id="([^"]+)">', lambda m: f'<h2 id="{m.group(1)}" class="pb">' if m.group(1) not in ("introdução", "introducao") else m.group(0), h)
    return h


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
    subprocess.run([str(PANDOC), str(tmp), "-f", "markdown+pipe_tables+implicit_figures+raw_html+table_captions", "-t", "html5", "--standalone", "--embed-resources",
                    "--resource-path", str(src.parent), "--metadata", "title=Projeto Semestral EPO II 2026-2 – Fonte flyback 12 V / 3 A (UC3845) – Revisão B",
                    "--metadata", "lang=pt-BR", "-H", str(hdr), "-o", str(html)], check=True, cwd=str(src.parent))
    h = html.read_text(encoding="utf-8")
    h = h.replace("<body>", "<body><div class=\"container\">").replace("</body>", "</div></body>")
    h = re.sub(r"<header id=\"title-block-header\">.*?</header>", "", h, flags=re.S)
    h = pos_processa(h)
    html.write_text(h, encoding="utf-8")
    pdf = src.parent / "RELATORIO_MATEUS_SALGADO_PROJETO.pdf"   # convencao das tarefas (o HTML intermediario continua RELATORIO_VISUAL.html)
    subprocess.run([str(CHROME), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--print-to-pdf=" + str(pdf), "--run-all-compositor-stages-before-draw",
                    "--virtual-time-budget=20000", html.resolve().as_uri()], check=True, capture_output=True)
    tmp.unlink(); hdr.unlink()
    print("ok:", html.name, f"{html.stat().st_size / 1e6:.1f} MB (imagens embutidas)", pdf.name, f"{pdf.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
