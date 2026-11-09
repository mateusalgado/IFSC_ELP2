# Guia de montagem e ensaio – Fonte flyback 12 V / 3 A (UC3845) – **Revisão B**

Este guia serve para a decisão **montar ou não montar** (Possibilidade II do enunciado) e, se a decisão for montar, para executar o protótipo com segurança e validar os resultados de projeto. Os valores de projeto vêm de `02_Calculos/resultados/RESULTADOS_TEORIA.md` (cálculo) e de `03_Simulacao/runs/medidas.json` (simulação) **da revisão B**; nenhum valor deste guia é medição física. As referências de componentes (R, C, D, TP…) são as do esquemático B (`04_KiCad/fonte_flyback_12V3A_esquematico.pdf`).

> **Atenção – rede elétrica.** O primário fica em até 370 V CC (264 VAC) e **não é isolado da rede**. Lâmpada em série limita corrente e variac ajusta tensão: **nenhum dos dois isola**. Energize o protótipo somente pelo **transformador isolador do laboratório** (ou pela bancada isolada e supervisionada pelo responsável), mantenha o **terra de proteção do osciloscópio ligado** e meça o primário só com **sonda diferencial** especificada para a tensão diferencial (≥ 700 V), tensão de modo comum e categoria (CAT II 600 V ou superior). Nunca ligue a garra de terra de uma sonda comum a qualquer ponto do primário. O capacitor de barramento C1 (150 µF / 400 V) guarda **≈ 10 J** a 370 V: antes de tocar na placa, descarregue com **resistor de 4,7 kΩ / 10 W de fio** com cabos isolados (τ ≈ 0,7 s; potência inicial 29 W, energia absorvida 10 J, dentro da capacidade de pulso de um resistor de 10 W) e **confirme < 30 V com multímetro CAT II 600 V** antes de manusear. O ensaio de curto-circuito na saída só é liberado com os limites da seção 5.4.

## 1. Critérios para decidir montar ou não

| Critério | Possibilidade I (só projeto + Tarefa Extra) | Possibilidade II (protótipo) |
|---|---|---|
| Custo | zero | BOM B ≈ US$ 42,7 por fonte com a PCI rateada em 5 placas (≈ R$ 235); saída de caixa para 1 exemplar comprando o lote mínimo de 5 placas ≈ US$ 81 (42,7 − 9,6 + 48) antes de fretes, impostos e mínimos; ver `05_BOM_Custo/custo.md` |
| Prazo | relatório pronto | compra (2–4 semanas importado; 1 semana lojas BR) + enrolar o trafo (2 h) + montagem (3 h) + ensaios (4 h) — iniciar até **meados de novembro/2026** para a apresentação de 21/12 |
| Bancada necessária | nenhuma | transformador isolador, variac, osciloscópio com sonda diferencial, multímetro CAT II, wattímetro de potência ativa (ou V·I com sonda de corrente), carga eletrônica ou resistores 4 Ω/40 W e 8 Ω/20 W, medidor LCR (Lp e Llk), termômetro IR ou termopar |
| Risco técnico | — | enrolamento do transformador (Lp, Llk e isolação), disponibilidade do STF13N65M2 (substitutos listados), ajuste do entreferro |
| Ganho na avaliação | relatório + Tarefa Extra (13 itens) | "o funcionamento do circuito é levado em conta na avaliação" (plano de ensino) + formas de onda experimentais |

Recomendação: montar se houver acesso à bancada isolada com sonda diferencial e supervisão; caso contrário, entregar a Possibilidade I com a Tarefa Extra (modelo em `09_Tarefa_Extra/`).

## 2. Lista de compra (revisão B)

Lista completa com part numbers e preços de referência em `05_BOM_Custo/BOM.xlsx`. Mudanças da revisão B em relação à A: C1 150 µF/400 V (tolerância do barramento a 90 V), fusível 5 × 20 T2A/250 V em porta-fusível de clipes Keystone 3517 (troca sem dessoldar; o axial soldado fica para o produto), laços de fio JP1 (fase, após o fusível) e JP2 (secundário, entre T1 e D1) para sonda de corrente (05/11), choke de modo comum Schaffner RN214 2 × 10 mH / 1,2 A, R5 ∥ R6 (18 kΩ ∥ 18 kΩ = 9 kΩ no grampo), filtro do ISENSE 330 Ω / 100 pF junto ao pino 3, R9/R10 = 0,68 Ω ∥ 0,68 Ω, compensador Rz 21,5 kΩ / Cz 270 nF, **R13 = 100 Ω** (série do auxiliar: faz o VCC cair no curto e o CI entrar em hiccup), **Q1 = STF13N65M2 (TO-220FP isolado)** com dissipador clip sem tensão, TL431 com pinagem física K-A-REF (1-2-3), capacitor Y1 com passo 10 mm.

