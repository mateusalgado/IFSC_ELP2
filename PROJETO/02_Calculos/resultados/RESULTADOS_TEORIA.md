# Resultados dos cálculos de projeto (gerado por run_all.py)



---

<!-- entrada.py -->
# Estagio de entrada

Pin = Po/eta = 36/0.82 = 43.90 W ; Rs = 2.0 ohm

## Escolha do capacitor de bulk (90 VAC, 50 Hz, plena carga)

| C | C/Po | Vbulk mín (V) | Ondulação (V) | I_C,rms (A) | FP | THD (%) |
|---|---|---|---|---|---|---|
| 68 µF | 1.89 µF/W | 80,9 | 43,6 | 0,72 | 0,611 | 104,2 |
| 82 µF | 2.28 µF/W | 88,2 | 36,2 | 0,74 | 0,604 | 111,9 |
| 100 µF | 2.78 µF/W | 94,6 | 29,8 | 0,76 | 0,595 | 119,4 |
| 120 µF | 3.33 µF/W | 99,4 | 24,9 | 0,78 | 0,587 | 125,6 |

## Retificador + bulk com C = 100 µF (plena carga)

| Vac | f (Hz) | Vb mín | Vb máx | ΔVb | I pico (A) | I in,rms (A) | I D,med (A) | I D,rms (A) | I C,rms (A) | FP | THD % | cond. (°) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 90 | 50 | 94,6 | 124,3 | 29,8 | 2,49 | 0,86 | 0,199 | 0,61 | 0,76 | 0,595 | 119,4 | 49 |
| 90 | 60 | 99,4 | 124,2 | 24,9 | 2,57 | 0,87 | 0,195 | 0,62 | 0,78 | 0,587 | 125,6 | 46 |
| 127 | 50 | 155,2 | 176,8 | 21,5 | 2,26 | 0,67 | 0,132 | 0,48 | 0,62 | 0,530 | 152,0 | 35 |
| 127 | 60 | 158,6 | 176,6 | 18,0 | 2,32 | 0,68 | 0,131 | 0,48 | 0,63 | 0,522 | 157,3 | 33 |
| 220 | 50 | 295,4 | 308,3 | 12,9 | 1,95 | 0,47 | 0,073 | 0,33 | 0,45 | 0,432 | 205,5 | 21 |
| 220 | 60 | 297,3 | 308,0 | 10,7 | 1,98 | 0,47 | 0,073 | 0,34 | 0,45 | 0,427 | 209,2 | 21 |
| 264 | 50 | 359,6 | 370,4 | 10,8 | 1,85 | 0,42 | 0,060 | 0,30 | 0,40 | 0,404 | 223,9 | 18 |
| 264 | 60 | 361,2 | 370,2 | 9,0 | 1,88 | 0,42 | 0,060 | 0,30 | 0,40 | 0,400 | 227,0 | 18 |

## Proteções e componentes de entrada

- Corrente eficaz de entrada máxima (90 VAC): 0.86 A → fusível 2,5× = 2.16 A → **T 2 A / 250 V (5x20 mm, ação lenta)**
- Inrush sem NTC (264 VAC): 187 A ; com NTC 10 Ω frio: 31.1 A → **NTC 10 Ω / 2–3 A (ex.: 10D-9 ou 10D-11)**
- Varistor: **MOV 275 VAC (ex.: S14K275 / 14D431K), Vclamp ≈ 710 V @ 50 A**
- Ponte: I_med = 0.199 A, I_rms = 0.61 A, I_pico = 2.5 A, VRRM ≥ 560 V → **GBU4J (4 A / 600 V) ou KBP206 (2 A / 600 V)**
- Bulk: 100 µF / 400 V, I_C,rms = 0.76 A (90 VAC) → **Nichicon UCY2G101MHD ou Rubycon 400BXW100MEFC16X35 (100 µF/400 V, 105 °C)**
- Vbulk mín (90 VAC/50 Hz) = 94.6 V ; Vbulk máx (264 VAC) = 370.2 V

Figura: assets/entrada_formas_de_onda.png



---

<!-- transformador.py -->
# Projeto fisico do transformador flyback (Aula 04C)

Dados: Po = 36 W, fs = 65 kHz, Vbulk,min = 94.6 V, η = 0.82, B = 0.25 T, kw = 0.4, kp = 0.3, J = 450 A/cm², Dmax = 0.43

