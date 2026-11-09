"""Pasta das amostras (.raw) da revisao B.
Os .raw (0,3-1,3 GB cada) sao gravados FORA do OneDrive (C:\\Users\\<user>\\ELP2_sim_runs\\REV_B) porque a sincronizacao
continua de arquivos em crescimento consumia CPU/memoria e deixava o LTspice 10x mais lento. Os .log, .net e medidas.json
sao copiados para 03_Simulacao/runs (OneDrive); os .raw dos casos usados no relatorio sao copiados ao final (copia_raws()).
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS_ONEDRIVE = HERE / "runs"
LOCAL = Path(os.environ.get("ELP2_RUNS_LOCAL", str(Path.home() / "ELP2_sim_runs" / "REV_B") if os.name == "nt" else "/mnt/c/Users/mateu/ELP2_sim_runs/REV_B"))


def runs_dir():
    """onde procurar um .raw: local (se existir) senao a pasta runs do projeto"""
    return LOCAL if LOCAL.exists() else RUNS_ONEDRIVE


def raw_path(case):
    for d in (LOCAL, RUNS_ONEDRIVE):
        p = d / f"{case}.raw"
        if p.exists():
            return p
    return RUNS_ONEDRIVE / f"{case}.raw"


def copia_raws(casos):
    RUNS_ONEDRIVE.mkdir(exist_ok=True)
    for c in casos:
        src = LOCAL / f"{c}.raw"
        if src.exists():
            shutil.copy2(src, RUNS_ONEDRIVE / f"{c}.raw")
            print("copiado", c)
