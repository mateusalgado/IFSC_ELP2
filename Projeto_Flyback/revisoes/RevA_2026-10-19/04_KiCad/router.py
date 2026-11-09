"""Mini-roteador guloso para a PCI (2 camadas, THT).

Para cada rede, liga os pads em ordem de arvore geradora (vizinho mais proximo) com caminhos
retos, em L, em Z ou em U, na camada F.Cu ou B.Cu (ou com uma via no vertice), verificando:
  - isolamento a pads de outras redes (circulos), trilhas ja roteadas de outras redes (mesma camada),
    furos de fixacao, fenda de isolacao e borda da placa;
  - isolamento maior (1,5 mm) para redes de alta tensao (classe HV);
  - barreira primario/secundario: redes do primario ficam em x <= 75,5; do secundario em x >= 80,5.
Saida: rotas.json (trilhas e vias) consumido por gera_pcb.py. Pure Python 3.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from placement import POS, pad_abs, W, H, SLOT_X
from sexp import parse, find, find_all

CLR = 0.3            # isolamento padrao (mm)
CLR_HV = 1.0         # isolamento para redes HV (IPC-2221 B4 + margem)
EDGE = 1.0
HV_NETS = {"/BULK", "/DRAIN", "Net-(D2-K)", "Net-(BR1-Pad2)", "Net-(BR1-Pad3)", "Net-(CX1-Pad1)", "Net-(CX1-Pad2)",
           "Net-(J1-Pin_1)", "Net-(J1-Pin_2)", "Net-(R1-Pad2)", "Net-(R5-Pad2)", "Net-(R3-Pad2)"}
SEC_NETS = {"SGND", "/VO", "Net-(D1-K)", "Net-(T1-S2)", "Net-(U2-REF)", "Net-(C14-Pad2)", "Net-(C9-Pad1)", "/KA", "/LEDA"}
WIDTH = {"/BULK": 1.5, "/DRAIN": 1.0, "/SW": 1.0, "Net-(D2-K)": 1.0, "Net-(BR1-Pad2)": 1.2, "Net-(BR1-Pad3)": 1.2,
         "Net-(CX1-Pad1)": 1.2, "Net-(CX1-Pad2)": 1.2, "Net-(J1-Pin_1)": 1.2, "Net-(J1-Pin_2)": 1.2,
         "Net-(D1-K)": 2.0, "Net-(T1-S2)": 2.0, "Net-(R5-Pad2)": 1.0, "Net-(R3-Pad2)": 1.0, "Net-(R1-Pad2)": 1.0, "/VO": 2.0, "SGND": 2.0, "PGND": 1.0, "/VCC": 0.8, "/AUX": 0.8, "Net-(D4-K)": 0.8}
ZONE_NETS = {"PGND", "SGND"}      # ligadas pela zona da camada inferior; roteia so o laco critico
PRIM_XMAX, SEC_XMIN = 81.5, 86.5
ILHA_Y0 = 60.5          # inicio (y) da ilha de terra de sinal do controle
JOG_MAX = 6.0           # comprimento maximo de um pulo em B.Cu dentro da ilha
VIA_D, VIA_DRILL = 1.0, 0.5
GRID = 0.5


def frange(a, b, step):
    x = a
    while x <= b:
        yield x
        x += step


def seg_pt_dist(a, b, p):
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def seg_seg_dist(a, b, c, d):
    def cross(o, p, q):
        return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])
    def inter(p1, p2, p3, p4):
        d1 = cross(p3, p4, p1); d2 = cross(p3, p4, p2); d3 = cross(p1, p2, p3); d4 = cross(p1, p2, p4)
        if ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0)) and d1 != 0 and d2 != 0 and d3 != 0 and d4 != 0:
            return True
        return False
    if inter(a, b, c, d):
        return 0.0
    return min(seg_pt_dist(a, b, c), seg_pt_dist(a, b, d), seg_pt_dist(c, d, a), seg_pt_dist(c, d, b))


class Router:
    def __init__(self):
        info = json.loads((HERE / "fp_info.json").read_text(encoding="utf-8"))
        doc = parse((HERE / "netlist.net").read_text(encoding="utf-8"))[0]
        comps = {str(find(c, "ref")[1]): str(find(c, "footprint")[1]) for c in find_all(find(doc, "components"), "comp")}
        self.nets = {}
        padnet = {}
        for n in find_all(find(doc, "nets"), "net"):
            name = str(find(n, "name")[1])
            for node in find_all(n, "node"):
                padnet[(str(find(node, "ref")[1]), str(find(node, "pin")[1]))] = name
        self.pads = []   # dict(ref, num, net, x, y, r)
        self.smd_pts = set()
        for ref, fp in comps.items():
            if ref not in POS or fp not in info:
                continue
            x, y, rot = POS[ref]
            pos = pad_abs(fp, x, y, rot, info)
            sizes = {p["num"]: max(p["sx"], p["sy"]) / 2 for p in info[fp]["pads"]}
            smd = {p["num"] for p in info[fp]["pads"] if not p.get("drill")}
            for num, (px, py) in pos.items():
                net = padnet.get((ref, num), f"nc-{ref}-{num}")
                self.pads.append(dict(ref=ref, num=num, net=net, x=px, y=py, r=sizes.get(num, 1.0), smd=num in smd))
                if num in smd:
                    self.smd_pts.add((px, py))
                if net.startswith("unconnected") or net.startswith("nc-"):
                    continue
                self.nets.setdefault(net, []).append(self.pads[-1])
        for ref in ("H1", "H2", "H3", "H4"):
            x, y, _ = POS[ref]
            self.pads.append(dict(ref=ref, num="", net=f"hole-{ref}", x=x, y=y, r=1.6))
        self.tracks = []   # dict(net, layer, a, b, w)
        self.vias = []     # dict(net, x, y)
        self.fail = []

    # ------------------------------------------------------------ checagens
    def clr_for(self, net, other):
        return CLR_HV if (net in HV_NETS or other in HV_NETS) else CLR

    def seg_ok(self, net, layer, a, b, w):
        # borda
        for p in (a, b):
            if p[0] < EDGE or p[1] < EDGE or p[0] > W - EDGE or p[1] > H - EDGE:
                return False
        # barreira
        xs = (a[0], b[0])
        if net in SEC_NETS:
            if min(xs) < SEC_XMIN:
                return False
        elif net not in ZONE_NETS or net == "PGND":
            if max(xs) > PRIM_XMAX:
                return False
        # fenda de isolacao (duas faixas verticais em x = SLOT_X)
        for (y0, y1) in ((29.0, 59.0), (68.0, 82.0)):
            if seg_seg_dist(a, b, (SLOT_X, y0), (SLOT_X, y1)) < w / 2 + 1.2:
                return False
        # Aula 08: plano de terra de sinal (ilha do controle, B.Cu) fica inteiro -> nenhuma outra rede em B.Cu nessa regiao
        # (permite-se apenas um 'pulo' curto por baixo de outra trilha, <= JOG_MAX, que nao parte o plano)
        if layer == "B.Cu" and net != "PGND" and max(a[1], b[1]) > ILHA_Y0 - w / 2 and min(xs) < PRIM_XMAX                 and math.hypot(b[0] - a[0], b[1] - a[1]) > JOG_MAX:
            return False
        # pads de outras redes
        for p in self.pads:
            if p["net"] == net:
                continue
            if seg_pt_dist(a, b, (p["x"], p["y"])) < p["r"] + w / 2 + self.clr_for(net, p["net"]):
                return False
        # trilhas de outras redes na mesma camada
        for t in self.tracks:
            if t["net"] == net or t["layer"] != layer:
                continue
            if seg_seg_dist(a, b, t["a"], t["b"]) < t["w"] / 2 + w / 2 + self.clr_for(net, t["net"]):
                return False
        # vias de outras redes
        for v in self.vias:
            if v["net"] == net:
                continue
            if seg_pt_dist(a, b, (v["x"], v["y"])) < VIA_D / 2 + w / 2 + self.clr_for(net, v["net"]):
                return False
        return True

    def via_ok(self, net, p):
        if p[0] < EDGE + 1 or p[1] < EDGE + 1 or p[0] > W - EDGE - 1 or p[1] > H - EDGE - 1:
            return False
        for q in self.pads:
            if q["net"] == net:
                continue
            if math.hypot(p[0] - q["x"], p[1] - q["y"]) < q["r"] + VIA_D / 2 + self.clr_for(net, q["net"]):
                return False
        for t in self.tracks:
            if t["net"] == net:
                continue
            if seg_pt_dist(t["a"], t["b"], p) < t["w"] / 2 + VIA_D / 2 + self.clr_for(net, t["net"]):
                return False
        for v in self.vias:
            if v["net"] != net and math.hypot(p[0] - v["x"], p[1] - v["y"]) < VIA_D + self.clr_for(net, v["net"]):
                return False
        return True

    def path_ok(self, net, pts, layers, w):
        """pts: lista de pontos; layers: camada de cada segmento"""
        # pads SMD (pontos de teste) so existem em F.Cu
        if pts[0] in self.smd_pts and layers[0] != "F.Cu":
            return False
        if pts[-1] in self.smd_pts and layers[-1] != "F.Cu":
            return False
        for (a, b), ly in zip(zip(pts[:-1], pts[1:]), layers):
            if a == b:
                continue
            if not self.seg_ok(net, ly, a, b, w):
                return False
        for i in range(1, len(pts) - 1):
            if layers[i - 1] != layers[i] and not self.via_ok(net, pts[i]):
                return False
        return True

    # ------------------------------------------------------------ candidatos
    def candidates(self, a, b):
        ax, ay = a; bx, by = b
        c = []
        c.append([a, b]) if (ax == bx or ay == by) else None
        c.append([a, (bx, ay), b]); c.append([a, (ax, by), b])
        span = max(abs(bx - ax), abs(by - ay))
        offs = [k * GRID for k in range(1, int(60 / GRID))]
        # Z e U
        for o in sorted(set([0.0] + offs), key=abs):
            for m in (min(ax, bx) + o, max(ax, bx) - o, min(ax, bx) - o, max(ax, bx) + o):
                c.append([a, (m, ay), (m, by), b])
            for m in (min(ay, by) + o, max(ay, by) - o, min(ay, by) - o, max(ay, by) + o):
                c.append([a, (ax, m), (bx, m), b])
        return c

    def candidates3(self, a, b, step=1.0, margem=14.0):
        ax, ay = a; bx, by = b
        out = []
        x0, x1 = max(EDGE + 1, min(ax, bx) - margem), min(W - EDGE - 1, max(ax, bx) + margem)
        y0, y1 = max(EDGE + 1, min(ay, by) - margem), min(H - EDGE - 1, max(ay, by) + margem)
        xs = list(frange(x0, x1, step)); ys = list(frange(y0, y1, step))
        for m1 in xs:
            for m2 in ys:
                out.append([a, (m1, ay), (m1, m2), (bx, m2), b])
                out.append([a, (ax, m2), (m1, m2), (m1, by), b])
        return out

    @staticmethod
    def comprimento(pts, layers):
        L = sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(pts[:-1], pts[1:]))
        vias = sum(1 for i in range(1, len(pts) - 1) if layers[i - 1] != layers[i])
        return L + 6.0 * vias + 0.5 * (len(pts) - 2)

    def connect(self, net, a, b, w):
        """devolve o caminho valido mais curto (comprimento + penalidade por via e por dobra)"""
        best = None
        def testa(pts, layers):
            nonlocal best
            if self.path_ok(net, pts, layers, w):
                c = self.comprimento(pts, layers)
                if best is None or c < best[0]:
                    best = (c, pts, layers)
        for pts in self.candidates(a, b):
            n = len(pts) - 1
            for ly in ("F.Cu", "B.Cu"):
                testa(pts, [ly] * n)
            if n >= 2:
                for layers in (("F.Cu",) * (n - 1) + ("B.Cu",), ("B.Cu",) * (n - 1) + ("F.Cu",), ("F.Cu",) + ("B.Cu",) * (n - 1), ("B.Cu",) + ("F.Cu",) * (n - 1)):
                    testa(pts, list(layers))
            if n == 3:
                testa(pts, ["F.Cu", "B.Cu", "F.Cu"]); testa(pts, ["B.Cu", "F.Cu", "B.Cu"])
        if best is None:
            # 'pulo' curto em B.Cu (2 vias) por baixo de uma trilha que bloqueia um trecho reto em F.Cu
            for pts in self.candidates(a, b)[:120]:
                for i in range(len(pts) - 1):
                    p, q = pts[i], pts[i + 1]
                    L = math.hypot(q[0] - p[0], q[1] - p[1])
                    if L <= JOG_MAX + 2:
                        continue
                    ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
                    J = 4.0
                    for s in frange(1.0, L - J - 1.0, 1.0):
                        q1 = (round(p[0] + ux * s, 3), round(p[1] + uy * s, 3)); q2 = (round(q1[0] + ux * J, 3), round(q1[1] + uy * J, 3))
                        npts = pts[:i + 1] + [q1, q2] + pts[i + 1:]
                        layers = ["F.Cu"] * (len(npts) - 1); layers[i + 1] = "B.Cu"
                        testa(npts, layers)
                if best is not None:
                    break
        if best is None:
            for pts in self.candidates3(a, b):
                for layers in (["F.Cu"] * 4, ["B.Cu"] * 4, ["F.Cu", "F.Cu", "B.Cu", "B.Cu"], ["B.Cu", "B.Cu", "F.Cu", "F.Cu"],
                               ["F.Cu", "B.Cu", "B.Cu", "F.Cu"], ["B.Cu", "F.Cu", "F.Cu", "B.Cu"]):
                    testa(pts, layers)
        if best is None:
            return None, None
        return best[1], best[2]

    def chamfer(self, net, pts, layers, w):
        """Aula 08: evitar trilhas a 90 graus -> substitui cada canto reto (sem via) por dois cantos de 45 graus,
        desde que a diagonal respeite os isolamentos."""
        pts = list(pts); layers = list(layers)
        out = [pts[0]]; ol = []
        for i in range(1, len(pts) - 1):
            A, P, B = out[-1], pts[i], pts[i + 1]
            L1, L2 = layers[i - 1], layers[i]
            ax, ay = A[0] - P[0], A[1] - P[1]; bx, by = B[0] - P[0], B[1] - P[1]
            la, lb = math.hypot(ax, ay), math.hypot(bx, by)
            feito = False
            if L1 == L2 and la > 0.2 and lb > 0.2 and abs(ax * bx + ay * by) < 1e-6:
                for d in (max(1.5, 1.5 * w), 1.0, 0.6):
                    d = min(d, la / 2, lb / 2)
                    P1 = (round(P[0] + ax / la * d, 3), round(P[1] + ay / la * d, 3))
                    P2 = (round(P[0] + bx / lb * d, 3), round(P[1] + by / lb * d, 3))
                    if self.seg_ok(net, L1, P1, P2, w):
                        out += [P1, P2]; ol += [L1, L1]; feito = True; break
            if not feito:
                out.append(P); ol.append(L1)
        out.append(pts[-1]); ol.append(layers[-1])
        return out, ol

    def add_path(self, net, pts, layers, w):
        pts, layers = self.chamfer(net, pts, layers, w)
        for (a, b), ly in zip(zip(pts[:-1], pts[1:]), layers):
            if a != b:
                self.tracks.append(dict(net=net, layer=ly, a=a, b=b, w=w))
        for i in range(1, len(pts) - 1):
            if layers[i - 1] != layers[i]:
                self.vias.append(dict(net=net, x=pts[i][0], y=pts[i][1]))

    def route_net(self, net, pads, w):
        done = [pads[0]]
        todo = pads[1:]
        pend = []
        while todo:
            best = min(((math.hypot(p["x"] - q["x"], p["y"] - q["y"]), p, q) for p in todo for q in done), key=lambda t: t[0])
            _, p, q = best
            todo.remove(p)
            # tenta ligar p a cada pad ja ligado, do mais proximo ao mais distante
            ok = False
            for q2 in sorted(done, key=lambda q: math.hypot(p["x"] - q["x"], p["y"] - q["y"])):
                pts, layers = self.connect(net, (q2["x"], q2["y"]), (p["x"], p["y"]), w)
                if pts:
                    self.add_path(net, pts, layers, w); ok = True; break
            if ok:
                done.append(p)
            else:
                pend.append(p)
        # segunda passada: pads que falharam, agora com mais pads ligados
        for p in list(pend):
            for q2 in sorted(done, key=lambda q: math.hypot(p["x"] - q["x"], p["y"] - q["y"])):
                pts, layers = self.connect(net, (q2["x"], q2["y"]), (p["x"], p["y"]), w)
                if pts:
                    self.add_path(net, pts, layers, w); done.append(p); pend.remove(p); break
        for p in pend:
            q = min(done, key=lambda q: math.hypot(p["x"] - q["x"], p["y"] - q["y"]))
            self.fail.append((net, f"{p['ref']}.{p['num']}", self.explain(net, (q["x"], q["y"]), (p["x"], p["y"]), w)))

    def explain(self, net, a, b, w):
        import collections
        cnt = collections.Counter()
        for pts in self.candidates(a, b)[:300]:
            for ly in ("F.Cu", "B.Cu"):
                for s0, s1 in zip(pts[:-1], pts[1:]):
                    if s0 == s1:
                        continue
                    bl = self.blocker(net, ly, s0, s1, w)
                    if bl:
                        cnt[bl] += 1; break
        return cnt.most_common(4)

    def blocker(self, net, layer, a, b, w):
        for p in (a, b):
            if p[0] < EDGE or p[1] < EDGE or p[0] > W - EDGE or p[1] > H - EDGE:
                return "borda"
        xs = (a[0], b[0])
        if net in SEC_NETS and min(xs) < SEC_XMIN:
            return "barreira"
        if net not in SEC_NETS and (net not in ZONE_NETS or net == "PGND") and max(xs) > PRIM_XMAX:
            return "barreira"
        for (y0, y1) in ((29.0, 59.0), (68.0, 82.0)):
            if seg_seg_dist(a, b, (SLOT_X, y0), (SLOT_X, y1)) < w / 2 + 1.2:
                return "fenda"
        for p in self.pads:
            if p["net"] != net and seg_pt_dist(a, b, (p["x"], p["y"])) < p["r"] + w / 2 + self.clr_for(net, p["net"]):
                return f"pad {p['ref']}.{p['num']}[{p['net']}]"
        for t in self.tracks:
            if t["net"] != net and t["layer"] == layer and seg_seg_dist(a, b, t["a"], t["b"]) < t["w"] / 2 + w / 2 + self.clr_for(net, t["net"]):
                return f"trilha {t['net']} {layer}"
        return None

    def run(self, order):
        for net in order:
            if net not in self.nets:
                continue
            pads = self.nets[net]
            w = WIDTH.get(net, 0.5)
            if net in ZONE_NETS:
                continue
            self.route_net(net, pads, w)

    def route_zone_loops(self):
        """lacos criticos de terra em F.Cu (retorno do Rsense ao bulk; retorno do secundario ao banco de capacitores)"""
        P = {(p["ref"], p["num"]): (p["x"], p["y"]) for p in self.pads}
        for net, chain, w in (("PGND", [("R10", "2"), ("R9", "2"), ("C1", "2")], 1.5), ("SGND", [("T1", "7"), ("T1", "6"), ("C10", "2")], 2.0),
("SGND", [("C10", "2"), ("C11", "2"), ("C12", "2"), ("C13", "2"), ("J2", "2")], 2.0),
                              ("SGND", [("CY1", "2"), ("U2", "2")], 0.8)):
            for a, b in zip(chain[:-1], chain[1:]):
                pts, layers = self.connect(net, P[a], P[b], w)
                if pts:
                    self.add_path(net, pts, layers, w)
                else:
                    self.fail.append((net, f"{a}-{b}"))


ORDER = ["/BULK", "/DRAIN", "/COMP", "/DRV", "/GATE", "/SW", "Net-(D2-K)", "Net-(R5-Pad2)", "Net-(BR1-Pad2)", "Net-(BR1-Pad3)", "Net-(CX1-Pad1)", "Net-(CX1-Pad2)",
         "Net-(J1-Pin_1)", "Net-(J1-Pin_2)", "Net-(R1-Pad2)", "Net-(R3-Pad2)", "Net-(T1-S2)", "Net-(D1-K)", "/VO", "Net-(C9-Pad1)",
         "/CS", "/VCC", "/AUX", "Net-(D4-K)", "/VREF", "Net-(U1-RC)", "/KA", "/LEDA", "Net-(U2-REF)", "Net-(C14-Pad2)"]

def ilha_continua(r, passo=0.5):
    """Rasteriza a ilha de terra de sinal (B.Cu, y>=ILHA_Y0, x<=81) e verifica, por flood-fill a partir do ponto-estrela,
    se todos os pads PGND da ilha ficam no mesmo pedaco de cobre."""
    xs = [x for x in frange(1.0, 81.0, passo)]; ys = [y for y in frange(ILHA_Y0 + 0.5, H - 1.0, passo)]
    nx, ny = len(xs), len(ys)
    livre = [[True] * ny for _ in range(nx)]
    obst = [(t["a"], t["b"], t["w"] / 2 + 0.5) for t in r.tracks if t["layer"] == "B.Cu" and t["net"] != "PGND"]
    obst += [((v["x"], v["y"]), (v["x"], v["y"]), VIA_D / 2 + 0.5) for v in r.vias if v["net"] != "PGND"]
    obst += [((p["x"], p["y"]), (p["x"], p["y"]), p["r"] + 0.5) for p in r.pads if p["net"] != "PGND" and p["y"] > ILHA_Y0 - 2 and p["x"] < 82]
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            for a, b, d in obst:
                if seg_pt_dist(a, b, (x, y)) < d:
                    livre[i][j] = False; break
    def idx(p):
        return min(range(nx), key=lambda i: abs(xs[i] - p[0])), min(range(ny), key=lambda j: abs(ys[j] - p[1]))
    P = {(p["ref"], p["num"]): (p["x"], p["y"]) for p in r.pads}
    s = idx((P[("R10", "2")][0], ILHA_Y0 + 1.0))
    vis = set([s]); fila = [s]
    while fila:
        i, j = fila.pop()
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            k, l = i + di, j + dj
            if 0 <= k < nx and 0 <= l < ny and (k, l) not in vis and livre[k][l]:
                vis.add((k, l)); fila.append((k, l))
    fora = []
    for p in r.pads:
        if p["net"] == "PGND" and p["y"] > ILHA_Y0 and p["x"] < 82:
            i, j = idx((p["x"], p["y"]))
            viz = [(i + di, j + dj) for di in range(-3, 4) for dj in range(-3, 4)]
            if not any(v in vis for v in viz):
                fora.append(f"{p['ref']}.{p['num']}")
    return fora


if __name__ == "__main__":
    r = Router()
    # Aula 08: terra de sinal (ilha do UC3845) ligado ao terra de potencia em UM unico ponto - o lado frio do Rsense (R10.2)
    P = {(p["ref"], p["num"]): (p["x"], p["y"]) for p in r.pads}
    estrela = [P[("R10", "2")], (P[("R10", "2")][0], 62.0)]
    assert r.path_ok("PGND", estrela, ["B.Cu"], 1.5), "estrela PGND bloqueada"
    r.add_path("PGND", estrela, ["B.Cu"], 1.5)
    r.route_zone_loops()
    r.run(ORDER)
    restantes = [n for n in r.nets if n not in ORDER and n not in ZONE_NETS]
    r.run(restantes)
    out = dict(tracks=[dict(net=t["net"], layer=t["layer"], x1=t["a"][0], y1=t["a"][1], x2=t["b"][0], y2=t["b"][1], w=t["w"]) for t in r.tracks],
               vias=[dict(net=v["net"], x=v["x"], y=v["y"], d=VIA_D, drill=VIA_DRILL) for v in {(v["net"], v["x"], v["y"]): v for v in r.vias}.values()])
    (HERE / "rotas.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"trilhas: {len(r.tracks)}  vias: {len(r.vias)}  falhas: {len(r.fail)}")
    fora = ilha_continua(r)
    print("ilha de terra de sinal continua:", "sim" if not fora else f"NAO - pads isolados: {fora}")
    for f in r.fail:
        print("  FALHA", f)
