"""Figuras das simulacoes LTspice (le runs/<caso>.raw). Uso: python3 plota.py <caso> [<caso> ...]
Gera analise/<caso>_ciclo.png (2 ciclos de comutacao) e analise/<caso>_rede.png (ciclos de rede / transitorio).
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from rawread import read_raw, janela

OUT = HERE / "analise"
OUT.mkdir(exist_ok=True)
FS = 64.7e3


def fig_ciclo(caso, d, t_end=None):
    t = d["time"]
    t1 = t[-1] if t_end is None else t_end
    w = janela(d, t1 - 2.2 / FS, t1)
    tt = (w["time"] - w["time"][0]) * 1e6
    fig, ax = plt.subplots(5, 1, figsize=(10, 10), sharex=True)
    ax[0].plot(tt, w["v(drain)"], "C3"); ax[0].set_ylabel("v_DS (V)")
    ax[1].plot(tt, w["i(l_p)"], "C0", label="i_p"); ax[1].plot(tt, w["i(d_out)"] / 6, "C1", label="i_D / n"); ax[1].set_ylabel("A"); ax[1].legend(loc="upper right")
    ax[2].plot(tt, w["i(d_out)"], "C1"); ax[2].set_ylabel("i_D (A)")
    ax[3].plot(tt, w["v(gate)"], "C2", label="v_GS"); ax[3].plot(tt, w["v(isns)"] * 10, "C4", label="v_ISENSE ×10"); ax[3].plot(tt, w["v(uc_th)"] * 10, "k--", lw=1, label="limiar ×10"); ax[3].set_ylabel("V"); ax[3].legend(loc="upper right", fontsize=8)
    ax[4].plot(tt, ((w["v(vo)"] - w["v(sgnd)"]) - (w["v(vo)"] - w["v(sgnd)"]).mean()) * 1e3, "C5", label="Δv_o (após LC)"); ax[4].plot(tt, ((w["v(vout)"] - w["v(sgnd)"]) - (w["v(vout)"] - w["v(sgnd)"]).mean()) * 1e3, "C6", lw=0.8, label="Δv no banco C1"); ax[4].set_ylabel("mV"); ax[4].legend(loc="upper right", fontsize=8)
    ax[4].set_xlabel("tempo (µs)")
    for a in ax:
        a.grid(alpha=.3)
    fig.suptitle(f"{caso}: ciclos de comutação (t ≈ {t1*1e3:.1f} ms)"); fig.tight_layout()
    fig.savefig(OUT / f"{caso}_ciclo.png", dpi=140); plt.close(fig)


def fig_rede(caso, d, t0=0.0):
    w = janela(d, t0, d["time"][-1])
    tt = w["time"] * 1e3
    fig, ax = plt.subplots(4, 1, figsize=(10, 9), sharex=True)
    ax[0].plot(tt, w["v(bulk)"], "C0", label="v_bulk"); ax[0].plot(tt, np.abs(w["v(l)"] - w["v(n)"]), "0.6", lw=.6, label="|v_rede|"); ax[0].set_ylabel("V"); ax[0].legend(loc="lower right", fontsize=8)
    ax[1].plot(tt, w["v(vo)"] - w["v(sgnd)"], "C1"); ax[1].set_ylabel("v_o (V)")
    ax[2].plot(tt, w["i(v_ac)"] * -1, "C3", lw=.7); ax[2].set_ylabel("i_rede (A)")
    ax[3].plot(tt, w["v(comp)"], "C4", label="COMP"); ax[3].plot(tt, w["v(vcc)"], "C2", label="VCC"); ax[3].set_ylabel("V"); ax[3].legend(loc="lower right", fontsize=8)
    ax[3].set_xlabel("tempo (ms)")
    for a in ax:
        a.grid(alpha=.3)
    fig.suptitle(f"{caso}: ciclos de rede / transitório"); fig.tight_layout()
    fig.savefig(OUT / f"{caso}_rede.png", dpi=140); plt.close(fig)


def fig_comut(caso, d, t_end=None):
    """zoom no desligamento e no ligamento do MOSFET (ultimo ciclo)"""
    t = d["time"]
    t1 = t[-1] if t_end is None else t_end
    w = janela(d, t1 - 1.2 / FS, t1)
    g = w["v(gate)"]; tw = w["time"]
    # instante de desligamento: ultima descida do gate abaixo de 5 V
    idx = np.where((g[:-1] > 5) & (g[1:] <= 5))[0]
    ion = np.where((g[:-1] < 5) & (g[1:] >= 5))[0]
    if len(idx) == 0 or len(ion) == 0:
        return
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for a, i0, titulo in ((ax[0], ion[-1], "ligamento"), (ax[1], idx[-1], "desligamento")):
        t0 = tw[i0]
        z = janela(d, t0 - 150e-9, t0 + 250e-9)
        tz = (z["time"] - t0) * 1e9
        a.plot(tz, z["v(drain)"], "C3", label="v_DS (V)")
        a2 = a.twinx(); a2.plot(tz, z["id(m1)"], "C0", label="i_D (A)"); a2.plot(tz, z["v(gate)"], "C2", lw=.8, label="v_GS (V)")
        a.set_xlabel("tempo (ns)"); a.set_ylabel("v_DS (V)", color="C3"); a2.set_ylabel("i_D (A), v_GS (V)")
        a.set_title(f"{titulo}"); a.grid(alpha=.3)
        h1, l1 = a.get_legend_handles_labels(); h2, l2 = a2.get_legend_handles_labels(); a.legend(h1 + h2, l1 + l2, fontsize=8, loc="center right")
    fig.suptitle(f"{caso}: comutação do MOSFET"); fig.tight_layout()
    fig.savefig(OUT / f"{caso}_comut.png", dpi=140); plt.close(fig)


if __name__ == "__main__":
    for caso in sys.argv[1:]:
        d = read_raw(HERE / "runs" / f"{caso}.raw")
        fig_ciclo(caso, d)
        fig_rede(caso, d)
        fig_comut(caso, d)
        print("ok", caso)
