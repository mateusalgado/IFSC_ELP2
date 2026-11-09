"""Corrige orientacao do zener de VCC e as condicoes iniciais dos capacitores (nos internos de ESR)."""
from pathlib import Path
p = Path(__file__).resolve().parent.parent / "gera_netlist.py"
s = p.read_text(encoding="utf-8")
s = s.replace("D_z vcc 0 DZ34", "D_z 0 vcc DZ34")
old_ic = '    ic = "" if startup else f".ic V(bulk)={vpk*0.95:.1f} V(vout)={VO} V(vo)={VO} V(vcc)=15 V(comp)=2.5\\n"\n'
new_ic = '    ic = "" if startup else f".ic V(bulk)={vpk*0.95:.1f} V(bulkc)={vpk*0.95:.1f} V(vout)={VO} V(voutc)={VO} V(vo)={VO} V(voc)={VO} V(vcc)=15 V(vccc)=15 V(comp)=2.5\\n"\n'
old_st = '    ic_start = f".ic V(bulk)={vpk*0.95:.1f} V(vcc)=8.2\\n" if startup else ""\n'
new_st = '    ic_start = f".ic V(bulk)={vpk*0.95:.1f} V(bulkc)={vpk*0.95:.1f} V(vcc)=8.2 V(vccc)=8.2\\n" if startup else ""\n'
assert old_ic in s and old_st in s, "linhas .ic nao encontradas"
s = s.replace(old_ic, new_ic).replace(old_st, new_st)
p.write_text(s, encoding="utf-8")
print("ok: zener", "D_z 0 vcc DZ34" in s, "| ic", "V(vccc)=15" in s)
