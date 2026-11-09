# Projeto de uma fonte chaveada flyback 12 V / 3 A com entrada universal e controle por UC3845

**Disciplina:** ELP22109 – Eletrônica de Potência II (2026-2) · **Projeto Semestral – Tema II**
**Aluno:** Mateus Salgado Barboza Costa · **Professor:** Joabel Moia · **Instituição:** IFSC – Campus Florianópolis, Engenharia Eletrônica
**Data:** dezembro de 2026

## 1. Introdução

O objetivo deste trabalho é realizar o projeto completo de um conversor estático segundo o Tema II do projeto semestral: retificador em ponte completa a diodos com filtro capacitivo seguido de uma fonte chaveada **flyback**, com o circuito integrado dedicado **UC3845**, proteções contra surtos da rede, filtro de EMI, grampeamento de tensão sobre o transistor (snubber) e malha fechada da tensão de saída. O produto idealizado é uma fonte de alimentação CA-CC de **36 W (12 V / 3 A)** com entrada universal **90–264 VAC**, da mesma classe das fontes de mesa de roteadores, modems, câmeras de CFTV, fitas de LED e pequenos equipamentos de automação. O enunciado prevê validação em 127 V e 220 V, de modo que o projeto cobre as duas redes brasileiras com margem.

O circuito recebe a rede, limita o surto de ligação (NTC), absorve sobretensões (varistor), filtra a interferência conduzida (X2, choke de modo comum, Y1), retifica e armazena energia no capacitor de *bulk*, e transfere a energia ao secundário por um transformador flyback comutado a 65 kHz por um MOSFET de 650 V comandado em modo corrente de pico pelo UC3845. A saída é retificada por um diodo Schottky, filtrada por um banco de capacitores de baixa RSE e um pós-filtro LC, e regulada por uma malha com TL431 e optoacoplador, que mantém a isolação galvânica.

Foi adotada a **Possibilidade I** (projeto sem bancada, com a Tarefa Extra), mas todos os entregáveis foram preparados para servir à Possibilidade II: a placa está roteada, verificada e com Gerbers prontos, há lista de compra e um guia de montagem e ensaio (`08_Montagem/GUIA_MONTAGEM.md`), de modo que a decisão de montar o protótipo pode ser tomada com o custo e o prazo conhecidos.

## 2. Fundamentação teórica

### 2.1 Conversor flyback em condução descontínua com controle por corrente de pico

No flyback, durante a condução do MOSFET (intervalo D·T) o primário do transformador (na verdade um indutor acoplado) recebe a tensão de *bulk* V<sub>b</sub> e a corrente cresce linearmente até I<sub>p</sub> = V<sub>b</sub>·D·T/L<sub>p</sub>, armazenando a energia W = ½·L<sub>p</sub>·I<sub>p</sub>²; com o transistor bloqueado, a energia é entregue ao secundário pelo diodo, com corrente de pico I<sub>s,pk</sub> = n·I<sub>p</sub> (n = N<sub>p</sub>/N<sub>s</sub>), que decresce com inclinação (V<sub>o</sub>+V<sub>f</sub>)/L<sub>s</sub> durante D<sub>2</sub>·T. Projetou-se o conversor em **modo de condução descontínua (MCD)** na pior condição (V<sub>b,mín</sub> em 90 VAC e plena carga), pelo método da Aula 04C (Barbi): I<sub>p</sub> = 2·P<sub>o</sub>/(η·V<sub>b,mín</sub>·D<sub>máx</sub>), L<sub>p</sub> = V<sub>b,mín</sub>·D<sub>máx</sub>/(I<sub>p</sub>·f<sub>s</sub>) e tensão refletida V<sub>r</sub> = D<sub>máx</sub>/(1−D<sub>máx</sub>)·V<sub>b,mín</sub>, o que define n = V<sub>r</sub>/(V<sub>o</sub>+V<sub>f</sub>). No MCD a potência transferida é P = ½·L<sub>p</sub>·I<sub>p</sub>²·f<sub>s</sub>·η, independente da tensão de entrada: o controle por **corrente de pico** fixa I<sub>p</sub> ciclo a ciclo e torna a planta de primeira ordem (polo em f<sub>p</sub> = 1/(π·R<sub>o</sub>·C<sub>o</sub>)), o que simplifica a compensação e dá limitação de corrente inerente. Durante o bloqueio, o MOSFET suporta V<sub>b</sub> + V<sub>r</sub> mais a sobretensão da indutância de dispersão L<sub>lk</sub>, que precisa ser grampeada.

### 2.2 Estágio de entrada, proteções e qualidade de energia

A ponte com filtro capacitivo conduz apenas perto do pico da rede (Aula 06): a corrente de entrada é pulsada, com fator de potência da ordem de 0,4–0,6 e distorção harmônica elevada, aceitáveis para uma fonte de 36 W (abaixo dos 75 W da IEC 61000-3-2 classe D). O capacitor de *bulk* é escolhido pela tensão mínima que deve manter no vale (regra prática de 2–3 µF/W para entrada universal), e dele decorrem a corrente eficaz no capacitor e nos diodos. As proteções seguem a Aula 07: fusível de ação lenta (2–3× a corrente eficaz de entrada), NTC para limitar a corrente de *inrush* no capacitor de *bulk*, varistor de 275 VAC para surtos, e grampo RCD no dreno do MOSFET. O filtro de EMI (Aula 08) combina capacitores X2 (modo diferencial), um choke de modo comum e um capacitor Y1 entre os terras do primário e do secundário.

### 2.3 Projeto do transformador em alta frequência (Aula 04C)

