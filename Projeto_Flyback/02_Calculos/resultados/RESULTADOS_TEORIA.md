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
| 150 µF | 4.17 µF/W | 104,1 | 19,9 | 0,80 | 0,579 | 132,0 |

## Retificador + bulk com C = 150 µF (plena carga)

| Vac | f (Hz) | Vb mín | Vb máx | ΔVb | I pico (A) | I in,rms (A) | I D,med (A) | I D,rms (A) | I C,rms (A) | FP | THD % | cond. (°) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 90 | 50 | 104,1 | 124,0 | 19,9 | 2,66 | 0,89 | 0,192 | 0,63 | 0,80 | 0,579 | 132,0 | 42 |
| 90 | 60 | 107,2 | 123,8 | 16,6 | 2,72 | 0,90 | 0,190 | 0,63 | 0,81 | 0,574 | 136,2 | 40 |
| 127 | 50 | 161,9 | 176,4 | 14,4 | 2,39 | 0,69 | 0,130 | 0,49 | 0,64 | 0,514 | 162,4 | 31 |
| 127 | 60 | 164,1 | 176,1 | 12,0 | 2,43 | 0,70 | 0,129 | 0,50 | 0,65 | 0,510 | 165,5 | 30 |
| 220 | 50 | 299,1 | 307,7 | 8,6 | 2,02 | 0,48 | 0,072 | 0,34 | 0,46 | 0,423 | 212,4 | 20 |
| 220 | 60 | 300,3 | 307,5 | 7,2 | 2,03 | 0,48 | 0,072 | 0,34 | 0,46 | 0,421 | 214,3 | 20 |
| 264 | 50 | 362,7 | 369,9 | 7,2 | 1,90 | 0,42 | 0,060 | 0,30 | 0,41 | 0,397 | 229,7 | 17 |
| 264 | 60 | 363,6 | 369,6 | 6,0 | 1,92 | 0,43 | 0,060 | 0,30 | 0,41 | 0,395 | 231,3 | 17 |

## Proteções e componentes de entrada

- Corrente eficaz de entrada máxima (90 VAC): 0.89 A → fusível 2,5× = 2.22 A → **T 2 A / 500 V (5x20 mm, ação lenta)**
- Inrush sem NTC (264 VAC): 187 A ; com NTC 10 Ω frio: 31.1 A → **NTC 10 Ω / 2–3 A (ex.: 10D-9 ou 10D-11)**
- Varistor: **MOV 275 VAC (ex.: S14K275 / 14D431K), Vclamp ≈ 710 V @ 50 A**
- Ponte: I_med = 0.192 A, I_rms = 0.63 A, I_pico = 2.7 A, VRRM ≥ 560 V → **GBU4J (4 A / 600 V) ou KBP206 (2 A / 600 V)**
- Bulk: 150 µF / 400 V, I_C,rms = 0.80 A (90 VAC) → **Nichicon UCY2G151MHD (150 µF/400 V, 105 °C)**
- Vbulk mín (90 VAC/50 Hz) = 104.1 V ; Vbulk máx (264 VAC) = 369.6 V

Figura: assets/entrada_formas_de_onda.png



---

<!-- transformador.py -->
# Projeto fisico do transformador flyback (Aula 04C)

Dados: Po = 36 W, fs = 65 kHz, Vbulk,min = 94.6 V, η = 0.82, B = 0.25 T, kw = 0.4, kp = 0.3, J = 450 A/cm², Dmax = 0.43

- Ip = 2.159 A ; W = Po/(η·fs) = 675 µJ
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
- Primário: Ip,rms = 0.814 A → 1 × 23 AWG ; Secundário: Is,rms = 5.45 A → 5 × 23 AWG ; Auxiliar: 1 × 28 AWG
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

- Vbulk mín = 94.6 V (90 VAC/50 Hz), Vbulk máx = 369.6 V (264 VAC)
- Vr = Dmax/(1−Dmax)·Vbulk,min = 0.43/(1−0.43)·94.6 = **71.4 V**
- n = Np/Ns = Vr/(Vo+Vf) = 71.4/(12.0+0.7) = **5.62**
- Ip = 2·Po/(η·Vbulk,min·Dmax) = 2·36/(0.82·94.6·0.43) = **2.159 A**
- Lp = Vbulk,min·Dmax/(Ip·fs) = **289.9 µH** ; energia por ciclo W = Po/(η·fs) = 675 µJ

