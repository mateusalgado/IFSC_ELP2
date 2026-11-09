"""Releitura dos transitorios da revisao B direto dos .raw (memmap, so as colunas usadas):
  - partida_90V / partida_264V: afundamento do VCC apos o UVLO, tempo ate Vo >= 11,4 V, Vo maximo, Vds maximo, Ip maximo;
  - degrau_90V / degrau_264V / ctr05_90V: degrau de subida (t_up) e de descida (t_down): Vo antes, minimo/maximo nos 5 ms
    seguintes, tempo de retorno a +-1 % (0,12 V) e a +-0,5 %;
  - curto_220V: janelas (chama a mesma logica de analisa_curto.py).
Saida: runs/transitorios.json. Uso (WSL): python3 analisa_transitorios.py
"""
import json
import re
import sys
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from gera_netlist import CASOS
from runs_dir import raw_path


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


class Raw:
    def __init__(self, path):
        names, npts, nvars, dbl, start = header(path)
        rec = np.dtype([("t", "<f8")] + [(f"v{i}", "<f8" if dbl else "<f4") for i in range(1, nvars)])
        self.mm = np.memmap(path, dtype=rec, mode="r", offset=start, shape=(npts,))
        self.t = np.abs(np.asarray(self.mm["t"], dtype=np.float64))
        self.col = {nm: f"v{i}" for i, nm in enumerate(names) if i > 0}

    def v(self, nm):
        return np.asarray(self.mm[self.col[nm]], dtype=np.float64)

    def vo(self):
        return self.v("v(vo)") - self.v("v(sgnd)")


def partida(nome):
    r = Raw(raw_path(nome))
    t = r.t; vo = r.vo(); vcc = r.v("v(vcc)"); vds = r.v("v(drain)") - r.v("v(sw)"); ip = r.v("i(l_p)")
    i = np.where(vo >= 11.4)[0]
    j = vcc[: np.searchsorted(t, 20e-3)].argmin()
    return dict(vcc_inicial=float(vcc[0]), vcc_min=float(vcc[j]), t_vcc_min_ms=float(t[j] * 1e3), t_vo_11v4_ms=float(t[i[0]] * 1e3) if len(i) else None,
                vo_max=float(vo.max()), vds_max=float(vds.max()), ip_max=float(ip.max()), t_fim_ms=float(t[-1] * 1e3))


def degrau(nome, t_up, t_down):
    r = Raw(raw_path(nome))
    t = r.t; vo = r.vo(); ip = r.v("i(l_p)")
    out = {}
    for tag, te, sinal in (("subida", t_up, -1), ("descida", t_down, +1)):
        m0 = (t >= te - 1e-3) & (t < te)
        v0 = float(vo[m0].mean())
        m1 = (t >= te) & (t <= te + 8e-3)
        tt = t[m1]; vv = vo[m1]
        ext = float(vv.min()) if sinal < 0 else float(vv.max())
        # retorno: ultimo instante fora da faixa +-1 % em torno do valor final (media dos ultimos 2 ms da janela)
        vf = float(vo[(t >= te + 15e-3) & (t <= te + 19e-3)].mean()) if t[-1] >= te + 19e-3 else float(vv[-200:].mean())
        for tol, key in ((0.12, "t_retorno_1pct_ms"), (0.06, "t_retorno_0p5pct_ms")):
            fora = np.where(np.abs(vv - vf) > tol)[0]
            out.setdefault(tag, {})[key] = float((tt[fora[-1]] - te) * 1e3) if len(fora) else 0.0
        out[tag].update(vo_antes=v0, vo_extremo=ext, desvio_mV=(ext - v0) * 1e3, vo_final=vf, ip_max=float(ip[m1].max()))
    return out


def main():
    res = {}
    for nome in ("partida_90V", "partida_264V"):
        if raw_path(nome).exists():
            res[nome] = partida(nome); print(nome, res[nome])
    for nome in ("degrau_90V", "degrau_264V", "ctr05_90V"):
        if raw_path(nome).exists():
            t_up = CASOS[nome]["step_load"][0]
            res[nome] = degrau(nome, t_up, t_up + 20e-3); print(nome, res[nome])
    (HERE / "runs" / "transitorios.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print("-> runs/transitorios.json")


if __name__ == "__main__":
    main()
