"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
# Projeto Semestral EPO II 2026-2 – Fonte flyback 12 V / 3 A, entrada universal, UC3845 (Tema II) — **Revisão B**
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py

"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
Aluno: Mateus Salgado Barboza Costa · Prof. Joabel Moia · IFSC · Entrega/apresentação: **21/12/2026**
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py

"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
Revisão B (novembro/2026) em resposta ao parecer técnico `REVISAO_TECNICA_V1.pdf` sobre a revisão A (19/10/2026; pasta completa da A em `revisoes/RevA_2026-10-19/`, sem os `.raw`). Enunciados em `../00_Disciplina/`. Cada número publicado nesta pasta tem origem marcada: **[C]** cálculo (`02_Calculos`), **[S]** simulação LTspice B (`03_Simulacao/runs`), **[CAD]** verificação ERC/DRC (`04_KiCad`), **[M]** medição física — **não há medições físicas: o protótipo não foi montado.**
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py

"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
## Entregáveis principais
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py

"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| O quê | Onde | Origem |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
|---|---|---|
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| **Relatório B** (6 seções do plano de ensino; 28 p., didático: 12 memórias de cálculo, 21 tabelas, 20 figuras, etiquetas de origem) | `06_Relatorio/RELATORIO_MATEUS_SALGADO_PROJETO.pdf` e `RELATORIO_VISUAL.html` (autossuficiente, abre em qualquer lugar); fonte `RELATORIO.template.md` → `preenche_relatorio.py` → `RELATORIO.md` + `tabelas/` → `build.py`; diagrama `diagrama_blocos.py` | C/S/CAD |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| **Apresentação B** (16 slides) | `07_Apresentacao/APRESENTACAO_MATEUS_SALGADO_PROJETO.pdf` (`slides.html`) | C/S/CAD |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Especificação e aplicações | `01_Especificacao/requisitos.md` (nota da revisão B) | — |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Cálculos teóricos (scripts + resultados + figuras) | `02_Calculos/*.py`, `resultados/RESULTADOS_TEORIA.md`, `resultados/*.json`, `assets/*.png` | C |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Simulação LTspice B (23 casos, janelas, figuras) | `03_Simulacao/` (`gera_netlist.py`, `executa_b.py`, `runs_dir.py`, `analisa_curto.py`, `analisa_transitorios.py`, `hiccup_tempos.py`, `plota.py`, `plota_curto.py`, `runs/medidas.json`, `runs/*.log/.net`, `analise/*.png`) | S |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Esquemático KiCad 10 (ERC 0 erros / 0 avisos) | `04_KiCad/fonte_flyback_12V3A.kicad_sch`, `fonte_flyback_12V3A_esquematico.pdf` | CAD |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Layout B (DRC 0 erros, 0 não conectados, paridade OK, cobertura das regras) | `04_KiCad/fonte_flyback_12V3A.kicad_pcb`, `drc_B.json`, `teste_regras/`, `gerbers/`, `imagens/`, `3d/`, `VERIFICACAO_LAYOUT.md`, `ANALISE_PLACEMENT.md` (placement como produto; melhorias para a revisão C); utilitários em `04_KiCad/utils/` | CAD |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| BOM B com part numbers e custo (1 e 100 un., PCI incluída) | `05_BOM_Custo/BOM.xlsx`, `custo.xlsx`, `custo.md` (`bom.py`) | — |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Guia de montagem e ensaio B (ficha de T1, instrumentação, critérios de aceite) | `08_Montagem/GUIA_MONTAGEM.md` (`preenche_guia.py`) | C/S |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Tarefa Extra (modelo com os 13 itens; depende de fotos) | `09_Tarefa_Extra/RELATORIO_TAREFA_EXTRA.md` | — |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Parecer da revisão A | `REVISAO_TECNICA_V1.pdf` | — |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py

"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
## Resultados em uma linha
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py

"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
12 V / 3 A, 90–264 VAC, 65 kHz, MCD; **STF13N65M2 (TO-220FP isolado)** + STPS20H100CT; trafo E-30/7 42:7:9, L<sub>p</sub> 294 µH; C1 150 µF; V<sub>o</sub> [S] 12,06 V em toda a faixa, ondulação ≤ 4,2 mV (excursão total ≤ 9,2 mV), V<sub>ds</sub> máx 482 V (74 % de 650 V), η 82,8–85,3 % (85,3 % em 220 V), MF 88° [C]; partida a frio e degraus nos dois sentidos estáveis; **curto-circuito com desligamento por UVLO e hiccup** (155 ms até o UVLO, 13 % de ciclo de falha em 220 V) [S]; placa 140 × 90 mm 2 camadas com classes atribuídas, isolação 6,4 mm e DRC verificável, placement revisto em 05/11 antes do pedido (entrada em linha, porta-fusível, laços JP1/JP2 para sonda de corrente, Q1 afastado de C1) [CAD]; custo US$ 42,73 (1 un.) / 22,37 (100 un.).
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py

