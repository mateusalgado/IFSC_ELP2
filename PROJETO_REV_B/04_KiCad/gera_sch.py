"""Gera o esquematico KiCad (fonte_flyback_12V3A.kicad_sch) da fonte flyback 12 V / 3 A com UC3845,
a partir dos valores finais de 02_Calculos/resultados/*.json.

Convencoes:
  - coordenadas em mm, grade de 1,27 mm; folha A3 paisagem;
  - simbolos das bibliotecas oficiais do KiCad 10 (embutidos em lib_symbols) + simbolo proprio do transformador;
  - transformacao biblioteca (Y para cima) -> esquema (Y para baixo) e rotacao CCW (como no KiCad);
  - ligacoes de potencia por fios; nos de controle por labels locais; terras por simbolos de alimentacao
    PGND (primario) e SGND (secundario).
Saida: fonte_flyback_12V3A.kicad_sch, fonte_flyback_12V3A.kicad_pro, fonte.kicad_sym, sym-lib-table, fp-lib-table,
       netlist_componentes.json
"""
import json
import math
import uuid
from pathlib import Path

from sexp import parse, dumps, QStr, find, find_all, load_symbol, symbol_pins

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "02_Calculos" / "resultados"
LIB = Path("C:/Program Files/KiCad/10.0/share/kicad/symbols") if __import__("os").name=="nt" else Path("/mnt/c/Program Files/KiCad/10.0/share/kicad/symbols")
PROJ = "fonte_flyback_12V3A"
ROOT_UUID = "0f4e2c6a-3b1d-4e0a-9c2d-5a6b7c8d9e01"


def j(name):
    return json.loads((RES / f"{name}.json").read_text(encoding="utf-8"))


ent, fb, tr, sd, sn, uc, sc, cp, em = (j(n) for n in ("entrada", "flyback", "trafo", "saida", "snubber", "uc3845", "semicondutores", "compensador", "emi"))


def U():
    return QStr(str(uuid.uuid4()))


def eng(x, unit):
    if x >= 1e6:
        s = f"{x/1e6:g}M"
    elif x >= 1e3:
        s = f"{x/1e3:g}k"
    elif x >= 1:
        s = f"{x:g}"
    elif x >= 1e-3:
        s = f"{x*1e3:g}m"
    elif x >= 1e-6:
        s = f"{x*1e6:g}u"
    elif x >= 1e-9:
        s = f"{x*1e9:g}n"
    else:
        s = f"{x*1e12:g}p"
    return s + unit


# ------------------------------------------------------------------ footprints
FP = dict(
    R="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",
    R1W="Resistor_THT:R_Axial_DIN0411_L9.9mm_D3.6mm_P12.70mm_Horizontal",
    R2W="Resistor_THT:R_Axial_DIN0414_L11.9mm_D4.5mm_P15.24mm_Horizontal",
    C_cer="Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm",
    C_cer_hv="Capacitor_THT:C_Disc_D7.5mm_W5.0mm_P10.00mm",
    C_Y="Capacitor_THT:C_Disc_D9.0mm_W5.0mm_P10.00mm",
    C_X2="Capacitor_THT:C_Rect_L18.0mm_W8.0mm_P15.00mm_FKS3_FKP3",
    C_film="Capacitor_THT:C_Rect_L7.0mm_W2.5mm_P5.00mm",
    CP_bulk="Capacitor_THT:CP_Radial_D18.0mm_P7.50mm",
    CP_out="Capacitor_THT:CP_Radial_D10.0mm_P5.00mm",
    CP_vcc="Capacitor_THT:CP_Radial_D8.0mm_P3.50mm",
    D41="Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal",
    D35="Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal",
    TO220="Package_TO_SOT_THT:TO-220-3_Vertical",
    TO92="fonte:TL431_TI_LP",
    DIP8="Package_DIP:DIP-8_W7.62mm",
    DIP4="Package_DIP:DIP-4_W7.62mm",
    GBU="Diode_THT:Diode_Bridge_Vishay_GBU",
    FUSE="Fuse:Fuseholder_Clip-5x20mm_Keystone_3517_Inline_P23.11x6.76mm_D1.70mm_Horizontal",   # porta-fusivel (clipes) no prototipo
    JP="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",   # laco de fio para sonda de corrente
    MOV="Varistor:RV_Disc_D12mm_W4.2mm_P7.5mm",
    NTC="Capacitor_THT:C_Disc_D9.0mm_W5.0mm_P7.50mm",
    CM="Inductor_THT:Choke_Schaffner_RN214-04-15.5x23.0mm",
    L_pos="Inductor_THT:L_Radial_D7.0mm_P3.00mm",
    TERM="TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal",
    TP="TestPoint:TestPoint_THTPad_D2.0mm_Drill1.0mm",
    HOLE="MountingHole:MountingHole_3.2mm_M3",
    TRAFO="fonte:Trafo_EE30_10pin",
)

# ------------------------------------------------------------------ valores finais
R_SN2 = 2 * sn["R"]
VAL = dict(
    F1="T 2A 250V 5x20", JP1="fio (I ca)", JP2="fio (I sec)", RV1="S14K275", RT1="NTC 10R", CX1=eng(em["C_X"], "F") + " X2", CX2=eng(em["C_X2"], "F") + " X2",
    L1="10mH CM", BR1="GBU4J", C1=eng(ent["C"], "F") + " 400V", R1="470k", R2="470k",
    R3="82k 1W", R4="82k 1W", T1="EE30/15/7 Np42 Ns7 Na9",
    D2="UF4007", C2=eng(sn["C"], "F") + " 630V", R5=eng(R_SN2, "") + " 2W", R6=eng(R_SN2, "") + " 2W",
    Q1="STF13N65M2", R7=eng(uc["driver"]["R_G"], ""), D3="1N4148", R8="10k", R9=eng(2 * uc["sense"]["RS"], "") + " 1W", R10=eng(2 * uc["sense"]["RS"], "") + " 1W",
    R11="330R", C3="100p", U1="UC3845", R12=eng(uc["oscilador"]["RT"], ""), C4=eng(uc["oscilador"]["CT"], "F"),
    C5=eng(uc["partida"]["C_vcc"], "F") + " 35V", C6="100n", C7="1u", D4="UF4004", R13=eng(uc["partida"]["R_aux"], "R"), R14=eng(cp["Rpu"], ""), C8=eng(cp["Cp"], "F"),
    D1="STPS20H100CT", R15=eng(sn["rc_diodo"]["R"], ""), C9=eng(sn["rc_diodo"]["C"], "F") + " 100V",
    C10="1000u 25V", C11="1000u 25V", C12="1000u 25V", L2=eng(sd["L_pos"], "H"), C13=eng(sd["C_pos"], "F") + " 25V",
    R16=eng(cp["Ra"], ""), R17=eng(cp["Rb"], ""), U2="TL431", R18=eng(cp["Rz"], ""), C14=eng(cp["Cz"], "F"),
    R19=eng(cp["Rled"], ""), R20=eng(cp["R_bias"], ""), U3="PC817", CY1=eng(em["C_Y"], "F") + " Y1",
    J1="ENTRADA CA", J2="SAIDA 12V",
)

