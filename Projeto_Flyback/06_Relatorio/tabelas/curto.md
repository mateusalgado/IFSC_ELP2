| Janela (S, 220 VAC) | Id(Q1) máx (A) | I<sub>p</sub> máx (A) | B equiv. (T) | I(D1) máx (A) | I(D1) rms (A) | V<sub>ds</sub> máx (V) | VCC mín (V) | V<sub>o</sub> máx (V) | P<sub>D1</sub> média (W) |
|---|---|---|---|---|---|---|---|---|---|
| aplicação (2 ms) | 8,05 | 8,05 | 0,94 | 56,8 | 21,5 | 560 | 14,16 | 12,06 | 13,17 |
| curto sustentado | 3,41 | 3,41 | 0,40 | 23,9 | 13,1 | 423 | 7,60 | 0,21 | 6,23 |
| recuperação | 0,00 | 0,00 | 0,00 | 0,0 | 0,0 | 309 | 7,66 | 0,00 | 0,00 |

Releitura do .raw (`analisa_curto.py`, `hiccup_tempos.py`): pulsos de comando no curto sustentado = 11721; hiccup: 163 ms até o UVLO, 130 ms desligado, 20 ms ligado por tentativa (ciclo de trabalho da falha 14 %; cálculo: 15,5 ms / 10,4 %). Curto removido em 380 ms com o CI desligado: VCC = 7,90 V no fim da simulação (420 ms), religamento na tentativa seguinte do hiccup, seguido da partida normal.
