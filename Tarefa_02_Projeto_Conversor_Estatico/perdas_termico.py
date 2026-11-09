"""Calculo de perdas nos semicondutores e dimensionamento termico - Tarefa 02.

Metodologia: Aula 3 "Metodologia de Projeto aplicada em conversores
estaticos de potencia" (Prof. Joabel Moia) + mesmo metodo/fator termico
adotado na Tarefa 01 (kT = 1,7 para Tj,proj = 125 C), para manter as
duas tarefas comparaveis.

Todos os parametros de datasheet usados estao citados nos comentarios
e nas Referencias do RELATORIO.md.
"""

from calculos_buck import (
    VIN, VOUT, FS, D, DI_L,
    IT_RMS, IT_MED, IT_PICO,
    ID_RMS, ID_MED, ID_PICO,
    IC_RMS, IL_MAX,
)

# ------------------------------------------------------------------
# Hipoteses termicas (identicas a Tarefa 01)
# ------------------------------------------------------------------
TA = 40.0          # C, temperatura ambiente de projeto
TJ_PROJ = 125.0    # C, meta conservadora de juncao
RTHCS = 0.5        # C/W, capsula-dissipador com pasta termica
KT = 1.7           # fator de correcao de RDS(on) em Tj_proj (curva normalizada)
VGS_DRIVE = 10.0   # V, tensao de acionamento do gate


def rthsa_max(p_diss: float, rthjc: float) -> float:
    """R_theta,SA maxima admissivel dada a perda e o RθJC do componente."""
    return (TJ_PROJ - TA) / p_diss - rthjc - RTHCS


# ==================================================================
# 1) TRANSISTORES (100 V, TO-220) — dados de datasheet
# ==================================================================
mosfets = {
    "IRLZ44N (Vishay) - usado na Tarefa 01": dict(
        vds_max=55.0, rds_on_25=22e-3, qg=63e-9, tr=26e-9, tf=11e-9,
        rthjc=1.4, nota="VDS=55V < 2*Vin=72V -> margem de pior caso insuficiente",
    ),
    "IRF540N (Vishay/Infineon, legado planar)": dict(
        vds_max=100.0, rds_on_25=44e-3, qg=71e-9, tr=35e-9, tf=35e-9,
        rthjc=1.15, nota="datasheet Infineon PD-94812 / IRF540NPbF",
    ),
    "IPP039N10N5 (Infineon OptiMOS 5, trench)": dict(
        vds_max=100.0, rds_on_25=3.9e-3, qg=76e-9, tr=10e-9, tf=17e-9,
        rthjc=0.5, nota="datasheet Infineon Rev.2.0 2016-11-22",
    ),
}

print("=" * 70)
print("TRANSISTORES - perdas em Tj_proj = 125 C, VDS(off) = Vin, Ipk = IL_max")
print("=" * 70)
for nome, p in mosfets.items():
    p_cond = p["rds_on_25"] * KT * IT_RMS ** 2
    p_sw = (FS / 2) * (p["tr"] + p["tf"]) * VIN * IL_MAX
    p_g = p["qg"] * VGS_DRIVE * FS
    p_total = p_cond + p_sw + p_g
    print(f"\n{nome}")
    print(f"  {p['nota']}")
    print(f"  P_cond = {p_cond*1000:.1f} mW   P_sw = {p_sw*1000:.1f} mW   P_g = {p_g*1000:.1f} mW")
    print(f"  P_total = {p_total:.3f} W")
    rth_ja_req = (TJ_PROJ - TA) / p_total
    print(f"  RthJA requerido (sem dissipador) = {rth_ja_req:.1f} C/W")
    rsa = rthsa_max(p_total, p["rthjc"])
    print(f"  RthSA_max (com dissipador, RthJC={p['rthjc']}) = {rsa:.1f} C/W")

# ==================================================================
# 2) DIODOS (100 V, TO-220) — dados de datasheet
# ==================================================================
print("\n" + "=" * 70)
print("DIODOS - perdas de conducao (ID_med, ID_rms do freewheeling)")
print("=" * 70)

