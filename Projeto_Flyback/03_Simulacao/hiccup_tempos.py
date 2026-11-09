"""Tempos do hiccup no curto (releitura do .raw): instantes em que VCC cruza o UVLO (7,6 V descendo / 8,4 V subindo)
e intervalos ligado/desligado. Uso (WSL): python3 hiccup_tempos.py [raw] [t_on_ms] [t_off_ms]  -> runs/<caso>_hiccup.json"""
import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rawread import read_raw
from runs_dir import raw_path
raw = Path(sys.argv[1]) if len(sys.argv) > 1 else raw_path("curto_220V")
t_on = float(sys.argv[2]) / 1e3 if len(sys.argv) > 2 else 60e-3
t_off = float(sys.argv[3]) / 1e3 if len(sys.argv) > 3 else 380e-3
d = read_raw(raw)
t = np.asarray(d["time"]); v = np.asarray(d["v(vcc)"]); g = np.asarray(d["v(gate)"])
# maquina de estados (histerese): desliga ao cruzar 7,6 V descendo, religa no primeiro pulso de gate (VCC atinge os 8,4 V do modelo e o CI passa a consumir)
estado = True; off = []; on = []
for i in range(1, len(v), 1):
    if estado and v[i] < 7.6: estado = False; off.append(t[i])
    elif (not estado) and g[i] > 5.0: estado = True; on.append(t[i])   # religamento = primeiro pulso de gate apos o desligamento
off = np.array(off); on = np.array(on)
ev = sorted([(x, "off") for x in off] + [(x, "on") for x in on])
res = dict(t_on_ms=t_on * 1e3, t_off_ms=t_off * 1e3, eventos=[(round(x * 1e3, 1), k) for x, k in ev],
           vcc_fim=float(v[-1]), t_fim_ms=float(t[-1] * 1e3), vcc_no_curto=float(np.interp(t_on, t, v)))
if off.size: res["t_ate_uvlo_ms"] = float((off[0] - t_on) * 1e3)
if off.size and on.size:
    r = [b - a for a in off for b in on if b > a]
    res["t_recarga_ms"] = float(min(r) * 1e3) if r else None
if off.size > 1 and on.size:
    l = [b - a for a in on for b in off if b > a]
    res["t_ligado_ms"] = float(min(l) * 1e3) if l else None
if res.get("t_recarga_ms") and res.get("t_ligado_ms"):
    res["duty_falha_pct"] = 100 * res["t_ligado_ms"] / (res["t_ligado_ms"] + res["t_recarga_ms"])
res["religou_apos_remocao"] = bool(on.size and on[-1] > t_off)
out = Path(__file__).resolve().parent / "runs" / (raw.stem + "_hiccup.json")
out.write_text(json.dumps(res, indent=1), encoding="utf-8")
print(json.dumps(res, indent=1))