# ------------------------------------------------------------------ simbolos
_cache = {}


def lib_sym(lib, name):
    key = f"{lib}:{name}"
    if key in _cache:
        return _cache[key]
    sym = load_symbol(LIB / f"{lib}.kicad_sym", name)
    ext = find(sym, "extends")
    if ext:
        base = parse(dumps(load_symbol(LIB / f"{lib}.kicad_sym", ext[1])))[0]
        base[1] = QStr(name)
        for sub in find_all(base, "symbol"):
            sub[1] = QStr(sub[1].replace(ext[1], name, 1))
        props = {p[1]: p for p in find_all(base, "property")}
        for p in find_all(sym, "property"):
            if p[1] in props:
                props[p[1]][2] = p[2]
            else:
                base.append(p)
        sym = base
    sym = parse(dumps(sym))[0]
    sym[1] = QStr(key)
    _cache[key] = sym
    return sym


def tl431_symbol():
    part = parse(dumps(lib_sym("Reference_Voltage","TL431LP")))[0]
    part[1] = QStr("fonte:TL431_TI_LP")
    for unit in find_all(part, "symbol"):
        unit[1] = QStr(str(unit[1]).replace("TL431LP","TL431_TI_LP"))
        for pin in find_all(unit,"pin"):
            number=find(pin,"number")
            number[1] = QStr({"1":"3","2":"2","3":"1"}[str(number[1])])
    return part

def trafo_symbol():
    """simbolo proprio: primario (esq.), secundario (dir., cima; 2 pinos por terminal) e auxiliar (dir., baixo).
    Pontos: P1 (primario, lado do bulk), S1 (secundario, lado do SGND), A1 (auxiliar, lado do PGND)."""
    pins = [  # numero, nome, x, y (Y para cima), rot
        ("1", "P1", -10.16, 7.62, 0), ("2", "PT", -10.16, 0, 0), ("3", "P2", -10.16, -7.62, 0),
        ("9", "S2", 10.16, 10.16, 180), ("10", "S2b", 10.16, 7.62, 180), ("6", "S1", 10.16, 2.54, 180), ("7", "S1b", 10.16, 0, 180),
        ("5", "A2", 10.16, -7.62, 180), ("4", "A1", 10.16, -12.7, 180), ("8", "SH", 0, -15.24, 90),
    ]
    body = [
        "symbol", QStr("fonte:T_Flyback"),
        ["pin_names", ["offset", 1.016]], ["exclude_from_sim", "no"], ["in_bom", "yes"], ["on_board", "yes"],
        ["property", QStr("Reference"), QStr("T"), ["at", 0, 17.78, 0], ["effects", ["font", ["size", 1.27, 1.27]]]],
        ["property", QStr("Value"), QStr("T_Flyback"), ["at", 0, -17.78, 0], ["effects", ["font", ["size", 1.27, 1.27]]]],
        ["property", QStr("Footprint"), QStr(FP["TRAFO"]), ["at", 0, 0, 0], ["hide", "yes"], ["effects", ["font", ["size", 1.27, 1.27]]]],
        ["property", QStr("Datasheet"), QStr(""), ["at", 0, 0, 0], ["hide", "yes"], ["effects", ["font", ["size", 1.27, 1.27]]]],
    ]
    g = ["symbol", QStr("T_Flyback_0_1")]

    def stroke():
        return ["stroke", ["width", 0.254], ["type", "default"]]

    def coil(x, y0, y1, n, dirn):
        step = (y1 - y0) / n
        for k in range(n):
            ya, yb = y0 + k * step, y0 + (k + 1) * step
            g.append(["arc", ["start", x, ya], ["mid", x + dirn * abs(step) / 2, (ya + yb) / 2], ["end", x, yb], stroke(), ["fill", ["type", "none"]]])
    coil(-2.54, 7.62, -7.62, 6, -1)        # primario
    coil(2.54, 10.16, 2.54, 3, 1)          # secundario
    coil(2.54, -7.62, -12.7, 2, 1)         # auxiliar
    for x in (-0.508, 0.508):
        g.append(["polyline", ["pts", ["xy", x, 12.7], ["xy", x, -13.97]], stroke(), ["fill", ["type", "none"]]])
    for (x0, y0, x1, y1) in [(-7.62, 7.62, -2.54, 7.62), (-7.62, -7.62, -2.54, -7.62), (-7.62, 0, -5.08, 0),
                             (7.62, 10.16, 2.54, 10.16), (7.62, 7.62, 7.62, 10.16), (7.62, 2.54, 2.54, 2.54), (7.62, 0, 7.62, 2.54),
                             (7.62, -7.62, 2.54, -7.62), (7.62, -12.7, 2.54, -12.7)]:
        g.append(["polyline", ["pts", ["xy", x0, y0], ["xy", x1, y1]], stroke(), ["fill", ["type", "none"]]])
    for (x, y) in [(-3.81, 8.89), (3.81, 1.27), (3.81, -13.97)]:
        g.append(["circle", ["center", x, y], ["radius", 0.381], stroke(), ["fill", ["type", "outline"]]])
    body.append(g)
    p = ["symbol", QStr("T_Flyback_1_1")]
    for num, nm, x, y, rot in pins:
        p.append(["pin", "passive", "line", ["at", x, y, rot], ["length", 2.54], ["name", QStr(nm), ["effects", ["font", ["size", 1.0, 1.0]]]],
                  ["number", QStr(num), ["effects", ["font", ["size", 1.0, 1.0]]]]])
    body.append(p)
    return body


