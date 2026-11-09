"""Diagrama de blocos da fonte (SVG) para o relatorio: assets/diagrama_blocos.svg. Pure Python.
Uso: python diagrama_blocos.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
W, H = 1040, 430
PRIM, SEC = "#e8f1fa", "#e9f7ee"
INK, MUTED, ACC = "#1b1f24", "#5b6470", "#0b5fa5"
els = []


def rect(x, y, w, h, fill, stroke=ACC, r=6, dash=""):
    els.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.4" {dash}/>')


def text(x, y, s, size=13, weight="normal", fill=INK, anchor="middle"):
    els.append(f'<text x="{x}" y="{y}" font-family="Segoe UI, Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{s}</text>')


def box(x, y, w, h, title, lines, fill):
    rect(x, y, w, h, fill)
    text(x + w / 2, y + 20, title, 13.5, "bold", ACC)
    for i, ln in enumerate(lines):
        text(x + w / 2, y + 38 + i * 15, ln, 11.2, fill=MUTED)


def arrow(x1, y1, x2, y2, color=INK, dash=""):
    els.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.8" marker-end="url(#a)" {dash}/>')


# faixa de potencia (y = 60..160)
y, h = 60, 100
blocos = [
    (20, 118, "Rede", ["90–264 V~", "50/60 Hz", "J1 (L, N)"]),
    (150, 140, "Proteções", ["F1 T2A 250 V", "RV1 S14K275", "RT1 NTC 10 Ω"]),
    (302, 150, "Filtro de EMI", ["CX1 220 nF X2", "L1 2 × 10 mH", "CX2 100 nF, CY1 2,2 nF"]),
    (464, 150, "Retificador + bulk", ["BR1 GBU4J", "C1 150 µF / 400 V", "V_bulk 104–370 V"]),
    (626, 160, "Flyback 65 kHz", ["T1 E-30/7 42:7:9", "Q1 STF13N65M2", "grampo RCD 9 kΩ / 22 nF"]),
]
for x, w, t, ln in blocos:
    box(x, y, w, h, t, ln, PRIM)
box(820, y, 200, h, "Saída 12 V / 3 A", ["D1 STPS20H100CT", "3 × 1000 µF + L2 3,3 µH / 470 µF", "J2 (+12 V, 0 V)"], SEC)
xs = [20 + 118, 150 + 140, 302 + 150, 464 + 150, 626 + 160]
nxt = [150, 302, 464, 626, 820]
for a, b in zip(xs, nxt):
    arrow(a + 2, y + h / 2, b - 3, y + h / 2)

# barreira de isolacao
els.append(f'<line x1="800" y1="30" x2="800" y2="{H - 20}" stroke="{ACC}" stroke-width="1.6" stroke-dasharray="7 5"/>')
text(800, 24, "isolação primário / secundário (T1, U3, CY1; 6,4 mm na PCI)", 11, fill=ACC)
text(400, 24, "PRIMÁRIO (referência PGND)", 11.5, "bold", ACC)
text(920, 46, "SECUNDÁRIO (SGND)", 11.5, "bold", "#1a7f37")

# faixa de comando (y = 230..330)
y2, h2 = 230, 100
box(464, y2, 150, h2, "Partida e auxiliar", ["R3/R4 2 × 82 kΩ", "N_aux 9 esp. → 15 V", "D4 UF4004 + R13 100 Ω"], PRIM)
box(626, y2, 160, h2, "UC3845 (modo corrente)", ["R_T 6,04 kΩ / C_T 2,2 nF", "R_sense 2 × 0,68 Ω", "R_g 10 Ω → gate de Q1"], PRIM)
box(820, y2, 200, h2, "Realimentação", ["TL431 (9,53 k / 2,49 k)", "R_z 21,5 kΩ / C_z 270 nF", "PC817 → COMP (hiccup via VCC)"], SEC)
# ligacoes do comando
arrow(614 + 2, y2 + h2 / 2, 626 - 3, y2 + h2 / 2)                       # aux -> VCC
arrow(706, y2 - 2, 706, y + h + 3, ACC)                                  # gate -> flyback
text(716, y2 - 10, "gate", 10.5, fill=ACC, anchor="start")
arrow(539, y2 - 2, 539, y + h + 3, MUTED, 'stroke-dasharray="4 3"')      # bulk -> partida
text(548, y2 - 10, "V_bulk → R_start", 10.5, fill=MUTED, anchor="start")
arrow(706, y2 + h2 + 2, 706, y2 + h2 + 40, MUTED, 'stroke-dasharray="4 3"')
text(716, y2 + h2 + 30, "T1 aux (pinos 4–5)", 10.5, fill=MUTED, anchor="start")
arrow(820 - 3, y2 + h2 / 2, 786 + 2, y2 + h2 / 2, "#1a7f37")            # opto -> COMP
text(803, y2 + h2 / 2 - 8, "opto", 10, fill="#1a7f37")
arrow(920, y + h + 2, 920, y2 - 3, "#1a7f37")                            # Vo -> divisor
text(930, y + h + 40, "V_o → divisor", 10.5, fill="#1a7f37", anchor="start")
text(20, H - 8, "Pontos de medida: TP1 BULK, TP2 DRAIN, TP3 SW (R_sense), TP4 GATE, TP5 VCC, TP6 VREF, TP7 COMP, TP8 CS, TP9 PGND, TP10 VO, TP11 SGND; laços JP1 (I rede) e JP2 (I secundário).", 10.5, fill=MUTED, anchor="start")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       f'<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{INK}"/></marker></defs>'
       f'<rect width="{W}" height="{H}" fill="#fff"/>' + "".join(els) + "</svg>")
(HERE / "assets" / "diagrama_blocos.svg").write_text(svg, encoding="utf-8")
print("ok assets/diagrama_blocos.svg")
