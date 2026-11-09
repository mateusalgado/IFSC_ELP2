# Verificação do layout da PCI – **Revisão B** (Aula 08, IPC-2221 e parecer técnico V1)

Placa: `fonte_flyback_12V3A.kicad_pcb` rev. B, placement revisto em 05/11/2026 antes do pedido da PCI (`ANALISE_PLACEMENT.md`) — 140 × 90 mm, dupla face, FR-4 1,6 mm, cobre 35 µm, furos metalizados, 71 footprints (todos PTH; JP1/JP2 são laços de fio), 35 redes, 364 trilhas, 6 vias.

## 1. Resultado do DRC (verificação de CAD)

`kicad-cli pcb drc --severity-all --schematic-parity --refill-zones` (`drc_B.json`): **0 erros, 0 itens não conectados, 0 divergências com o esquemático B**, 3 avisos de serigrafia:

| Aviso | Causa | Decisão |
|---|---|---|
| 2 × `silk_edge_clearance` em U3 (opto) | o corpo do PC817 cruza a fenda de isolação, por projeto (pinos 3/4 no primário, 1/2 no secundário, 7,62 mm entre fileiras) | aceito; a serigrafia do corpo não é cobre |
| 1 × `silk_over_copper` ("K" do D3 sobre o pad 1 de R8) | marcação de cátodo do footprint DO-35 junto ao pad vizinho (1,4 mm entre pads) | aceito; marcação redundante com a serigrafia de referência |

**Classes de rede atribuídas** (parecer, item 05): no `.kicad_pro` todas as redes do primário em alta tensão estão em `HV` (/BULK, /DRAIN, Net-(D2-K), Net-(BR1-Pad2/3), Net-(JP1-A/B), Net-(CX1-Pad2), Net-(J1-Pin_1/2), Net-(R1-Pad2), Net-(R3-Pad2), Net-(R5-Pad2), `unconnected-(T1-PT-Pad2)`); as do secundário em `SEC` (/KA, /LEDA, Net-(U2-REF), Net-(C14-Pad2), Net-(C9-Pad1), `unconnected-(T1-SH-Pad8)` – pino 8 tratado como **secundário** pelo lado físico do carretel) ou `SEC_PWR` (/VO, SGND, Net-(D1-K), Net-(JP2-A/B)); a regra `isolacao_prim_sec` do `.kicad_dru` inclui `SEC_PWR` e, desde 05/11, exige **6,4 mm** (IEC 62368-1, isolação reforçada, 250 V rms, grau de poluição 2, material IIIb). Sob o opto vale a exceção `isolacao_fenda_opto` (6,0 mm, limitada à área de regra `fenda_opto`): o DIP-4 tem 6,02 mm entre as fileiras de pads e a fenda de 1,2 mm interrompe a linha de fuga (IEC 60664-1, ranhura ≥ 1 mm). Sem a exceção o DRC acusa 8 violações, todas em U3 (comprovado numa cópia); o roteador limita o **cobre** do primário a x ≤ 81,2 e o do secundário a x ≥ 87,6.

**Ensaio de cobertura do DRC** (`testa_regras.py`, cópia em `teste_regras/`): com cinco violações deliberadas inseridas na cópia, cada regra disparou — `HV_clearance` (0,25 mm detectado), `isolacao_prim_sec` (2,1–3,4 mm detectados), `largura_HV` (0,5 mm), `largura_SEC_potencia` (0,8 mm), `borda` (0 mm). Resultado em `teste_regras/resultado.json`. Na placa entregue nenhuma dessas regras aponta ocorrência.

## 2. Alterações de layout da revisão B (em relação à A)

