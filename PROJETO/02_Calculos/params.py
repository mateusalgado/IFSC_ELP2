"""Parametros centrais do projeto: fonte flyback 12 V / 3 A, UC3845.

Todos os scripts de 02_Calculos importam daqui. Resultados sao salvos em
resultados/*.json para os scripts seguintes e para o relatorio.
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "resultados"
ASSETS = HERE / "assets"
RES.mkdir(exist_ok=True)
ASSETS.mkdir(exist_ok=True)

# ---------------- Especificacao ----------------
VAC_MIN, VAC_MAX = 90.0, 264.0          # V eficaz
VAC_NOM = (127.0, 220.0)
F_LINE = (50.0, 60.0)                    # Hz (50 Hz e o pior caso para o bulk)
VO = 12.0                                # V
IO = 3.0                                 # A
PO = VO * IO                             # 36 W
ETA = 0.82                               # rendimento alvo (revisto apos o orcamento de perdas: 85 % -> 82 %)
PIN = PO / ETA                           # potencia de entrada
FS = 65e3                                # Hz
DMAX = 0.43                              # UC3845 garante >= 0,46; margem para o vale de 90 VAC
VF_DIODE_OUT = 0.7                       # queda do Schottky de saida (estimativa p/ relacao de espiras)
VF_BRIDGE = 1.0                          # queda por diodo da ponte
DVO_PP_MAX = 0.12                        # 1 % de Vo
TA = 40.0                                # C
TJ_PROJ = 125.0                          # C
R_THCS = 0.5                             # C/W (pasta termica)

# cargas e tensoes para as tabelas de esforcos
LOAD_POINTS = (0.10, 0.50, 1.00)
VAC_POINTS = (90.0, 127.0, 220.0, 264.0)


def save(name, data):
    p = RES / f"{name}.json"
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


def load(name, default=None):
    p = RES / f"{name}.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return default


def fmt(x, nd=3):
    if isinstance(x, float):
        return f"{x:.{nd}f}".replace(".", ",")
    return str(x)


def md_table(headers, rows, align=None):
    out = ["| " + " | ".join(headers) + " |"]
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def si(x, unit="", nd=3):
    """formata com prefixo SI"""
    if x == 0:
        return f"0 {unit}"
    e = int(math.floor(math.log10(abs(x)) / 3) * 3)
    e = max(min(e, 9), -12)
    pref = {-12: "p", -9: "n", -6: "µ", -3: "m", 0: "", 3: "k", 6: "M", 9: "G"}[e]
    return f"{x / 10**e:.{nd}g} {pref}{unit}"