# ------------------------------------------------------------------ esquematico
class Sch:
    def __init__(self):
        self.items = []
        self.libs = {}
        self.inst = {}
        self.comps = []
        self.nflag = 0

    def place(self, ref, lib_id, value, footprint, x, y, rot=0, lib_node=None, in_bom=True):
        if lib_node is None:
            lib, name = lib_id.split(":")
            lib_node = lib_sym(lib, name)
        self.libs.setdefault(lib_id, lib_node)
        pins = symbol_pins(lib_node)
        th = math.radians(rot)
        pos = {}
        for p in pins:
            qx, qy = p["x"], -p["y"]
            sx = x + qx * math.cos(th) + qy * math.sin(th)
            sy = y - qx * math.sin(th) + qy * math.cos(th)
            pos[p["number"]] = (round(sx, 2), round(sy, 2))
        self.inst[ref] = dict(lib_id=lib_id, at=(x, y), rot=rot, pins=pos)
        if rot in (0, 180):
            pr, pv, prot, just = (x + 2.54, y - 1.27), (x + 2.54, y + 1.27), 0, [["justify", "left"]]
        else:
            pr, pv, prot, just = (x, y - 3.3), (x, y + 3.3), (360 - rot) % 360, []
        hide_ref = [["hide", "yes"]] if ref.startswith("#") else []
        sym = ["symbol", ["lib_id", QStr(lib_id)], ["at", x, y, rot], ["unit", 1], ["exclude_from_sim", "no"], ["in_bom", "yes" if in_bom else "no"],
               ["on_board", "yes"], ["dnp", "no"], ["uuid", U()],
               ["property", QStr("Reference"), QStr(ref), ["at", pr[0], pr[1], prot]] + hide_ref + [["effects", ["font", ["size", 1.27, 1.27]]] + just],
               ["property", QStr("Value"), QStr(value), ["at", pv[0], pv[1], prot], ["effects", ["font", ["size", 1.0, 1.0]]] + just],
               ["property", QStr("Footprint"), QStr(footprint), ["at", x, y, 0], ["hide", "yes"], ["effects", ["font", ["size", 1.27, 1.27]]]],
               ["property", QStr("Datasheet"), QStr(""), ["at", x, y, 0], ["hide", "yes"], ["effects", ["font", ["size", 1.27, 1.27]]]]]
        for p in pins:
            sym.append(["pin", QStr(p["number"]), ["uuid", U()]])
        sym.append(["instances", ["project", QStr(PROJ), ["path", QStr("/" + ROOT_UUID), ["reference", QStr(ref)], ["unit", 1]]]])
        self.items.append(sym)
        if in_bom:
            self.comps.append(dict(ref=ref, value=value, footprint=footprint, lib_id=lib_id))
        return self

    def pin(self, ref, num):
        return self.inst[ref]["pins"][str(num)]

    def wire(self, *pts):
        for a, b in zip(pts[:-1], pts[1:]):
            if a == b:
                continue
            assert a[0] == b[0] or a[1] == b[1], f"fio diagonal {a} -> {b}"
            self.items.append(["wire", ["pts", ["xy", a[0], a[1]], ["xy", b[0], b[1]]], ["stroke", ["width", 0.1524], ["type", "default"]], ["uuid", U()]])
        return self

    def junction(self, p):
        self.items.append(["junction", ["at", p[0], p[1]], ["diameter", 0], ["color", 0, 0, 0, 0], ["uuid", U()]])

    def label(self, name, p, rot=0):
        just = {0: ["justify", "left", "bottom"], 180: ["justify", "right", "bottom"], 90: ["justify", "left", "bottom"], 270: ["justify", "right", "bottom"]}[rot]
        self.items.append(["label", QStr(name), ["at", p[0], p[1], rot], ["effects", ["font", ["size", 1.27, 1.27]], just], ["uuid", U()]])

    def text(self, s, x, y, size=2.0, bold=False):
        eff = ["effects", ["font", ["size", size, size]] + ([["bold", "yes"]] if bold else []), ["justify", "left", "bottom"]]
        self.items.append(["text", QStr(s), ["exclude_from_sim", "no"], ["at", x, y, 0], eff, ["uuid", U()]])

    def nc(self, p):
        self.items.append(["no_connect", ["at", p[0], p[1]], ["uuid", U()]])

    def power(self, net, x, y, rot=0):
        self.nflag += 1
        self.place(f"#PWR{self.nflag:02d}", "power:GND", net, "", x, y, rot, in_bom=False)

    def flag(self, x, y):
        self.nflag += 1
        self.place(f"#FLG{self.nflag:02d}", "power:PWR_FLAG", "PWR_FLAG", "", x, y, 0, in_bom=False)

    def dump(self):
        libs = ["lib_symbols"] + list(self.libs.values())
        doc = ["kicad_sch", ["version", 20260101], ["generator", QStr("eeschema")], ["generator_version", QStr("10.0")], ["uuid", QStr(ROOT_UUID)],
               ["paper", QStr("A3")],
               ["title_block", ["title", QStr("Fonte chaveada flyback 12 V / 3 A - UC3845")], ["date", QStr("2026-11-05")], ["rev", QStr("B")],
                ["company", QStr("IFSC - Eletronica de Potencia II - Mateus Salgado Barboza Costa")]],
               libs] + self.items + [["sheet_instances", ["path", QStr("/"), ["page", QStr("1")]]]]
        return dumps(doc)