| Mudança | Motivo | Evidência |
|---|---|---|
| Esquemático B: R5 ∥ R6 (9 kΩ no grampo), filtro ISENSE 330 Ω/100 pF no pino 3 (C3 junto a U1), TL431 com footprint próprio K-A-REF, choke Schaffner RN214 (1-2 / 3-4), fusível axial 500 V, C1 150 µF (Ø18), R13 = 100 Ω, Q1 = STF13N65M2 (TO-220FP) | itens 01–04 do parecer e proteção de curto (hiccup) | `gera_sch.py`, `netlist.net`, ERC 0 |
| Barreira do roteador do secundário em x = 87,9 mm (era 86,5) | trilhas /LEDA do opto ficavam a 5,1–5,8 mm dos pinos 3/4 (primário) | DRC: 4 erros de `isolacao_prim_sec` → 0 |
| Laço SGND CY1 → U2 com 1,5 mm (era 0,8) | classe SEC_PWR exige ≥ 1,5 mm | DRC `largura_SEC_potencia` 5 → 0 |
| J1 deslocado de x = 11 para 16 mm | pads da rede ficavam a 2,5 mm do pad do furo H1 (parafuso do gabinete pode ser PE) | distância pad–furo ≥ 6 mm (verificado por script) |
| CX1 de x = 3,5 para 6,5 mm | pad da rede a 2,2 mm da borda (gabinete) | ≥ 3 mm da borda para todas as redes da entrada |
| D1 de y = 24 para 20 mm | afastar o dissipador do diodo dos eletrolíticos C10–C12 (vida útil) | +4 mm entre aleta e capacitores |
| J2 na borda direita (132, 70) a 90° | gabinete: entrada da rede à esquerda/alto, saída 12 V pela borda direita; cabo não cruza a placa | render 3D |
| R16/R17/R18/C14 reposicionados | abrir espaço para J2 sem sobreposição de cortejos | `placement.py` 0 problemas |
| Q1 em TO-220FP (isolado) | o dissipador clip ficava no potencial do dreno (~500 V) com o TO-220 metálico; o FP dispensa mica e deixa o clip sem tensão | `semicondutores.py`: Tj ≈ 72 °C com RθJC 3,5 °C/W |
| **05/11** J1 na borda esquerda (7, 16) a 270°, abrindo para fora; filtro de entrada em coluna (F1, JP1, RV1, RT1, R1, R2, CX1 encostado nos pinos 1/3 de L1; L1 a 270°) | Aula 08: fluxo linear; capacitor X eficaz só com ligação curta ao choke; cabos de entrada e saída em faces opostas da caixa | redes da rede de 80 para 54 mm (`comprimento_redes.txt`); pads da rede ≥ 8,5 mm dos furos e ≥ 7 mm da borda |
| **05/11** F1 em porta-fusível de clipes 5 × 20 (Keystone 3517) | trocar o fusível sem dessoldar durante os ensaios (curto, partida); produto volta ao axial soldado | esquemático/BOM; roteador trata os dois pads de cada clipe |
| **05/11** JP1 (fase, após F1) e JP2 (T1 9/10 → ânodos de D1): laços de fio de 10,16 mm | Aula 08: "em caso de protótipos, prever pontos de medida de corrente"; THD da entrada (Aula 06) e corrente de D1 | `gera_sch.py`, netlist (Net-(JP1-A/B), Net-(JP2-A/B)) |
| **05/11** Q1 de (48, 44) para (55, 48); C1 para x = 47; R3/R4, gate (R7/D3/R8), shunt (R9/R10 a 180°), D2/C2 e TP2–TP4 reacomodados | dreno a 15,7 mm do pino 3 de T1 (era 24,8); clip de Q1 a 6 mm do corpo de C1 (era 3,5; vida do eletrolítico, Aula 03) | /DRAIN 66 → 62 mm; `placement.py` 0 sobreposições |
| **05/11** C10/C11/C12 com passo 12 mm (era 11) | retrabalho dos eletrolíticos | `placement.py` |
| **05/11** Serigrafia: "F1 T2A 250V", "N"/"L" em J1, "0V"/"+12V 3A" em J2, "C1 400V DESCARREGAR" | marcação exigida junto ao fusível (IEC 62368-1) e segurança na bancada | `gera_pcb.py`; DRC sem `silk_over_copper` novo |
| **05/11** Regra `isolacao_prim_sec` 6,0 → 6,4 mm + exceção `isolacao_fenda_opto` | isolação reforçada a 250 V (IEC 62368-1) | DRC 0 erros; cópia sem a exceção: 8 violações só em U3 |

## 3. Checklist da Aula 08 (atualizado para a B)

