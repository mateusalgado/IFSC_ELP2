# Cronograma do protótipo (Possibilidade II) – decisão de 04/11/2026, apresentação 21/12/2026

Folga total ≈ 6,5 semanas. O caminho crítico é a **chegada da PCI e dos importados** (2–4 semanas); por isso o pedido sai na primeira semana e o transformador é enrolado enquanto a placa não chega. Cada etapa tem um entregável verificável e aponta para a seção do `GUIA_MONTAGEM.md` que a descreve.

| Semana | Datas | Etapa | Entregável / critério de saída | Guia |
|---|---|---|---|---|
| 1 | 04–10/11 | **Pedir** PCI (`04_KiCad/gerbers/fonte_flyback_12V3A_B_gerbers.zip`, 5 placas, 2 camadas, 1,6 mm, 35 µm, HASL sem chumbo, fendas em Edge.Cuts) e os importados (`PEDIDO_COMPRA.md`, prioridade 1–2); confirmar com o professor a bancada isolada (isolador, variac, sonda diferencial, LCR, wattímetro) | pedidos feitos, números de rastreio; bancada confirmada por escrito | §1, §2 |
| 2 | 11–17/11 | Comprar núcleo/carretel/fio/fita e passivos nacionais; **enrolar T1** (2 unidades) e medir L<sub>p</sub>, L<sub>lk</sub>, relação e fase | dois trafos com L<sub>p</sub> = 265–325 µH, L<sub>lk</sub> < 9 µH, fase correta, registrados em `REGISTRO_MEDICOES.md` §1 | §3 |
| 3 | 18–24/11 | Recebimento; conferir PCI contra `04_KiCad/imagens/pcb_camadas.pdf` (fendas, furos, serigrafia); separar o kit por blocos | kit completo conferido; discrepâncias anotadas (substitutos da §2) | §2, §4 |
| 4 | 25/11–01/12 | **Montagem blocos 1 e 2** (entrada/retificador; controle sem potência) e ensaios de cada bloco | V<sub>bulk</sub> ≈ 175 V em 127 V; VREF 5,0 V; 65 kHz no pino 6 com D ≤ 48 %; registros §2 | §4 |
| 5 | 02–08/12 | **Blocos 3 e 4** (potência em tensão reduzida; malha fechada) e **regime permanente** em 90/127/220/264 V × 10/50/100 % | tabela 5.1 do guia preenchida com [M]; formas de onda salvas (dreno, SW, V<sub>o</sub>) | §4, §5.1 |
| 6 | 09–13/12 | Partida a frio, degraus, térmico (Q1, D1, R5/R6, T1 após 30 min), rendimento com wattímetro; **curto-circuito só se os limites da §5.4 forem atendidos**, 127 V primeiro, 2 s | tabelas 5.2–5.4 preenchidas; fotos do protótipo e das telas | §5.2–5.4, §6 |
| 7 | 14–18/12 | **Revisão C**: `medicoes.json` → relatório com coluna [M] (teoria × simulação × medição, desvios e explicações), slides com fotos e formas de onda | `RELATORIO_VISUAL.pdf` e `slides.pdf` da revisão C | — |
| — | 19–20/12 | Ensaio da apresentação (15 min), kit e protótipo embalados para a bancada | — | — |
| **21/12** | | **Apresentação** com o protótipo funcionando | | |

Regras de contingência:

- PCI não chega até 24/11: montar o bloco 2 (controle) em protoboard/placa padrão para validar o UC3845, T1 e o driver; manter a placa B para o restante.
- STF13N65M2 em falta: IPA65R400CE (TO-220FP) ou FQPF13N65 (nacional); registrar a troca no `REGISTRO_MEDICOES.md` §0 e no relatório C.
- Choke Schaffner em falta: choke 10 mH / ≥ 1 A de fonte ATX com L e R<sub>dc</sub> medidos (anotar).
- T1 fora de faixa após duas tentativas: ajustar só o entreferro (L<sub>p</sub>) — não mudar espiras; L<sub>lk</sub> > 9 µH é aceitável para o ensaio se V<sub>ds</sub> medido em 264 V ficar ≤ 520 V (caso L<sub>lk</sub> 3 % simulado: 497 V).
- Sem sonda diferencial: **não medir o primário**; validar só pelo secundário (V<sub>o</sub>, ondulação, degraus, rendimento com wattímetro) e registrar a limitação.
- Qualquer evento de fumaça/fusível: desligar, descarregar C1, seguir a tabela de diagnóstico (§6) antes de religar.
