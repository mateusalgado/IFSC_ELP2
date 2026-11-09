"""Componentes associados ao UC3845 (Aula 05 + datasheet TI SLUS223).

- oscilador RT/CT (fsw = fosc/2 no UC3845), tempo morto;
- resistor de sensoriamento de corrente e filtro RC;
- partida (resistor de startup + capacitor de VCC) e alimentacao pelo auxiliar;
- resistor de gate e capacidade de acionamento (driver = totem-pole do CI);
- compensacao de rampa (provisao).
Saida: resultados/uc3845.json
"""
import math
from params import *

# dados do UC3845 (TI, SLUS223)
VCC_ON, VCC_OFF = 8.4, 7.6          # V (7,8-9,0 / 7,0-8,2)
I_START_MAX = 0.5e-3                # A (startup current max)
I_CC_TYP, I_CC_MAX = 11e-3, 17e-3   # A (operating)
V_REF = 5.0
V_CS_TH_MIN, V_CS_TH_TYP = 0.9, 1.0 # V limiar do comparador de corrente
I_DIS = 8.3e-3                      # A corrente de descarga de CT (tipico)
DV_OSC = 1.6                        # V excursao de CT (~1,2 a 2,8 V)
VCC_ZENER = 30.0                    # V (min)
V_OUT_HI = 13.0                     # V nivel alto da saida com VCC = 15 V
I_OUT_PK = 1.0                      # A

C_VCC = 220e-6
R_AUX = 100.0                       # ohm, serie do auxiliar (rev. B: 10 -> 100 ohm para o VCC cair no curto e o CI entrar em hiccup)
CT = 2.2e-9
R_G = 10.0
R_DRV_SRC, R_DRV_SINK = 20.0, 10.0  # ohm, saida do CI (estimado a partir de 1 A de pico)
R_CS_FILT, C_CS_FILT = 330, 100e-12
E96 = [1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.30, 1.33, 1.37, 1.40, 1.43, 1.47, 1.50, 1.54, 1.58, 1.62, 1.65, 1.69, 1.74, 1.78, 1.82, 1.87, 1.91, 1.96, 2.00, 2.05, 2.10, 2.15, 2.21, 2.26, 2.32, 2.37, 2.43, 2.49, 2.55, 2.61, 2.67, 2.74, 2.80, 2.87, 2.94, 3.01, 3.09, 3.16, 3.24, 3.32, 3.40, 3.48, 3.57, 3.65, 3.74, 3.83, 3.92, 4.02, 4.12, 4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23, 5.36, 5.49, 5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65, 6.81, 6.98, 7.15, 7.32, 7.50, 7.68, 7.87, 8.06, 8.25, 8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76]


def e96(x):
    dec = 10 ** math.floor(math.log10(x))
    return min((v * dec for v in E96 + [10.0]), key=lambda v: abs(math.log(v / x)))