"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
## O que mudou da A para a B (parecer técnico)
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py

"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Item | B |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
|---|---|
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Curto-circuito (9 A / 596 V, sem desligamento) | R13 = 100 Ω no auxiliar → VCC cai, UVLO desliga, hiccup; janelas aplicação / sustentado / recuperação; transitório de aplicação documentado (7,8 A, 555 V no modelo linear; núcleo real satura ≈ 3 A) |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Grampo RCD em série na placa | R5 ∥ R6 = 9 kΩ no esquemático, na placa e no modelo |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Filtro do ISENSE | 330 Ω / 100 pF no pino 3 (τ = 33 ns) |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Choke 0,7 A | Schaffner RN214 2 × 10 mH / 1,2 A, pinagem 1-2 / 3-4 |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Barramento | C1 = 150 µF (vale 104 V; 99,8 V com −20 %) |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Classes de rede / DRC | HV, SEC, SEC_PWR atribuídas; `utils/testa_regras.py` prova que cada regra dispara |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| T1 / TL431 / guia | pinagem única (1-BULK, 3-DRAIN, 4-PGND, 5-AUX, 6/7-SGND, 9/10-ânodos de D1), TL431 K-A-REF, instrumentação com isolador + sonda diferencial e terra de proteção mantido, curto físico bloqueado até os limites |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Estabilidade | planta com pós-filtro L2–C13 e polo do opto; R<sub>z</sub> 21,5 kΩ / C<sub>z</sub> 270 nF |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Placa para teste e produto | MOSFET isolado (clip sem potencial), furos M3 ≥ 6 mm da rede, conectores em bordas opostas, D1 longe dos eletrolíticos, dissipadores necessários em Q1 e D1 (térmico em `VERIFICACAO_LAYOUT.md`); **05/11:** J1 abrindo para a borda esquerda, filtro de entrada em coluna, porta-fusível 5 × 20, JP1/JP2 para sonda de corrente, Q1 a 15,7 mm de T1 e 6 mm de C1, eletrolíticos de saída com passo 12 mm, serigrafia de segurança (F1, L/N, +12 V/0 V, C1 400 V), regra de 6,4 mm (`ANALISE_PLACEMENT.md`) |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py

"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
## Checklist do enunciado
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py

"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Item | Estado | Onde |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
|---|---|---|
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Requisitos do projeto | ✔ | relatório §4.1 (tabela de requisitos e verificação), `01_Especificacao` |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Aplicações | ✔ | relatório §1 |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Levantamento das características elétricas | ✔ | §4.2–4.3 (memórias de cálculo 1–3), `02_Calculos` |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Simulação do conversor | ✔ (B, 23 casos) | §4.11, `03_Simulacao` |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Esquemático | ✔ | §4.12, `04_KiCad` |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Projeto físico do transformador | ✔ | §4.4 (memória de cálculo 4), `transformador.py`, guia §3 |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Escolha dos capacitores | ✔ | §4.2 e §4.5, `saida.py`, `entrada.py` |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Escolha dos diodos | ✔ | §4.7 (memória de cálculo 8) |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Componentes associados ao CI | ✔ | §4.8–4.9, `uc3845.py`, `compensador.py` |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Escolha do driver | ✔ | §4.8 (saída totem-pole do UC3845) |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Transistor: perdas e dissipador | ✔ | §4.7 (memória de cálculo 7), `semicondutores.py` |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Lista de materiais com part number e custo (com PCI) | ✔ | §4.13, `05_BOM_Custo` |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Layout da PCI (potência + comando) | ✔ | §4.14 (tabela de regras e verificação), `04_KiCad` |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Relatório nas 6 seções | ✔ | `06_Relatorio` |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Apresentação | ✔ | `07_Apresentacao` |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| Tarefa Extra | ☐ opcional (Possibilidade II escolhida); modelo pronto em `09_Tarefa_Extra` |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
| **Protótipo (Possibilidade II)** | **em andamento** — decisão de 04/11/2026; pedido `08_Montagem/PEDIDO_COMPRA.md`, cronograma `CRONOGRAMA.md`, registro `REGISTRO_MEDICOES.md`, Gerbers `04_KiCad/gerbers/fonte_flyback_12V3A_B_gerbers.zip` (placement de 05/11/2026) |
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py

"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
## Limitações conhecidas (B)
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py

"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
- Partida a frio em 90 VAC leva 7,4 s até o UVLO com I<sub>start</sub> máximo (1,1 s em 264 V) [S]; para produto, 2 × 68 kΩ ou partida ativa.
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
- O modelo do transformador é linear: o transitório de aplicação do curto (7,8 A) é um limite superior; o núcleo real satura em ≈ 3 A. Medir L<sub>lk</sub> e saturação no trafo real.
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
- Em carga leve a simulação fica 11–22 % abaixo da teoria em V<sub>ds</sub> e I<sub>s,pk</sub> (hipóteses conservadoras do cálculo); listado na tabela 10 do relatório.
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
- A BOM é orçamento de engenharia (preços da A + provisões), não cotação de compra.
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
- Nenhum ensaio de emissões conduzidas; filtro de EMI dimensionado por curva ideal.
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
- Trilhas longas de controle permanecem (/COMP 109 mm, /CS 56 mm, gate 80 mm): mover o bloco do UC3845 para junto de Q1 e deitar D1 ficam para a revisão C, decididos pelas medições em TP7/TP8 e pelas temperaturas (`04_KiCad/ANALISE_PLACEMENT.md` §6–7).
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py

