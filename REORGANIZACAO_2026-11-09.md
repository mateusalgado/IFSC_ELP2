# Proposta de reorganização da pasta ELP2 (aguardando confirmação)

Data: 09/11/2026. Nada foi movido ou apagado ainda. Depois da confirmação eu executo, atualizo as referências nos README/slides, rodo um teste de regeneração (relatório B) e faço o commit no GitHub.

## 1. Estrutura proposta

```
ELP2/
  README.md                                  novo: índice do repositório (disciplina, tarefas, projeto)
  .gitignore
  00_Disciplina/                             material do professor (continua FORA do git)
      Aula_00_Apresentacao_Disciplina.pdf … Aula_08_Layout_PCI_DFM.pdf   (11 PDFs, nomes sem espaços/acentos)
      Plano_Ensino_EPO_II.pdf
      Instalacao_PSIM.pdf
      Enunciado_Projeto_Semestral.pdf        (hoje duplicado em PROJETO/ e PROJETO_REV_B/)
      Enunciado_Tarefa_Extra.pdf             (hoje "Tarefa extra - Análise Física Produto ….pdf", duplicado)
  Tarefa_01_Calculo_Termico_Dissipador/      (nome mantido; limpeza interna)
  Tarefa_02_Projeto_Conversor_Estatico/      (nome mantido)
  Tarefa_03_Projeto_Indutor_Alta_Frequencia/ (sem acento no nome: evita problemas em shell, URL e GitHub)
  Projeto_Flyback_RevA/                      era PROJETO/        (19/10/2026, preservada: só limpeza de caches e .raw)
  Projeto_Flyback_RevB/                      era PROJETO_REV_B/  (revisão vigente)
```

Dentro de `Projeto_Flyback_RevB/` as pastas `01_…09_` ficam como estão (a numeração já segue o enunciado). Mudanças internas:

| Onde | Mudança |
|---|---|
| `04_KiCad/` | criar `utils/` e mover para lá os auxiliares que ainda servem: `debug_router.py`, `dump_pins.py`, `pads_por_rede.py`, `netlist_resumo.py`, `erc_resumo.py`, `fp_info.py`, `comprimento_redes.py`, `testa_regras.py`, `sexp.py` (**não**: `sexp.py` é importado por `gera_sch.py`/`gera_pcb.py` → fica na raiz de 04_KiCad). `router_B3.log` → `router.log` |
| `06_Relatorio/` | `build.py` passa a gravar também `RELATORIO_MATEUS_SALGADO_PROJETO.pdf` (mesma convenção das tarefas); `RELATORIO_VISUAL.pdf` deixa de existir |
| `07_Apresentacao/` | `slides.pdf` → `APRESENTACAO_MATEUS_SALGADO_PROJETO.pdf` (fonte `slides.html` mantida) |
| `03_Simulacao/` | `PSIM_OPCIONAL.md` passa a citar `executa_b.py` (hoje cita o `roda.py` da A) |
| raiz da RevB | `REVISAO_TECNICA_V1.pdf` fica (é citado em todos os documentos); os dois enunciados vão para `00_Disciplina/` e o README aponta para lá |

## 2. Exclusões propostas

### 2a. Pesados e regeneráveis (fora do git; libera ≈ 8,7 GB no OneDrive)

| Item | Tamanho | Por quê |
|---|---|---|
| `PROJETO/03_Simulacao/runs/*.raw`, `*.op.raw`, `*.db` (revisão A) | 3,9 GB | resultados brutos da A; os `.log`, `.net` e `medidas.json` ficam, e a A continua reproduzível com `roda.py` |
| `PROJETO_REV_B/03_Simulacao/runs/*.raw` (8 casos publicados) | 4,8 GB | são **cópias**: os 44 `.raw` da B estão em `C:\Users\mateu\ELP2_sim_runs\REV_B` (11 GB, fora do OneDrive). `runs_dir.copia_raws()` recopia quando precisar; o README passa a dizer onde estão |

### 2b. Rascunhos e arquivos já consumidos (RevB, `04_KiCad/`)

