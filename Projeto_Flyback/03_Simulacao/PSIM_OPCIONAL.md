# Reprodução da simulação no PSIM (opcional) – revisão B

A simulação oficial do projeto foi feita em LTspice (`gera_netlist.py` → `netlists/*.net`, `executa_b.py`, `plota.py`), com modelo comportamental do UC3845 validado contra o datasheet. Se for desejado mostrar a figura também na ferramenta da disciplina, o exemplo `PSIM\examples\PWM IC\UC3844-flyback.psimsch` (PSIM 9.1.1) pode ser adaptado com os valores finais abaixo (o UC3844 do exemplo tem o mesmo bloco funcional do UC3845; trocar o limite de razão cíclica para 50 % no bloco do CI, se disponível, ou manter o UC3844 com D < 0,5 garantido pelo projeto).

## Valores finais a colocar no esquemático do PSIM

| Elemento do exemplo | Valor do projeto |
|---|---|
| Fonte CA | 90 / 127 / 220 / 264 V rms, 50 ou 60 Hz |
| Ponte + capacitor de bulk | 4 diodos; C = 150 µF, ESR 0,8 Ω (NTC 2 Ω + dispersão do choke 200 µH / 0,39 Ω em série com a fonte) |
| Transformador (bloco "TF_IDEAL" ou "flyback transformer") | Lp = 294 µH, Np:Ns:Naux = 42:7:9 ; Llk = 5,9 µH (2 %) no primário |
| MOSFET | 650 V, Rds(on) = 0,43 Ω (ou chave ideal com Ron = 0,6 Ω para 100 °C) |
| Snubber RCD | D = UF4007 (ou ideal), C = 22 nF, R = 9,1 kΩ |
| Diodo de saída | Schottky Vf = 0,55 V, Rd = 4,5 mΩ |
| Capacitores de saída | 3 × 1000 µF (ESR 19 mΩ cada) + pós-filtro L = 3,3 µH / C = 470 µF (ESR 40 mΩ) |
| Carga | 4 Ω (3 A), 8 Ω (50 %), 40 Ω (10 %) |
| UC3845: RT / CT | 6,04 kΩ / 2,2 nF (fsw = 65 kHz) |
| Rsense + filtro | 0,34 Ω (2 × 0,68 Ω) ; 330 Ω / 100 pF no pino 3 |
| Resistor de gate | 10 Ω |
| Partida e VCC | 164 kΩ do bulk ao VCC ; C_VCC = 220 µF ; auxiliar com UF4004 + **100 Ω** (R13, hiccup no curto) |
| Realimentação | TL431 com Ra = 9,53 kΩ, Rb = 2,49 kΩ, Rz = 21,5 kΩ, Cz = 270 nF, R_LED = 2,74 kΩ, R_bias = 1 kΩ ; PC817 CTR = 1 ; pull-up do COMP 4,7 kΩ ao VREF (5 V), C_p = 1 nF |
| Passo de simulação | 50 ns ; tempo total 100 ms (regime, 6 ciclos de rede) / 100 ms (partida a frio) / 120 ms (degraus em 80 e 100 ms) / 420 ms (curto de 60 a 380 ms) |

## Rodar em lote (sem abrir a interface)

```
"C:\Program Files\Powersim\PSIM9.1.1\PsimCmd.exe" -i "fonte_flyback.psimsch" -o "fonte_flyback.txt" -v "Vin=220" -v "Rload=4" -t 60e-3 -s 50e-9
```

O arquivo de saída (`.txt`) pode ser lido no SIMVIEW ou em Python (colunas separadas por espaço) com o mesmo `plota.py` adaptado.

## Grandezas a comparar com a Tabela do relatório

Vo médio e ondulação, Ip (corrente no Rsense ÷ 0,33), Is,pk, Vds máx (com e sem snubber), Vbulk mínimo, rendimento (Pin/Po) e o degrau de carga 50 → 100 %.