| Item | Importado (Mouser/Digi-Key) | Alternativa nacional |
|---|---|---|
| MOSFET 650 V isolado | STF13N65M2 (TO-220FP); IPA65R400CE | FQPF13N65 (TO-220F) |
| Diodo de saída | STPS20H100CT | MBR20100CT |
| Ponte | GBU4J | KBP206, GBU406 |
| UC3845 | UC3845BN (ST) / UC3845BNG (onsemi) | UC3845 (qualquer fabricante, DIP-8) |
| Núcleo + carretel | TDK E30/15/7 N87 + B66318 | **Thornton NEE-30/15/7 IP12R + carretel CNEE-30/15/7 10 pinos** (núcleo do projeto) |
| Choke MC 2 × 10 mH / 1,2 A | Schaffner RN214-1.2-02-10M | choke 10 mH / ≥ 1 A de fonte ATX (medir L e Rdc) |
| Capacitores X2/Y1 | EPCOS B32922 / Vishay VY1 | qualquer X2 305 VAC e Y1 250 VAC certificados |
| Eletrolíticos 25 V baixo ESR | Rubycon ZLH | Panasonic FR / Nichicon PW (1000 µF/25 V, 105 °C, low-ESR) |
| Fio esmaltado | 23 AWG (0,573 mm) e 28 AWG, 15 m | idem |
| Dissipadores clip TO-220 | Aavid 574502B00000G (Q1 e D1) | dissipador de alumínio 25 × 20 mm (RθSA ≤ 24 °C/W) |

## 3. Transformador T1 – ficha de fabricação (núcleo E-30/7 = NEE-30/15/7, carretel 10 pinos)

Dados de projeto (Aula 04C): N<sub>p</sub> = **42** espiras (1 × 23 AWG), N<sub>s</sub> = **7** espiras (5 × 23 AWG em paralelo), N<sub>aux</sub> = **9** espiras (1 × 28 AWG), L<sub>p</sub> = **294 µH**, entreferro total **0,45 mm** na perna central (ou espaçador de 0,23 mm em cada perna externa), B<sub>pico</sub> = 0,25 T, K<sub>ocup</sub> = 0,46. Fios: 23 AWG = 0,258 mm² (5 fios = 1,29 mm²); um único fio de 0,6 mm (0,28 mm²) **não** substitui os cinco.

**Pinagem fixada pela netlist B** (footprint `Trafo_EE30_10pin`, pinos 1–5 no lado do primário, 6–10 no lado do secundário):

| Pino | Enrolamento | Liga em | Observação |
|---|---|---|---|
| 1 | primário – início (ponto) | /BULK (+ do C1) | |
| 2 | — | sem ligação | pino de apoio (centro do primário, não usar) |
| 3 | primário – fim | /DRAIN (dreno de Q1, D2, TP2) | |
| 4 | auxiliar – início (ponto) | PGND | |
| 5 | auxiliar – fim | /AUX (ânodo de D4 → R13 → VCC) | |
| 6 e 7 | secundário – início (ponto), **os 5 fios divididos entre os dois pinos** | SGND | |
| 8 | — | sem ligação (blindagem opcional) | se usar folha de cobre entre primário e secundário, ligar aqui **não**: ligar ao pino 1 (bulk) pelo lado do primário |
| 9 e 10 | secundário – fim, **os 5 fios divididos entre os dois pinos** | ânodos de D1 (pinos 1 e 3 do STPS20H100CT) | |

Ordem de camadas (sanduíche, reduz a dispersão) – todos os enrolamentos no **mesmo sentido de rotação**, olhando o carretel pelos pinos do primário:

