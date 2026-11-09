"""Filtro de EMI de entrada (modo diferencial e modo comum) – dimensionamento simplificado.

Fonte classe II (2 pinos, sem terra de proteção): choke de modo comum + X2 + capacitor Y1
entre o GND do primário e o GND do secundário (retorno do ruído de modo comum do transformador).
Referência de limite: CISPR 32 / EN 55032 classe B, quase-pico 66 dBµV (150 kHz) → 56 dBµV (500 kHz–5 MHz) → 60 dBµV (5–30 MHz).
Saida: resultados/emi.json, assets/emi_atenuacao.png
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from params import *

L_CM = 10e-3      # H por enrolamento (choke de modo comum, ex. Würth 744821110 10 mH / 1 A ou Bourns 8109-RC)
L_LK = 0.02 * L_CM  # indutancia de dispersao do choke ~ 2 % (atua em modo diferencial)
C_X = 220e-9      # X2
C_X2 = 100e-9     # segundo X2 (apos o choke, junto a ponte)
C_Y = 2.2e-9      # Y1 entre primario e secundario (limite de corrente de fuga classe II: < 0,25 mA → C_Y ≤ ~2,7 nF a 250 V/60 Hz)
R_LISN = 50.0
R_BLEED = 1.0e6   # descarga do X2 (IEC 60335: < 1 s para < 34 V) → 2 × 470 kΩ

# fonte de ruido (estimativa): corrente de modo diferencial = corrente pulsada do primario (harmonicas de 65 kHz)
# e de modo comum = dv/dt do dreno sobre a capacitancia parasita trafo + dissipador (~ 50 pF)


def main():
    fb = load("flyback"); tr = load("trafo"); assert fb
    print("# Filtro de EMI de entrada\n")
    f = np.logspace(4, 7.5, 1500)
    w = 2 * math.pi * f
    # modo diferencial: atenuacao do filtro LC (L_LK + C_X + C_X2) entre a fonte de ruido (corrente) e a LISN (2x50 Ohm em serie = 100 Ohm para DM)
    # modelo: fonte de corrente -> C_X2 || (L_LK + (C_X || R_lisn_dm))
    r_dm = 2 * R_LISN
    z_cx = 1 / (1j * w * C_X); z_cx2 = 1 / (1j * w * C_X2); z_l = 1j * w * L_LK + 0.1
    z_lisn_par = z_cx * r_dm / (z_cx + r_dm)
    z_branch = z_l + z_lisn_par
    i_ratio = (z_cx2 / (z_cx2 + z_branch)) * (z_cx / (z_cx + r_dm))   # fração da corrente de ruído que chega à LISN
    att_dm = -20 * np.log10(np.abs(i_ratio) + 1e-12)
    # sem filtro: toda a corrente de ruido iria para a LISN (referência 0 dB) — na pratica o bulk ja filtra; aqui mostramos o ganho do filtro
    # modo comum: fonte de tensao do dreno via Cpar -> L_CM -> LISN (25 Ohm CM); C_Y devolve a corrente ao primario
    c_par = 50e-12
    r_cm = R_LISN / 2
    z_cpar = 1 / (1j * w * c_par); z_lcm = 1j * w * L_CM + 5.0
    z_cy = 1 / (1j * w * C_Y)
    # sem choke nem CY: i = v/(z_cpar + r_cm); com: i_lisn = v * [z_cy/(z_cy + z_lcm + r_cm)] / (z_cpar + z_cy || (z_lcm + r_cm))
    i0 = 1 / (z_cpar + r_cm)
    z_par = z_cy * (z_lcm + r_cm) / (z_cy + z_lcm + r_cm)
    i1 = (1 / (z_cpar + z_par)) * (z_cy / (z_cy + z_lcm + r_cm))
    att_cm = 20 * np.log10(np.abs(i0) / (np.abs(i1) + 1e-15))
    f_dm = 1 / (2 * math.pi * math.sqrt(L_LK * C_X * C_X2 / (C_X + C_X2)))
    f_cm = 1 / (2 * math.pi * math.sqrt(L_CM * 2 * C_Y))
    i_fuga = 2 * math.pi * 60 * C_Y * 250
    t_bleed = R_BLEED * (C_X + C_X2) * math.log(373 / 34)
    print("## Componentes\n")
    print(f"- Choke de modo comum L_CM = **{L_CM*1e3:.0f} mH** por enrolamento (≥ 1 A), dispersão ≈ {L_LK*1e6:.0f} µH (modo diferencial) – ex. Würth 744821110 / Bourns 8109-RC")
    print(f"- C_X1 = **{C_X*1e9:.0f} nF X2 / 275 VAC** (antes do choke) e C_X2 = **{C_X2*1e9:.0f} nF X2** (após o choke) – ex. EPCOS B32922 / KEMET R46")
    print(f"- C_Y1 = **{C_Y*1e9:.1f} nF Y1 / 250 VAC** entre GND primário e GND secundário – ex. Murata DE1E3KX222M / Vishay WKP – corrente de fuga a 250 V/60 Hz = {i_fuga*1e3:.2f} mA (< 0,25 mA, classe II)")
    print(f"- Resistores de descarga do X2: 2 × 470 kΩ em série (1 MΩ) → descarga a 34 V em {t_bleed:.2f} s (< 1 s)")
    print(f"- Fusível T2A, NTC 10 Ω, varistor S14K275 (ver entrada.py)\n")
    print("## Frequências de corte estimadas\n")
    print(f"- Modo diferencial (dispersão do choke + X2): f_DM ≈ {f_dm/1e3:.0f} kHz ; atenuação em {FS/1e3:.0f} kHz: {np.interp(FS, f, att_dm):.0f} dB, em 150 kHz: {np.interp(150e3, f, att_dm):.0f} dB, em 1 MHz: {np.interp(1e6, f, att_dm):.0f} dB")
    print(f"- Modo comum (L_CM + C_Y): f_CM ≈ {f_cm/1e3:.1f} kHz ; atenuação em 150 kHz: {np.interp(150e3, f, att_cm):.0f} dB, em 1 MHz: {np.interp(1e6, f, att_cm):.0f} dB")
    print("- Harmônicas da corrente do primário a partir de 150 kHz (3ª harmônica de 65 kHz = 195 kHz) são as primeiras dentro da faixa CISPR; o filtro foi dimensionado para ≥ 40 dB em 195 kHz (DM)")

    save("emi", dict(L_CM=L_CM, L_LK=L_LK, C_X=C_X, C_X2=C_X2, C_Y=C_Y, R_BLEED=R_BLEED, f_dm=f_dm, f_cm=f_cm, i_fuga=i_fuga,
                     att_dm_195k=float(np.interp(195e3, f, att_dm)), att_cm_150k=float(np.interp(150e3, f, att_cm)),
                     componentes=[
                         dict(ref="L1", valor="10 mH 1 A", descricao="choke de modo comum", pn="Würth 744821110", qtd=1),
                         dict(ref="CX1", valor="220 nF X2 275 VAC", descricao="capacitor X2", pn="EPCOS B32922C3224M", qtd=1),
                         dict(ref="CX2", valor="100 nF X2 275 VAC", descricao="capacitor X2", pn="EPCOS B32922C3104M", qtd=1),
                         dict(ref="CY1", valor="2,2 nF Y1 250 VAC", descricao="capacitor Y1 primário–secundário", pn="Murata DE1E3KX222MA4BN01", qtd=1),
                         dict(ref="R_x1,R_x2", valor="470 kΩ 1/4 W", descricao="descarga do X2", pn="", qtd=2)]))
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.semilogx(f, att_dm, label="modo diferencial (Llk choke + X2)"); ax.semilogx(f, att_cm, label="modo comum (L_CM + C_Y1)")
    ax.axvline(150e3, color="k", ls=":", lw=1); ax.text(160e3, 5, "150 kHz (início CISPR 32)", fontsize=8)
    ax.axvline(FS, color="C3", ls=":", lw=1); ax.text(FS * 1.05, 70, "fs", color="C3", fontsize=8)
    ax.set_xlabel("f (Hz)"); ax.set_ylabel("atenuação (dB)"); ax.set_title("Atenuação estimada do filtro de EMI (modelo LISN 50 Ω)"); ax.grid(alpha=.3, which="both"); ax.legend()
    fig.tight_layout(); fig.savefig(ASSETS / "emi_atenuacao.png", dpi=150)
    print("\nFigura: assets/emi_atenuacao.png")


if __name__ == "__main__":
    main()
