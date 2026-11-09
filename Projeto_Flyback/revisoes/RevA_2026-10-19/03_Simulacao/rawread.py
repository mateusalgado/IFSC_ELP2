"""Leitor de arquivos .raw binarios do LTspice (transiente) -> numpy.

Formato: cabecalho texto (ate 'Binary:'), depois registros: tempo em float64 e
as demais variaveis em float32 (sem o flag 'double'). Com compressao LTspice
(padrao em lote) os pontos sao esparsos no tempo: usamos interpolacao quando
necessario.
"""
import re
import numpy as np
from pathlib import Path


def read_raw(path):
    data = Path(path).read_bytes()
    # cabecalho pode ser UTF-16LE (Windows) ou ASCII
    if data[:2] == b"T\x00" or data[1:2] == b"\x00":
        enc = "utf-16-le"
        idx = data.find("Binary:\n".encode(enc))
        hdr = data[:idx].decode(enc)
        start = idx + len("Binary:\n".encode(enc))
    else:
        enc = "ascii"
        idx = data.find(b"Binary:\n")
        hdr = data[:idx].decode("latin-1")
        start = idx + len(b"Binary:\n")
    npts = int(re.search(r"No\. Points:\s*(\d+)", hdr).group(1))
    nvars = int(re.search(r"No\. Variables:\s*(\d+)", hdr).group(1))
    flags = re.search(r"Flags:\s*(.*)", hdr).group(1)
    names = []
    for line in hdr.split("Variables:")[-1].strip().splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0].isdigit():
            names.append(parts[1].lower())
    dbl = "double" in flags
    rec = np.dtype([("t", "<f8")] + [(f"v{i}", "<f8" if dbl else "<f4") for i in range(1, nvars)])
    arr = np.frombuffer(data, dtype=rec, count=npts, offset=start)
    out = {"time": np.abs(arr["t"].astype(np.float64))}
    for i, nm in enumerate(names[1:], start=1):
        out[nm] = arr[f"v{i}"].astype(np.float64)
    return out


def janela(d, t0, t1):
    t = d["time"]
    m = (t >= t0) & (t <= t1)
    return {k: v[m] for k, v in d.items()}


if __name__ == "__main__":
    import sys
    d = read_raw(sys.argv[1])
    print(len(d["time"]), "pontos;", list(d)[:12])
