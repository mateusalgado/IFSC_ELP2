"""Posicionamento dos componentes na PCI (mm, origem no canto superior esquerdo, y para baixo, rot CCW)
+ verificador de sobreposicao de courtyards (roda em qualquer Python 3 com fp_info.json).

Placa B, placement revisto em 05/11/2026 (antes do pedido da PCI; ver ANALISE_PLACEMENT.md):
  - entrada em linha: J1 na borda esquerda (abre para fora) -> F1 (porta-fusivel 5x20) -> JP1 (laco p/ sonda de corrente)
    -> RV1 / RT1 -> R1/R2 -> CX1 encostado nos pinos de entrada de L1 (1 e 3, em cima) -> L1 -> CX2 -> BR1;
  - Q1 deslocado para (55, 48): dreno a 15,7 mm do pino 3 de T1 e clip a 6 mm do corpo de C1 (era 3,5);
    R3/R4, gate (R7/D3/R8), shunt (R9/R10) e TPs reacomodados; C1 em x = 47;
  - JP2 (laco p/ sonda de corrente do secundario) entre T1 (9/10) e os anodos de D1;
  - eletroliticos de saida com passo 12 mm (retrabalho).
Regioes (Aula 08: fluxo entrada -> saida, controle agrupado, isolacao):
  A entrada/EMI      x 2-40   y 2-60      B bulk/snubber/MOSFET/trafo  x 40-72  y 2-60
  C controle UC3845  x 2-56   y 60-84     D auxiliar/opto/Y            x 56-84  y 60-84
  E secundario       x 96-138 y 2-60      F realimentacao              x 84-138 y 60-84
Barreira de isolacao: fenda em x = 84; zona PGND ate x = 78 (81 no fundo, junto ao opto/Y), zona SGND a partir de x = 88,5 (102 no topo).
"""
import json
import math
from pathlib import Path

W, H = 140.0, 90.0
SLOT_X = 84.0

POS = {
    # A - entrada (coluna junto a borda esquerda, fluxo de cima para baixo)
    "J1": (7.0, 16.0, 270), "F1": (12.0, 7.0, 0), "JP1": (30.0, 14.0, 0), "RV1": (16.5, 14.0, 0), "RT1": (17.0, 20.1, 0),
    "R1": (28.0, 17.2, 0), "R2": (24.0, 24.5, 0), "CX1": (16.0, 33.5, 0),
    "L1": (21.0, 41.0, 270), "CX2": (12.0, 59.6, 0), "BR1": (33.5, 42.0, 270),
    # B - bulk, MOSFET, snubber, trafo
    "C1": (47.0, 32.5, 90), "Q1": (55.0, 48.0, 0), "R9": (60.0, 54.5, 180), "R10": (60.0, 59.5, 180),
    "R7": (50.0, 50.4, 90), "D3": (47.0, 50.4, 90), "R8": (44.0, 50.3, 270),
    "R5": (58.0, 6.0, 0), "R6": (58.0, 13.0, 0), "D2": (57.0, 17.5, 0), "C2": (70.0, 21.0, 0),
    "R3": (62.0, 24.3, 270), "R4": (65.2, 44.0, 270),
    "T1": (84.0, 44.0, 0),
    "TP1": (52.0, 14.0, 0), "TP2": (65.8, 35.5, 0), "TP3": (56.0, 63.5, 0), "TP4": (58.0, 40.5, 0),
    # C - controle
    "U1": (14.0, 66.0, 0), "R12": (10.0, 78.0, 0), "C4": (23.5, 78.5, 0), "C7": (32.0, 78.0, 0),
    "R14": (14.0, 82.0, 0), "R11": (29.0, 75.3, 90), "C5": (35.0, 70.0, 0), "C6": (25.5, 70.5, 90),
    "C8": (11.5, 65.5, 180), "C3": (10.0, 74.5, 180),
    "TP5": (53.0, 68.0, 0), "TP6": (32.0, 82.0, 0), "TP7": (38.5, 63.2, 0), "TP8": (9.0, 71.0, 0), "TP9": (50.0, 82.0, 0),
    # D - auxiliar, opto, Y
    "D4": (60.0, 64.0, 0), "R13": (60.0, 69.0, 0), "CY1": (79.0, 63.4, 0), "U3": (88.0, 72.0, 180),
    # E - secundario
    "JP2": (98.0, 25.5, 0), "R15": (106.0, 12.0, 0), "C9": (120.0, 12.0, 0), "D1": (110.0, 20.0, 0),
    "C10": (108.0, 36.0, 90), "C11": (120.0, 36.0, 90), "C12": (132.0, 36.0, 90),
    "L2": (114.0, 50.0, 0), "C13": (125.0, 50.0, 90), "TP10": (134.0, 50.0, 0), "TP11": (134.0, 56.0, 0),
    # F - realimentacao e saida
    "R19": (96.0, 63.0, 0), "R20": (96.0, 67.0, 0), "U2": (110.0, 70.0, 0), "R16": (114.0, 62.0, 0), "R17": (114.0, 65.4, 0),
    "R18": (118.0, 74.8, 0), "C14": (118.0, 78.0, 0), "J2": (132.0, 70.0, 90),
    # furos
    "H1": (4.0, 4.0, 0), "H2": (136.0, 4.0, 0), "H3": (4.0, 86.0, 0), "H4": (136.0, 86.0, 0),
}


