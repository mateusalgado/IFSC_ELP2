# Análise do posicionamento dos componentes – placa B como produto e como placa de ensaio

Data: 05/11/2026. Base: `placement.py` (coordenadas), `fonte_flyback_12V3A.kicad_pcb`, `comprimento_redes.py` → `comprimento_redes.txt` (comprimento de trilha por rede, medido no pcbnew), `imagens/pcb_completa.png`, `3d/pcb_3d_iso.png`, `VERIFICACAO_LAYOUT.md`. Referências: Aula 08 (layout e DFM), Aula 07 (fonte chaveada), Aula 03 (metodologia, vida útil de capacitores), Aula 02 (dissipadores), Tarefa Extra (roteiro de análise física de produto), Tarefas 1–3.

**Estado (05/11/2026, tarde):** as melhorias de baixo custo do §6 foram **aplicadas antes do pedido da PCI** (ver §7); o §1 descreve a placa como estava de manhã. As demais melhorias valem para uma **revisão C de layout orientada a produto**, e três delas (bloco de controle mais perto de Q1/T1, filtro de entrada em linha, dissipadores na borda) só se justificam se as medições do protótipo mostrarem o problema que elas previnem. Nada aqui foi medido; tudo é geometria [CAD] e cálculo [C].

## 1. Mapa das regiões e o que cada posição implica

Origem no canto superior esquerdo, x para a direita, y para baixo, em mm. Barreira primário/secundário em x = 84 (fenda sob T1 e U3; 6,0 mm de isolação nas demais partes).

