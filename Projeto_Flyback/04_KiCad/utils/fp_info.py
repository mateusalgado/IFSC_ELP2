"""Roda com o Python do KiCad (pcbnew): lista caixa envolvente (courtyard/bbox) e pads dos footprints usados.
Uso: "C:\\Program Files\\KiCad\\10.0\\bin\\python.exe" utils\\fp_info.py  (a partir de 04_KiCad)
"""
import json
import sys
from pathlib import Path
import pcbnew

HERE = Path(__file__).resolve().parent.parent   # 04_KiCad (netlist.net, fonte.pretty, fp_info.json)
LIBROOT = Path(r"C:\Program Files\KiCad\10.0\share\kicad\footprints")
import re
txt = (HERE / "netlist.net").read_text(encoding="utf-8")
fps = sorted(set(re.findall(r'\(footprint "([^"]+)"\)', txt)) - {""})
out = {}
for fp in fps:
    lib, name = fp.split(":")
    libpath = str(HERE / "fonte.pretty") if lib == "fonte" else str(LIBROOT / f"{lib}.pretty")
    m = pcbnew.FootprintLoad(libpath, name)
    if m is None:
        print("NAO ENCONTRADO", fp); continue
    bb = m.GetBoundingBox(False, False)
    cy = m.GetCourtyard(pcbnew.F_CrtYd).BBox() if hasattr(m, "GetCourtyard") else bb
    pads = []
    for p in m.Pads():
        pos = p.GetPosition()
        pads.append(dict(num=p.GetNumber(), x=pos.x / 1e6, y=pos.y / 1e6, sx=p.GetSizeX() / 1e6 if hasattr(p, "GetSizeX") else p.GetSize().x / 1e6,
                         sy=p.GetSizeY() / 1e6 if hasattr(p, "GetSizeY") else p.GetSize().y / 1e6, drill=p.GetDrillSizeX() / 1e6 if p.GetDrillSizeX() else 0))
    out[fp] = dict(w=bb.GetWidth() / 1e6, h=bb.GetHeight() / 1e6, x0=bb.GetX() / 1e6, y0=bb.GetY() / 1e6,
                   cw=cy.GetWidth() / 1e6, ch=cy.GetHeight() / 1e6, cx0=cy.GetX() / 1e6, cy0=cy.GetY() / 1e6, pads=pads)
    print(f"{fp:75} crt {cy.GetWidth()/1e6:6.1f} x {cy.GetHeight()/1e6:6.1f} mm  pads: " + " ".join(f"{p['num']}({p['x']:.2f},{p['y']:.2f})" for p in pads[:6]))
(HERE / "fp_info.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print("pcbnew", pcbnew.GetBuildVersion())
