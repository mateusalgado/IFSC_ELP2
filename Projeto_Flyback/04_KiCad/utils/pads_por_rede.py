"""Lista as coordenadas absolutas dos pads por rede (para desenhar as rotas em rotas.py)."""
import json
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from placement import POS, pad_abs
from sexp import parse, find, find_all

info = json.loads((HERE / "fp_info.json").read_text(encoding="utf-8"))
doc = parse((HERE / "netlist.net").read_text(encoding="utf-8"))[0]
comps = {str(find(c, "ref")[1]): str(find(c, "footprint")[1]) for c in find_all(find(doc, "components"), "comp")}
nets = {}
for n in find_all(find(doc, "nets"), "net"):
    name = str(find(n, "name")[1])
    for node in find_all(n, "node"):
        nets.setdefault(name, []).append((str(find(node, "ref")[1]), str(find(node, "pin")[1])))
for name in sorted(nets):
    items = []
    for ref, pin in nets[name]:
        fp = comps[ref]
        pads = pad_abs(fp, *POS[ref], info)
        if pin in pads:
            items.append(f"{ref}.{pin}@({pads[pin][0]:.2f},{pads[pin][1]:.2f})")
    print(f"{name:16} {' '.join(items)}")