| Região | Componentes (posição) | Vantagens | Desvantagens / risco | Melhoria proposta (C) |
|---|---|---|---|---|
| **A – entrada e EMI** (x 2–40, y 2–60) | J1 (16, 13), RV1 (28, 6), RT1 (36, 15), F1 (6, 24), CX1 (6,5, 33), R1/R2, L1 (11, 52), CX2 (12, 58), BR1 (33,5, 42) | Rede confinada ao canto superior esquerdo, a 70 mm de T1 (magnéticos afastados, Aula 08); MOV e NTC junto ao conector; pads da rede ≥ 6 mm dos furos e ≥ 3 mm da borda | O caminho da rede faz zigue-zague: J1 → F1 (esquerda) → RV1 (topo) → RT1 (direita) → CX1 (esquerda) → L1; as redes dos pads de CX1 somam **80 mm cada** [CAD]. Trilha longa entre o capacitor X e o choke degrada o filtro (indutância série do X) e aumenta a área do laço da rede | Alinhar F1 → RV1 → RT1 em coluna junto à borda esquerda e colocar CX1 encostado nos pinos de entrada de L1 (ganho estimado: redes CX1 de 80 para ≈ 35 mm). J1 na borda esquerda (rot. 90°) de frente para J2, para cabo de entrada e de saída em faces opostas da caixa |
| **B – barramento, Q1, snubber, T1** (x 40–72, y 2–60) | C1 (46, 25–32,5; Ø18 × 40 mm), Q1 (48, 44), R9/R10 (45,5, 53/58), R7/D3/R8 (37–43, 50), R5/R6 (58, 6/13), D2/C2 (57–70, 20), R3/R4 (62, 24/41), T1 (84, 44) | Laço fonte → R9/R10 → PGND curto (10 mm); gate R7/D3/R8 encostados em Q1; R5/R6 (2 W) no topo, a 11 mm de C1; TP1/TP2/TP3/TP4 em volta de Q1; MOSFET isolado (clip sem potencial) | **Q1 e seu clip ficam a ≈ 4 mm do corpo de C1** (eletrolítico de 400 V: cada 10 °C a mais corta a vida pela metade, Aula 03). Dreno de Q1 a **24,8 mm** do pino 3 de T1 (pads em (48, 44) e (72,75, 44)); rede /DRAIN com 66 mm incluindo o ramo do snubber e TP2 — é o nó de maior dv/dt da placa. C1 de 40 mm de altura no centro define a altura interna do gabinete (≈ 45 mm) | Girar Q1 180° e deslocá-lo para (58, 44), entre C1 e T1: dreno a ≈ 12 mm do pino 3, clip voltado para T1 e não para C1; C1 em 18 × 35 mm (mesmo passo 7,5 mm) ou deitado se a caixa for baixa. Em produto, Q1 na borda inferior (y ≈ 80) com dissipador parafusado na parede da caixa |
| **C – controle UC3845** (x 2–56, y 60–84) | U1 (14, 66), C6/C8/C3/R11/C4/C7/R12/R14 em volta, C5 (35, 70), TP5–TP9 | Analógicos do CI agrupados; 100 nF (C6) a 4,3 mm do VCC; filtro do ISENSE no pino 3 com retorno pela ilha de terra de sinal; ilha ligada ao PGND de potência num só ponto (lado frio do shunt) | U1 está no canto oposto a Q1 e ao opto: trilhas **/DRV 35 mm + /GATE 45 mm** (comando), **/CS 54 mm** (medida), **/VCC 65 mm** e **/COMP 107 mm** (nó de alta impedância, pull-up 4,7 kΩ, atravessa a placa até U3). A Aula 08 pede driver junto ao transistor e sinais de medida curtos. A faixa x 40–75, y 72–88 está vazia (só TP9 e serigrafia) | Mover o bloco C inteiro para x 30–60 (centro da faixa inferior), com U1 em ≈ (42, 68): /DRV + /GATE ≈ 25 mm, /CS ≈ 20 mm, /COMP ≈ 45 mm. D4/R13 (auxiliar) vão para a esquerda. É a mudança de maior efeito sobre imunidade a ruído; **decidir pelas medições** em TP8 (CS) e TP7 (COMP) com o protótipo B |
| **D – auxiliar, opto, Y** (x 56–84, y 60–84) | D4 (60, 64), R13 (60, 69), CY1 (79, 63), U3 (88, 72, atravessando a fenda) | CY1 une PGND e SGND perto de T1 e do opto (caminho curto para a corrente de modo comum); opto com 6,0 mm entre fileiras e fenda de 1,2 mm | Região pouco ocupada; o opto fica a 66 mm de U1 (ver /COMP) | Absorvida pela proposta da região C |
| **E – secundário de potência** (x 96–135, y 2–60) | R15/C9 (106–120, 12), D1 (110, 20), C10/C11/C12 (110–132, 36), L2 (114, 50), C13 (125, 50), TP10/TP11 | D1 a 10 mm acima dos eletrolíticos (afastado na B); RC do diodo junto a D1; L2 a 30 mm de T1; trilhas de 2,0 mm | Laço T1 → D1 → C10 → T1 ≈ 22 + 11 + 20 mm (D1 acima da linha dos pinos 6–10 de T1, que estão em y 34–54); a corrente de 13 A de pico alimenta C10 primeiro e C11/C12 em cadeia, logo C10 recebe a maior parcela de corrente eficaz (RSE e vida desiguais, Aula 03); 1 mm entre os corpos de C10/C11/C12 dificulta retrabalho | D1 deitado em (104, 30) com ânodos voltados para os pinos 9/10 e cátodo para C10/C11 (laço ≈ 30 mm); alimentar o banco pelo ponto médio entre C10 e C11 (trilha simétrica); passo 12 mm entre os eletrolíticos; em produto, D1 na borda superior com dissipador parafusado |
| **F – realimentação e saída** (x 84–135, y 60–84) | R19/R20 (96, 63/67), U2 TL431 (110, 70), R16/R17 (114, 62/65), R18/C14 (118, 75/78), J2 (132, 70) | Divisor sente a tensão junto a C13/J2 (regulação de carga nos bornes); TL431 e compensador longe de T1 (38 mm) e sobre SGND; J2 na borda direita | Sem marcação de polaridade e tensão no silk de J2; saída em face perpendicular à entrada (J1 abre para a borda superior, J2 para a direita) | Silk "+12 V 3 A / −" em J2, "L N 90–264 V~" em J1 e "F1 T2A 250V" junto ao fusível (exigência de marcação em IEC 62368-1); J1 e J2 em bordas opostas |
| **Mecânica** | H1–H4 a 4 mm dos cantos; 140 × 90 mm; só PTH; soquete em U1 | Furos ≥ 6 mm das redes da entrada; espaço para sonda e pinça térmica; todos os componentes trocáveis com ferro comum; U1 trocável sem dessoldar | Área: as faixas x 40–75 × y 72–88, x 96–135 × y 2–10 e x 96–104 × y 26–60 estão vazias — uma versão produto cabe em ≈ 120 × 80 mm (−24 %) sem reduzir isolação; F1 axial soldado obriga dessoldar se queimar durante os ensaios | Protótipo: porta-fusível 5 × 20 com clipes (mesmo furo de 5 mm) e manter o fusível axial para produto. Produto: reduzir a placa depois de fixar a posição dos dissipadores |