1. **Primário, 1ª metade – 21 espiras** de 23 AWG, começando no **pino 1** (ponto), uma camada uniforme, terminando em fio solto (não soldar no pino 2). Uma camada de fita de poliéster (Mylar) 10 mm.
2. **Auxiliar – 9 espiras** de 28 AWG espalhadas na largura, **início no pino 4**, fim no **pino 5**. Fita.
3. **Secundário – 7 espiras** com **5 fios 23 AWG em paralelo** torcidos (ou fio triplo-isolado equivalente a 1,3 mm²): **início nos pinos 6/7** (ponto), fim nos **pinos 9/10**; se usar fio esmaltado comum, **3 camadas de fita** antes e depois e margem de 3 mm nas bordas (isolação reforçada). Fita.
4. **Primário, 2ª metade – 21 espiras** de 23 AWG em série com a 1ª (continuar o fio solto), terminando no **pino 3**. Fita externa, 2 camadas.
5. Pontos (início de cada enrolamento): pino 1 (primário), pino 4 (auxiliar), pinos 6/7 (secundário). Com essa polaridade a tensão do secundário e do auxiliar aparece **durante o bloqueio** de Q1 (flyback); os ânodos de D1 e de D4 ficam nos fins dos enrolamentos (pinos 9/10 e 5).
6. Montar o núcleo com entreferro **só na perna central** (0,45 mm, lixado ou núcleo com gap de fábrica AL ≈ 170 nH/esp²) **ou** espaçadores de 0,23 mm nas duas pernas externas. Presilhas ou fita.

Verificações antes de montar na placa:

| Ensaio | Como | Aceite |
|---|---|---|
| L<sub>p</sub> | LCR em 10–100 kHz nos pinos 1–3 | 265–325 µH (294 ± 10 %); alto → mais gap; baixo → menos gap |
| L<sub>lk</sub> | pinos 1–3 com 6/7 curto-circuitados a 9/10 | < 9 µH (3 % de L<sub>p</sub>); se maior, refazer o sanduíche |
| Relação e fase | senoide de 5 V / 10 kHz do gerador nos pinos 1–3; medir 6/7–9/10 e 4–5 com osciloscópio, pontos alinhados | 42:7 → 0,83 V (±5 %) e 42:9 → 1,07 V, mesma polaridade dos pontos |
| Isolação primário–secundário | megôhmetro 500 V entre (1,3) e (6,7,9,10), se disponível | ≥ 100 MΩ (procedimento definido com o laboratório; sem hi-pot sem equipamento adequado) |
| Encaixe | os 5 fios do secundário entram nos pinos e a altura total das camadas cabe no carretel | sim |

## 4. Ordem de montagem da placa (por blocos, testando cada um)

Use a serigrafia e `04_KiCad/imagens/pcb_silk.png` (revisão B). Soldar do mais baixo para o mais alto: resistores → diodos → soquete DIP-8 → cerâmicos → TL431 (TO-92, lado plano conforme serigrafia: pinos K-A-REF = 1-2-3) → opto → eletrolíticos pequenos → Q1 (TO-220FP, **sem mica**, com clip) e D1 (TO-220 no clip) → bornes, clipes do fusível (o fusível só entra antes do bloco 1), laços JP1/JP2 (fio nu de 0,8 mm, arco de ≈ 5 mm acima da placa), NTC, varistor, X2/Y1 → choke L1 (pinos 1-2 e 3-4 são os enrolamentos; pontos em 1 e 3), indutor L2 → C1 (150 µF, deitado se o gabinete exigir) → T1 por último, conferindo a pinagem da seção 3.

**Bloco 1 – Entrada e retificador** (sem Q1, sem U1, sem T1): pelo isolador + variac a 127 V; medir V<sub>bulk</sub> ≈ 175 V entre TP1 e TP9; sem aquecimento; varistor e NTC frios. Desligar e descarregar C1 (ver aviso).

**Bloco 2 – Controle (UC3845) sem potência**: desligado da rede e com C1 descarregado; alimentar TP5 (VCC) com fonte de bancada 15 V / 50 mA contra TP9 (PGND). Medir: TP6 (VREF) = 5,0 V; dente de serra no pino 4 (1,2–2,8 V, ≈ 130 kHz); pino 6 (saída): pulsos de ≈ 13 V em **≈ 65 kHz** com razão cíclica ≤ 48 %. Consumo 15–20 mA. Inserir Q1 e verificar TP4 (gate): bordas limpas, sem oscilação.

