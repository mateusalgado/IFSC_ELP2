# Projeto de uma fonte chaveada flyback 12 V / 3 A com entrada universal e controle por UC3845 — Revisão B

**Disciplina:** ELP22109 – Eletrônica de Potência II (2026-2) · **Projeto Semestral – Tema II**
**Aluno:** Mateus Salgado Barboza Costa · **Professor:** Joabel Moia · **Instituição:** IFSC – Campus Florianópolis, Engenharia Eletrônica
**Revisão B – novembro de 2026** (revisão A de 19/10/2026 preservada em `PROJETO/`; parecer técnico V1 de 04/11/2026 em `REVISAO_TECNICA_V1.pdf`)

> **Origem de cada resultado.** Neste relatório cada número é marcado por **[C]** cálculo (`02_Calculos`), **[S]** simulação LTspice da revisão B (`03_Simulacao/runs/medidas.json` e releitura dos `.raw`), **[CAD]** verificação de CAD (ERC/DRC do KiCad, `04_KiCad/drc_B.json`) ou **[M]** medição física. **Não há medições físicas nesta revisão**: o protótipo não foi montado.

## 1. Introdução

O objetivo deste trabalho é realizar o projeto completo de um conversor estático segundo o Tema II do projeto semestral: retificador em ponte completa a diodos com filtro capacitivo seguido de uma fonte chaveada **flyback**, com o circuito integrado dedicado **UC3845**, proteções contra surtos da rede, filtro de EMI, grampeamento de tensão sobre o transistor (snubber) e malha fechada da tensão de saída. O produto idealizado é uma fonte CA-CC de **36 W (12 V / 3 A)** com entrada universal **90–264 VAC**, da classe das fontes de mesa de roteadores, câmeras de CFTV, fitas de LED e automação. O enunciado prevê validação em 127 V e 220 V.

A revisão A foi submetida a um parecer técnico independente, que manteve a arquitetura e devolveu o projeto para correção antes de encomendar a placa ou energizar o primário, apontando: esforços em curto-circuito maiores que os publicados (9 A no MOSFET, 596 V no dreno) e ausência de desligamento; o grampo RCD com os resistores em série na placa (36,4 kΩ) em vez de em paralelo (9 kΩ) como no modelo; o filtro do sensor de corrente no lado errado do resistor; o choke de modo comum abaixo da corrente eficaz de entrada; classes de rede não atribuídas no projeto KiCad (regras de 1 mm e 6 mm sem efeito); instruções incompatíveis para o secundário do transformador no guia; e janelas de medição que omitiam os transitórios. Esta **revisão B** corrige cada item, refaz todas as simulações com janelas antes/durante/depois de cada evento, acrescenta a **proteção de curto-circuito por hiccup**, torna o DRC verificável (classes atribuídas e ensaio de cobertura das regras) e reorganiza a placa para um protótipo de teste confiável e para um produto com gabinete.

Com a revisão B fechada, optou-se pela **Possibilidade II** (protótipo): o pedido de compra, o cronograma até 21/12 e o registro de medições estão em `08_Montagem`; os resultados experimentais entrarão na revisão C. Este relatório ainda não contém medições.

## 2. Fundamentação teórica

### 2.1 Flyback em condução descontínua com controle por corrente de pico

Durante a condução do MOSFET (D·T) o primário recebe a tensão de *bulk* V<sub>b</sub> e a corrente cresce até I<sub>p</sub> = V<sub>b</sub>·D·T/L<sub>p</sub>, armazenando W = ½·L<sub>p</sub>·I<sub>p</sub>²; com o transistor bloqueado a energia é entregue ao secundário pelo diodo com I<sub>s,pk</sub> = n·I<sub>p</sub>, que decresce com (V<sub>o</sub>+V<sub>f</sub>)/L<sub>s</sub> durante D<sub>2</sub>·T. O projeto em **MCD** na pior condição (V<sub>b,mín</sub>, plena carga) segue a Aula 04C (Barbi): I<sub>p</sub> = 2·P<sub>o</sub>/(η·V<sub>b,mín</sub>·D<sub>máx</sub>), L<sub>p</sub> = V<sub>b,mín</sub>·D<sub>máx</sub>/(I<sub>p</sub>·f<sub>s</sub>), V<sub>r</sub> = D<sub>máx</sub>/(1−D<sub>máx</sub>)·V<sub>b,mín</sub> e n = V<sub>r</sub>/(V<sub>o</sub>+V<sub>f</sub>). No controle por **corrente de pico** o comparador do UC3845 encerra cada ciclo quando a tensão no resistor de sensoriamento atinge o limiar (COMP−1,4)/3 ≤ 1 V: a planta fica de primeira ordem e o limite de corrente é inerente — **mas só enquanto o núcleo é reiniciado a cada ciclo**. Com a saída em curto a tensão refletida cai a poucos volts, a corrente magnetizante não se extingue no bloqueio e cresce a cada ciclo pelo tempo mínimo de condução do CI (atraso do comparador, do driver e do filtro RC) até que as quedas resistivas do secundário forneçam o reset: é esse o mecanismo do transitório observado no curto e a razão de a proteção precisar de um segundo nível (desligamento por UVLO).

### 2.2 Estágio de entrada, proteções e qualidade de energia

