"""Grampeador RCD do MOSFET (Aula 07) + RC de amortecimento no diodo de saida.

Energia da indutancia de dispersao a cada ciclo: E = 1/2 Llk Ip^2.
Com a tensao de grampo Vc (acima do bulk) a potencia no snubber e
    P = 1/2 Llk Ip^2 fs * Vc/(Vc - Vr)
porque, enquanto o diodo do snubber conduz, o primario continua
entregando energia ao capacitor (Vr refletida). Saida: resultados/snubber.json
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from params import *

K_CLAMP = 1.8            # Vc = 1,8 Vr (compromisso perda x tensao no MOSFET, ver figura)
DV_C = 0.10              # ondulacao permitida no capacitor do grampo (10 %)
LLK_FRACS = (0.01, 0.02, 0.03)
E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]


def e24(x):
    dec = 10 ** math.floor(math.log10(x))
    return min((v * dec for v in E24 + [10.0]), key=lambda v: abs(math.log(v / x)))


def rcd(Llk, Ip, Vr, Vb_max, k=K_CLAMP):
    Vc = k * Vr
    E = 0.5 * Llk * Ip ** 2
    P = E * FS * Vc / (Vc - Vr)
    R = Vc ** 2 / P
    C = Vc / (DV_C * Vc * R * FS)       # C >= 1/(dVc/Vc * R * fs)
    t_clamp = Llk * Ip / (Vc - Vr)       # tempo de condução do diodo do snubber
    Vds = Vb_max + Vc
    return dict(Llk=Llk, Vc=Vc, E_uJ=E * 1e6, P=P, R=R, C=C, t_clamp_ns=t_clamp * 1e9, Vds_max=Vds)


def main():
    fb = load("flyback"); tr = load("trafo"); assert fb and tr
    Lp, Ip, Vr, Vb_max = tr["Lp_real"], fb["Ip_max"], fb["Vr"], fb["vbulk_max"]
    print("# Snubber RCD do MOSFET\n")
    print(f"Lp = {Lp*1e6:.0f} µH, Ip = {Ip:.2f} A, Vr = {Vr:.1f} V, Vbulk máx = {Vb_max:.0f} V, fs = {FS/1e3:.0f} kHz, Vc = {K_CLAMP}·Vr = {K_CLAMP*Vr:.0f} V\n")
    rows = []; res = {}
    for f in LLK_FRACS:
        r = rcd(f * Lp, Ip, Vr, Vb_max)
        res[f"{int(f*100)}%"] = r
        rows.append([f"{f*100:.0f} % ({f*Lp*1e6:.1f} µH)", fmt(r["E_uJ"], 1), fmt(r["P"], 2), fmt(r["R"] / 1e3, 1), fmt(r["C"] * 1e9, 1), fmt(r["t_clamp_ns"], 0), fmt(r["Vds_max"], 0)])
    print(md_table(["Llk", "E/ciclo (µJ)", "P snubber (W)", "R (kΩ)", "C mín (nF)", "t grampo (ns)", "Vds máx (V)"], rows))

    # dimensionamento: projeta para 2 % (tipico de enrolamento sanduiche) e verifica 3 %
    proj = res["2%"]; pior = res["3%"]
    R = e24(proj["R"]); C = next(v for v in (10e-9, 15e-9, 22e-9, 33e-9, 47e-9, 68e-9) if v >= proj["C"])
    # com R e C escolhidos, recalcula a tensao de grampo real para Llk 2 % e 3 % (equilibrio de energia)
    def vc_real(Llk, R):
        # resolve E*fs*Vc/(Vc-Vr) = Vc^2/R  ->  Vc^2 - E fs R Vc - ... : Vc (Vc - Vr) = E fs R
        a = 0.5 * Llk * Ip ** 2 * FS * R
        return (Vr + math.sqrt(Vr ** 2 + 4 * a)) / 2
    vc2, vc3 = vc_real(0.02 * Lp, R), vc_real(0.03 * Lp, R)
    P2, P3 = vc2 ** 2 / R, vc3 ** 2 / R
    print(f"\n## Componentes escolhidos (projeto para Llk = 2 %, verificação a 3 %)\n")
    print(f"- R = **{R/1e3:.0f} kΩ**, potência dissipada {P2:.2f} W (2 %) a {P3:.2f} W (3 %) → 2 resistores de {2*R/1e3:.0f} kΩ / 2 W em paralelo (ou 1 × {R/1e3:.0f} kΩ / 3 W) ; C = **{C*1e9:.0f} nF / 630 V** (poliéster ou cerâmico) ; diodo **UF4007** (1 A, 1000 V, trr 75 ns) ou **MUR160**")
    print(f"- Tensão de grampo real: {vc2:.0f} V (Llk 2 %) / {vc3:.0f} V (Llk 3 %) → Vds máx = {Vb_max+vc2:.0f} / {Vb_max+vc3:.0f} V (classe 650 V: {100*(Vb_max+vc3)/650:.0f} % no pior caso)")
    print(f"- Pico de corrente no diodo do snubber = Ip = {Ip:.2f} A ; condução ≈ {proj['t_clamp_ns']:.0f} ns por ciclo")
    print("- Alternativa: TVS P6KE180A (Vbr 171–189 V, Vclamp ≈ 246 V @ 24 A) em série com UF4007 → Vds máx ≈ 370 + 246 = 616 V (95 %): **não adotada** (margem insuficiente a 264 VAC)")

    # RC no diodo de saida (amortece ringing de Llk_sec com a capacitancia do Schottky)
    Cj = 400e-12           # STPS20H100CT, ~400 pF @ 10 V por perna x2 -> estimativa
    Llk_sec = 0.02 * Lp / tr["n_real"] ** 2
    f_ring = 1 / (2 * math.pi * math.sqrt(Llk_sec * 2 * Cj))
    Rd = math.sqrt(Llk_sec / (2 * Cj)); Cd = 3 * 2 * Cj
    Pd = Cd * (VO + Vb_max / tr["n_real"]) ** 2 * FS
    print(f"\n## RC de amortecimento no diodo de saída\n")
    print(f"- Llk refletida ao secundário ≈ {Llk_sec*1e9:.0f} nH ; Cj ≈ {2*Cj*1e12:.0f} pF → f ring ≈ {f_ring/1e6:.1f} MHz ; R = √(L/C) ≈ {Rd:.1f} Ω → **{e24(Rd):.0f} Ω** ; C ≈ 3·Cj → **{e24(Cd)*1e9:.1f} nF / 100 V** ; P ≈ C·V²·fs = {Pd:.2f} W → resistor 1/2 W")

    save("snubber", dict(K_CLAMP=K_CLAMP, R=R, C=C, Vc_2pct=vc2, Vc_3pct=vc3, P_2pct=P2, P_3pct=P3, Vds_max_3pct=Vb_max + vc3,
                         diodo="UF4007", tabela=res, rc_diodo=dict(R=e24(Rd), C=e24(Cd), P=Pd),
                         componentes=[
                             dict(ref="R_sn1,R_sn2", valor=f"{2*R/1e3:.0f} kΩ 2 W", descricao="resistor do grampo RCD (2 em paralelo)", pn="Vishay PR02 / Yageo FKN2WSJR", qtd=2),
                             dict(ref="C_sn", valor=f"{C*1e9:.0f} nF 630 V", descricao="capacitor do grampo RCD", pn="EPCOS B32521 / KEMET R82", qtd=1),
                             dict(ref="D_sn", valor="UF4007", descricao="diodo ultrarrápido do grampo", pn="Vishay UF4007-E3/54", qtd=1),
                             dict(ref="R_d", valor=f"{e24(Rd):.0f} Ω 1/2 W", descricao="RC de amortecimento do diodo de saída", pn="", qtd=1),
                             dict(ref="C_d", valor=f"{e24(Cd)*1e9:.1f} nF 100 V", descricao="RC de amortecimento do diodo de saída", pn="", qtd=1)]))

    # figura: P e Vds vs K_CLAMP para Llk 2 %
    ks = np.linspace(1.2, 2.5, 60)
    Ps = [rcd(0.02 * Lp, Ip, Vr, Vb_max, k)["P"] for k in ks]
    Vs = [rcd(0.02 * Lp, Ip, Vr, Vb_max, k)["Vds_max"] for k in ks]
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(ks, Ps, "C0", label="P snubber (W), Llk = 2 %"); ax.set_xlabel("Vc / Vr"); ax.set_ylabel("P (W)", color="C0"); ax.grid(alpha=.3)
    ax2 = ax.twinx(); ax2.plot(ks, Vs, "C3", label="Vds máx (V)"); ax2.axhline(0.8 * 650, color="C3", ls="--", lw=1); ax2.set_ylabel("Vds máx (V)", color="C3")
    ax.axvline(K_CLAMP, color="k", ls=":"); ax.set_title("Compromisso do grampo RCD: perda × tensão no MOSFET")
    fig.tight_layout(); fig.savefig(ASSETS / "snubber_compromisso.png", dpi=150)
    print("\nFigura: assets/snubber_compromisso.png")


if __name__ == "__main__":
    main()
