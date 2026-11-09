"""Projeto eletrico do conversor flyback (MCD) - esforcos de tensao e corrente.

Metodo (Aula 04C / Barbi, Projeto de Fontes Chaveadas):
  - relacao de espiras n = Np/Ns a partir de Dmax na menor tensao de bulk
    (fronteira MCC/MCD em plena carga e Vin minimo);
  - Ip = 2 Pout / (eta Vinmin Dmax); Lp = Vinmin Dmax / (Ip fs);
  - em qualquer outro ponto (MCD): Ip = sqrt(2 Pin / (Lp fs)), D = Ip Lp fs / Vbulk.
Se resultados/trafo.json existir, usa n e Lp reais (apos arredondar espiras)
e marca a tabela como final.
Saidas: resultados/flyback.json, assets/flyback_formas_de_onda.png
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from params import *

K_CLAMP = 1.8          # tensao de grampo do snubber = K_CLAMP * Vr (1,5 na Aula 07; 1,8 reduz a perda no RCD)
K_LLK = 0.03           # indutancia de dispersao estimada = 3 % de Lp


def ponto(vbulk, carga, n, Lp, fs=FS):
    """esforcos em um ponto de operacao (MCD ou MCC)"""
    po = PO * carga
    pin = po / ETA
    vr = n * (VO + VF_DIODE_OUT)
    d_bcm = vr / (vbulk + vr)
    ip_bcm = 2 * pin / (vbulk * d_bcm)
    lp_bcm = vbulk * d_bcm / (ip_bcm * fs)
    if Lp <= lp_bcm:   # MCD
        ip = math.sqrt(2 * pin / (Lp * fs))
        d = ip * Lp * fs / vbulk
        d2 = ip * Lp * fs / vr
        modo = "MCD"
        ip_min = 0.0
    else:              # MCC
        d = d_bcm
        d2 = 1 - d
        i_med_p = pin / (vbulk * d)
        dip = vbulk * d / (Lp * fs)
        ip = i_med_p + dip / 2
        ip_min = i_med_p - dip / 2
        modo = "MCC"
    ton = d / fs
    ip_rms = ip * math.sqrt(d / 3) if modo == "MCD" else math.sqrt(d * (ip ** 2 + ip * ip_min + ip_min ** 2) / 3)
    ip_avg = ip * d / 2 if modo == "MCD" else d * (ip + ip_min) / 2
    is_pk = n * ip
    is_pk_min = n * ip_min
    is_rms = is_pk * math.sqrt(d2 / 3) if modo == "MCD" else math.sqrt(d2 * (is_pk ** 2 + is_pk * is_pk_min + is_pk_min ** 2) / 3)
    io = po / VO
    ic_rms = math.sqrt(max(is_rms ** 2 - io ** 2, 0))
    vds_off = vbulk + vr
    vds_clamp = vbulk + K_CLAMP * vr
    vd_rev = VO + vbulk / n
    return dict(vbulk=vbulk, carga=carga, modo=modo, D=d, D2=d2, ton_ns=ton * 1e9, Ip=ip, Ip_min=ip_min, Ip_rms=ip_rms, Ip_avg=ip_avg,
                Is_pk=is_pk, Is_rms=is_rms, Is_avg=io, Ic_rms=ic_rms, Vr=vr, Vds_off=vds_off, Vds_clamp=vds_clamp,
                Vd_rev=vd_rev, Pin=pin)


def main():
    ent = load("entrada")
    vb_min = min(94.6, ent["vbulk_min"]) if ent else 94.6  # vale conservador para manter o projeto de T1
    vb_max = ent["vbulk_max"] if ent else VAC_MAX * math.sqrt(2)
    trafo = load("trafo")

    print("# Projeto eletrico do flyback\n")
    vr = DMAX / (1 - DMAX) * vb_min
    n_calc = vr / (VO + VF_DIODE_OUT)
    ip = 2 * PO / (ETA * vb_min * DMAX)
    lp = vb_min * DMAX / (ip * FS)
    w = PO / (ETA * FS)
    print("## Projeto preliminar (fronteira MCD/MCC em Vbulk mín. e plena carga)\n")
    print(f"- Vbulk mín = {vb_min:.1f} V (90 VAC/50 Hz), Vbulk máx = {vb_max:.1f} V (264 VAC)")
    print(f"- Vr = Dmax/(1−Dmax)·Vbulk,min = {DMAX}/(1−{DMAX})·{vb_min:.1f} = **{vr:.1f} V**")
    print(f"- n = Np/Ns = Vr/(Vo+Vf) = {vr:.1f}/({VO}+{VF_DIODE_OUT}) = **{n_calc:.2f}**")
    print(f"- Ip = 2·Po/(η·Vbulk,min·Dmax) = 2·{PO:.0f}/({ETA}·{vb_min:.1f}·{DMAX}) = **{ip:.3f} A**")
    print(f"- Lp = Vbulk,min·Dmax/(Ip·fs) = **{lp*1e6:.1f} µH** ; energia por ciclo W = Po/(η·fs) = {w*1e6:.0f} µJ")

    if trafo:
        n = trafo["n_real"]; Lp = trafo["Lp_real"]
        print(f"\n**Valores finais do transformador (trafo.json):** n = {n:.3f} ({trafo['Np']}:{trafo['Ns']}), Lp = {Lp*1e6:.1f} µH\n")
        status = "final"
    else:
        n = n_calc; Lp = lp; status = "preliminar"

    pts = {}
    rows = []
    for vac in VAC_POINTS:
        key50 = f"{vac:.0f}V_50Hz"
        vb = ent["pontos"][key50]["vbulk_min"] if ent else vac * math.sqrt(2) * 0.8
        vbmax = ent["pontos"][f"{vac:.0f}V_60Hz"]["vbulk_max"] if ent else vac * math.sqrt(2)
        for carga in LOAD_POINTS:
            r = ponto(vb, carga, n, Lp)
            rv = ponto(vbmax, carga, n, Lp)
            r["Vds_off_max"] = rv["Vds_off"]; r["Vds_clamp_max"] = rv["Vds_clamp"]; r["Vd_rev_max"] = rv["Vd_rev"]
            r["vbulk_pico"] = vbmax
            pts[f"{vac:.0f}V_{int(carga*100)}%"] = r
            rows.append([f"{vac:.0f}", f"{int(carga*100)}", fmt(vb, 0), r["modo"], fmt(r["D"], 3), fmt(r["ton_ns"], 0),
                         fmt(r["Ip"], 2), fmt(r["Ip_rms"], 3), fmt(r["Is_pk"], 1), fmt(r["Is_rms"], 2), fmt(r["Ic_rms"], 2),
                         fmt(r["Vds_off_max"], 0), fmt(r["Vds_clamp_max"], 0), fmt(r["Vd_rev_max"], 0)])
    print(f"## Esforços por ponto de operação ({status}; correntes no vale de Vbulk, tensões no pico)\n")
    print(md_table(["Vac", "carga %", "Vb vale", "modo", "D", "ton (ns)", "Ip (A)", "Ip,rms (A)", "Is,pk (A)", "Is,rms (A)",
                    "Ic,rms (A)", "Vds off (V)", "Vds c/ grampo (V)", "Vd rev (V)"], rows))

    pior_i = pts["90V_100%"]
    pior_v = pts["264V_100%"]
    resumo = dict(
        status=status, n=n, Lp=Lp, n_calc=n_calc, Lp_calc=lp, Ip_calc=ip, Vr=pior_i["Vr"], W_uJ=w * 1e6,
        Ip_max=pior_i["Ip"], Ip_rms_max=pior_i["Ip_rms"], Is_pk_max=pior_i["Is_pk"], Is_rms_max=pior_i["Is_rms"],
        Ic_rms_max=pior_i["Ic_rms"], D_max=pior_i["D"],
        Vds_off_max=pior_v["Vds_off_max"], Vds_clamp_max=pior_v["Vds_clamp_max"], Vd_rev_max=pior_v["Vd_rev_max"],
        Llk_est=K_LLK * Lp, K_CLAMP=K_CLAMP, vbulk_min=vb_min, vbulk_max=vb_max, pontos=pts,
        ton_min_ns=min(p["ton_ns"] for p in pts.values()),
    )
    print("\n## Resumo para a escolha dos semicondutores\n")
    print(f"- MOSFET: Vds máx (com grampo a {K_CLAMP}·Vr) = **{resumo['Vds_clamp_max']:.0f} V** → classe 650 V (≤ 80 % → {0.8*650:.0f} V); Ip = {resumo['Ip_max']:.2f} A ; Ip,rms = {resumo['Ip_rms_max']:.3f} A")
    print(f"- Diodo de saída: Vrev máx = **{resumo['Vd_rev_max']:.0f} V** → Schottky 100 V; Is,pk = {resumo['Is_pk_max']:.1f} A ; Is,rms = {resumo['Is_rms_max']:.2f} A ; Is,med = {IO} A")
    print(f"- Capacitores de saída: Ic,rms = **{resumo['Ic_rms_max']:.2f} A** (90 VAC, plena carga)")
    print(f"- ton mínimo (264 VAC, 10 %) = {resumo['ton_min_ns']:.0f} ns (UC3845: ok se > ~350 ns)")
    print(f"- Llk estimada ({K_LLK*100:.0f} % de Lp) = {resumo['Llk_est']*1e6:.1f} µH (entrada do snubber)")
    save("flyback", resumo)

    fig, ax = plt.subplots(4, 2, figsize=(11, 9), sharex="col")
    for col, key in enumerate(("90V_100%", "264V_100%")):
        p = pts[key]
        vb = p["vbulk"] if col == 0 else p["vbulk_pico"]
        T = 1 / FS
        t = np.linspace(0, 2 * T, 2000)
        tt = t % T
        ton = p["D"] * T; toff2 = p["D2"] * T
        ip = np.where(tt < ton, p["Ip"] * tt / ton, 0)
        isec = np.where((tt >= ton) & (tt < ton + toff2), p["Is_pk"] * (1 - (tt - ton) / toff2), 0)
        vds = np.where(tt < ton, 0, np.where(tt < ton + toff2, vb + p["Vr"], vb))
        vd = np.where(tt < ton, -(VO + vb / n), np.where(tt < ton + toff2, -VF_DIODE_OUT, -VO))
        for a, y, lab in zip(ax[:, col], (ip, isec, vds, vd), ("i_p (A)", "i_s (A)", "v_DS (V)", "v_D (V)")):
            a.plot(t * 1e6, y, lw=1.5); a.set_ylabel(lab); a.grid(alpha=.3)
        ax[0, col].set_title(f"{key.replace('_', ', ')} carga – Vbulk = {vb:.0f} V, D = {p['D']:.2f}, {p['modo']}")
        ax[3, col].set_xlabel("tempo (µs)")
    fig.suptitle("Formas de onda teóricas do flyback (sem sobretensão de dispersão)")
    fig.tight_layout()
    fig.savefig(ASSETS / "flyback_formas_de_onda.png", dpi=150)
    print("\nFigura: assets/flyback_formas_de_onda.png")


if __name__ == "__main__":
    main()