def build():
    s = Sch()
    tsym = trafo_symbol()
    P = s.pin
    # ============================ ENTRADA ============================
    s.place("J1", "Connector:Screw_Terminal_01x02", VAL["J1"], FP["TERM"], 25.4, 60.96, 180)   # pinos a direita: 1 (30.48,60.96) 2 (30.48,58.42)
    s.place("F1", "Device:Fuse", VAL["F1"], FP["FUSE"], 45.72, 53.34, 90)
    s.place("JP1", "Jumper:Jumper_2_Bridged", VAL["JP1"], FP["JP"], 55.88, 53.34, 180)   # laco de fio em serie com a fase (sonda de corrente)
    s.place("RT1", "Device:Thermistor_NTC", VAL["RT1"], FP["NTC"], 45.72, 71.12, 90)
    s.place("RV1", "Device:Varistor", VAL["RV1"], FP["MOV"], 60.96, 62.23, 0)
    s.place("CX1", "Device:C", VAL["CX1"], FP["C_X2"], 71.12, 62.23, 0)
    s.place("R1", "Device:R", VAL["R1"], FP["R"], 81.28, 58.42, 0)
    s.place("R2", "Device:R", VAL["R2"], FP["R"], 81.28, 66.04, 0)
    s.place("L1", "Device:L_Coupled", VAL["L1"], FP["CM"], 96.52, 62.23, 0)
    s.place("CX2", "Device:C", VAL["CX2"], FP["C_X2"], 111.76, 62.23, 0)
    s.place("BR1", "Device:D_Bridge_+AA-", VAL["BR1"], FP["GBU"], 127.0, 62.23, 90)            # rot 90: + cima, - baixo, CA esq/dir
    s.place("C1", "Device:C_Polarized", VAL["C1"], FP["CP_bulk"], 144.78, 71.12, 0)
    s.place("R3", "Device:R", VAL["R3"], FP["R1W"], 152.4, 86.36, 0)
    s.place("R4", "Device:R", VAL["R4"], FP["R1W"], 152.4, 99.06, 0)
    # snubber, trafo, MOSFET
    s.place("R5", "Device:R", VAL["R5"], FP["R2W"], 157.48, 60.96, 0)
    s.place("R6", "Device:R", VAL["R6"], FP["R2W"], 165.1, 60.96, 0)
    s.place("C2", "Device:C", VAL["C2"], FP["C_cer_hv"], 170.18, 60.96, 0)
    s.place("D2", "Device:D", VAL["D2"], FP["D41"], 177.8, 78.74, 270)                           # K em cima, A embaixo
    s.place("T1", "fonte:T_Flyback", VAL["T1"], FP["TRAFO"], 198.12, 71.12, 0, lib_node=tsym)
    s.place("Q1", "Transistor_FET:Q_NMOS_GDS", VAL["Q1"], FP["TO220"], 185.42, 104.14, 0)
    s.place("R7", "Device:R", VAL["R7"], FP["R"], 170.18, 104.14, 90)
    s.place("D3", "Device:D", VAL["D3"], FP["D35"], 170.18, 96.52, 0)                            # horizontal: K esq, A dir
    s.place("R8", "Device:R", VAL["R8"], FP["R"], 177.8, 114.3, 0)
    s.place("R9", "Device:R", VAL["R9"], FP["R1W"], 187.96, 127.0, 0)
    s.place("R10", "Device:R", VAL["R10"], FP["R1W"], 195.58, 127.0, 0)
    # secundario
    s.place("D1", "Device:D_Schottky_Dual_CommonCathode_AKA", VAL["D1"], FP["TO220"], 231.14, 55.88, 0)
    s.inst["D1"]["at"] = (231.14, 55.88)
    s.place("JP2", "Jumper:Jumper_2_Bridged", VAL["JP2"], FP["JP"], 215.9, 55.88, 90)     # laco de fio em serie com o secundario (sonda de corrente)
    s.place("R15", "Device:R", VAL["R15"], FP["R"], 226.06, 43.18, 90)
    s.place("C9", "Device:C", VAL["C9"], FP["C_film"], 236.22, 43.18, 90)
    s.place("C10", "Device:C_Polarized", VAL["C10"], FP["CP_out"], 251.46, 73.66, 0)
    s.place("C11", "Device:C_Polarized", VAL["C11"], FP["CP_out"], 261.62, 73.66, 0)
    s.place("C12", "Device:C_Polarized", VAL["C12"], FP["CP_out"], 271.78, 73.66, 0)
    s.place("L2", "Device:L", VAL["L2"], FP["L_pos"], 284.48, 60.96, 90)
    s.place("C13", "Device:C_Polarized", VAL["C13"], FP["CP_out"], 297.18, 73.66, 0)
    s.place("J2", "Connector:Screw_Terminal_01x02", VAL["J2"], FP["TERM"], 320.04, 58.42, 0)     # pinos a esquerda: 1 (314.96,58.42) 2 (314.96,60.96)
    # ============================ CONTROLE ============================
    s.place("U1", "Regulator_Controller:UC3845_DIP8", VAL["U1"], FP["DIP8"], 111.76, 165.1, 0)
    s.place("R12", "Device:R", VAL["R12"], FP["R"], 81.28, 157.48, 0)
    s.place("C4", "Device:C", VAL["C4"], FP["C_cer"], 81.28, 180.34, 0)
    s.place("C7", "Device:C", VAL["C7"], FP["C_cer"], 73.66, 157.48, 0)
    s.place("R14", "Device:R", VAL["R14"], FP["R"], 76.2, 140.97, 0)
    s.place("C8", "Device:C", VAL["C8"], FP["C_cer"], 63.5, 152.4, 0)
    s.place("U3", "Isolator:PC817", VAL["U3"], FP["DIP4"], 40.64, 170.18, 0)
    s.place("R11", "Device:R", VAL["R11"], FP["R"], 137.16, 170.18, 90)
    s.place("C3", "Device:C", VAL["C3"], FP["C_cer"], 147.32, 180.34, 0)
    s.place("C5", "Device:C_Polarized", VAL["C5"], FP["CP_vcc"], 134.62, 139.7, 0)
    s.place("C6", "Device:C", VAL["C6"], FP["C_cer"], 142.24, 139.7, 0)
    s.place("R13", "Device:R", VAL["R13"], FP["R"], 152.4, 132.08, 90)
    s.place("D4", "Device:D", VAL["D4"], FP["D41"], 162.56, 132.08, 0)                           # K esq, A dir
    # ============================ REALIMENTACAO ============================
    s.place("R16", "Device:R", VAL["R16"], FP["R"], 292.1, 215.9, 0)
    s.place("R17", "Device:R", VAL["R17"], FP["R"], 292.1, 243.84, 0)
    s.place("U2", "fonte:TL431_TI_LP", VAL["U2"], FP["TO92"], 271.78, 236.22, 0,lib_node=tl431_symbol())
    s.place("R18", "Device:R", VAL["R18"], FP["R"], 281.94, 228.6, 90)
    s.place("C14", "Device:C", VAL["C14"], FP["C_cer"], 271.78, 220.98, 90)
    s.place("R19", "Device:R", VAL["R19"], FP["R"], 248.92, 210.82, 0)
    s.place("R20", "Device:R", VAL["R20"], FP["R"], 238.76, 228.6, 0)
    s.place("CY1", "Device:C", VAL["CY1"], FP["C_Y"], 215.9, 182.88, 0)
    # pontos de teste e furos
    TPS = [("BULK", 139.7, 40.64), ("DRAIN", 198.12, 96.52), ("SW", 198.12, 116.84), ("GATE", 177.8, 93.98),
           ("VCC", 119.38, 139.7), ("VREF", 73.66, 180.34), ("COMP", 55.88, 152.4), ("CS", 139.7, 180.34),
           ("PGND", 127.0, 190.5), ("VO", 307.34, 48.26), ("SGND", 307.34, 83.82)]
    for i, (nm, x, y) in enumerate(TPS, start=1):
        s.place(f"TP{i}", "Connector:TestPoint", nm, FP["TP"], x, y, 0, in_bom=False)
    for i, (x, y) in enumerate([(360.68, 220.98), (370.84, 220.98), (360.68, 231.14), (370.84, 231.14)], start=1):
        s.place(f"H{i}", "Mechanical:MountingHole", "M3", FP["HOLE"], x, y, 0, in_bom=False)

    # ---------------------------------------------------------------- ENTRADA (fios)
    j1a, j1b = P("J1", 1), P("J1", 2)          # pino 2 (cima) = L, pino 1 (baixo) = N
    f1a, f1b = P("F1", 1), P("F1", 2)
    rt1a, rt1b = P("RT1", 1), P("RT1", 2)
    s.wire(j1b, (j1b[0], f1a[1]), f1a)
    s.wire(j1a, (j1a[0], rt1a[1]), rt1a)
    topy, boty = f1b[1], rt1b[1]
    rv1, rv2 = P("RV1", 1), P("RV1", 2)
    s.wire(f1b, (50.8, topy))                      # F1 -> JP1 (pinos em 50,8 e 60,96)
    s.wire((rv1[0], topy), rv1); s.wire(rt1b, (rv2[0], boty), rv2)
    cx1a, cx1b = P("CX1", 1), P("CX1", 2)
    s.wire((cx1a[0], topy), cx1a); s.wire((cx1b[0], boty), cx1b)
    r1a, r1b, r2a, r2b = P("R1", 1), P("R1", 2), P("R2", 1), P("R2", 2)
    s.wire((r1a[0], topy), r1a); s.wire(r1b, r2a); s.wire(r2b, (r2b[0], boty))
    l1_1, l1_2, l1_3, l1_4 = P("L1", 1), P("L1", 2), P("L1", 3), P("L1", 4)
    s.wire((rv1[0], topy), (l1_1[0], topy), l1_1)
    s.wire((rv2[0], boty), (l1_3[0], boty), l1_3)
    for p in ((rv1[0], topy), (rv2[0], boty), (cx1a[0], topy), (cx1b[0], boty), (r1a[0], topy), (r2b[0], boty)):
        s.junction(p)
    cx2a, cx2b = P("CX2", 1), P("CX2", 2)
    s.wire(l1_2, (cx2a[0], l1_2[1]), cx2a); s.wire(l1_4, (cx2b[0], l1_4[1]), cx2b)
    s.junction((cx2a[0], l1_2[1])); s.junction((cx2b[0], l1_4[1]))
    # ponte (rot 90): + cima, - baixo, CA esquerda (pino 2) e direita (pino 3)
    brp, brac_l, brac_r, brm = P("BR1", 1), P("BR1", 2), P("BR1", 3), P("BR1", 4)
    s.wire((cx2a[0], l1_2[1]), (brac_l[0] - 2.54, l1_2[1]), (brac_l[0] - 2.54, brac_l[1]), brac_l)
    s.wire(cx2b, (cx2b[0], 76.2), (brac_r[0] + 2.54, 76.2), (brac_r[0] + 2.54, brac_r[1]), brac_r)
    bulky = 48.26
    c1a, c1b = P("C1", 1), P("C1", 2)
    s.wire(brp, (brp[0], bulky), (c1a[0], bulky), c1a); s.junction((c1a[0], bulky))
    s.wire(brm, (brm[0], 72.39), (c1b[0], 72.39), c1b)
    s.wire(c1b, (c1b[0], 99.06)); s.power("PGND", c1b[0], 99.06)
    s.wire((c1b[0], 93.98), (c1b[0] + 5.08, 93.98)); s.junction((c1b[0], 93.98)); s.flag(c1b[0] + 5.08, 93.98)
    # startup
    r3a, r3b, r4a, r4b = P("R3", 1), P("R3", 2), P("R4", 1), P("R4", 2)
    s.wire((c1a[0], bulky), (r3a[0], bulky), r3a); s.junction((r3a[0], bulky))
    s.wire(r3b, r4a); s.wire(r4b, (r4b[0], r4b[1] + 2.54)); s.label("VCC", (r4b[0], r4b[1] + 2.54), 270)
    # snubber RCD
    r5a, r5b, r6a, r6b = P("R5", 1), P("R5", 2), P("R6", 1), P("R6", 2)
    c2a, c2b = P("C2", 1), P("C2", 2)
    d2k, d2a = P("D2", 1), P("D2", 2)
    snuby = 71.12
    s.wire((r3a[0], bulky), (r5a[0], bulky), r5a); s.junction((r5a[0], bulky))
    s.wire((r6a[0], bulky), r6a); s.junction((r6a[0], bulky))
    s.wire(r5b, (r5b[0], snuby), (r6b[0], snuby)); s.junction((r6b[0], snuby))
    s.wire(r6b, (r6b[0], snuby), (d2k[0], snuby), d2k); s.junction((c2b[0], snuby))
    s.wire((r5a[0], bulky), (c2a[0], bulky), c2a); s.junction((c2a[0], bulky))
    s.wire(c2b, (c2b[0], snuby))
    s.text("Snubber RCD", 158.75, 45.72, 1.5)
    # trafo primario
    t1p1, t1pt, t1p2 = P("T1", 1), P("T1", 2), P("T1", 3)
    s.nc(t1pt)
    s.wire((c2a[0], bulky), (t1p1[0] - 5.08, bulky), (t1p1[0] - 5.08, t1p1[1]), t1p1)
    drain_x = t1p2[0] - 7.62
    qg, qd, qs = P("Q1", 1), P("Q1", 2), P("Q1", 3)
    s.wire(t1p2, (drain_x, t1p2[1]), (drain_x, 96.52), (qd[0], 96.52), qd)
    s.wire((drain_x, d2a[1] + 3.81), (d2a[0], d2a[1] + 3.81), d2a); s.junction((drain_x, d2a[1] + 3.81))
    # gate: Rg + diodo antiparalelo + Rgs ; sensor
    r7a, r7b = P("R7", 1), P("R7", 2)
    d3k, d3a = P("D3", 1), P("D3", 2)
    s.wire(r7b, qg); s.junction(qg)
    s.wire(r7a, (r7a[0] - 2.54, r7a[1])); s.label("DRV", (r7a[0] - 2.54, r7a[1]), 180)
    s.wire(d3k, (r7a[0], d3k[1]), r7a); s.wire(d3a, (r7b[0], d3a[1]), r7b); s.junction(r7a)
    r8a, r8b = P("R8", 1), P("R8", 2)
    s.wire(r8a, (r8a[0], qg[1])); s.junction((r8a[0], qg[1]))
    s.wire(qs, (qs[0], 120.65)); s.junction((qs[0], 111.76)); s.junction((qs[0], 120.65))
    s.wire(r8b, (r8b[0], 120.65), (qs[0], 120.65))
    s.wire((qs[0], 111.76), (qs[0] + 5.08, 111.76)); s.label("SW", (qs[0] + 5.08, 111.76))
    r9a, r9b, r10a, r10b = P("R9", 1), P("R9", 2), P("R10", 1), P("R10", 2)
    s.wire((qs[0], 120.65), r9a); s.wire(r9a, (r10a[0], r9a[1]), r10a); s.junction(r9a)
    s.wire(r9b, (r10b[0], r9b[1]), r10b); s.junction(r9b)
    s.wire(r9b, (r9b[0], r9b[1] + 2.54)); s.power("PGND", r9b[0], r9b[1] + 2.54)
    s.wire(qg, (qg[0], qg[1] - 5.08)); s.label("GATE", (qg[0], qg[1] - 5.08), 90)
    s.text("Rsense 2 x 0,66 ohm (1 W)", 203.2, 135.89, 1.5)
    s.text("JP1/JP2: lacos de fio para sonda de corrente (Aula 08)", 20.32, 45.72, 1.3)
    # ---------------------------------------------------------------- SECUNDARIO
    t1s2, t1s2b, t1s1, t1s1b, t1a2, t1a1, t1sh = P("T1", 9), P("T1", 10), P("T1", 6), P("T1", 7), P("T1", 5), P("T1", 4), P("T1", 8)
    s.nc(t1sh)
    d1a1, d1k, d1a2 = P("D1", 1), P("D1", 2), P("D1", 3)
    secx = t1s2[0] + 7.62
    sgx = t1s2[0] + 10.16
    # S2/S2b -> SECN -> anodos do diodo
    # S2/S2b -> JP2 (laco p/ sonda de corrente, pinos em y = 60,96 e 50,8) -> anodos do diodo
    s.wire(t1s2, (secx, t1s2[1])); s.wire(t1s2b, (secx, t1s2b[1]), (secx, t1s2[1])); s.junction((secx, t1s2[1]))
    s.wire((secx, 50.8), (secx, 48.26))
    s.wire(d1a1, (d1a1[0] - 2.54, d1a1[1]), (d1a1[0] - 2.54, 48.26)); s.junction((d1a1[0] - 2.54, 48.26))
    s.wire(d1a2, (d1a2[0] + 2.54, d1a2[1]), (d1a2[0] + 2.54, 48.26), (secx, 48.26)); s.junction((secx, 48.26))
    # RC do diodo acima
    r15a, r15b, c9a, c9b = P("R15", 1), P("R15", 2), P("C9", 1), P("C9", 2)
    s.wire((secx, 48.26), (secx, r15a[1]), r15a); s.wire(r15b, c9a)
    vouty = d1k[1]
    s.wire(c9b, (c9b[0] + 3.81, c9b[1]), (c9b[0] + 3.81, vouty)); s.junction((c9b[0] + 3.81, vouty))
    s.wire(d1k, (c9b[0] + 3.81, vouty))
    # S1/S1b (ponto) -> SGND
    s.wire(t1s1, (sgx, t1s1[1])); s.wire(t1s1b, (sgx, t1s1b[1])); s.junction((sgx, t1s1b[1]))
    s.wire((sgx, t1s1[1]), (sgx, 91.44)); s.junction((sgx, 91.44))
    s.wire((sgx, 91.44), (sgx, 93.98)); s.power("SGND", sgx, 93.98)
    # auxiliar: A2 -> AUX (label), A1 (ponto) -> PGND
    s.wire(t1a2, (t1a2[0] + 5.08, t1a2[1])); s.label("AUX", (t1a2[0] + 5.08, t1a2[1]))
    s.wire(t1a1, (t1a1[0] + 5.08, t1a1[1]), (t1a1[0] + 5.08, 91.44)); s.power("PGND", t1a1[0] + 5.08, 91.44)
    # banco de capacitores + LC + saida
    for ref in ("C10", "C11", "C12"):
        a, b = P(ref, 1), P(ref, 2)
        s.wire((a[0], vouty), a); s.wire(b, (b[0], 91.44)); s.junction((a[0], vouty)); s.junction((b[0], 91.44))
    s.wire((c9b[0] + 3.81, vouty), (P("C12", 1)[0], vouty))
    l2a, l2b = P("L2", 1), P("L2", 2)
    s.wire((P("C12", 1)[0], vouty), l2a)
    c13a, c13b = P("C13", 1), P("C13", 2)
    s.wire(l2b, (c13a[0], vouty), c13a); s.junction((c13a[0], vouty))
    s.wire(c13b, (c13b[0], 91.44)); s.junction((c13b[0], 91.44))
    s.wire((sgx, 91.44), (c13b[0], 91.44))
    j2a, j2b = P("J2", 1), P("J2", 2)
    s.wire((c13a[0], vouty), (c13a[0] + 5.08, vouty), (c13a[0] + 5.08, 53.34), (j2a[0] - 2.54, 53.34), (j2a[0] - 2.54, j2a[1]), j2a)
    s.wire(j2b, (j2b[0] - 5.08, j2b[1]), (j2b[0] - 5.08, 91.44), (c13b[0], 91.44))
    s.label("VO", (c13a[0] + 5.08, 53.34), 0)
    s.wire((c13b[0], 91.44), (c13b[0], 96.52)); s.power("SGND", c13b[0], 96.52)
    s.wire((c13b[0], 93.98), (c13b[0] + 5.08, 93.98)); s.junction((c13b[0], 93.98)); s.flag(c13b[0] + 5.08, 93.98)
    s.text("3 x 1000 uF ZLH + filtro LC", 251.46, 87.63, 1.5)
    # ---------------------------------------------------------------- CONTROLE (fios)
    comp, fbp, cs, rc, gnd, out, vcc, vref = (P("U1", n) for n in ("1", "2", "3", "4", "5", "6", "7", "8"))
    s.wire(gnd, (gnd[0], gnd[1] + 5.08)); s.power("PGND", gnd[0], gnd[1] + 5.08)
    s.wire(fbp, (fbp[0] - 5.08, fbp[1])); s.power("PGND", fbp[0] - 5.08, fbp[1], 270)
    s.wire(out, (out[0] + 5.08, out[1])); s.label("DRV", (out[0] + 5.08, out[1]))
    # VREF: sobe pela esquerda ate y = 149.86 e vai para RT, C_ref e label
    vrefy = 149.86
    r12a, r12b, c4a, c4b = P("R12", 1), P("R12", 2), P("C4", 1), P("C4", 2)
    c7a, c7b = P("C7", 1), P("C7", 2)
    s.wire(vref, (91.44, vref[1]), (91.44, vrefy), (c7a[0], vrefy))
    s.wire(r12a, (r12a[0], vrefy)); s.junction((r12a[0], vrefy))
    s.wire(c7a, (c7a[0], vrefy)); s.wire((c7a[0], vrefy), (c7a[0] - 5.08, vrefy)); s.label("VREF", (c7a[0] - 5.08, vrefy), 180); s.junction((c7a[0], vrefy))
    s.wire(c7b, (c7b[0], c7b[1] + 2.54)); s.power("PGND", c7b[0], c7b[1] + 2.54)
    # RC: RT (baixo) e CT
    s.wire(rc, (r12b[0], rc[1])); s.wire(r12b, (r12b[0], rc[1])); s.junction((r12b[0], rc[1]))
    s.wire((r12b[0], rc[1]), c4a)
    s.wire(c4b, (c4b[0], c4b[1] + 2.54)); s.power("PGND", c4b[0], c4b[1] + 2.54)
    # COMP: sobe em x = 96.52 ate y = 147.32, segue para a esquerda (pull-up, Cp, opto)
    compy = 147.32
    r14a, r14b, c8a, c8b = P("R14", 1), P("R14", 2), P("C8", 1), P("C8", 2)
    o1, o2, o3, o4 = P("U3", 1), P("U3", 2), P("U3", 3), P("U3", 4)
    s.wire(comp, (96.52, comp[1]), (96.52, compy), (50.8, compy))
    s.wire(r14b, (r14b[0], compy)); s.junction((r14b[0], compy))
    s.wire(r14a, (r14a[0], r14a[1] - 2.54)); s.label("VREF", (r14a[0], r14a[1] - 2.54), 90)
    s.wire(c8a, (c8a[0], compy)); s.junction((c8a[0], compy))
    s.wire(c8b, (c8b[0], c8b[1] + 2.54)); s.power("PGND", c8b[0], c8b[1] + 2.54)
    s.wire(o4, (50.8, o4[1]), (50.8, compy))
    s.wire(o3, (50.8, o3[1]), (50.8, o3[1] + 5.08)); s.power("PGND", 50.8, o3[1] + 5.08)
    s.wire(o1, (o1[0] - 2.54, o1[1])); s.label("LEDA", (o1[0] - 2.54, o1[1]), 180)
    s.wire(o2, (o2[0] - 2.54, o2[1])); s.label("KA", (o2[0] - 2.54, o2[1]), 180)
    s.label("COMP", (88.9, compy), 0)
    s.text("isolacao", 40.64, 160.02, 1.5)
    # CS: filtro RC
    r11a, r11b, c3a, c3b = P("R11", 1), P("R11", 2), P("C3", 1), P("C3", 2)
    s.wire(cs, r11a)
    s.wire(r11b, (r11b[0] + 5.08, r11b[1])); s.label("SW", (r11b[0] + 5.08, r11b[1]))
    s.wire(c3a, (c3a[0], c3a[1] - 2.54)); s.label("CS", (c3a[0], c3a[1] - 2.54))
    s.wire(c3b, (c3b[0], c3b[1] + 2.54)); s.power("PGND", c3b[0], c3b[1] + 2.54)
    s.label("CS", (127.0, cs[1]), 0)
    # VCC: C5, C6, auxiliar, flag
    c5a, c5b, c6a, c6b = P("C5", 1), P("C5", 2), P("C6", 1), P("C6", 2)
    vccy = c5a[1] - 2.54
    s.wire(vcc, (vcc[0], vccy), (146.05, vccy))
    s.label("VCC", (vcc[0], vcc[1] - 5.08), 90)
    s.wire(c5a, (c5a[0], vccy)); s.wire(c6a, (c6a[0], vccy)); s.junction((c5a[0], vccy)); s.junction((c6a[0], vccy))
    s.wire(c5b, (c5b[0], c5b[1] + 2.54)); s.power("PGND", c5b[0], c5b[1] + 2.54)
    s.wire(c6b, (c6b[0], c5b[1] + 2.54), (c5b[0], c5b[1] + 2.54)); s.junction((c5b[0], c5b[1] + 2.54))
    s.wire((124.46, vccy), (124.46, vccy - 5.08)); s.junction((124.46, vccy)); s.flag(124.46, vccy - 5.08)
    r13a, r13b, d4k, d4a = P("R13", 1), P("R13", 2), P("D4", 1), P("D4", 2)
    s.wire((146.05, vccy), (146.05, r13a[1]), r13a)
    s.wire(r13b, d4k)
    s.wire(d4a, (d4a[0] + 2.54, d4a[1])); s.label("AUX", (d4a[0] + 2.54, d4a[1]))
    s.text("VCC pelo auxiliar (15 V) + partida por R3/R4", 128.27, 123.19, 1.3)
    # ---------------------------------------------------------------- REALIMENTACAO (fios)
    ra1, ra2, rb1, rb2 = P("R16", 1), P("R16", 2), P("R17", 1), P("R17", 2)
    tref, ta, tk = P("U2", 3), P("U2", 2), P("U2", 1)
    rz1, rz2, cz1, cz2 = P("R18", 1), P("R18", 2), P("C14", 1), P("C14", 2)
    s.wire(ra1, (ra1[0], ra1[1] - 2.54)); s.label("VO", (ra1[0], ra1[1] - 2.54), 90)
    s.wire(ra2, rb1)
    refy = 229.87
    s.wire((ra2[0], refy), (tref[0], refy), tref); s.junction((ra2[0], refy))
    s.wire(rz2, (ra2[0], rz2[1])); s.junction((ra2[0], rz2[1]))
    s.wire(rb2, (rb2[0], rb2[1] + 2.54)); s.power("SGND", rb2[0], rb2[1] + 2.54)
    s.wire(ta, (ta[0] - 2.54, ta[1]), (ta[0] - 2.54, ta[1] + 5.08)); s.power("SGND", ta[0] - 2.54, ta[1] + 5.08)
    s.wire(cz2, (rz1[0], cz2[1]), rz1)
    kx = tk[0] + 2.54
    kay = 248.92
    s.wire(cz1, (262.89, cz1[1]), (262.89, kay), (kx, kay), (kx, tk[1]), tk)
    s.label("KA", (kx, kay), 270)
    rl1, rl2, rbias1, rbias2 = P("R19", 1), P("R19", 2), P("R20", 1), P("R20", 2)
    s.wire(rl1, (rl1[0], rl1[1] - 2.54)); s.label("VO", (rl1[0], rl1[1] - 2.54), 90)
    s.wire(rl2, (rl2[0], 222.25), (rbias1[0], 222.25), rbias1); s.junction((rbias1[0], 222.25))
    s.wire((rbias1[0], 222.25), (rbias1[0] - 5.08, 222.25)); s.label("LEDA", (rbias1[0] - 5.08, 222.25), 180)
    s.wire(rbias2, (rbias2[0], rbias2[1] + 2.54), (rbias2[0] - 5.08, rbias2[1] + 2.54)); s.label("KA", (rbias2[0] - 5.08, rbias2[1] + 2.54), 180)
    s.text("Realimentacao: TL431 + PC817 (compensador tipo 2)", 238.76, 200.66, 1.5)
    # Y cap
    cy1, cy2 = P("CY1", 1), P("CY1", 2)
    s.wire(cy1, (cy1[0], cy1[1] - 5.08)); s.power("PGND", cy1[0], cy1[1] - 5.08, 180)
    s.wire(cy2, (cy2[0], cy2[1] + 5.08)); s.power("SGND", cy2[0], cy2[1] + 5.08)
    s.text("Y1 primario-secundario", 205.74, 198.12, 1.3)
    # pontos de teste
    for i, (nm, x, y) in enumerate(TPS, start=1):
        p = P(f"TP{i}", 1)
        s.wire(p, (p[0], p[1] + 2.54))
        if nm in ("PGND", "SGND"):
            s.power(nm, p[0], p[1] + 2.54)
        else:
            s.label(nm, (p[0], p[1] + 2.54), 270)
    s.label("DRAIN", (drain_x, 96.52), 270)
    s.label("BULK", (brp[0] - 2.54, bulky), 180)
    s.wire((brp[0], bulky), (brp[0] - 2.54, bulky))
    # textos
    s.text("ENTRADA, PROTECOES E FILTRO DE EMI", 30.48, 38.1, 2.0, True)
    s.text("RETIFICADOR + BULK", 116.84, 30.48, 2.0, True)
    s.text("FLYBACK", 190.5, 22.86, 2.0, True)
    s.text("SAIDA 12 V / 3 A", 266.7, 30.48, 2.0, True)
    s.text("CONTROLE UC3845 (modo corrente de pico, 65 kHz)", 63.5, 121.92, 2.0, True)
    s.text("Fonte chaveada flyback 12 V / 3 A  -  Vin 90-264 VAC  -  UC3845  -  IFSC EPO II 2026-2  -  Mateus S. B. Costa", 20.32, 270.0, 2.5, True)
    return s