def bbox(fp, x, y, rot, info):
    f = info[fp]
    cx0, cy0, cw, ch = f["cx0"], f["cy0"], f["cw"], f["ch"]
    corners = [(cx0, cy0), (cx0 + cw, cy0), (cx0, cy0 + ch), (cx0 + cw, cy0 + ch)]
    th = math.radians(rot)
    pts = [(x + px * math.cos(th) + py * math.sin(th), y - px * math.sin(th) + py * math.cos(th)) for px, py in corners]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def pad_abs(fp, x, y, rot, info):
    th = math.radians(rot)
    out = {}
    for p in info[fp]["pads"]:
        px, py = p["x"], p["y"]
        out[p["num"]] = (round(x + px * math.cos(th) + py * math.sin(th), 3), round(y - px * math.sin(th) + py * math.cos(th), 3))
    return out


def checa(comps, info, margem=0.0):
    boxes = {}
    for ref, fp in comps.items():
        if ref not in POS or fp not in info:
            continue
        boxes[ref] = bbox(fp, *POS[ref], info)
    probs = []
    refs = sorted(boxes)
    for i, a in enumerate(refs):
        ax0, ay0, ax1, ay1 = boxes[a]
        if ax0 < 0 or ay0 < 0 or ax1 > W or ay1 > H:
            probs.append(f"{a} fora da placa {boxes[a]}")
        for b in refs[i + 1:]:
            bx0, by0, bx1, by1 = boxes[b]
            if ax0 < bx1 + margem and bx0 < ax1 + margem and ay0 < by1 + margem and by0 < ay1 + margem:
                ox = min(ax1, bx1) - max(ax0, bx0); oy = min(ay1, by1) - max(ay0, by0)
                probs.append(f"{a} x {b}: sobreposicao {ox:.2f} x {oy:.2f} mm")
    return probs, boxes


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    info = json.loads((here / "fp_info.json").read_text(encoding="utf-8"))
    comps = {c["ref"]: c["footprint"] for c in json.loads((here / "netlist_componentes.json").read_text(encoding="utf-8"))}
    comps.update({f"TP{i}": "TestPoint:TestPoint_THTPad_D2.0mm_Drill1.0mm" for i in range(1, 12)})
    comps.update({f"H{i}": "MountingHole:MountingHole_3.2mm_M3" for i in range(1, 5)})
    faltam = [r for r in comps if r not in POS]
    print("sem posicao:", faltam)
    probs, boxes = checa(comps, info, margem=0.0)
    print("problemas:", len(probs))
    for p in probs:
        print("  ", p)