- Ip = 2.160 A ; W = Po/(η·fs) = 675 µJ
- AeAw mín = 1,1·Po·10⁴/(kw·kp·J·fs·B) = **0.451 cm⁴**

## Comparação de núcleos Thornton

| Núcleo | AeAw | lg (mm) | Np | Ns | Naux | n | Lp (µH) | B pico (T) | fio prim. | fio sec. | P núcleo (W) | P cobre (W) | ΔT (°C) | Kocup | atende |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E-30/7 | 0,48 | 0,45 | 42 | 7 | 9 | 6,00 | 294 | 0,250 | 1×23 | 5×23 | 0,62 | 0,35 | 29,1 | 0,46 | sim |
| E-30/14 | 1,02 | 0,23 | 21 | 3 | 4 | 7,00 | 294 | 0,250 | 1×23 | 6×23 | 1,23 | 0,19 | 32,4 | 0,22 | sim |
| E-42/15 | 2,84 | 0,15 | 14 | 2 | 3 | 7,00 | 297 | 0,250 | 1×23 | 6×23 | 2,63 | 0,16 | 43,7 | 0,08 | não |

## Núcleo escolhido: **E-30/7** (Thornton NEE-30/7, material IP12R)

- Entreferro total lg = 2·µ0·W/(B²·Ae) = **0.45 mm** (espaçador de 0.23 mm em cada perna externa, ou 0.45 mm só na perna central)
- Np = B·lg/(µ0·Ip) = **42 espiras** ; Ns = Np/n = **7** ; Naux = **9** (Vaux ≈ 15.0 V) → n real = 6.000
- Lp real = µ0·Np²·Ae/lg = **294 µH** ; Ip real (90 VAC, 100 %) = 2.144 A (MCD, D = 0.433) ; B pico real = 0.250 T
- Profundidade de penetração Δ = 7,5/√fs = 0.0294 cm → d máx = 0.059 cm → fio ≤ 23 AWG
- Primário: Ip,rms = 0.815 A → 1 × 23 AWG ; Secundário: Is,rms = 5.45 A → 5 × 23 AWG ; Auxiliar: 1 × 28 AWG
- Resistências (100 °C): Rp = 209.9 mΩ, Rs = 7.00 mΩ
- Perdas: núcleo 0.62 W + cobre 0.35 W = **0.96 W** ; Rt = 30.2 °C/W → **ΔT = 29.1 °C**
- Ocupação: Aw,nec = 0.368 cm² / Aw = 0.8 cm² → **Kocup = 0.46**
- Llk estimada (3 %) = 8.8 µH ; tensão refletida Vr = 76.2 V

## Sensibilidade à densidade de fluxo (E-30/7)

| B (T) | Np | Ns | lg (mm) | Lp (µH) | P núcleo (W) | P cobre (W) | ΔT (°C) | Kocup |
|---|---|---|---|---|---|---|---|---|
| 0,20 | 53 | 9 | 0,71 | 299 | 0,36 | 0,43 | 24,0 | 0,58 |
| 0,25 | 42 | 7 | 0,45 | 294 | 0,62 | 0,35 | 29,1 | 0,46 |
| 0,30 | 35 | 6 | 0,31 | 294 | 0,95 | 0,29 | 37,5 | 0,39 |

Figura: assets/trafo_nucleos.png



---

<!-- flyback.py -->
# Projeto eletrico do flyback

## Projeto preliminar (fronteira MCD/MCC em Vbulk mín. e plena carga)

- Vbulk mín = 94.6 V (90 VAC/50 Hz), Vbulk máx = 370.2 V (264 VAC)
- Vr = Dmax/(1−Dmax)·Vbulk,min = 0.43/(1−0.43)·94.6 = **71.3 V**
- n = Np/Ns = Vr/(Vo+Vf) = 71.3/(12.0+0.7) = **5.62**
- Ip = 2·Po/(η·Vbulk,min·Dmax) = 2·36/(0.82·94.6·0.43) = **2.160 A**
- Lp = Vbulk,min·Dmax/(Ip·fs) = **289.7 µH** ; energia por ciclo W = Po/(η·fs) = 675 µJ

**Valores finais do transformador (trafo.json):** n = 6.000 (42:7), Lp = 293.8 µH

## Esforços por ponto de operação (final; correntes no vale de Vbulk, tensões no pico)

