"""Lista pinos (numero, nome, posicao, rotacao) dos simbolos usados no projeto."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sexp import load_symbol, symbol_pins, find

LIB = Path("/mnt/c/Program Files/KiCad/10.0/share/kicad/symbols")
SIMBOLOS = ["Device:R", "Device:C", "Device:C_Polarized", "Device:L", "Device:L_Coupled", "Device:D", "Device:D_Schottky",
            "Device:D_Zener", "Device:Fuse", "Device:Varistor", "Device:Thermistor_NTC", "Device:D_Bridge_+-AA",
            "Device:Transformer_1P_2S", "Regulator_Controller:UC3845_DIP8", "Regulator_Controller:UC3842_DIP8",
            "Isolator:PC817", "Reference_Voltage:TL431LP", "Connector:Screw_Terminal_01x02", "Connector:TestPoint",
            "Mechanical:MountingHole", "Transistor_FET:Q_NMOS_GDS", "power:GND", "power:PWR_FLAG"]
for s in SIMBOLOS:
    lib, name = s.split(":")
    try:
        sym = load_symbol(LIB / f"{lib}.kicad_sym", name)
    except Exception as e:
        print("===", s, "ERRO", e); continue
    ext = find(sym, "extends")
    pins = symbol_pins(sym)
    if ext and not pins:
        base = load_symbol(LIB / f"{lib}.kicad_sym", ext[1])
        pins = symbol_pins(base)
    print("===", s, f"(extends {ext[1]})" if ext else "")
    for p in pins:
        print(f"   pin {p['number']:>3} {p['name']:<10} at ({p['x']:6.2f},{p['y']:6.2f}) rot {p['rot']:5.0f} len {p['length']}")