## 2. Comprimentos de trilha que importam (medidos no pcbnew, `comprimento_redes.txt`)

| Rede | mm | Papel | Avaliação |
|---|---|---|---|
| /COMP | 106,6 | nó de compensação, alta impedância (R14 4,7 kΩ) | longa demais; C8 (1 nF) em U1 atenua, mas é a primeira suspeita se houver jitter no PWM |
| /CS | 54,4 | sinal do shunt para o pino 3 | aceitável com o filtro RC no pino 3 e retorno pela ilha; ideal ≤ 25 mm |
| /DRV + /GATE | 35,1 + 44,7 | comando do gate (R7/D3 ficam em Q1) | 80 mm até o gate; UC3845 tolera, mas é anel de ruído para os sinais de medida |
| /VCC | 65,3 | alimentação do CI vinda do auxiliar | C5 (220 µF) e C6 (100 nF) em U1 resolvem |
| /DRAIN | 66,1 | nó de maior dv/dt (inclui snubber e TP2) | encurtar com Q1 em (58, 44) |
| Net-(CX1-Pad1/2) | 80 + 80 | rede entre NTC, CX1 e L1 | filtro de entrada em linha reduz à metade |
| Net-(D1-K) / Net-(T1-S2) | 75 / 51 | laço do secundário (13 A de pico) | D1 deitado entre T1 e C10 |
| SGND / PGND | 140 / 47 | retornos com plano na face inferior | sem ação (plano) |

## 3. Térmico, altura e gabinete

- **Fontes de calor** [C]: Q1 1,15 W (clip 24 °C/W → T<sub>j</sub> ≈ 72 °C), D1 1,78 W (≈ 84 °C), R5/R6 1,0 W cada, BR1 0,67 W, RT1 ≈ 0,4 W, R3/R4 0,42 W cada, T1 ΔT ≈ 29 °C. A Aula 03 manda "considerar que o conversor vai estar em um gabinete": sem ventilação, +15–20 °C internos → Q1/D1 ≈ 90/105 °C, dentro da meta de 125 °C.
- **Capacitores perto do calor**: C1 a 4 mm do clip de Q1 e a 11 mm de R5/R6; C10–C12 a 10 mm de D1. Em produto, mover Q1 e D1 para a borda e deixar os eletrolíticos no lado frio (Aula 03: vida útil dobra a cada −10 °C).
- **Um dissipador para dois dispositivos** (Aula 02): Q1 é isolado (TO-220FP) e o tab de D1 está em +12 V; um perfil único na parede da caixa exigiria isolação reforçada no lado de Q1 e isolante no de D1, e o dissipador ficaria sem potencial. Só vale em caixa metálica classe I; em caixa plástica classe II, dois dissipadores separados.
- **Altura**: C1 (40 mm) > T1 (≈ 30 mm) > L1 (23 mm) > D1/Q1 com clip (≈ 25 mm). Trocar C1 por 18 × 35 mm ou 16 × 35 mm (150 µF/400 V existe nos dois) baixa a caixa para ≈ 40 mm.
- **Isolação para produto**: a regra do DRC usa 6,0 mm; para isolação reforçada a 250 V (IEC 62368-1, grau de poluição 2, material IIIb) o valor de referência é **6,4 mm** de escoamento. Na revisão C subir a regra `isolacao_prim_sec` para 6,4 mm (há espaço: a fenda cobre T1 e U3; só CY1 e as trilhas /LEDA e /KA precisam deslocar 0,5 mm).

