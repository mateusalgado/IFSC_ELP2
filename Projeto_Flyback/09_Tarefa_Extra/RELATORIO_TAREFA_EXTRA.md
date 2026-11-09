# Tarefa Extra – Análise física de um produto comercial (modelo a preencher)

**Disciplina:** Eletrônica de Potência II (2026-2) · **Aluno:** Mateus Salgado Barboza Costa · **Professor:** Joabel Moia

> Obrigatória apenas na Possibilidade I (sem protótipo). Escolha um produto com conversor chaveado (carregador de celular/notebook, fonte de roteador, fonte de LED, reator eletrônico, fonte ATX) e **fotografe**: etiqueta, placa pelo lado dos componentes, lado das trilhas, transformador, dissipadores, conectores. As fotos vão em `fotos/` e são referenciadas abaixo. Os 13 itens seguem o enunciado da Tarefa Extra; cada item traz o que observar e como relacionar com as aulas.

## 1. Identificação do produto
Fabricante, modelo, uso, dados da etiqueta (Vin, Vout, Iout, potência, classe de isolação, normas/certificações: INMETRO, CE, UL). Foto da etiqueta.

## 2. Topologia do conversor
Pela inspeção: ponte + bulk + flyback (um transformador pequeno, um MOSFET ou CI integrado com chave, um diodo/Schottky no secundário) ou forward, buck, PFC + LLC (dois magnéticos, dois capacitores grandes). Desenhar o diagrama de blocos como no `01_Especificacao/requisitos.md`.

## 3. Circuito integrado de controle
Código do CI (ex.: TNY, LNK, VIPer, OB2263, UC3845, NCP1200). Procurar o datasheet; frequência de comutação, modo de controle (corrente de pico, PFM, quasi-ressonante), proteções internas. Relacionar com a Aula 05 e 07.

## 4. Transistor de potência
Encapsulamento (TO-220, TO-252, integrado no CI), tensão e corrente nominais; estimar as perdas como na Aula 02 e comparar com o dissipador existente (ou a ausência dele).

## 5. Diodos
Ponte (ou 4 diodos 1N4007), diodo de saída (Schottky SB/SR/MBR…), diodo do snubber (FR107/UF4007), diodo do auxiliar. Tensões e correntes de catálogo versus as do produto.

## 6. Transformador / indutores
Núcleo (EE, EF, RM, ER) e tamanho estimado com régua; número de pinos; presença de fita, fio triplo-isolado, blindagem; estimar Np/Ns pela relação de tensões (Aula 04C). Choke de modo comum e indutor do pós-filtro.

## 7. Capacitores
Bulk (µF/V, marca, temperatura), capacitores de saída (low-ESR?), X2 e Y1, cerâmicos de desacoplamento. Comparar com os critérios da Aula 03 (capacitância, tensão, corrente eficaz, temperatura, RSE, custo).

## 8. Proteções
Fusível (valor), NTC, varistor, TVS/snubber RCD, proteção de sobrecorrente/sobretensão na saída (pela análise do circuito ou do CI). Relacionar com a Aula 07.

## 9. Filtro de EMI
Presença de X2, choke de modo comum, Y1, resistor de descarga; o que falta para a classe do produto.

## 10. Realimentação e isolação
Optoacoplador + TL431 (ou regulação pelo auxiliar – primary-side regulation); distâncias de isolação na placa (fenda, ≥ 6 mm?), classe de isolação do opto e do transformador (Aula 08).

## 11. Layout da PCI (Aula 08)
Face simples ou dupla; fluxo entrada → saída; laços de alta frequência curtos; terra de sinal e de potência; trilhas a 45° ou 90°; dissipação por área de cobre; DFM (solda por onda, espaçamentos, serigrafia). Fotos das duas faces com anotações.

## 12. Dissipação térmica
Dissipadores, cobre da placa, ventilação do gabinete; estimar a temperatura (Aula 02) e comparar com o encapsulamento.

## 13. Custo e comparação com o projeto desenvolvido
Estimar a BOM do produto comercial (part numbers visíveis) e comparar com `05_BOM_Custo/custo.md` (rev. B: US$ 42,73 por fonte em 1 unidade; US$ 22,91 em 100 unidades): o que o produto comercial simplifica (CI com chave integrada, face simples, menos proteções) e o que o projeto do semestre faz melhor (snubber, EMI, isolação, pontos de teste).

## Referências
Aulas 02, 03, 04C, 05, 07 e 08 da disciplina; datasheets dos componentes identificados; `06_Relatorio/RELATORIO.md`.