A ponte com filtro capacitivo conduz perto do pico da rede (Aula 06): corrente pulsada, fator de potência 0,4–0,6 e THD elevada, aceitáveis para 36 W (abaixo dos 75 W da IEC 61000-3-2 classe D). O capacitor de *bulk* define a tensão mínima no vale (critério de 90 V do guia com margem para tolerância de −20 % e ESR) e as correntes eficazes nos diodos e no próprio capacitor. Proteções (Aula 07): fusível de ação lenta com tensão nominal igual ou superior à máxima da rede (500 V), NTC para o *inrush*, varistor 275 VAC, grampo RCD. Filtro de EMI (Aula 08): X2 (modo diferencial), choke de modo comum dimensionado para a corrente eficaz de entrada e Y1 entre os terras.

### 2.3 Transformador em alta frequência (Aula 04C)

A<sub>e</sub>A<sub>w</sub> = 1,1·P<sub>o</sub>·10⁴/(k<sub>w</sub>·k<sub>p</sub>·J·f<sub>s</sub>·B<sub>máx</sub>); l<sub>g</sub> = 2·µ<sub>0</sub>·W/(B²·A<sub>e</sub>); N<sub>p</sub> = B·l<sub>g</sub>/(µ<sub>0</sub>·I<sub>p</sub>); bitola limitada por Δ = 7,5/√f<sub>s</sub>; J = 450 A/cm²; K<sub>ocup</sub> ≤ 0,7; perdas no núcleo (IP12R) e no cobre; ΔT = P·R<sub>t</sub>, R<sub>t</sub> = 23·(A<sub>e</sub>A<sub>w</sub>)<sup>−0,37</sup>. O núcleo com entreferro satura em I<sub>sat</sub> ≈ I<sub>p</sub>·B<sub>sat</sub>/B<sub>máx</sub> (≈ 3 A para B<sub>sat</sub> = 0,35 T), o que limita, na prática, o transitório de curto (o modelo de simulação usa indutores lineares e portanto **não** representa a saturação).

### 2.4 Perdas e dissipadores (Aula 02)

Condução R<sub>DS(on)</sub>(T<sub>j</sub>)·I<sub>rms</sub>²; comutação ½·V·I·t<sub>f,ef</sub>·f<sub>s</sub> (ligação com corrente nula em MCD, só a descarga de C<sub>oss</sub>); diodo Schottky V<sub>0</sub>·I<sub>méd</sub> + R<sub>d</sub>·I<sub>rms</sub>². R<sub>θSA</sub> = (T<sub>j</sub>−T<sub>a</sub>)/P − R<sub>θJC</sub> − R<sub>θCS</sub>, com T<sub>j</sub> = 125 °C e T<sub>a</sub> = 40 °C (Tarefas 1 e 2). Em um encapsulamento isolado (TO-220FP) a aleta fica sem tensão, ao custo de R<sub>θJC</sub> maior.

### 2.5 Comando com o UC3845 (Aula 05)

Oscilador f<sub>osc</sub> ≈ 1,72/(R<sub>T</sub>·C<sub>T</sub>), flip-flop (f<sub>sw</sub> = f<sub>osc</sub>/2, D ≤ 50 %), comparador de corrente (1 V), UVLO 8,4/7,6 V, saída totem-pole de 1 A, partida por resistor do *bulk* e alimentação pelo auxiliar. **Hiccup:** se o auxiliar não sustenta o VCC (saída em curto), C<sub>VCC</sub> descarrega com I<sub>CC</sub> − I<sub>start</sub> até o UVLO, o CI desliga, R<sub>start</sub> recarrega até 8,4 V e o CI tenta de novo; o ciclo de trabalho da falha é t<sub>run</sub>/(t<sub>run</sub>+t<sub>recarga</sub>) e independe de C<sub>VCC</sub>. Para isso o resistor série do auxiliar precisa filtrar os picos de dispersão que, com 10 Ω, mantinham o VCC em 13 V no curto. Malha: TL431 + PC817, compensador tipo 2; o modelo de pequenos sinais inclui o banco de capacitores com ESR, o pós-filtro L2–C13 e o polo do optoacoplador (parecer, item 08).

### 2.6 Layout (Aula 08 e IPC-2221)

Fluxo linear, agrupamento por função, laços curtos, trilhas a 45°, terras de sinal e de potência unidos num único ponto, 100 nF junto ao VCC, larguras e isolamentos por corrente e tensão (IPC-2221), isolação primário–secundário ≥ 6,4 mm (IEC 62368-1) com fendas, planos de terra, pontos de teste e DFM. Na revisão B as regras passaram a ser **verificáveis**: classes atribuídas a todas as redes e ensaio de cobertura com violações deliberadas numa cópia.

## 3. Materiais e métodos

Mesma cadeia automatizada da revisão A (Python/numpy, LTspice em lote, KiCad 10 por `kicad-cli` e `pcbnew`), com as alterações da B:

1. **Referência elétrica única** (parecer, passo 1): `02_Calculos` → `04_KiCad/gera_sch.py` → `netlist.net` → `05_BOM_Custo/bom.py`. Valores da B: C1 150 µF/400 V (18 × 40 mm), fusível axial T2A/500 V (Littelfuse 477), choke Schaffner RN214 2 × 10 mH / 1,2 A (pinos 1-2 e 3-4), R5 ∥ R6 = 9 kΩ (2 × 18 kΩ 2 W em paralelo no esquemático e na placa), filtro do ISENSE R11 = 330 Ω / C3 = 100 pF **no pino 3** (τ = 33 ns), R9 ∥ R10 = 2 × 0,68 Ω = 0,34 Ω, compensador R<sub>z</sub> = 21,5 kΩ / C<sub>z</sub> = 270 nF (f<sub>c</sub> ≈ 0,8 kHz), TL431 com footprint próprio K-A-REF (1-2-3, TI tabela 5-1), Y1 com passo 10 mm, **R13 = 100 Ω** no auxiliar (hiccup), **Q1 = STF13N65M2** (TO-220FP isolado; mesmo die do STP13N65M2 usado no modelo).
2. **Simulação** (`03_Simulacao/gera_netlist.py`, `executa_b.py`): modelo comportamental do UC3845 (UVLO 8,5/7,9 V no modelo, I<sub>start</sub> 0,5 mA), VDMOS do STP13N65M2, TL431/PC817 comportamentais, L<sub>lk</sub> = 2 %, ESR explícitas. 23 casos: regime 90/127/220/264 V × 10/50/100 % (6 ciclos de rede, medição nos 2 últimos); **partida a frio** em 90 e 264 V (pré-carga de C1 e C5 descarregados com I<sub>start</sub> máximo até o UVLO, transferindo tensão de barramento e **fase da rede** do cruzamento para o início do chaveamento); degraus 50 → 100 % (80 ms) e 100 → 50 % (100 ms) em 90 e 264 V e com CTR = 0,5; curto de **60 a 380 ms** em 220 V com medições separadas na aplicação (2 ms), no curto sustentado e na recuperação; tolerância do barramento (C1 = 120 µF, −20 %); sem grampo; L<sub>lk</sub> = 3 %. Os `.raw` (0,3–1,3 GB) são relidos por `analisa_curto.py` e `analisa_transitorios.py` para as janelas; as tabelas do relatório vêm de `06_Relatorio/gera_tabelas.py`.
3. **Esquemático e placa**: `gera_sch.py` (ERC), `placement.py` (sem sobreposições), `router.py` + `completa_rotas.py` (busca em grade para os ramos /DRV e /CS), `gera_pcb.py`, DRC com paridade e preenchimento de zonas, `utils/testa_regras.py` (cobertura do DRC), exportação de Gerbers/furação/3D da mesma revisão.
4. **BOM e custo** (`bom.py` → `BOM.xlsx`, `custo.xlsx`), **guia de montagem B** (`08_Montagem`, pinagem do T1 fixada, instrumentação com isolador e sonda diferencial, curto bloqueado até os limites) e **Tarefa Extra** (modelo).

Hipóteses: η = 0,82; D<sub>máx</sub> = 0,43; B<sub>máx</sub> = 0,25 T; J = 450 A/cm²; k<sub>w</sub> = 0,4; k<sub>p</sub> = 0,3; grampo em 1,8·V<sub>r</sub>; L<sub>lk</sub> = 2 % (verificação a 3 %); T<sub>a</sub> = 40 °C; T<sub>j</sub> = 125 °C; para manter o transformador da A, o vale de projeto de T1 ficou em 94,6 V (conservador) embora com 150 µF o vale calculado em 90 V/50 Hz seja 104,1 V [C].

## 4. Resultados

### 4.1 Requisitos e estágio de entrada [C]

| Grandeza | Valor |
|---|---|
| Entrada | 90–264 VAC, 50/60 Hz (nominais 127 e 220 V) |
| Saída | 12,0 V ± 5 %, 0,3–3,0 A (36 W), ondulação ≤ 120 mV p-p |
| Comutação | 65 kHz (UC3845, D ≤ 0,5) |
| Rendimento | meta 85 % em 220 V (critério fixado); hipótese de cálculo 82 % |
| Proteções | fusível T2A/500 V, NTC 10 Ω, MOV S14K275, limite ciclo a ciclo, **hiccup por UVLO no curto**, grampo RCD |
| EMI | X2 220 nF + choke MC 2 × 10 mH (1,2 A) + X2 100 nF, Y1 2,2 nF |
| Isolação | transformador + opto; ≥ 6,4 mm na PCI (verificado pelo DRC) |

Com **C1 = 150 µF / 400 V**: V<sub>bulk,mín</sub> = 104,1 V em 90 V/50 Hz (82 µF daria 88 V, abaixo do critério de 90 V do guia; 120 µF, −20 % de tolerância, dá ≈ 100 V — caso simulado em 4.6), corrente eficaz no capacitor 0,80 A, corrente eficaz de entrada **0,89 A** em 90 V → choke de **1,2 A** (o Würth 744821110 da A era de 0,7 A / 250 VCA), fusível T2A/500 V (2,5 × I<sub>rms</sub>; interrupção 1500 A conforme catálogo Littelfuse 477), ponte GBU4J (0,19 A médios por diodo, V<sub>RRM</sub> 600 V), inrush 31 A com NTC (187 A sem).

![Figura 1 – Estágio de entrada: tensão de bulk e corrente da rede (entrada.py, revisão B).](assets/entrada_formas_de_onda.png)

### 4.2 Flyback e transformador [C]