| # | Item | Como foi atendido | Evidência |
|---|---|---|---|
| 1 | Planejamento: área, PTH, face dupla, fixação | 140 × 90 mm, 2 camadas, 4 furos M3 nos cantos (≥ 6 mm das redes da entrada), J1 na borda esquerda e J2 na direita, ambos abrindo para fora; pads da rede ≥ 8,5 mm dos furos e ≥ 7 mm da borda | render 3D, script de distâncias |
| 2 | Começar pelos maiores; quentes afastados | T1 sobre a fenda; C1 (Ø18) e L1 fixados primeiro; Q1 (1,15 W) a 14 mm de BR1; R5/R6 (2 W no total) no topo, a 10 mm de C1 e 20 mm de T1; NTC (quente) a 20 mm de C1; D1 (1,8 W) a 10 mm dos eletrolíticos de saída | `placement.py` |
| 3 | Fluxo linear | rede (J1, alto-esquerda) → EMI → ponte/bulk → Q1/T1 → D1 → capacitores → L2 → J2 (direita) | `imagens/pcb_completa.png` |
| 4 | Agrupar por função; trilhas na área | regiões A–F; roteador limita o cobre do primário a x ≤ 81,2 e o do secundário a x ≥ 87,6 (6,4 mm) | `router.py` |
| 5 | Magnéticos afastados | L1 a 70 mm de T1; L2 a 30 mm | `placement.py` |
| 6 | Sensores e analógicos junto ao CI | R9/R10 a 38 mm de T1; filtro do ISENSE (R11/C3) agora **junto ao pino 3** com retorno à ilha de terra de sinal; RT/CT, VREF, 100 nF (C6, 4,3 mm do VCC) e C8 ao redor de U1 | `placement.py` |
| 7 | **Sem trilhas a 90°** | 255 cantos chanfrados a 45°; dos 21 ângulos retos restantes, 19 são saídas de duas trilhas de um mesmo pad e 2 estão a 0,1 mm de um pad (R9.1, U1.3) | script de contagem (pcbnew) |
| 8 | Trilhas comutadas curtas | laço Q1–R9/R10–PGND com 10 mm; dreno de Q1 a 24,8 mm do pino 3 de T1 (rede /DRAIN 66 mm com snubber e TP2 — encurtável na revisão C, ver `ANALISE_PLACEMENT.md`); laço T1–D1–C10 em trilhas de 2,0 mm | `comprimento_redes.py` |
| 9 | Largura e isolamento por corrente e tensão (IPC-2221) | HV ≥ 1,0 mm e isolamento ≥ 1,0 mm (B4, 301–500 V com máscara: 0,8 mm); bulk 1,5 mm; secundário de potência 2,0 mm (5,45 A rms, ΔT < 20 °C a 35 µm); sinais 0,5 mm; borda ≥ 0,5 mm — **todas as regras verificadas pelo DRC e pelo ensaio de cobertura** | `.kicad_dru`, `drc_B.json`, `teste_regras/` |
| 10 | Isolação primário/secundário | ≥ 6,4 mm entre qualquer item SEC/SEC_PWR e o primário (DRC; exceção de 6,0 mm só sob a fenda do opto), fendas de 1,2 mm sob T1 e U3; Y1 com 10 mm de passo (8 mm entre pads); opto com 6,0 mm entre fileiras de pads | DRC |
| 11 | GND de sinal × GND de potência, ponto único | plano PGND de potência e ilha PGND de sinal unidos só pela trilha-estrela no lado frio do Rsense; roteador verifica a ilha contínua ("ilha de terra de sinal contínua: sim") | `gera_pcb.py`, `router.py` |
| 12 | Driver junto ao transistor | UC3845 comanda Q1 direto; R7/D3/R8 junto ao gate; trilha DRV sobre a ilha de terra | layout |
| 13 | Sinais de medida com retorno próximo | CS: Rsense → R11/C3 (junto a U1) sobre a ilha; realimentação na região F sobre SGND | layout |
| 14 | 100 nF no VCC do CI | C6 a 4,3 mm do pino 7 | `placement.py` |
| 15 | Datasheet do CI (§8.4 do UC3845) | bypass junto ao VCC ✔, compensação junto ao CI ✔, realimentação longe de T1 ✔, trilhas de potência ≥ 0,381 mm/A ✔ | datasheet |
| 16 | Modo diferencial / filtro MC | CX1–L1–CX2 + CY1; ida e volta do secundário lado a lado | esquemático |
| 17 | Plano de referência | PGND e SGND na face inferior (`connect_pads yes`) | `gera_pcb.py` |
| 18 | Pontos de medida | TP1 BULK, TP2 DRAIN, TP3 SW, TP4 GATE, TP5 VCC, TP6 VREF, TP7 COMP, TP8 CS, TP9 PGND, TP10 VO, TP11 SGND | esquemático |
| 19 | DFM | PTH para solda manual/onda; menor distância borda-borda entre pads de componentes diferentes 0,95 mm (U1–C8, sinal); referências posicionadas automaticamente fora dos cortejos; sem SMD → ladrões de solda não se aplicam; porta-fusível de clipes e laços JP1/JP2 para a bancada | script |
| 20 | Dissipador, fixação, inserção | clips em Q1 (isolado) e D1; furos M3; peças altas (C1 18 × 40 mm, T1, L1) agrupadas | render 3D |