| Vac | carga % | Vb vale | modo | D | ton (ns) | Ip (A) | Ip,rms (A) | Is,pk (A) | Is,rms (A) | Ic,rms (A) | Vds off (V) | Vds c/ grampo (V) | Vd rev (V) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 90 | 10 | 95 | MCD | 0,137 | 2107 | 0,68 | 0,145 | 4,1 | 0,97 | 0,92 | 200 | 261 | 33 |
| 90 | 50 | 95 | MCD | 0,306 | 4711 | 1,52 | 0,484 | 9,1 | 3,24 | 2,87 | 200 | 261 | 33 |
| 90 | 100 | 95 | MCD | 0,433 | 6663 | 2,14 | 0,815 | 12,9 | 5,45 | 4,54 | 200 | 261 | 33 |
| 127 | 10 | 155 | MCD | 0,083 | 1283 | 0,68 | 0,113 | 4,1 | 0,97 | 0,92 | 253 | 314 | 41 |
| 127 | 50 | 155 | MCD | 0,187 | 2870 | 1,52 | 0,378 | 9,1 | 3,24 | 2,87 | 253 | 314 | 41 |
| 127 | 100 | 155 | MCD | 0,264 | 4058 | 2,14 | 0,636 | 12,9 | 5,45 | 4,54 | 253 | 314 | 41 |
| 220 | 10 | 295 | MCD | 0,044 | 674 | 0,68 | 0,082 | 4,1 | 0,97 | 0,92 | 384 | 445 | 63 |
| 220 | 50 | 295 | MCD | 0,098 | 1508 | 1,52 | 0,274 | 9,1 | 3,24 | 2,87 | 384 | 445 | 63 |
| 220 | 100 | 295 | MCD | 0,139 | 2133 | 2,14 | 0,461 | 12,9 | 5,45 | 4,54 | 384 | 445 | 63 |
| 264 | 10 | 360 | MCD | 0,036 | 554 | 0,68 | 0,074 | 4,1 | 0,97 | 0,92 | 446 | 507 | 74 |
| 264 | 50 | 360 | MCD | 0,081 | 1239 | 1,52 | 0,248 | 9,1 | 3,24 | 2,87 | 446 | 507 | 74 |
| 264 | 100 | 360 | MCD | 0,114 | 1752 | 2,14 | 0,418 | 12,9 | 5,45 | 4,54 | 446 | 507 | 74 |

## Resumo para a escolha dos semicondutores

- MOSFET: Vds máx (com grampo a 1.8·Vr) = **507 V** → classe 650 V (≤ 80 % → 520 V); Ip = 2.14 A ; Ip,rms = 0.815 A
- Diodo de saída: Vrev máx = **74 V** → Schottky 100 V; Is,pk = 12.9 A ; Is,rms = 5.45 A ; Is,med = 3.0 A
- Capacitores de saída: Ic,rms = **4.54 A** (90 VAC, plena carga)
- ton mínimo (264 VAC, 10 %) = 554 ns (UC3845: ok se > ~350 ns)
- Llk estimada (3 % de Lp) = 8.8 µH (entrada do snubber)

Figura: assets/flyback_formas_de_onda.png



---

<!-- saida.py -->
# Filtro de saída

Pior caso (90 VAC, plena carga): Is,pk = 12.9 A, D = 0.433, D2 = 0.537, Ic,rms = 4.54 A

## Critérios (Aula 03)

1. Capacitância mínima (ΔV_C = 50 mV): C ≥ Io·(1−D2)·T/ΔV = 427 µF
2. RSE máxima para ΔVo ≤ 120 mV sem pós-filtro: RSE ≤ 5.4 mΩ → impraticável com 1 eletrolítico ⇒ banco em paralelo + pós-filtro LC
3. Corrente eficaz: Ic,rms = 4.54 A (dado de catálogo a 105 °C, 100 kHz)
4. Tensão: ≥ 1,5–2 × Vo → 25 V
5. Temperatura: 105 °C, vida ≥ 5000 h; operação a Ta = 40 °C prolonga a vida
6. Custo/volume: eletrolítico de baixa impedância 10 × 20 mm

