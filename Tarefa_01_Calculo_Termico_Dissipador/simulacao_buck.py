"""Simulacao numerica ideal do conversor Buck da Tarefa 01.

Gera as formas de onda em regime permanente usadas no relatorio.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


VIN = 36.0
VOUT = 12.0
POUT = 100.0
FS = 100e3
L = 100e-6
C = 100e-6
D = VOUT / VIN
TS = 1 / FS
IO = POUT / VOUT
RLOAD = VOUT**2 / POUT
DI = (VIN - VOUT) * D * TS / L


def main() -> None:
    assets = Path(__file__).parent / "assets"
    assets.mkdir(exist_ok=True)

    # Três períodos em regime permanente, com 1200 pontos por período.
    t = np.linspace(0, 3 * TS, 3601)
    tau = np.mod(t, TS)
    ton = D * TS
    il_min = IO - DI / 2
    il_max = IO + DI / 2
    switch_on = tau < ton

    il = np.where(
        switch_on,
        il_min + (VIN - VOUT) / L * tau,
        il_max - VOUT / L * (tau - ton),
    )
    it = np.where(switch_on, il, 0.0)
    diode = np.where(switch_on, 0.0, il)
    vsw = np.where(switch_on, VIN, 0.0)

    # Integração da corrente do capacitor; remove-se o valor médio para obter
    # apenas a ondulação periódica de tensão em torno de 12 V.
    dt = t[1] - t[0]
    vc_ripple = np.cumsum((il - IO) / C) * dt
    vc_ripple -= np.mean(vc_ripple)
    vc = VOUT + vc_ripple

    fig, axes = plt.subplots(5, 1, figsize=(10, 10), sharex=True)
    traces = [
        (vsw, r"$v_{sw}$ [V]", "#2563eb"),
        (il, r"$i_L$ [A]", "#059669"),
        (it, r"$i_T$ [A]", "#dc2626"),
        (diode, r"$i_D$ [A]", "#7c3aed"),
        (vc, r"$v_o$ [V]", "#d97706"),
    ]
    for ax, (y, label, color) in zip(axes, traces):
        ax.plot(t * 1e6, y, color=color, linewidth=1.7)
        ax.set_ylabel(label)
        ax.grid(True, alpha=0.25)
    axes[-1].set_xlabel("Tempo [µs]")
    fig.suptitle("Buck ideal em regime permanente - três períodos de comutação")
    fig.tight_layout()
    fig.savefig(assets / "formas_de_onda_buck.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    print(f"D={D:.6f}")
    print(f"Rload={RLOAD:.6f} ohm")
    print(f"Io={IO:.6f} A")
    print(f"delta_iL_pp={DI:.6f} A")
    print(f"iL_min={il_min:.6f} A")
    print(f"iL_max={il_max:.6f} A")
    print(f"delta_vo_pp_sim={(vc.max()-vc.min()):.6f} V")


if __name__ == "__main__":
    main()
