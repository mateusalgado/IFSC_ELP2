"""Preenche os marcadores {{...}} do GUIA_MONTAGEM.md com os valores da simulacao B
(runs/medidas.json, runs/transitorios.json). Mantem o GUIA_MONTAGEM.md como fonte (os marcadores sao
substituidos no proprio arquivo; o template fica em GUIA_MONTAGEM.template.md). Uso (WSL): python3 preenche_guia.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = HERE.parent
med = json.load(open(P / "03_Simulacao/runs/medidas.json", encoding="utf-8"))
tra = json.load(open(P / "03_Simulacao/runs/transitorios.json", encoding="utf-8"))
uc = json.load(open(P / "02_Calculos/resultados/uc3845.json", encoding="utf-8"))
tpl = HERE / "GUIA_MONTAGEM.template.md"
src = HERE / "GUIA_MONTAGEM.md"
if not tpl.exists():
    tpl.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
txt = tpl.read_text(encoding="utf-8")


def f(x, n=2):
    return "-" if x is None else f"{x:.{n}f}".replace(".", ",")


reg = {k: v for k, v in med.items() if k.startswith("regime_")}
vo = [v["vo_avg"] for v in reg.values()]
c = med.get("curto_220V", {})
d90, d264 = tra.get("degrau_90V", {}), tra.get("degrau_264V", {})
hic = {r[0]: r for r in uc["partida"].get("hiccup", [])}
def _t_degrau():
    if not (d90 and d264):
        return "-"
    xs = [x[s] for x in (d90, d264) for s in ("subida", "descida")]
    t1 = max(x["t_retorno_1pct_ms"] for x in xs)
    t05 = max(x["t_retorno_0p5pct_ms"] for x in xs)
    dv = max(abs(x["desvio_mV"]) for x in xs)
    if t1 == 0:
        return f"não sai de ± 1 % (desvio máx. {f(dv, 0)} mV); ± 0,5 % em {f(t05, 1)} ms"
    return f"{f(t1, 1)} ms (± 1 %); {f(t05, 1)} ms (± 0,5 %)"


hic_s = json.load(open(P / "03_Simulacao/runs/curto_220V_hiccup.json", encoding="utf-8")) if (P / "03_Simulacao/runs/curto_220V_hiccup.json").exists() else {}
val = {
    "vo_min": f(min(vo)), "vo_max": f(max(vo)), "vopp": f(1e3 * max(v["vo_pp"] for v in reg.values()), 1),
    "ripple_total": f(1e3 * max(v.get("ripple_total", 0) for v in reg.values()), 1),
    "vbulk_min_90": f(med["regime_90V_100pct"]["vbulk_min"], 1), "ip_90": f(med["regime_90V_100pct"]["ip_pk"]),
    "vds_264": f(med["regime_264V_100pct"]["vds_max"], 0), "vd_264": f(-med["regime_264V_100pct"]["vd_min"], 0),
    "eta_220": f(100 * med["regime_220V_100pct"]["po"] / med["regime_220V_100pct"]["pin"], 1), "vcc_220": f(med["regime_220V_100pct"]["vcc_avg"], 1),
    "t_uv_90": f(med["partida_90V"].get("t_uv"), 2), "t_uv_264": f(med["partida_264V"].get("t_uv"), 2),
    "t_vo_90": f(tra["partida_90V"]["t_vo_11v4_ms"], 1), "t_vo_264": f(tra["partida_264V"]["t_vo_11v4_ms"], 1),
    "vds_part_264": f(med["partida_264V"]["vds_max"], 0), "ip_part": f(max(med["partida_90V"]["ip_pk"], med["partida_264V"]["ip_pk"])),
    "degrau": f"90 V: {f(d90['subida']['desvio_mV'], 0)} mV na subida / +{f(d90['descida']['desvio_mV'], 0)} mV na descida; 264 V: {f(d264['subida']['desvio_mV'], 0)} / +{f(d264['descida']['desvio_mV'], 0)} mV" if d90 and d264 else "-",
    "t_degrau": _t_degrau(),
    "iq_aplic": f(c.get("iq_aplic"), 1), "vds_aplic": f(c.get("vds_aplic"), 0), "iq_sust": f(c.get("iq_sust"), 1), "id1rms_sust": f(c.get("id1rms_sust"), 1),
    "t_uvlo": hic.get("220", ["", "-"])[1],
    "hic_uvlo_s": f(hic_s.get("t_ate_uvlo_ms"), 0), "hic_rec_s": f(hic_s.get("t_recarga_ms"), 0), "hic_on_s": f(hic_s.get("t_ligado_ms"), 0), "hic_duty_s": f(hic_s.get("duty_falha_pct"), 0),
}
out = re.sub(r"\{\{(\w+)\}\}", lambda m: val.get(m.group(1), m.group(0)), txt)
src.write_text(out, encoding="utf-8")
faltam = re.findall(r"\{\{(\w+)\}\}", out)
print("guia preenchido;", "marcadores restantes:", faltam)
