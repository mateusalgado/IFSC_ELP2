"""Ensaio de cobertura do DRC (parecer, item 05): numa COPIA da placa B insere violacoes deliberadas e verifica
que cada regra do .kicad_dru dispara:
  1. HV_clearance        -> trilha de rede nao-HV a 0,5 mm de um pad /BULK;
  2. isolacao_prim_sec   -> trilha SGND (SEC_PWR) a 2 mm de um pad do primario (PGND);
  3. largura_HV          -> trilha /BULK com 0,5 mm;
  4. largura_SEC_potencia-> trilha /VO com 0,8 mm;
  5. borda               -> trilha a 0,2 mm da borda.
Uso: "C:\\Program Files\\KiCad\\10.0\\bin\\python.exe" testa_regras.py  (gera teste_regras/ e roda o kicad-cli)
"""
import json
import shutil
import subprocess
from pathlib import Path
import pcbnew

HERE = Path(__file__).resolve().parent
T = HERE / "teste_regras"
T.mkdir(exist_ok=True)
for f in ("fonte_flyback_12V3A.kicad_pcb", "fonte_flyback_12V3A.kicad_pro", "fonte_flyback_12V3A.kicad_dru", "fp-lib-table"):
    shutil.copy(HERE / f, T / f)
if (HERE / "fonte.pretty").exists() and not (T / "fonte.pretty").exists():
    shutil.copytree(HERE / "fonte.pretty", T / "fonte.pretty")
b = pcbnew.LoadBoard(str(T / "fonte_flyback_12V3A.kicad_pcb"))
mm = lambda x, y: pcbnew.VECTOR2I(int(x * 1e6), int(y * 1e6))
nets = {n.GetNetname(): n for n in b.GetNetInfo().NetsByName().values()} if hasattr(b.GetNetInfo(), "NetsByName") else {}
if not nets:
    for i in range(b.GetNetCount()):
        n = b.FindNet(i)
        if n: nets[n.GetNetname()] = n
pads = {}
for fp in b.GetFootprints():
    for p in fp.Pads():
        pads[(fp.GetReference(), p.GetNumber())] = p


def track(net, x1, y1, x2, y2, w, layer=pcbnew.F_Cu):
    t = pcbnew.PCB_TRACK(b)
    t.SetStart(mm(x1, y1)); t.SetEnd(mm(x2, y2)); t.SetWidth(int(w * 1e6)); t.SetLayer(layer); t.SetNet(nets[net]); b.Add(t)


c1 = pads[("C1", "1")].GetPosition(); c1x, c1y = c1.x / 1e6, c1.y / 1e6          # /BULK (HV)
t1 = pads[("T1", "4")].GetPosition(); t4x, t4y = t1.x / 1e6, t1.y / 1e6          # PGND (primario)
# 1. HV_clearance: trilha /VCC a 0,5 mm do pad de C1 (raio do pad ~1,2 mm)
track("/VCC", c1x + 1.7, c1y - 3, c1x + 1.7, c1y + 3, 0.5)
# 2. isolacao_prim_sec: trilha SGND a 2 mm do pad PGND de T1 (lado primario)
track("SGND", t4x - 3.0, t4y - 2, t4x - 3.0, t4y + 2, 0.8)
# 3. largura_HV: trilha /BULK de 0,5 mm
track("/BULK", c1x, c1y, c1x, c1y - 4, 0.5)
# 4. largura_SEC_potencia: trilha /VO de 0,8 mm
j2 = pads[("J2", "1")].GetPosition(); track("/VO", j2.x / 1e6, j2.y / 1e6, j2.x / 1e6, j2.y / 1e6 - 3, 0.8)
# 5. borda: trilha /VCC a 0,2 mm da borda inferior
track("/VCC", 40, 89.8, 44, 89.8, 0.5)
pcbnew.SaveBoard(str(T / "fonte_flyback_12V3A.kicad_pcb"), b)
r = subprocess.run([r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe", "pcb", "drc", "--output", str(T / "drc_teste.json"), "--format", "json", "--severity-all",
                    str(T / "fonte_flyback_12V3A.kicad_pcb")], capture_output=True, text=True)
d = json.load(open(T / "drc_teste.json", encoding="utf-8"))
regras = {}
for v in d["violations"]:
    desc = v["description"]
    for nome in ("HV_clearance", "isolacao_prim_sec", "largura_HV", "largura_SEC_potencia", "borda", "HV_pinos_mesmo_componente"):
        if f"regra '{nome}'" in desc or f"rule '{nome}'" in desc or f"'{nome}'" in desc:
            regras.setdefault(nome, []).append(desc[:100])
res = {k: len(v) for k, v in regras.items()}
print("regras disparadas na copia com violacoes deliberadas:", res)
(T / "resultado.json").write_text(json.dumps(dict(regras=regras, total=len(d["violations"])), indent=1, ensure_ascii=False), encoding="utf-8")
esperadas = ["HV_clearance", "isolacao_prim_sec", "largura_HV", "largura_SEC_potencia", "borda"]
print("faltou disparar:", [e for e in esperadas if e not in regras])