| Capacitor | n paralelo | RSE eq (mΩ) | I ripple (A) | I ripple ≥ Ic,rms | ΔV RSE (mV) | ΔV C (mV) | ΔV1 total (mV) | P RSE (W) |
|---|---|---|---|---|---|---|---|---|
| Rubycon ZLH 1000µF/25V (10x20) | 2 | 9,5 | 4,00 | não | 122 | 11 | 133 | 0,20 |
| Rubycon ZLH 1000µF/25V (10x20) | 3 | 6,3 | 6,00 | sim | 81 | 7 | 89 | 0,13 |
| Nichicon UPW 1000µF/25V (10x20) | 2 | 15,0 | 3,32 | não | 193 | 11 | 204 | 0,31 |
| Nichicon UPW 1000µF/25V (10x20) | 3 | 10,0 | 4,98 | sim | 129 | 7 | 136 | 0,21 |
| Rubycon ZLH 1500µF/25V (12.5x20) | 2 | 7,5 | 5,10 | sim | 96 | 7 | 104 | 0,15 |
| Rubycon ZLH 1500µF/25V (12.5x20) | 3 | 5,0 | 7,65 | sim | 64 | 5 | 69 | 0,10 |

## Escolha: **3 × Rubycon ZLH 1000µF/25V (10x20)** → RSE eq = 6.3 mΩ, I ripple = 6.0 A ≥ 4.54 A, ΔV1 = 89 mV
## Pós-filtro LC: L = 3.3 µH, C = 470 µF (RSE 40 mΩ) → fc = 4.0 kHz, atenuação em 65 kHz = -30 dB → ΔVo ≈ **2.7 mV** (meta 120 mV)
- Indutor do pós-filtro: 3.3 µH, I_DC = 3.0 A → toroide de pó de ferro T68-26 (~10 esp. de 20 AWG) ou indutor radial 3,3 µH ≥ 4 A

Figura: assets/saida_ripple.png



---

<!-- snubber.py -->
# Snubber RCD do MOSFET

Lp = 294 µH, Ip = 2.14 A, Vr = 76.2 V, Vbulk máx = 370 V, fs = 65 kHz, Vc = 1.8·Vr = 137 V

| Llk | E/ciclo (µJ) | P snubber (W) | R (kΩ) | C mín (nF) | t grampo (ns) | Vds máx (V) |
|---|---|---|---|---|---|---|
| 1 % (2.9 µH) | 6,8 | 0,99 | 19,0 | 8,1 | 103 | 507 |
| 2 % (5.9 µH) | 13,5 | 1,98 | 9,5 | 16,2 | 207 | 507 |
| 3 % (8.8 µH) | 20,3 | 2,96 | 6,3 | 24,2 | 310 | 507 |

## Componentes escolhidos (projeto para Llk = 2 %, verificação a 3 %)

- R = **9 kΩ**, potência dissipada 2.01 W (2 %) a 2.61 W (3 %) → 2 resistores de 18 kΩ / 2 W em paralelo (ou 1 × 9 kΩ / 3 W) ; C = **22 nF / 630 V** (poliéster ou cerâmico) ; diodo **UF4007** (1 A, 1000 V, trr 75 ns) ou **MUR160**
- Tensão de grampo real: 135 V (Llk 2 %) / 154 V (Llk 3 %) → Vds máx = 505 / 524 V (classe 650 V: 81 % no pior caso)
- Pico de corrente no diodo do snubber = Ip = 2.14 A ; condução ≈ 207 ns por ciclo
- Alternativa: TVS P6KE180A (Vbr 171–189 V, Vclamp ≈ 246 V @ 24 A) em série com UF4007 → Vds máx ≈ 370 + 246 = 616 V (95 %): **não adotada** (margem insuficiente a 264 VAC)

## RC de amortecimento no diodo de saída

- Llk refletida ao secundário ≈ 163 nH ; Cj ≈ 800 pF → f ring ≈ 13.9 MHz ; R = √(L/C) ≈ 14.3 Ω → **15 Ω** ; C ≈ 3·Cj → **2.4 nF / 100 V** ; P ≈ C·V²·fs = 0.85 W → resistor 1/2 W

Figura: assets/snubber_compromisso.png



---

<!-- uc3845.py -->
# Componentes associados ao UC3845

## Oscilador

- UC3845: fsw = fosc/2 → fosc = 130 kHz ; fosc ≈ 1,72/(RT·CT) → com CT = 2.2 nF, RT = 6.01 kΩ → **RT = 6.04 kΩ (E96), CT = 2.2 nF (NP0/C0G)** → fosc = 129.4 kHz, **fsw = 64.7 kHz**
- Tempo morto do oscilador: CT·ΔV/Idis = 424 ns → Dmax do oscilador 94.5 % (o flip-flop limita a 50 %; datasheet 46–50 %)

