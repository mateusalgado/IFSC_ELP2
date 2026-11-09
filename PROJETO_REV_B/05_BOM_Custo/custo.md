# Lista de materiais e custo

Orçamento de engenharia em US$: preços herdados da A e provisões B para componentes trocados, sem cotação de compra; cambio adotado US$ 1 = R$ 5.50.

| Bloco | Itens | US$ (1 un.) | US$ (100 un.) | % |
|---|---|---|---|---|
| PCI (2 camadas, 140x90 mm, FR-4 1,6 mm) | 1 | 9.60 | 1.90 | 22.5 |
| Filtro EMI | 6 | 6.01 | 3.87 | 14.1 |
| Secundario | 10 | 5.05 | 3.14 | 11.8 |
| Transformador | 2 | 4.50 | 3.00 | 10.5 |
| Retificador e bulk | 2 | 3.90 | 2.55 | 9.1 |
| Potencia primaria | 4 | 3.10 | 2.08 | 7.3 |
| Entrada e protecoes | 6 | 3.00 | 1.88 | 7.0 |
| Mecanica | 17 | 2.80 | 1.42 | 6.6 |
| Comando UC3845 | 16 | 2.55 | 1.38 | 6.0 |
| Realimentacao | 10 | 1.21 | 0.61 | 2.8 |
| Snubber RCD | 4 | 1.01 | 0.54 | 2.4 |
| **Total por fonte** | 78 | **42.73** (R$ 235) | **22.37** (R$ 123) | 100 |

## BOM completa