O produto de áreas mínimo do núcleo é A<sub>e</sub>A<sub>w</sub> = 1,1·P<sub>o</sub>·10⁴/(k<sub>w</sub>·k<sub>p</sub>·J·f<sub>s</sub>·B<sub>máx</sub>), o entreferro l<sub>g</sub> = 2·µ<sub>0</sub>·W/(B²·A<sub>e</sub>) armazena a energia W = P<sub>o</sub>/(η·f<sub>s</sub>), e o número de espiras do primário N<sub>p</sub> = B·l<sub>g</sub>/(µ<sub>0</sub>·I<sub>p</sub>). A bitola dos condutores é limitada pelo efeito pelicular, Δ = 7,5/√f<sub>s</sub> (cm), com fios em paralelo para a corrente eficaz com J = 450 A/cm². Verificam-se a ocupação da janela (K<sub>ocup</sub> ≤ 0,7), as perdas no núcleo (curva do material IP12R) e no cobre, e a elevação de temperatura ΔT = (P<sub>núcleo</sub>+P<sub>cobre</sub>)·R<sub>t</sub>, com R<sub>t</sub> = 23·(A<sub>e</sub>A<sub>w</sub>)<sup>−0,37</sup>.

### 2.4 Perdas nos semicondutores e dissipadores (Aula 02)

As perdas no MOSFET são de condução, R<sub>DS(on)</sub>(T<sub>j</sub>)·I<sub>rms</sub>², e de comutação, ½·V·I·(t<sub>r</sub>+t<sub>f</sub>)·f<sub>s</sub> mais a energia da capacitância de saída C<sub>oss</sub>; no flyback em MCD o MOSFET liga com corrente nula, de modo que a perda de ligação se resume à descarga de C<sub>oss</sub>, e a perda de desligamento depende do tempo de queda efetivo imposto pelo circuito de gate (Q<sub>gd</sub>, resistor de gate e capacidade de dreno do driver). O diodo Schottky dissipa V<sub>0</sub>·I<sub>méd</sub> + R<sub>d</sub>·I<sub>rms</sub>² sem perda de recuperação reversa. Com a temperatura de junção de projeto (125 °C) e a ambiente (40 °C) determina-se a resistência térmica máxima do dissipador, R<sub>θSA</sub> = (T<sub>j</sub> − T<sub>a</sub>)/P − R<sub>θJC</sub> − R<sub>θCS</sub>, como nas Tarefas 1 e 2.

### 2.5 Circuito de comando com o UC3845 (Aula 05)

O UC3845 é um controlador PWM de modo corrente com oscilador programado por R<sub>T</sub> e C<sub>T</sub> (f<sub>osc</sub> ≈ 1,72/(R<sub>T</sub>·C<sub>T</sub>)), flip-flop que limita a razão cíclica a 50 % (f<sub>sw</sub> = f<sub>osc</sub>/2), comparador de corrente com limiar de 1 V no pino ISENSE, amplificador de erro com saída em COMP, referência de 5 V, UVLO de 8,4/7,6 V e saída totem-pole de 1 A capaz de acionar o MOSFET diretamente. A partida é feita por um resistor do *bulk* ao VCC e, em regime, por um enrolamento auxiliar; o resistor de sensoriamento define o limite de corrente de pico, e um filtro RC remove o pico de borda da corrente do primário. Em malha fechada, o TL431 compara uma amostra de V<sub>o</sub> com 2,495 V e, por meio do LED do optoacoplador, puxa o pino COMP para baixo; o compensador tipo 2 (R<sub>z</sub>, C<sub>z</sub> no TL431) coloca um zero sobre o polo da planta e fixa a frequência de cruzamento com margem de fase ≥ 45°.

### 2.6 Layout de PCI (Aula 08 e IPC-2221)

As regras adotadas foram: fluxo de potência linear (entrada de um lado, saída do outro), agrupamento por função, laços de alta frequência curtos, trilhas sem cantos de 90° (chanfros a 45°), separação dos terras de sinal e de potência com um único ponto de união, capacitor de 100 nF junto ao VCC do CI, largura de trilha e distâncias por corrente e tensão (IPC-2221), isolação primário–secundário ≥ 6 mm com fendas sob o transformador e o optoacoplador, plano de terra na face inferior, pontos de teste e regras de DFM para a montagem.

## 3. Materiais e métodos

O projeto foi executado em oito etapas, todas automatizadas por scripts (Python 3 com numpy/matplotlib; LTspice XVII em lote; KiCad 10 por `kicad-cli` e pela API `pcbnew`), de modo que qualquer alteração de parâmetro pode ser propagada até a placa:

1. **Especificação** (`01_Especificacao/requisitos.md`): requisitos elétricos, aplicações, diagrama de blocos e checklist do enunciado.
2. **Cálculos teóricos** (`02_Calculos/*.py` → `resultados/RESULTADOS_TEORIA.md` e `*.json`): parâmetros globais em `params.py` (V<sub>o</sub> = 12 V, I<sub>o</sub> = 3 A, η = 0,82, f<sub>s</sub> = 65 kHz, D<sub>máx</sub> = 0,43, T<sub>a</sub> = 40 °C, T<sub>j</sub> = 125 °C); estágio de entrada por simulação numérica do retificador com capacitor (`entrada.py`); flyback pelo método da Aula 04C (`flyback.py`, `transformador.py`, com a tabela de núcleos Thornton); filtro de saída pelos seis critérios da Aula 03 (`saida.py`); snubber RCD (`snubber.py`); componentes do UC3845 (`uc3845.py`); semicondutores, perdas e dissipadores com o mesmo modelo das Tarefas 1 e 2 (`semicondutores.py`); compensador (`compensador.py`); filtro de EMI (`emi.py`).
3. **Simulação** (`03_Simulacao/`): netlists LTspice geradas por `gera_netlist.py` com modelo comportamental próprio do UC3845 (oscilador, latch de 50 %, comparador de corrente com limiar de 1 V, UVLO 8,4/7,6 V, driver com R<sub>g</sub>), modelo VDMOS do STP13N65M2 (R<sub>DS(on)</sub>, C<sub>gd</sub>, C<sub>oss</sub> do datasheet), TL431 e PC817 comportamentais, indutância de dispersão e RSE dos capacitores explícitas. Foram simulados 20 casos: regime permanente em 90/127/220/264 VAC × 10/50/100 % de carga, partida em 90 e 264 VAC, degrau de carga 50→100 % em 90 e 264 VAC, curto-circuito na saída, operação sem snubber, L<sub>lk</sub> = 3 % e optoacoplador com CTR = 0,5. Os resultados (`.raw`) foram lidos em Python e as medidas consolidadas em `runs/medidas.json`; as tabelas teoria × simulação do relatório são geradas por `06_Relatorio/gera_tabelas.py`.
4. **Ciclo de ajuste**: cada divergência relevante entre teoria e simulação motivou uma revisão dos scripts (seção 4.6), repetindo o lote até fechar.
5. **Esquemático** (`04_KiCad/gera_sch.py` → `fonte_flyback_12V3A.kicad_sch`): gerado por script com os valores finais; ERC sem erros; PDF, netlist e BOM exportados por `kicad-cli`.
6. **Layout** (`placement.py`, `router.py`, `gera_pcb.py`): posicionamento com verificação de sobreposição de *courtyards*, roteador próprio em duas camadas com classes de rede (HV, SEC, SEC_PWR), regras de projeto em `fonte_flyback_12V3A.kicad_dru`, chanfros a 45°, ilha de terra de sinal e verificação de continuidade do plano; DRC com paridade com o esquemático; Gerbers, furação, imagens e render 3D.
7. **BOM e custo** (`05_BOM_Custo/bom.py` → `BOM.xlsx`, `custo.xlsx`), com part numbers, distribuidor e preços de referência para 1 e 100 unidades, incluindo a PCI.
8. **Guia de montagem e ensaio** (`08_Montagem/GUIA_MONTAGEM.md`) e modelo da Tarefa Extra (`09_Tarefa_Extra/`).

Hipóteses de projeto: rendimento 82 % (verificado a posteriori pelo orçamento de perdas), D<sub>máx</sub> = 0,43 (margem sobre os 46–50 % do UC3845), B<sub>máx</sub> = 0,25 T, J = 450 A/cm², k<sub>w</sub> = 0,4, k<sub>p</sub> = 0,3, grampo em 1,8·V<sub>r</sub>, L<sub>lk</sub> = 2 % de L<sub>p</sub> (verificação a 3 %), temperatura ambiente 40 °C.

## 4. Resultados

### 4.1 Requisitos e características elétricas

| Grandeza | Valor |
|---|---|
| Tensão de entrada | 90–264 VAC, 50/60 Hz (nominais 127 e 220 V) |
| Saída | 12,0 V ± 5 %, 0,3–3,0 A (36 W), ondulação ≤ 120 mV p-p |
| Frequência de comutação | 65 kHz (UC3845, D ≤ 0,5) |
| Rendimento (meta / hipótese) | ≥ 85 % / 82 % |
| Proteções | fusível T2A, NTC 10 Ω, varistor S14K275, limitação de corrente ciclo a ciclo, curto-circuito, grampo RCD |
| EMI | X2 220 nF + choke MC 10 mH + X2 100 nF, Y1 2,2 nF |
| Isolação | transformador + optoacoplador; ≥ 6 mm na PCI |
| Potência de entrada | 43,9 W em plena carga (η = 0,82) |

**Estágio de entrada.** A simulação numérica do retificador com capacitor (fig. 1) levou à escolha de **C<sub>bulk</sub> = 100 µF / 400 V** (2,8 µF/W): tensão mínima de 94,6 V em 90 VAC/50 Hz (ondulação 29,8 V), corrente eficaz no capacitor 0,76 A, corrente eficaz de entrada 0,86 A, fator de potência 0,60 (119 % de THD) em 90 V e 0,43 em 220 V — típico de retificador com filtro capacitivo (Aula 06). Proteções: fusível **T 2 A/250 V** (2,5 × 0,86 A), **NTC 10 Ω** (inrush de 187 A sem NTC para 31 A), varistor **S14K275**, ponte **GBU4J** (I<sub>méd</sub> 0,2 A por diodo, V<sub>RRM</sub> 600 V ≥ 1,5 × 370 V, I<sub>FSM</sub> ≥ 100 A).

![Figura 1 – Estágio de entrada: tensão de bulk e corrente da rede em 90 e 220 VAC (entrada.py).](assets/entrada_formas_de_onda.png)

### 4.2 Projeto elétrico do flyback e transformador

Com V<sub>b,mín</sub> = 94,6 V e D<sub>máx</sub> = 0,43: V<sub>r</sub> = 71,3 V, n = 5,62, I<sub>p</sub> = 2,16 A, L<sub>p</sub> = 290 µH, W = 675 µJ. O produto de áreas mínimo é 0,451 cm⁴, atendido pelo núcleo **Thornton E-30/7 (NEE-30/15/7, IP12R)**, A<sub>e</sub>A<sub>w</sub> = 0,48 cm⁴ (tabela 1): l<sub>g</sub> = **0,45 mm**, **N<sub>p</sub> = 42**, **N<sub>s</sub> = 7** (n = 6,0, V<sub>r</sub> = 76,2 V), **N<sub>aux</sub> = 9** (V<sub>aux</sub> ≈ 15 V), **L<sub>p</sub> = 294 µH**, B<sub>pico</sub> = 0,25 T. A profundidade de penetração em 65 kHz (0,29 mm) limita o fio a 23 AWG: primário 1 × 23 AWG (I<sub>p,rms</sub> = 0,82 A), secundário 5 × 23 AWG (I<sub>s,rms</sub> = 5,45 A), auxiliar 1 × 28 AWG. Perdas 0,62 W (núcleo) + 0,35 W (cobre) → ΔT = 29 °C; K<sub>ocup</sub> = 0,46. O núcleo E-30/14, embora caiba, teria o dobro de perdas no núcleo; o E-42/15 ficaria subutilizado (K<sub>ocup</sub> = 0,08). A ordem de enrolamento (sanduíche: ½ primário, auxiliar, secundário, ½ primário) e a execução do entreferro estão no guia de montagem.