| Arquivo | Por quê |
|---|---|
| `patch_cosm.py`, `patch_hide.py`, `patch_sec.py`, `patch_pcb_netlist.py` | remendos únicos já incorporados em `gera_sch.py`/`gera_pcb.py` |
| `bisect_sch.py`, `test_pcb_api.py` | depuração de travamentos do KiCad, resolvidos |
| `pcb_top.svg`, `pcb_B_top.svg`, `svg/fonte_flyback_12V3A.svg` | imagens antigas; as atuais estão em `imagens/` e o esquemático em PDF |
| `drc.json` | DRC de antes da B (o vigente é `drc_B.json`) |
| `router_B.log`, `router_B2.log` | arquivos vazios (0 kB) |
| `bom_kicad.csv` | BOM bruta do KiCad não usada (a BOM é `05_BOM_Custo/bom.py`) |
| `~fonte_flyback_12V3A.kicad_pro.lck`, `*.kicad_prl`, `__pycache__/` | bloqueio, preferências locais e cache |

### 2c. Rascunhos (RevB, outras pastas)

| Arquivo | Por quê |
|---|---|
| `03_Simulacao/batch.sh` (0 kB), `03_Simulacao/roda.py` | executor da A; a B usa `executa_b.py` |
| `03_Simulacao/modelos/` | pasta vazia |
| `06_Relatorio/assets/pcb_3d_fundo.png`, `pcb_3d_topo.png`, `pcb_completa.png`, `pcb_silk.png`, `trafo_nucleos.png` | cópias não referenciadas pelo relatório nem pelos slides (originais em `04_KiCad/` e `02_Calculos/assets/`) |
| `08_Montagem/pedido_compra.json` | subproduto de 0 kB não lido por ninguém |

### 2d. Tarefas 1–3

| Arquivo | Por quê |
|---|---|
| T1: `RELATORIO.html`, `RELATORIO_CONVERTED.html`, `relatorio_simples.html`, `gerar_pdf.py`, `gerar_pdf_simples.py`, `output/pdf/Tarefa_01_….pdf`, `tmp/pdfs/*.png` | tentativas intermediárias de gerar o PDF; o entregue é `RELATORIO_MATEUS_SALGADO_TAREFA1.pdf` e a fonte é `RELATORIO.md` + `RELATORIO_VISUAL.html` |
| T1: `Tarefa1 $9.0.2$.psimsch` **ou** `Tarefa1.psimsch` | duas versões do mesmo esquema PSIM (13 e 18 kB); proponho manter `Tarefa1.psimsch` e **perguntar** antes de apagar a outra, pois não sei qual você abriu por último |
| T2: `1 - Conversor Buck.psimsch/.sm/.smv` | idênticos byte a byte aos da Tarefa 1 (md5 igual). Proponho **manter** (cada tarefa fica autocontida); apago só se você preferir |

### 2e. Revisão A (preservada)

Além dos `.raw`/`.db`, só caches: `__pycache__/`, `*.kicad_prl`. As pastas `03_Simulacao/testes/` (3,9 MB, testes dos modelos do UC3845) e `04_KiCad/testes/` (1,3 MB, testes de símbolos) são história do desenvolvimento da A: proponho **manter** porque a A é a referência que o parecer avaliou.

## 3. O que não muda

Todos os scripts geradores e seus dados de entrada (`02_Calculos`, `gera_netlist.py`, `executa_b.py`, `gera_sch.py`, `placement.py`, `router.py`, `completa_rotas.py`, `gera_pcb.py`, `rotas.py`, `fp_info.json`, `netlist*.json`, `rotas.json`, `teste_regras/`), `.kicad_*`, Gerbers, imagens atuais, BOM, relatório (fonte, template, tabelas, assets usados), slides, guia, pedido, cronograma, registro, Tarefa Extra, `REVISAO_TECNICA_V1.pdf`.

## 4. Depois de executar

1. Atualizar referências: `Projeto_Flyback_RevB/README.md` (5 menções a `../PROJETO/` e `PROJETO_REV_B`), `Projeto_Flyback_RevA/README.md`, `slides.html` (1 menção), `PSIM_OPCIONAL.md`, `build.py`, `.gitignore` (novos caminhos), memória da sessão.
2. Teste de regeneração: `preenche_relatorio.py` + `build.py` e `preenche_guia.py` na RevB, para provar que a limpeza não quebrou a cadeia.
3. Novo `README.md` na raiz do repositório e commit "Reorganização da pasta ELP2" no GitHub (`git mv` preserva o histórico dos arquivos).

## 5. Pontos que dependem da sua resposta

- **(A)** aprovar tudo como está;
- **(B)** manter os 8 `.raw` publicados dentro de `Projeto_Flyback_RevB` (4,8 GB no OneDrive) em vez de apagar as cópias;
- **(C)** qual `Tarefa1*.psimsch` manter;
- **(D)** apagar também os PSIM duplicados da Tarefa 2.
