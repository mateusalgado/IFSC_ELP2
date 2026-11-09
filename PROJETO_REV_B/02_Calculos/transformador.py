"""Projeto fisico do transformador flyback - 14 passos da Aula 04C (Barbi).

Nucleos Thornton (tabela da aula) e fios AWG (tabela de Barbi, rho a 20 C;
rho a 100 C = 1,336 x). Saida: resultados/trafo.json, assets/trafo_nucleos.png
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from params import *

B_MAX = 0.25        # T (ferrite IP12R Thornton; 0,3 T na aula a 20 kHz -> reduzido por perdas a 65 kHz)
KW = 0.4            # fator de utilizacao da janela
KP = 0.3            # fator de ocupacao do primario (flyback)
J = 450.0           # A/cm2
KH, KE = 4e-5, 4e-10
MU0 = 4e-7 * math.pi
V_AUX = 15.0        # tensao do enrolamento auxiliar (VCC do UC3845)
VF_AUX = 0.9
I_AUX_RMS = 0.05    # A (consumo do UC3845 + gate) - estimativa
V_MOSFET = 650.0    # classe de tensao do MOSFET
V_DIODO = 100.0     # classe de tensao do diodo Schottky de saida

# nucleo: Ae, Aw, le, lt, Ve, AeAw  (cm2, cm2, cm, cm, cm3, cm4)
NUCLEOS = {
    "E-20":    (0.312, 0.26, 4.28, 3.8, 1.34, 0.08),
    "E-30/7":  (0.60, 0.80, 6.7, 5.6, 4.00, 0.48),
    "E-30/14": (1.20, 0.85, 6.7, 6.7, 8.00, 1.02),
    "E-42/15": (1.81, 1.57, 9.7, 8.7, 17.10, 2.84),
    "E-42/20": (2.40, 1.57, 9.7, 10.5, 23.30, 3.77),
    "E-55":    (3.54, 2.50, 12.0, 11.6, 42.50, 8.85),
}
# AWG: diametro cobre (cm), Acu (cm2), S isolado (cm2), rho 20C (ohm/cm)
FIOS = {
    20: (0.081, 0.005176, 0.006244, 0.000333), 21: (0.072, 0.004105, 0.005004, 0.000420),
    22: (0.064, 0.003255, 0.004013, 0.000530), 23: (0.057, 0.002582, 0.003221, 0.000668),
    24: (0.051, 0.002047, 0.002586, 0.000842), 25: (0.045, 0.001624, 0.002078, 0.001062),
    26: (0.040, 0.001287, 0.001671, 0.001339), 27: (0.036, 0.001021, 0.001344, 0.001689),
    28: (0.032, 0.000810, 0.001083, 0.002129), 29: (0.029, 0.000642, 0.000872, 0.002685),
    30: (0.025, 0.000509, 0.000704, 0.003386),
}


def projeto(nucleo, fb, B=B_MAX):
    Ae, Aw, le, lt, Ve, AeAw = NUCLEOS[nucleo]
    vb_min = fb["vbulk_min"]
    Ip = fb["Ip_calc"]; n_calc = fb["n_calc"]
    W = PO / (ETA * FS)
    lg = 2 * MU0 * W / (B ** 2 * Ae * 1e-4)          # m (total)
    Np = math.ceil(B * lg / (MU0 * Ip))
    # Ns: entre floor e ceil de Np/n, escolhe o que equilibra as margens de tensao
    # do MOSFET (classe 650 V) e do diodo Schottky (classe 100 V) na maior tensao de rede
    vb_max = fb["vbulk_max"]
    def margem(ns):
        nr = Np / ns
        vds = vb_max + 1.5 * nr * (VO + VF_DIODE_OUT)
        vd = VO + vb_max / nr
        return max(vds / V_MOSFET, vd / V_DIODO)
    cands_ns = sorted({max(1, math.floor(Np / n_calc)), max(1, math.ceil(Np / n_calc))})
    Ns = min(cands_ns, key=margem)
    n_real = Np / Ns
    Naux = max(1, round(Ns * (V_AUX + VF_AUX) / (VO + VF_DIODE_OUT)))
    Lp_real = MU0 * Np ** 2 * Ae * 1e-4 / lg
    vr = n_real * (VO + VF_DIODE_OUT)
    d_bcm = vr / (vb_min + vr)
    ip_bcm = 2 * PIN / (vb_min * d_bcm)
    lp_bcm = vb_min * d_bcm / (ip_bcm * FS)
    if Lp_real <= lp_bcm:
        Ip_real = math.sqrt(2 * PIN / (Lp_real * FS)); D = Ip_real * Lp_real * FS / vb_min; modo = "MCD"
    else:
        D = d_bcm; dip = vb_min * D / (Lp_real * FS); Ip_real = PIN / (vb_min * D) + dip / 2; modo = "MCC"
    B_real = MU0 * Np * Ip_real / lg
    D2 = Ip_real * Lp_real * FS / vr
    Ip_rms = Ip_real * math.sqrt(D / 3)
    Is_pk = n_real * Ip_real
    Is_rms = Is_pk * math.sqrt(D2 / 3)
    P_nuc = B_real ** 2.4 * (KH * FS + KE * FS ** 2) * Ve
    delta = 7.5 / math.sqrt(FS)
    d_max = 2 * delta
    awg_max = min(a for a, f in FIOS.items() if f[0] <= d_max)

    def fios(I_rms, awg):
        S = I_rms / J
        return max(1, math.ceil(S / FIOS[awg][1])), S
    awg_p = awg_max; nf_p, Sp = fios(Ip_rms, awg_p)
    awg_s = awg_max; nf_s, Ss = fios(Is_rms, awg_s)
    awg_a = 28;      nf_a, Sa = fios(I_AUX_RMS, awg_a)

    def R(N, awg, nf):
        return N * FIOS[awg][3] * 1.336 * lt / nf
    Rp, Rs, Ra = R(Np, awg_p, nf_p), R(Ns, awg_s, nf_s), R(Naux, awg_a, nf_a)
    P_cu = Rp * Ip_rms ** 2 + Rs * Is_rms ** 2 + Ra * I_AUX_RMS ** 2
    P_tot = P_nuc + P_cu
    Rt = 23 * AeAw ** -0.37
    dT = Rt * P_tot
    Aw_nec = (Np * nf_p * FIOS[awg_p][2] + Ns * nf_s * FIOS[awg_s][2] + Naux * nf_a * FIOS[awg_a][2]) / 0.7
    Kocup = Aw_nec / Aw
    Llk = 0.03 * Lp_real
    return dict(nucleo=nucleo, Ae=Ae, Aw=Aw, le=le, lt=lt, Ve=Ve, AeAw=AeAw, B=B, B_real=B_real, lg_mm=lg * 1e3,
                lg_espacador_mm=lg * 1e3 / 2, Np=Np, Ns=Ns, Naux=Naux, n_real=n_real, Lp_real=Lp_real,
                Ip_real=Ip_real, D=D, D2=D2, modo=modo, Ip_rms=Ip_rms, Is_pk=Is_pk, Is_rms=Is_rms, Vr=vr,
                delta_cm=delta, d_max_cm=d_max, awg_p=awg_p, nf_p=nf_p, awg_s=awg_s, nf_s=nf_s, awg_a=awg_a, nf_a=nf_a,
                Rp=Rp, Rs=Rs, Ra=Ra, P_nuc=P_nuc, P_cu=P_cu, P_tot=P_tot, Rt=Rt, dT=dT, Aw_nec=Aw_nec, Kocup=Kocup,
                Llk_est=Llk, W_uJ=W * 1e6, AeAw_min=1.1 * PO * 1e4 / (KW * KP * J * FS * B))


def main():
    fb = load("flyback")
    assert fb, "rode flyback.py antes"
    print("# Projeto fisico do transformador flyback (Aula 04C)\n")
    aeaw_min = 1.1 * PO * 1e4 / (KW * KP * J * FS * B_MAX)
    print(f"Dados: Po = {PO:.0f} W, fs = {FS/1e3:.0f} kHz, Vbulk,min = {fb['vbulk_min']:.1f} V, η = {ETA}, B = {B_MAX} T, kw = {KW}, kp = {KP}, J = {J:.0f} A/cm², Dmax = {DMAX}")
    print(f"\n- Ip = {fb['Ip_calc']:.3f} A ; W = Po/(η·fs) = {PO/(ETA*FS)*1e6:.0f} µJ")
    print(f"- AeAw mín = 1,1·Po·10⁴/(kw·kp·J·fs·B) = **{aeaw_min:.3f} cm⁴**\n")

    rows = []; cands = {}
    for nome in ("E-30/7", "E-30/14", "E-42/15"):
        r = projeto(nome, fb)
        cands[nome] = r
        ok = "sim" if (r["Kocup"] <= 1.0 and r["dT"] <= 40 and r["AeAw"] >= aeaw_min) else "não"
        rows.append([nome, fmt(r["AeAw"], 2), fmt(r["lg_mm"], 2), r["Np"], r["Ns"], r["Naux"], fmt(r["n_real"], 2),
                     fmt(r["Lp_real"] * 1e6, 0), fmt(r["B_real"], 3), f"{r['nf_p']}×{r['awg_p']}", f"{r['nf_s']}×{r['awg_s']}",
                     fmt(r["P_nuc"], 2), fmt(r["P_cu"], 2), fmt(r["dT"], 1), fmt(r["Kocup"], 2), ok])
    print("## Comparação de núcleos Thornton\n")
    print(md_table(["Núcleo", "AeAw", "lg (mm)", "Np", "Ns", "Naux", "n", "Lp (µH)", "B pico (T)", "fio prim.", "fio sec.",
                    "P núcleo (W)", "P cobre (W)", "ΔT (°C)", "Kocup", "atende"], rows))

    escolhido = next(nome for nome in ("E-30/7", "E-30/14", "E-42/15")
                     if cands[nome]["Kocup"] <= 1.0 and cands[nome]["dT"] <= 40 and cands[nome]["AeAw"] >= aeaw_min)
    r = cands[escolhido]
    print(f"\n## Núcleo escolhido: **{escolhido}** (Thornton NEE-{escolhido[2:]}, material IP12R)\n")
    print(f"- Entreferro total lg = 2·µ0·W/(B²·Ae) = **{r['lg_mm']:.2f} mm** (espaçador de {r['lg_espacador_mm']:.2f} mm em cada perna externa, ou {r['lg_mm']:.2f} mm só na perna central)")
    print(f"- Np = B·lg/(µ0·Ip) = **{r['Np']} espiras** ; Ns = Np/n = **{r['Ns']}** ; Naux = **{r['Naux']}** (Vaux ≈ {V_AUX} V) → n real = {r['n_real']:.3f}")
    print(f"- Lp real = µ0·Np²·Ae/lg = **{r['Lp_real']*1e6:.0f} µH** ; Ip real (90 VAC, 100 %) = {r['Ip_real']:.3f} A ({r['modo']}, D = {r['D']:.3f}) ; B pico real = {r['B_real']:.3f} T")
    print(f"- Profundidade de penetração Δ = 7,5/√fs = {r['delta_cm']:.4f} cm → d máx = {r['d_max_cm']:.3f} cm → fio ≤ {r['awg_p']} AWG")
    print(f"- Primário: Ip,rms = {r['Ip_rms']:.3f} A → {r['nf_p']} × {r['awg_p']} AWG ; Secundário: Is,rms = {r['Is_rms']:.2f} A → {r['nf_s']} × {r['awg_s']} AWG ; Auxiliar: {r['nf_a']} × {r['awg_a']} AWG")
    print(f"- Resistências (100 °C): Rp = {r['Rp']*1e3:.1f} mΩ, Rs = {r['Rs']*1e3:.2f} mΩ")
    print(f"- Perdas: núcleo {r['P_nuc']:.2f} W + cobre {r['P_cu']:.2f} W = **{r['P_tot']:.2f} W** ; Rt = {r['Rt']:.1f} °C/W → **ΔT = {r['dT']:.1f} °C**")
    print(f"- Ocupação: Aw,nec = {r['Aw_nec']:.3f} cm² / Aw = {r['Aw']} cm² → **Kocup = {r['Kocup']:.2f}**")
    print(f"- Llk estimada (3 %) = {r['Llk_est']*1e6:.1f} µH ; tensão refletida Vr = {r['Vr']:.1f} V")

    rows = []
    for B in (0.20, 0.25, 0.30):
        rb = projeto(escolhido, fb, B)
        rows.append([fmt(B, 2), rb["Np"], rb["Ns"], fmt(rb["lg_mm"], 2), fmt(rb["Lp_real"] * 1e6, 0), fmt(rb["P_nuc"], 2), fmt(rb["P_cu"], 2), fmt(rb["dT"], 1), fmt(rb["Kocup"], 2)])
    print(f"\n## Sensibilidade à densidade de fluxo ({escolhido})\n")
    print(md_table(["B (T)", "Np", "Ns", "lg (mm)", "Lp (µH)", "P núcleo (W)", "P cobre (W)", "ΔT (°C)", "Kocup"], rows))

    r["candidatos"] = {k: dict(v) for k, v in cands.items()}
    r["B_MAX"] = B_MAX; r["KW"] = KW; r["KP"] = KP; r["J"] = J; r["V_AUX"] = V_AUX
    r["ordem_enrolamento"] = ("1) metade do primário (Np/2) junto ao carretel; 2) auxiliar; 3) secundário com fio triplo-isolado "
                              "(ou 3 camadas de fita de poliéster); 4) outra metade do primário (sanduíche, reduz Llk). "
                              "Blindagem de cobre opcional entre primário e secundário ligada ao bulk negativo.")
    save("trafo", r)

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    nomes = list(cands)
    ax[0].bar(nomes, [cands[k]["Kocup"] for k in nomes], color=["C0" if k == escolhido else "0.7" for k in nomes])
    ax[0].axhline(1.0, color="C3", ls="--", label="limite (Kocup = 1)"); ax[0].set_ylabel("Kocup"); ax[0].legend(); ax[0].grid(alpha=.3, axis="y")
    w = 0.35; x = np.arange(len(nomes))
    ax[1].bar(x - w / 2, [cands[k]["P_nuc"] for k in nomes], w, label="núcleo")
    ax[1].bar(x + w / 2, [cands[k]["P_cu"] for k in nomes], w, label="cobre")
    ax2 = ax[1].twinx(); ax2.plot(x, [cands[k]["dT"] for k in nomes], "k.-", label="ΔT"); ax2.set_ylabel("ΔT (°C)")
    ax[1].set_xticks(x); ax[1].set_xticklabels(nomes); ax[1].set_ylabel("perdas (W)"); ax[1].legend(loc="upper left"); ax[1].grid(alpha=.3, axis="y")
    fig.suptitle(f"Transformador flyback – comparação de núcleos (B = {B_MAX} T, fs = {FS/1e3:.0f} kHz)")
    fig.tight_layout(); fig.savefig(ASSETS / "trafo_nucleos.png", dpi=150)
    print("\nFigura: assets/trafo_nucleos.png")


if __name__ == "__main__":
    main()