**Tabela 1 – Comparação de núcleos (transformador.py).**

| Núcleo | A<sub>e</sub>A<sub>w</sub> (cm⁴) | l<sub>g</sub> (mm) | N<sub>p</sub> | N<sub>s</sub> | N<sub>aux</sub> | L<sub>p</sub> (µH) | fio prim. | fio sec. | P núcleo (W) | P cobre (W) | ΔT (°C) | K<sub>ocup</sub> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **E-30/7** | 0,48 | 0,45 | 42 | 7 | 9 | 294 | 1×23 | 5×23 | 0,62 | 0,35 | 29,1 | 0,46 |
| E-30/14 | 1,02 | 0,23 | 21 | 3 | 4 | 294 | 1×23 | 6×23 | 1,23 | 0,19 | 32,4 | 0,22 |
| E-42/15 | 2,84 | 0,15 | 14 | 2 | 3 | 297 | 1×23 | 6×23 | 2,63 | 0,16 | 43,7 | 0,08 |

![Figura 2 – Formas de onda teóricas do flyback em 90 VAC e 264 VAC, plena carga (flyback.py).](assets/flyback_formas_de_onda.png)

**Esforços teóricos (tabela 2).** Em toda a faixa o conversor opera em MCD com I<sub>p</sub> = 2,14 A; a razão cíclica vai de 0,43 (90 V) a 0,11 (264 V), o tempo de condução mínimo é 554 ns (264 V, 10 %), acima do mínimo do UC3845. A tensão máxima no MOSFET com grampo a 1,8·V<sub>r</sub> é **507 V** em 264 VAC (78 % de 650 V); a tensão reversa no diodo de saída é 74 V (Schottky de 100 V); a corrente eficaz nos capacitores de saída é 4,54 A.

**Tabela 2 – Esforços teóricos por ponto de operação (flyback.py).**

| V<sub>ac</sub> | carga | D | t<sub>on</sub> (ns) | I<sub>p</sub> (A) | I<sub>p,rms</sub> (A) | I<sub>s,pk</sub> (A) | I<sub>s,rms</sub> (A) | I<sub>c,rms</sub> (A) | V<sub>ds</sub> grampo (V) | V<sub>d,rev</sub> (V) |
|---|---|---|---|---|---|---|---|---|---|---|
| 90 | 100 % | 0,433 | 6663 | 2,14 | 0,815 | 12,9 | 5,45 | 4,54 | 261 | 33 |
| 127 | 100 % | 0,264 | 4058 | 2,14 | 0,636 | 12,9 | 5,45 | 4,54 | 314 | 41 |
| 220 | 100 % | 0,139 | 2133 | 2,14 | 0,461 | 12,9 | 5,45 | 4,54 | 445 | 63 |
| 264 | 100 % | 0,114 | 1752 | 2,14 | 0,418 | 12,9 | 5,45 | 4,54 | 507 | 74 |
| 264 | 10 % | 0,036 | 554 | 0,68 | 0,074 | 4,1 | 0,97 | 0,92 | 507 | 74 |

### 4.3 Escolha dos capacitores, filtro de saída e snubber

**Capacitores de saída (Aula 03).** C<sub>mín</sub> = 427 µF para ΔV<sub>C</sub> = 50 mV; a RSE máxima para 120 mV sem pós-filtro seria 5,4 mΩ, impraticável com um único eletrolítico, de modo que se adotou um banco de **3 × Rubycon ZLH 1000 µF/25 V** (RSE equivalente 6,3 mΩ, corrente de ondulação admissível 6,0 A ≥ 4,54 A, ΔV<sub>1</sub> = 89 mV) seguido de **pós-filtro LC 3,3 µH + 470 µF** (f<sub>c</sub> = 4,0 kHz, −30 dB em 65 kHz), resultando em ondulação teórica de 2,7 mV (fig. 3). Demais capacitores: bulk 100 µF/400 V 105 °C (Nichicon UCY), VCC 220 µF/35 V + 100 nF, VREF 1 µF, C<sub>T</sub> 2,2 nF C0G, X2 220 nF e 100 nF, Y1 2,2 nF (fuga 0,21 mA < 0,25 mA, classe II), snubber 22 nF/630 V de filme.

![Figura 3 – Ondulação de saída no banco de capacitores e após o pós-filtro LC (saida.py).](assets/saida_ripple.png)

**Snubber RCD (Aula 07).** Com L<sub>lk</sub> = 2 % de L<sub>p</sub> (5,9 µH) e grampo V<sub>c</sub> = 1,8·V<sub>r</sub> = 137 V, a energia por ciclo é 13,5 µJ e a potência 2,0 W: **R = 9,1 kΩ (2 × 18,2 kΩ / 2 W em paralelo)**, **C = 22 nF / 630 V**, diodo **UF4007**. Para L<sub>lk</sub> = 3 % a potência sobe a 2,6 W e V<sub>ds</sub> a 524 V (81 %). A alternativa com TVS P6KE180A foi descartada por deixar V<sub>ds</sub> em 616 V (95 %). No diodo de saída, um RC de amortecimento de 15 Ω + 2,2 nF/100 V (f<sub>ring</sub> ≈ 14 MHz) limita o ringing (fig. 4).

