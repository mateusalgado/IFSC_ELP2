"""Escolha dos semicondutores, perdas e dissipadores (Aulas 02 e 03; mesmo metodo das Tarefas 1 e 2).

MOSFET (flyback em MCD):
  P_cond = Ip_rms^2 * RDS(on)(125 C)
  P_on   = 1/2 Co(er) Vds_on^2 fs        (entrada em conducao com corrente nula: so a energia de Coss)
  P_off  = 1/2 Vds_clamp Ip t_f,eff fs   (t_f,eff = max(tf datasheet, Qgd/Ig,off))
  P_gate = Qg Vgs fs
Diodo Schottky: P = V0 Io + Rd Is_rms^2 (modelo V0 + Rd I, 125 C). Ponte: idem com 4 diodos.
Saida: resultados/semicondutores.json, assets/perdas_semicondutores.png
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from params import *

# ---- MOSFETs candidatos (datasheets: Infineon IPA65R400CE rev 2.1 2017; ST STP13N65M2 DS10587 rev 2; onsemi NTPF190N65S3HF/FCPF190N65S3) ----
MOSFETS = {
    "IPA65R400CE (Infineon CoolMOS CE, TO-220FP)": dict(
        vds=650, rds25=0.40, k_t=2.1, qg=20e-9, qgs=4e-9, qgd=6e-9, vpl=5.5, coer=32e-12, tf=11e-9, rg_int=17.0, rthjc=4.0, rthja=80.0, tj=150, isolado=True,
        preco="≈ US$ 1,0"),
    "STP13N65M2 (ST MDmesh M2, TO-220)": dict(
        vds=650, rds25=0.43, k_t=2.0, qg=17e-9, qgs=3.3e-9, qgd=7e-9, vpl=5.0, coer=27.5e-12, tf=12e-9, rg_int=6.5, rthjc=1.14, rthja=62.5, tj=150, isolado=False,
        preco="≈ US$ 1,3"),
    "FCPF190N65S3 (onsemi SuperFET III, TO-220F)": dict(
        vds=650, rds25=0.19, k_t=2.0, qg=34e-9, qgs=11e-9, qgd=13e-9, vpl=5.5, coer=59e-12, tf=14e-9, rg_int=1.5, rthjc=3.5, rthja=62.5, tj=150, isolado=True,
        preco="≈ US$ 1,9"),
}
# ---- diodos de saida (modelo V0 + Rd I a 125 C) ----
DIODOS = {
    "STPS20H100CT (ST, 2×10 A, 100 V) – ânodos em paralelo": dict(v0=0.55, rd=0.0045, rthjc=0.45, vrrm=100, tj=175, pn="STPS20H100CT"),
    "STPS20H100CT (ST) – uma perna": dict(v0=0.55, rd=0.009, rthjc=0.9, vrrm=100, tj=175, pn="STPS20H100CT"),
    "MBR20100CT (onsemi/Vishay, 2×10 A, 100 V) – paralelo": dict(v0=0.62, rd=0.006, rthjc=1.0, vrrm=100, tj=150, pn="MBR20100CT"),
    "MBR10100 (onsemi, 10 A, 100 V)": dict(v0=0.65, rd=0.012, rthjc=2.0, vrrm=100, tj=150, pn="MBR10100G"),
}
PONTE = dict(nome="GBU4J (Vishay, 4 A / 600 V)", v0=0.75, rd=0.06, rthja=20.0, pn="GBU4J-E3/51")
DISSIPADORES = {  # RthSA em conveccao natural, TO-220
    "sem dissipador": None,
    "clip Aavid 574502B00000G (TO-220, 19×13 mm)": 24.0,
    "Same Sky HSE17-252525P (25×25×25 mm)": 12.6,
    "Same Sky HSE15-644225P (64×42×25 mm)": 7.0,
}
VGS_DRV = 13.0


def perdas_mosfet(m, p, vds_on, vds_clamp, r_g_ext=10.0, r_drv_sink=10.0):
    rds = m["rds25"] * m["k_t"]
    p_cond = p["Ip_rms"] ** 2 * rds
    p_on = 0.5 * m["coer"] * vds_on ** 2 * FS
    ig_off = m["vpl"] / (r_g_ext + m["rg_int"] + r_drv_sink)
    tf_eff = max(m["tf"], m["qgd"] / ig_off)
    p_off = 0.5 * vds_clamp * p["Ip"] * tf_eff * FS
    p_gate = m["qg"] * VGS_DRV * FS
    return dict(rds_125=rds, P_cond=p_cond, P_on=p_on, P_off=p_off, P_gate=p_gate, tf_eff_ns=tf_eff * 1e9,
                P_total=p_cond + p_on + p_off + p_gate)


def dissipador(P, rthjc, rthja, isolado):
    rthcs = 0.3 if isolado else R_THCS          # FullPAK: sem mica -> interface direta; TO-220: pasta + mica
    rthsa_max = (TJ_PROJ - TA) / P - rthjc - rthcs
    tj_sem = TA + P * rthja
    if tj_sem <= 100.0:            # sem dissipador so se Tj ficar abaixo de 100 C (margem sobre a meta de 125 C)
        return "sem dissipador", None, rthsa_max, tj_sem
    for nome, rsa in DISSIPADORES.items():
        if rsa is not None and rsa <= rthsa_max:
            return nome, rsa, rthsa_max, TA + P * (rthjc + rthcs + rsa)
    return "NENHUM ATENDE", None, rthsa_max, None


def main():
    fb = load("flyback"); tr = load("trafo"); ent = load("entrada"); sn = load("snubber"); uc = load("uc3845"); sd = load("saida")
    assert fb and tr and ent and sn and uc and sd
    pts = fb["pontos"]
    p_lo, p_hi = pts["90V_100%"], pts["264V_100%"]
    vds_clamp = fb["vbulk_max"] + sn["Vc_2pct"]
    print("# Semicondutores: pré-escolha, perdas e dissipadores\n")
    print("## Pré-escolha (Aula 03: tensão de bloqueio, corrente de pico e média, pior caso)\n")
    print(f"- MOSFET: Vds máx (264 VAC + grampo) = {vds_clamp:.0f} V → classe **650 V** ({100*vds_clamp/650:.0f} %); Ip = {fb['Ip_max']:.2f} A, Ip,rms = {fb['Ip_rms_max']:.3f} A → ID ≥ 4 A ; TO-220 (dissipador possível)")
    print(f"- Diodo de saída: Vrev = {fb['Vd_rev_max']:.0f} V → Schottky **100 V** ({fb['Vd_rev_max']:.0f} %); Is,pk = {fb['Is_pk_max']:.1f} A, Is,med = {IO:.0f} A, Is,rms = {fb['Is_rms_max']:.2f} A → ≥ 10 A ; Schottky (sem recuperação reversa, Aula 02)")
    print(f"- Ponte: VRRM ≥ 1,5·{fb['vbulk_max']:.0f} = {1.5*fb['vbulk_max']:.0f} V → **600 V** ; I_med/diodo = {ent['protecoes']['ponte']['i_med_max']:.2f} A, I_pico = {ent['protecoes']['ponte']['i_pico_max']:.1f} A, surto de inrush {ent['protecoes']['i_inrush_pico_264V']:.0f} A → 2–4 A (IFSM ≥ 100 A)")

    # ---- MOSFETs ----
    print("\n## MOSFET – perdas (90 VAC: pior condução; 264 VAC: pior comutação)\n")
    rows = []; res_m = {}
    for nome, m in MOSFETS.items():
        r_lo = perdas_mosfet(m, p_lo, p_lo["vbulk"], ent["pontos"]["90V_60Hz"]["vbulk_max"] + sn["Vc_2pct"], uc["driver"]["R_g_off"], uc["driver"]["R_drv_sink"])
        r_hi = perdas_mosfet(m, p_hi, p_hi["vbulk_pico"], vds_clamp, uc["driver"]["R_g_off"], uc["driver"]["R_drv_sink"])
        pior = max(r_lo, r_hi, key=lambda r: r["P_total"])
        dis, rsa, rsa_max, tj = dissipador(pior["P_total"], m["rthjc"], m["rthja"], m["isolado"])
        res_m[nome] = dict(lo=r_lo, hi=r_hi, pior=pior, dissipador=dis, rthsa=rsa, rthsa_max=rsa_max, tj=tj, dados=m)
        rows.append([nome, fmt(m["rds25"] * 1e3, 0), fmt(m["qg"] * 1e9, 0), fmt(pior["P_cond"], 2), fmt(r_hi["P_on"], 2), fmt(pior["P_off"], 2), fmt(pior["P_gate"], 3),
                     fmt(r_lo["P_total"], 2), fmt(r_hi["P_total"], 2), fmt(m["rthjc"], 2), fmt(rsa_max, 0), dis, fmt(tj, 0), m["preco"]])
    print(md_table(["MOSFET", "RDS(on) 25 °C (mΩ)", "Qg (nC)", "P cond (W)", "P on/Coss (W)", "P off (W)", "P gate (W)", "P tot 90 V (W)", "P tot 264 V (W)",
                    "RθJC", "RθSA máx", "dissipador", "Tj (°C)", "custo"], rows))
    # escolha: menor perda total entre os que dispensam dissipador grande; criterio: P_total pior caso
    escolhido_m = min(res_m, key=lambda k: res_m[k]["pior"]["P_total"])
    m = res_m[escolhido_m]
    print(f"\n**Escolhido: {escolhido_m}** – menor perda total ({m['pior']['P_total']:.2f} W), RθJC = {m['dados']['rthjc']} °C/W, "
          f"{'encapsulamento isolado (sem mica)' if m['dados']['isolado'] else 'TO-220 padrão (mica + pasta)'} ; dissipador: **{m['dissipador']}** → Tj ≈ {m['tj']:.0f} °C (meta ≤ {TJ_PROJ:.0f} °C)")
    print(f"- tf efetivo (carga de gate, Ig,off = Vpl/(Rg+Rg,int+Rdrv)) = {m['pior']['tf_eff_ns']:.0f} ns ; sem dissipador Tj seria {TA + m['pior']['P_total']*m['dados']['rthja']:.0f} °C")

    # ---- diodo de saida ----
    print("\n## Diodo de saída – perdas e dissipador\n")
    rows = []; res_d = {}
    for nome, d in DIODOS.items():
        P = d["v0"] * IO + d["rd"] * fb["Is_rms_max"] ** 2
        dis, rsa, rsa_max, tj = dissipador(P, d["rthjc"], 62.0, False)
        res_d[nome] = dict(P=P, dissipador=dis, rthsa=rsa, rthsa_max=rsa_max, tj=tj, dados=d)
        rows.append([nome, fmt(d["v0"], 2), fmt(d["rd"] * 1e3, 1), fmt(P, 2), fmt(d["rthjc"], 2), fmt(rsa_max, 1), dis, fmt(tj, 0)])
    print(md_table(["Diodo", "V0 (V)", "Rd (mΩ)", "P (W)", "RθJC", "RθSA máx", "dissipador", "Tj (°C)"], rows))
    escolhido_d = "STPS20H100CT (ST, 2×10 A, 100 V) – ânodos em paralelo"
    d = res_d[escolhido_d]
    print(f"\n**Escolhido: {escolhido_d}** – P = {d['P']:.2f} W, dissipador **{d['dissipador']}** → Tj ≈ {d['tj']:.0f} °C (mesma prática das Tarefas 1 e 2; Tj máx 175 °C)")

    # ---- ponte ----
    pb = ent["protecoes"]["ponte"]
    P_ponte = 4 * (PONTE["v0"] * pb["i_med_max"] + PONTE["rd"] * pb["i_rms_max"] ** 2)
    tj_ponte = TA + P_ponte * PONTE["rthja"]
    print(f"\n## Ponte retificadora\n\n- **{PONTE['nome']}**: P ≈ 4·(V0·I_med + Rd·I_rms²) = {P_ponte:.2f} W (90 VAC) ; RθJA ≈ {PONTE['rthja']:.0f} °C/W → Tj ≈ {tj_ponte:.0f} °C → sem dissipador")

    # ---- orcamento de perdas e rendimento ----
    print("\n## Orçamento de perdas e rendimento estimado (plena carga)\n")
    def budget(vac):
        p = pts[f"{vac:.0f}V_100%"]
        e = ent["pontos"][f"{vac:.0f}V_50Hz"]
        key = "lo" if vac < 150 else "hi"
        pm = m[key]["P_total"]
        pd = d["dados"]["v0"] * IO + d["dados"]["rd"] * p["Is_rms"] ** 2
        pponte = 4 * (PONTE["v0"] * e["i_diode_avg"] + PONTE["rd"] * e["i_diode_rms"] ** 2)
        ptr = tr["P_nuc"] + tr["Rp"] * p["Ip_rms"] ** 2 + tr["Rs"] * p["Is_rms"] ** 2
        psn = sn["P_2pct"] * (p["Ip"] / fb["Ip_max"]) ** 2
        prs = p["Ip_rms"] ** 2 * uc["sense"]["RS"]
        pst = e["vbulk_max"] ** 2 / uc["partida"]["R_start"]
        pcap = sd["ESR1"] * p["Ic_rms"] ** 2
        pntc = e["i_rms_in"] ** 2 * 1.0
        pl = IO ** 2 * 0.01
        pci = 15e-3 * 15.0
        itens = dict(MOSFET=pm, diodo=pd, ponte=pponte, transformador=ptr, snubber=psn, Rsense=prs, startup=pst, capacitores_saida=pcap, NTC=pntc, indutor_LC=pl, UC3845=pci)
        tot = sum(itens.values())
        return itens, tot, PO / (PO + tot)
    rows = []; bud = {}
    for vac in (90.0, 127.0, 220.0, 264.0):
        itens, tot, eta = budget(vac)
        bud[f"{vac:.0f}V"] = dict(itens=itens, total=tot, eta=eta)
        rows.append([f"{vac:.0f}"] + [fmt(itens[k], 2) for k in itens] + [fmt(tot, 2), fmt(eta * 100, 1)])
    print(md_table(["Vac"] + list(bud["90V"]["itens"].keys()) + ["total (W)", "η (%)"], rows))
    print(f"\nHipótese de projeto η = {ETA*100:.0f} % → estimativa {min(b['eta'] for b in bud.values())*100:.1f}–{max(b['eta'] for b in bud.values())*100:.1f} % : {'consistente' if min(b['eta'] for b in bud.values()) >= ETA - 0.02 else 'REVER hipótese de rendimento'}")

    save("semicondutores", dict(
        mosfet=dict(nome=escolhido_m, **{k: v for k, v in m.items() if k != "dados"}, dados=m["dados"]),
        mosfets=res_m, diodo=dict(nome=escolhido_d, **d), diodos=res_d,
        ponte=dict(**PONTE, P=P_ponte, tj=tj_ponte), orcamento=bud,
        componentes=[
            dict(ref="Q1", valor=escolhido_m.split(" ")[0], descricao="MOSFET 650 V", pn=escolhido_m.split(" ")[0], qtd=1),
            dict(ref="HS1", valor=m["dissipador"], descricao="dissipador do MOSFET", pn="", qtd=0 if m["dissipador"] == "sem dissipador" else 1),
            dict(ref="D1", valor="STPS20H100CT", descricao="Schottky de saída 2×10 A/100 V (pernas em paralelo)", pn="STPS20H100CT", qtd=1),
            dict(ref="HS2", valor=d["dissipador"], descricao="dissipador do diodo", pn="", qtd=0 if d["dissipador"] == "sem dissipador" else 1),
            dict(ref="BR1", valor="GBU4J", descricao="ponte retificadora 4 A/600 V", pn=PONTE["pn"], qtd=1)]))

    # figura
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    nomes = [k.split(" ")[0] for k in res_m]
    parts = ["P_cond", "P_on", "P_off", "P_gate"]; labels = ["condução", "Coss (on)", "comutação (off)", "gate"]
    bottom = np.zeros(len(nomes))
    for pk, lab in zip(parts, labels):
        vals = np.array([max(res_m[k]["lo"][pk], res_m[k]["hi"][pk]) for k in res_m])
        ax[0].bar(nomes, vals, bottom=bottom, label=lab); bottom += vals
    ax[0].set_ylabel("perdas (W)"); ax[0].set_title("MOSFET – pior caso por parcela"); ax[0].legend(); ax[0].grid(alpha=.3, axis="y")
    b = bud["90V"]["itens"]; b2 = bud["220V"]["itens"]
    x = np.arange(len(b)); w = 0.38
    ax[1].bar(x - w / 2, list(b.values()), w, label="90 VAC"); ax[1].bar(x + w / 2, list(b2.values()), w, label="220 VAC")
    ax[1].set_xticks(x); ax[1].set_xticklabels(list(b.keys()), rotation=45, ha="right"); ax[1].set_ylabel("W"); ax[1].set_title("Orçamento de perdas (plena carga)"); ax[1].legend(); ax[1].grid(alpha=.3, axis="y")
    fig.tight_layout(); fig.savefig(ASSETS / "perdas_semicondutores.png", dpi=150)
    print("\nFigura: assets/perdas_semicondutores.png")


if __name__ == "__main__":
    main()
