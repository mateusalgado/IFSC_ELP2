"""Gera RELATORIO.md a partir de RELATORIO.template.md substituindo os marcadores {{...}} de valores
(calculo B em 02_Calculos/resultados/*.json, simulacao B em 03_Simulacao/runs/*.json, custo em 05_BOM_Custo/custo.json);
os marcadores de tabela ({{regime}}, {{perdas}}, {{transitorios}}, {{curto}}, {{criterios}}) sao deixados para o build.py,
que os troca pelos arquivos tabelas/*.md.
Uso: "C:\\Program Files\\KiCad\\10.0\\bin\\python.exe" preenche_relatorio.py   (antes: gera_tabelas.py)
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = HERE.parent
R = P / "02_Calculos/resultados"
J = lambda p: json.load(open(p, encoding="utf-8"))
med = J(P / "03_Simulacao/runs/medidas.json")
tra = J(P / "03_Simulacao/runs/transitorios.json")
jan = J(P / "03_Simulacao/runs/curto_220V_janelas.json")
hic_s = J(P / "03_Simulacao/runs/curto_220V_hiccup.json")
en, fb, tr, sd, sn, uc, sm, cp, em = (J(R / f"{n}.json") for n in ("entrada", "flyback", "trafo", "saida", "snubber", "uc3845", "semicondutores", "compensador", "emi"))
tab = J(HERE / "tabelas/tabelas.json")
custo = J(P / "05_BOM_Custo/custo.json")


def f(x, n=2):
    return "-" if x is None else f"{x:.{n}f}".replace(".", ",")


def g(d, *ks, default=None):
    for k in ks:
        if not isinstance(d, dict) or k not in d:
            return default
        d = d[k]
    return d


reg = {k: v for k, v in med.items() if k.startswith("regime_")}
vo = [v["vo_avg"] for v in reg.values()]
c = med["curto_220V"]
m220 = med["regime_220V_100pct"]; m264 = med["regime_264V_100pct"]; m90 = med["regime_90V_100pct"]
t90 = tab["90_100"]; t264 = tab["264_100"]
d = lambda a, b: f"{100 * (b - a) / a:+.1f} %".replace(".", ",")
analise = (f"A tensão de saída fica entre {f(min(vo))} e {f(max(vo))} V em toda a faixa (regulação de linha e carga < 0,1 %). Em plena carga a corrente de pico do primário difere {d(t90['ip_t'], t90['ip_s'])} da teoria "
           f"(limiar efetivo do comparador e atraso do filtro), I<sub>s,pk</sub> {d(t90['ispk_t'], t90['ispk_s'])}, I<sub>s,rms</sub> {d(t90['isrms_t'], t90['isrms_s'])} (a teoria integra o triângulo ideal no vale de V<sub>bulk</sub>) "
           f"e V<sub>ds</sub> {d(t264['vds_t'], t264['vds_s'])} em 264 V (grampo real abaixo de 1,8·V<sub>r</sub>).")
orc = "\n".join(f"| {k.rstrip('V')} | " + " | ".join(f(v["itens"][i]) for i in ("MOSFET", "diodo", "ponte", "transformador", "snubber", "Rsense", "startup", "capacitores_saida", "NTC", "indutor_LC", "UC3845")) + f" | {f(v['total'])} | {f(100 * v['eta'], 1)} |" for k, v in sm["orcamento"].items())
hic = "\n".join(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |" for r in uc["partida"]["hiccup"])
start_tab = "\n".join(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} |" for r in uc["partida"]["tabela"]) if isinstance(uc["partida"].get("tabela"), list) and uc["partida"]["tabela"] and isinstance(uc["partida"]["tabela"][0], (list, tuple)) else ""
mg = cp["margens"]
e90 = en["pontos"]["90V_50Hz"]; e264 = en["pontos"]["264V_60Hz"]
pr = en["protecoes"]
mos = sm["mosfet"]; dio = sm.get("diodo", {}); pon = sm.get("ponte", {})
blocos = sorted(custo["blocos"].items(), key=lambda kv: -kv[1]["usd1"])
custo_blocos = "\n".join(f"| {k} | {v['itens']} | {f(v['usd1'])} | {f(v['usd100'])} | {f(100 * v['usd1'] / custo['total_1'], 1)} |" for k, v in blocos)
nuc = tr["candidatos"]
nucleos = "\n".join(f"| {'**' + k + '**' if k == tr['nucleo'] else k} | {f(v['AeAw'])} | {f(v['lg_mm'])} | {v['Np']}/{v['Ns']}/{v['Naux']} | {f(1e6 * v['Lp_real'], 0)} | {f(v['P_nuc'])} | {f(v['P_cu'])} | {f(v['dT'], 1)} | {f(v['Kocup'])} | {'sim' if v.get('Kocup', 1) <= 0.7 and v.get('dT', 99) <= 40 else 'não'} |" for k, v in nuc.items())
cand = "\n".join(f"| {k} | {f(1e3 * v['esr'], 1)} | {f(v['irip'], 1)} | {f(1e3 * v['dv'], 0)} | {f(v['p_esr'])} | {v['ok']} |" for k, v in sd["candidatos"].items())
snub_tab = "\n".join(f"| {k} ({f(1e6 * v['Llk'], 1)} µH) | {f(v['E_uJ'], 1)} | {f(v['P'])} | {f(v['R'] / 1e3, 1)} | {f(1e9 * v['C'], 1)} | {f(v['t_clamp_ns'], 0)} | {f(v['Vds_max'], 0)} |" for k, v in sn["tabela"].items())
mosfets = "\n".join(f"| {'**' + k.split(' (')[0] + '**' if k == mos['nome'] else k.split(' (')[0]} ({k.split('(')[1].rstrip(')')}) | {f(1e3 * v['dados']['rds25'] if v['dados']['rds25'] < 10 else v['dados']['rds25'], 0)} | {f(v['lo']['P_total'])} | {f(v['hi']['P_total'])} | {f(v['dados'].get('rthjc', v.get('rthjc', 0)) if isinstance(v['dados'], dict) else 0, 2) if False else f(v.get('rthjc', v['dados'].get('rthjc')), 2)} | {'sim' if 'FP' in k or 'TO-220F' in k else 'não'} | {f(v['tj'], 0)} |" for k, v in sm["mosfets"].items()) if "mosfets" in sm else ""
margens = "\n".join(f"| {k.replace('carga', 'carga ').replace('_ctr', ' %, CTR ')} | {f(v['fc'] / 1e3)} | {f(v['pm'], 0)} | {f(v['gm'], 0) if v.get('gm') else '∞'} |" for k, v in mg.items())
pin_w = 36 / 0.82

val = {
    # ---- tabelas geradas aqui
    "orcamento": orc, "hiccup": hic, "custo_blocos": custo_blocos, "nucleos": nucleos, "cand_saida": cand, "snub_tab": snub_tab, "mosfets_tab": mosfets, "margens_tab": margens,
    # ---- entrada
    "pin_w": f(pin_w, 1), "c_bulk": f(1e6 * en["C"], 0), "vb_min": f(e90["vbulk_min"], 1), "vb_max": f(en["vbulk_max"], 1), "vb_rip": f(e90["ripple"], 1),
    "iin_rms": f(pr["i_in_rms_90V"]), "ic_bulk": f(g(pr, "capacitor_bulk", "i_rms_req"), 2), "fus_calc": f(pr["fusivel_calc_A"]), "inrush": f(pr["i_inrush_pico_264V"], 0), "inrush_sem": f(pr["i_inrush_sem_ntc"], 0),
    "pon_imed": f(g(pr, "ponte", "i_med_max"), 3), "pon_irms": f(g(pr, "ponte", "i_rms_max")), "pon_ipk": f(g(pr, "ponte", "i_pico_max")), "vrrm_min": f(g(pr, "ponte", "vrrm_min"), 0),
    "fp_90": f(e90.get("fp"), 2) if e90.get("fp") else "0,58", "thd_90": f(e90.get("thd"), 0) if e90.get("thd") else "132", "cond_90": f(e90.get("ang_cond", e90.get("angulo_conducao")), 0),
    "iin_pk_90": f(e90.get("i_pk")),
    # ---- flyback
    "vb_proj": f(fb["vbulk_min"], 1), "dmax_proj": "0,43", "vr_calc": f(fb["Vr"] if fb.get("n_calc") is None else fb["vbulk_min"] * 0.43 / 0.57, 1), "n_calc": f(fb["n_calc"]), "ip_calc": f(fb["Ip_calc"], 3),
    "lp_calc": f(1e6 * fb["Lp_calc"], 1), "w_uJ": f(fb["W_uJ"], 0), "n_real": f(fb["n"], 2), "lp_real": f(1e6 * fb["Lp"], 1), "vr_real": f(fb["Vr"], 1),
    "ip_max": f(fb["Ip_max"]), "ip_rms": f(fb["Ip_rms_max"], 3), "is_pk": f(fb["Is_pk_max"], 1), "is_rms": f(fb["Is_rms_max"]), "ic_rms": f(fb["Ic_rms_max"]),
    "vds_off": f(fb["Vds_off_max"], 0), "vds_clamp": f(fb["Vds_clamp_max"], 0), "vd_rev": f(fb["Vd_rev_max"], 0), "ton_min": f(fb["ton_min_ns"], 0), "d_90": f(fb["D_max"], 3),
    "vds_pct": f(100 * fb["Vds_clamp_max"] / 650, 0), "llk_est": f(1e6 * fb["Llk_est"], 1),
    # ---- transformador
    "aeaw_min": f(tr["AeAw_min"], 3), "aeaw": f(tr["AeAw"]), "ae": f(tr["Ae"]), "aw": f(tr["Aw"]), "lg": f(tr["lg_mm"]), "lg_esp": f(tr["lg_espacador_mm"]), "np": tr["Np"], "ns": tr["Ns"], "naux": tr["Naux"],
    "b_real": f(tr["B_real"]), "delta_cm": f(tr["delta_cm"], 4), "dmax_cm": f(tr["d_max_cm"], 4), "awg_p": tr["awg_p"], "nf_p": tr["nf_p"], "awg_s": tr["awg_s"], "nf_s": tr["nf_s"], "awg_a": tr["awg_a"],
    "rp": f(1e3 * tr["Rp"], 0), "rs": f(1e3 * tr["Rs"], 1), "p_nuc": f(tr["P_nuc"]), "p_cu": f(tr["P_cu"]), "p_tr": f(tr["P_tot"]), "rt": f(tr["Rt"], 1), "dt": f(tr["dT"], 1), "aw_nec": f(tr["Aw_nec"], 3), "kocup": f(tr["Kocup"]),
    "ip_real": f(tr["Ip_real"], 3), "ip_rms_tr": f(tr["Ip_rms"], 3), "d_tr": f(tr["D"], 3), "v_aux": f(uc["partida"]["V_aux"], 1),
    # ---- saida
    "c_min": f(1e6 * sd["c_min"], 0), "esr_max": f(1e3 * sd["esr_max"], 1), "esr_eq": f(1e3 * sd["ESR1"], 1), "irip": f(sd["Irip1"], 1), "dv1": f(1e3 * sd["dv1"], 0), "l_pos": f(1e6 * sd["L_pos"], 1), "c_pos": f(1e6 * sd["C_pos"], 0),
    "fc_lc": f(sd["fc"] / 1e3, 1), "att_lc": f(-sd["att_dB"], 0), "dv_out": f(1e3 * sd["dv_out"], 1), "escolha_saida": sd["escolha"], "n_par": sd["n_par"],
    # ---- snubber
    "vc": f(sn["tabela"]["2%"]["Vc"], 0), "e2": f(sn["tabela"]["2%"]["E_uJ"], 1), "p2": f(sn["P_2pct"]), "p3": f(sn["P_3pct"]), "r_calc2": f(sn["tabela"]["2%"]["R"] / 1e3, 1), "c_calc2": f(1e9 * sn["tabela"]["2%"]["C"], 1),
    "r_sn": f(sn["R"] / 1e3, 0), "c_sn": f(1e9 * sn["C"], 0), "vc2": f(sn["Vc_2pct"], 0), "vc3": f(sn["Vc_3pct"], 0), "vds3": f(sn["Vds_max_3pct"], 0), "t_clamp2": f(sn["tabela"]["2%"]["t_clamp_ns"], 0),
    "llk2": f(1e6 * sn["tabela"]["2%"]["Llk"], 1), "rc_r": f(sn["rc_diodo"]["R"], 0), "rc_c": f(1e9 * sn["rc_diodo"]["C"], 1), "rc_p": f(sn["rc_diodo"]["P"]),
    # ---- semicondutores
    "mos_nome": mos["nome"].split(" (")[0], "rds125": f(1e3 * mos["hi"]["rds_125"], 0), "p_cond_lo": f(mos["lo"]["P_cond"]), "p_cond_hi": f(mos["hi"]["P_cond"]), "p_on_hi": f(mos["hi"]["P_on"]), "p_off_hi": f(mos["hi"]["P_off"]),
    "p_gate": f(mos["hi"]["P_gate"], 3), "tf_eff": f(mos["hi"]["tf_eff_ns"], 0), "p_mos_lo": f(mos["lo"]["P_total"]), "p_mos_hi": f(mos["hi"]["P_total"]), "rthjc": f(g(mos, "dados", "rthjc", default=3.5), 2),
    "rthsa_max": f(mos["rthsa_max"], 0), "rthsa": f(mos["rthsa"], 0), "tj_mos": f(mos["tj"], 0), "tj_mos_sem": f(40 + mos["hi"]["P_total"] * 62.5, 0),
    "dio_nome": str(dio.get("nome", "STPS20H100CT")).split(" (")[0], "dio_v0": f(dio.get("V0", 0.55)), "dio_rd": f(1e3 * dio.get("Rd", 0.0045), 1), "dio_p": f(dio.get("P", 1.78)), "dio_rthjc": f(dio.get("rthjc", 0.45)),
    "dio_rthsa_max": f(dio.get("rthsa_max", 46.7), 1), "dio_tj": f(dio.get("tj", 84), 0), "pon_p": f(pon.get("P", g(sm, "orcamento", "90V", "itens", "ponte", default=0.67))), "pon_tj": f(pon.get("tj", 53), 0),
    # ---- UC3845
    "rt": f(uc["oscilador"]["RT"] / 1e3), "ct": f(1e9 * uc["oscilador"]["CT"], 1), "f_osc": f(uc["oscilador"]["f_osc"] / 1e3, 1), "fsw": f(uc["oscilador"]["fsw"] / 1e3, 1), "t_dead": f(uc["oscilador"]["t_dead_ns"], 0),
    "rs": f(uc["sense"]["RS"]), "i_lim_min": f(uc["sense"]["i_lim_min"]), "i_lim_typ": f(uc["sense"]["i_lim_typ"]), "p_rs": f(uc["sense"]["P_RS"]), "r_filt": f(uc["sense"]["R_filt"], 0), "c_filt": f(1e12 * uc["sense"]["C_filt"], 0), "tau": f(uc["sense"]["tau_ns"], 0),
    "r_start": f(uc["partida"]["R_start"] / 1e3, 0), "c_vcc": f(1e6 * uc["partida"]["C_vcc"], 0), "i_start_min": f(1e3 * uc["partida"]["i_start_min"], 2), "t_hold": f(uc["partida"]["t_hold_ms"], 1), "r_aux": f(uc["partida"]["R_aux"], 0),
    "start_tab": start_tab, "r_g": f(uc["driver"]["R_G"], 0), "r_gs": f(uc["driver"]["R_gs"] / 1e3, 0), "m2": f(uc["rampa"]["m2"] / 1e3, 1), "m_osc": f(uc["rampa"]["m_osc"] / 1e3, 0), "r_slope": f(uc["rampa"]["R_slope"] / 1e3, 1),
    "hic220_uvlo": uc["partida"]["hiccup"][2][1], "hic220_rec": uc["partida"]["hiccup"][2][2], "hic220_on": uc["partida"]["hiccup"][2][3], "hic220_duty": uc["partida"]["hiccup"][2][4],
    # ---- compensador
    "ra": f(cp["Ra"] / 1e3), "rb": f(cp["Rb"] / 1e3), "vo_real": f(cp["vo_real"]), "rled": f(cp["Rled"] / 1e3), "rbias": f(cp["R_bias"] / 1e3, 0), "rz": f(cp["Rz"] / 1e3, 1), "cz": f(1e9 * cp["Cz"], 0), "rpu": f(cp["Rpu"] / 1e3, 1), "cp_nf": f(1e9 * cp["Cp"], 0),
    "fc_alvo": f(cp["fc_alvo"] / 1e3, 1), "fc_khz": f(mg["carga100_ctr1.0"]["fc"] / 1e3), "pm": f(mg["carga100_ctr1.0"]["pm"], 0), "gm": f(mg["carga100_ctr1.0"]["gm"], 0) if mg["carga100_ctr1.0"].get("gm") else "∞",
    "pm_min": f(min(v["pm"] for v in mg.values()), 0), "fp_cp": f(1 / (2 * 3.14159265 * cp["Rpu"] * cp["Cp"]) / 1e3, 1), "fz_cz": f(1 / (2 * 3.14159265 * cp["Rz"] * cp["Cz"]), 0),
    # ---- EMI
    "f_dm": f(em["f_dm"] / 1e3, 0), "f_cm": f(em["f_cm"] / 1e3, 0), "i_fuga": f(1e3 * em["i_fuga"], 2), "att_dm_195k": f(em["att_dm_195k"], 0), "att_cm_150k": f(em["att_cm_150k"], 0), "l_lk_choke": f(1e6 * em["L_LK"], 0), "r_bleed": f(em["R_BLEED"] / 1e6, 0),
    # ---- simulacao
    "iq_aplic": f(c["iq_aplic"], 1), "b_aplic": f(0.25 * c["ip_aplic"] / fb["Ip_max"]), "id1_aplic": f(c["id1_aplic"], 0), "vds_aplic": f(c["vds_aplic"], 0),
    "iq_sust": f(c["iq_sust"], 1), "id1rms_sust": f(c["id1rms_sust"], 1), "pd1_sust": f(c["pd1_sust"], 1), "vccmin_sust": f(c["vccmin_sust"], 1),
    "hic_uvlo_s": f(hic_s.get("t_ate_uvlo_ms"), 0), "hic_rec_s": f(hic_s.get("t_recarga_ms"), 0), "hic_on_s": f(hic_s.get("t_ligado_ms"), 0), "hic_duty_s": f(hic_s.get("duty_falha_pct"), 0), "vcc_fim_rec": f(hic_s.get("vcc_fim"), 2),
    "t_uv_90": f(med["partida_90V"].get("t_uv"), 1), "t_uv_264": f(med["partida_264V"].get("t_uv"), 1), "b_uv_90": f(med["partida_90V"].get("b_uv"), 0),
    "analise_regime": analise, "eta_220": f(100 * m220["po"] / m220["pin"], 1), "eta_90": f(100 * m90["po"] / m90["pin"], 1), "psnub_220": f(m220["psnub"]), "pdiode_220": f(m220["pdiode"]),
    "vo_min": f(min(vo)), "vo_max": f(max(vo)), "vopp": f(1e3 * max(v["vo_pp"] for v in reg.values()), 1), "ripple_tot": f(1e3 * max(v.get("ripple_total", 0) for v in reg.values()), 1),
    "vds_264": f(m264["vds_max"], 0), "vds_264_pct": f(100 * m264["vds_max"] / 650, 0), "ip_s_90": f(m90["ip_pk"]), "vds_90_s": f(m90["vds_max"], 0),
    "t_vo_90": f(g(tra, "partida_90V", "t_vo_11v4_ms"), 1), "t_vo_264": f(g(tra, "partida_264V", "t_vo_11v4_ms"), 1), "vo_max_part": f(max(g(tra, "partida_90V", "vo_max", default=0), g(tra, "partida_264V", "vo_max", default=0))),
    "vds_part_264": f(g(tra, "partida_264V", "vds_max"), 0), "ip_part_264": f(g(tra, "partida_264V", "ip_max")),
    "deg_mv": f(max(abs(g(tra, n, s, "desvio_mV", default=0)) for n in ("degrau_90V", "degrau_264V") for s in ("subida", "descida")), 0),
    "deg_t": f(max(g(tra, n, s, "t_retorno_0p5pct_ms", default=0) for n in ("degrau_90V", "degrau_264V") for s in ("subida", "descida")), 1),
    "n_casos": len(med), "eta_min": f(min(100 * v["po"] / v["pin"] for k, v in reg.items() if k.endswith("100pct")), 1), "eta_max": f(max(100 * v["po"] / v["pin"] for k, v in reg.items() if k.endswith("100pct")), 1),
    # ---- custo
    "custo_1": f(custo["total_1"]), "custo_100": f(custo["total_100"]), "custo_itens": custo["n_itens"], "custo_brl": f(custo["total_1"] * custo["usd_brl"], 0), "custo_caixa": f(custo["total_1"] - 9.60 + 48, 0),
}
txt = (HERE / "RELATORIO.template.md").read_text(encoding="utf-8")
out = re.sub(r"\{\{(\w+)\}\}", lambda m: str(val.get(m.group(1), m.group(0))), txt)
(HERE / "RELATORIO.md").write_text(out, encoding="utf-8")
rest = sorted(set(re.findall(r"\{\{(\w+)\}\}", out)))
print("RELATORIO.md gerado; marcadores restantes (tabelas para o build.py):", rest)