**Valores finais do transformador (trafo.json):** n = 6.000 (42:7), Lp = 293.8 µH

## Esforços por ponto de operação (final; correntes no vale de Vbulk, tensões no pico)

| Vac | carga % | Vb vale | modo | D | ton (ns) | Ip (A) | Ip,rms (A) | Is,pk (A) | Is,rms (A) | Ic,rms (A) | Vds off (V) | Vds c/ grampo (V) | Vd rev (V) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 90 | 10 | 104 | MCD | 0,124 | 1914 | 0,68 | 0,138 | 4,1 | 0,97 | 0,92 | 200 | 261 | 33 |
| 90 | 50 | 104 | MCD | 0,278 | 4280 | 1,52 | 0,462 | 9,1 | 3,24 | 2,87 | 200 | 261 | 33 |
| 90 | 100 | 104 | MCD | 0,393 | 6053 | 2,14 | 0,776 | 12,9 | 5,45 | 4,54 | 200 | 261 | 33 |
| 127 | 10 | 162 | MCD | 0,080 | 1230 | 0,68 | 0,111 | 4,1 | 0,97 | 0,92 | 252 | 313 | 41 |
| 127 | 50 | 162 | MCD | 0,179 | 2751 | 1,52 | 0,370 | 9,1 | 3,24 | 2,87 | 252 | 313 | 41 |
| 127 | 100 | 162 | MCD | 0,253 | 3890 | 2,14 | 0,623 | 12,9 | 5,45 | 4,54 | 252 | 313 | 41 |
| 220 | 10 | 299 | MCD | 0,043 | 666 | 0,68 | 0,081 | 4,1 | 0,97 | 0,92 | 384 | 445 | 63 |
| 220 | 50 | 299 | MCD | 0,097 | 1489 | 1,52 | 0,272 | 9,1 | 3,24 | 2,87 | 384 | 445 | 63 |
| 220 | 100 | 299 | MCD | 0,137 | 2106 | 2,14 | 0,458 | 12,9 | 5,45 | 4,54 | 384 | 445 | 63 |
| 264 | 10 | 363 | MCD | 0,036 | 549 | 0,68 | 0,074 | 4,1 | 0,97 | 0,92 | 446 | 507 | 74 |
| 264 | 50 | 363 | MCD | 0,080 | 1228 | 1,52 | 0,247 | 9,1 | 3,24 | 2,87 | 446 | 507 | 74 |
| 264 | 100 | 363 | MCD | 0,113 | 1737 | 2,14 | 0,416 | 12,9 | 5,45 | 4,54 | 446 | 507 | 74 |

## Resumo para a escolha dos semicondutores

- MOSFET: Vds máx (com grampo a 1.8·Vr) = **507 V** → classe 650 V (≤ 80 % → 520 V); Ip = 2.14 A ; Ip,rms = 0.776 A
- Diodo de saída: Vrev máx = **74 V** → Schottky 100 V; Is,pk = 12.9 A ; Is,rms = 5.45 A ; Is,med = 3.0 A
- Capacitores de saída: Ic,rms = **4.54 A** (90 VAC, plena carga)
- ton mínimo (264 VAC, 10 %) = 549 ns (UC3845: ok se > ~350 ns)
- Llk estimada (3 % de Lp) = 8.8 µH (entrada do snubber)

Figura: assets/flyback_formas_de_onda.png



---

<!-- saida.py -->
# Filtro de saída

Pior caso (90 VAC, plena carga): Is,pk = 12.9 A, D = 0.393, D2 = 0.537, Ic,rms = 4.54 A

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

- R = **9 kΩ**, potência dissipada 2.02 W (2 %) a 2.62 W (3 %) → 2 resistores de 18 kΩ / 2 W em paralelo (ou 1 × 9 kΩ / 3 W) ; C = **22 nF / 630 V** (poliéster ou cerâmico) ; diodo **UF4007** (1 A, 1000 V, trr 75 ns) ou **MUR160**
- Tensão de grampo real: 135 V (Llk 2 %) / 153 V (Llk 3 %) → Vds máx = 504 / 523 V (classe 650 V: 80 % no pior caso)
- Pico de corrente no diodo do snubber = Ip = 2.14 A ; condução ≈ 207 ns por ciclo
- Alternativa: TVS P6KE180A (Vbr 171–189 V, Vclamp ≈ 246 V @ 24 A) em série com UF4007 → Vds máx ≈ 370 + 246 = 616 V (95 %): **não adotada** (margem insuficiente a 264 VAC)