## 4. Montagem e manutenção (roteiro da Tarefa Extra aplicado à nossa placa)

| Item da Tarefa Extra | Como a placa B se sai | Melhoria |
|---|---|---|
| Conectores e interface com a rede | bornes a parafuso 5,08 mm nas duas pontas; sem terra de proteção (classe II) | prever um 3.º pino em J1 (PE) só se a caixa for metálica |
| Gabinete | não existe (optativo no enunciado); placa prevê 4 furos M3 e altura 45 mm | caixa plástica 150 × 100 × 50 mm com grelhas sobre Q1/D1/T1 |
| Atendimento a normas | fusível 500 V, MOV, X2/Y1, 6,0 mm, fenda; sem marcação no silk | silk de F1, J1, J2 e símbolo de alta tensão; 6,4 mm |
| Proteções de entrada | F1 T2A, RV1 275 V, RT1 10 Ω | fusistor em vez de NTC + fusível é alternativa de custo (Aula 07), não recomendada para 3 A |
| Filtro de EMI | CX1 220 nF, L1 2 × 10 mH, CX2 100 nF, CY1 2,2 nF | encurtar a ligação CX1–L1 (região A); ensaio com LISN fica pendente |
| Retificador e capacitor de filtro | GBU4J PTH, C1 150 µF/400 V 105 °C | vida útil de C1 ainda não calculada pelo método da Aula 03 (ver §5) |
| Magnéticos | EE30/15/7 IP12R, L2 radial comercial | L2 poderia ser um toroide projetado pelo método da Tarefa 3 |
| PCI: distribuição e manutenção | blocos legíveis, silk com regiões, TP com nome, U1 em soquete; F1 soldado; C10–C12 com 1 mm entre corpos | porta-fusível no protótipo; passo 12 mm nos eletrolíticos |
| Semicondutores | STF13N65M2 TO-220FP, STPS20H100CT, UF4007/UF4004, 1N4148 | — |
| Térmico | 2 clips 24 °C/W | ver §3 |
| CI | UC3845 DIP-8, TL431, PC817 | — |
| Outros blocos (snubber) | RCD R5 ∥ R6 / C2 / D2 no topo | TVS P6KE em paralelo com o RCD é a alternativa citada na Aula 07 para reduzir R5/R6 |

**Ordem de montagem sugerida pela geometria** (do mais baixo ao mais alto, como manda a solda manual PTH): resistores e diodos deitados → cerâmicos e TPs → DIP/soquete, TL431, opto → R3/R4/R7/R8/R11 em pé → eletrolíticos pequenos (C5, C13) → Q1/D1 com clips (antes de C1, para o ferro alcançar os pads) → C10–C12 → bornes → BR1, RV1, RT1, CX1/CX2, L1 → C1 → T1 por último (10 pinos, com ohmímetro conferindo 1-3, 4-5, 6/7-9/10 antes de soldar).

**DFM para produção em onda** (Aula 08): menor distância entre pads de componentes diferentes 0,95 mm (U1–C8), abaixo dos 2,5 mm de referência; eixos dos axiais misturados (horizontais e verticais, R3/R4/R7/R8/R11 em pé) → efeito de sombra de C1/L1/T1 sobre componentes pequenos atrás deles no sentido da onda. Irrelevante para o protótipo (solda manual); em produto, alinhar os axiais no sentido da onda e abrir 2,5 mm.

## 5. O que o material de referência sugere que ainda não foi feito