![Figura 4 – Compromisso potência × tensão de grampo do snubber (snubber.py).](assets/snubber_compromisso.png)

### 4.4 Escolha dos diodos, do transistor, perdas e dissipadores

**Pré-escolha (Aula 03).** MOSFET: V<sub>ds</sub> ≤ 80 % → classe 650 V, I<sub>D</sub> ≥ 4 A, TO-220; diodo de saída: Schottky 100 V, ≥ 10 A; ponte 600 V / 2–4 A. Foram comparados três MOSFETs (tabela 3) com o modelo de perdas das Tarefas 1 e 2 (R<sub>DS(on)</sub> a 125 °C, descarga de C<sub>oss</sub>, desligamento com t<sub>f</sub> efetivo imposto pelo gate, perda de gate).

**Tabela 3 – MOSFETs candidatos, perdas em plena carga e dissipador (semicondutores.py).**

| MOSFET | R<sub>DS(on)</sub> 25 °C (mΩ) | Q<sub>g</sub> (nC) | P<sub>tot</sub> 90 V (W) | P<sub>tot</sub> 264 V (W) | R<sub>θJC</sub> (°C/W) | R<sub>θSA</sub> máx (°C/W) | dissipador | T<sub>j</sub> (°C) |
|---|---|---|---|---|---|---|---|---|
| IPA65R400CE (Infineon, TO-220FP) | 400 | 20 | 1,14 | 1,38 | 4,0 | 57 | clip Aavid 574502 | 79 |
| **STP13N65M2 (ST MDmesh M2, TO-220)** | 430 | 17 | 1,04 | 1,15 | 1,14 | 72 | clip Aavid 574502 | 69 |
| FCPF190N65S3 (onsemi, TO-220F) | 190 | 34 | 0,83 | 1,40 | 3,5 | 57 | clip Aavid 574502 | 79 |

Escolhido o **STP13N65M2** (menor perda total no pior caso, 1,15 W em 264 V; sem dissipador T<sub>j</sub> seria 112 °C, acima da margem adotada de 100 °C, por isso o clip de 24 °C/W com mica e pasta → T<sub>j</sub> ≈ 69 °C). Como o componente está em falta em alguns distribuidores, a BOM lista substitutos diretos (STF13N65M2, IPA65R400CE). **Diodo de saída: STPS20H100CT** (dois diodos de 10 A/100 V em paralelo): P = 1,78 W, clip de 24 °C/W → T<sub>j</sub> ≈ 84 °C (tabela 4). **Ponte GBU4J**: 0,69 W, T<sub>j</sub> ≈ 54 °C sem dissipador. Diodo do snubber UF4007, do auxiliar UF4004, do gate 1N4148.

**Tabela 4 – Diodos de saída candidatos (semicondutores.py).**

| Diodo | V<sub>0</sub> (V) | R<sub>d</sub> (mΩ) | P (W) | R<sub>θJC</sub> | R<sub>θSA</sub> máx | T<sub>j</sub> (°C) |
|---|---|---|---|---|---|---|
| **STPS20H100CT – ânodos em paralelo** | 0,55 | 4,5 | 1,78 | 0,45 | 46,7 | 84 |
| STPS20H100CT – uma perna | 0,55 | 9,0 | 1,92 | 0,90 | 42,9 | 89 |
| MBR20100CT – paralelo | 0,62 | 6,0 | 2,04 | 1,00 | 40,2 | 92 |
| MBR10100 | 0,65 | 12,0 | 2,31 | 2,00 | 34,4 | 101 |

![Figura 5 – Distribuição de perdas em plena carga por tensão de rede (semicondutores.py).](assets/perdas_semicondutores.png)

**Orçamento de perdas (tabela 5).** O total varia de 7,4 a 8,0 W, com o snubber (2,0 W), o diodo (1,8 W), o MOSFET (1,0–1,15 W), o transformador (0,9 W) e o NTC (0,74 W em 90 V) como maiores parcelas: η = 81,9–83,0 %, coerente com a hipótese de 82 %.

**Tabela 5 – Orçamento de perdas em plena carga (W).**

| V<sub>ac</sub> | MOSFET | diodo | ponte | trafo | snubber | R<sub>sense</sub> | partida | cap. saída | NTC | L<sub>LC</sub> | UC3845 | total | η (%) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 90 | 1,04 | 1,78 | 0,69 | 0,96 | 2,01 | 0,22 | 0,09 | 0,13 | 0,74 | 0,09 | 0,22 | 7,98 | 81,9 |
| 127 | 1,04 | 1,78 | 0,45 | 0,91 | 2,01 | 0,13 | 0,19 | 0,13 | 0,45 | 0,09 | 0,22 | 7,41 | 82,9 |
| 220 | 1,15 | 1,78 | 0,24 | 0,87 | 2,01 | 0,07 | 0,58 | 0,13 | 0,22 | 0,09 | 0,22 | 7,37 | 83,0 |
| 264 | 1,15 | 1,78 | 0,20 | 0,86 | 2,01 | 0,06 | 0,84 | 0,13 | 0,17 | 0,09 | 0,22 | 7,52 | 82,7 |

### 4.5 Componentes associados ao CI, driver e malha de realimentação

