"""Gera netlists LTspice da fonte flyback 12 V / 3 A com UC3845 a partir dos resultados de 02_Calculos.

Modelo:
  - rede senoidal + fusivel/NTC (R serie) + dispersao do choke (DM) + X2 + ponte + bulk;
  - transformador: Lp, Ls, Laux acoplados (K -> Llk = (1-K^2) Lp);
  - MOSFET VDMOS parametrizado pelo datasheet (STP13N65M2), diodos com modelos SPICE;
  - UC3845 comportamental: UVLO com histerese, oscilador (clock) + flip-flop toggle (fsw = fosc/2,
    Dmax < 50 %), latch PWM (set no clock, reset pelo comparador de corrente), limiar (COMP-1,4)/3
    limitado a 1 V, driver totem-pole, VREF 5 V, consumo;
  - realimentacao: divisor + TL431 (transcondutancia ideal) + PC817 (CTR) + pull-up no COMP.
Casos: regime (VAC x carga), partida, degrau de carga, curto, snubber on/off.
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "02_Calculos" / "resultados"
NET = HERE / "netlists"
NET.mkdir(exist_ok=True)


def j(name):
    return json.loads((RES / f"{name}.json").read_text(encoding="utf-8"))


ent, fb, tr, sd, sn, uc, sc, cp, em = (j(n) for n in ("entrada", "flyback", "trafo", "saida", "snubber", "uc3845", "semicondutores", "compensador", "emi"))

Lp = tr["Lp_real"]; n = tr["n_real"]; na = tr["Naux"] / tr["Np"]
Ls = Lp / n ** 2; La = Lp * na ** 2
K_LLK = 0.02                                   # Llk/Lp alvo
K = math.sqrt(1 - K_LLK)
RS = uc["sense"]["RS"]
RT, CT = uc["oscilador"]["RT"], uc["oscilador"]["CT"]
F_OSC = uc["oscilador"]["f_osc"]
T_DEAD = uc["oscilador"]["t_dead_ns"] * 1e-9
R_START = uc["partida"]["R_start"]; C_VCC = uc["partida"]["C_vcc"]; R_AUX = uc["partida"].get("R_aux", 10.0)
RG = uc["driver"]["R_G"]
R_SN, C_SN = sn["R"], sn["C"]
C1, ESR1 = sd["C1"], sd["ESR1"]; L_POS, C_POS, ESR_POS = sd["L_pos"], sd["C_pos"], sd["ESR_pos"]
RA, RB, RLED, RBIAS, RZ, CZ, RPU, CPC, CTR = cp["Ra"], cp["Rb"], cp["Rled"], cp["R_bias"], cp["Rz"], cp["Cz"], cp["Rpu"], cp["Cp"], cp["CTR"]
C_BULK = ent["C"]; R_SERIE = ent["R_SERIE"]
RC_D = sn["rc_diodo"]
VO = 12.0; PO = 36.0

MODELOS = f"""
* ---- modelos ----
.model STP13N65M2 VDMOS(Rg=6.5 Vto=3.5 Kp=6 Lambda=0.001 Rd=0.30 Rs=0.01 Cgdmax=150p Cgdmin=15p a=0.5 Cgs=560p Cjo=400p m=0.6 Vj=0.8 Is=1e-12 n=1.2 Rds=2e7 mtriode=1.2 ksubthres=0.1)
.model STPS20H100 D(Is=2e-8 n=1.05 Rs=0.0045 Cjo=1.2n m=0.5 Vj=0.6 bv=100 Ibv=1u)
.model DBR D(Is=1e-9 n=1.5 Rs=0.03 bv=600 Cjo=50p tt=1u)
.model UF4007 D(Is=1e-9 n=1.6 Rs=0.05 Cjo=20p tt=50n bv=1000)
.model UF4004 D(Is=1e-9 n=1.6 Rs=0.08 Cjo=15p tt=50n bv=400)
.model D1N4148 D(Is=2.5n n=1.75 Rs=0.5 Cjo=4p tt=10n bv=100)
.model DLED D(Is=1e-15 n=1.8 Rs=1)
.model DZ34 D(Is=1e-12 bv=34 Ibv=1m)
.model DIDEAL D(Is=1e-14 n=1 Rs=0.1 Cjo=10p)
"""


def uc3845_sub():
    """UC3845 comportamental em nivel superior (nos uc_*): pinos externos comp, isns, vcc, drv, vref"""
    t_osc = 1 / F_OSC
    return f"""
