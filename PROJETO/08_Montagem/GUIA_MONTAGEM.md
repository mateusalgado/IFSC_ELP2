# Guia de montagem e ensaio – Fonte flyback 12 V / 3 A (UC3845)

Este guia serve para a decisão **montar ou não montar** (Possibilidade II do enunciado) e, se a decisão for montar, para executar o protótipo com segurança e validar os resultados de projeto. Todos os valores vêm de `02_Calculos/resultados/RESULTADOS_TEORIA.md` e da simulação em `03_Simulacao/runs/medidas.json`.

> **Atenção – rede elétrica.** O primário fica em até 370 V CC (264 VAC) e não é isolado da rede. Use **transformador isolador** ou, no mínimo, **lâmpada em série** (100 W) nos primeiros ensaios, osciloscópio com **sonda diferencial** ou com o osciloscópio isolado da rede, e nunca ligue o terra da sonda no primário com o osciloscópio aterrado. O capacitor de bulk (100 µF/400 V) guarda carga por vários segundos: descarregue com resistor de 10 kΩ/5 W antes de tocar na placa.

## 1. Critérios para decidir montar ou não

| Critério | Possibilidade I (só projeto + Tarefa Extra) | Possibilidade II (protótipo) |
|---|---|---|
| Custo | zero | ≈ US$ 40 por fonte (R$ 220) + frete; ver `05_BOM_Custo/custo.md` (a PCI em 5 unidades é 24 % do custo) |
| Prazo | relatório pronto | compra (2–4 semanas importado; 1 semana lojas BR) + enrolar o trafo (2 h) + montagem (3 h) + ensaios (4 h) — iniciar até **meados de novembro/2026** para a apresentação de 21/12 |
| Bancada necessária | nenhuma | variac ou transformador isolador, osciloscópio (sonda diferencial), multímetro, carga eletrônica ou resistores 4 Ω/40 W e 8 Ω/20 W, medidor LCR (para Lp) |
| Risco técnico | — | enrolamento do transformador (Lp e Llk), disponibilidade do STP13N65M2 (há substitutos), ajuste do entreferro |
| Ganho na avaliação | relatório + Tarefa Extra (13 itens) | "o funcionamento do circuito é levado em conta na avaliação" (plano de ensino) + formas de onda experimentais |

Recomendação: montar se houver acesso à bancada com isolador e sonda diferencial; caso contrário, entregar a Possibilidade I com a Tarefa Extra (modelo em `09_Tarefa_Extra/`).

## 2. Lista de compra

Lista completa com part numbers e preços em `05_BOM_Custo/BOM.xlsx`. Alternativas em lojas nacionais (Soldafria, Baú da Eletrônica, Eletrônica Castro, Multcomercial):

| Item | Importado (Mouser/Digi-Key) | Alternativa nacional |
|---|---|---|
| MOSFET 650 V | STP13N65M2 (ou STF13N65M2, IPA65R400CE) | FQPF13N65 / 2SK3878 / IRFBC40 (600 V — margem menor, só para 127 V) |
| Diodo de saída | STPS20H100CT | MBR20100CT, MBR20100 |
| Ponte | GBU4J | KBP206, GBU406 |
| UC3845 | UC3845BN (ST) / UC3845BNG (onsemi) | UC3845 (qualquer fabricante, DIP-8) |
| Núcleo + carretel | TDK E30/15/7 N87 + B66318 | **Thornton NEE-30/15/7 IP12R + carretel CNEE-30/15/7** (preferido: é o núcleo do projeto) |
| Choke MC 10 mH | Würth 744821110 | choke de modo comum 10 mH/1 A de fonte ATX sucateada (medir) |
| Capacitores X2/Y1 | EPCOS B32922 / Vishay VY1 | qualquer X2 275 VAC e Y1 250 VAC certificados |
| Eletrolíticos 25 V baixo ESR | Rubycon ZLH | Panasonic FR / Nichicon PW (1000 µF/25 V, 105 °C, low-ESR) |
| Fio esmaltado | 23 AWG (0,573 mm) e 28 AWG, 15 m | idem |
| Dissipadores clip TO-220 | Aavid 574502B00000G | dissipador de alumínio 25 × 20 mm com furo (RθSA ≤ 24 °C/W) |

## 3. Enrolamento do transformador T1 (núcleo E-30/7 = NEE-30/15/7)

Dados de projeto (Aula 04C): Np = **42** espiras (1 × 23 AWG), Ns = **7** espiras (5 × 23 AWG em paralelo), Naux = **9** espiras (1 × 28 AWG), Lp = **294 µH**, entreferro total **0,45 mm** na perna central (ou espaçador de 0,23 mm em cada perna externa), B pico = 0,25 T, Kocup = 0,46.

Ordem (sanduíche, reduz a dispersão):