"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
## Decisão tomada: montar o protótipo (Possibilidade II, 04/11/2026)
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py

"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
1. **Semana 1 (até 10/11):** pedir a PCI (zip dos Gerbers, 5 placas) e os importados conforme `08_Montagem/PEDIDO_COMPRA.md` (≈ US$ 109 com sobressalentes e lote de 5 placas, sem frete); confirmar a bancada isolada com o professor.
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
2. Seguir `08_Montagem/CRONOGRAMA.md` (7 semanas até 21/12) e anotar tudo em `08_Montagem/REGISTRO_MEDICOES.md` → `medicoes.json` (modelo `medicoes.template.json`).
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
3. A **revisão C** (semana 7) acrescenta a coluna [M] ao relatório e as fotos/formas de onda aos slides; até lá nenhum número publicado é medição.
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
4. Tarefa Extra passa a ser opcional.
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py

"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
## Como regenerar tudo (revisão B)
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py

"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
```bash
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
# teoria (WSL)
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
wsl -d Ubuntu -- bash -c 'cd /mnt/c/.../Projeto_Flyback/02_Calculos && python3 run_all.py'
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
# simulação: gera netlists e roda o LTspice em lote (Windows, python do KiCad; .raw fora do OneDrive, ver runs_dir.py)
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
"C:\Program Files\KiCad\10.0\bin\python.exe" 03_Simulacao\executa_b.py
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
# releitura dos .raw e figuras (WSL; não rodar junto com o LTspice)
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
wsl -d Ubuntu -- bash -c 'cd /mnt/c/.../Projeto_Flyback/03_Simulacao && python3 analisa_curto.py <raw> 60 380 && python3 hiccup_tempos.py <raw> 60 380 && python3 plota_curto.py <raw> 60 380 && python3 analisa_transitorios.py && python3 plota.py regime_90V_100pct regime_264V_100pct partida_90V degrau_90V sem_snubber_264V'
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
# KiCad: esquemático → ERC/netlist → placement → roteador → placa → DRC → cobertura das regras → exportações
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
wsl -d Ubuntu -- bash -c 'cd /mnt/c/.../Projeto_Flyback/04_KiCad && python3 gera_sch.py && python3 utils/fp_info.py && python3 placement.py && python3 router.py && python3 completa_rotas.py'
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
"C:\Program Files\KiCad\10.0\bin\python.exe" 04_KiCad\gera_pcb.py
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" pcb drc --severity-all --schematic-parity --refill-zones --format json -o 04_KiCad\drc_B.json 04_KiCad\fonte_flyback_12V3A.kicad_pcb
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
"C:\Program Files\KiCad\10.0\bin\python.exe" 04_KiCad\utils\testa_regras.py
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
"C:\Program Files\KiCad\10.0\bin\python.exe" 04_KiCad\utils\comprimento_redes.py > 04_KiCad\comprimento_redes.txt
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
# BOM, tabelas, relatório, guia e slides
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
wsl -d Ubuntu -- bash -c 'cd /mnt/c/.../Projeto_Flyback/05_BOM_Custo && python3 bom.py'
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
"C:\Program Files\KiCad\10.0\bin\python.exe" 06_Relatorio\diagrama_blocos.py
"C:\Program Files\KiCad\10.0\bin\python.exe" 06_Relatorio\gera_tabelas.py
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
"C:\Program Files\KiCad\10.0\bin\python.exe" 06_Relatorio\preenche_relatorio.py
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
"C:\Program Files\KiCad\10.0\bin\python.exe" 06_Relatorio\build.py
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
"C:\Program Files\KiCad\10.0\bin\python.exe" 08_Montagem\preenche_guia.py
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
```
"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py

"C:Program FilesKiCad10.0binpython.exe" 06_Relatoriodiagrama_blocos.py
Ferramentas: Python 3 (numpy, matplotlib) no WSL Ubuntu e python do KiCad (numpy) no Windows; LTspice 26; KiCad 10 (kicad-cli, pcbnew); pandoc; Chrome headless (PDF); LibreOffice (xlsx). Os `.raw` de 0,1–1,8 GB (44 casos, 11 GB) ficam **só** em `C:\Users\mateu\ELP2_sim_runs\REV_B`, fora do OneDrive e do git; `03_Simulacao/runs/` guarda `.log`, `.net`, `medidas.json` e as janelas; `runs_dir.copia_raws()` copia um caso para `runs/` quando for preciso reler.