**Bloco 3 – Potência em tensão reduzida**: com T1 montado, isolador + variac a 40–60 VAC, carga 40 Ω (0,3 A). A partida pelo R3/R4 pode levar vários segundos nessa tensão. Verificar V<sub>o</sub> subindo e regulando em 12 V; TP2 (dreno, sonda diferencial): rampa e patamar do grampo sem ringing excessivo; TP3 (SW): triângulo de corrente até ≈ 0,3 V (× 1/0,34 Ω). Se V<sub>o</sub> passar de 13 V sem regular: TL431/opto (R16/R17, LED).

**Bloco 4 – Tensão plena**: 127 V e depois 220 V pelo isolador; carga 10 % → 50 % → 100 % (4 Ω/40 W). Medir a tabela da seção 5. 30 min a plena carga e temperaturas (IR/termopar): Q1, D1, T1, R5/R6, NTC, C1, C10–C12.

**Bloco 5 – Transitórios**: degraus 50 ↔ 100 % nos dois sentidos (carga eletrônica); partida a frio em 90 V e 264 V (variac); o **curto-circuito só com os limites da seção 5.4**.

## 5. Grandezas esperadas e critério de aceite

Origem de cada valor: **C** = cálculo (`RESULTADOS_TEORIA.md`), **S** = simulação LTspice B (`medidas.json`), **M** = medição física (a preencher no ensaio).

### 5.1 Regime permanente

| Grandeza | Onde medir | C | S (B) | Aceite |
|---|---|---|---|---|
| V<sub>o</sub> (0,3–3 A, 90–264 V) | J2 / TP10–TP11 | 12,04 V | 12,06–12,06 V | 11,4–12,6 V |
| Ondulação de chaveamento (p-p, 20 MHz) | TP10 | 2,7 mV (após LC) | ≤ 4,8 mV | ≤ 120 mV |
| Excursão total de V<sub>o</sub> em ciclos inteiros da rede | TP10 | — | ≤ 8,5 mV | ≤ 120 mV |
| f<sub>sw</sub> | TP4 ou pino 6 | 64,7 kHz | 64,7 kHz | 60–70 kHz |
| V<sub>bulk</sub> mín. (90 V, 3 A, 50 Hz) | TP1 | 104 V (150 µF) | 103,9 V | ≥ 95 V |
| I<sub>p</sub> (90 V, 3 A) | TP3 ÷ 0,34 Ω | 2,14 A | 2,06 A | ≤ 2,5 A |
| V<sub>ds</sub> máx (264 V, 3 A) | dreno (diferencial) | 507 V | 482 V | ≤ 520 V |
| V<sub>rev</sub> máx em D1 | D1 (K–A) | 74 V | 86 V | ≤ 100 V |
| Rendimento 220 V, 3 A (potência ativa) | wattímetro ou v(t)·i(t) | 83,0 % | 85,2 % | ≥ 85 % (meta); ≥ 83 % (cálculo) |
| VCC em regime | TP5 | 15,4 V | 14,1 V | 12–18 V |
| Temperaturas a 40 °C (Q1 aleta, D1 aleta, T1) | IR/termopar | T<sub>j</sub> 72 / 84 °C; ΔT trafo 29 °C | — | ≤ 100 °C na aleta; trafo ≤ 80 °C |

### 5.2 Partida a frio (C1 e C5 descarregados)

| Grandeza | C | S (B) | Aceite |
|---|---|---|---|
| Tempo até UVLO (8,4 V) em 90 / 264 V | 4,3 s / 1,0 s | 7,34 s / 1,05 s | < 10 s |
| V<sub>o</sub> ≥ 11,4 V após o início do chaveamento | — | 5,3 ms / 4,3 ms | < 50 ms, sem sobretensão > 12,6 V |
| V<sub>ds</sub> máx na partida em 264 V | 507 V | 515 V | ≤ 520 V |
| Pico de I<sub>p</sub> na partida (primeiros ciclos, saída em zero → sem reset do núcleo) | 2,9 A (limite ciclo a ciclo) | 3,47 A por < 1 ms (modelo linear; núcleo real satura ≈ 3 A) | ≤ 3,5 A por < 1 ms; parar se > 4 A ou se durar > 2 ms |

### 5.3 Degraus de carga 50 ↔ 100 %