## Sensoriamento de corrente (pino ISENSE)

- Ip nominal máx = 2.14 A ; alvo de limitação = 1,25·Ip = 2.68 A → Rs = 0,9 V/2.68 = 0.336 Ω → **Rs = 0.33 Ω** (2 × 0.66 Ω / 1 W em paralelo)
- Limite de corrente resultante: 2.73 A (Vth mín 0,9 V) a 3.03 A (típ. 1,0 V) ; potência em Rs = Ip,rms²·Rs = 0.22 W
- Filtro RC de borda: R = 1000 Ω, C = 220 pF → τ = 220 ns (ton mín = 554 ns → τ < ton,mín/2 ✓)

## Partida (resistor de startup) e alimentação

- R_start = **2 × 82 kΩ / 1 W em série** (164 kΩ) do bulk ao VCC ; C_VCC = **220 µF / 35 V** + 100 nF cerâmico junto ao pino
| Vac | Vbulk pico (V) | I R_start (mA) | I líquida p/ C (mA) | t partida (s) | P R_start (W) |
|---|---|---|---|---|---|
| 90 | 124 | 0,73 | 0,43 | 4,3 | 0,09 |
| 127 | 177 | 1,05 | 0,75 | 2,5 | 0,19 |
| 220 | 308 | 1,85 | 1,55 | 1,2 | 0,58 |
| 264 | 370 | 2,23 | 1,93 | 1,0 | 0,84 |
- Corrente mínima de startup (vale de 90 VAC): 0.53 mA ≥ 0.5 mA (máx. do CI) ✓ ; consumo em operação ≈ 19.2 mA
- Tempo que C_VCC sustenta o CI entre 8,4 e 7,6 V sem o auxiliar: 9.2 ms (o auxiliar deve estabelecer VCC antes disso → soft-start curto)
- Auxiliar: Naux/Ns = 9/7 → Vaux ≈ 15.4 V (< 30 V do zener interno ✓, > 7.6 V ✓) ; diodo **UF4004** + resistor série 10 Ω (filtra o pico de dispersão)

## Acionamento do MOSFET (driver)

- O UC3845 tem saída totem-pole de ±1 A de pico (tr/tf ≈ 50 ns em 1 nF), suficiente para MOSFETs de até ~100 nC a 65 kHz → **driver = o próprio CI**, sem driver externo (Aula 05: circuito básico não isolado, fonte e MOSFET na mesma referência)
- Rg = **10 Ω** (série) + diodo 1N4148 antiparalelo com Rg (desliga mais rápido) + 10 kΩ gate–source (mantém bloqueado antes da partida)

## Compensação de rampa (provisão)

- D máx de projeto = 0.433 < 0,5 e operação em MCD → **não é obrigatória**. Provisão na PCI: resistor do pino RT/CT ao nó ISENSE (após o filtro)
- Inclinação de descida sensoriada m2 = Vr/Lp·Rs = 85.6 mV/µs ; rampa do oscilador 219 mV/µs → para ma = 0,5·m2: R_slope ≈ 5 kΩ (não montar por padrão)

## Outros

- VREF: 1 µF cerâmico ao GND junto ao pino (≥ 0,1 µF) ; VCC: 100 nF cerâmico + C_VCC ; VFB ao GND (amplificador de erro em saturação alta; o controle é feito pelo optoacoplador no pino COMP com pull-up de 4,7 kΩ ao VREF)



---

<!-- semicondutores.py -->
# Semicondutores: pré-escolha, perdas e dissipadores

## Pré-escolha (Aula 03: tensão de bloqueio, corrente de pico e média, pior caso)

- MOSFET: Vds máx (264 VAC + grampo) = 505 V → classe **650 V** (78 %); Ip = 2.14 A, Ip,rms = 0.815 A → ID ≥ 4 A ; TO-220 (dissipador possível)
- Diodo de saída: Vrev = 74 V → Schottky **100 V** (74 %); Is,pk = 12.9 A, Is,med = 3 A, Is,rms = 5.45 A → ≥ 10 A ; Schottky (sem recuperação reversa, Aula 02)
- Ponte: VRRM ≥ 1,5·370 = 555 V → **600 V** ; I_med/diodo = 0.20 A, I_pico = 2.5 A, surto de inrush 31 A → 2–4 A (IFSM ≥ 100 A)

## MOSFET – perdas (90 VAC: pior condução; 264 VAC: pior comutação)