| Fonte | Tópico | Como aplicar aqui | Esforço |
|---|---|---|---|
| Aula 08 | "Em caso de protótipos, prever pontos de medida de corrente" | hoje só há TPs de tensão; o shunt (TP3) dá I<sub>p</sub>, mas não há laço para sonda de corrente no secundário nem na rede. Prever em C dois jumpers de fio (2 pinos, 10 mm) em série com o pino 9/10 de T1 e com J1; no protótipo B, usar um fio em laço soldado no lugar de R15 ou na saída de D1 | baixo |
| Aula 08 | "Placa para uma família de produtos (potências diferentes)" | a mesma placa aceita 12 V/2 A, 15 V/2,4 A ou 24 V/1,5 A trocando T1 (espiras), D1, R16/R17 e os eletrolíticos (25 → 35 V, mesmo Ø10). Documentar a família na BOM como variantes | baixo |
| Aula 08 | Trilha de guarda ligada ao GND em sinais sensíveis | contornar /CS e /COMP com cobre de SGND na face superior (guard ring) na revisão C, já que ambos correm sobre a ilha na inferior | baixo |
| Aula 08 | Fluxo linear entrada → saída, driver junto ao transistor | regiões A e C (§1) | médio (novo roteamento) |
| Aula 03 | Vida útil do eletrolítico: L = L<sub>0</sub> · 2<sup>(T<sub>máx</sub> − T<sub>núcleo</sub>)/10</sup>, com aquecimento por RSE · I<sub>ef</sub>² | acrescentar `vida_util.py` em `02_Calculos`: C1 (I<sub>ef</sub> do bulk, T ≈ 55–60 °C) e C10–C12 (I<sub>ef</sub> 5,45 A dividido; ZLH 10 kh a 105 °C). Resultado esperado: ≥ 40 kh para C1 e ≥ 100 kh para a saída; confirmar com a temperatura medida no ensaio térmico (registro §6) | baixo |
| Aula 02 | Vários dispositivos no mesmo dissipador; centralizar o dispositivo; HS Dissipadores (nacional, como na Tarefa 1) | produto: perfil HS na parede da caixa; protótipo: manter os clips | baixo |
| Aula 07 | Lista de requisitos de fonte industrial (RECOM): standby, faixa de entrada, proteções OVP/OCP/curto, certificações, garantia | usar como pauta da seção "produto" na apresentação: o que a fonte atende (faixa 90–264 V, curto por hiccup, EMI) e o que não (OVP de saída, standby < 0,3 W, certificação) | baixo |
| Aula 07 | Exemplos de semestres anteriores: 12 V/3,5 A com FAN7554 (2024-2), 12 V/3 A com UCC28712 (2026-1), formas de onda em 127 e 220 V | padronizar os slides de resultados experimentais como nos exemplos do professor: dreno e corrente em 127 V e 220 V, lado a lado | baixo |
| Aula 07 | TVS/Transil como grampo alternativo ao RCD | já dimensionado em `snubber.py` (P6KE); ensaio comparativo no protótipo se R5/R6 aquecerem além de 1 W | médio |
| Aula 06 | THD e fator de potência do retificador com filtro capacitivo | medir corrente da rede em 127 e 220 V (sonda de corrente) e comparar com o cálculo de `entrada.py`; 36 W está abaixo dos 75 W da IEC 61000-3-2 classe D, mas o professor dá o exemplo com THD ≈ 150 % | baixo |
| Aula 05 | Sensor de corrente e de tensão | o shunt R9/R10 e o divisor R16/R17 são os sensores; documentar as larguras de banda (filtro 33 ns no CS; polo do opto) na seção de comando | baixo |
| Tarefa 1/2 | Cross-check de perdas no Power Stage Designer 5 | já feito em `semicondutores.py`; repetir com o R<sub>DS(on)</sub> do STF13N65M2 a 100 °C após medir a temperatura do clip | baixo |
| Tarefa 3 | Projeto de indutor toroidal (SMath, método Kg) | L2 (3,3 µH, 3,6 A) como toroide de pó de ferro projetado por nós, em vez do radial comercial: mostra o método da disciplina também no secundário | médio |
| Tarefa Extra | Roteiro de 13 itens | aplicado à nossa própria placa no §4; serve de slide "a fonte vista como produto" | feito |

## 6. Decisão recomendada