| Grandeza | S (B) | Aceite |
|---|---|---|
| Afundamento / sobressinal de V<sub>o</sub> (90 V e 264 V) | 90 V: -114 mV na subida / +115 mV na descida; 264 V: -113 / +116 mV | dentro de 11,4–12,6 V |
| Retorno à faixa ± 1 % / ± 0,5 % | não sai de ± 1 % (desvio máx. 116 mV); ± 0,5 % em 4,4 ms | < 5 ms, sem oscilação sustentada |

### 5.4 Curto-circuito na saída – limites para liberar o ensaio

Comportamento previsto (simulação B, 220 V): ao aplicar o curto o primário sobe por alguns ciclos acima do limite (não há reset do núcleo com a saída em zero) até 8,0 A e V<sub>ds</sub> = 560 V; em seguida a limitação ciclo a ciclo segura I<sub>p</sub> em 3,4 A, D1 conduz 13,1 A eficazes e, com R13 = 100 Ω, o VCC cai e o CI **desliga por UVLO em ≈ 151 ms** (cálculo; simulação B: 163 ms até o UVLO, 130 ms desligado, 20 ms ligado por tentativa, ciclo de trabalho 14 % em 220 V). Ao remover o curto a fonte religa na tentativa seguinte do hiccup (até 130 ms) com a partida normal. O núcleo real satura acima de ≈ 3 A (B ≈ 0,35 T), o que **encurta** o transitório; os picos ficam dentro dos limites pulsados (Q1: 44 A; D1: I<sub>FSM</sub> 200 A).

Liberação do ensaio físico de curto **somente** se: (a) a simulação B mostrar o desligamento por UVLO e a recuperação (documentado em `06_Relatorio` §4.11); (b) o ensaio for feito com isolador, carga por chave de curto com resistência ≤ 50 mΩ e fio curto, a 127 V primeiro; (c) duração máxima de **2 s** no primeiro ensaio, com osciloscópio em TP3 (corrente) e VCC (TP5); (d) critério de parada: I<sub>p</sub> sustentada > 3,5 A, VCC não cair abaixo de 8 V em 300 ms (simulação: 163 ms), ou aquecimento de D1 > 100 °C. Só depois de confirmado o hiccup, estender para 30 s.

## 6. Diagnóstico rápido

| Sintoma | Causa provável | Ação |
|---|---|---|
| Não parte, VCC oscila entre 7,6 e 8,4 V | auxiliar invertido (pinos 4/5) ou N<sub>aux</sub> insuficiente; R13 muito alto para a carga | conferir fase (seção 3); medir V(pino 5) no bloqueio |
| V<sub>o</sub> sobe acima de 13 V e não regula | TL431 montado invertido (K-A-REF), opto invertido, R16/R17 | medir V<sub>KA</sub> (2–6 V) e corrente do LED |
| Fusível queima na primeira ligação | polaridade do primário invertida (forward), gap zero (saturação) | medir L<sub>p</sub> e conferir pontos |
| V<sub>ds</sub> > 550 V ou ringing forte | L<sub>lk</sub> alta, R5/R6 ou C2 errados, D2 lento | medir L<sub>lk</sub>; usar UF4007 |
| Ruído audível / instabilidade em carga leve | modo burst em 10 % (normal em modo corrente de pico MCD) | aceitar ou aumentar C<sub>z</sub> |
| R5/R6 > 80 °C | L<sub>lk</sub> > 3 % | refazer o enrolamento em sanduíche |
| Hiccup em operação normal (VCC cai) | R13 alto demais com o consumo real do CI/gate | reduzir R13 para 47 Ω e repetir o ensaio de curto |

## 7. Pontos de medição (revisão B)

TP1 BULK (+), TP2 DRAIN (dreno de Q1, **só sonda diferencial**), TP3 SW (tensão no R<sub>sense</sub> = corrente do primário × 0,34 Ω), TP4 GATE, TP5 VCC, TP6 VREF, TP7 COMP, TP8 CS (pino 3), TP9 PGND, TP10 VO, TP11 SGND. Corrente do secundário: sonda de corrente no laço JP2 (em série com os pinos 9/10 de T1 → ânodos de D1). Corrente de entrada: sonda de corrente no laço JP1 (fase, após o fusível) ou no cabo do isolador; potência de entrada por wattímetro de potência ativa (V<sub>ef</sub>·I<sub>ef</sub> dá potência aparente).
