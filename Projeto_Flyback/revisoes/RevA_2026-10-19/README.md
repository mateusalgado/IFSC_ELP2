# Projeto Semestral EPO II 2026-2 – Fonte flyback 12 V / 3 A, entrada universal, UC3845 (Tema II)

Aluno: Mateus Salgado Barboza Costa · Prof. Joabel Moia · IFSC · Entrega/apresentação: **21/12/2026**

## Entregáveis principais

| O quê | Onde |
|---|---|
| **Relatório** (6 seções do plano de ensino, 20 páginas) | `06_Relatorio/RELATORIO_VISUAL.pdf` (fonte: `RELATORIO.md`, tabelas em `tabelas/`, `build.py`) |
| **Apresentação** (14 slides) | `07_Apresentacao/slides.pdf` (`slides.html`) |
| Especificação e aplicações | `01_Especificacao/requisitos.md` |
| Cálculos teóricos (scripts + resultados + figuras) | `02_Calculos/*.py`, `resultados/RESULTADOS_TEORIA.md`, `resultados/*.json`, `assets/*.png` |
| Simulação LTspice (20 casos, medidas, 60 figuras) | `03_Simulacao/` (`gera_netlist.py`, `roda.py`, `plota.py`, `runs/medidas.json`, `analise/*.png`, `PSIM_OPCIONAL.md`) |
| Esquemático KiCad 10 (ERC 0) | `04_KiCad/fonte_flyback_12V3A.kicad_sch`, `fonte_flyback_12V3A_esquematico.pdf` |
| Layout (DRC 0 erros, 0 não conectados, paridade OK) | `04_KiCad/fonte_flyback_12V3A.kicad_pcb`, `gerbers/`, `imagens/`, `3d/`, `VERIFICACAO_LAYOUT.md` |
| BOM com part numbers e custo (1 e 100 un., PCI incluída) | `05_BOM_Custo/BOM.xlsx`, `custo.xlsx`, `custo.md` (`bom.py`) |
| Guia de montagem e ensaio (decisão montar / não montar) | `08_Montagem/GUIA_MONTAGEM.md` |
| Tarefa Extra (modelo com os 13 itens; depende de fotos) | `09_Tarefa_Extra/RELATORIO_TAREFA_EXTRA.md` |

## Resultados em uma linha

12 V / 3 A, 90–264 VAC, 65 kHz, MCD; STP13N65M2 + STPS20H100CT; trafo E-30/7 42:7:9, Lp 294 µH; Vo sim. 12,07–12,08 V, ondulação < 4 mV, Vds máx 482 V (74 %), η 83–85,5 %, MF 99°; placa 140 × 90 mm 2 camadas; custo US$ 39,78 (1 un.) / 20,63 (100 un.).

## Checklist do enunciado (Possibilidade I)

| Item | Estado | Onde |
|---|---|---|
| Requisitos do projeto | ✔ | relatório §4.1, `01_Especificacao` |
| Aplicações | ✔ | relatório §1 |
| Levantamento das características elétricas | ✔ | §4.1–4.2, `02_Calculos` |
| Simulação do conversor | ✔ | §4.6, `03_Simulacao` |
| Esquemático | ✔ | §4.7, `04_KiCad` |
| Projeto físico do transformador | ✔ | §4.2, `transformador.py` |
| Escolha dos capacitores | ✔ | §4.3, `saida.py`, `entrada.py` |
| Escolha dos diodos | ✔ | §4.4 |
| Componentes associados ao CI | ✔ | §4.5, `uc3845.py`, `compensador.py` |
| Escolha do driver | ✔ | §4.5 (saída totem-pole do UC3845) |
| Transistor: perdas e dissipador | ✔ | §4.4, `semicondutores.py` |
| Lista de materiais com part number e custo (com PCI) | ✔ | §4.8, `05_BOM_Custo` |
| Layout da PCI (potência + comando) | ✔ | §4.9, `04_KiCad` |
| Relatório nas 6 seções | ✔ | `06_Relatorio` |
| Apresentação | ✔ | `07_Apresentacao` |
| Tarefa Extra | ☐ modelo pronto; **faltam as fotos do produto comercial** (obrigatória só na Possibilidade I) |
| Protótipo (Possibilidade II) | ☐ opcional; guia e critérios em `08_Montagem` |

## Decisão pendente do aluno

1. **Montar ou não o protótipo** (ver `08_Montagem/GUIA_MONTAGEM.md` §1: custo ≈ R$ 220, prazo 3–4 semanas, precisa de isolador/variac e sonda diferencial).
2. Se não montar: fotografar um produto comercial e preencher `09_Tarefa_Extra/RELATORIO_TAREFA_EXTRA.md`.
3. Conferir os preços da BOM no distribuidor antes de comprar (referências de out/2026) e a disponibilidade do STP13N65M2 (substitutos listados).

## Como regenerar tudo

```bash
# teoria (WSL)
wsl -d Ubuntu -- bash -c 'cd /mnt/c/.../PROJETO/02_Calculos && python3 run_all.py'
# simulação (gera netlists, roda LTspice em lote, plota)
wsl -d Ubuntu -- bash -c 'cd /mnt/c/.../PROJETO/03_Simulacao && python3 gera_netlist.py && python3 roda.py && python3 plota.py'
# KiCad: esquemático → ERC/netlist → placement → roteador → placa → DRC → exportações
wsl -d Ubuntu -- bash -c 'cd /mnt/c/.../PROJETO/04_KiCad && python3 gera_sch.py && python3 placement.py && python3 router.py'
"C:\Program Files\KiCad\10.0\bin\python.exe" 04_KiCad\gera_pcb.py
"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" pcb drc --severity-all --schematic-parity --refill-zones --save-board 04_KiCad\fonte_flyback_12V3A.kicad_pcb
# BOM, tabelas e relatório
wsl -d Ubuntu -- bash -c 'cd /mnt/c/.../PROJETO/05_BOM_Custo && python3 bom.py; cd ../06_Relatorio && python3 gera_tabelas.py'
"C:\Program Files\KiCad\10.0\bin\python.exe" 06_Relatorio\build.py
```

Ferramentas: Python 3 (numpy, matplotlib) no WSL Ubuntu; LTspice XVII; KiCad 10 (kicad-cli, pcbnew); pandoc; Chrome headless (PDF); LibreOffice (xlsx).
