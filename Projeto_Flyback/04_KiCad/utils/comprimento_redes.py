"""Comprimento de trilha por rede e caixa envolvente dos footprints da placa B (pcbnew do KiCad 10).
Uso: "C:\Program Files\KiCad\10.0\bin\python.exe" utils\comprimento_redes.py [placa.kicad_pcb] > comprimento_redes.txt  (a partir de 04_KiCad)
"""
import pcbnew, sys
from pathlib import Path
b = pcbnew.LoadBoard(sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent.parent / "fonte_flyback_12V3A.kicad_pcb"))
from collections import defaultdict
L = defaultdict(float); n = defaultdict(int)
for t in b.GetTracks():
    if t.GetClass() == "PCB_TRACK":
        L[t.GetNetname()] += t.GetLength()/1e6; n[t.GetNetname()] += 1
for k in sorted(L, key=lambda k: -L[k]):
    print(f"{k:28s} {L[k]:7.1f} mm  {n[k]} segs")
# component list with layer/height summary
print("--- footprints")
for f in b.GetFootprints():
    bb = f.GetBoundingBox(False, False)
    print(f.GetReference(), f.GetFPIDAsString().split(":")[-1][:40], round(f.GetPosition().x/1e6,1), round(f.GetPosition().y/1e6,1), round(bb.GetWidth()/1e6,1), round(bb.GetHeight()/1e6,1))