| MOSFET | RDS(on) 25 °C (mΩ) | Qg (nC) | P cond (W) | P on/Coss (W) | P off (W) | P gate (W) | P tot 90 V (W) | P tot 264 V (W) | RθJC | RθSA máx | dissipador | Tj (°C) | custo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| IPA65R400CE (Infineon CoolMOS CE, TO-220FP) | 400 | 20 | 0,15 | 0,14 | 1,08 | 0,017 | 1,14 | 1,38 | 4,00 | 57 | clip Aavid 574502B00000G (TO-220, 19×13 mm) | 79 | ≈ US$ 1,0 |
| STP13N65M2 (ST MDmesh M2, TO-220) | 430 | 17 | 0,15 | 0,12 | 0,86 | 0,014 | 1,04 | 1,15 | 1,14 | 72 | clip Aavid 574502B00000G (TO-220, 19×13 mm) | 69 | ≈ US$ 1,3 |
| FCPF190N65S3 (onsemi SuperFET III, TO-220F) | 190 | 34 | 0,07 | 0,26 | 1,04 | 0,029 | 0,83 | 1,40 | 3,50 | 57 | clip Aavid 574502B00000G (TO-220, 19×13 mm) | 79 | ≈ US$ 1,9 |

**Escolhido: STP13N65M2 (ST MDmesh M2, TO-220)** – menor perda total (1.15 W), RθJC = 1.14 °C/W, TO-220 padrão (mica + pasta) ; dissipador: **clip Aavid 574502B00000G (TO-220, 19×13 mm)** → Tj ≈ 69 °C (meta ≤ 125 °C)
- tf efetivo (carga de gate, Ig,off = Vpl/(Rg+Rg,int+Rdrv)) = 24 ns ; sem dissipador Tj seria 112 °C

## Diodo de saída – perdas e dissipador

| Diodo | V0 (V) | Rd (mΩ) | P (W) | RθJC | RθSA máx | dissipador | Tj (°C) |
|---|---|---|---|---|---|---|---|
| STPS20H100CT (ST, 2×10 A, 100 V) – ânodos em paralelo | 0,55 | 4,5 | 1,78 | 0,45 | 46,7 | clip Aavid 574502B00000G (TO-220, 19×13 mm) | 84 |
| STPS20H100CT (ST) – uma perna | 0,55 | 9,0 | 1,92 | 0,90 | 42,9 | clip Aavid 574502B00000G (TO-220, 19×13 mm) | 89 |
| MBR20100CT (onsemi/Vishay, 2×10 A, 100 V) – paralelo | 0,62 | 6,0 | 2,04 | 1,00 | 40,2 | clip Aavid 574502B00000G (TO-220, 19×13 mm) | 92 |
| MBR10100 (onsemi, 10 A, 100 V) | 0,65 | 12,0 | 2,31 | 2,00 | 34,4 | clip Aavid 574502B00000G (TO-220, 19×13 mm) | 101 |

**Escolhido: STPS20H100CT (ST, 2×10 A, 100 V) – ânodos em paralelo** – P = 1.78 W, dissipador **clip Aavid 574502B00000G (TO-220, 19×13 mm)** → Tj ≈ 84 °C (mesma prática das Tarefas 1 e 2; Tj máx 175 °C)

## Ponte retificadora

- **GBU4J (Vishay, 4 A / 600 V)**: P ≈ 4·(V0·I_med + Rd·I_rms²) = 0.69 W (90 VAC) ; RθJA ≈ 20 °C/W → Tj ≈ 54 °C → sem dissipador

## Orçamento de perdas e rendimento estimado (plena carga)

| Vac | MOSFET | diodo | ponte | transformador | snubber | Rsense | startup | capacitores_saida | NTC | indutor_LC | UC3845 | total (W) | η (%) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 90 | 1,04 | 1,78 | 0,69 | 0,96 | 2,01 | 0,22 | 0,09 | 0,13 | 0,74 | 0,09 | 0,22 | 7,98 | 81,9 |
| 127 | 1,04 | 1,78 | 0,45 | 0,91 | 2,01 | 0,13 | 0,19 | 0,13 | 0,45 | 0,09 | 0,22 | 7,41 | 82,9 |
| 220 | 1,15 | 1,78 | 0,24 | 0,87 | 2,01 | 0,07 | 0,58 | 0,13 | 0,22 | 0,09 | 0,22 | 7,37 | 83,0 |
| 264 | 1,15 | 1,78 | 0,20 | 0,86 | 2,01 | 0,06 | 0,84 | 0,13 | 0,17 | 0,09 | 0,22 | 7,52 | 82,7 |

