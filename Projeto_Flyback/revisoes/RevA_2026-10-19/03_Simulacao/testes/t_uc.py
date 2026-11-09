"""Teste isolado do subcircuito comportamental do UC3845 (UVLO, oscilador, latch, driver)."""
import subprocess, sys
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import gera_netlist as g
from rawread import read_raw

LT = "/mnt/c/Users/mateu/AppData/Local/Programs/ADI/LTspice/LTspice.exe"
WIN = r"C:\Users\mateu\OneDrive\Documentos\ELP2\PROJETO\03_Simulacao\testes"

net = """* teste do subcircuito UC3845
V_vcc vcc 0 PWL(0 0 200u 15 400u 15 450u 7 600u 7 650u 15 1m 15)
V_is isns 0 PULSE(0 1.2 0 6u 0.1u 0.1u 15.4u)
R_pu vref comp 4.7k
C_pc comp 0 1n
I_opto comp 0 0.5m
X_uc comp isns vcc drv 0 vref UC3845B
R_l drv 0 1k
""" + g.uc3845_sub() + """
.model DZ34 D(Is=1e-12 bv=34 Ibv=1m)
.tran 0 1m 0 20n
.end
"""
(HERE / "t_uc.net").write_text(net)
subprocess.run([LT, "-b", "-Run", WIN + r"\t_uc.net"], check=False)
print((HERE / "t_uc.log").read_text(errors="ignore")[-600:])
d = read_raw(HERE / "t_uc.raw"); t = d["time"]
print(sorted(k for k in d if "x_uc" in k))
keys = ("v(vcc)", "v(x_uc:on)", "v(vref)", "v(comp)", "v(x_uc:th)", "v(x_uc:q)", "v(x_uc:qb)", "v(x_uc:ql)", "v(x_uc:clk)", "v(x_uc:rst)", "v(x_uc:drv)", "v(drv)")
for tt in (100e-6, 300e-6, 303e-6, 306e-6, 310e-6, 500e-6, 800e-6):
    i = min(np.searchsorted(t, tt), len(t) - 1)
    print("t=%.0fus" % (tt * 1e6), {k: round(float(d[k][i]), 3) for k in keys if k in d})
m = (t > 300e-6) & (t < 400e-6)
drv = d["v(drv)"][m]
print("drv 300-400us: min %.2f max %.2f media %.2f" % (drv.min(), drv.max(), drv.mean()))
if "v(x_uc:q)" in d:
    q = d["v(x_uc:q)"][m]; tq = t[m]
    edges = tq[np.where(np.diff(q) > 0.5)[0]]
    print("subidas de Q (us):", np.round(edges[:6] * 1e6, 2), "-> periodo", np.round(np.diff(edges[:6]) * 1e6, 2))