1. **Fabricar a B com o placement de 05/11** (§7; Gerbers regerados). Nenhum item restante é defeito funcional; o DRC, a isolação e os laços de potência atendem à Aula 08.
2. **Antes de decidir a revisão C de layout, medir no protótipo B**: ruído em TP8 (CS) e TP7 (COMP) com o dreno comutando; temperatura do corpo de C1 ao lado do clip de Q1; temperatura de C10 contra C12 (desequilíbrio da corrente eficaz). Esses três números decidem as três mudanças de maior custo (bloco C, Q1/C1, D1 deitado).
3. **Aplicar na C sem depender de medição** (baixo custo, só placement/silk): filtro de entrada em linha, J1 e J2 em bordas opostas, silk de F1/J1/J2, regra de 6,4 mm, passo 12 mm nos eletrolíticos, jumpers para sonda de corrente, porta-fusível no protótipo.
4. **Documentos novos para a revisão C**: `02_Calculos/vida_util.py` (Aula 03), slide "a fonte como produto" com os 13 itens da Tarefa Extra, slide de família de produtos.

## 7. Revisão aplicada em 05/11/2026 (antes do pedido) e conferência item a item

Aplicado em `placement.py`, `gera_sch.py`, `router.py`, `gera_pcb.py`, `.kicad_dru`, `.kicad_pro`; placa regerada, DRC 0 erros / 0 não conectados / 0 divergências (3 avisos de serigrafia já justificados), cobertura das regras OK, Gerbers e imagens da mesma revisão (`gerbers/fonte_flyback_12V3A_B_gerbers.zip`).

| Item | Antes (manhã) | Depois (placa enviada) |
|---|---|---|
| J1 | (16, 13) abrindo para o interior da placa | (7, 16) a 270°, abrindo para a borda esquerda; J2 inalterado abrindo para a direita |
| Filtro de entrada | zigue-zague; redes dos pads de CX1 com 80 + 80 mm | coluna F1 → JP1 → RV1/RT1 → R1/R2 → CX1 → L1 (pinos de entrada 1/3 em cima, L1 a 270°) → CX2 → BR1; 54 + 55 mm |
| F1 | axial soldado (477) | porta-fusível de clipes 5 × 20 (Keystone 3517), fusível T2A/250 V 215; silk "F1 T2A 250V" |
| Medida de corrente | só TP3 (shunt) | JP1 (fase) e JP2 (T1 9/10 → D1) para sonda de corrente |
| Q1 | (48, 44): dreno a 24,8 mm de T1.3, clip a 3,5 mm de C1 | (55, 48): dreno a 15,7 mm, clip a 6 mm de C1; /DRAIN 66 → 62 mm |
| Eletrolíticos de saída | passo 11 mm | passo 12 mm |
| Serigrafia | regiões e TPs | + "N"/"L", "0V"/"+12V 3A", "C1 400V DESCARREGAR" |
| Isolação | 6,0 mm (roteador pelo eixo da trilha) | 6,4 mm pelo cobre; exceção 6,0 mm só sob a fenda do opto (sem ela: 8 violações em U3) |
| Não aplicado (revisão C) | — | bloco UC3845 junto a Q1 (/COMP 109, /CS 56, gate 80 mm), D1 deitado, Q1/D1 na borda com dissipador parafusado, C1 18 × 35 |

**Conferência final (pedido do aluno: posição, trilhas, formato, bornes, entrada, filtro, sinais, Q1/D1 com dissipadores, L1/L2/T1, capacitores)** — tudo [CAD], medido na placa gerada:

- **Posição dos blocos:** fluxo rede (esquerda) → EMI → ponte/bulk → Q1/T1 (centro) → D1/capacitores/L2 → J2 (direita). Regiões sem cruzamento; `placement.py` 0 sobreposições de cortejo. OK.
- **Bornes:** J1 pads a 7 mm da borda e 8,5 mm de H1 (≥ 6 mm exigidos para parafuso que pode ser PE); J2 na borda direita com "+12V 3A"/"0V". Ambos MKDS 5,08 mm, cabo de 1,5 mm². OK.
- **Entrada e proteções:** ordem J1 → F1 → JP1 → RV1 (varistor em paralelo após o fusível) → RT1 (NTC em série no neutro) → CX1 → L1 → CX2 → BR1. Fusível antes de tudo, MOV depois do fusível (o fusível abre se o MOV falhar em curto). OK.
- **Filtro de EMI:** CX1 encostado nos pinos de entrada de L1 (1/3, em cima), CX2 nos pinos de saída (2/4, embaixo) e junto a BR1; CY1 entre PGND e SGND junto a T1/U3, fora da fenda; L1 a 70 mm de T1 e 30 mm de L2 (magnéticos afastados). OK. Pendente só o ensaio com LISN.
- **Larguras de trilha (IPC-2221, 35 µm):** rede 1,2 mm (0,75 A rms, ΔT < 5 °C); bulk 1,5 mm; HV/dreno 1,0 mm (2,1 A pico, 0,8 A rms); secundário de potência 2,0 mm (5,45 A rms, ΔT < 20 °C; 13 A de pico); SGND/VO 2,0 mm; VCC/aux 0,8; sinais 0,5 mm. Regras `largura_HV` ≥ 1,0 e `largura_SEC_potencia` ≥ 1,5 verificadas pelo DRC. OK.
- **Formato das trilhas:** 255 dobras a 45°, 21 ângulos retos só em saídas de pad (19) ou a 0,1 mm de um pad (2); nenhuma trilha de sinal atravessa a ilha de terra na face inferior por mais de 6 mm; ilha contínua (flood-fill). OK.
- **Sinais e terras:** PGND de potência e ilha PGND de sinal unidos num ponto (lado frio de R10); CS filtrado no pino 3 (R11/C3) com retorno pela ilha; 100 nF (C6) a 4,3 mm do VCC; realimentação (U2, R16–R18, C14) sobre SGND a 38 mm de T1; opto atravessando a fenda. Pendência conhecida: /COMP 109 mm, /CS 56 mm, /DRV + /GATE 80 mm (U1 longe de Q1) — decidir na revisão C com as medições em TP7/TP8.
- **Q1 (STF13N65M2, TO-220FP) e dissipador:** clip 24 °C/W (HS1), T<sub>j</sub> ≈ 72 °C [C]; isolado (clip sem potencial), a 6 mm do corpo de C1 e 12 mm de BR1; gate R7/D3/R8 a ≤ 8 mm do pino; laço fonte → R9/R10 → PGND de 7 mm; TP2 (dreno, sonda diferencial), TP3 (shunt), TP4 (gate) ao lado. OK para o protótipo; em produto, borda + dissipador parafusado.
- **D1 (STPS20H100CT) e dissipador:** clip 24 °C/W (HS2), T<sub>j</sub> ≈ 84 °C [C]; 10 mm acima de C10–C12; RC R15/C9 junto; laço T1 → JP2 → D1 → C10 ≈ 50 mm (aceitável; D1 deitado reduziria para ≈ 30 mm na C). OK.
- **BR1 (GBU4J):** 0,67 W, T<sub>j</sub> ≈ 53 °C sem dissipador [C]; vertical entre L1 e C1, furo livre para parafusar à caixa em produto. OK.
- **T1 (EE30/15/7):** centrado na fenda de 1,2 mm, pinos 1–5 no primário (x = 72,75) e 6–10 no secundário (x = 95,25), 22,5 mm entre fileiras; cortejo de 33 mm respeitado por Q1/R4/JP2. OK.
- **L1 (RN214) e L2 (3,3 µH):** L1 deitado na borda esquerda (23 mm de altura), L2 radial entre o banco e C13; 30 mm entre L2 e T1. OK.
- **Capacitores:** C1 150 µF/400 V 18 × 40 mm a 6 mm de Q1 e 11 mm de R5/R6 (define a altura da caixa, 45 mm; 18 × 35 em produto); C10–C12 ZLH 1000 µF/25 V com passo 12 mm, alimentados por C10 (trilha simétrica fica para a C); C13 470 µF junto a J2; C5 220 µF/35 V junto a U1; cerâmicos C3/C6/C8 encostados em U1; CX1/CX2 X2 e CY1 Y1 com 10 mm de passo. OK.
- **Resistores quentes:** R5/R6 (1 W cada) no topo, a 11 mm de C1 e 20 mm de T1; R3/R4 (0,42 W) em pé; NTC a 20 mm de C1 — montar R5/R6/R3/R4 a 3 mm da placa. OK.
- **Furos e caixa:** 4 × M3 a 4 mm dos cantos, ≥ 8,5 mm de qualquer pad da rede; altura mínima interna 45 mm (C1). OK.
