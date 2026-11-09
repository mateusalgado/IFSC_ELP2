"""Malha de tensao: TL431 + PC817 + UC3845 em modo corrente de pico (compensador tipo 2).

Modelo de pequenos sinais (flyback MCD, controle por corrente de pico):
  Po = 1/2 Lp Ip^2 fs  e  Ip = Vcomp_eff/(3 Rs)   (ganho 3 V/V do comparador, datasheet)
  -> Vo = Ip * sqrt(Lp fs Ro / 2)  =>  Gvc(0) = dVo/dVcomp = sqrt(Lp fs Ro/2)/(3 Rs)
  polo da carga em MCD: fp = 2/(2 pi Ro Co) ; zero da RSE: fz = 1/(2 pi RSE Co)
Compensador (TL431 com Zf = Rz + 1/sCz entre catodo e REF; divisor Ra/Rb; LED via Rled;
pull-up Rpu no COMP; polo do opto por Cp no COMP):
  Gc(s) = CTR * Rpu/Rled * (1 + Zf/Ra) * 1/(1 + s Rpu Cp)
Saida: resultados/compensador.json, assets/compensador_bode.png
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from params import *

VREF_431 = 2.495
CTR = 1.0            # PC817 rank B/C (0,8-1,6); projeto no valor central, verificado em 0,5 e 1,6
RPU = 4.7e3          # pull-up COMP-VREF (Ohm)
CP = 1.0e-9          # capacitor no COMP (polo de alta frequencia junto com Cce do opto ~ 1 nF)
VF_LED = 1.2
I_DIV = 1.0e-3       # corrente no divisor
FC_ALVO = 1500.0     # Hz
R_BIAS = 1.0e3       # resistor em paralelo com o LED (garante Ika >= 1 mA no TL431)


def e96(x):
    E96 = [1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.30, 1.33, 1.37, 1.40, 1.43, 1.47, 1.50, 1.54, 1.58, 1.62, 1.65, 1.69, 1.74, 1.78, 1.82, 1.87, 1.91, 1.96, 2.00, 2.05, 2.10, 2.15, 2.21, 2.26, 2.32, 2.37, 2.43, 2.49, 2.55, 2.61, 2.67, 2.74, 2.80, 2.87, 2.94, 3.01, 3.09, 3.16, 3.24, 3.32, 3.40, 3.48, 3.57, 3.65, 3.74, 3.83, 3.92, 4.02, 4.12, 4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23, 5.36, 5.49, 5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65, 6.81, 6.98, 7.15, 7.32, 7.50, 7.68, 7.87, 8.06, 8.25, 8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76]
    dec = 10 ** math.floor(math.log10(x))
    return min((v * dec for v in E96 + [10.0]), key=lambda v: abs(math.log(v / x)))


def e12(x):
    E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
    dec = 10 ** math.floor(math.log10(x))
    return min((v * dec for v in E12 + [10.0]), key=lambda v: abs(math.log(v / x)))


def planta(f, Lp, Rs, Ro, Co, esr, modo_mcc=False):
    s = 2j * math.pi * f
    g0 = math.sqrt(Lp * FS * Ro / 2) / (3 * Rs)
    wp = 2 / (Ro * Co)
    wz = 1 / (esr * Co)
    return g0 * (1 + s / wz) / (1 + s / wp)


def comp(f, Ra, Rz, Cz, Rled, ctr=CTR, rpu=RPU, cp=CP):
    s = 2j * math.pi * f
    zf = Rz + 1 / (s * Cz)
    return ctr * rpu / Rled * (1 + zf / Ra) / (1 + s * rpu * cp)


def margens(f, T):
    mag = 20 * np.log10(np.abs(T)); ph = np.unwrap(np.angle(T)) * 180 / math.pi
    idx = np.where(np.diff(np.sign(mag)) < 0)[0]
    if len(idx) == 0:
        return None, None, mag, ph
    i = idx[0]
    fc = f[i]; pm = 180 + ph[i]
    return fc, pm, mag, ph


def main():
    tr = load("trafo"); uc = load("uc3845"); sd = load("saida"); assert tr and uc and sd
    Lp = tr["Lp_real"]; Rs = uc["sense"]["RS"]
    Co = sd["C1"] + sd["C_pos"]; esr = sd["ESR1"]
    print("# Compensador da malha de tensão (TL431 + PC817 + UC3845)\n")
    # divisor
    Rb = e96(VREF_431 / I_DIV); Ra = e96((VO - VREF_431) / (VREF_431 / Rb))
    vo_real = VREF_431 * (1 + Ra / Rb)
    print(f"## Divisor de realimentação\n\n- Rb = **{Rb/1e3:.2f} kΩ**, Ra = **{Ra/1e3:.2f} kΩ** (1 %) → Vo = 2,495·(1 + Ra/Rb) = **{vo_real:.2f} V**")
    # LED: corrente maxima quando TL431 satura em Vka = 2,5 V
    i_led_max = 3.0e-3
    Rled = e96((VO - VF_LED - 2.5) / i_led_max)
    i_bias = VF_LED / R_BIAS
    print(f"- R_LED = **{Rled:.0f} Ω** → I_LED máx = {(VO-VF_LED-2.5)/Rled*1e3:.1f} mA (Vka = 2,5 V) ; R_bias = {R_BIAS/1e3:.0f} kΩ em paralelo com o LED → I_ka ≥ {i_bias*1e3:.1f} mA (TL431 exige ≥ 1 mA)")
    print(f"- COMP: pull-up R_pu = {RPU/1e3:.1f} kΩ ao VREF ; C_p = {CP*1e9:.0f} nF (polo em {1/(2*math.pi*RPU*CP)/1e3:.1f} kHz) ; PC817 CTR = {CTR} (rank B/C)\n")

    # planta em plena carga e em 10 %
    f = np.logspace(0, 5, 2000)
    rows = []
    print("## Planta (controle → saída), modo corrente de pico em MCD\n")
    for carga in (1.0, 0.5, 0.1):
        Ro = VO ** 2 / (PO * carga)
        g0 = math.sqrt(Lp * FS * Ro / 2) / (3 * Rs)
        fp = 2 / (2 * math.pi * Ro * Co); fz = 1 / (2 * math.pi * esr * Co)
        rows.append([f"{carga*100:.0f}", fmt(Ro, 1), fmt(g0, 2), fmt(20 * math.log10(g0), 1), fmt(fp, 1), fmt(fz / 1e3, 1)])
    print(md_table(["carga %", "Ro (Ω)", "G0 (V/V)", "G0 (dB)", "fp (Hz)", "fz RSE (kHz)"], rows))

    # projeto do tipo 2: zero em fp (plena carga), cruzamento em FC_ALVO
    Ro = VO ** 2 / PO
    fp = 2 / (2 * math.pi * Ro * Co)
    fz_c = fp                                  # zero do compensador sobre o polo da planta
    # ganho necessario em fc: |Gvc(fc)| * |Gc(fc)| = 1 ; com zero em fp: |1 + Zf/Ra| ≈ Rz/Ra + 1 ... resolve numericamente
    g_fc = abs(planta(FC_ALVO, Lp, Rs, Ro, Co, esr))
    # escolhe Rz/Ra para ganho mid-band: Gc_mid ≈ CTR*Rpu/Rled*(1 + Rz/Ra)  -> 1/g_fc (ignorando Cp)
    gc_need = 1 / g_fc
    k = gc_need / (CTR * RPU / Rled) - 1
    Rz = e96(max(k, 0.1) * Ra); Cz = e12(1 / (2 * math.pi * fz_c * Rz))
    print(f"\n## Compensador tipo 2 (zero sobre o polo da planta em plena carga, fc alvo = {FC_ALVO/1e3:.1f} kHz)\n")
    print(f"- |Gvc(fc)| = {20*math.log10(g_fc):.1f} dB → ganho necessário do compensador {20*math.log10(gc_need):.1f} dB → Rz/Ra = {k:.2f} → **Rz = {Rz/1e3:.2f} kΩ**, **Cz = {Cz*1e9:.0f} nF** (fz = {1/(2*math.pi*Rz*Cz):.0f} Hz)")

    # verificacao com margens para varias condicoes
    res = {}
    fig, ax = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
    for carga, ctr, ls in ((1.0, 1.0, "-"), (0.1, 1.0, "--"), (1.0, 1.6, ":"), (1.0, 0.5, "-.")):
        Ro = VO ** 2 / (PO * carga)
        T = planta(f, Lp, Rs, Ro, Co, esr) * comp(f, Ra, Rz, Cz, Rled, ctr)
        fc, pm, mag, ph = margens(f, T)
        gm_idx = np.where(np.diff(np.sign(ph + 180)) != 0)[0]
        gm = -mag[gm_idx[0]] if len(gm_idx) else None
        res[f"carga{int(carga*100)}_ctr{ctr}"] = dict(fc=fc, pm=pm, gm=gm)
        ax[0].semilogx(f, mag, ls, label=f"carga {carga*100:.0f} %, CTR {ctr}: fc = {fc/1e3:.2f} kHz, MF = {pm:.0f}°")
        ax[1].semilogx(f, ph, ls)
    ax[0].axhline(0, color="k", lw=.8); ax[0].set_ylabel("|T| (dB)"); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3, which="both")
    ax[1].axhline(-180, color="k", lw=.8); ax[1].set_ylabel("fase (°)"); ax[1].set_xlabel("f (Hz)"); ax[1].grid(alpha=.3, which="both")
    fig.suptitle("Ganho de malha T(s) = Gvc·Gc – flyback MCD em modo corrente, TL431 + PC817"); fig.tight_layout()
    fig.savefig(ASSETS / "compensador_bode.png", dpi=150)
    rows = [[k, fmt(v["fc"] / 1e3, 2) if v["fc"] else "—", fmt(v["pm"], 0) if v["pm"] else "—", fmt(v["gm"], 0) if v["gm"] else "∞"] for k, v in res.items()]
    print("\n## Margens de estabilidade\n")
    print(md_table(["condição", "fc (kHz)", "margem de fase (°)", "margem de ganho (dB)"], rows))
    ok = all(v["pm"] is not None and v["pm"] >= 45 for v in res.values())
    print(f"\nCritério MF ≥ 45° em todas as condições: **{'atende' if ok else 'NÃO atende – rever'}**")
    print("- Observação: em 90 VAC/plena carga o conversor entra levemente em MCC (D ≈ 0,44 < 0,5): o ganho da planta cai e surge o zero no semiplano direito em alta frequência (> 10 kHz, fora da banda); a simulação em LTspice verifica o degrau de carga nessa condição.")
    save("compensador", dict(Ra=Ra, Rb=Rb, Rled=Rled, R_bias=R_BIAS, Rz=Rz, Cz=Cz, Rpu=RPU, Cp=CP, CTR=CTR, fc_alvo=FC_ALVO, vo_real=vo_real, margens=res,
                             componentes=[
                                 dict(ref="U2", valor="TL431", descricao="referência ajustável 2,495 V, TO-92", pn="TI TL431ACLP / onsemi TL431BCLPG", qtd=1),
                                 dict(ref="U3", valor="PC817", descricao="optoacoplador CTR 80–160 % (rank B/C)", pn="Sharp PC817X2 / Everlight EL817C", qtd=1),
                                 dict(ref="Ra", valor=f"{Ra/1e3:.2f} kΩ 1 %", descricao="divisor superior", pn="", qtd=1),
                                 dict(ref="Rb", valor=f"{Rb/1e3:.2f} kΩ 1 %", descricao="divisor inferior", pn="", qtd=1),
                                 dict(ref="R_led", valor=f"{Rled:.0f} Ω", descricao="série do LED do opto", pn="", qtd=1),
                                 dict(ref="R_bias", valor=f"{R_BIAS/1e3:.0f} kΩ", descricao="polarização mínima do TL431", pn="", qtd=1),
                                 dict(ref="Rz", valor=f"{Rz/1e3:.2f} kΩ", descricao="compensador tipo 2", pn="", qtd=1),
                                 dict(ref="Cz", valor=f"{Cz*1e9:.0f} nF", descricao="compensador tipo 2", pn="", qtd=1),
                                 dict(ref="C_p", valor=f"{CP*1e9:.0f} nF", descricao="polo no COMP", pn="", qtd=1)]))
    print("\nFigura: assets/compensador_bode.png")


if __name__ == "__main__":
    main()