**Oscilador:** R<sub>T</sub> = 6,04 kΩ (E96), C<sub>T</sub> = 2,2 nF C0G → f<sub>osc</sub> = 129,4 kHz, **f<sub>sw</sub> = 64,7 kHz**. **Sensoriamento:** limite de corrente em 1,25·I<sub>p</sub> = 2,68 A → **R<sub>s</sub> = 0,33 Ω** (2 × 0,68 Ω / 1 W em paralelo; 0,22 W), limite real 2,7–3,0 A; filtro 1 kΩ / 220 pF (τ = 220 ns < t<sub>on,mín</sub>/2). **Partida:** 2 × 82 kΩ / 1 W em série do *bulk* ao VCC (corrente mínima 0,53 mA ≥ 0,5 mA no vale de 90 V; partida em 1–4,3 s; 0,84 W em 264 V), C<sub>VCC</sub> = 220 µF/35 V (sustenta 9,2 ms entre 8,4 e 7,6 V), auxiliar de 15,4 V com UF4004 + 10 Ω. **Driver:** a saída totem-pole de ±1 A do UC3845 aciona diretamente o MOSFET (Q<sub>g</sub> = 17 nC: 1,1 mA médios a 65 kHz, tempos de borda ≈ 25 ns) — circuito básico não isolado da Aula 05, pois CI e MOSFET compartilham a referência; R<sub>g</sub> = 10 Ω, 1N4148 antiparalelo (desligamento rápido) e 10 kΩ gate–source. **Compensação de rampa:** não necessária (MCD, D < 0,5); há provisão na placa. **Realimentação:** divisor R<sub>a</sub> = 9,53 kΩ / R<sub>b</sub> = 2,49 kΩ (V<sub>o</sub> = 12,04 V), R<sub>LED</sub> = 2,74 kΩ, R<sub>bias</sub> = 1 kΩ, pull-up de 4,7 kΩ no COMP com C<sub>p</sub> = 1 nF; a planta (modo corrente em MCD) tem ganho 15,9 dB e polo em 22,9 Hz em plena carga; compensador tipo 2 com **R<sub>z</sub> = 47,5 kΩ, C<sub>z</sub> = 150 nF** (zero em 22 Hz) dá f<sub>c</sub> = 1,49 kHz e **margem de fase 99°**, mantendo-se ≥ 91° para 10 % de carga e CTR de 0,5 a 1,6 (fig. 6).

![Figura 6 – Diagrama de Bode da planta, do compensador e da malha aberta (compensador.py).](assets/compensador_bode.png)

**Filtro de EMI:** choke de modo comum 10 mH (Würth 744821110, dispersão ≈ 200 µH para o modo diferencial), X2 220 nF antes e 100 nF depois, Y1 2,2 nF entre os terras e 2 × 470 kΩ de descarga (34 V em 0,77 s): f<sub>DM</sub> ≈ 43 kHz (51 dB em 150 kHz), f<sub>CM</sub> ≈ 24 kHz (26 dB em 150 kHz) (fig. 7).

![Figura 7 – Atenuação estimada do filtro de EMI nos modos diferencial e comum (emi.py).](assets/emi_atenuacao.png)

### 4.6 Simulação e comparação com a teoria

A fig. 8 mostra as formas de onda de um ciclo em 90 VAC e 264 VAC, plena carga, e a fig. 9 a partida em 90 VAC e o degrau de carga. A tabela 6 compara os esforços teóricos com os simulados nos 12 pontos de operação e a tabela 7 as perdas e o rendimento em plena carga; a tabela 8 resume os casos especiais.

![Figura 8 – Simulação LTspice: um ciclo de comutação em 90 VAC (esquerda) e 264 VAC (direita), plena carga.](assets/regime_90V_100pct_ciclo.png)

![Figura 8b – Detalhe da comutação em 264 VAC, plena carga: tensão de dreno com o grampo RCD.](assets/regime_264V_100pct_comut.png)

**Tabela 6 – Teoria × simulação em regime permanente (gera_tabelas.py).**

{{regime}}

**Tabela 7 – Perdas e rendimento em plena carga: teoria × simulação.**

{{perdas}}

**Tabela 8 – Casos especiais simulados.**

{{especiais}}

![Figura 9 – Partida em 90 VAC (tensões de bulk, VCC e saída) e degrau de carga 50 → 100 % em 90 VAC.](assets/partida_90V_rede.png)

![Figura 9b – Degrau de carga 50 → 100 % em 90 VAC: tensão de saída e corrente do primário.](assets/degrau_90V_rede.png)

![Figura 10 – Tensão de dreno em 264 VAC sem snubber (828 V) e com Llk = 3 % (496 V).](assets/sem_snubber_264V_comut.png)

![Figura 10b – Tensão de dreno em 264 VAC com Llk = 3 % de Lp.](assets/llk3pct_264V_comut.png)

![Figura 11 – Curto-circuito na saída em 220 VAC: limitação ciclo a ciclo e recuperação.](assets/curto_220V_rede.png)

**Análise.** A tensão de saída fica entre 12,07 e 12,08 V em toda a faixa (regulação de linha e carga < 0,1 %), com ondulação de 1–4 mV após o pós-filtro. A corrente de pico do primário difere −3,5 % da teoria (o controle por corrente de pico com o limiar efetivo do comparador a 0,9–1,0 V e o atraso do filtro RC fixam I<sub>p</sub> ligeiramente abaixo); a corrente de pico do secundário fica +5 % (dispersão e amortecimento do RC do diodo), e a corrente eficaz do secundário −10 %, porque a teoria assume o triângulo ideal com V<sub>b</sub> no vale enquanto a simulação integra sobre o ciclo da rede. A tensão de dreno em plena carga fica 5–6 % abaixo da teoria (grampo real em 1,6–1,7·V<sub>r</sub>); em carga leve o grampo cai (menos energia de dispersão), e a diferença chega a −21 %, a favor da segurança. O rendimento simulado (83,3 % em 90 V, 85,5 % em 220 V) é 1–2 pontos superior ao orçamento teórico, principalmente porque o snubber dissipa 1,2–1,5 W (grampo mais baixo) e o MOSFET 0,4–0,9 W (comutação suave em MCD); as perdas no diodo e na ponte coincidem em ±4 %. Em 10 % de carga o rendimento cai para 64–73 % por causa das perdas fixas (snubber, resistores de partida, CI), comportamento esperado em um flyback sem modo *burst*.

