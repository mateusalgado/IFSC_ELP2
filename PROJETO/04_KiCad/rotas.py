"""Aplica as trilhas/vias de rotas.json na placa (chamado por gera_pcb.py dentro do Python do KiCad)."""
import json
from pathlib import Path
import pcbnew

HERE = Path(__file__).resolve().parent
LAYER = {"F.Cu": pcbnew.F_Cu, "B.Cu": pcbnew.B_Cu}


def aplica(board, fps, netinfo, nets, mm, FromMM):
    data = json.loads((HERE / "rotas.json").read_text(encoding="utf-8"))
    n = 0
    for t in data["tracks"]:
        tr = pcbnew.PCB_TRACK(board)
        tr.SetStart(mm(t["x1"], t["y1"])); tr.SetEnd(mm(t["x2"], t["y2"]))
        tr.SetWidth(FromMM(t["w"])); tr.SetLayer(LAYER[t["layer"]])
        if t["net"] in netinfo:
            tr.SetNet(netinfo[t["net"]])
        board.Add(tr); n += 1
    for v in data["vias"]:
        via = pcbnew.PCB_VIA(board)
        via.SetPosition(mm(v["x"], v["y"]))
        via.SetWidth(FromMM(v["d"])); via.SetDrill(FromMM(v["drill"]))
        via.SetViaType(pcbnew.VIATYPE_THROUGH)
        via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
        if v["net"] in netinfo:
            via.SetNet(netinfo[v["net"]])
        board.Add(via)
    print(f"rotas: {n} trilhas, {len(data['vias'])} vias")
