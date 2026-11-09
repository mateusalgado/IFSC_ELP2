"""Mostra valores de sinais de um .raw em instantes dados. Uso: peek.py <caso> t1,t2,... sinal1 sinal2 ..."""
import sys
import numpy as np
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from rawread import read_raw

caso = sys.argv[1]
times = [float(x) for x in sys.argv[2].split(",")]
keys = sys.argv[3:]
d = read_raw(HERE.parent / "runs" / f"{caso}.raw")
t = d["time"]
missing = [k for k in keys if k not in d]
if missing:
    print("nao encontrados:", missing)
keys = [k for k in keys if k in d]
print("t(us)".rjust(9) + "".join(k.rjust(13) for k in keys))
for tt in times:
    i = min(np.searchsorted(t, tt), len(t) - 1)
    print(f"{tt*1e6:9.1f}" + "".join(f"{float(d[k][i]):13.4g}" for k in keys))
for k in keys:
    print(f"{k}: min {d[k].min():.4g} max {d[k].max():.4g}")
