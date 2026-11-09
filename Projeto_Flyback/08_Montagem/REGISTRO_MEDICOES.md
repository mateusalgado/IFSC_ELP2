# Registro de medições do protótipo – revisão B (Possibilidade II)

Preencher **durante** os ensaios, na ordem do `GUIA_MONTAGEM.md`. Cada linha tem a referência de cálculo [C] e de simulação [S] já preenchida pela revisão B; a coluna **[M]** é a medição física (instrumento, escala e condição anotados). Ao final, copiar os valores para `medicoes.json` (modelo em `medicoes.template.json`) — a revisão C do relatório lê esse arquivo. Nada aqui foi medido ainda: todas as células [M] estão vazias.

Identificação: data ____/____/2026 · bancada ____________ · responsável ____________ · instrumentos (modelo/série): osciloscópio ________ sonda diferencial ________ multímetro ________ wattímetro ________ LCR ________ carga ________

## 0. Divergências de montagem em relação à BOM B

| Ref. | Previsto (BOM B) | Montado | Motivo |
|---|---|---|---|
| | | | |

## 1. Transformador T1 (antes de montar na placa) – guia §3

| Ensaio | Aceite | T1 nº 1 [M] | T1 nº 2 [M] | Instrumento / condição |
|---|---|---|---|---|
| L<sub>p</sub> (pinos 1–3) | 265–325 µH | | | LCR, ___ kHz |
| L<sub>lk</sub> (1–3 com 6/7 curto a 9/10) | < 9 µH | | | |
| Relação 42:7 (5 V / 10 kHz em 1–3 → 6/7–9/10) | 0,83 V ± 5 %, mesma polaridade | | | |
| Relação 42:9 (→ 4–5) | 1,07 V ± 5 % | | | |
| Isolação prim–sec (500 V) | ≥ 100 MΩ | | | |
| Entreferro final / AL | 0,45 mm central | | | |

## 2. Blocos 1 e 2 – guia §4

| Grandeza | Aceite | [M] | Condição |
|---|---|---|---|
| V<sub>bulk</sub> (TP1–TP9) em 127 V, bloco 1 | ≈ 175 V | | isolador + variac |
| VREF (TP6) com 15 V em TP5 | 5,0 V | | fonte de bancada |
| Dente de serra pino 4 | 1,2–2,8 V, ≈ 130 kHz | | |
| Saída pino 6 | ≈ 13 V, 65 kHz, D ≤ 48 % | | |
| Consumo do CI | 15–20 mA | | |
| Gate (TP4) com Q1 | bordas limpas, sem oscilação | | |
| Bloco 3: V<sub>o</sub> em 40–60 VAC, 40 Ω | 12 V regulando | | |

## 3. Regime permanente – guia §5.1 (carga 100 % = 4 Ω; 50 % = 8 Ω; 10 % = 40 Ω)

| V<sub>ac</sub> | carga | V<sub>o</sub> [M] (V) | ΔV<sub>o</sub> chav. [M] (mV) | excursão total [M] (mV) | I<sub>p</sub> [M] (A, TP3÷0,34) | V<sub>ds</sub> máx [M] (V, dif.) | V<sub>rev</sub> D1 [M] (V) | VCC [M] (V) | P<sub>in</sub> [M] (W) | η [M] (%) | V<sub>bulk</sub> mín [M] (V) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 90 | 10 % | | | | | | | | | | |
| 90 | 50 % | | | | | | | | | | |
| 90 | 100 % | | | | | | | | | | |
| 127 | 10 % | | | | | | | | | | |
| 127 | 50 % | | | | | | | | | | |
| 127 | 100 % | | | | | | | | | | |
| 220 | 10 % | | | | | | | | | | |
| 220 | 50 % | | | | | | | | | | |
| 220 | 100 % | | | | | | | | | | |
| 264 | 10 % | | | | | | | | | | |
| 264 | 50 % | | | | | | | | | | |
| 264 | 100 % | | | | | | | | | | |

