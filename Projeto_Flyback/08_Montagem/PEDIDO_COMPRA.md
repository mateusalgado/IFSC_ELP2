# Pedido de compra – 1 protótipo (Possibilidade II) – revisão B

Gerado de `05_BOM_Custo/BOM.csv` por `pedido_compra.py`. Quantidades = por placa + sobressalentes; preços de referência (orçamento de engenharia, out/nov 2026), sem frete nem impostos. **Total estimado: US$ 108.55 (≈ R$ 597 a R$ 5,50/US$)** — a PCI entra pelo lote mínimo de 5 placas (US$ 48 com frete).

Prioridade de compra (prazo de chegada): 1) PCI (enviar `04_KiCad/gerbers/fonte_flyback_12V3A_B_gerbers.zip`); 2) importados de prazo longo (STF13N65M2, STPS20H100CT, choke Schaffner, Rubycon ZLH, UC3845, PC817); 3) núcleo/carretel/fio (Thornton ou loja nacional); 4) passivos comuns e mecânica (loja nacional).

| Refs | Descrição | Valor | Fabricante / PN | Fornecedor | por placa | comprar | motivo | US$ |
|---|---|---|---|---|---|---|---|---|
| J1 | Borne a parafuso 2 vias 5,08 mm (entrada CA) | MKDS 1,5/2-5,08 | Phoenix Contact 1715022 | Mouser 651-1715022 | 1 | 1 |  | 0.80 |
| F1 | Fusível cerâmico 5 × 20 mm de ação lenta (em porta-fusível de clipes) | T 2 A / 250 VCA | Littelfuse 0215002.MXP | Mouser 576-0215002.MXP | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 1.20 |
| F1h | Clipe para fusível 5 × 20 mm, PTH (par) | Keystone 3517 (passo 23,11 mm) | Keystone 3517 | Mouser 534-3517 | 2 | 3 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.75 |
| JP1,JP2 | Laço de fio para sonda de corrente (fase da rede; secundário de T1) | fio 0,8 mm nu, laço de 10 mm elevado 5 mm | diversos - | fio de sobra (lojas BR) | 2 | 3 | rolo/metragem já cobre 2 trafos | 0.00 |
| RV1 | Varistor 275 VAC disco 14 mm | S14K275 | TDK/EPCOS B72214S0271K101 | Mouser 871-B72214S0271K101 | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.90 |
| RT1 | Termistor NTC de inrush 10 ohm, 2 A | 10 ohm @25 C, diam. 11 mm | Ametherm SL10 10002 | Digi-Key 570-1024-ND | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 1.30 |
| CX1 | Capacitor X2 220 nF 305 VAC | 220 nF X2, passo 15 mm | TDK/EPCOS B32922C3224K | Mouser 871-B32922C3224K | 1 | 3 | mínimo de loja / reserva | 1.65 |
| CX2 | Capacitor X2 100 nF 305 VAC | 100 nF X2, passo 15 mm | TDK/EPCOS B32922C3104K | Mouser 871-B32922C3104K | 1 | 3 | mínimo de loja / reserva | 1.35 |
| L1 | Choke de modo comum | 2 x 10 mH, 1,2 A a 40 °C, 300 VCA | TE / Schaffner RN214-1.2-02-10M | Schaffner série RN | 1 | 1 |  | 4.50 |
| CY1 | Capacitor Y1 2,2 nF 500 VAC | 2,2 nF Y1, passo 10 mm | Vishay VY1222M63Y5UQ63V0 | Mouser 594-VY1222M63Y5UQ63V0 | 1 | 3 | mínimo de loja / reserva | 1.35 |
| R1,R2 | Resistor de descarga do X2 470 kohm 1/4 W | 470 kohm 1 % | Yageo MFR-25FBF52-470K | Mouser 603-MFR-25FBF52-470K | 2 | 4 | mínimo de loja / reserva | 0.12 |
| BR1 | Ponte retificadora 600 V / 4 A | GBU4J | Vishay GBU4J-E3/51 | Mouser 625-GBU4J-E3 | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 1.40 |
| C1 | Capacitor eletrolítico de barramento | 150 µF / 400 V, 105 °C, 18 x 40 mm | Nichicon UCY2G151MHD | Nichicon UCY | 1 | 2 | reserva | 6.40 |
| R3,R4 | Resistor de partida 82 kohm 1 W | 82 kohm 5 % 1 W | Vishay PR01000108209JR500 | Mouser 594-PR01000108209JR5 | 2 | 3 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.36 |
| D2 | Diodo ultrarrapido do snubber 1000 V / 1 A | UF4007 | Vishay UF4007-E3/54 | Mouser 625-UF4007-E3 | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.40 |
| C2 | Capacitor de filme 22 nF / 630 V do snubber | 22 nF 630 V, passo 10 mm | TDK/EPCOS B32652A6223J | Mouser 871-B32652A6223J | 1 | 3 | mínimo de loja / reserva | 1.35 |
| R5,R6 | Resistor do snubber 18 kohm 2 W | 18 kohm 5 % 2 W | Vishay PR02000201802JR500 | Mouser 594-PR02000201802JR5 | 2 | 4 | mínimo de loja / reserva | 0.72 |
| Q1 | MOSFET 650 V / 11 A TO-220FP (encapsulamento isolado) MDmesh M2 | STF13N65M2 | STMicroelectronics STF13N65M2 | Mouser 511-STF13N65M2 | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 4.40 |
| HS1 | Dissipador clip TO-220 24 C/W | 574502B00000G | Aavid/Boyd 574502B00000G | Mouser 532-574502B00000 | 1 | 1 |  | 0.60 |
| ISO1 | Kit isolador TO-220 (mica + bucha) - nao necessario com Q1 em TO-220FP | mica TO-220 | Aavid/Boyd 4880G | Mouser 532-4880G | 0 | 0 |  | 0.00 |
| R9,R10 | Resistor de sensoriamento 0,68 ohm 1 W (2 em paralelo) | 0,68 ohm 5 % 1 W | TE Connectivity ROX1SJR68 | TE ROX | 2 | 4 | mínimo de loja / reserva | 0.60 |
| R7 | Resistor de gate 10 ohm 1/4 W | 10 ohm 5 % | Yageo CFR-25JB-52-10R | Mouser 603-CFR-25JB-52-10R | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.04 |
| D3 | Diodo de descarga do gate | 1N4148 | onsemi 1N4148 | Mouser 512-1N4148 | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.10 |
| R8 | Resistor gate-source 10 kohm | 10 kohm 5 % | Yageo CFR-25JB-52-10K | Mouser 603-CFR-25JB-52-10K | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.04 |
| T1 | Transformador flyback EE30/15/7, Lp = 294 uH, Np 42 / Ns 7 / Naux 9 | nucleo NEE-30/15/7 IP12R (2 pc) + carretel 10 pinos + 2 presilhas | Thornton (BR) NEE-30/15/7-IP12R + CNEE-30/15/7-10P | Thornton / lojas BR (Soldafria, Bau da Eletronica) | 1 | 3 | um para errar o enrolamento | 10.50 |
| T1w | Fio esmaltado 23 AWG (0,573 mm) + fita Mylar/Kapton 10 mm | ~15 m | diversos - | lojas BR | 1 | 3 | um para errar o enrolamento | 3.00 |
| D1 | Diodo Schottky duplo 100 V / 2x10 A TO-220 | STPS20H100CT | STMicroelectronics STPS20H100CT | Mouser 511-STPS20H100CT | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 1.90 |
| HS2 | Dissipador clip TO-220 24 C/W | 574502B00000G | Aavid/Boyd 574502B00000G | Mouser 532-574502B00000 | 1 | 1 |  | 0.60 |
| R15 | Resistor RC do diodo 15 ohm 1/2 W | 15 ohm 5 % 0,5 W | Vishay SFR25H0001509JR500 | Mouser 594-SFR25H0001509JR5 | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.10 |
| C9 | Capacitor de filme RC do diodo 2,2 nF / 100 V | 2,2 nF 100 V | WIMA FKP2D012201D00JSSD | Mouser 505-FKP2D012201D00JSSD | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.50 |
| C10,C11,C12 | Capacitor eletrolitico baixo ESR 1000 uF / 25 V | Rubycon ZLH 1000 uF 25 V, 10x20 | Rubycon 25ZLH1000MEFC10X20 | Mouser 232-25ZLH1000MEFC10X | 3 | 4 | reserva | 2.20 |
| L2 | Indutor do pos-filtro 3,3 uH / 3,6 A típ. | 3,3 uH radial, Isat típ. 11,3 A | Bourns RLB0914-3R3ML | Mouser 652-RLB0914-3R3ML | 1 | 1 |  | 0.35 |
| C13 | Capacitor eletrolitico 470 uF / 25 V | Rubycon ZLH 470 uF 25 V, 10x12,5 | Rubycon 25ZLH470MEFC10X12.5 | Mouser 232-25ZLH470MEFC10X1 | 1 | 2 | reserva | 0.80 |
| J2 | Borne a parafuso 2 vias 5,08 mm (saida 12 V) | MKDS 1,5/2-5,08 | Phoenix Contact 1715022 | Mouser 651-1715022 | 1 | 1 |  | 0.80 |
| U1 | Controlador PWM modo corrente | UC3845BN DIP-8 | STMicroelectronics (ou onsemi UC3845BNG) UC3845BN | Mouser 511-UC3845BN | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 1.70 |
| U1s | Soquete DIP-8 | DIP-8 | diversos - | LCSC / lojas BR | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.30 |
| R12 | Resistor RT 6,04 kohm 1 % | 6,04 kohm 1 % | Yageo MFR-25FBF52-6K04 | Mouser 603-MFR-25FBF52-6K04 | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.06 |
| C4 | Capacitor CT 2,2 nF C0G/NP0 | 2,2 nF 50 V C0G | TDK FG18C0G1H222JNT06 | Mouser 810-FG18C0G1H222JNT6 | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.40 |
| R11 | Resistor do filtro de CS 330 ohm | 330 ohm 5 % | Yageo CFR-25JB-52-330R | Mouser 603-CFR-25JB-52-330R | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.04 |
| C3 | Capacitor do filtro de CS 100 pF | 100 pF 50 V C0G | TDK FG18C0G1H101JNT06 | Mouser 810-FG18C0G1H101JNT6 | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.30 |
| C6 | Capacitor de desacoplamento 100 nF | 100 nF 50 V X7R | KEMET C320C104K5R5TA | Mouser 80-C320C104K5R | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.24 |
| C7 | Capacitor do VREF 1 uF | 1 uF 50 V X7R | KEMET C330C105K5R5TA | Mouser 80-C330C105K5R | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.40 |
| C5 | Capacitor do VCC 220 uF / 35 V | 220 uF 35 V 105 C | Panasonic EEU-FR1V221 | Mouser 667-EEU-FR1V221 | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.60 |
| D4 | Diodo do auxiliar 400 V / 1 A ultrarrapido | UF4004 | Vishay UF4004-E3/54 | Mouser 625-UF4004-E3 | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.36 |
| R13 | Resistor serie do auxiliar 100 ohm (hiccup no curto) | 100 ohm 5 % 1/4 W | Yageo CFR-25JB-52-100R | Mouser 603-CFR-25JB-52-100R | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.04 |
| R14 | Resistor de pull-up do COMP 4,7 kohm | 4,7 kohm 5 % | Yageo CFR-25JB-52-4K7 | Mouser 603-CFR-25JB-52-4K7 | 1 | 3 | mínimo de loja / reserva | 0.06 |
| C8 | Capacitor do COMP 1 nF | 1 nF 50 V C0G | TDK FG18C0G1H102JNT06 | Mouser 810-FG18C0G1H102JNT6 | 1 | 2 | reserva | 0.30 |
| U3 | Optoacoplador CTR 100-200 % | PC817X2NSZ9F | Sharp PC817X2NSZ9F | Mouser 852-PC817X2NSZ9F | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.90 |
| U2 | Referencia ajustavel 2,5 V | TL431ACLP TO-92 | Texas Instruments TL431ACLPR | Mouser 595-TL431ACLP | 1 | 1 |  | 0.30 |
| R16 | Resistor divisor Ra 9,53 kohm 1 % | 9,53 kohm 1 % | Yageo MFR-25FBF52-9K53 | Mouser 603-MFR-25FBF52-9K53 | 1 | 3 | mínimo de loja / reserva | 0.09 |
| R17 | Resistor divisor Rb 2,49 kohm 1 % | 2,49 kohm 1 % | Yageo MFR-25FBF52-2K49 | Mouser 603-MFR-25FBF52-2K49 | 1 | 3 | mínimo de loja / reserva | 0.09 |
| R18 | Resistor do compensador Rz 21,5 kohm 1 % | 21,5 kohm 1 % | Yageo MFR-25FBF52-21K5 | Mouser 603-MFR-25FBF52-21K5 | 1 | 3 | mínimo de loja / reserva | 0.09 |
| C14 | Capacitor do compensador Cz 270 nF | 270 nF 50 V X7R | KEMET C322C274K5R5TA | Mouser 80-C322C274K5R | 1 | 2 | reserva | 0.30 |
| R19 | Resistor do LED do opto 2,74 kohm 1 % | 2,74 kohm 1 % | Yageo MFR-25FBF52-2K74 | Mouser 603-MFR-25FBF52-2K74 | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.06 |
| R20 | Resistor de polarizacao do TL431 1 kohm | 1 kohm 5 % | Yageo CFR-25JB-52-1K | Mouser 603-CFR-25JB-52-1K | 1 | 2 | sobressalente (componente sensível a erro de montagem/ensaio) | 0.04 |
| TP1-TP11 | Ponto de teste (terminal PTH) | Keystone 5000 ou pino de header | Keystone 5000 | Mouser 534-5000 | 11 | 11 |  | 2.20 |
| H1-H4 | Espacador M3 x 10 mm + parafuso e porca | M3 | diversos - | lojas BR | 4 | 4 |  | 0.60 |
| PCB | Placa de circuito impresso 2 camadas FR-4 1,6 mm, 140 x 90 mm, HASL sem chumbo | fonte_flyback_12V3A (gerbers/) | JLCPCB / PCBWay - | cotacao on-line com os Gerbers | 1 | 5 | lote mínimo do fabricante (5 placas) | 48.00 |
| **Total** | | | | | | | | **108.55** |

## Itens fora da BOM (bancada e montagem)

| Item | Para quê | Observação |
|---|---|---|
| Resistor de fio 4,7 kΩ / 10 W com cabos isolados | descarga de C1 (10 J) | obrigatório antes de tocar na placa |
| Resistores de carga 4 Ω / 40 W e 8 Ω / 20 W (ou carga eletrônica) | 100 % e 50 % de carga | com dissipador |
| Fita de poliéster (Mylar) 10 mm, verniz/esmalte | transformador | 3 camadas entre primário e secundário |
| Soquete DIP-8 | U1 | já na BOM (mecânica) — conferir |
| Estanho 0,8 mm, fluxo, isopropílico | montagem | |
| Chave de curto com fio curto ≤ 50 mΩ | ensaio de curto (seção 5.4 do guia) | só após liberar os limites |
| Termopar ou termômetro IR | térmico de Q1, D1, R5/R6, T1 | |
| Transformador isolador, variac, sonda diferencial ≥ 700 V, multímetro CAT II 600 V, LCR, wattímetro | laboratório | confirmar disponibilidade com o professor antes de comprar |
