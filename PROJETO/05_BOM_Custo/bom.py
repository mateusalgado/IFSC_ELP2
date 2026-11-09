"""Lista de materiais (BOM) com part number, fabricante, distribuidor e custo (1 un. e 100 un.) + PCI.
Gera BOM.csv, custo.csv (resumo por bloco), custo.md e custo.json; os .xlsx sao convertidos pelo LibreOffice a partir dos CSV.
Precos: referencia em USD de catalogos de distribuidores (Mouser/Digi-Key/LCSC/RS) consultados em out/2026 - conferir antes de comprar.
Cambio adotado: USD_BRL (parametro). Roda em qualquer Python 3.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
USD_BRL = 5.50
PCB_5 = 48.0        # USD: JLCPCB/PCBWay 2 camadas 140x90 mm, 5 pecas (~ $28) + frete (~ $20)
PCB_100 = 190.0     # USD: 100 pecas (~ $140) + frete

# (refs, qtd, descricao, valor/especificacao, fabricante, part number, distribuidor/codigo, bloco, USD 1 un, USD 100 un, observacao)
B = [
 ("J1", 1, "Borne a parafuso 2 vias 5,08 mm (entrada CA)", "MKDS 1,5/2-5,08", "Phoenix Contact", "1715022", "Mouser 651-1715022", "Entrada e protecoes", 0.80, 0.55, ""),
 ("F1", 1, "Fusivel 5x20 mm retardado", "T 2 A / 250 V", "Littelfuse", "0218002.MXP", "Mouser 576-0218002.MXP", "Entrada e protecoes", 0.30, 0.18, ""),
 ("F1h", 1, "Porta-fusivel 5x20 mm para PCI", "PTF/78", "Littelfuse", "64900001039", "Mouser 576-64900001039", "Entrada e protecoes", 0.45, 0.30, ""),
 ("RV1", 1, "Varistor 275 VAC disco 14 mm", "S14K275", "TDK/EPCOS", "B72214S0271K101", "Mouser 871-B72214S0271K101", "Entrada e protecoes", 0.45, 0.28, ""),
 ("RT1", 1, "Termistor NTC de inrush 10 ohm, 2 A", "10 ohm @25 C, diam. 11 mm", "Ametherm", "SL10 10002", "Digi-Key 570-1024-ND", "Entrada e protecoes", 0.65, 0.40, "alternativa: Thermometrics CL-110"),
 ("CX1", 1, "Capacitor X2 220 nF 305 VAC", "220 nF X2, passo 15 mm", "TDK/EPCOS", "B32922C3224K", "Mouser 871-B32922C3224K", "Filtro EMI", 0.55, 0.32, ""),
 ("CX2", 1, "Capacitor X2 100 nF 305 VAC", "100 nF X2, passo 15 mm", "TDK/EPCOS", "B32922C3104K", "Mouser 871-B32922C3104K", "Filtro EMI", 0.45, 0.26, ""),
 ("L1", 1, "Choke de modo comum 10 mH / 0,7 A", "WE-CMB XS 10 mH", "Wurth Elektronik", "744821110", "Mouser 710-744821110", "Filtro EMI", 3.00, 2.10, "RS/Farnell GBP 2,6-2,9"),
 ("CY1", 1, "Capacitor Y1 2,2 nF 250 VAC", "2,2 nF Y1, passo 10 mm", "Vishay", "VY1222M63Y5UQ63V0", "Mouser 594-VY1222M63Y5UQ63V0", "Filtro EMI", 0.45, 0.26, ""),
 ("R1,R2", 2, "Resistor de descarga do X2 470 kohm 1/4 W", "470 kohm 1 %", "Yageo", "MFR-25FBF52-470K", "Mouser 603-MFR-25FBF52-470K", "Filtro EMI", 0.03, 0.015, ""),
 ("BR1", 1, "Ponte retificadora 600 V / 4 A", "GBU4J", "Vishay", "GBU4J-E3/51", "Mouser 625-GBU4J-E3", "Retificador e bulk", 0.70, 0.45, ""),
 ("C1", 1, "Capacitor eletrolitico 100 uF / 400 V 105 C", "100 uF 400 V, 16x25 mm", "Nichicon", "UCY2G101MHD", "Mouser 647-UCY2G101MHD", "Retificador e bulk", 1.90, 1.30, "alt.: Rubycon 400BXW100MEFC16X35"),
 ("R3,R4", 2, "Resistor de partida 82 kohm 1 W", "82 kohm 5 % 1 W", "Vishay", "PR01000108209JR500", "Mouser 594-PR01000108209JR5", "Comando UC3845", 0.12, 0.07, ""),
 ("D2", 1, "Diodo ultrarrapido do snubber 1000 V / 1 A", "UF4007", "Vishay", "UF4007-E3/54", "Mouser 625-UF4007-E3", "Snubber RCD", 0.20, 0.09, ""),
 ("C2", 1, "Capacitor de filme 22 nF / 630 V do snubber", "22 nF 630 V, passo 10 mm", "TDK/EPCOS", "B32652A6223J", "Mouser 871-B32652A6223J", "Snubber RCD", 0.45, 0.25, ""),
 ("R5,R6", 2, "Resistor do snubber 18,2 kohm 2 W", "18,2 kohm 5 % 2 W", "Vishay", "PR02000201802JR500", "Mouser 594-PR02000201802JR5", "Snubber RCD", 0.18, 0.10, ""),
 ("Q1", 1, "MOSFET 650 V / 11 A TO-220 MDmesh M2", "STP13N65M2", "STMicroelectronics", "STP13N65M2", "Mouser 511-STP13N65M2", "Potencia primaria", 2.10, 1.45, "em falta em alguns distribuidores (out/2026): substitutos STF13N65M2 (TO-220FP), IPA65R400CE, FQPF13N65"),
 ("HS1", 1, "Dissipador clip TO-220 24 C/W", "574502B00000G", "Aavid/Boyd", "574502B00000G", "Mouser 532-574502B00000", "Potencia primaria", 0.60, 0.40, ""),
 ("ISO1", 1, "Kit isolador TO-220 (mica + bucha) + parafuso M3", "mica TO-220", "Aavid/Boyd", "4880G", "Mouser 532-4880G", "Potencia primaria", 0.30, 0.18, ""),
 ("R9,R10", 2, "Resistor de sensoriamento 0,68 ohm 1 W (2 em paralelo)", "0,68 ohm 5 % 1 W", "Vishay", "PR01000100688JR500", "Mouser 594-PR01000100688JR5", "Potencia primaria", 0.15, 0.09, "0,66 ohm calculado -> 2 x 0,68 ohm em paralelo = 0,34 ohm"),
 ("R7", 1, "Resistor de gate 10 ohm 1/4 W", "10 ohm 5 %", "Yageo", "CFR-25JB-52-10R", "Mouser 603-CFR-25JB-52-10R", "Comando UC3845", 0.02, 0.01, ""),
 ("D3", 1, "Diodo de descarga do gate", "1N4148", "onsemi", "1N4148", "Mouser 512-1N4148", "Comando UC3845", 0.05, 0.02, ""),
 ("R8", 1, "Resistor gate-source 10 kohm", "10 kohm 5 %", "Yageo", "CFR-25JB-52-10K", "Mouser 603-CFR-25JB-52-10K", "Comando UC3845", 0.02, 0.01, ""),
 ("T1", 1, "Transformador flyback EE30/15/7, Lp = 294 uH, Np 42 / Ns 7 / Naux 9", "nucleo NEE-30/15/7 IP12R (2 pc) + carretel 10 pinos + 2 presilhas", "Thornton (BR)", "NEE-30/15/7-IP12R + CNEE-30/15/7-10P", "Thornton / lojas BR (Soldafria, Bau da Eletronica)", "Transformador", 3.50, 2.40, "alt. importada: TDK B66317G0500X187 (N87, 2 pc) + carretel B66318B1010T001; fio 23 AWG esmaltado ~15 m"),
 ("T1w", 1, "Fio esmaltado 23 AWG (0,573 mm) + fita Mylar/Kapton 10 mm", "~15 m", "diversos", "-", "lojas BR", "Transformador", 1.00, 0.60, ""),
 ("D1", 1, "Diodo Schottky duplo 100 V / 2x10 A TO-220", "STPS20H100CT", "STMicroelectronics", "STPS20H100CT", "Mouser 511-STPS20H100CT", "Secundario", 0.95, 0.60, "RS UK GBP 0,42"),
 ("HS2", 1, "Dissipador clip TO-220 24 C/W", "574502B00000G", "Aavid/Boyd", "574502B00000G", "Mouser 532-574502B00000", "Secundario", 0.60, 0.40, ""),
 ("R15", 1, "Resistor RC do diodo 15 ohm 1/2 W", "15 ohm 5 % 0,5 W", "Vishay", "SFR25H0001509JR500", "Mouser 594-SFR25H0001509JR5", "Secundario", 0.05, 0.03, ""),
 ("C9", 1, "Capacitor de filme RC do diodo 2,2 nF / 100 V", "2,2 nF 100 V", "WIMA", "FKP2D012201D00JSSD", "Mouser 505-FKP2D012201D00JSSD", "Secundario", 0.25, 0.14, "calculado 2,4 nF -> 2,2 nF comercial"),
 ("C10,C11,C12", 3, "Capacitor eletrolitico baixo ESR 1000 uF / 25 V", "Rubycon ZLH 1000 uF 25 V, 10x20", "Rubycon", "25ZLH1000MEFC10X20", "Mouser 232-25ZLH1000MEFC10X", "Secundario", 0.55, 0.32, ""),
 ("L2", 1, "Indutor do pos-filtro 3,3 uH / 4 A", "3,3 uH radial", "Bourns", "RLB0914-3R3ML", "Mouser 652-RLB0914-3R3ML", "Secundario", 0.35, 0.22, ""),
 ("C13", 1, "Capacitor eletrolitico 470 uF / 25 V", "Rubycon ZLH 470 uF 25 V, 10x12,5", "Rubycon", "25ZLH470MEFC10X12.5", "Mouser 232-25ZLH470MEFC10X1", "Secundario", 0.40, 0.24, ""),
 ("J2", 1, "Borne a parafuso 2 vias 5,08 mm (saida 12 V)", "MKDS 1,5/2-5,08", "Phoenix Contact", "1715022", "Mouser 651-1715022", "Secundario", 0.80, 0.55, ""),
 ("U1", 1, "Controlador PWM modo corrente", "UC3845BN DIP-8", "STMicroelectronics (ou onsemi UC3845BNG)", "UC3845BN", "Mouser 511-UC3845BN", "Comando UC3845", 0.85, 0.50, "LCSC C5175 US$ 0,47"),
 ("U1s", 1, "Soquete DIP-8", "DIP-8", "diversos", "-", "LCSC / lojas BR", "Comando UC3845", 0.15, 0.08, ""),
 ("R12", 1, "Resistor RT 6,04 kohm 1 %", "6,04 kohm 1 %", "Yageo", "MFR-25FBF52-6K04", "Mouser 603-MFR-25FBF52-6K04", "Comando UC3845", 0.03, 0.015, ""),
 ("C4", 1, "Capacitor CT 2,2 nF C0G/NP0", "2,2 nF 50 V C0G", "TDK", "FG18C0G1H222JNT06", "Mouser 810-FG18C0G1H222JNT6", "Comando UC3845", 0.20, 0.10, ""),
 ("R11", 1, "Resistor do filtro de CS 1 kohm", "1 kohm 5 %", "Yageo", "CFR-25JB-52-1K", "Mouser 603-CFR-25JB-52-1K", "Comando UC3845", 0.02, 0.01, ""),
 ("C3", 1, "Capacitor do filtro de CS 220 pF", "220 pF 50 V C0G", "TDK", "FG18C0G1H221JNT06", "Mouser 810-FG18C0G1H221JNT6", "Comando UC3845", 0.15, 0.08, ""),
 ("C6", 1, "Capacitor de desacoplamento 100 nF", "100 nF 50 V X7R", "KEMET", "C320C104K5R5TA", "Mouser 80-C320C104K5R", "Comando UC3845", 0.12, 0.06, ""),
 ("C7", 1, "Capacitor do VREF 1 uF", "1 uF 50 V X7R", "KEMET", "C330C105K5R5TA", "Mouser 80-C330C105K5R", "Comando UC3845", 0.20, 0.10, ""),
 ("C5", 1, "Capacitor do VCC 220 uF / 35 V", "220 uF 35 V 105 C", "Panasonic", "EEU-FR1V221", "Mouser 667-EEU-FR1V221", "Comando UC3845", 0.30, 0.16, ""),
 ("D4", 1, "Diodo do auxiliar 400 V / 1 A ultrarrapido", "UF4004", "Vishay", "UF4004-E3/54", "Mouser 625-UF4004-E3", "Comando UC3845", 0.18, 0.08, ""),
 ("R13", 1, "Resistor serie do auxiliar 10 ohm", "10 ohm 5 %", "Yageo", "CFR-25JB-52-10R", "Mouser 603-CFR-25JB-52-10R", "Comando UC3845", 0.02, 0.01, ""),
 ("R14", 1, "Resistor de pull-up do COMP 4,7 kohm", "4,7 kohm 5 %", "Yageo", "CFR-25JB-52-4K7", "Mouser 603-CFR-25JB-52-4K7", "Realimentacao", 0.02, 0.01, ""),
 ("C8", 1, "Capacitor do COMP 1 nF", "1 nF 50 V C0G", "TDK", "FG18C0G1H102JNT06", "Mouser 810-FG18C0G1H102JNT6", "Realimentacao", 0.15, 0.08, ""),
 ("U3", 1, "Optoacoplador CTR 100-200 %", "PC817X2NSZ9F", "Sharp", "PC817X2NSZ9F", "Mouser 852-PC817X2NSZ9F", "Realimentacao", 0.45, 0.25, ""),
 ("U2", 1, "Referencia ajustavel 2,5 V", "TL431ACLP TO-92", "Texas Instruments", "TL431ACLPR", "Mouser 595-TL431ACLP", "Realimentacao", 0.30, 0.12, ""),
 ("R16", 1, "Resistor divisor Ra 9,53 kohm 1 %", "9,53 kohm 1 %", "Yageo", "MFR-25FBF52-9K53", "Mouser 603-MFR-25FBF52-9K53", "Realimentacao", 0.03, 0.015, ""),
 ("R17", 1, "Resistor divisor Rb 2,49 kohm 1 %", "2,49 kohm 1 %", "Yageo", "MFR-25FBF52-2K49", "Mouser 603-MFR-25FBF52-2K49", "Realimentacao", 0.03, 0.015, ""),
 ("R18", 1, "Resistor do compensador Rz 47,5 kohm 1 %", "47,5 kohm 1 %", "Yageo", "MFR-25FBF52-47K5", "Mouser 603-MFR-25FBF52-47K5", "Realimentacao", 0.03, 0.015, ""),
 ("C14", 1, "Capacitor do compensador Cz 150 nF", "150 nF 50 V X7R", "KEMET", "C322C154K5R5TA", "Mouser 80-C322C154K5R", "Realimentacao", 0.15, 0.08, ""),
 ("R19", 1, "Resistor do LED do opto 2,74 kohm 1 %", "2,74 kohm 1 %", "Yageo", "MFR-25FBF52-2K74", "Mouser 603-MFR-25FBF52-2K74", "Realimentacao", 0.03, 0.015, ""),
 ("R20", 1, "Resistor de polarizacao do TL431 1 kohm", "1 kohm 5 %", "Yageo", "CFR-25JB-52-1K", "Mouser 603-CFR-25JB-52-1K", "Realimentacao", 0.02, 0.01, ""),
 ("TP1-TP11", 11, "Ponto de teste (terminal PTH)", "Keystone 5000 ou pino de header", "Keystone", "5000", "Mouser 534-5000", "Mecanica", 0.20, 0.10, "opcional: pino de header"),
 ("H1-H4", 4, "Espacador M3 x 10 mm + parafuso e porca", "M3", "diversos", "-", "lojas BR", "Mecanica", 0.15, 0.08, ""),
]

PCB_BLOCO = "PCI (2 camadas, 140x90 mm, FR-4 1,6 mm)"


def main():
    rows = []
    t1 = t100 = 0.0
    bloco = {}
    for refs, q, desc, val, fab, pn, dist, bl, p1, p100, obs in B:
        c1, c100 = q * p1, q * p100
        t1 += c1
        t100 += c100
        b = bloco.setdefault(bl, [0.0, 0.0, 0])
        b[0] += c1
        b[1] += c100
        b[2] += q
        rows.append([refs, q, desc, val, fab, pn, dist, bl, f"{p1:.2f}", f"{p100:.3f}", f"{c1:.2f}", f"{c100:.2f}", obs])
    pcb1, pcb100 = PCB_5 / 5, PCB_100 / 100
    bloco[PCB_BLOCO] = [pcb1, pcb100, 1]
    rows.append(["PCB", 1, "Placa de circuito impresso 2 camadas FR-4 1,6 mm, 140 x 90 mm, HASL sem chumbo", "fonte_flyback_12V3A (gerbers/)", "JLCPCB / PCBWay", "-",
                 "cotacao on-line com os Gerbers", PCB_BLOCO, f"{pcb1:.2f}", f"{pcb100:.3f}", f"{pcb1:.2f}", f"{pcb100:.2f}", f"5 pc = US$ {PCB_5:.0f} com frete; 100 pc = US$ {PCB_100:.0f}"])
    t1 += pcb1
    t100 += pcb100
    hdr = ["Refs", "Qtd", "Descricao", "Valor / especificacao", "Fabricante", "Part number", "Distribuidor / codigo", "Bloco",
           "US$ unit. (1)", "US$ unit. (100)", "US$ total (1 un.)", "US$ total (100 un., por fonte)", "Observacao"]
    with open(HERE / "BOM.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(hdr)
        w.writerows(rows)
        w.writerow([])
        w.writerow(["TOTAL por fonte", "", "", "", "", "", "", "", "", "", f"{t1:.2f}", f"{t100:.2f}",
                    f"R$ {t1 * USD_BRL:.2f} (1 un.) / R$ {t100 * USD_BRL:.2f} (100 un.) a US$ 1 = R$ {USD_BRL:.2f}"])
    with open(HERE / "custo.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Bloco", "Itens", "US$ (1 un.)", "US$ (100 un.)", "% (1 un.)", "R$ (1 un.)", "R$ (100 un.)"])
        for bl, (c1, c100, q) in sorted(bloco.items(), key=lambda kv: -kv[1][0]):
            w.writerow([bl, q, f"{c1:.2f}", f"{c100:.2f}", f"{100 * c1 / t1:.1f}", f"{c1 * USD_BRL:.2f}", f"{c100 * USD_BRL:.2f}"])
        w.writerow(["TOTAL", sum(b[2] for b in bloco.values()), f"{t1:.2f}", f"{t100:.2f}", "100", f"{t1 * USD_BRL:.2f}", f"{t100 * USD_BRL:.2f}"])
    md = ["# Lista de materiais e custo", "",
          f"Precos de referencia em US$ (catalogos Mouser/Digi-Key/LCSC/RS consultados em out/2026 - conferir antes da compra); cambio adotado US$ 1 = R$ {USD_BRL:.2f}.", "",
          "| Bloco | Itens | US$ (1 un.) | US$ (100 un.) | % |", "|---|---|---|---|---|"]
    for bl, (c1, c100, q) in sorted(bloco.items(), key=lambda kv: -kv[1][0]):
        md.append(f"| {bl} | {q} | {c1:.2f} | {c100:.2f} | {100 * c1 / t1:.1f} |")
    md.append(f"| **Total por fonte** | {sum(b[2] for b in bloco.values())} | **{t1:.2f}** (R$ {t1 * USD_BRL:.0f}) | **{t100:.2f}** (R$ {t100 * USD_BRL:.0f}) | 100 |")
    md += ["", "## BOM completa", "", "| Refs | Qtd | Descricao | Part number | Fabricante | Distribuidor | US$ un. (1) | US$ un. (100) | Obs. |",
           "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[5]} | {r[4]} | {r[6]} | {r[8]} | {r[9]} | {r[12]} |")
    (HERE / "custo.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(dict(total_1=t1, total_100=t100, usd_brl=USD_BRL, n_itens=len(rows),
                   blocos={k: dict(usd1=v[0], usd100=v[1], itens=v[2]) for k, v in bloco.items()}),
              open(HERE / "custo.json", "w"), indent=1)
    print(f"itens: {len(rows)}  total 1 un.: US$ {t1:.2f} (R$ {t1 * USD_BRL:.0f})  100 un.: US$ {t100:.2f}/un. (R$ {t100 * USD_BRL:.0f})")
    for bl, (c1, c100, q) in sorted(bloco.items(), key=lambda kv: -kv[1][0]):
        print(f"  {bl:45} {c1:6.2f}  {c100:6.2f}  {100 * c1 / t1:5.1f} %")


if __name__ == "__main__":
    main()
