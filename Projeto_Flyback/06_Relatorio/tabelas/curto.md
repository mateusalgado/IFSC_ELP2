| Janela (S, 220 VAC) | Id(Q1) máx (A) | I<sub>p</sub> máx (A) | B equiv. (T) | I(D1) máx (A) | I(D1) rms (A) | V<sub>ds</sub> máx (V) | VCC mín (V) | V<sub>o</sub> máx (V) | P<sub>D1</sub> média (W) |
|---|---|---|---|---|---|---|---|---|---|
| aplicação (2 ms) | 7,80 | 7,79 | 0,91 | 55,1 | 20,9 | 555 | 14,16 | 12,06 | 12,81 |
| curto sustentado | 3,34 | 3,34 | 0,39 | 23,6 | 12,5 | 422 | 7,90 | 0,21 | 5,70 |
| recuperação | 0,00 | 0,00 | 0,00 | 0,0 | 0,0 | 310 | 8,23 | 0,00 | 0,00 |

Releitura do .raw (`analisa_curto.py`, `hiccup_tempos.py`): pulsos de comando no curto sustentado = 10859; hiccup: 155 ms até o UVLO, 97 ms desligado, 15 ms ligado por tentativa (ciclo de trabalho da falha 13 %; cálculo: 15,5 ms / 10,4 %). Curto removido em 380 ms com o CI desligado: VCC = 8,48 V no fim da simulação (420 ms), religamento na tentativa seguinte do hiccup, seguido da partida normal.
