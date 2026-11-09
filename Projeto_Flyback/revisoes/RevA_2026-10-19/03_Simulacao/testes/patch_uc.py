"""Substitui o subcircuito do UC3845 por um modelo em nivel superior (nos uc_*) em gera_netlist.py."""
from pathlib import Path
import re

p = Path(__file__).resolve().parent.parent / "gera_netlist.py"
s = p.read_text(encoding="utf-8")

novo = '''def uc3845_sub():
    """UC3845 comportamental em nivel superior (nos uc_*): pinos externos comp, isns, vcc, drv, vref"""
    t_osc = 1 / F_OSC
    return f"""
* ---- UC3845 comportamental (nos uc_*) ----
* UVLO com histerese: liga em 8,4 V, desliga em 7,6 V (porta 7 do dispositivo A = saida verdadeira)
A_uvlo vcc 0 0 0 0 0 uc_on 0 SCHMITT vt=8.0 vh=0.4 vhigh=1 vlow=0 trise=10n tfall=10n
* consumo: 0,3 mA antes da partida, 11 mA em operacao; zener de 34 V
B_icc vcc 0 I=if(V(uc_on)>0.5, 11m, 0.3m)
D_z vcc 0 DZ34
* referencia 5 V quando ligado
B_ref vref 0 V=if(V(uc_on)>0.5, 5, 0)
R_ref vref 0 1Meg
* oscilador: pulso de descarga (tempo morto) a fosc; onda de meio periodo a fsw = fosc/2 -> Dmax < 50 %
V_clk uc_clk 0 PULSE(0 1 {t_osc*0.5:.4e} 5n 5n {T_DEAD:.4e} {t_osc:.6e})
V_half uc_half 0 PULSE(0 1 {t_osc*0.5 + T_DEAD + 10e-9:.4e} 5n 5n {t_osc - 20e-9:.6e} {2*t_osc:.6e})
* limiar do comparador de corrente: (COMP - 1,4)/3 limitado a [0, 1] V
B_th uc_th 0 V=limit((V(comp)-1.4)/3, 0, 1.0)
B_cmp uc_rst 0 V=if(V(isns) > V(uc_th), 1, 0)
* latch PWM: set no pulso de clock (saida bloqueada durante o clock), reset pelo comparador
A_latch uc_clk uc_rst 0 0 0 0 uc_ql 0 SRFLOP
B_drv uc_drv 0 V=if(V(uc_on)>0.5 & V(uc_ql)>0.5 & V(uc_half)>0.5 & V(uc_clk)<0.5, 1, 0)
* driver totem-pole: alto = VCC - 1,5 V, resistencia de saida ~10 ohm
B_out uc_outi 0 V=if(V(uc_drv)>0.5, V(vcc)-1.5, 0)
R_out uc_outi drv 10
"""
'''
s = re.sub(r'def uc3845_sub\(\):.*?\n"""\n', novo, s, count=1, flags=re.S)
s = s.replace("X_uc comp isns vcc drv 0 vref UC3845B\n", "")
p.write_text(s, encoding="utf-8")
print("patched", "uc_on" in s, "X_uc" not in s)