* ---- UC3845 comportamental (nos uc_*) ----
* UVLO com histerese: liga em 8,4 V, desliga em 7,6 V (porta 7 do dispositivo A = saida verdadeira)
A_uvlo vcc 0 0 0 0 0 uc_on 0 SCHMITT vt=8.2 vh=0.3 vhigh=1 vlow=0 trise=10n tfall=10n
* consumo: 0,3 mA antes da partida, 11 mA em operacao; zener de 34 V
B_icc vcc 0 I=if(V(uc_on)>0.5, 11m, 0.5m)
D_z 0 vcc DZ34
* referencia 5 V quando ligado
B_ref vref 0 V=if(V(uc_on)>0.5, 5, 0)
R_ref vref 0 1Meg
* oscilador: pulso de descarga (tempo morto) a fosc; onda de meio periodo a fsw = fosc/2 -> Dmax < 50 %
V_clk uc_clk 0 PULSE(0 1 {t_osc*0.5:.4e} 5n 5n {T_DEAD:.4e} {t_osc:.6e})
V_half uc_half 0 PULSE(0 1 {t_osc*0.5 + T_DEAD + 10e-9:.4e} 5n 5n {t_osc - 20e-9:.6e} {2*t_osc:.6e})
* limiar do comparador de corrente: (COMP - 1,4)/3 limitado a [0, 1] V
B_th uc_th 0 V=limit((V(comp)-1.4)/3, 0, 1.0)
B_cmp uc_cmp 0 V=0.5+0.5*tanh((V(isns)-V(uc_th)-0.01)*2000)
R_cmp uc_cmp uc_rst 1k
C_cmp uc_rst 0 100p
* latch PWM: set no pulso de clock (saida bloqueada durante o clock), reset pelo comparador
A_latch uc_clk uc_rst 0 0 0 0 uc_ql 0 SRFLOP
B_drv uc_drv 0 V=if(V(uc_on)>0.5 & V(uc_ql)>0.5 & V(uc_half)>0.5 & V(uc_clk)<0.5, 1, 0)
* driver totem-pole: alto = VCC - 1,5 V, resistencia de saida ~10 ohm
B_out uc_outi 0 V=if(V(uc_drv)>0.5, V(vcc)-1.5, 0)
R_out uc_outi drv 10
"""


def netlist(nome, vac=220.0, fline=60.0, carga=1.0, tstop=40e-3, startup=False, snubber=True,
            step_load=None, short=None, llk=K_LLK, meas_from=None, ctr=CTR, cbulk=C_BULK, phase=0, handoff=None, maxstep=100e-9):
    """step_load=(t, carga2) ; short=(t_on, t_off)"""
    k = math.sqrt(1 - llk)
    vpk = vac * math.sqrt(2)
    rload = VO ** 2 / (PO * carga)
    meas_from = tstop - 2 / fline if meas_from is None else meas_from
    # condicoes iniciais para regime: bulk carregado, saida em 12 V, VCC em 15 V
    ic = "" if startup else f".ic V(bulk)={vpk*0.95:.1f} V(bulkc)={vpk*0.95:.1f} V(vout)={VO} V(voutc)={VO} V(vo)={VO} V(voc)={VO} V(vcc)=15 V(vccc)=15 V(comp)=2.5 V(sgnd)=0\n"
    ic_start = ""
    if startup:
        assert handoff, "Gerar a pré-carga e fornecer as condições no cruzamento UVLO"
        ic_start = f".ic V(bulk)={handoff:.7f} V(bulkc)={handoff:.7f} V(vcc)=8.501 V(vccc)=8.501 V(vo)=0 V(vout)=0 V(voutc)=0 V(voc)=0 V(sgnd)=0\n"
    # carga: resistor fixo + degrau opcional (resistor chaveado) + curto opcional
    load = f"Rload vo sgnd {rload:.4f}\n"
    if step_load:
        t2, c2 = step_load
        r2 = VO ** 2 / (PO * (c2 - carga)) if c2 > carga else None
        if r2:
            load += f"Rstep vo nstep {r2:.4f}\nS_step nstep sgnd ctl_step 0 SW\nV_step ctl_step 0 PULSE(0 1 {t2:.4e} 1u 1u 20m 1)\n"
    if short:
        t_on, t_off = short
        load += f"S_short vo sgnd ctl_sh 0 SWSHORT\nV_sh ctl_sh 0 PULSE(0 1 {t_on:.4e} 1u 1u {t_off - t_on:.4e} 1)\n"
    snub = (f"D_sn drain snub UF4007\nC_sn snub bulk {C_SN:.3e}\nR_sn snub bulk {R_SN:.1f}\n" if snubber else "* sem snubber\n")
    nl = f"""* Fonte flyback 12 V / 3 A com UC3845 - caso: {nome}
