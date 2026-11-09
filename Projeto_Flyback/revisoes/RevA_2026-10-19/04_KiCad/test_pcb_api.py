"""Bisseciona o crash do SaveBoard no pcbnew standalone. Uso: python test_pcb_api.py <estagio 1..5>"""
import sys
from pathlib import Path
import pcbnew
from pcbnew import VECTOR2I, FromMM

st = int(sys.argv[1])
HERE = Path(__file__).resolve().parent
out = HERE / "testes" / f"t_{st}.kicad_pcb"
out.parent.mkdir(exist_ok=True)
board = pcbnew.NewBoard(str(out))


def mm(x, y):
    return VECTOR2I(FromMM(x), FromMM(y))


if st >= 1:   # contorno
    s = pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetStart(mm(0, 0)); s.SetEnd(mm(50, 0)); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(FromMM(0.1)); board.Add(s)
if st >= 2:   # rede + footprint
    ni = pcbnew.NETINFO_ITEM(board, "N1"); board.Add(ni)
    m = pcbnew.FootprintLoad(r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Resistor_THT.pretty", "R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
    m.SetReference("R1"); m.SetPosition(mm(10, 10)); m.SetOrientationDegrees(90)
    for pad in m.Pads():
        pad.SetNet(ni)
    board.Add(m)
if st >= 3:   # texto
    t = pcbnew.PCB_TEXT(board); t.SetText("abc"); t.SetPosition(mm(20, 20)); t.SetLayer(pcbnew.F_SilkS); t.SetTextSize(VECTOR2I(FromMM(1), FromMM(1))); board.Add(t)
if st >= 4:   # zona
    z = pcbnew.ZONE(board); z.SetLayer(pcbnew.B_Cu); z.SetNet(ni)
    poly = pcbnew.SHAPE_POLY_SET(); poly.NewOutline()
    for (x, y) in [(1, 1), (40, 1), (40, 30), (1, 30)]:
        poly.Append(FromMM(x), FromMM(y))
    z.SetOutline(poly); board.Add(z)
if st >= 5:   # design settings
    ds = board.GetDesignSettings(); ds.m_MinClearance = FromMM(0.3); ds.SetCopperLayerCount(2)
pcbnew.SaveBoard(str(out), board)
print("estagio", st, "ok")
