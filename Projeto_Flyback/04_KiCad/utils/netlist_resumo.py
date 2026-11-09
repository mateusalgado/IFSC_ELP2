"""Imprime as redes da netlist exportada pelo kicad-cli (netlist.net)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sexp import parse, find, find_all

doc = parse(Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "netlist.net").read_text(encoding="utf-8"))[0]
nets = find(doc, "nets")
lst = find_all(nets, "net")
print("redes:", len(lst))
for n in lst:
    name = find(n, "name")[1]
    nodes = [f"{find(x, 'ref')[1]}.{find(x, 'pin')[1]}" for x in find_all(n, "node")]
    print(f"{str(name):14} ({len(nodes):2}): {' '.join(nodes)}")