Os casos especiais confirmam: partida sem sobretensão em 90 e 264 VAC (V<sub>o</sub> máx 12,06 V); degraus de carga sem oscilação (ΔV<sub>o</sub> < 15 mV, resposta em < 1 ms, coerente com a margem de fase de 99°); mesmo com CTR = 0,5 a malha permanece estável; **sem o snubber a tensão de dreno chega a 828 V (127 % de 650 V), o que comprova a necessidade do grampo**; com L<sub>lk</sub> = 3 % o pico é 496 V (76 %). No curto-circuito a limitação ciclo a ciclo mantém I<sub>p</sub> em 2,7–3,0 A em regime, mas há um transitório de 4,3 A no instante do curto (atraso do filtro de corrente e do driver) e a corrente eficaz no diodo sobe a 17 A enquanto o curto dura: o UC3845 não tem proteção de curto temporizada, e a fonte só reduz a potência quando o VCC auxiliar cai e o CI entra em *hiccup* pelo UVLO. Essa é uma **limitação documentada** do projeto: um produto comercial acrescentaria um circuito de sobrecorrente no secundário ou um CI com temporizador de falha, o que fica como sugestão.

**Ajustes feitos no ciclo teoria → simulação → teoria:** D<sub>máx</sub> reduzido de 0,45 para 0,43 (margem para os 46 % mínimos do UC3845 e para o MCC em 90 V); grampo elevado de 1,5 para 1,8·V<sub>r</sub> (menor potência no snubber, V<sub>ds</sub> ainda ≤ 80 %); η de 0,85 para 0,82 após o orçamento de perdas; N<sub>s</sub> escolhido equilibrando as margens de tensão do MOSFET (650 V) e do diodo (100 V); regra de dissipador para T<sub>j</sub> > 100 °C; capacitor Y1 com passo de 10 mm e redes HV com largura ≥ 1 mm após o DRC; modelo do MOSFET com C<sub>gd</sub> e C<sub>oss</sub> de catálogo após a primeira simulação, excessivamente ideal, mostrar comutação sem perdas.

**Tabela 9 – Verificação dos critérios de projeto.**

{{criterios}}

### 4.7 Esquemático

O esquemático completo (fig. 12; PDF em `04_KiCad/fonte_flyback_12V3A_esquematico.pdf`) reúne os seis blocos: entrada/proteções/EMI, retificador + bulk, flyback com snubber e Rsense, controle UC3845 com partida e auxiliar, realimentação TL431/PC817 e saída com pós-filtro, além de 11 pontos de teste e 4 furos de fixação. ERC: 0 erros, 0 avisos; 54 componentes, 34 redes.

![Figura 12 – Esquemático da fonte (KiCad 10).](assets/esquematico.png)

### 4.8 Lista de materiais e custo

A BOM completa (`05_BOM_Custo/BOM.xlsx`, 57 itens) traz part number, fabricante, código de distribuidor e preço de referência para 1 e 100 unidades (catálogos Mouser/Digi-Key/LCSC/RS consultados em outubro de 2026, câmbio adotado R$ 5,50). O custo por fonte é **US$ 39,78 (≈ R$ 219) em 1 unidade** e **US$ 20,63 (≈ R$ 113) em 100 unidades**, incluindo a PCI (tabela 10). Em 1 unidade a placa (lote de 5 com frete) é 24 % do custo; em 100 unidades os maiores blocos são o secundário (diodo com dissipador e capacitores de baixa RSE), o filtro de EMI e o transformador.

**Tabela 10 – Custo por bloco (bom.py).**

| Bloco | Itens | US$ (1 un.) | US$ (100 un.) | % (1 un.) |
|---|---|---|---|---|
| PCI (2 camadas, 140 × 90 mm) | 1 | 9,60 | 1,90 | 24,1 |
| Secundário | 10 | 5,05 | 3,14 | 12,7 |
| Filtro EMI | 6 | 4,51 | 2,97 | 11,3 |
| Transformador | 2 | 4,50 | 3,00 | 11,3 |
| Potência primária | 5 | 3,30 | 2,21 | 8,3 |
| Mecânica (pontos de teste, espaçadores) | 15 | 2,80 | 1,42 | 7,0 |
| Entrada e proteções | 5 | 2,65 | 1,71 | 6,7 |
| Retificador e bulk | 2 | 2,60 | 1,75 | 6,5 |
| Comando UC3845 | 16 | 2,55 | 1,38 | 6,4 |
| Realimentação | 10 | 1,21 | 0,61 | 3,0 |
| Snubber RCD | 4 | 1,01 | 0,54 | 2,5 |
| **Total por fonte** | 76 | **39,78** | **20,63** | 100 |

### 4.9 Layout da PCI

A placa (fig. 13 a 15) tem **140 × 90 mm**, duas camadas, FR-4 de 1,6 mm, cobre de 35 µm e todos os componentes PTH (montagem manual ou por onda). O posicionamento segue o fluxo linear rede → EMI → ponte/bulk → MOSFET/transformador → secundário → saída, com o circuito de comando agrupado abaixo do primário e a realimentação no secundário; o transformador fica sobre a fenda de isolação e o optoacoplador sobre uma segunda fenda. As regras de projeto (`fonte_flyback_12V3A.kicad_dru`, classes HV/SEC/SEC_PWR) impõem isolamento ≥ 1,0 mm nas redes de alta tensão (IPC-2221 B4 para 301–500 V com máscara: 0,8 mm), **≥ 6 mm entre primário e secundário**, trilhas ≥ 1,0 mm nas redes HV, 2,0 mm no secundário de potência (5,45 A rms) e 1,5 mm no bulk. O roteador substitui os cantos de 90° por chanfros a 45° (222 chanfros; os ângulos retos restantes são saídas de trilhas em pads). O terra de potência (plano inferior sob o primário) e o terra de sinal (ilha sob o UC3845, opto e auxiliares) são zonas separadas unidas por uma única trilha no lado frio do R<sub>sense</sub>, e o roteador verifica que a ilha permanece contínua; o capacitor de 100 nF fica a 4,3 mm do pino VCC. Resultado do DRC (`kicad-cli pcb drc --severity-all --schematic-parity`): **0 erros, 0 itens não conectados, 0 divergências com o esquemático**, 4 avisos de serigrafia (opto sobre a fenda, intencional). A verificação item a item contra a Aula 08 está em `04_KiCad/VERIFICACAO_LAYOUT.md`; os arquivos de fabricação (Gerbers RS-274X e furação Excellon) em `04_KiCad/gerbers/`.