Projeto preliminar com V<sub>b,mín</sub> = 94,6 V (conservador) e D<sub>máx</sub> = 0,43: V<sub>r</sub> = 71,3 V, n = 5,62, I<sub>p</sub> = 2,16 A, L<sub>p</sub> = 290 µH. Núcleo **Thornton E-30/7 (NEE-30/15/7, IP12R)**: l<sub>g</sub> = 0,45 mm, **N<sub>p</sub> = 42, N<sub>s</sub> = 7, N<sub>aux</sub> = 9**, L<sub>p</sub> = 294 µH, B<sub>pico</sub> = 0,25 T, fios 1 × 23 AWG (primário), 5 × 23 AWG (secundário), 1 × 28 AWG (auxiliar), perdas 0,96 W, ΔT = 29 °C, K<sub>ocup</sub> = 0,46 (tabela 1). Com o vale real de 104 V (150 µF) a razão cíclica em 90 V/plena carga cai a 0,39 e o modo continua MCD. A ficha de fabricação (pinagem 1-BULK, 3-DRAIN, 4-PGND, 5-AUX, 6/7-SGND, 9/10-ânodos de D1, 2 e 8 livres; ordem de camadas; ensaios de L<sub>p</sub>, L<sub>lk</sub>, relação e fase) está no guia de montagem §3.

**Tabela 1 – Núcleos candidatos [C].**

| Núcleo | A<sub>e</sub>A<sub>w</sub> (cm⁴) | l<sub>g</sub> (mm) | N<sub>p</sub>/N<sub>s</sub>/N<sub>aux</sub> | L<sub>p</sub> (µH) | P núcleo (W) | P cobre (W) | ΔT (°C) | K<sub>ocup</sub> |
|---|---|---|---|---|---|---|---|---|
| **E-30/7** | 0,48 | 0,45 | 42/7/9 | 294 | 0,62 | 0,35 | 29,1 | 0,46 |
| E-30/14 | 1,02 | 0,23 | 21/3/4 | 294 | 1,23 | 0,19 | 32,4 | 0,22 |
| E-42/15 | 2,84 | 0,15 | 14/2/3 | 297 | 2,63 | 0,16 | 43,7 | 0,08 |

![Figura 2 – Formas de onda teóricas do flyback em 90 e 264 VAC, plena carga (flyback.py).](assets/flyback_formas_de_onda.png)

Esforços teóricos (tabela 2): I<sub>p</sub> = 2,14 A em toda a faixa (MCD), V<sub>ds</sub> máx = **507 V** em 264 V com grampo a 1,8·V<sub>r</sub>, V<sub>rev</sub> do diodo 74 V, I<sub>s,rms</sub> = 5,45 A, I<sub>c,rms</sub> = 4,54 A.

**Tabela 2 – Esforços teóricos por ponto de operação [C].**

| V<sub>ac</sub> | carga | D | I<sub>p</sub> (A) | I<sub>p,rms</sub> (A) | I<sub>s,pk</sub> (A) | I<sub>s,rms</sub> (A) | I<sub>c,rms</sub> (A) | V<sub>ds</sub> grampo (V) | V<sub>d,rev</sub> (V) |
|---|---|---|---|---|---|---|---|---|---|
| 90 | 100 % | 0,393 | 2,14 | 0,776 | 12,9 | 5,45 | 4,54 | 261 | 33 |
| 127 | 100 % | 0,258 | 2,14 | 0,629 | 12,9 | 5,45 | 4,54 | 314 | 41 |
| 220 | 100 % | 0,138 | 2,14 | 0,460 | 12,9 | 5,45 | 4,54 | 445 | 63 |
| 264 | 100 % | 0,114 | 2,14 | 0,418 | 12,9 | 5,45 | 4,54 | 507 | 74 |
| 264 | 10 % | 0,036 | 0,68 | 0,074 | 4,1 | 0,97 | 0,92 | 507 | 74 |

### 4.3 Capacitores, filtro de saída e snubber [C]

Saída: 3 × Rubycon ZLH 1000 µF/25 V (RSE 6,3 mΩ, I<sub>ripple</sub> 6,0 A ≥ 4,54 A, ΔV<sub>1</sub> = 89 mV) + pós-filtro 3,3 µH (Bourns RLB0914, I<sub>sat</sub> 11 A) / 470 µF → ondulação teórica 2,7 mV (fig. 3). Bulk 150 µF/400 V 105 °C (Nichicon UCY2G151MHD); VCC 220 µF/35 V + 100 nF; VREF 1 µF; C<sub>T</sub> 2,2 nF C0G; X2 220 nF e 100 nF; Y1 2,2 nF (passo 10 mm); snubber 22 nF/630 V de filme. **Snubber RCD**: R = 9 kΩ (**2 × 18 kΩ / 2 W em paralelo**, 2,0 W no conjunto com L<sub>lk</sub> 2 %; 2,6 W a 3 %), C = 22 nF/630 V, UF4007; V<sub>ds</sub> = 507/524 V (fig. 4). RC do diodo de saída 15 Ω + 2,2 nF/100 V (valor comercial instalado e simulado).

![Figura 3 – Ondulação de saída no banco e após o pós-filtro (saida.py).](assets/saida_ripple.png)

![Figura 4 – Compromisso potência × tensão de grampo do snubber (snubber.py).](assets/snubber_compromisso.png)

### 4.4 Diodos, transistor, perdas e dissipadores [C]