Hipótese de projeto η = 82 % → estimativa 81.9–83.0 % : consistente

Figura: assets/perdas_semicondutores.png



---

<!-- compensador.py -->
# Compensador da malha de tensão (TL431 + PC817 + UC3845)

## Divisor de realimentação

- Rb = **2.49 kΩ**, Ra = **9.53 kΩ** (1 %) → Vo = 2,495·(1 + Ra/Rb) = **12.04 V**
- R_LED = **2740 Ω** → I_LED máx = 3.0 mA (Vka = 2,5 V) ; R_bias = 1 kΩ em paralelo com o LED → I_ka ≥ 1.2 mA (TL431 exige ≥ 1 mA)
- COMP: pull-up R_pu = 4.7 kΩ ao VREF ; C_p = 1 nF (polo em 33.9 kHz) ; PC817 CTR = 1.0 (rank B/C)

## Planta (controle → saída), modo corrente de pico em MCD

| carga % | Ro (Ω) | G0 (V/V) | G0 (dB) | fp (Hz) | fz RSE (kHz) |
|---|---|---|---|---|---|
| 100 | 4,0 | 6,24 | 15,9 | 22,9 | 7,2 |
| 50 | 8,0 | 8,83 | 18,9 | 11,5 | 7,2 |
| 10 | 40,0 | 19,74 | 25,9 | 2,3 | 7,2 |

## Compensador tipo 2 (zero sobre o polo da planta em plena carga, fc alvo = 1.5 kHz)

- |Gvc(fc)| = -20.2 dB → ganho necessário do compensador 20.2 dB → Rz/Ra = 4.98 → **Rz = 47.50 kΩ**, **Cz = 150 nF** (fz = 22 Hz)

## Margens de estabilidade

| condição | fc (kHz) | margem de fase (°) | margem de ganho (dB) |
|---|---|---|---|
| carga100_ctr1.0 | 1,49 | 99 | ∞ |
| carga10_ctr1.0 | 0,46 | 91 | ∞ |
| carga100_ctr1.6 | 2,48 | 105 | ∞ |
| carga100_ctr0.5 | 0,74 | 95 | ∞ |

Critério MF ≥ 45° em todas as condições: **atende**
- Observação: em 90 VAC/plena carga o conversor entra levemente em MCC (D ≈ 0,44 < 0,5): o ganho da planta cai e surge o zero no semiplano direito em alta frequência (> 10 kHz, fora da banda); a simulação em LTspice verifica o degrau de carga nessa condição.

Figura: assets/compensador_bode.png



---

<!-- emi.py -->
# Filtro de EMI de entrada

## Componentes

- Choke de modo comum L_CM = **10 mH** por enrolamento (≥ 1 A), dispersão ≈ 200 µH (modo diferencial) – ex. Würth 744821110 / Bourns 8109-RC
- C_X1 = **220 nF X2 / 275 VAC** (antes do choke) e C_X2 = **100 nF X2** (após o choke) – ex. EPCOS B32922 / KEMET R46
- C_Y1 = **2.2 nF Y1 / 250 VAC** entre GND primário e GND secundário – ex. Murata DE1E3KX222M / Vishay WKP – corrente de fuga a 250 V/60 Hz = 0.21 mA (< 0,25 mA, classe II)
- Resistores de descarga do X2: 2 × 470 kΩ em série (1 MΩ) → descarga a 34 V em 0.77 s (< 1 s)
- Fusível T2A, NTC 10 Ω, varistor S14K275 (ver entrada.py)

## Frequências de corte estimadas

- Modo diferencial (dispersão do choke + X2): f_DM ≈ 43 kHz ; atenuação em 65 kHz: 25 dB, em 150 kHz: 51 dB, em 1 MHz: 101 dB
- Modo comum (L_CM + C_Y): f_CM ≈ 24.0 kHz ; atenuação em 150 kHz: 26 dB, em 1 MHz: 59 dB
- Harmônicas da corrente do primário a partir de 150 kHz (3ª harmônica de 65 kHz = 195 kHz) são as primeiras dentro da faixa CISPR; o filtro foi dimensionado para ≥ 40 dB em 195 kHz (DM)

Figura: assets/emi_atenuacao.png
