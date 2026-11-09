"""Comparador de corrente com pulso minimo (atraso RC ~100 ns) e nivel definido quando ISENSE = limiar = 0."""
from pathlib import Path
g = Path(__file__).resolve().parent.parent / "gera_netlist.py"; s = g.read_text(encoding="utf-8")
old = "B_cmp uc_rst 0 V=0.5+0.5*tanh((V(isns)-V(uc_th))*2000)"
new = ("B_cmp uc_cmp 0 V=0.5+0.5*tanh((V(isns)-V(uc_th)-0.01)*2000)\n"
       "R_cmp uc_cmp uc_rst 1k\n"
       "C_cmp uc_rst 0 100p")
assert old in s
s = s.replace(old, new)
g.write_text(s, encoding="utf-8")
print("ok")