1. **Primário 1ª metade – 21 espiras** de 23 AWG, do pino 1 ao pino 2 (pinos do carretel conforme o footprint `Trafo_EE30_10pin`: primário pinos 1–3, auxiliar 4–5, secundário 6–10), 1 camada uniforme, sentido horário olhando o carretel pelos pinos do primário. Marcar o início (ponto) no pino 1. Uma camada de fita de poliéster (Mylar) 10 mm.
2. **Auxiliar – 9 espiras** de 28 AWG espalhadas na largura do carretel, pino 4 (início) ao pino 5. Fita.
3. **Secundário – 7 espiras** com **5 fios 23 AWG em paralelo** (ou fio triplo-isolado 0,6 mm; se usar fio esmaltado comum, colocar **3 camadas de fita** antes e depois, e respeitar a margem de 3 mm nas bordas do carretel para a isolação reforçada). Início no pino 9 (ponto), fim no pino 7 (SGND). Os 5 fios torcidos juntos; soldar todos os 5 em cada pino.
4. **Primário 2ª metade – 21 espiras** de 23 AWG, em série com a 1ª (continuar do pino 2 ao pino 3) — **mesmo sentido** da primeira metade. Fita externa 2 camadas.
5. Polaridade (pontos no esquemático): o início do primário (pino 1) vai ao **bulk (+)**; o fim (pino 3) ao **dreno** do MOSFET. O secundário e o auxiliar devem ser enrolados **no mesmo sentido** do primário, e ligados de modo que o **fim** de cada um vá ao ânodo do diodo (flyback = tensão invertida): pino 9 → SGND/ponto, pino 7 → ânodo do D1 … conferir com o esquemático antes de soldar; se a fonte não partir ou a saída ficar próxima de zero, inverter o auxiliar.
6. Montar o núcleo com o **entreferro só na perna central** (lixar a perna central 0,45 mm ou usar núcleo com gap de fábrica "AL ≈ 170 nH/esp²") **ou** espaçadores de 0,23 mm (papel/Mylar) nas duas pernas externas (gap total = 2 × 0,23 mm). Presilhas ou fita.
7. **Medir Lp** (pinos 1–3) com LCR a 10–100 kHz: alvo **294 µH ± 10 %** (265–325 µH). Lp alto → aumentar o gap; Lp baixo → reduzir. **Medir Llk**: curto-circuitar o secundário (pinos 7–9) e medir nos pinos 1–3: alvo **< 9 µH (3 %)**; se > 9 µH, o snubber dissipa mais (ver `snubber.py`) — refazer o sanduíche.
8. Teste de isolação: ≥ 1 kΩ·M entre primário e secundário (megôhmetro 500 V, se disponível).

## 4. Ordem de montagem da placa (por blocos, testando cada um)

Use a serigrafia (referências) e `04_KiCad/imagens/pcb_silk.png`. Soldar do mais baixo para o mais alto: resistores → diodos → soquete DIP-8 → cerâmicos → TO-92 (TL431) → opto → eletrolíticos pequenos → TO-220 com dissipadores (mica + bucha no MOSFET; o diodo pode ir direto no clip) → bornes, porta-fusível, NTC, varistor, X2/Y1 → choke L1, indutor L2 → bulk C1 → transformador T1 (por último; conferir a polaridade dos pinos).

**Bloco 1 – Entrada e retificador** (sem Q1, sem U1, sem T1): ligar em 127 V com lâmpada em série; medir Vbulk ≈ 180 V, sem aquecimento, varistor e NTC frios.

**Bloco 2 – Controle (UC3845) sem potência**: desligar da rede; alimentar o pino 7 (VCC, TP5) com fonte de bancada 15 V / 50 mA (através do PGND = TP9). Medir: VREF (TP6) = 5,0 V; oscilação no CT (pino 4, dente de serra 1,2–2,8 V, 130 kHz); saída (pino 6 do U1): pulsos de 15 V em **≈ 65 kHz** com razão cíclica ≈ 45–48 % (COMP flutuando → máximo). Consumo ≈ 15–20 mA. Inserir Q1 e verificar o gate (TP4): pulsos limpos, sem oscilação.

**Bloco 3 – Potência em malha aberta reduzida**: com T1 montado, variac a 40–60 VAC com lâmpada em série, carga de 40 Ω (0,3 A). Esperar partida (VCC sobe por R3/R4 até 8,4 V, pode levar vários segundos a 40 V). Verificar Vo subindo e se estabilizando em 12 V; dreno (TP2-DRAIN, sonda diferencial): rampa e patamar de grampo sem "ringing" excessivo; corrente no Rsense (TP3-SW, triângulo até ≈ 0,3 V). Se Vo for a mais de 13 V e não regular: verificar o opto/TL431 (R16/R17, LED aceso?).