## 4. Avaliação para placa de teste confiável e para produto com gabinete

**Dissipadores (necessidade, cálculo):** Q1 STF13N65M2 dissipa 1,15 W no pior caso (264 V): sem dissipador T<sub>j</sub> ≈ 112 °C (R<sub>θJA</sub> 62,5 °C/W) → **necessário**; com clip de 24 °C/W, T<sub>j</sub> ≈ 72 °C. D1 STPS20H100CT dissipa 1,78 W: sem dissipador ≈ 150 °C → **necessário**; com clip, T<sub>j</sub> ≈ 84 °C. Ponte GBU4J 0,67 W, T<sub>j</sub> ≈ 53 °C sem dissipador (fixá-la pelo furo ao gabinete em produto, opcional). R5/R6 (1,0 W cada, 2 W nominais) e R3/R4 (0,42 W cada a 264 V) aquecem: montar afastados 3 mm da placa; NTC opera quente por projeto (≈ 0,4 W em regime). Transformador ΔT 29 °C. Para gabinete fechado sem ventilação, prever ΔT interna de 15–20 °C: T<sub>j</sub> de Q1/D1 vai a ≈ 90/105 °C, ainda dentro da meta de 125 °C; em produto, substituir os clips por dissipadores de 10–12 °C/W (Same Sky HSE17) ou usar a parede do gabinete.

**Posição dos componentes (05/11):** J1 abre para a borda esquerda e J2 para a direita (cabos em faces opostas da caixa); filtro de entrada em coluna J1 → F1 → JP1 → RV1/RT1 → R1/R2 → CX1 → L1 → CX2 → BR1; Q1 a 6 mm do corpo de C1 e com o dreno a 15,7 mm do pino 3 de T1; D1 a 10 mm de C10–C12 (passo 12 mm); componentes altos (C1 40 mm, T1 ≈ 25 mm, L1 23 mm) agrupados no centro/esquerda, o que define a altura mínima interna do gabinete (≈ 45 mm); conector da rede e fusível próximos à borda de entrada; MOV e NTC junto ao conector; o lado secundário livre de componentes altos à direita (J2). Para produto: C1 em versão 18 × 35 mm ou deitado; adicionar furos para o dissipador parafusado e, se o gabinete for metálico, terminal de PE junto a J1 (classe I) ou gabinete plástico com distâncias de 6,4 mm da rede às superfícies acessíveis (classe II).

**Formato e espessura das trilhas:** todas as dobras a 45°; larguras 0,5 (sinal), 0,8 (VCC/aux), 1,0 (HV e PGND), 1,2 (rede), 1,5 (bulk), 2,0 mm (secundário de potência); nenhuma trilha de sinal cruza a ilha de terra na face inferior com mais de 6 mm (pulos curtos). Para produto com corrente de saída contínua de 3 A e picos de 13 A no secundário, 2,0 mm a 35 µm fica abaixo de 20 °C de elevação (IPC-2221); em produção em volume, cobre de 70 µm na face inferior ou trilha de 3 mm reduziria a elevação para < 10 °C. Teardrops nos pads PTH e cantos arredondados nas trilhas de 2 mm ficam como melhoria de fabricação (não gerados pelo roteador).

**Análise do posicionamento (05/11/2026):** `ANALISE_PLACEMENT.md` lista, região por região, vantagens, desvantagens e as melhorias de uma revisão C orientada a produto (bloco de controle junto a Q1/T1, filtro de entrada em linha, Q1 afastado de C1, D1 deitado, silk de segurança, 6,4 mm, jumpers de corrente), com os comprimentos de trilha medidos em `comprimento_redes.txt`.

**Pendências para um produto (fora do escopo do protótipo):** ensaio de emissões conduzidas com LISN; ensaio de rigidez dielétrica primário–secundário (3 kV) no transformador real; certificação do fusível e do MOV para a categoria de sobretensão; gabinete e proteção contra contato.

Fluxo reprodutível: `gera_sch.py` → `kicad-cli sch erc / export netlist` → `fp_info.py` → `placement.py` → `router.py` → `completa_rotas.py` (ramos /DRV e /CS por busca em grade) → `gera_pcb.py` → `kicad-cli pcb drc --refill-zones --schematic-parity` → `testa_regras.py` → `comprimento_redes.py` → exportações (`gerbers/`, `imagens/`, `3d/`). Análise de placement e revisão item a item: `ANALISE_PLACEMENT.md`.