| Refs | Qtd | Descricao | Part number | Fabricante | Distribuidor | US$ un. (1) | US$ un. (100) | Obs. |
|---|---|---|---|---|---|---|---|---|
| J1 | 1 | Borne a parafuso 2 vias 5,08 mm (entrada CA) | 1715022 | Phoenix Contact | Mouser 651-1715022 | 0.80 | 0.550 |  |
| F1 | 1 | Fusível cerâmico 5 × 20 mm de ação lenta (em porta-fusível de clipes) | 0215002.MXP | Littelfuse | Mouser 576-0215002.MXP | 0.60 | 0.350 | Rev. B (05/11): porta-fusível no protótipo para trocar sem dessoldar nos ensaios; em produto, fusível axial soldado 477 (US$ 2,00). Conferir Icc e curva tempo-corrente. |
| F1h | 2 | Clipe para fusível 5 × 20 mm, PTH (par) | 3517 | Keystone | Mouser 534-3517 | 0.25 | 0.150 | Rev. B (05/11): footprint Fuseholder_Clip-5x20mm_Keystone_3517; alternativa nacional: clipe 5 mm de loja |
| JP1,JP2 | 2 | Laço de fio para sonda de corrente (fase da rede; secundário de T1) | - | diversos | fio de sobra (lojas BR) | 0.00 | 0.000 | Rev. B (05/11), Aula 08: pontos de medida de corrente no protótipo; em produto, fio curto rente à placa ou trilha |
| RV1 | 1 | Varistor 275 VAC disco 14 mm | B72214S0271K101 | TDK/EPCOS | Mouser 871-B72214S0271K101 | 0.45 | 0.280 |  |
| RT1 | 1 | Termistor NTC de inrush 10 ohm, 2 A | SL10 10002 | Ametherm | Digi-Key 570-1024-ND | 0.65 | 0.400 | alternativa: Thermometrics CL-110 |
| CX1 | 1 | Capacitor X2 220 nF 305 VAC | B32922C3224K | TDK/EPCOS | Mouser 871-B32922C3224K | 0.55 | 0.320 |  |
| CX2 | 1 | Capacitor X2 100 nF 305 VAC | B32922C3104K | TDK/EPCOS | Mouser 871-B32922C3104K | 0.45 | 0.260 |  |
| L1 | 1 | Choke de modo comum | RN214-1.2-02-10M | TE / Schaffner | Schaffner série RN | 4.50 | 3.000 | Orçamento B. Rdc 195 mΩ por enrolamento. Pinos 1-2 e 3-4; pontos em 1 e 3. |
| CY1 | 1 | Capacitor Y1 2,2 nF 500 VAC | VY1222M63Y5UQ63V0 | Vishay | Mouser 594-VY1222M63Y5UQ63V0 | 0.45 | 0.260 |  |
| R1,R2 | 2 | Resistor de descarga do X2 470 kohm 1/4 W | MFR-25FBF52-470K | Yageo | Mouser 603-MFR-25FBF52-470K | 0.03 | 0.015 |  |
| BR1 | 1 | Ponte retificadora 600 V / 4 A | GBU4J-E3/51 | Vishay | Mouser 625-GBU4J-E3 | 0.70 | 0.450 |  |
| C1 | 1 | Capacitor eletrolítico de barramento | UCY2G151MHD | Nichicon | Nichicon UCY | 3.20 | 2.100 | Orçamento B. Avaliar ondulação por frequência e temperatura. |
| R3,R4 | 2 | Resistor de partida 82 kohm 1 W | PR01000108209JR500 | Vishay | Mouser 594-PR01000108209JR5 | 0.12 | 0.070 |  |
| D2 | 1 | Diodo ultrarrapido do snubber 1000 V / 1 A | UF4007-E3/54 | Vishay | Mouser 625-UF4007-E3 | 0.20 | 0.090 |  |
| C2 | 1 | Capacitor de filme 22 nF / 630 V do snubber | B32652A6223J | TDK/EPCOS | Mouser 871-B32652A6223J | 0.45 | 0.250 |  |
| R5,R6 | 2 | Resistor do snubber 18 kohm 2 W | PR02000201802JR500 | Vishay | Mouser 594-PR02000201802JR5 | 0.18 | 0.100 | Paralelo: 9 kΩ, 4 W nominais no conjunto. |
| Q1 | 1 | MOSFET 650 V / 11 A TO-220FP (encapsulamento isolado) MDmesh M2 | STF13N65M2 | STMicroelectronics | Mouser 511-STF13N65M2 | 2.20 | 1.500 | Rev. B: versao isolada (dissipador clip sem potencial do dreno). Mesmo die do STP13N65M2 usado no modelo LTspice. Substitutos: IPA65R400CE (TO-220FP), FCPF190N65S3 |
| HS1 | 1 | Dissipador clip TO-220 24 C/W | 574502B00000G | Aavid/Boyd | Mouser 532-574502B00000 | 0.60 | 0.400 |  |
| ISO1 | 0 | Kit isolador TO-220 (mica + bucha) - nao necessario com Q1 em TO-220FP | 4880G | Aavid/Boyd | Mouser 532-4880G | 0.30 | 0.180 | Rev. B: quantidade 0; manter so se Q1 voltar a TO-220 metalico |
| R9,R10 | 2 | Resistor de sensoriamento 0,68 ohm 1 W (2 em paralelo) | ROX1SJR68 | TE Connectivity | TE ROX | 0.15 | 0.090 | 2 x 0,68 ohm em paralelo = 0,34 ohm |
| R7 | 1 | Resistor de gate 10 ohm 1/4 W | CFR-25JB-52-10R | Yageo | Mouser 603-CFR-25JB-52-10R | 0.02 | 0.010 |  |
| D3 | 1 | Diodo de descarga do gate | 1N4148 | onsemi | Mouser 512-1N4148 | 0.05 | 0.020 |  |
| R8 | 1 | Resistor gate-source 10 kohm | CFR-25JB-52-10K | Yageo | Mouser 603-CFR-25JB-52-10K | 0.02 | 0.010 |  |
| T1 | 1 | Transformador flyback EE30/15/7, Lp = 294 uH, Np 42 / Ns 7 / Naux 9 | NEE-30/15/7-IP12R + CNEE-30/15/7-10P | Thornton (BR) | Thornton / lojas BR (Soldafria, Bau da Eletronica) | 3.50 | 2.400 | alt. importada: TDK B66317G0500X187 (N87, 2 pc) + carretel B66318B1010T001; fio 23 AWG esmaltado ~15 m |
| T1w | 1 | Fio esmaltado 23 AWG (0,573 mm) + fita Mylar/Kapton 10 mm | - | diversos | lojas BR | 1.00 | 0.600 |  |
| D1 | 1 | Diodo Schottky duplo 100 V / 2x10 A TO-220 | STPS20H100CT | STMicroelectronics | Mouser 511-STPS20H100CT | 0.95 | 0.600 | RS UK GBP 0,42 |
| HS2 | 1 | Dissipador clip TO-220 24 C/W | 574502B00000G | Aavid/Boyd | Mouser 532-574502B00000 | 0.60 | 0.400 |  |
| R15 | 1 | Resistor RC do diodo 15 ohm 1/2 W | SFR25H0001509JR500 | Vishay | Mouser 594-SFR25H0001509JR5 | 0.05 | 0.030 |  |
| C9 | 1 | Capacitor de filme RC do diodo 2,2 nF / 100 V | FKP2D012201D00JSSD | WIMA | Mouser 505-FKP2D012201D00JSSD | 0.25 | 0.140 | 2,2 nF instalado e simulado |
| C10,C11,C12 | 3 | Capacitor eletrolitico baixo ESR 1000 uF / 25 V | 25ZLH1000MEFC10X20 | Rubycon | Mouser 232-25ZLH1000MEFC10X | 0.55 | 0.320 |  |
| L2 | 1 | Indutor do pos-filtro 3,3 uH / 3,6 A típ. | RLB0914-3R3ML | Bourns | Mouser 652-RLB0914-3R3ML | 0.35 | 0.220 |  |
| C13 | 1 | Capacitor eletrolitico 470 uF / 25 V | 25ZLH470MEFC10X12.5 | Rubycon | Mouser 232-25ZLH470MEFC10X1 | 0.40 | 0.240 |  |
| J2 | 1 | Borne a parafuso 2 vias 5,08 mm (saida 12 V) | 1715022 | Phoenix Contact | Mouser 651-1715022 | 0.80 | 0.550 |  |
| U1 | 1 | Controlador PWM modo corrente | UC3845BN | STMicroelectronics (ou onsemi UC3845BNG) | Mouser 511-UC3845BN | 0.85 | 0.500 | LCSC C5175 US$ 0,47 |
| U1s | 1 | Soquete DIP-8 | - | diversos | LCSC / lojas BR | 0.15 | 0.080 |  |
| R12 | 1 | Resistor RT 6,04 kohm 1 % | MFR-25FBF52-6K04 | Yageo | Mouser 603-MFR-25FBF52-6K04 | 0.03 | 0.015 |  |
| C4 | 1 | Capacitor CT 2,2 nF C0G/NP0 | FG18C0G1H222JNT06 | TDK | Mouser 810-FG18C0G1H222JNT6 | 0.20 | 0.100 |  |
| R11 | 1 | Resistor do filtro de CS 330 ohm | CFR-25JB-52-330R | Yageo | Mouser 603-CFR-25JB-52-330R | 0.02 | 0.010 |  |
| C3 | 1 | Capacitor do filtro de CS 100 pF | FG18C0G1H101JNT06 | TDK | Mouser 810-FG18C0G1H101JNT6 | 0.15 | 0.080 |  |
| C6 | 1 | Capacitor de desacoplamento 100 nF | C320C104K5R5TA | KEMET | Mouser 80-C320C104K5R | 0.12 | 0.060 |  |
| C7 | 1 | Capacitor do VREF 1 uF | C330C105K5R5TA | KEMET | Mouser 80-C330C105K5R | 0.20 | 0.100 |  |
| C5 | 1 | Capacitor do VCC 220 uF / 35 V | EEU-FR1V221 | Panasonic | Mouser 667-EEU-FR1V221 | 0.30 | 0.160 |  |
| D4 | 1 | Diodo do auxiliar 400 V / 1 A ultrarrapido | UF4004-E3/54 | Vishay | Mouser 625-UF4004-E3 | 0.18 | 0.080 |  |
| R13 | 1 | Resistor serie do auxiliar 100 ohm (hiccup no curto) | CFR-25JB-52-100R | Yageo | Mouser 603-CFR-25JB-52-100R | 0.02 | 0.010 | Rev. B: 10 -> 100 ohm para o VCC cair no curto-circuito e o UC3845 desligar por UVLO |
| R14 | 1 | Resistor de pull-up do COMP 4,7 kohm | CFR-25JB-52-4K7 | Yageo | Mouser 603-CFR-25JB-52-4K7 | 0.02 | 0.010 |  |
| C8 | 1 | Capacitor do COMP 1 nF | FG18C0G1H102JNT06 | TDK | Mouser 810-FG18C0G1H102JNT6 | 0.15 | 0.080 |  |
| U3 | 1 | Optoacoplador CTR 100-200 % | PC817X2NSZ9F | Sharp | Mouser 852-PC817X2NSZ9F | 0.45 | 0.250 |  |
| U2 | 1 | Referencia ajustavel 2,5 V | TL431ACLPR | Texas Instruments | Mouser 595-TL431ACLP | 0.30 | 0.120 |  |
| R16 | 1 | Resistor divisor Ra 9,53 kohm 1 % | MFR-25FBF52-9K53 | Yageo | Mouser 603-MFR-25FBF52-9K53 | 0.03 | 0.015 |  |
| R17 | 1 | Resistor divisor Rb 2,49 kohm 1 % | MFR-25FBF52-2K49 | Yageo | Mouser 603-MFR-25FBF52-2K49 | 0.03 | 0.015 |  |
| R18 | 1 | Resistor do compensador Rz 21,5 kohm 1 % | MFR-25FBF52-21K5 | Yageo | Mouser 603-MFR-25FBF52-21K5 | 0.03 | 0.015 |  |
| C14 | 1 | Capacitor do compensador Cz 270 nF | C322C274K5R5TA | KEMET | Mouser 80-C322C274K5R | 0.15 | 0.080 |  |
| R19 | 1 | Resistor do LED do opto 2,74 kohm 1 % | MFR-25FBF52-2K74 | Yageo | Mouser 603-MFR-25FBF52-2K74 | 0.03 | 0.015 |  |
| R20 | 1 | Resistor de polarizacao do TL431 1 kohm | CFR-25JB-52-1K | Yageo | Mouser 603-CFR-25JB-52-1K | 0.02 | 0.010 |  |
| TP1-TP11 | 11 | Ponto de teste (terminal PTH) | 5000 | Keystone | Mouser 534-5000 | 0.20 | 0.100 | opcional: pino de header |
| H1-H4 | 4 | Espacador M3 x 10 mm + parafuso e porca | - | diversos | lojas BR | 0.15 | 0.080 |  |
| PCB | 1 | Placa de circuito impresso 2 camadas FR-4 1,6 mm, 140 x 90 mm, HASL sem chumbo | - | JLCPCB / PCBWay | cotacao on-line com os Gerbers | 9.60 | 1.900 | 5 pc = US$ 48 com frete; 100 pc = US$ 190 |