def main():
    fb = load("flyback"); tr = load("trafo"); ent = load("entrada"); assert fb and tr and ent
    out = {}
    print("# Componentes associados ao UC3845\n")

    # ---- oscilador ----
    f_osc = 2 * FS
    rt = 1.72 / (f_osc * CT)
    RT = e96(rt)
    f_osc_real = 1.72 / (RT * CT); fsw = f_osc_real / 2
    t_dead = CT * DV_OSC / I_DIS
    d_max_osc = 1 - t_dead * f_osc_real
    print("## Oscilador\n")
    print(f"- UC3845: fsw = fosc/2 → fosc = {f_osc/1e3:.0f} kHz ; fosc ≈ 1,72/(RT·CT) → com CT = {CT*1e9:.1f} nF, RT = {rt/1e3:.2f} kΩ → **RT = {RT/1e3:.2f} kΩ (E96), CT = {CT*1e9:.1f} nF (NP0/C0G)** → fosc = {f_osc_real/1e3:.1f} kHz, **fsw = {fsw/1e3:.1f} kHz**")
    print(f"- Tempo morto do oscilador: CT·ΔV/Idis = {t_dead*1e9:.0f} ns → Dmax do oscilador {d_max_osc*100:.1f} % (o flip-flop limita a 50 %; datasheet 46–50 %)")
    out["oscilador"] = dict(RT=RT, CT=CT, f_osc=f_osc_real, fsw=fsw, t_dead_ns=t_dead * 1e9)

    # ---- sensoriamento de corrente ----
    Ip = fb["Ip_max"]
    i_lim_alvo = 1.25 * Ip                       # limite de corrente ~25 % acima do pico nominal
    rs = V_CS_TH_MIN / i_lim_alvo
    RS = 0.68 / 2
    i_lim_min, i_lim_typ = V_CS_TH_MIN / RS, V_CS_TH_TYP / RS
    p_rs = fb["Ip_rms_max"] ** 2 * RS
    tau = R_CS_FILT * C_CS_FILT
    print("\n## Sensoriamento de corrente (pino ISENSE)\n")
    print(f"- Ip nominal máx = {Ip:.2f} A ; alvo de limitação = 1,25·Ip = {i_lim_alvo:.2f} A → Rs = 0,9 V/{i_lim_alvo:.2f} = {rs:.3f} Ω → **Rs = {RS} Ω** (2 × {2*RS:.2f} Ω / 1 W em paralelo)")
    print(f"- Limite de corrente resultante: {i_lim_min:.2f} A (Vth mín 0,9 V) a {i_lim_typ:.2f} A (típ. 1,0 V) ; potência em Rs = Ip,rms²·Rs = {p_rs:.2f} W")
    print(f"- Filtro RC de borda: R = {R_CS_FILT:.0f} Ω, C = {C_CS_FILT*1e12:.0f} pF → τ = {tau*1e9:.0f} ns (ton mín = {fb['ton_min_ns']:.0f} ns → τ < ton,mín/2 ✓)")
    out["sense"] = dict(RS=RS, i_lim_min=i_lim_min, i_lim_typ=i_lim_typ, P_RS=p_rs, R_filt=R_CS_FILT, C_filt=C_CS_FILT, tau_ns=tau * 1e9)

    # ---- partida e alimentacao ----
    i_cc = I_CC_MAX + 34e-9 * fsw
    R_START = 2 * 82e3
    rows = []
    for vac in VAC_POINTS:
        vb = ent["pontos"][f"{vac:.0f}V_60Hz"]["vbulk_max"]
        i_r = (vb - VCC_ON / 2) / R_START
        i_net = i_r - 0.3e-3
        t_start = C_VCC * VCC_ON / max(i_net, 1e-6)
        p_r = vb ** 2 / R_START
        rows.append([f"{vac:.0f}", fmt(vb, 0), fmt(i_r * 1e3, 2), fmt(i_net * 1e3, 2), fmt(t_start, 1), fmt(p_r, 2)])
    print("\n## Partida (resistor de startup) e alimentação\n")
    print(f"- R_start = **2 × 82 kΩ / 1 W em série** ({R_START/1e3:.0f} kΩ) do bulk ao VCC ; C_VCC = **{C_VCC*1e6:.0f} µF / 35 V** + 100 nF cerâmico junto ao pino")
    print(md_table(["Vac", "Vbulk pico (V)", "I R_start (mA)", "I líquida p/ C (mA)", "t partida (s)", "P R_start (W)"], rows))
    vb_min = ent["vbulk_min"]
    i_min = (vb_min - VCC_ON) / R_START
    t_hold = C_VCC * (VCC_ON - VCC_OFF) / i_cc
    v_aux = tr["Naux"] / tr["Ns"] * (VO + VF_DIODE_OUT) - 0.9
    print(f"- Corrente mínima de startup (vale de 90 VAC): {i_min*1e3:.2f} mA ≥ {I_START_MAX*1e3:.1f} mA (máx. do CI) ✓ ; consumo em operação ≈ {i_cc*1e3:.1f} mA")
    print(f"- Tempo que C_VCC sustenta o CI entre 8,4 e 7,6 V sem o auxiliar: {t_hold*1e3:.1f} ms (o auxiliar deve estabelecer VCC antes disso → soft-start curto)")
    print(f"- Auxiliar: Naux/Ns = {tr['Naux']}/{tr['Ns']} → Vaux ≈ {v_aux:.1f} V (< {VCC_ZENER:.0f} V do zener interno ✓, > {VCC_OFF} V ✓) ; diodo **UF4004** + resistor série **{R_AUX:.0f} Ω** (rev. B: filtra o pico de dispersão para que, com a saída em curto, o auxiliar não sustente o VCC e o CI desligue por UVLO)")
    # ---- protecao de curto por hiccup (rev. B) ----
    i_cc_typ = I_CC_TYP + 34e-9 * fsw
    rows2 = []
    for vac in VAC_POINTS:
        vb = ent["pontos"][f"{vac:.0f}V_60Hz"]["vbulk_max"]
        i_st = (vb - 8.0) / R_START
        t_decay = C_VCC * (v_aux - VCC_OFF) / max(i_cc_typ - i_st, 1e-6)
        t_charge = C_VCC * (VCC_ON - VCC_OFF) / max(i_st - 0.5e-3, 1e-6)
        t_run = C_VCC * (VCC_ON - VCC_OFF) / max(i_cc_typ - i_st, 1e-6)
        duty = t_run / (t_charge + t_run)
        rows2.append([f"{vac:.0f}", fmt(t_decay * 1e3, 0), fmt(t_charge * 1e3, 0), fmt(t_run * 1e3, 1), fmt(100 * duty, 1)])
    print("\n### Curto-circuito na saída: desligamento por UVLO e religamento (hiccup)\n")
    print(f"- Com a saída em curto a tensão do auxiliar cai a ≈ {tr['Naux']/tr['Ns']*0.7:.1f} V e, com R_aux = {R_AUX:.0f} Ω, os picos de dispersão não sustentam o VCC: C_VCC descarrega de {v_aux:.1f} V a {VCC_OFF} V com I_CC − I_start, o CI desliga, R_start recarrega C_VCC até {VCC_ON} V e o CI tenta de novo por t_run")
    print(md_table(["Vac", "t até UVLO (ms)", "t recarga (ms)", "t ligado por tentativa (ms)", "ciclo de trabalho da falha (%)"], rows2))
    out["partida"] = dict(R_start=R_START, C_vcc=C_VCC, R_aux=R_AUX, i_start_min=i_min, t_hold_ms=t_hold * 1e3, V_aux=v_aux, tabela=rows, hiccup=rows2)

    # ---- driver / gate ----
    print("\n## Acionamento do MOSFET (driver)\n")
    print(f"- O UC3845 tem saída totem-pole de ±{I_OUT_PK:.0f} A de pico (tr/tf ≈ 50 ns em 1 nF), suficiente para MOSFETs de até ~100 nC a 65 kHz → **driver = o próprio CI**, sem driver externo (Aula 05: circuito básico não isolado, fonte e MOSFET na mesma referência)")
    print(f"- Rg = **{R_G:.0f} Ω** (série) + diodo 1N4148 antiparalelo com Rg (desliga mais rápido) + 10 kΩ gate–source (mantém bloqueado antes da partida)")
    out["driver"] = dict(R_G=R_G, R_g_off=1.0, R_drv_src=R_DRV_SRC, R_drv_sink=R_DRV_SINK, R_gs=10e3)

    # ---- compensacao de rampa (provisao) ----
    # m2 (down slope do sensor) = Vr/Lp * Rs ; rampa do oscilador ~ dV/dt = DV_OSC*fosc (parte de subida ~ 2/3 do periodo)
    m2 = fb["Vr"] / tr["Lp_real"] * RS
    m_osc = DV_OSC / (1 / f_osc_real * (1 - t_dead * f_osc_real))
    ma_alvo = 0.5 * m2
    r_slope = R_CS_FILT * m_osc / ma_alvo          # divisor R_slope / R_filt sobre a rampa
    print("\n## Compensação de rampa (provisão)\n")
    print(f"- D máx de projeto = {fb['D_max']:.3f} < 0,5 e operação em MCD → **não é obrigatória**. Provisão na PCI: resistor do pino RT/CT ao nó ISENSE (após o filtro)")
    print(f"- Inclinação de descida sensoriada m2 = Vr/Lp·Rs = {m2/1e3:.1f} mV/µs ; rampa do oscilador {m_osc/1e3:.0f} mV/µs → para ma = 0,5·m2: R_slope ≈ {r_slope/1e3:.0f} kΩ (não montar por padrão)")
    out["rampa"] = dict(m2=m2, m_osc=m_osc, R_slope=r_slope)

    # ---- outros ----
    print("\n## Outros\n")
    print("- VREF: 1 µF cerâmico ao GND junto ao pino (≥ 0,1 µF) ; VCC: 100 nF cerâmico + C_VCC ; VFB ao GND (amplificador de erro em saturação alta; o controle é feito pelo optoacoplador no pino COMP com pull-up de 4,7 kΩ ao VREF)")
    out["componentes"] = [
        dict(ref="U1", valor="UC3845", descricao="controlador PWM modo corrente, DIP-8", pn="TI UC3845AN / onsemi UC3845BNG", qtd=1),
        dict(ref="RT", valor=f"{RT/1e3:.2f} kΩ 1 %", descricao="resistor do oscilador", pn="", qtd=1),
        dict(ref="CT", valor=f"{CT*1e9:.1f} nF NP0", descricao="capacitor do oscilador", pn="", qtd=1),
        dict(ref="Rs1,Rs2", valor=f"{2*RS:.2f} Ω 1 W", descricao="sensor de corrente (2 em paralelo)", pn="", qtd=2),
        dict(ref="R_cs", valor=f"{R_CS_FILT:.0f} Ω", descricao="filtro do ISENSE", pn="", qtd=1),
        dict(ref="C_cs", valor=f"{C_CS_FILT*1e12:.0f} pF", descricao="filtro do ISENSE", pn="", qtd=1),
        dict(ref="R_st1,R_st2", valor="82 kΩ 1 W", descricao="startup (série)", pn="", qtd=2),
        dict(ref="C_vcc", valor="220 µF 35 V", descricao="capacitor de VCC", pn="", qtd=1),
        dict(ref="C_vcc2", valor="100 nF 50 V", descricao="desacoplamento VCC", pn="", qtd=1),
        dict(ref="C_ref", valor="1 µF 50 V", descricao="desacoplamento VREF", pn="", qtd=1),
        dict(ref="D_aux", valor="UF4004", descricao="retificador do auxiliar", pn="", qtd=1),
        dict(ref="R_aux", valor=f"{R_AUX:.0f} Ω", descricao="série do auxiliar (hiccup)", pn="", qtd=1),
        dict(ref="Rg", valor="10 Ω", descricao="resistor de gate", pn="", qtd=1),
        dict(ref="D_g", valor="1N4148", descricao="desligamento rápido do gate", pn="", qtd=1),
        dict(ref="R_gs", valor="10 kΩ", descricao="pull-down gate-source", pn="", qtd=1),
        dict(ref="R_pu", valor="4,7 kΩ", descricao="pull-up COMP–VREF", pn="", qtd=1),
    ]
    save("uc3845", out)


if __name__ == "__main__":
    main()
