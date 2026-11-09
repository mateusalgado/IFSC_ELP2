"""Releitura do curto-circuito (revisao B) a partir do .raw, por janelas:
aplicacao (t_on .. t_on+2 ms), curto sustentado (t_on+2 ms .. t_off), recuperacao (t_off .. fim).
Le o .raw por memmap (so as colunas necessarias) para nao carregar 900 MB em memoria.
Uso: python3 analisa_curto.py [runs/curto_220V.raw] [t_on_ms] [t_off_ms]
Saida: runs/curto_janelas.json + impressao da tabela.
"""
import json
import re
import sys
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
from runs_dir import raw_path
path = Path(sys.argv[1]) if len(sys.argv) > 1 else raw_path("curto_220V")
t_on = float(sys.argv[2]) * 1e-3 if len(sys.argv) > 2 else 60e-3
t_off = float(sys.argv[3]) * 1e-3 if len(sys.argv) > 3 else 120e-3


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


def v(nm):
    return np.asarray(mm[col[nm]], dtype=np.float64)


def diff(a, b):
    return v(a) - v(b)


sig = {
    "Id(M1)": v("id(m1)"), "I(L_p)": v("i(l_p)"), "I(D_out)": v("i(d_out)"), "Vds": diff("v(drain)", "v(sw)"),
    "Vcc": v("v(vcc)"), "Vo": diff("v(vo)", "v(sgnd)"), "Vdrv": v("v(drv)"), "Vcomp": v("v(comp)"), "Visns": v("v(isns)"),
    "I(C_o1)": v("i(c_o1)"), "Vbulk": v("v(bulk)"),
}
tfim = t[-1]
janelas = {
    "antes (regime)": (t_on - 5e-3, t_on),
    "aplicacao (2 ms)": (t_on, t_on + 2e-3),
    "curto sustentado": (t_on + 2e-3, t_off),
    "recuperacao": (t_off, tfim),
}


def rms(x, tt):
    if len(x) < 2:
        return float("nan")
    return float(np.sqrt(np.trapz(x * x, tt) / (tt[-1] - tt[0])))


def avg(x, tt):
    if len(x) < 2:
        return float("nan")
    return float(np.trapz(x, tt) / (tt[-1] - tt[0]))


out = {}
for nome, (a, b) in janelas.items():
    m = (t >= a) & (t <= b)
    tt = t[m]
    r = {"t0_ms": a * 1e3, "t1_ms": b * 1e3, "amostras": int(m.sum())}
    for k, x in sig.items():
        xx = x[m]
        if len(xx) == 0:
            continue
        r[k] = dict(max=float(xx.max()), min=float(xx.min()), rms=rms(xx, tt), avg=avg(xx, tt), t_max_ms=float(tt[xx.argmax()] * 1e3), t_min_ms=float(tt[xx.argmin()] * 1e3))
    # pulsos de comando: o CI continua chaveando? (bordas de subida do DRV)
    d = sig["Vdrv"][m]
    edges = int(np.sum((d[1:] > 5) & (d[:-1] <= 5)))
    r["pulsos_drv"] = edges
    r["f_drv_kHz"] = edges / (b - a) / 1e3 if b > a else 0
    # energia/pulso maxima no primario: 0,5*Lp*Ip^2 (Lp de trafo.json)
    out[nome] = r

tr = json.loads((HERE.parent / "02_Calculos" / "resultados" / "trafo.json").read_text(encoding="utf-8"))
Lp = tr["Lp_real"]; Ip_proj = tr["Ip_real"]; B_proj = tr["B_real"]
# fluxo: B proporcional a corrente magnetizante (indutor linear) -> B = B_proj * I / Ip_proj
for nome, r in out.items():
    if "I(L_p)" in r:
        r["B_pico_T"] = B_proj * r["I(L_p)"]["max"] / Ip_proj
        r["E_pulso_uJ"] = 0.5 * Lp * r["I(L_p)"]["max"] ** 2 * 1e6
# recuperacao: tempo ate Vo voltar a >= 11,4 V apos t_off
m = t >= t_off
vo = sig["Vo"][m]; tt = t[m]
idx = np.where(vo >= 11.4)[0]
out["recuperacao"]["t_volta_11V4_ms"] = float((tt[idx[0]] - t_off) * 1e3) if len(idx) else None
out["_info"] = dict(arquivo=str(path.name), pontos=int(npts), t_fim_ms=tfim * 1e3, t_on_ms=t_on * 1e3, t_off_ms=t_off * 1e3, Lp_uH=Lp * 1e6, Ip_proj=Ip_proj, B_proj=B_proj)
(HERE / "runs" / (path.stem + "_janelas.json")).write_text(json.dumps(out, indent=1), encoding="utf-8")

print(f"{path.name}: {npts} pontos, t_fim = {tfim*1e3:.1f} ms, curto {t_on*1e3:.0f}-{t_off*1e3:.0f} ms")
print(f"{'janela':18} {'Id(M1) max':>11} {'I(L_p) max':>11} {'B pico':>7} {'Id(D1) max':>11} {'Id(D1) rms':>11} {'Vds max':>8} {'Vcc min':>8} {'Vo min':>7} {'Vo max':>7} {'pulsos':>7} {'f_drv':>7}")
for nome, r in out.items():
    if nome.startswith("_"):
        continue
    print(f"{nome:18} {r['Id(M1)']['max']:11.2f} {r['I(L_p)']['max']:11.2f} {r.get('B_pico_T', 0):7.3f} {r['I(D_out)']['max']:11.1f} {r['I(D_out)']['rms']:11.2f} {r['Vds']['max']:8.0f} {r['Vcc']['min']:8.2f} {r['Vo']['min']:7.2f} {r['Vo']['max']:7.2f} {r['pulsos_drv']:7d} {r['f_drv_kHz']:7.1f}")
print("retorno a 11,4 V apos t_off:", out["recuperacao"].get("t_volta_11V4_ms"), "ms")