Pré-escolha: MOSFET 650 V (V<sub>ds</sub> ≤ 80 %), diodo Schottky 100 V/≥ 10 A, ponte 600 V/4 A. Entre os MOSFETs candidatos (tabela 3) as perdas são equivalentes (1,15 W no pior caso) e a revisão B escolhe o **STF13N65M2 em TO-220FP (isolado)**: R<sub>θJC</sub> 3,5 °C/W, T<sub>j</sub> ≈ 72 °C com o clip de 24 °C/W, **sem mica e com a aleta sem potencial** — no TO-220 metálico da A a aleta ficava no potencial do dreno (≈ 500 V). Sem dissipador T<sub>j</sub> seria 112 °C: o dissipador é necessário. **Diodo STPS20H100CT** (2 × 10 A em paralelo): 1,78 W, clip → T<sub>j</sub> ≈ 84 °C (sem dissipador ≈ 150 °C: necessário). Ponte GBU4J: 0,67 W, T<sub>j</sub> ≈ 53 °C sem dissipador. Resistores quentes: R5/R6 (1,0 W cada), R3/R4 (0,42 W cada a 264 V), NTC — afastados dos eletrolíticos na placa.

**Tabela 3 – MOSFETs candidatos [C].**

| MOSFET | R<sub>DS(on)</sub> (mΩ) | P<sub>tot</sub> 90 V (W) | P<sub>tot</sub> 264 V (W) | R<sub>θJC</sub> (°C/W) | isolado | T<sub>j</sub> com clip (°C) |
|---|---|---|---|---|---|---|
| IPA65R400CE (TO-220FP) | 400 | 1,14 | 1,38 | 4,0 | sim | 79 |
| STP13N65M2 (TO-220) | 430 | 1,04 | 1,15 | 1,14 | não | 69 |
| **STF13N65M2 (TO-220FP)** | 430 | 1,04 | 1,15 | 3,5 | **sim** | **72** |
| FCPF190N65S3 (TO-220F) | 190 | 0,83 | 1,40 | 3,5 | sim | 79 |

![Figura 5 – Distribuição de perdas em plena carga (semicondutores.py).](assets/perdas_semicondutores.png)

**Tabela 4 – Orçamento de perdas em plena carga [C] (W).**

| V<sub>ac</sub> | MOSFET | diodo | ponte | trafo | snubber | R<sub>sense</sub> | partida | cap. saída | NTC | L<sub>LC</sub> | UC3845 | total | η (%) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 90 | 0,98 | 1,78 | 0,67 | 0,95 | 2,02 | 0,20 | 0,09 | 0,13 | 0,79 | 0,09 | 0,22 | 7,94 | 81,9 |
| 127 | 0,98 | 1,78 | 0,45 | 0,90 | 2,02 | 0,13 | 0,19 | 0,13 | 0,48 | 0,09 | 0,22 | 7,39 | 83,0 |
| 220 | 1,15 | 1,78 | 0,24 | 0,87 | 2,02 | 0,07 | 0,58 | 0,13 | 0,23 | 0,09 | 0,22 | 7,39 | 83,0 |
| 264 | 1,15 | 1,78 | 0,20 | 0,86 | 2,02 | 0,06 | 0,83 | 0,13 | 0,18 | 0,09 | 0,22 | 7,53 | 82,7 |

### 4.5 Componentes do CI, driver, proteção de curto e malha de realimentação [C]

R<sub>T</sub> = 6,04 kΩ, C<sub>T</sub> = 2,2 nF → f<sub>sw</sub> = 64,7 kHz. **R<sub>s</sub> = 0,34 Ω** (2 × 0,68 Ω / 1 W): limite 2,65–2,94 A; **filtro 330 Ω / 100 pF no pino 3** (τ = 33 ns, atraso mínimo para reduzir o excesso de corrente na aplicação do curto). Partida 2 × 82 kΩ / 1 W (I<sub>start</sub> ≥ 0,5 mA no vale de 90 V): tempo até o UVLO de 1,0–4,3 s com I<sub>CC,start</sub> típico de 0,3 mA [C] e de 1,1 s (264 V) a **7,4 s (90 V)** com o máximo de 0,5 mA [S, pré-carga] — partida lenta em rede baixa, aceitável para fonte de mesa, mas um produto pediria 2 × 68 kΩ ou partida ativa; C<sub>VCC</sub> 220 µF (sustenta 9,2 ms entre 8,4 e 7,6 V; o auxiliar assume em < 6 ms [S]). Auxiliar 15,4 V com UF4004 + **R13 = 100 Ω**. **Proteção de curto (hiccup):** com a saída em curto o auxiliar cai a ≈ 0,9 V, o VCC descarrega com I<sub>CC</sub> − I<sub>start</sub> até 7,6 V, o CI desliga e religa após a recarga por R<sub>start</sub> (tabela 5): em 220 V o ciclo de trabalho da falha calculado é ≈ 10 % [C]; a simulação [S] dá 155 ms até o UVLO, 97 ms de recarga e 15 ms ligado por tentativa (ciclo de trabalho 13 %), o que reduz a corrente eficaz média de D1 no curto a ≈ √0,13 ≈ 0,37 do valor sustentado. Driver: saída totem-pole do UC3845 (R<sub>g</sub> 10 Ω + 1N4148 + 10 kΩ). Compensação de rampa: desnecessária (MCD, D < 0,5).

**Tabela 5 – Hiccup calculado [C] (C<sub>VCC</sub> = 220 µF, I<sub>CC</sub> = 13 mA).**

| V<sub>ac</sub> | t até UVLO (ms) | t recarga (ms) | t ligado por tentativa (ms) | ciclo de trabalho da falha (%) |
|---|---|---|---|---|
| 90 | 138 | 854 | 14,1 | 1,6 |
| 127 | 141 | 335 | 14,5 | 4,1 |
| 220 | 151 | 133 | 15,5 | 10,4 |
| 264 | 157 | 103 | 16,0 | 13,4 |

