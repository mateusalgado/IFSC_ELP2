"""Gera a PCI (fonte_flyback_12V3A.kicad_pcb) com o Python do KiCad (pcbnew):
  - contorno 130 x 85 mm, 4 furos M3, fenda de isolacao primario/secundario sob o trafo e o opto;
  - footprints das bibliotecas oficiais + fonte.pretty, redes da netlist exportada pelo kicad-cli;
  - posicionamento manual (regras da Aula 08: fluxo entrada -> saida, laco de alta di/dt curto,
    controle agrupado junto ao CI, isolacao >= 8 mm, dissipadores com espaco);
  - zonas de terra PGND (primario) e SGND (secundario) na camada inferior;
  - trilhas definidas em rotas.py (lista de conexoes com pontos de passagem).
Uso: "C:\\Program Files\\KiCad\\10.0\\bin\\python.exe" gera_pcb.py
"""
import json
import os
import re
import sys
STAGE = int(os.environ.get('STAGE', '99'))
KEEP = []
from pathlib import Path
import pcbnew
from pcbnew import VECTOR2I, FromMM

HERE = Path(__file__).resolve().parent
LIBROOT = Path(r"C:\Program Files\KiCad\10.0\share\kicad\footprints")
PROJ = "fonte_flyback_12V3A"
BARRIER_X = 84.0              # fenda de isolacao primario (esq) / secundario (dir)


def mm(x, y):
    return VECTOR2I(FromMM(x), FromMM(y))


# ------------------------------------------------------------------ netlist (kicad-cli sch export netlist)
def parse_netlist(path):
    """retorna {(ref, pin): netname}, {ref: (value, footprint)} a partir da netlist kicadsexpr"""
    sys.path.insert(0, str(HERE))
    from sexp import parse, find, find_all
    doc = parse(Path(path).read_text(encoding="utf-8"))[0]
    comps = {}
    for c in find_all(find(doc, "components"), "comp"):
        fp = find(c, "footprint")
        comps[str(find(c, "ref")[1])] = (str(find(c, "value")[1]), str(fp[1]) if fp else "")
    nets = {}
    for n in find_all(find(doc, "nets"), "net"):
        name = str(find(n, "name")[1])
        for node in find_all(n, "node"):
            nets[(str(find(node, "ref")[1]), str(find(node, "pin")[1]))] = name
    return nets, comps


# ------------------------------------------------------------------ posicionamento (x, y, rot) em mm
# origem no canto superior esquerdo da placa; y cresce para baixo. rot em graus (CCW no KiCad).
sys.path.insert(0, str(HERE))
from placement import POS, SLOT_X, W, H