## RC de amortecimento no diodo de saída

- Llk refletida ao secundário ≈ 163 nH ; Cj ≈ 800 pF → f ring ≈ 13.9 MHz ; R = √(L/C) ≈ 14.3 Ω → **15 Ω** ; C ≈ 3·Cj → **2.2 nF / 100 V** ; P ≈ C·V²·fs = 0.85 W → resistor 1/2 W

Figura: assets/snubber_compromisso.png



---

<!-- uc3845.py -->
# Componentes associados ao UC3845

## Oscilador

- UC3845: fsw = fosc/2 → fosc = 130 kHz ; fosc ≈ 1,72/(RT·CT) → com CT = 2.2 nF, RT = 6.01 kΩ → **RT = 6.04 kΩ (E96), CT = 2.2 nF (NP0/C0G)** → fosc = 129.4 kHz, **fsw = 64.7 kHz**
- Tempo morto do oscilador: CT·ΔV/Idis = 424 ns → Dmax do oscilador 94.5 % (o flip-flop limita a 50 %; datasheet 46–50 %)

## Sensoriamento de corrente (pino ISENSE)

- Ip nominal máx = 2.14 A ; alvo de limitação = 1,25·Ip = 2.68 A → Rs = 0,9 V/2.68 = 0.336 Ω → **Rs = 0.34 Ω** (2 × 0.68 Ω / 1 W em paralelo)
- Limite de corrente resultante: 2.65 A (Vth mín 0,9 V) a 2.94 A (típ. 1,0 V) ; potência em Rs = Ip,rms²·Rs = 0.20 W
- Filtro RC de borda: R = 330 Ω, C = 100 pF → τ = 33 ns (ton mín = 549 ns → τ < ton,mín/2 ✓)

## Partida (resistor de startup) e alimentação

- R_start = **2 × 82 kΩ / 1 W em série** (164 kΩ) do bulk ao VCC ; C_VCC = **220 µF / 35 V** + 100 nF cerâmico junto ao pino
| Vac | Vbulk pico (V) | I R_start (mA) | I líquida p/ C (mA) | t partida (s) | P R_start (W) |
|---|---|---|---|---|---|
| 90 | 124 | 0,73 | 0,43 | 4,3 | 0,09 |
| 127 | 176 | 1,05 | 0,75 | 2,5 | 0,19 |
| 220 | 307 | 1,85 | 1,55 | 1,2 | 0,58 |
| 264 | 370 | 2,23 | 1,93 | 1,0 | 0,83 |
- Corrente mínima de startup (vale de 90 VAC): 0.58 mA ≥ 0.5 mA (máx. do CI) ✓ ; consumo em operação ≈ 19.2 mA
- Tempo que C_VCC sustenta o CI entre 8,4 e 7,6 V sem o auxiliar: 9.2 ms (o auxiliar deve estabelecer VCC antes disso → soft-start curto)
- Auxiliar: Naux/Ns = 9/7 → Vaux ≈ 15.4 V (< 30 V do zener interno ✓, > 7.6 V ✓) ; diodo **UF4004** + resistor série **100 Ω** (rev. B: filtra o pico de dispersão para que, com a saída em curto, o auxiliar não sustente o VCC e o CI desligue por UVLO)

### Curto-circuito na saída: desligamento por UVLO e religamento (hiccup)

- Com a saída em curto a tensão do auxiliar cai a ≈ 0.9 V e, com R_aux = 100 Ω, os picos de dispersão não sustentam o VCC: C_VCC descarrega de 15.4 V a 7.6 V com I_CC − I_start, o CI desliga, R_start recarrega C_VCC até 8.4 V e o CI tenta de novo por t_run
| Vac | t até UVLO (ms) | t recarga (ms) | t ligado por tentativa (ms) | ciclo de trabalho da falha (%) |
|---|---|---|---|---|
| 90 | 138 | 854 | 14,1 | 1,6 |
| 127 | 141 | 335 | 14,5 | 4,1 |
| 220 | 151 | 133 | 15,5 | 10,4 |
| 264 | 157 | 103 | 16,0 | 13,4 |

## Acionamento do MOSFET (driver)

