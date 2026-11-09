"""Figuras do curto-circuito (revisao B) a partir do .raw por memmap:
  (a) janela completa: Vo, Vcc, Ip, I(D1), Vds;  (b) zoom na aplicacao do curto (t_on-0,5 ms .. t_on+2 ms).
Uso: python3 plota_curto.py [runs/curto_220V.raw] [t_on_ms] [t_off_ms] [sufixo]
"""
import re
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

HERE = Path(__file__).resolve().parent
from runs_dir import raw_path
path = Path(sys.argv[1]) if len(sys.argv) > 1 else raw_path("curto_220V")
t_on = float(sys.argv[2]) * 1e-3 if len(sys.argv) > 2 else 60e-3
t_off = float(sys.argv[3]) * 1e-3 if len(sys.argv) > 3 else 120e-3
suf = sys.argv[4] if len(sys.argv) > 4 else ""
OUT = HERE / "analise"
OUT.mkdir(exist_ok=True)


def header(path):
    with open(path, "rb") as f:
        head = f.read(200000)
    if head[1:2] == b"\x00":
        enc = "utf-16-le"; mark = "Binary:\n".encode(enc)
    else:
        enc = "latin-1"; mark = b"Binary:\n"
    idx = head.find(mark)
    hdr = head[:idx].decode(enc)
    npts = int(re.search(r"No\. Points:\s*(\d+)", hdr).group(1))
    nvars = int(re.search(r"No\. Variables:\s*(\d+)", hdr).group(1))
    flags = re.search(r"Flags:\s*(.*)", hdr).group(1)
    names = []
    for line in hdr.split("Variables:")[-1].strip().splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0].isdigit():
            names.append(parts[1].lower())
    return names, npts, nvars, "double" in flags, idx + len(mark)


names, npts, nvars, dbl, start = header(path)
rec = np.dtype([("t", "<f8")] + [(f"v{i}", "<f8" if dbl else "<f4") for i in range(1, nvars)])
mm = np.memmap(path, dtype=rec, mode="r", offset=start, shape=(npts,))
t = np.abs(np.asarray(mm["t"], dtype=np.float64))
col = {nm: f"v{i}" for i, nm in enumerate(names) if i > 0}
v = lambda nm: np.asarray(mm[col[nm]], dtype=np.float64)


def decim(m, nmax=400000):
    idx = np.where(m)[0]
    if len(idx) > nmax:
        idx = idx[:: int(np.ceil(len(idx) / nmax))]
    return idx


sig = dict(Vo=v("v(vo)") - v("v(sgnd)"), Vcc=v("v(vcc)"), Ip=v("i(l_p)"), Id1=v("i(d_out)"), Vds=v("v(drain)") - v("v(sw)"), Idm=v("id(m1)"))
for nome, (a, b) in {"janelas": (t_on - 10e-3, t[-1]), "aplicacao": (t_on - 0.3e-3, t_on + 2.0e-3)}.items():
    i = decim((t >= a) & (t <= b))
    tt = t[i] * 1e3
    fig, ax = plt.subplots(5, 1, figsize=(11, 11), sharex=True)
    ax[0].plot(tt, sig["Vo"][i], color="C0"); ax[0].set_ylabel("Vo (V)")
    ax[1].plot(tt, sig["Vcc"][i], color="C1"); ax[1].set_ylabel("VCC (V)"); ax[1].axhline(7.9, color="k", ls=":", lw=0.8); ax[1].axhline(8.5, color="k", ls=":", lw=0.8)
    ax[2].plot(tt, sig["Idm"][i], color="C3", lw=0.6); ax[2].set_ylabel("Id(Q1) (A)")
    ax[3].plot(tt, sig["Id1"][i], color="C2", lw=0.6); ax[3].set_ylabel("I(D1) (A)")
    ax[4].plot(tt, sig["Vds"][i], color="C4", lw=0.6); ax[4].set_ylabel("Vds (V)"); ax[4].set_xlabel("tempo (ms)")
    for a_ in ax:
        a_.grid(alpha=0.3); a_.axvline(t_on * 1e3, color="r", ls="--", lw=0.8)
        if a <= t_off <= b:
            a_.axvline(t_off * 1e3, color="g", ls="--", lw=0.8)
    fig.suptitle(f"{path.stem}{suf}: curto na saida de {t_on*1e3:.0f} a {t_off*1e3:.0f} ms ({nome})")
    fig.tight_layout()
    fig.savefig(OUT / f"{path.stem}{suf}_{nome}.png", dpi=110)
    plt.close(fig)
print("ok", OUT)
