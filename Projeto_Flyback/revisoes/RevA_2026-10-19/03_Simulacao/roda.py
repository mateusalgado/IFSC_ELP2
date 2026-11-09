"""Roda os netlists no LTspice em lote (Windows) e extrai os .meas do .log.

Uso (PowerShell/Git Bash, Python do WSL nao enxerga o LTspice -> este script e chamado
pelo WSL mas invoca o LTspice.exe via caminho /mnt/c):
    python3 roda.py [caso1 caso2 ...]
Resultados: runs/<caso>.log, runs/<caso>.raw, runs/medidas.json
"""
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
NET = HERE / "netlists"
RUNS = HERE / "runs"
RUNS.mkdir(exist_ok=True)
LTSPICE = "/mnt/c/Users/mateu/AppData/Local/Programs/ADI/LTspice/LTspice.exe"
WIN_RUNS = r"C:\Users\mateu\OneDrive\Documentos\ELP2\PROJETO\03_Simulacao\runs"
TIMEOUT_S = 900

SI = {"f": 1e-15, "p": 1e-12, "n": 1e-9, "u": 1e-6, "µ": 1e-6, "m": 1e-3, "k": 1e3, "meg": 1e6, "g": 1e9, "t": 1e12}


def parse_log(path):
    txt = path.read_text(encoding="utf-8", errors="ignore")
    meas = {}
    for m in re.finditer(r"^(\w+):\s+(?:[^=\n]*=)?\s*([-+0-9.eE]+)\s*(?:FROM|$|\s)", txt, re.M):
        try:
            meas[m.group(1).lower()] = float(m.group(2))
        except ValueError:
            pass
    # formato alternativo "name: AVG(v(vo))=1.2e+01 FROM 0 TO 1"
    for m in re.finditer(r"^(\w+):\s+\w+\([^)]*\)=([-+0-9.eE]+)", txt, re.M):
        meas[m.group(1).lower()] = float(m.group(2))
    for m in re.finditer(r"^(\w+)=([-+0-9.eE]+)", txt, re.M):
        meas.setdefault(m.group(1).lower(), float(m.group(2)))
    t = re.search(r"Total elapsed time:\s*([0-9.]+)\s*seconds", txt)
    meas["_elapsed_s"] = float(t.group(1)) if t else None
    meas["_erro"] = bool(re.search(r"(?i)error|singular|time step too small", txt))
    return meas


def roda(caso):
    src = NET / f"{caso}.net"
    dst = RUNS / f"{caso}.net"
    shutil.copy(src, dst)
    t0 = time.time()
    try:
        subprocess.run([LTSPICE, "-b", "-Run", f"{WIN_RUNS}\\{caso}.net"], check=False, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        subprocess.run(["/mnt/c/Windows/System32/taskkill.exe", "/F", "/IM", "LTspice.exe"], check=False, capture_output=True)
        print("   TIMEOUT -> LTspice morto", flush=True)
    dt = time.time() - t0
    log = RUNS / f"{caso}.log"
    m = parse_log(log) if log.exists() else {"_erro": True}
    m["_wall_s"] = dt
    return m


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    import gera_netlist as g
    sel = sys.argv[1:] or list(g.CASOS)
    todos = json.loads((RUNS / "medidas.json").read_text()) if (RUNS / "medidas.json").exists() else {}
    for caso in sel:
        g.netlist(caso, **g.CASOS[caso])
        print(f"[{time.strftime('%H:%M:%S')}] rodando {caso} ...", flush=True)
        m = roda(caso)
        todos[caso] = m
        (RUNS / "medidas.json").write_text(json.dumps(todos, indent=1), encoding="utf-8")
        chave = {k: v for k, v in m.items() if k in ("vo_avg", "vo_pp", "ip_pk", "vds_max", "is_rms", "pin", "po", "_wall_s", "_erro")}
        print("   ", chave, flush=True)