def build():
    nets, comps = parse_netlist(HERE / "netlist.net")
    out = HERE / f"{PROJ}.kicad_pcb"
    board = pcbnew.NewBoard(str(out))
    # --- regras de projeto ---
    ds = board.GetDesignSettings()
    if STAGE < 1: ds = None
    if ds is not None: pass

    if STAGE >= 1:
        ds.m_MinClearance = FromMM(0.2)
        ds.m_TrackMinWidth = FromMM(0.3)
        ds.m_ViasMinSize = FromMM(0.8)
        ds.m_MinThroughDrill = FromMM(0.4)
        ds.SetCopperLayerCount(2)
    tb=board.GetTitleBlock(); tb.SetRevision("B"); tb.SetDate("2026-11-05"); board.SetTitleBlock(tb)
    # --- contorno ---
    def line(x0, y0, x1, y1, layer=pcbnew.Edge_Cuts, w=0.1):
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(mm(x0, y0)); s.SetEnd(mm(x1, y1)); s.SetLayer(layer); s.SetWidth(FromMM(w))
        board.Add(s)
    line(0, 0, W, 0); line(W, 0, W, H); line(W, H, 0, H); line(0, H, 0, 0)
    # fenda de isolacao sob o trafo (entre as fileiras de pinos) e sob o opto / cap Y
    def slot(x, y0, y1, wslot=1.2):
        line(x - wslot / 2, y0, x - wslot / 2, y1); line(x + wslot / 2, y0, x + wslot / 2, y1)
        line(x - wslot / 2, y0, x + wslot / 2, y0); line(x - wslot / 2, y1, x + wslot / 2, y1)
    slot(SLOT_X, 29.0, 59.0)
    slot(SLOT_X, 68.0, 82.0)
    # --- redes ---
    netinfo = {}
    for name in sorted(set(nets.values())):
        ni = pcbnew.NETINFO_ITEM(board, name)
        board.Add(ni)
        netinfo[name] = ni
    # --- footprints ---
    fps = {}
    for ref, (value, fp) in comps.items():
        if not fp or STAGE < 2:
            continue
        lib, name = fp.split(":")
        libpath = str(HERE / "fonte.pretty") if lib == "fonte" else str(LIBROOT / f"{lib}.pretty")
        m = pcbnew.FootprintLoad(libpath, name)
        if m is None:
            print("footprint nao encontrado:", fp); continue
        m.SetFPID(pcbnew.LIB_ID(lib, name)); m.SetReference(ref); m.SetValue(value)
        x, y, rot = POS.get(ref, (W / 2, H / 2, 0))
        m.SetPosition(mm(x, y))
        m.SetOrientationDegrees(rot)
        for pad in m.Pads():
            key = (ref, pad.GetNumber())
            if key in nets:
                pad.SetNet(netinfo[nets[key]])
        # referencia: texto 0,8 mm acima da caixa envolvente (evita sobreposicao de silk); furos sem referencia
        r = m.Reference()
        r.SetTextSize(VECTOR2I(FromMM(0.8), FromMM(0.8))); r.SetTextThickness(FromMM(0.12))
        if ref.startswith("H"):
            r.SetVisible(False)
        board.Add(m)
        fps[ref] = m
    # --- posiciona as referencias onde nao colidem com outros footprints (silk limpo) ---
    boxes = {}
    for ref, m in fps.items():
        bb = m.GetBoundingBox(False, False)
        boxes[ref] = (bb.GetX() / 1e6, bb.GetY() / 1e6, bb.GetRight() / 1e6, bb.GetBottom() / 1e6)
    def livre(ref, rect):
        x0, y0, x1, y1 = rect
        if x0 < 1.5 or y0 < 1.5 or x1 > W - 1.5 or y1 > H - 1.5:
            return False
        if abs(SLOT_X - (x0 + x1) / 2) < (x1 - x0) / 2 + 1.0 and (29 <= y1 and y0 <= 59 or 68 <= y1 and y0 <= 82):
            return False
        for o, (a0, b0, a1, b1) in boxes.items():
            if o == ref:
                continue
            if x0 < a1 + 0.25 and x1 > a0 - 0.25 and y0 < b1 + 0.25 and y1 > b0 - 0.25:
                return False
        return True
    for ref, m in fps.items():
        if ref.startswith("H"):
            continue
        tw, th = 0.75 * len(ref) + 0.3, 1.0
        a0, b0, a1, b1 = boxes[ref]
        cx, cy = (a0 + a1) / 2, (b0 + b1) / 2
        cands = [(cx, b0 - 0.8), (cx, b1 + 0.8), (a0 - tw / 2 - 0.5, cy), (a1 + tw / 2 + 0.5, cy),
                 (a0 + tw / 2, b0 - 0.8), (a1 - tw / 2, b0 - 0.8), (a0 + tw / 2, b1 + 0.8), (a1 - tw / 2, b1 + 0.8),
                 (a0 - tw / 2 - 0.5, b0 + th / 2), (a1 + tw / 2 + 0.5, b0 + th / 2), (a0 - tw / 2 - 0.5, b1 - th / 2), (a1 + tw / 2 + 0.5, b1 - th / 2),
                 (cx, b0 - 1.9), (cx, b1 + 1.9)]
        pos = None
        for (x, y) in cands:
            if livre(ref, (x - tw / 2, y - th / 2, x + tw / 2, y + th / 2)):
                pos = (x, y); break
        if pos is None:
            pos = (cx, b0 - 0.8)
            print("referencia sem lugar livre:", ref)
        r = m.Reference(); r.SetTextAngleDegrees(0); r.SetPosition(mm(*pos))
        boxes[ref + "#"] = (pos[0] - tw / 2, pos[1] - th / 2, pos[0] + tw / 2, pos[1] + th / 2)
    # --- zonas de terra (camada inferior) ---
    def zone(net, pts, layer=pcbnew.B_Cu, clearance=0.5):
        z = pcbnew.ZONE(board)
        z.SetLayer(layer); z.SetNet(netinfo[net])



        poly = pcbnew.SHAPE_POLY_SET()
        poly.NewOutline()
        for (x, y) in pts:
            poly.Append(FromMM(x), FromMM(y))
        z.SetOutline(poly)
        KEEP.append(poly); KEEP.append(z)
        board.Add(z)
        return z
    # area de regra (sem restricoes) que delimita a excecao de isolacao sob a fenda do opto (ver .kicad_dru "isolacao_fenda_opto")
    if STAGE >= 3:
        ra = pcbnew.ZONE(board); ra.SetIsRuleArea(True); ra.SetZoneName("fenda_opto")
        try:
            ls = pcbnew.LSET(); ls.AddLayer(pcbnew.F_Cu); ls.AddLayer(pcbnew.B_Cu); ra.SetLayerSet(ls)
        except Exception as e:
            print("layerset da area de regra:", e); ra.SetLayer(pcbnew.F_Cu)
        for setter in ("SetDoNotAllowCopperPour", "SetDoNotAllowTracks", "SetDoNotAllowVias", "SetDoNotAllowPads", "SetDoNotAllowFootprints"):
            if hasattr(ra, setter): getattr(ra, setter)(False)
        rp = pcbnew.SHAPE_POLY_SET(); rp.NewOutline()
        for (x, y) in ((77.0, 65.0), (92.0, 65.0), (92.0, 79.0), (77.0, 79.0)):
            rp.Append(FromMM(x), FromMM(y))
        ra.SetOutline(rp); KEEP.append(rp); KEEP.append(ra); board.Add(ra)
    # Aula 08: terra de potencia e terra de sinal (ilha do controle, y >= 61) separados, unidos num unico ponto (trilha-estrela no Rsense)
    if STAGE >= 3: zone("PGND", [(1, 1), (78, 1), (78, 60), (81, 60), (81, 66.5), (75, 66.5), (75, 60), (1, 60)])
    if STAGE >= 3: zone("PGND", [(1, 61), (74, 61), (74, 67.5), (81, 67.5), (81, H - 1), (1, H - 1)])
    if STAGE >= 3: zone("SGND", [(102, 1), (W - 1, 1), (W - 1, H - 1), (88.5, H - 1), (88.5, 60), (90, 60), (90, 26), (102, 26)])
    # --- trilhas ---
    try:
        import rotas
        rotas.aplica(board, fps, netinfo, nets, mm, FromMM)
    except ImportError:
        print("rotas.py ausente: placa sem trilhas")
    # --- textos ---
    if STAGE < 4:
        pcbnew.SaveBoard(str(out), board); print('salvo antes dos textos'); return
    t = pcbnew.PCB_TEXT(board)
    t.SetText("REV B (05/11/2026) - FLYBACK 12V/3A UC3845 - IFSC EPO II 2026-2 - M. S. B. Costa"); t.SetPosition(mm(70, 88)); t.SetLayer(pcbnew.F_SilkS)
    t.SetTextSize(VECTOR2I(FromMM(1.2), FromMM(1.2))); board.Add(t)
    # marcacoes de seguranca e de uso (IEC 62368-1: valor do fusivel junto a F1; polaridade e tensao na saida; L/N na entrada; aviso do bulk)
    def silk(s, x, y, size=0.8):
        tt = pcbnew.PCB_TEXT(board); tt.SetText(s); tt.SetPosition(mm(x, y)); tt.SetLayer(pcbnew.F_SilkS)
        tt.SetTextSize(VECTOR2I(FromMM(size), FromMM(size))); tt.SetTextThickness(FromMM(0.12)); board.Add(tt)
    silk("F1 T2A 250V", 43.0, 7.0); silk("N", 10.75, 16.0); silk("L", 10.75, 21.08)
    silk("0V", 131.0, 60.3); silk("+12V 3A", 133.0, 75.0)
    silk("C1 400V DESCARREGAR", 46.5, 17.6)
    t2 = pcbnew.PCB_TEXT(board)
    t2.SetText("PRIMARIO - ALTA TENSAO"); t2.SetPosition(mm(60, 85)); t2.SetLayer(pcbnew.F_SilkS)
    t2.SetTextSize(VECTOR2I(FromMM(1.0), FromMM(1.0))); board.Add(t2)
    t3 = pcbnew.PCB_TEXT(board)
    t3.SetText("SECUNDARIO 12V"); t3.SetPosition(mm(122, 4)); t3.SetLayer(pcbnew.F_SilkS)
    t3.SetTextSize(VECTOR2I(FromMM(1.0), FromMM(1.0))); board.Add(t3)
    out = HERE / f"{PROJ}.kicad_pcb"
    pcbnew.SaveBoard(str(out), board)
    print("ok:", out.name, len(fps), "footprints", len(netinfo), "redes")
    # preenchimento das zonas: recarrega a placa do arquivo (o Fill em BOARD() recem-criado falha no Python standalone)
    try:
        b2 = pcbnew.LoadBoard(str(out))
        filler = pcbnew.ZONE_FILLER(b2)
        filler.Fill(b2.Zones())
        pcbnew.SaveBoard(str(out), b2)
        print("zonas preenchidas")
    except Exception as e:
        print("zonas nao preenchidas:", e)


if __name__ == "__main__":
    build()