**Bloco 4 – Tensão plena**: retirar a lâmpada, 127 V, depois 220 V; carga de 10 % → 50 % → 100 % (4 Ω/40 W). Medir a tabela da seção 5. Deixar 30 min a plena carga e medir temperaturas (termopar ou IR): MOSFET, D1, T1, R5/R6, NTC.

**Bloco 5 – Ensaios de proteção**: curto-circuito na saída por 10 s a 220 V (esperado: "hiccup", sem dano, Ip limitado a ≈ 3 A pelo Rsense — simulação: 4,3 A de pico em transitório); degrau de carga 50 ↔ 100 % (esperado: afundamento < 300 mV, recuperação < 2 ms); partida a 90 V e 264 V.

## 5. Tabela de ensaio (valores esperados de projeto/simulação) e critério de aceite

| Grandeza | Onde medir | Esperado (teoria / simulação) | Aceite |
|---|---|---|---|
| Vo (0,3–3 A, 90–264 V) | J2 / TP10 | 12,04 V / 12,06–12,08 V | 11,4–12,6 V |
| Ondulação de saída (p-p) | TP10, AC, 20 MHz | 2,7 mV (após LC) / 3–4 mV; nos capacitores C10–C12: 89 mV | ≤ 120 mV |
| fsw | TP4 (GATE) ou pino 6 do U1 | 64,7 kHz | 60–70 kHz |
| Vbulk mín. (90 V, 3 A) | TP1 | 94,6 V / 95,6 V | ≥ 90 V |
| Ip (90 V, 3 A) | TP3 (SW) ÷ 0,33 Ω | 2,14 A / 2,07 A | ≤ 2,5 A |
| D (90 V, 3 A) | TP4 (GATE) | 0,43 / 0,43 | ≤ 0,48 |
| Vds máx (264 V, 3 A) | TP2 – dreno (diferencial) | 507 V / 482 V (496 V com Llk 3 %) | ≤ 520 V (80 % de 650 V) |
| Vreversa máx no D1 | cátodo–ânodo de D1 | 74 V / 86 V (com ringing) | ≤ 100 V |
| Rendimento 220 V, 3 A | wattímetro ou V·I entrada e saída | 83 % / 85,5 % | ≥ 80 % |
| Corrente de entrada eficaz 90 V | alicate / Rshunt | 0,86 A / 0,80 A | ≤ 1,0 A |
| VCC em regime | TP5 | 15,4 V / 15,6 V | 12–18 V |
| Temperaturas a 40 °C ambiente (ou corrigir): MOSFET, D1, T1 | IR/termopar | Tj 69 °C, 84 °C; ΔT trafo 29 °C | ≤ 100 °C na aleta; trafo ≤ 80 °C |
| Partida 90 V / 264 V | TP10 | < 100 ms após VCC = 8,4 V (sim.: ok) | sem sobretensão > 13 V |
| Curto na saída | J2 | hiccup, Ip ≤ 3 A | sem dano em 30 s |

Critério de aceite global: todas as linhas em "aceite" em 127 V e 220 V (condições que o professor valida) e sem aquecimento anormal após 30 min.

## 6. Diagnóstico rápido

| Sintoma | Causa provável | Ação |
|---|---|---|
| Não parte, VCC oscila entre 7,6 e 8,4 V (pulsos de 10 ms) | auxiliar invertido ou Naux insuficiente | inverter os pinos 4–5 do auxiliar |
| Vo sobe acima de 13 V e não regula | opto/TL431 sem polarização (R19/R20, R16/R17) ou opto invertido | medir Vka do TL431 (deve variar 2–6 V) |
| Fusível queima / MOSFET curto na primeira ligação | polaridade do primário invertida (mesma polaridade no secundário → forward), gap zero (saturação) | medir Lp e conferir pontos |
| Vds > 550 V ou ringing forte | Llk alta, snubber C2/R5/R6 com valor errado, D2 lento | medir Llk, usar UF4007 |
| Ruído audível / instabilidade em carga leve | modo burst em 10 % (normal em modo corrente de pico em MCD) | aceitar ou aumentar Cz |
| Aquece R5/R6 (> 80 °C) | Llk > 3 % | refazer o enrolamento em sanduíche |

## 7. Pontos de medição

TP1 BULK (+), TP2 DRAIN (dreno do MOSFET, sonda diferencial), TP3 SW (tensão no Rsense = corrente do primário × 0,33 Ω), TP4 GATE, TP5 VCC, TP6 VREF, TP7 COMP, TP8 CS (pino 3), TP9 PGND, TP10 VO, TP11 SGND. Dreno do MOSFET: terminal central de Q1 (sonda diferencial 1000 V). Corrente do secundário: laço de fio no pino 9 de T1 com sonda de corrente.
