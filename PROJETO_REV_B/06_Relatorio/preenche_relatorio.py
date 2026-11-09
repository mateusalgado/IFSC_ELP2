"""Gera RELATORIO.md a partir de RELATORIO.template.md substituindo os marcadores {{...}} de valores
(simulacao B, calculo B); os marcadores de tabela ({{regime}}, {{perdas}}, {{transitorios}}, {{curto}}, {{criterios}})
sao deixados para o build.py, que os troca pelos arquivos tabelas/*.md. Uso (WSL): python3 gera_tabelas.py && python3 preenche_relatorio.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = HERE.parent
R = P / "02_Calculos/resultados"
med = json.load(open(P / "03_Simulacao/runs/medidas.json", encoding="utf-8"))
tra = json.load(open(P / "03_Simulacao/runs/transitorios.json", encoding="utf-8"))
jan = json.load(open(P / "03_Simulacao/runs/curto_220V_janelas.json", encoding="utf-8"))
hic_s = json.load(open(P / "03_Simulacao/runs/curto_220V_hiccup.json", encoding="utf-8"))
uc = json.load(open(R / "uc3845.json", encoding="utf-8"))
cp = json.load(open(R / "compensador.json", encoding="utf-8"))
sm = json.load(open(R / "semicondutores.json", encoding="utf-8"))
fb = json.load(open(R / "flyback.json", encoding="utf-8"))
tab = json.load(open(HERE / "tabelas/tabelas.json", encoding="utf-8"))


def f(x, n=2):
    return "-" if x is None else f"{x:.{n}f}".replace(".", ",")


reg = {k: v for k, v in med.items() if k.startswith("regime_")}
vo = [v["vo_avg"] for v in reg.values()]
c = med["curto_220V"]
m220 = med["regime_220V_100pct"]; m264 = med["regime_264V_100pct"]; m90 = med["regime_90V_100pct"]
# analise do regime (deltas em plena carga)
t90 = tab["90_100"]; t264 = tab["264_100"]
d = lambda a, b: f"{100 * (b - a) / a:+.1f} %".replace(".", ",")
analise = (f"A tensão de saída fica entre {f(min(vo))} e {f(max(vo))} V em toda a faixa (regulação de linha e carga < 0,1 %). Em plena carga a corrente de pico do primário difere {d(t90['ip_t'], t90['ip_s'])} da teoria "
           f"(limiar efetivo do comparador e atraso do filtro), I<sub>s,pk</sub> {d(t90['ispk_t'], t90['ispk_s'])}, I<sub>s,rms</sub> {d(t90['isrms_t'], t90['isrms_s'])} (a teoria integra o triângulo ideal no vale de V<sub>bulk</sub>) "
           f"e V<sub>ds</sub> {d(t264['vds_t'], t264['vds_s'])} em 264 V (grampo real abaixo de 1,8·V<sub>r</sub>).")
orc = "\n".join(f"| {k.rstrip('V')} | " + " | ".join(f(v["itens"][i]) for i in ("MOSFET", "diodo", "ponte", "transformador", "snubber", "Rsense", "startup", "capacitores_saida", "NTC", "indutor_LC", "UC3845")) + f" | {f(v['total'])} | {f(100 * v['eta'], 1)} |" for k, v in sm["orcamento"].items())
hic = "\n".join(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |" for r in uc["partida"]["hiccup"])
mg = cp["margens"]
val = {
    "orcamento": orc, "hiccup": hic,
    "fc_khz": f(mg["carga100_ctr1.0"]["fc"] / 1e3), "pm": f(mg["carga100_ctr1.0"]["pm"], 0), "gm": f(mg["carga100_ctr1.0"]["gm"], 0) if mg["carga100_ctr1.0"].get("gm") else "∞",
    "pm_min": f(min(v["pm"] for v in mg.values()), 0),
    "iq_aplic": f(c["iq_aplic"], 1), "b_aplic": f(0.25 * c["ip_aplic"] / fb["Ip_max"]), "id1_aplic": f(c["id1_aplic"], 0), "vds_aplic": f(c["vds_aplic"], 0),
    "iq_sust": f(c["iq_sust"], 1), "id1rms_sust": f(c["id1rms_sust"], 1), "pd1_sust": f(c["pd1_sust"], 1), "vccmin_sust": f(c["vccmin_sust"], 1),
    "t_rec": f(jan.get("recuperacao", {}).get("t_volta_11V4_ms"), 1),
    "hic_uvlo_s": f(hic_s.get("t_ate_uvlo_ms"), 0), "hic_rec_s": f(hic_s.get("t_recarga_ms"), 0), "hic_on_s": f(hic_s.get("t_ligado_ms"), 0), "hic_duty_s": f(hic_s.get("duty_falha_pct"), 0), "vcc_fim_rec": f(hic_s.get("vcc_fim"), 2),
    "t_uv_90": f(med["partida_90V"].get("t_uv"), 1), "t_uv_264": f(med["partida_264V"].get("t_uv"), 1),
    "analise_regime": analise,
    "eta_220": f(100 * m220["po"] / m220["pin"], 1), "psnub_220": f(m220["psnub"]), "pdiode_220": f(m220["pdiode"]),
    "vo_min": f(min(vo)), "vo_max": f(max(vo)), "vopp": f(1e3 * max(v["vo_pp"] for v in reg.values()), 1),
    "vds_264": f(m264["vds_max"], 0), "vds_264_pct": f(100 * m264["vds_max"] / 650, 0),
}
txt = (HERE / "RELATORIO.template.md").read_text(encoding="utf-8")
out = re.sub(r"\{\{(\w+)\}\}", lambda m: val.get(m.group(1), m.group(0)), txt)
(HERE / "RELATORIO.md").write_text(out, encoding="utf-8")
rest = sorted(set(re.findall(r"\{\{(\w+)\}\}", out)))
print("RELATORIO.md gerado; marcadores restantes (tabelas para o build.py):", rest)
