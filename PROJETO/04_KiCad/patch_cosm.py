"""Cosmetica do esquematico: texto horizontal em simbolos rotacionados, refs de #PWR/#FLG ocultas, textos movidos."""
from pathlib import Path
p = Path(__file__).resolve().parent / "gera_sch.py"
s = p.read_text(encoding="utf-8")
old = '''        dx = 2.54 if rot in (0, 180) else 0
        dy = -1.27 if rot in (0, 180) else -3.81
        sym = ["symbol", ["lib_id", QStr(lib_id)], ["at", x, y, rot], ["unit", 1], ["exclude_from_sim", "no"], ["in_bom", "yes" if in_bom else "no"],
               ["on_board", "yes"], ["dnp", "no"], ["uuid", U()],
               ["property", QStr("Reference"), QStr(ref), ["at", x + dx, y + dy, 0], ["effects", ["font", ["size", 1.27, 1.27]], ["justify", "left"]]],
               ["property", QStr("Value"), QStr(value), ["at", x + dx, y + dy + 2.54, 0], ["effects", ["font", ["size", 1.0, 1.0]], ["justify", "left"]]],'''
new = '''        if rot in (0, 180):
            pr, pv, prot, just = (x + 2.54, y - 1.27), (x + 2.54, y + 1.27), 0, [["justify", "left"]]
        else:
            pr, pv, prot, just = (x, y - 3.3), (x, y + 3.3), (360 - rot) % 360, []
        hide_ref = [["hide", "yes"]] if ref.startswith("#") else []
        sym = ["symbol", ["lib_id", QStr(lib_id)], ["at", x, y, rot], ["unit", 1], ["exclude_from_sim", "no"], ["in_bom", "yes" if in_bom else "no"],
               ["on_board", "yes"], ["dnp", "no"], ["uuid", U()],
               ["property", QStr("Reference"), QStr(ref), ["at", pr[0], pr[1], prot]] + hide_ref + [["effects", ["font", ["size", 1.27, 1.27]]] + just],
               ["property", QStr("Value"), QStr(value), ["at", pv[0], pv[1], prot], ["effects", ["font", ["size", 1.0, 1.0]]] + just],'''
assert old in s
s = s.replace(old, new)
s = s.replace('s.text("Rsense 2 x 0,66 ohm", 200.66, 128.27, 1.5)', 's.text("Rsense 2 x 0,66 ohm (1 W)", 203.2, 135.89, 1.5)')
s = s.replace('s.text("VCC pelo auxiliar (15 V) + partida por R3/R4", 128.27, 125.73, 1.3)', 's.text("VCC pelo auxiliar (15 V) + partida por R3/R4", 128.27, 123.19, 1.3)')
s = s.replace('s.place("D1", "Device:D_Schottky_Dual_CommonCathode_AKA", VAL["D1"], FP["TO220"], 231.14, 55.88, 0)',
              's.place("D1", "Device:D_Schottky_Dual_CommonCathode_AKA", VAL["D1"], FP["TO220"], 231.14, 55.88, 0)\n    s.inst["D1"]["at"] = (231.14, 55.88)')
p.write_text(s, encoding="utf-8")
print("ok")
