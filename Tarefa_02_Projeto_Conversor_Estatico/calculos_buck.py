"""Calculos eletricos e formas de onda do conversor Buck da Tarefa 02.

Especificacao (aula 3, 17/08/2026):
    Vin = 36 V, Vout = 12 V, Po = 100 W, fs = 50 kHz, L = 100 uH.

Gera:
    - assets/formas_de_onda_buck.png : v_sw, i_L, i_T, i_D, i_C, v_o
    - Impressao no console de todos os esforcos de tensao/corrente
      usados no relatorio (RELATORIO.md).

Mesmo padrao grafico da Tarefa 01 (simulacao_buck.py).
"""

import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Dados de projeto
# ------------------------------------------------------------------
VIN = 36.0
VOUT = 12.0
POUT = 100.0
FS = 50e3
L = 100e-6

D = VOUT / VIN
TS = 1 / FS
TON = D * TS
TOFF = (1 - D) * TS
IO = POUT / VOUT
RLOAD = VOUT ** 2 / POUT

# Ondulacao de corrente no indutor (MCC)
DI_L = (VIN - VOUT) * D * TS / L
IL_MIN = IO - DI_L / 2
IL_MAX = IO + DI_L / 2
IL_RMS = math.sqrt(IO ** 2 + DI_L ** 2 / 12)

# Esforcos no transistor (conduz durante D*Ts)
IT_MED = D * IO
IT_RMS = math.sqrt(D * (IO ** 2 + DI_L ** 2 / 12))
IT_PICO = IL_MAX
VDS_BLOQ = VIN

# Esforcos no diodo (conduz durante (1-D)*Ts)
ID_MED = (1 - D) * IO
ID_RMS = math.sqrt((1 - D) * (IO ** 2 + DI_L ** 2 / 12))
ID_PICO = IL_MAX
VR_BLOQ = VIN

# Corrente eficaz no capacitor (componente CA de i_L, forma triangular)
IC_RMS = DI_L / math.sqrt(12)

# Capacitancia minima e RSE maxima para ondulacao-alvo de saida
DVO_ALVO_PCT = 0.01
DVO_ALVO = DVO_ALVO_PCT * VOUT
C_MIN = DI_L / (8 * FS * DVO_ALVO)
# Criterio da aula 3 (exemplo Boost): RSE_max = k * dVo / dIL, k = 0.2
RSE_MAX = 0.2 * DVO_ALVO / DI_L

# Capacitor de saida escolhido (Nichicon UPW1E102MHD - Secao 9 do relatorio)
C_ESCOLHIDO = 1000e-6
ESR_ESCOLHIDO = 70e-3


def resumo() -> None:
    print(f"D               = {D:.6f}")
    print(f"Ts              = {TS*1e6:.3f} us  (ton={TON*1e6:.3f} us, toff={TOFF*1e6:.3f} us)")
    print(f"Rload           = {RLOAD:.6f} ohm")
    print(f"Io = IL_med     = {IO:.6f} A")
    print(f"delta_iL_pp     = {DI_L:.6f} A")
    print(f"IL_min          = {IL_MIN:.6f} A")
    print(f"IL_max          = {IL_MAX:.6f} A")
    print(f"IL_rms          = {IL_RMS:.6f} A")
    print("--- Transistor ---")
    print(f"IT_med          = {IT_MED:.6f} A")
    print(f"IT_rms          = {IT_RMS:.6f} A")
    print(f"IT_pico         = {IT_PICO:.6f} A")
    print(f"VDS_bloqueio    = {VDS_BLOQ:.6f} V")
    print("--- Diodo ---")
    print(f"ID_med          = {ID_MED:.6f} A")
    print(f"ID_rms          = {ID_RMS:.6f} A")
    print(f"ID_pico         = {ID_PICO:.6f} A")
    print(f"VR_bloqueio     = {VR_BLOQ:.6f} V")
    print("--- Capacitor ---")
    print(f"IC_rms          = {IC_RMS:.6f} A")
    print(f"C_min (dVo={DVO_ALVO_PCT*100:.0f}%) = {C_MIN*1e6:.3f} uF")
    print(f"RSE_max (crit. aula) = {RSE_MAX*1e3:.3f} mOhm")


def plot_waveforms() -> None:
    assets = Path(__file__).parent / "assets"
    assets.mkdir(exist_ok=True)

    # Tres periodos em regime permanente, 1200 pontos por periodo.
    t = np.linspace(0, 3 * TS, 3601)
    tau = np.mod(t, TS)
    switch_on = tau < TON

    il = np.where(
        switch_on,
        IL_MIN + (VIN - VOUT) / L * tau,
        IL_MAX - VOUT / L * (tau - TON),
    )
    it = np.where(switch_on, il, 0.0)
    idiode = np.where(switch_on, 0.0, il)
    vsw = np.where(switch_on, VIN, 0.0)
    ic = il - IO

    # Tensao de saida real: parcela capacitiva (integral de i_C/C) + parcela
    # resistiva (ESR * i_C), evidenciando visualmente por que a RSE domina
    # a ondulacao (Secao 9 do relatorio).
    dt = t[1] - t[0]
    vc_cap = np.cumsum(ic / C_ESCOLHIDO) * dt
    vc_cap -= np.mean(vc_cap)
    vc_esr = ESR_ESCOLHIDO * ic
    vo = VOUT + vc_cap + vc_esr

    fig, axes = plt.subplots(6, 1, figsize=(10, 12), sharex=True)
    traces = [
        (vsw, r"$v_{sw}$ [V]", "#2563eb"),
        (il, r"$i_L$ [A]", "#059669"),
        (it, r"$i_T$ [A]", "#dc2626"),
        (idiode, r"$i_D$ [A]", "#7c3aed"),
        (ic, r"$i_C$ [A]", "#d97706"),
        (vo, r"$v_o$ [V]", "#0f766e"),
    ]
    for ax, (y, label, color) in zip(axes, traces):
        ax.plot(t * 1e6, y, color=color, linewidth=1.7)
        ax.set_ylabel(label)
        ax.grid(True, alpha=0.25)
    axes[-1].set_xlabel(r"Tempo [$\mu s$]")
    fig.suptitle("Buck ideal em regime permanente - fs = 50 kHz - tres periodos de comutacao")
    fig.tight_layout()

    out_path = assets / "formas_de_onda_buck.png"
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)

    print(f"\nFigura salva em {out_path}")
    print(f"dVo_pp (simulado, com C={C_ESCOLHIDO*1e6:.0f}uF, ESR={ESR_ESCOLHIDO*1000:.0f}mOhm) "
          f"= {(vo.max()-vo.min())*1000:.2f} mV")


if __name__ == "__main__":
    resumo()
    plot_waveforms()