**Malha:** divisor R<sub>a</sub> = 9,53 kΩ / R<sub>b</sub> = 2,49 kΩ (12,04 V), R<sub>LED</sub> = 2,74 kΩ, R<sub>bias</sub> = 1 kΩ, pull-up 4,7 kΩ, C<sub>p</sub> = 1 nF. O modelo da planta da B inclui o banco de capacitores com RSE, o pós-filtro L2–C13 (ressonância ≈ 4 kHz) e um polo do opto em 10 kHz; o compensador tipo 2 com **R<sub>z</sub> = 21,5 kΩ, C<sub>z</sub> = 270 nF** cruza em 0,79 kHz com **margem de fase 88°** e margem de ganho 13 dB em plena carga, mantendo-se ≥ 86° para 10 % de carga e CTR de 0,5 a 1,6 (fig. 6). A margem é um resultado do modelo [C]; os degraus simulados [S] confirmam a ausência de oscilação, mas não medem a margem.

![Figura 6 – Bode da planta com pós-filtro, compensador e malha aberta (compensador.py, revisão B).](assets/compensador_bode.png)

**Filtro de EMI:** choke 2 × 10 mH (Schaffner RN214-1.2-02-10M, 1,2 A a 40 °C, R<sub>dc</sub> 195 mΩ), X2 220 nF + 100 nF, Y1 2,2 nF, 2 × 470 kΩ: f<sub>DM</sub> ≈ 43 kHz, f<sub>CM</sub> ≈ 24 kHz (fig. 7); curva ideal — a medição com LISN fica para o protótipo.

![Figura 7 – Atenuação estimada do filtro de EMI (emi.py).](assets/emi_atenuacao.png)

### 4.6 Simulação da revisão B e comparação com a teoria [S]

**Regime permanente (tabela 6).** Medições nos dois últimos ciclos de rede de seis simulados; a ondulação é dada separadamente como ondulação de chaveamento (20 períodos) e excursão total em ciclos inteiros da rede (parecer, item "partida e ondulação").

**Tabela 6 – Teoria [C] × simulação [S] em regime permanente.**

{{regime}}

**Tabela 7 – Perdas e rendimento em plena carga [C] × [S].**

{{perdas}}

![Figura 8 – Um ciclo de comutação em 90 VAC e 264 VAC, plena carga [S].](assets/regime_90V_100pct_ciclo.png)

![Figura 8b – Comutação em 264 VAC, plena carga: dreno com o grampo RCD [S].](assets/regime_264V_100pct_comut.png)

**Transitórios (tabela 8).** Partida a frio: pré-carga com C1 e C5 descarregados e I<sub>start</sub> máximo (0,5 mA) até o UVLO; a tensão de barramento e a fase da rede nesse instante são transferidas ao modelo de chaveamento. Degraus nos dois sentidos após estabilização. Tolerância do barramento com C1 = 120 µF.

**Tabela 8 – Transitórios [S].**

{{transitorios}}

![Figura 9 – Partida a frio em 90 VAC: bulk, VCC e saída [S].](assets/partida_90V_rede.png)

![Figura 9b – Degraus de carga 50 → 100 → 50 % em 90 VAC [S].](assets/degrau_90V_rede.png)

**Curto-circuito (tabela 9, figs. 10–11).** O curto é aplicado em 60 ms e mantido até 380 ms. Na **aplicação**, a corrente do primário sobe por alguns ciclos acima do limite — não há reset do núcleo com a saída em zero — até 7,8 A (0,91 T no modelo linear; o núcleo real satura em ≈ 3 A, o que encurta o transitório), I(D1) chega a 55 A e V<sub>ds</sub> a 555 V (margem de falha fixada em 600 V, 92 % de 650 V, para pulsos). No **curto sustentado** a limitação ciclo a ciclo segura I<sub>p</sub> em 3,3 A e D1 conduz 12,5 A eficazes com 5,7 W; com R13 = 100 Ω o VCC cai e o CI **desliga por UVLO** (VCC mínimo 7,9 V), religando após a recarga (155 ms até o primeiro desligamento, 97 ms desligado, 15 ms ligado por tentativa) — comportamento que **não existia na revisão A** (VCC ficava em 13 V e o curto era sustentado indefinidamente). Na **recuperação** o curto é removido (380 ms) com o CI desligado no hiccup: a saída permanece em zero até o próximo cruzamento do UVLO (VCC = 8,48 V no fim dos 40 ms simulados, religamento ≈ 4 ms depois) e a sequência seguinte é a partida normal da fig. 9, sem sobretensão [S]; o tempo de recuperação é, portanto, até um período de recarga (97 ms em 220 V).

**Tabela 9 – Curto-circuito em 220 VAC por janelas [S].**

{{curto}}

![Figura 10 – Curto-circuito em 220 VAC: janela completa (aplicação, sustentado com hiccup, recuperação) [S].](assets/curto_220V_janelas.png)

![Figura 11 – Curto-circuito em 220 VAC: zoom na aplicação (transitório sem reset do núcleo) [S].](assets/curto_220V_aplicacao.png)

![Figura 12 – Dreno sem grampo (264 VAC) [S].](assets/sem_snubber_264V_comut.png)

