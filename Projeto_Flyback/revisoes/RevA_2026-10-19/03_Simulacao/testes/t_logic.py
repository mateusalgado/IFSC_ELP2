"""Determina empiricamente a ordem dos pinos dos dispositivos A (SCHMITT, DFLOP, SRFLOP) do LTspice."""
import subprocess
import numpy as np
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from rawread import read_raw

LT = "/mnt/c/Users/mateu/AppData/Local/Programs/ADI/LTspice/LTspice.exe"
WIN = r"C:\Users\mateu\OneDrive\Documentos\ELP2\PROJETO\03_Simulacao\testes"
net = """* teste de pinos dos dispositivos A
V_in in 0 PWL(0 0 10u 10 20u 10 30u 0 40u 0)
A_s in 0 0 0 0 s6 s7 0 SCHMITT vt=5 vh=1 vhigh=1 vlow=0
* DFLOP: D=d7(realimentado de porta 7), CLK=clk
V_clk clk 0 PULSE(0 1 1u 10n 10n 1u 5u)
A_d d7 clk 0 0 0 d6 d7 0 DFLOP
* SRFLOP: S pulso em 2us, R pulso em 12us
V_s s 0 PULSE(0 1 2u 10n 10n 1u 100u)
V_r r 0 PULSE(0 1 12u 10n 10n 1u 100u)
A_sr s r 0 0 0 q6 q7 0 SRFLOP
.tran 0 40u 0 10n
.end
"""
(HERE / "t_logic.net").write_text(net)
subprocess.run([LT, "-b", "-Run", WIN + r"\t_logic.net"], check=False)
d = read_raw(HERE / "t_logic.raw"); t = d["time"]
for tt in (5e-6, 15e-6, 25e-6, 35e-6):
    i = min(np.searchsorted(t, tt), len(t) - 1)
    print("t=%.0fus" % (tt * 1e6), {k: round(float(d[k][i]), 2) for k in ("v(in)", "v(s6)", "v(s7)", "v(q6)", "v(q7)")})
m = (t > 0) & (t < 25e-6)
for k in ("v(d6)", "v(d7)"):
    edges = t[m][np.where(np.diff(d[k][m]) > 0.5)[0]]
    print(k, "subidas (us):", np.round(edges * 1e6, 2))