![Figura 13 – Face superior da PCI (cobre e serigrafia).](assets/pcb_F.Cu.png)

![Figura 14 – Face inferior: planos de terra do primário (com a ilha de sinal) e do secundário.](assets/pcb_B.Cu.png)

![Figura 15 – Render 3D da placa montada (KiCad).](assets/pcb_3d_iso.png)

### 4.10 Montagem e ensaio (preparação para a Possibilidade II)

O guia `08_Montagem/GUIA_MONTAGEM.md` contém a lista de compra com alternativas nacionais, o procedimento de enrolar o transformador (ordem em sanduíche, isolação, entreferro, medida de L<sub>p</sub> = 294 µH ± 10 % e L<sub>lk</sub> < 9 µH), a montagem por blocos com teste de cada um (entrada, controle com fonte de bancada, potência em tensão reduzida com lâmpada em série, tensão plena, proteções), a tabela de grandezas esperadas com critério de aceite e um guia de diagnóstico. Os resultados experimentais, se o protótipo for montado, entram na tabela 6 como terceira coluna.

## 5. Conclusão

O projeto atingiu o objetivo da introdução: uma fonte flyback de 12 V / 3 A com entrada universal e UC3845 foi especificada, calculada, simulada, ajustada e levada até o layout final verificado. Os resultados da simulação confirmam a teoria dentro de 10 % nos esforços de corrente e tensão, com regulação melhor que 0,1 %, ondulação de poucos milivolts, V<sub>ds</sub> máximo de 482–496 V (74–76 % de 650 V), partida e degraus de carga estáveis (margem de fase de 99°) e rendimento de 83–85,5 % em plena carga, acima da hipótese de projeto de 82 % e no limite da meta de 85 %; as maiores parcelas de perda são o snubber, o diodo de saída e o NTC. A simulação sem snubber (828 V) demonstra que o grampo é indispensável, e o ensaio de curto-circuito mostra a limitação do UC3845 sem temporizador de falha, apontando uma melhoria para um produto. Todos os itens do enunciado foram cobertos: requisitos e aplicações, simulações, esquemático, projeto físico do transformador, capacitores, diodos, componentes do CI, driver, transistor com perdas e dissipador, BOM com part numbers e custo (US$ 39,78 por unidade; US$ 20,63 em 100) e layout com potência e comando, seguindo as práticas da Aula 08 e a IPC-2221. Como trabalhos futuros, sugerem-se a proteção de sobrecorrente no secundário, um modo *burst* para elevar o rendimento em carga leve, a medição de L<sub>lk</sub> do transformador real para fechar o dimensionamento do snubber e, se houver bancada, a montagem do protótipo com o roteiro preparado.

## 6. Referências bibliográficas

1. MOIA, J. *Apresentações das Aulas 01 a 08 – Eletrônica de Potência II*. IFSC, 2026 (revisão de eletrônica de potência; perdas e dissipadores; metodologia de projeto; eletromagnetismo, indutores e transformadores em alta frequência; circuitos de comando; QEE e correção do fator de potência; fontes chaveadas; layout de PCI com DFM).
2. BARBI, I. *Projeto de fontes chaveadas*. Florianópolis: Edição do Autor, 2003.
3. BARBI, I. *Eletrônica de potência*. 5. ed. Florianópolis: Edição do Autor, 2005.
4. ERICKSON, R. W.; MAKSIMOVIĆ, D. *Fundamentals of power electronics*. 2. ed. Norwell: Kluwer, 2001.
5. MOHAN, N.; UNDELAND, T.; ROBBINS, W. *Power electronics: converters, applications and design*. 2. ed. New York: Wiley, 1995.
6. TEXAS INSTRUMENTS. *UCx84x Current-Mode PWM Controllers* (datasheet SLUS223H). 2024.
7. STMICROELECTRONICS. *STP13N65M2 – N-channel 650 V, 0.43 Ω typ., 11 A MDmesh M2 Power MOSFET* (datasheet). 2022.
8. STMICROELECTRONICS. *STPS20H100CT – High voltage power Schottky rectifier* (datasheet).
9. INFINEON. *IPA65R400CE CoolMOS CE Power Transistor* (datasheet); ONSEMI. *FCPF190N65S3 SuperFET III* (datasheet).
10. THORNTON ELETRÔNICA. *Catálogo de núcleos de ferrite NEE – material IP12R*.
11. WÜRTH ELEKTRONIK. *WE-CMB Common Mode Power Line Choke 744821110* (datasheet).
12. IPC. *IPC-2221B – Generic Standard on Printed Board Design*. 2012.
13. ANALOG DEVICES. *LTspice XVII – Help: A-devices, VDMOS model*; KICAD. *KiCad 10 documentation – kicad-cli, custom design rules*.
14. IFSC. *Plano de Ensino – ELP22109 Eletrônica de Potência II, 2026-2* e *Projeto Semestral 2026-2* (enunciado).