- O UC3845 tem saída totem-pole de ±1 A de pico (tr/tf ≈ 50 ns em 1 nF), suficiente para MOSFETs de até ~100 nC a 65 kHz → **driver = o próprio CI**, sem driver externo (Aula 05: circuito básico não isolado, fonte e MOSFET na mesma referência)
- Rg = **10 Ω** (série) + diodo 1N4148 antiparalelo com Rg (desliga mais rápido) + 10 kΩ gate–source (mantém bloqueado antes da partida)

## Compensação de rampa (provisão)

- D máx de projeto = 0.393 < 0,5 e operação em MCD → **não é obrigatória**. Provisão na PCI: resistor do pino RT/CT ao nó ISENSE (após o filtro)
- Inclinação de descida sensoriada m2 = Vr/Lp·Rs = 88.2 mV/µs ; rampa do oscilador 219 mV/µs → para ma = 0,5·m2: R_slope ≈ 2 kΩ (não montar por padrão)

## Outros

- VREF: 1 µF cerâmico ao GND junto ao pino (≥ 0,1 µF) ; VCC: 100 nF cerâmico + C_VCC ; VFB ao GND (amplificador de erro em saturação alta; o controle é feito pelo optoacoplador no pino COMP com pull-up de 4,7 kΩ ao VREF)



---

<!-- semicondutores.py -->
# Semicondutores: pré-escolha, perdas e dissipadores

## Pré-escolha (Aula 03: tensão de bloqueio, corrente de pico e média, pior caso)

- MOSFET: Vds máx (264 VAC + grampo) = 504 V → classe **650 V** (78 %); Ip = 2.14 A, Ip,rms = 0.776 A → ID ≥ 4 A ; TO-220 (dissipador possível)
- Diodo de saída: Vrev = 74 V → Schottky **100 V** (74 %); Is,pk = 12.9 A, Is,med = 3 A, Is,rms = 5.45 A → ≥ 10 A ; Schottky (sem recuperação reversa, Aula 02)
- Ponte: VRRM ≥ 1,5·370 = 554 V → **600 V** ; I_med/diodo = 0.19 A, I_pico = 2.7 A, surto de inrush 31 A → 2–4 A (IFSM ≥ 100 A)

## MOSFET – perdas (90 VAC: pior condução; 264 VAC: pior comutação)

| MOSFET | RDS(on) 25 °C (mΩ) | Qg (nC) | P cond (W) | P on/Coss (W) | P off (W) | P gate (W) | P tot 90 V (W) | P tot 264 V (W) | RθJC | RθSA máx | dissipador | Tj (°C) | custo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| IPA65R400CE (Infineon CoolMOS CE, TO-220FP) | 400 | 20 | 0,15 | 0,14 | 1,07 | 0,017 | 1,09 | 1,38 | 4,00 | 57 | clip Aavid 574502B00000G (TO-220, 19×13 mm) | 79 | ≈ US$ 1,0 |
| STP13N65M2 (ST MDmesh M2, TO-220) | 430 | 17 | 0,15 | 0,12 | 0,86 | 0,014 | 0,98 | 1,15 | 1,14 | 72 | clip Aavid 574502B00000G (TO-220, 19×13 mm) | 69 | ≈ US$ 1,3 |
| STF13N65M2 (ST MDmesh M2, TO-220FP isolado) | 430 | 17 | 0,15 | 0,12 | 0,86 | 0,014 | 0,98 | 1,15 | 3,50 | 70 | clip Aavid 574502B00000G (TO-220, 19×13 mm) | 72 | ≈ US$ 1,4 |
| FCPF190N65S3 (onsemi SuperFET III, TO-220F) | 190 | 34 | 0,07 | 0,26 | 1,04 | 0,029 | 0,81 | 1,40 | 3,50 | 57 | clip Aavid 574502B00000G (TO-220, 19×13 mm) | 79 | ≈ US$ 1,9 |

**Escolhido: STF13N65M2 (ST MDmesh M2, TO-220FP isolado)** – menor perda total (1.15 W), RθJC = 3.5 °C/W, encapsulamento isolado TO-220FP (sem mica; dissipador clip sem tensão) ; dissipador: **clip Aavid 574502B00000G (TO-220, 19×13 mm)** → Tj ≈ 72 °C (meta ≤ 125 °C)
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

- **GBU4J (Vishay, 4 A / 600 V)**: P ≈ 4·(V0·I_med + Rd·I_rms²) = 0.67 W (90 VAC) ; RθJA ≈ 20 °C/W → Tj ≈ 53 °C → sem dissipador

