"""Estagio de entrada: ponte retificadora + capacitor de bulk + protecoes.

Metodo: simulacao numerica de um retificador de onda completa alimentando
carga de potencia constante (Pin), com resistencia serie (NTC quente + ESR
+ fiacao). Permite obter, para cada tensao de rede e capacitor candidato:
  - Vbulk min/max e ondulacao (120 Hz / 100 Hz);
  - corrente de pico, media e eficaz nos diodos da ponte;
  - corrente eficaz no capacitor de bulk;
  - corrente eficaz de entrada, fator de potencia e THD (Aula 06).
Saidas: resultados/entrada.json, assets/entrada_formas_de_onda.png
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from params import *

R_SERIE = 2.0      # ohm: NTC quente (~1 ohm) + ESR + trilhas/fiacao
C_CANDIDATOS = (68e-6, 82e-6, 100e-6, 120e-6)
C_ESCOLHIDO = 100e-6


def simula(vac, f_line, C, pin=PIN, rs=R_SERIE, ciclos=12, dt=2e-6):
    """retorna dicionario com grandezas do ultimo ciclo de rede"""
    vpk = vac * math.sqrt(2)
    T = 1 / f_line
    n = int(ciclos * T / dt)
    t = np.arange(n) * dt
    vin = vpk * np.sin(2 * math.pi * f_line * t)
    vc = np.empty(n)
    iin = np.zeros(n)
    vc[0] = vpk * 0.9
    for k in range(n - 1):
        va = abs(vin[k]) - 2 * VF_BRIDGE
        if va > vc[k]:
            i = (va - vc[k]) / rs
        else:
            i = 0.0
        iload = pin / max(vc[k], 20.0)
        vc[k + 1] = vc[k] + (i - iload) / C * dt
        iin[k] = i * np.sign(vin[k])
    iin[-1] = iin[-2]
    m = t >= (ciclos - 2) * T           # ultimos 2 ciclos (regime)
    tt, vv, ii, vcc = t[m], vin[m], iin[m], vc[m]
    i_rect = np.abs(ii)
    i_cap = i_rect - pin / vcc
    p_in = np.mean(vv * ii)
    irms = math.sqrt(np.mean(ii ** 2))
    vrms = math.sqrt(np.mean(vv ** 2))
    fp = p_in / (vrms * irms)
    one = tt >= (ciclos - 1) * T
    x = ii[one]
    X = np.abs(np.fft.rfft(x)) / len(x) * 2
    h1 = X[1]
    thd = math.sqrt(np.sum(X[2:40] ** 2)) / h1
    cond = (i_rect > 1e-3).mean() * 180.0  # graus por semiciclo
    return dict(
        vac=vac, f_line=f_line, C=C,
        vbulk_min=float(vcc.min()), vbulk_max=float(vcc.max()),
        ripple=float(vcc.max() - vcc.min()),
        i_pk=float(i_rect.max()), i_rms_in=irms,
        i_diode_avg=float(i_rect.mean() / 2), i_diode_rms=float(math.sqrt(np.mean(i_rect ** 2) / 2)),
        i_cap_rms=float(math.sqrt(np.mean(i_cap ** 2))),
        fp=fp, thd=thd, p_in=p_in, angulo_conducao=float(cond),
        t=tt - tt[0], vin=vv, iin=ii, vc=vcc,
    )


def main():
    print("# Estagio de entrada\n")
    print(f"Pin = Po/eta = {PO:.0f}/{ETA} = {PIN:.2f} W ; Rs = {R_SERIE} ohm\n")

    rows = []
    for C in C_CANDIDATOS:
        r = simula(VAC_MIN, 50.0, C)
        rows.append([si(C, "F"), f"{C*1e6/PO:.2f} µF/W", fmt(r["vbulk_min"], 1), fmt(r["ripple"], 1),
                     fmt(r["i_cap_rms"], 2), fmt(r["fp"], 3), fmt(r["thd"] * 100, 1)])
    print("## Escolha do capacitor de bulk (90 VAC, 50 Hz, plena carga)\n")
    print(md_table(["C", "C/Po", "Vbulk mín (V)", "Ondulação (V)", "I_C,rms (A)", "FP", "THD (%)"], rows))

    res = {}
    rows = []
    for vac in VAC_POINTS:
        for fl in (50.0, 60.0):
            r = simula(vac, fl, C_ESCOLHIDO)
            res[f"{vac:.0f}V_{fl:.0f}Hz"] = {k: v for k, v in r.items() if not isinstance(v, np.ndarray)}
            rows.append([f"{vac:.0f}", f"{fl:.0f}", fmt(r["vbulk_min"], 1), fmt(r["vbulk_max"], 1), fmt(r["ripple"], 1),
                         fmt(r["i_pk"], 2), fmt(r["i_rms_in"], 2), fmt(r["i_diode_avg"], 3), fmt(r["i_diode_rms"], 2),
                         fmt(r["i_cap_rms"], 2), fmt(r["fp"], 3), fmt(r["thd"] * 100, 1), fmt(r["angulo_conducao"], 0)])
    print(f"\n## Retificador + bulk com C = {si(C_ESCOLHIDO,'F')} (plena carga)\n")
    print(md_table(["Vac", "f (Hz)", "Vb mín", "Vb máx", "ΔVb", "I pico (A)", "I in,rms (A)", "I D,med (A)",
                    "I D,rms (A)", "I C,rms (A)", "FP", "THD %", "cond. (°)"], rows))

    pior = res["90V_50Hz"]
    melhor = res["264V_60Hz"]
    i_in_rms_max = pior["i_rms_in"]
    fusivel_calc = i_in_rms_max * 2.5
    vpk_max = VAC_MAX * math.sqrt(2)
    r_ntc_frio = 10.0
    i_inrush = vpk_max / (r_ntc_frio + R_SERIE)
    prot = dict(
        i_in_rms_90V=i_in_rms_max, fusivel_calc_A=fusivel_calc, fusivel_escolhido="T 2 A / 250 V (5x20 mm, ação lenta)",
        ntc="NTC 10 Ω / 2–3 A (ex.: 10D-9 ou 10D-11)", r_ntc_frio=r_ntc_frio, i_inrush_pico_264V=i_inrush,
        i_inrush_sem_ntc=vpk_max / R_SERIE,
        varistor="MOV 275 VAC (ex.: S14K275 / 14D431K), Vclamp ≈ 710 V @ 50 A",
        capacitor_bulk=dict(C=C_ESCOLHIDO, tensao="400 V", temp="105 °C", i_rms_req=pior["i_cap_rms"],
                            sugestao="Nichicon UCY2G101MHD ou Rubycon 400BXW100MEFC16X35 (100 µF/400 V, 105 °C)"),
        ponte=dict(i_med_max=pior["i_diode_avg"], i_rms_max=pior["i_diode_rms"], i_pico_max=pior["i_pk"],
                   vrrm_min=vpk_max * 1.5, sugestao="GBU4J (4 A / 600 V) ou KBP206 (2 A / 600 V)"),
    )
    print("\n## Proteções e componentes de entrada\n")
    print(f"- Corrente eficaz de entrada máxima (90 VAC): {pior['i_rms_in']:.2f} A → fusível 2,5× = {fusivel_calc:.2f} A → **{prot['fusivel_escolhido']}**")
    print(f"- Inrush sem NTC (264 VAC): {prot['i_inrush_sem_ntc']:.0f} A ; com NTC 10 Ω frio: {i_inrush:.1f} A → **{prot['ntc']}**")
    print(f"- Varistor: **{prot['varistor']}**")
    print(f"- Ponte: I_med = {pior['i_diode_avg']:.3f} A, I_rms = {pior['i_diode_rms']:.2f} A, I_pico = {pior['i_pk']:.1f} A, VRRM ≥ {vpk_max*1.5:.0f} V → **{prot['ponte']['sugestao']}**")
    print(f"- Bulk: {si(C_ESCOLHIDO,'F')} / 400 V, I_C,rms = {pior['i_cap_rms']:.2f} A (90 VAC) → **{prot['capacitor_bulk']['sugestao']}**")
    print(f"- Vbulk mín (90 VAC/50 Hz) = {pior['vbulk_min']:.1f} V ; Vbulk máx (264 VAC) = {melhor['vbulk_max']:.1f} V")

    save("entrada", dict(C=C_ESCOLHIDO, R_SERIE=R_SERIE, vbulk_min=pior["vbulk_min"], vbulk_max=melhor["vbulk_max"],
                         pontos=res, protecoes=prot))

    fig, ax = plt.subplots(2, 2, figsize=(11, 6.5))
    for col, (vac, fl) in enumerate(((90.0, 50.0), (220.0, 60.0))):
        r = simula(vac, fl, C_ESCOLHIDO)
        tms = r["t"] * 1e3
        ax[0, col].plot(tms, np.abs(r["vin"]), color="0.6", lw=1, label="|v_in|")
        ax[0, col].plot(tms, r["vc"], color="C0", lw=1.6, label="v_bulk")
        ax[0, col].set_title(f"{vac:.0f} VAC / {fl:.0f} Hz, C = {C_ESCOLHIDO*1e6:.0f} µF")
        ax[0, col].set_ylabel("tensão (V)"); ax[0, col].legend(loc="lower right"); ax[0, col].grid(alpha=.3)
        ax[1, col].plot(tms, r["iin"], color="C3", lw=1.2)
        ax[1, col].set_ylabel("i_in (A)"); ax[1, col].set_xlabel("tempo (ms)"); ax[1, col].grid(alpha=.3)
        ax[1, col].text(0.02, 0.92, f"FP = {r['fp']:.2f}, THD = {r['thd']*100:.0f} %", transform=ax[1, col].transAxes)
    fig.suptitle("Retificador de onda completa com filtro capacitivo – regime permanente, plena carga")
    fig.tight_layout()
    fig.savefig(ASSETS / "entrada_formas_de_onda.png", dpi=150)
    print("\nFigura: assets/entrada_formas_de_onda.png")


if __name__ == "__main__":
    main()