**Análise.** A tensão de saída fica entre 12,06 e 12,06 V em toda a faixa (regulação de linha e carga < 0,1 %). Em plena carga a corrente de pico do primário difere -3,7 % da teoria (limiar efetivo do comparador e atraso do filtro), I<sub>s,pk</sub> +10,1 %, I<sub>s,rms</sub> -10,2 % (a teoria integra o triângulo ideal no vale de V<sub>bulk</sub>) e V<sub>ds</sub> -4,9 % em 264 V (grampo real abaixo de 1,8·V<sub>r</sub>). Em carga leve a diferença de V<sub>ds</sub> (grampo mais baixo com menos energia de dispersão) e de I<sub>s,pk</sub> excede 10 % a favor da segurança: os casos excedidos estão listados na tabela 10 com as hipóteses do cálculo (triângulo ideal no vale de V<sub>bulk</sub>, grampo fixo em 1,8·V<sub>r</sub>). O rendimento simulado em 220 V/3 A é 85,3 % (meta 85 %; cálculo 83,0 %), com o grampo (1,32 W) e o diodo (1,72 W) como maiores parcelas.

**Tabela 10 – Verificação dos critérios de projeto.**

{{criterios}}

### 4.7 Esquemático [CAD]

Esquemático B (fig. 13; `04_KiCad/fonte_flyback_12V3A_esquematico.pdf`): ERC **0 erros, 0 avisos** (`erc.json`); 69 itens na netlist (54 componentes elétricos, 11 pontos de teste, 4 furos), 33 redes; R5 ∥ R6, C3 no pino 3, TL431 K-A-REF, choke 1-2/3-4, R13 100 Ω, Q1 STF13N65M2. Netlist, BOM e desenho do transformador descrevem a mesma ligação (parecer, passo 1).

![Figura 13 – Esquemático revisão B (KiCad 10).](assets/esquematico.png)

### 4.8 Lista de materiais e custo

BOM B (`05_BOM_Custo/BOM.xlsx`, 58 itens): orçamento de engenharia com preços herdados da A e provisões para os itens trocados (sem cotação de compra): **US$ 42,73 por fonte com a PCI rateada em 5 placas** (≈ R$ 235) e **US$ 22,37 em 100 unidades**. Para montar um único exemplar comprando o lote mínimo de 5 placas a saída de caixa é ≈ US$ 81 (42,73 − 9,60 + 48) antes de fretes, impostos e mínimos (parecer, item 11). Blocos: PCI 22 %, filtro EMI 14 %, secundário 12 %, transformador 10 %; o kit de mica foi retirado (Q1 isolado) e C9 fixado em 2,2 nF; em 05/11 o fusível axial soldado deu lugar a fusível 5 × 20 T2A/250 V em clipes (porta-fusível para os ensaios; o axial fica para o produto) e entraram os laços de fio JP1/JP2 para sonda de corrente (Aula 08).

### 4.9 Layout da PCI [CAD]

Placa B 140 × 90 mm, 2 camadas, todos PTH (fig. 14–16). Mudanças em relação à A, motivadas pelo parecer e pela orientação de placa de teste confiável e produto com gabinete: classes de rede atribuídas (HV, SEC, SEC_PWR; T1.8 como secundário) e regra de isolação incluindo SEC_PWR; laço SGND do Y1 com 1,5 mm; conector da rede afastado do furo de fixação (parafuso de gabinete pode ser PE); saída J2 na borda direita; D1 afastado dos eletrolíticos; Q1 isolado com clip sem tensão. **Placement revisto em 05/11/2026, antes do pedido da PCI** (análise região a região em `04_KiCad/ANALISE_PLACEMENT.md`): J1 na borda esquerda abrindo para fora e J2 na direita (cabos em faces opostas da caixa); filtro de entrada em coluna J1 → F1 → JP1 → RV1/RT1 → R1/R2 → CX1 → L1 → CX2 → BR1, com CX1 encostado nos pinos de entrada de L1 (redes da rede de 80 para 54 mm); porta-fusível 5 × 20 de clipes (troca sem dessoldar nos ensaios); laços de fio JP1 (fase) e JP2 (secundário) para sonda de corrente (Aula 08: "em protótipos, prever pontos de medida de corrente"); Q1 deslocado para junto de T1 (dreno a 15,7 mm do pino 3, era 24,8) e com o clip a 6 mm do corpo de C1 (era 3,5); eletrolíticos de saída com passo 12 mm; serigrafia de segurança (valor do fusível junto a F1, L/N em J1, +12 V/0 V em J2, aviso do C1 de 400 V); regra de isolação primário–secundário elevada para **6,4 mm** (IEC 62368-1, reforçada, 250 V), com exceção documentada de 6,0 mm só sob a fenda do opto (DIP-4 de 7,62 mm; a fenda interrompe a linha de fuga, IEC 60664-1), e o roteador passou a limitar o cobre (e não o eixo) das trilhas. **DRC: 0 erros, 0 itens não conectados, 0 divergências com o esquemático**; 3 avisos de serigrafia justificados (opto sobre a fenda; marca "K" do D3). **Ensaio de cobertura:** numa cópia com cinco violações deliberadas cada regra disparou (`HV_clearance`, `isolacao_prim_sec`, `largura_HV`, `largura_SEC_potencia`, `borda`); sem a exceção do opto o DRC acusa 8 violações, todas em U3. 255 cantos a 45° (21 ângulos retos: 19 saídas de pad, 2 a 0,1 mm de um pad); menor distância entre pads de componentes diferentes 0,95 mm (sinal); pads da rede a ≥ 8,5 mm dos furos e ≥ 7 mm da borda. Detalhes, avaliação térmica/mecânica para gabinete e pendências de produto em `04_KiCad/VERIFICACAO_LAYOUT.md`; fabricação em `04_KiCad/gerbers/` (Gerbers RS-274X, furação Excellon e mapa, **da mesma revisão B**, inspecionados junto com as fendas no `imagens/pcb_camadas.pdf`).