## Orçamento de perdas e rendimento estimado (plena carga)

| Vac | MOSFET | diodo | ponte | transformador | snubber | Rsense | startup | capacitores_saida | NTC | indutor_LC | UC3845 | total (W) | η (%) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 90 | 0,98 | 1,78 | 0,67 | 0,95 | 2,02 | 0,20 | 0,09 | 0,13 | 0,79 | 0,09 | 0,22 | 7,94 | 81,9 |
| 127 | 0,98 | 1,78 | 0,45 | 0,90 | 2,02 | 0,13 | 0,19 | 0,13 | 0,48 | 0,09 | 0,22 | 7,39 | 83,0 |
| 220 | 1,15 | 1,78 | 0,24 | 0,87 | 2,02 | 0,07 | 0,58 | 0,13 | 0,23 | 0,09 | 0,22 | 7,39 | 83,0 |
| 264 | 1,15 | 1,78 | 0,20 | 0,86 | 2,02 | 0,06 | 0,83 | 0,13 | 0,18 | 0,09 | 0,22 | 7,53 | 82,7 |

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
| 100 | 4,0 | 6,06 | 15,6 | 26,5 | 8,4 |
| 50 | 8,0 | 8,57 | 18,7 | 13,3 | 8,4 |
| 10 | 40,0 | 19,16 | 25,6 | 2,7 | 8,4 |

## Compensador tipo 2 (zero sobre o polo da planta em plena carga, fc alvo = 0.8 kHz)

- |Gvc(fc)| = -14.9 dB → ganho necessário do compensador 14.9 dB → Rz/Ra = 2.26 → **Rz = 21.50 kΩ**, **Cz = 270 nF** (fz = 27 Hz)

## Margens de estabilidade

| condição | fc (kHz) | margem de fase (°) | margem de ganho (dB) |
|---|---|---|---|
| carga100_ctr1.0 | 0,79 | 88 | 13 |
| carga10_ctr1.0 | 0,25 | 86 | 23 |
| carga100_ctr1.6 | 1,35 | 86 | 9 |
| carga100_ctr0.5 | 0,39 | 90 | 19 |

Critério MF ≥ 45° em todas as condições: **atende**
- Observação: em 90 VAC/plena carga o conversor entra levemente em MCC (D ≈ 0,44 < 0,5): o ganho da planta cai e surge o zero no semiplano direito em alta frequência (> 10 kHz, fora da banda); a simulação em LTspice verifica o degrau de carga nessa condição.

Figura: assets/compensador_bode.png



---

<!-- emi.py -->
# Filtro de EMI de entrada

## Componentes

- Choke de modo comum L_CM = **10 mH** por enrolamento (≥ 1 A), dispersão ≈ 200 µH (modo diferencial) – Schaffner RN214-1.2-02-10M (1,2 A a 40 °C ≥ 0,89 A rms em 90 V; rev. B)
- C_X1 = **220 nF X2 / 275 VAC** (antes do choke) e C_X2 = **100 nF X2** (após o choke) – ex. EPCOS B32922 / KEMET R46
- C_Y1 = **2.2 nF Y1 / 250 VAC** entre GND primário e GND secundário – ex. Murata DE1E3KX222M / Vishay WKP – corrente de fuga a 250 V/60 Hz = 0.21 mA (< 0,25 mA, classe II)
- Resistores de descarga do X2: 2 × 470 kΩ em série (1 MΩ) → descarga a 34 V em 0.77 s (< 1 s)
- Fusível T2A, NTC 10 Ω, varistor S14K275 (ver entrada.py)

## Frequências de corte estimadas

- Modo diferencial (dispersão do choke + X2): f_DM ≈ 43 kHz ; atenuação em 65 kHz: 25 dB, em 150 kHz: 51 dB, em 1 MHz: 101 dB
- Modo comum (L_CM + C_Y): f_CM ≈ 24.0 kHz ; atenuação em 150 kHz: 26 dB, em 1 MHz: 59 dB
- Harmônicas da corrente do primário a partir de 150 kHz (3ª harmônica de 65 kHz = 195 kHz) são as primeiras dentro da faixa CISPR; o filtro foi dimensionado para ≥ 40 dB em 195 kHz (DM)

Figura: assets/emi_atenuacao.png
