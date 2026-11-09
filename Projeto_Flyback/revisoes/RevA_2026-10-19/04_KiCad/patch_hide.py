"""Formato KiCad 10: (hide yes) como filho da propriedade; remove 'hide' de dentro de effects."""
from pathlib import Path
p = Path(__file__).resolve().parent / "gera_sch.py"
s = p.read_text(encoding="utf-8")
reps = [
    ('["property", QStr("Footprint"), QStr(FP["TRAFO"]), ["at", 0, 0, 0], ["effects", ["font", ["size", 1.27, 1.27]], "hide"]],',
     '["property", QStr("Footprint"), QStr(FP["TRAFO"]), ["at", 0, 0, 0], ["hide", "yes"], ["effects", ["font", ["size", 1.27, 1.27]]]],'),
    ('["property", QStr("Datasheet"), QStr(""), ["at", 0, 0, 0], ["effects", ["font", ["size", 1.27, 1.27]], "hide"]],\n    ]',
     '["property", QStr("Datasheet"), QStr(""), ["at", 0, 0, 0], ["hide", "yes"], ["effects", ["font", ["size", 1.27, 1.27]]]],\n    ]'),
    ('["property", QStr("Footprint"), QStr(footprint), ["at", x, y, 0], ["effects", ["font", ["size", 1.27, 1.27]], "hide"]],',
     '["property", QStr("Footprint"), QStr(footprint), ["at", x, y, 0], ["hide", "yes"], ["effects", ["font", ["size", 1.27, 1.27]]]],'),
    ('["property", QStr("Datasheet"), QStr(""), ["at", x, y, 0], ["effects", ["font", ["size", 1.27, 1.27]], "hide"]]]',
     '["property", QStr("Datasheet"), QStr(""), ["at", x, y, 0], ["hide", "yes"], ["effects", ["font", ["size", 1.27, 1.27]]]]]'),
    ('sym.append(["property", QStr(k), QStr(v), ["at", x, y, 0], ["effects", ["font", ["size", 1.27, 1.27]], "hide"]])',
     'sym.append(["property", QStr(k), QStr(v), ["at", x, y, 0], ["hide", "yes"], ["effects", ["font", ["size", 1.27, 1.27]]]])'),
]
for a, b in reps:
    assert a in s, a[:60]
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8")
print("ok")