![Figura 14 – Face superior da PCI B.](assets/pcb_F.Cu.png)

![Figura 15 – Face inferior: planos PGND (com a ilha de sinal) e SGND.](assets/pcb_B.Cu.png)

![Figura 16 – Render 3D da placa B (dissipadores e corpo de T1 não representados nos modelos 3D).](assets/pcb_3d_iso.png)

### 4.10 Montagem e ensaio (Possibilidade II em execução)

`08_Montagem/GUIA_MONTAGEM.md` (B): ficha de fabricação de T1 com pinagem única (6/7 SGND, 9/10 ânodos de D1, 4 PGND, 5 auxiliar), ensaios de L<sub>p</sub>, L<sub>lk</sub>, relação e fase antes de montar; montagem por blocos; instrumentação com transformador isolador, terra de proteção do osciloscópio mantido e sonda diferencial; descarga de C1 (10 J) com 4,7 kΩ/10 W e confirmação com multímetro; tabela de aceite com origem C/S/M; **curto-circuito físico bloqueado** até os limites da seção 5.4 (duração 2 s, parada por I<sub>p</sub> > 3,5 A ou VCC sem cair). Para a execução: `PEDIDO_COMPRA.md` (56 itens, ≈ US$ 111 com sobressalentes e lote de 5 placas), `CRONOGRAMA.md` (pedido até 10/11, T1 na semana 2, blocos nas semanas 4–5, ensaios na 6, revisão C na 7) e `REGISTRO_MEDICOES.md` com as células [M] em branco. Nenhum resultado experimental existe nesta revisão.

## 5. Conclusão

A revisão B responde ao parecer técnico com uma referência elétrica única (esquemático, netlist, BOM e desenho do transformador descrevendo a mesma peça e ligação), simulações refeitas com janelas antes/durante/depois de cada evento e uma proteção de curto-circuito efetiva: o transitório de aplicação do curto permanece (é inerente ao flyback sem reset com saída em zero e fica dentro dos limites pulsados dos semicondutores — 7,8 A e 555 V no modelo, menos no núcleo real por saturação), mas o curto sustentado agora termina em **desligamento por UVLO e hiccup** graças ao resistor de 100 Ω no auxiliar. Em regime a simulação B dá V<sub>o</sub> = 12,06–12,06 V, ondulação ≤ 4,2 mV, V<sub>ds</sub> = 482 V em 264 V (74 % de 650 V), partida a frio e degraus nos dois sentidos estáveis e rendimento de 85,3 % em 220 V. A placa B tem DRC com classes atribuídas e cobertura comprovada das regras, zero itens não conectados, paridade com o esquemático, dissipadores dimensionados (necessários em Q1 e D1), MOSFET isolado, conectores e distâncias pensados para gabinete, e pacote de fabricação da mesma revisão. Permanecem como trabalho futuro a medição de L<sub>lk</sub> e da saturação do transformador real, o ensaio de emissões conduzidas e, se houver bancada, o protótipo com o roteiro preparado.

## 6. Referências bibliográficas

1. MOIA, J. *Apresentações das Aulas 01 a 08 – Eletrônica de Potência II*. IFSC, 2026.
2. *Parecer sobre a primeira versão – Tema II, fonte flyback isolada de 12 V e 3 A* (REVISAO_TECNICA_V1.pdf), 04/11/2026.
3. BARBI, I. *Projeto de fontes chaveadas*. Florianópolis: Edição do Autor, 2003.
4. BARBI, I. *Eletrônica de potência*. 5. ed. Florianópolis: Edição do Autor, 2005.
5. ERICKSON, R. W.; MAKSIMOVIĆ, D. *Fundamentals of power electronics*. 2. ed. Kluwer, 2001.
6. MOHAN, N.; UNDELAND, T.; ROBBINS, W. *Power electronics: converters, applications and design*. 2. ed. Wiley, 1995.
7. TEXAS INSTRUMENTS. *UCx84x Current-Mode PWM Controllers* (SLUS223H), 2024; *TL431 / TL432* (SLVS543), tabela 5-1.
8. STMICROELECTRONICS. *STP13N65M2 / STF13N65M2* (DS10587); *STPS20H100CT*; *UC3845B*.
9. SCHAFFNER. *RN series common-mode chokes* (RN214); LITTELFUSE. *215 series 5 × 20 mm ceramic fuses* e *477 series*; KEYSTONE. *3517 fuse clips*; NICHICON. *UCY series*.
10. THORNTON ELETRÔNICA. *Núcleos de ferrite NEE – IP12R*.
11. IPC. *IPC-2221B – Generic Standard on Printed Board Design*, 2012.
12. TEKTRONIX. *Fundamentals of floating measurements and isolated input oscilloscopes* (application note).
13. ANALOG DEVICES. *LTspice – Help*; KICAD. *KiCad 10 documentation – kicad-cli, custom design rules*.
14. IFSC. *Plano de Ensino – ELP22109, 2026-2*; *Projeto Semestral 2026-2*; *Tarefa Extra*.