if __name__ == "__main__":
    s = build()
    (HERE / f"{PROJ}.kicad_sch").write_text(s.dump(), encoding="utf-8")
    lib = ["kicad_symbol_lib", ["version", 20241209], ["generator", QStr("kicad_symbol_editor")], ["generator_version", QStr("9.0")]]
    t = parse(dumps(trafo_symbol()))[0]; t[1] = QStr("T_Flyback")
    lib.append(t)
    u=tl431_symbol(); u[1]=QStr("TL431_TI_LP"); lib.append(u)
    (HERE / "fonte.kicad_sym").write_text(dumps(lib), encoding="utf-8")
    pro = {"board": {"design_settings": {}, "layer_presets": [], "viewports": []}, "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
           "meta": {"filename": f"{PROJ}.kicad_pro", "version": 3}, "net_settings": {"classes": [{"name": "Default", "clearance": 0.3, "track_width": 0.5, "via_diameter": 0.8, "via_drill": 0.4}]},
           "pcbnew": {"page_layout_descr_file": ""}, "schematic": {"legacy_lib_dir": "", "legacy_lib_list": []}, "sheets": [[ROOT_UUID, "Root"]], "text_variables": {}}
    if not (HERE / f"{PROJ}.kicad_pro").exists(): (HERE / f"{PROJ}.kicad_pro").write_text(json.dumps(pro, indent=2), encoding="utf-8")
    (HERE / "sym-lib-table").write_text('(sym_lib_table\n  (version 7)\n  (lib (name "fonte")(type "KiCad")(uri "${KIPRJMOD}/fonte.kicad_sym")(options "")(descr "simbolos do projeto"))\n)\n', encoding="utf-8")
    (HERE / "fp-lib-table").write_text('(fp_lib_table\n  (version 7)\n  (lib (name "fonte")(type "KiCad")(uri "${KIPRJMOD}/fonte.pretty")(options "")(descr "footprints do projeto"))\n)\n', encoding="utf-8")
    (HERE / "netlist_componentes.json").write_text(json.dumps(s.comps, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"ok: {len(s.comps)} componentes, {sum(1 for i in s.items if i[0]=='wire')} fios")