Referências B (plena carga): V<sub>o</sub> 12,06 V [S]; ondulação ≤ 4,2 mV / excursão ≤ 9,2 mV [S]; I<sub>p</sub> 2,06–2,07 A [S] (2,14 [C]); V<sub>ds</sub> 247 / 296 / 422 / 482 V [S] (261 / 314 / 445 / 507 [C]); η 82,8 / 84,8 / 85,3 / 84,6 % [S]; V<sub>bulk</sub> mín 104 V em 90 V/50 Hz [C].

Formas de onda a salvar (PNG/CSV do osciloscópio, nome `osc_<Vac>V_<carga>pct_<sinal>.png`): dreno (TP2, diferencial), SW (TP3), V<sub>o</sub> AC acoplado (TP10), corrente da rede (sonda de corrente) em 90 e 264 V plena carga.

## 4. Partida a frio – guia §5.2

| Grandeza | Aceite | 90 V [M] | 264 V [M] |
|---|---|---|---|
| Tempo até o UVLO (VCC chega a 8,4 V) | < 10 s (S: 7,4 / 1,1 s) | | |
| V<sub>o</sub> ≥ 11,4 V após início do chaveamento | < 50 ms, sem sobretensão > 12,6 V | | |
| V<sub>o</sub> máximo na partida | ≤ 12,6 V | | |
| V<sub>ds</sub> máx na partida | ≤ 520 V (S: 517 V em 264 V) | | |
| Pico de I<sub>p</sub> na partida | ≤ 3,5 A por < 1 ms (S: 3,1–3,45 A) | | |
| VCC mínimo após o UVLO | > 7,6 V | | |

## 5. Degraus de carga 50 ↔ 100 % – guia §5.3

| V<sub>ac</sub> | sentido | ΔV<sub>o</sub> [M] (mV) | retorno a ±1 % [M] (ms) | oscilação? | Referência B |
|---|---|---|---|---|---|
| 90 | 50 → 100 % | | | | −114 mV, não sai de ±1 % [S] |
| 90 | 100 → 50 % | | | | +115 mV [S] |
| 264 | 50 → 100 % | | | | −116 mV [S] |
| 264 | 100 → 50 % | | | | +113 mV [S] |

## 6. Térmico (após 30 min em 220 V / 3 A, T<sub>a</sub> = ____ °C)

| Componente | Previsto [C] | T medida [M] (°C) | Método |
|---|---|---|---|
| Q1 (aleta do clip) | T<sub>j</sub> ≈ 72 °C | | |
| D1 (aleta) | T<sub>j</sub> ≈ 84 °C | | |
| Ponte BR1 | T<sub>j</sub> ≈ 53 °C | | |
| R5 / R6 (grampo) | 1,0 W cada | | |
| T1 (núcleo / cobre) | ΔT ≈ 29 °C | | |
| C1, C10–C12 | < 60 °C | | |

## 7. Curto-circuito – guia §5.4 (SÓ se liberado: isolador, 127 V primeiro, 2 s, chave ≤ 50 mΩ)

| Grandeza | Limite de parada | [M] 127 V | [M] 220 V |
|---|---|---|---|
| I<sub>p</sub> sustentada (TP3) | > 3,5 A → parar | | |
| VCC cai abaixo de 8 V em ≤ 300 ms? | não cair → parar (S: 155 ms) | | |
| Período do hiccup (desligado / ligado) | S: 97 ms / 15 ms em 220 V | | |
| V<sub>ds</sub> máx na aplicação | ≤ 600 V (S: 555 V) | | |
| Temperatura de D1 após 30 s de curto | < 100 °C | | |
| Religamento ao remover o curto | sim, sem sobretensão | | |

## 8. Ocorrências e diagnósticos (guia §6)

| Data/hora | Sintoma | Causa encontrada | Ação |
|---|---|---|---|
| | | | |
