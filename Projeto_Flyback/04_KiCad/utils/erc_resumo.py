"""Resumo legivel do erc.json (kicad-cli sch erc --format json)."""
import json, collections, sys
from pathlib import Path
p = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "erc.json")
e = json.loads(p.read_text(encoding="utf-8"))
sh = e["sheets"][0]["violations"]
print(collections.Counter((v["severity"], v["type"]) for v in sh))
for v in sh:
    its = []
    for i in v.get("items", []):
        pos = i.get("pos", {})
        its.append(f"{i.get('description','')[:50]} @({pos.get('x', 0):.2f},{pos.get('y', 0):.2f})")
    print(f"{v['severity']:7} {v['type']:28} | {v['description'][:70]} | {' ; '.join(its[:3])}")
