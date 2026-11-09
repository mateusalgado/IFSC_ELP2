"""Ajusta o bloco do secundario em gera_sch.py para o simbolo D_Schottky_Dual_CommonCathode_AKA (A esq, K embaixo, A dir)."""
from pathlib import Path
p = Path(__file__).resolve().parent / "gera_sch.py"
s = p.read_text(encoding="utf-8")
s = s.replace('s.place("D1", "Device:D_Schottky_x2_KCom", VAL["D1"], FP["TO220"], 231.14, 55.88, 0)              # anodos esq, K dir',
              's.place("D1", "Device:D_Schottky_Dual_CommonCathode_AKA", VAL["D1"], FP["TO220"], 231.14, 55.88, 0)   # A esq, K embaixo, A dir')
s = s.replace('s.place("L2", "Device:L", VAL["L2"], FP["L_pos"], 284.48, 55.88, 90)                               # horizontal',
              's.place("L2", "Device:L", VAL["L2"], FP["L_pos"], 284.48, 60.96, 90)                               # horizontal')
old = s[s.index("    d1a1, d1k, d1a2 = P(\"D1\", 1), P(\"D1\", 2), P(\"D1\", 3)"):s.index("    # banco de capacitores")]
new = '''    d1a1, d1k, d1a2 = P("D1", 1), P("D1", 2), P("D1", 3)
    secx = t1s2[0] + 5.08
    s.wire(t1s2, (secx, t1s2[1])); s.wire(t1s2b, (secx, t1s2b[1])); s.junction((secx, t1s2[1]))
    s.wire((secx, t1s2b[1]), (secx, d1a1[1]), d1a1); s.junction((secx, d1a1[1]))
    # segundo anodo (direita) volta ao no SECN por cima do diodo
    s.wire(d1a2, (d1a2[0] + 2.54, d1a2[1]), (d1a2[0] + 2.54, 48.26), (secx, 48.26), (secx, d1a1[1]))
    s.label("SECN", (secx, 48.26), 90) if False else None
    # dot do secundario (S1) ao SGND
    sgx = t1s1[0] + 2.54
    s.wire(t1s1, (sgx, t1s1[1])); s.wire(t1s1b, (sgx, t1s1b[1])); s.junction((sgx, t1s1[1]))
    s.wire((sgx, t1s1[1]), (sgx, 91.44)); s.label("SGND", (sgx, 91.44), 270)
    # RC do diodo (entre SECN e VOUT)
    r15a, r15b, c9a, c9b = P("R15", 1), P("R15", 2), P("C9", 1), P("C9", 2)
    s.wire((secx, d1a1[1]), (secx, r15a[1]), r15a); s.wire(r15b, c9a)
    vouty = d1k[1]
    s.wire(c9b, (c9b[0] + 2.54, c9b[1]), (c9b[0] + 2.54, vouty)); s.junction((c9b[0] + 2.54, vouty))
    s.wire(d1k, (c9b[0] + 2.54, vouty))
'''
s = s.replace(old, new)
s = s.replace('    s.wire((d1k[0] + 2.54, vouty), (P("C12", 1)[0], vouty))', '    s.wire((c9b[0] + 2.54, vouty), (P("C12", 1)[0], vouty))')
p.write_text(s, encoding="utf-8")
print("ok")
