"""Posicionamento dos componentes na PCI (mm, origem no canto superior esquerdo, y para baixo, rot CCW)
+ verificador de sobreposicao de courtyards (roda em qualquer Python 3 com fp_info.json).

Regioes (Aula 08: fluxo entrada -> saida, controle agrupado, isolacao):
  A entrada/EMI      x 2-40   y 2-60      B bulk/snubber/MOSFET/trafo  x 40-72  y 2-60
  C controle UC3845  x 2-56   y 60-84     D auxiliar/opto/Y            x 56-84  y 60-84
  E secundario       x 96-128 y 2-60      F realimentacao              x 84-128 y 60-84
Barreira de isolacao: fenda em x = 78; zona PGND ate x = 72 (75 no fundo), zona SGND a partir de x = 84 (82,5 no fundo, 96 no topo).
"""
import json
import math
from pathlib import Path

W, H = 140.0, 90.0
SLOT_X = 84.0

POS = {
    # A - entrada
    "J1": (11.0, 13.0, 0), "RV1": (22.0, 7.0, 0), "RT1": (34.0, 14.0, 0), "F1": (6.0, 24.0, 0),
    "CX1": (4.0, 34.0, 0), "R1": (22.0, 31.0, 0), "R2": (32.16, 35.3, 180),
    "L1": (14.0, 48.0, 0), "CX2": (12.0, 56.0, 0), "BR1": (33.5, 42.0, 270),
    # B - bulk, MOSFET, snubber, trafo
    "C1": (48.0, 34.0, 90), "Q1": (48.0, 44.0, 0), "R9": (45.5, 53.4, 0), "R10": (45.5, 58.4, 0),
    "R7": (43.0, 49.9, 90), "D3": (40.0, 49.9, 90), "R8": (37.0, 49.84, 270),
    "R5": (58.0, 6.0, 0), "R6": (58.0, 13.0, 0), "D2": (57.0, 20.0, 0), "C2": (70.5, 21.0, 0),
    "T1": (84.0, 44.0, 0),
    "TP1": (52.0, 14.0, 0), "TP2": (58.0, 40.0, 0), "TP3": (58.0, 46.0, 0), "TP4": (58.0, 30.0, 0),
    # C - controle
    "U1": (14.0, 66.0, 0), "R12": (10.0, 78.0, 0), "C4": (24.0, 78.0, 0), "C7": (32.0, 78.0, 0),
    "R14": (14.0, 62.0, 0), "R11": (30.0, 74.0, 90), "C5": (35.0, 70.0, 0), "C6": (25.5, 70.5, 90),
    "C8": (11.5, 65.5, 180), "C3": (46.0, 73.0, 0), "R3": (62.0, 24.3, 270), "R4": (62.0, 41.3, 270),
    "TP5": (53.0, 68.0, 0), "TP6": (32.0, 82.0, 0), "TP7": (38.5, 63.2, 0), "TP8": (9.0, 71.0, 0), "TP9": (50.0, 82.0, 0),
    # D - auxiliar, opto, Y
    "D4": (60.0, 64.0, 0), "R13": (60.0, 69.0, 0), "CY1": (79.0, 63.4, 0), "U3": (88.0, 72.0, 180),
    # E - secundario
    "R15": (106.0, 12.0, 0), "C9": (120.0, 12.0, 0), "D1": (110.0, 24.0, 0),
    "C10": (110.5, 36.0, 90), "C11": (121.5, 36.0, 90), "C12": (132.5, 36.0, 90),
    "L2": (114.0, 50.0, 0), "C13": (125.0, 50.0, 90), "TP10": (134.0, 50.0, 0), "TP11": (134.0, 56.0, 0),
    # F - realimentacao e saida
    "R19": (96.0, 63.0, 0), "R20": (96.0, 67.0, 0), "U2": (110.0, 70.0, 0), "R16": (118.0, 62.0, 0), "R17": (118.0, 66.0, 0),
    "R18": (118.0, 70.0, 0), "C14": (131.0, 74.0, 0), "J2": (118.0, 78.0, 0),
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