* VAC = {vac} V, {fline} Hz, carga = {carga*100:.0f} %, Llk = {llk*100:.0f} % de Lp, snubber = {snubber}
.param VPK={vpk:.2f}
* ---- rede, protecoes, EMI (modo diferencial) e retificador ----
V_ac L N SINE(0 {{VPK}} {fline} 0 0 {phase})
R_ntc L L1 {R_SERIE:.2f}
L_dm L1 L2 {em['L_LK']:.3e} Rser=0.390
C_x2 L2 N 100n
C_x1 L1 N {em['C_X']:.3e}
D_br1 L2 bulk DBR
D_br2 N bulk DBR
D_br3 0 L2 DBR
D_br4 0 N DBR
C_bulk bulkc 0 {cbulk:.3e}
R_bulk bulk bulkc 0.8
* ---- transformador (Lp {Lp*1e6:.0f} uH, n = {n:.3f}, Naux/Np = {na:.3f}, K = {k:.5f}) ----
L_p bulk drain {Lp:.4e} Rser={tr['Rp']:.4f}
L_s sgnd secn {Ls:.4e} Rser={tr['Rs']:.4f}
L_a 0 auxn {La:.4e} Rser=0.05
K1 L_p L_s L_a {k:.6f}
* ---- MOSFET, sensor de corrente, gate ----
M1 drain gate sw sw STP13N65M2
R_s1 sw 0 {2*RS:.3f}
R_s2 sw 0 {2*RS:.3f}
R_cs sw isns 330
C_cs isns 0 100p
R_g drv gate {RG:.1f}
D_g gate drv D1N4148
R_gs gate sw 10k
* ---- snubber RCD ----
{snub}* ---- secundario: Schottky, banco de capacitores, pos-filtro LC, carga ----
D_out secn vout STPS20H100
R_d secn nrc {RC_D['R']:.1f}
C_d nrc vout {RC_D['C']:.3e}
C_o1 voutc sgnd {C1:.3e}
R_o1 vout voutc {ESR1:.4f}
L_pos vout vo {L_POS:.3e} Rser=0.01
C_o2 voc sgnd {C_POS:.3e}
R_o2 vo voc {ESR_POS:.3f}
{load}* referencia do secundario (Y1 + resistor de alta impedancia para o solver)
C_y sgnd 0 {em['C_Y']:.3e}
R_sg sgnd 0 10Meg
* ---- realimentacao: divisor, TL431, PC817 ----
R_a vo ref {RA:.1f}
R_b ref sgnd {RB:.1f}
R_z ref nz {RZ:.1f}
C_z nz ka {CZ:.3e}
B_431 ka sgnd I=max(0, 0.5*(V(ref,sgnd)-2.495))
D_431 sgnd ka DIDEAL
R_led vo ledk {RLED:.1f}
D_led ledk ka DLED
R_bias ledk ka {RBIAS:.1f}
G_opto comp 0 VALUE={{{ctr}*I(D_led)}}
D_oc 0 comp DIDEAL
C_pc comp 0 {CPC:.3e}
R_pu vref comp {RPU:.1f}
* ---- alimentacao do CI: startup + auxiliar ----
R_st1 bulk nst {R_START/2:.0f}
R_st2 nst vcc {R_START/2:.0f}
C_vcc vccc 0 {C_VCC:.3e}
R_vcc vcc vccc 0.1
C_vcc2 vcc 0 100n
D_aux auxn nax UF4004
R_aux nax vcc {R_AUX:.0f}
C_ref vref 0 1u
{uc3845_sub()}{MODELOS}
.model SW SW(Ron=1m Roff=1Meg Vt=0.5 Vh=0.1)
.model SWSHORT SW(Ron=10m Roff=1Meg Vt=0.5 Vh=0.1)
{ic}{ic_start}.options reltol=0.005 abstol=1e-8 vntol=1e-5 method=gear itl4=50 gmin=1e-10
.save V(drv) V(l2) I(D_br1) I(D_br2) I(D_br3) I(D_br4) V(vo) V(sgnd) V(vout) V(bulk) V(drain) V(gate) V(sw) V(isns) V(uc_th) V(comp) V(vcc) V(vref) V(l) V(n) V(secn) V(snub) V(ref) V(ka) I(V_ac) I(L_p) I(D_out) I(C_o1) I(C_bulk) I(Rload) I(D_led) Id(M1) I(D_sn) I(L_pos)
.tran 0 {tstop:.4e} 0 {maxstep:.0e}
* ---- medicoes ----
.meas TRAN Vo_avg AVG V(vo,sgnd) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Vo_pp PP V(vo,sgnd) FROM {tstop-4/F_OSC*20:.7e} TO {tstop:.4e}
.meas TRAN Vo_min MIN V(vo,sgnd) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Vo_max MAX V(vo,sgnd) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Vbulk_min MIN V(bulk) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Vbulk_max MAX V(bulk) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Ip_pk MAX I(L_p) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Ip_rms RMS I(L_p) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Is_pk MAX I(D_out) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Is_rms RMS I(D_out) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Is_avg AVG I(D_out) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Ic1_rms RMS I(C_o1) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Vds_max MAX V(drain,sw) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Vd_min MIN V(secn,vout) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Vcc_avg AVG V(vcc) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Vcomp_avg AVG V(comp) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Iin_rms RMS I(V_ac) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Iin_pk MAX -I(V_ac) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Pin AVG -V(L,N)*I(V_ac) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Po AVG V(vo,sgnd)*I(Rload) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Pmos AVG V(drain,sw)*Id(M1) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Pdiode AVG V(secn,vout)*I(D_out) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Psnub AVG V(snub,bulk)*V(snub,bulk)/{R_SN:.1f} FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Pbr AVG V(L2,bulk)*I(D_br1)+V(N,bulk)*I(D_br2)+-V(L2)*I(D_br3)-V(N)*I(D_br4) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Ic_bulk_rms RMS I(C_bulk) FROM {meas_from:.4e} TO {tstop:.4e}
.meas TRAN Vdrv_avg AVG V(drv) FROM {meas_from:.4e} TO {tstop:.4e}
.end
"""
    if not snubber:
        nl = nl.replace(f".meas TRAN Psnub AVG V(snub,bulk)*V(snub,bulk)/{R_SN:.1f}", ".meas TRAN Psnub AVG 0*V(bulk)")
    nl = nl.replace(".end\n", f".meas TRAN Ripple_total PP V(vo,sgnd) FROM {meas_from:.8f} TO {tstop:.8f}\n.end\n")
    if short:
        a, b = short
        janelas = {"aplic": (a, a + 2e-3), "sust": (a + 2e-3, b), "rec": (b, tstop)}
        extra = f".meas TRAN Iq_falha MAX Id(M1) FROM {a} TO {b}\n.meas TRAN Id_falha MAX I(D_out) FROM {a} TO {b}\n.meas TRAN Vds_falha MAX V(drain,sw) FROM {a} TO {b}\n.meas TRAN Vcc_falha MIN V(vcc) FROM {a} TO {b}\n"
        for jn, (t0, t1) in janelas.items():
            extra += (f".meas TRAN Iq_{jn} MAX Id(M1) FROM {t0:.6f} TO {t1:.6f}\n.meas TRAN Ip_{jn} MAX I(L_p) FROM {t0:.6f} TO {t1:.6f}\n"
                      f".meas TRAN Id1_{jn} MAX I(D_out) FROM {t0:.6f} TO {t1:.6f}\n.meas TRAN Id1rms_{jn} RMS I(D_out) FROM {t0:.6f} TO {t1:.6f}\n"
                      f".meas TRAN Vds_{jn} MAX V(drain,sw) FROM {t0:.6f} TO {t1:.6f}\n.meas TRAN Vccmin_{jn} MIN V(vcc) FROM {t0:.6f} TO {t1:.6f}\n"
                      f".meas TRAN Vomax_{jn} MAX V(vo,sgnd) FROM {t0:.6f} TO {t1:.6f}\n.meas TRAN Pd1_{jn} AVG V(secn,vout)*I(D_out) FROM {t0:.6f} TO {t1:.6f}\n")
        nl = nl.replace(".end\n", extra + ".end\n")
    (NET / f"{nome}.net").write_text(nl, encoding="utf-8")
    return NET / f"{nome}.net"


CASOS = {}


def define_casos():
    for vac, fl in ((90, 50), (127, 60), (220, 60), (264, 60)):
        for carga in (0.1, 0.5, 1.0):
            CASOS[f"regime_{vac}V_{int(carga*100)}pct"] = dict(vac=vac, fline=fl, carga=carga, tstop=6 / fl, meas_from=4 / fl)
    CASOS["bulk_min_90V"] = dict(vac=90, fline=50, tstop=0.12, meas_from=0.08, cbulk=120e-6)
    CASOS["partida_90V"] = dict(vac=90, fline=50, carga=1.0, tstop=100e-3, startup=True, meas_from=0)
    CASOS["partida_264V"] = dict(vac=264, fline=60, carga=1.0, tstop=100e-3, startup=True, meas_from=0)
    CASOS["degrau_90V"] = dict(vac=90, fline=50, carga=0.5, tstop=120e-3, step_load=(80e-3, 1.0), meas_from=80e-3)
    CASOS["degrau_264V"] = dict(vac=264, fline=60, carga=0.5, tstop=120e-3, step_load=(80e-3, 1.0), meas_from=80e-3)
    CASOS["curto_220V"] = dict(vac=220, fline=60, carga=1.0, tstop=420e-3, short=(60e-3, 380e-3), meas_from=60e-3, maxstep=200e-9)
    CASOS["sem_snubber_264V"] = dict(vac=264, fline=60, carga=1.0, tstop=25e-3, snubber=False, meas_from=20e-3)
    CASOS["llk3pct_264V"] = dict(vac=264, fline=60, carga=1.0, tstop=25e-3, llk=0.03, meas_from=20e-3)
    CASOS["ctr05_90V"] = dict(vac=90, fline=50, carga=0.5, tstop=120e-3, ctr=0.5, step_load=(80e-3, 1.0), meas_from=80e-3)


define_casos()

if __name__ == "__main__":
    import sys
    sel = sys.argv[1:] or list(CASOS)
    for nome in sel:
        p = netlist(nome, **CASOS[nome])
        print("gerado", p.name)
