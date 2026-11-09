"""Troca o parser de netlist (regex) por sexp.parse em gera_pcb.py."""
from pathlib import Path
p = Path(__file__).resolve().parent / "gera_pcb.py"
s = p.read_text(encoding="utf-8")
i0 = s.index("def parse_netlist(path):")
i1 = s.index("# ------------------------------------------------------------------ posicionamento")
new = '''def parse_netlist(path):
    """retorna {(ref, pin): netname}, {ref: (value, footprint)} a partir da netlist kicadsexpr"""
    sys.path.insert(0, str(HERE))
    from sexp import parse, find, find_all
    doc = parse(Path(path).read_text(encoding="utf-8"))[0]
    comps = {}
    for c in find_all(find(doc, "components"), "comp"):
        fp = find(c, "footprint")
        comps[str(find(c, "ref")[1])] = (str(find(c, "value")[1]), str(fp[1]) if fp else "")
    nets = {}
    for n in find_all(find(doc, "nets"), "net"):
        name = str(find(n, "name")[1])
        for node in find_all(n, "node"):
            nets[(str(find(node, "ref")[1]), str(find(node, "pin")[1]))] = name
    return nets, comps


'''
s = s[:i0] + new + s[i1:]
p.write_text(s, encoding="utf-8")
print("ok")