# MUR860 (ultrarrapido Si) - modelo simples V_F constante (dado de datasheet)
vf_mur860 = 1.2  # V @ 8A, 150 C (pior caso)
qrr_mur860 = 195e-9
p_mur860_cond = vf_mur860 * ID_MED
p_mur860_rr = qrr_mur860 * VIN * FS
p_mur860 = p_mur860_cond + p_mur860_rr
print(f"\nMUR860 (usado na Tarefa 01, ultrarrapido)")
print(f"  P_cond = {p_mur860_cond:.3f} W   P_rr = {p_mur860_rr:.3f} W   Total = {p_mur860:.3f} W")

# MBR20100CT (Schottky, Vishay) - VF tipico 0,65 V @ 10A/25C (unico ponto do datasheet)
vf_mbr = 0.65
p_mbr_single = vf_mbr * ID_MED
rthjc_mbr = 2.0
p_mbr_par = vf_mbr * ID_MED  # V0*I nao muda ao paralelizar (mesmo modelo de 1 ponto)
print(f"\nMBR20100CT (Schottky, usado/escolhido na Tarefa 01)")
print(f"  VF=0,65V (unico ponto de datasheet) -> P_cond = {p_mbr_single:.3f} W")

# STPS20H100C (Schottky, ST) - modelo VF = V0 + Rd*I ajustado a partir de 2 pontos
# Tj = 125 C: (10A, 0.64V) e (20A, 0.73V)  =>  Rd = 9 mOhm ; V0 = 0.55 V
RD_STPS = (0.73 - 0.64) / (20 - 10)
V0_STPS = 0.64 - RD_STPS * 10
p_stps_single = V0_STPS * ID_MED + RD_STPS * ID_RMS ** 2
rthjc_stps = 0.9
# Com os dois anodos internos em paralelo (mesmo truque usado no MBR20100CT da Tarefa 01)
i_leg_med = ID_MED / 2
i_leg_rms = ID_RMS / 2
p_stps_par = 2 * (V0_STPS * i_leg_med + RD_STPS * i_leg_rms ** 2)
rthjc_stps_par = rthjc_stps / 2
print(f"\nSTPS20H100C (Schottky, ST, Tj_max=175C) - modelo VF=V0+Rd*I @125C")
print(f"  V0={V0_STPS:.3f} V, Rd={RD_STPS*1000:.2f} mOhm")
print(f"  Um so terminal:      P_cond = {p_stps_single:.3f} W  (RthJC={rthjc_stps} C/W)")
print(f"  Anodos em paralelo:  P_cond = {p_stps_par:.3f} W  (RthJC_eff={rthjc_stps_par} C/W)")

print("\n--- Termico dos diodos (RthCS = 0,5 C/W, pasta termica) ---")
print(f"MUR860:            RthSA_max = {rthsa_max(p_mur860, 2.0):.2f} C/W")
print(f"MBR20100CT:     RthSA_max = {rthsa_max(p_mbr_single, rthjc_mbr):.2f} C/W")
print(f"STPS20H100C (par): RthSA_max = {rthsa_max(p_stps_par, rthjc_stps_par):.2f} C/W")

# ==================================================================
# 3) CAPACITOR DE SAIDA
# ==================================================================
print("\n" + "=" * 70)
print("CAPACITOR DE SAIDA - Nichicon UPW1E102MHD (1000 uF / 25 V)")
print("=" * 70)
C_ESCOLHIDO = 1000e-6
ESR_ESCOLHIDO = 70e-3   # ohm, typ @ 100 kHz / 20 C (datasheet)

dvo_capacitivo = DI_L / (8 * FS * C_ESCOLHIDO)
dvo_esr = ESR_ESCOLHIDO * DI_L
dvo_total = dvo_capacitivo + dvo_esr
p_rse = ESR_ESCOLHIDO * IC_RMS ** 2
print(f"  dVo (parcela capacitiva) = {dvo_capacitivo*1000:.2f} mV")
print(f"  dVo (parcela da RSE)     = {dvo_esr*1000:.2f} mV")
print(f"  dVo total estimado       = {dvo_total*1000:.2f} mV  ({dvo_total/VOUT*100:.3f}% de Vo)")
print(f"  IC_rms = {IC_RMS:.4f} A  (rating do capacitor: 1,66 A @105C -> folga {1.66/IC_RMS:.1f}x)")
print(f"  P_RSE = {p_rse*1000:.2f} mW (desprezivel, sem necessidade de dissipador)")
