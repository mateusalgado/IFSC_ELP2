"""Explica por que uma ligacao falha no roteador: lista os obstaculos que bloqueiam os primeiros candidatos.
Uso: python3 debug_router.py NET REF.PIN REF.PIN   (ex.: /BULK C1.1 T1.1)"""
import sys, math, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import router as R

net, a_id, b_id = sys.argv[1], sys.argv[2], sys.argv[3]
r = R.Router()
r.route_zone_loops()
for n in R.ORDER:
    if n == net:
        break
    if n in r.nets and n not in R.ZONE_NETS:
        r.route_net(n, r.nets[n], R.WIDTH.get(n, 0.5))
P = {f"{p['ref']}.{p['num']}": p for p in r.pads}
a, b = P[a_id], P[b_id]
w = R.WIDTH.get(net, 0.5)
blockers = collections.Counter()


def seg_blocker(net, layer, a, b, w):
    for p in (a, b):
        if p[0] < R.EDGE or p[1] < R.EDGE or p[0] > R.W - R.EDGE or p[1] > R.H - R.EDGE:
            return "borda"
    xs = (a[0], b[0])
    if net in R.SEC_NETS and min(xs) < R.SEC_XMIN:
        return "barreira(sec)"
    if net not in R.SEC_NETS and (net not in R.ZONE_NETS or net == "PGND") and max(xs) > R.PRIM_XMAX:
        return "barreira(prim)"
    for (y0, y1) in ((29.0, 59.0), (68.0, 82.0)):
        if R.seg_seg_dist(a, b, (R.SLOT_X, y0), (R.SLOT_X, y1)) < w / 2 + 1.2:
            return "fenda"
    for p in r.pads:
        if p["net"] == net:
            continue
        if R.seg_pt_dist(a, b, (p["x"], p["y"])) < p["r"] + w / 2 + r.clr_for(net, p["net"]):
            return f"pad {p['ref']}.{p['num']}[{p['net']}]"
    for t in r.tracks:
        if t["net"] == net or t["layer"] != layer:
            continue
        if R.seg_seg_dist(a, b, t["a"], t["b"]) < t["w"] / 2 + w / 2 + r.clr_for(net, t["net"]):
            return f"trilha {t['net']} {layer}"
    return None


cands = r.candidates((a["x"], a["y"]), (b["x"], b["y"]))
print(f"{net}: {a_id}@({a['x']},{a['y']}) -> {b_id}@({b['x']},{b['y']})  w={w}  candidatos={len(cands)}")
shown = 0
for pts in cands[:400]:
    for ly in ("F.Cu", "B.Cu"):
        bl = None
        for s0, s1 in zip(pts[:-1], pts[1:]):
            if s0 == s1:
                continue
            bl = seg_blocker(net, ly, s0, s1, w)
            if bl:
                break
        if bl is None:
            print("  OK:", ly, pts); shown += 1
        else:
            blockers[bl] += 1
            if shown < 6 and len(pts) <= 3:
                print(f"  {ly} {[tuple(round(c,1) for c in q) for q in pts]} -> {bl}"); shown += 1
print("bloqueios mais frequentes:", blockers.most_common(8))
