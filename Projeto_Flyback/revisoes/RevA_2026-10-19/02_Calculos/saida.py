"""Filtro de saida: capacitores (6 criterios da Aula 03) + pos-filtro LC.

Saida: resultados/saida.json, assets/saida_ripple.png
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from params import *

# candidatos (dados de catalogo a 105 C / 100 kHz)
CAPS = {
    "Rubycon ZLH 1000µF/25V (10x20)": dict(C=1000e-6, ESR=0.019, Irip=2.00, V=25),
    "Nichicon UPW 1000µF/25V (10x20)": dict(C=1000e-6, ESR=0.030, Irip=1.66, V=25),
    "Rubycon ZLH 1500µF/25V (12.5x20)": dict(C=1500e-6, ESR=0.015, Irip=2.55, V=25),
}
ESCOLHA = "Rubycon ZLH 1000µF/25V (10x20)"
N_PAR = 3
L_POS = 3.3e-6      # H, indutor do pos-filtro (> 3 A)
C_POS = 470e-6      # F, capacitor apos o LC
ESR_POS = 0.040


def main():
    fb = load("flyback"); assert fb
    p = fb["pontos"]["90V_100%"]
    T = 1 / FS
    d, d2 = p["D"], p["D2"]
    is_pk, ic_rms = p["Is_pk"], p["Ic_rms"]
    print("# Filtro de saída\n")
    print(f"Pior caso (90 VAC, plena carga): Is,pk = {is_pk:.1f} A, D = {d:.3f}, D2 = {d2:.3f}, Ic,rms = {ic_rms:.2f} A\n")
    dv_cap = 0.05
    c_min = IO * (1 - d2) * T / dv_cap
    esr_max = (DVO_PP_MAX - dv_cap) / is_pk
    print("## Critérios (Aula 03)\n")
    print(f"1. Capacitância mínima (ΔV_C = {dv_cap*1e3:.0f} mV): C ≥ Io·(1−D2)·T/ΔV = {c_min*1e6:.0f} µF")
    print(f"2. RSE máxima para ΔVo ≤ {DVO_PP_MAX*1e3:.0f} mV sem pós-filtro: RSE ≤ {esr_max*1e3:.1f} mΩ → impraticável com 1 eletrolítico ⇒ banco em paralelo + pós-filtro LC")
    print(f"3. Corrente eficaz: Ic,rms = {ic_rms:.2f} A (dado de catálogo a 105 °C, 100 kHz)")
    print(f"4. Tensão: ≥ 1,5–2 × Vo → 25 V")
    print(f"5. Temperatura: 105 °C, vida ≥ 5000 h; operação a Ta = 40 °C prolonga a vida")
    print(f"6. Custo/volume: eletrolítico de baixa impedância 10 × 20 mm\n")
    rows = []; res = {}
    for nome, c in CAPS.items():
        for npar in (2, 3):
            esr = c["ESR"] / npar; irip = c["Irip"] * npar
            dv_esr = is_pk * esr
            dv_c = IO * (1 - d2) * T / (c["C"] * npar)
            dv = dv_esr + dv_c
            p_esr = esr * ic_rms ** 2
            ok = "sim" if irip >= ic_rms else "não"
            res[f"{nome} x{npar}"] = dict(esr=esr, irip=irip, dv=dv, p_esr=p_esr, ok=ok)
            rows.append([nome, npar, fmt(esr * 1e3, 1), fmt(irip, 2), ok, fmt(dv_esr * 1e3, 0), fmt(dv_c * 1e3, 0), fmt(dv * 1e3, 0), fmt(p_esr, 2)])
    print(md_table(["Capacitor", "n paralelo", "RSE eq (mΩ)", "I ripple (A)", "I ripple ≥ Ic,rms", "ΔV RSE (mV)", "ΔV C (mV)", "ΔV1 total (mV)", "P RSE (W)"], rows))
    c = CAPS[ESCOLHA]; esr1 = c["ESR"] / N_PAR; c1 = c["C"] * N_PAR
    dv1 = is_pk * esr1 + IO * (1 - d2) * T / c1
    fc = 1 / (2 * math.pi * math.sqrt(L_POS * C_POS))
    w = 2 * math.pi * FS
    zc = complex(ESR_POS, -1 / (w * C_POS)); zl = complex(0.01, w * L_POS)
    att = abs(zc / (zc + zl))
    dv2 = dv1 * att
    print(f"\n## Escolha: **{N_PAR} × {ESCOLHA}** → RSE eq = {esr1*1e3:.1f} mΩ, I ripple = {c['Irip']*N_PAR:.1f} A ≥ {ic_rms:.2f} A, ΔV1 = {dv1*1e3:.0f} mV")
    print(f"## Pós-filtro LC: L = {L_POS*1e6:.1f} µH, C = {C_POS*1e6:.0f} µF (RSE {ESR_POS*1e3:.0f} mΩ) → fc = {fc/1e3:.1f} kHz, atenuação em {FS/1e3:.0f} kHz = {20*math.log10(att):.0f} dB → ΔVo ≈ **{dv2*1e3:.1f} mV** (meta {DVO_PP_MAX*1e3:.0f} mV)")
    print(f"- Indutor do pós-filtro: {L_POS*1e6:.1f} µH, I_DC = {IO} A → toroide de pó de ferro T68-26 (~10 esp. de 20 AWG) ou indutor radial 3,3 µH ≥ 4 A")
    save("saida", dict(escolha=ESCOLHA, n_par=N_PAR, C1=c1, ESR1=esr1, Irip1=c["Irip"] * N_PAR, dv1=dv1, L_pos=L_POS, C_pos=C_POS,
                       ESR_pos=ESR_POS, fc=fc, att_dB=20 * math.log10(att), dv_out=dv2, c_min=c_min, esr_max=esr_max, candidatos=res))

    t = np.linspace(0, 2 * T, 2000); tt = t % T
    ton = d * T; t2 = d2 * T
    isec = np.where((tt >= ton) & (tt < ton + t2), is_pk * (1 - (tt - ton) / t2), 0)
    ic = isec - IO
    v1 = ic * esr1 + np.cumsum(ic) * (t[1] - t[0]) / c1
    v1 -= v1.mean()
    fig, ax = plt.subplots(2, 1, figsize=(9, 5.5), sharex=True)
    ax[0].plot(t * 1e6, isec, label="i_D (A)"); ax[0].plot(t * 1e6, ic, label="i_C1 (A)"); ax[0].legend(); ax[0].grid(alpha=.3)
    ax[1].plot(t * 1e6, v1 * 1e3, label=f"ΔV no banco C1 ({N_PAR}×{c['C']*1e6:.0f} µF, RSE {esr1*1e3:.1f} mΩ)")
    ax[1].axhline(dv2 * 1e3 / 2, color="C3", ls="--", label=f"após LC: ±{dv2*1e3/2:.1f} mV"); ax[1].axhline(-dv2 * 1e3 / 2, color="C3", ls="--")
    ax[1].set_ylabel("mV"); ax[1].set_xlabel("tempo (µs)"); ax[1].legend(); ax[1].grid(alpha=.3)
    fig.suptitle("Ondulação de saída estimada (90 VAC, plena carga)"); fig.tight_layout()
    fig.savefig(ASSETS / "saida_ripple.png", dpi=150)
    print("\nFigura: assets/saida_ripple.png")


if __name__ == "__main__":
    main()
