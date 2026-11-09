# Especificação do produto – Fonte chaveada flyback 12 V / 3 A

**Projeto Semestral – Eletrônica de Potência II (2026-2)** · Tema II · Aluno: Mateus Salgado Barboza Costa · Prof. Joabel Moia

## 1. Ideia de produto e aplicações

Fonte de alimentação CA-CC compacta de **36 W (12 V / 3 A)**, entrada universal, para:

- roteadores, modems e switches de rede (12 V / 1–3 A);
- câmeras e gravadores de CFTV (12 V);
- fitas e luminárias LED de 12 V;
- automação residencial e pequenos equipamentos de bancada.

É a mesma classe das fontes "adaptador de mesa" de 36 W. O enunciado (Tema II) exige: retificador ponte completa com filtro capacitivo + conversor flyback, CI dedicado **UC3845**, proteção contra surtos da rede, filtro de EMI, grampeamento de tensão sobre o transistor (snubber) e malha fechada da tensão de saída.

## 2. Requisitos elétricos

| Item | Requisito | Origem |
|---|---|---|
| Tensão de entrada | 90 a 264 VAC eficaz ("multi tensão"), 50/60 Hz; nominal 127 V e 220 V | Enunciado (220 VAC ou multi tensão) |
| Tensão de saída | 12,0 V ± 5 % (11,4 a 12,6 V) em toda a faixa de linha e carga | Escolha de projeto (< 25 V, enunciado) |
| Corrente de saída | 0,3 A (10 %) a 3,0 A (100 %); potência nominal 36 W | Escolha de projeto |
| Ondulação de saída | ≤ 120 mV pico a pico (1 % de Vo) em plena carga | Mesmo critério das Tarefas 1–3 |
| Rendimento | ≥ 85 % em plena carga, 220 V | Meta de projeto (η usado nos cálculos) |
| Regulação de linha e carga | ≤ ±2 % (malha fechada com TL431 + optoacoplador) | Enunciado (malha fechada) |
| Frequência de comutação | 65 kHz (UC3845, razão cíclica máxima 50 %) | Escolha de projeto |
| Proteções | fusível de entrada, NTC de inrush, varistor 275 V (surtos), limitação de corrente ciclo a ciclo (Rsense), proteção de curto na saída, grampeamento RCD do MOSFET | Enunciado + Aula 07 |
| EMI | filtro de modo comum e diferencial (X2, choke de modo comum, Y) | Enunciado + Aula 08 |
| Isolação | transformador com isolação primário–secundário; realimentação por optoacoplador; distâncias de isolação na PCI ≥ 6 mm | Aula 08 / IPC-2221 |
| Temperatura | ambiente 0 a 40 °C; Tj de projeto 125 °C; dissipadores calculados para Ta = 40 °C | Mesmas hipóteses das Tarefas 1 e 2 |
| Conectores | entrada: borne/terminal para cabo CA (ou IEC C8); saída: borne de 2 vias (ou plug P4 5,5 × 2,1 mm) | Enunciado (conexão entrada/saída) |
| Construção | PCI face dupla, FR-4 1,6 mm, componentes PTH (inserção manual/onda), sem gabinete (opcional) | Enunciado Obs. 1, Aula 08 (DFM) |

## 3. Diagrama de blocos

```
Rede 90–264 VAC
   │
   ├─ Fusível ─ NTC ─ Varistor ─ Filtro EMI (X2 + choke MC + Y) ─ Ponte de diodos ─ Capacitor de bulk (≈100 µF / 400 V)
   │                                                                                       │
   │                                                     ┌──────── Snubber RCD ────────────┤
   │                                                     │                                 │
   │                                   Transformador flyback (Np : Ns : Naux) ◄── MOSFET 650 V ◄── UC3845 (modo corrente de pico, 65 kHz)
   │                                         │                 │                                ▲          ▲
   │                                         │                 └── Aux ─ Diodo ─ VCC do CI ─────┘          │ Rsense
   │                                         ▼                                                             │
   │                               Diodo Schottky ─ Capacitores de saída ─ Filtro LC ─ Saída 12 V / 3 A   │
   │                                                       │                                               │
   │                                                       └── Divisor ─ TL431 (compensador tipo 2) ─ PC817 ─┘ (isolação)
```

## 4. Checklist do enunciado (Possibilidade I) – estado

| Item do enunciado | Onde fica | Estado |
|---|---|---|
| Requisitos do projeto | `01_Especificacao/requisitos.md` | concluído |
| Aplicações do projeto | `01_Especificacao/requisitos.md` §1 | concluído |
| Levantamento das características elétricas | `02_Calculos/` | concluído |
| Simulação do conversor | `03_Simulacao/` | concluído |
| Projeto físico do transformador | `02_Calculos/transformador.py` | concluído |
| Escolha dos capacitores | `02_Calculos/entrada.py`, `flyback.py` | concluído |
| Escolha dos diodos | `02_Calculos/semicondutores.py` | concluído |
| Componentes associados ao CI | `02_Calculos/uc3845.py` | concluído |
| Escolha do driver | `02_Calculos/uc3845.py` (saída totem-pole do UC3845) | concluído |
| Escolha do transistor, perdas e dissipador | `02_Calculos/semicondutores.py` | concluído |
| Esquemático completo | `04_KiCad/` | concluído |
| Layout da PCI (potência + comando) | `04_KiCad/` | concluído |
| Lista de materiais com part number e custo (inclui PCI) | `05_BOM_Custo/` | concluído |
| Relatório (Introdução, Fundamentação, Materiais e Métodos, Resultados, Conclusão, Referências) | `06_Relatorio/` | concluído |
| Tarefa Extra (análise física de produto comercial) | `09_Tarefa_Extra/` | modelo pronto (depende de fotos) |
