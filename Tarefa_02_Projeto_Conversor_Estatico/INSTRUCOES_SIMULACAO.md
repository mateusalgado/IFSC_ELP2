# Instruções de Simulação no Power Stage Designer 5 (PSD5) — Tarefa 02

Troca de ferramenta: em vez do PSIM, vamos usar o **Power Stage Designer 5 (PSD5)**, da Texas Instruments — a mesma ferramenta usada na Tarefa 01 (RELATORIO.md, Seção 5.1). Ele é um formulário/planilha (não um esquemático), o que evita todos os problemas de fiação que tivemos com o PSIM.

Download: [ti.com/tool/POWERSTAGE-DESIGNER](https://www.ti.com/tool/POWERSTAGE-DESIGNER) — gratuito, precisa de Java.

Fonte da estrutura abaixo: *Power Stage Designer User's Guide* (TI, SLVUBB4B).

## 1. Abrir a topologia Buck

1. Abra o PSD5, menu **Topology → Buck** (não-síncrono — o nosso circuito tem diodo de roda livre, não um segundo MOSFET).
2. Preencha o formulário principal:

| Campo | Valor |
|---|---:|
| Vin | 36 V |
| Vout | 12 V |
| Iout (ou Pout, se o campo for potência) | 8,333 A (ou 100 W) |
| Frequência de comutação | 50 kHz |
| Indutância L | 100 µH *(o PSD5 sugere um L "recomendado" pela ondulação-alvo — ignore a sugestão e force 100 µH, que é o dado da tarefa)* |
| Capacitância de saída Cout | 1000 µF |
| ESR do capacitor | 70 mΩ |
| Vf do diodo (se pedir aqui) | 0,55 V |

3. O PSD5 recalcula duty cycle, formas de onda e esforços automaticamente. Confira que D ≈ 0,333 e que bate com a Seção 4 do relatório.

## 2. Registrar os esforços por componente

Clique em cada componente destacado no esquema (indutor, chave/MOSFET, diodo, capacitor) — abre uma janela com **pico, mínimo, RMS, médio e AC** daquele componente. Anote os valores de:

| Componente | O que anotar |
|---|---|
| Indutor | IL médio, IL mín, IL máx (ΔiL = máx−mín) |
| Chave (MOSFET) | IT,rms, IT médio |
| Diodo | ID,rms, ID médio |
| Capacitor | IC,rms |
| Saída (vo) | Vo médio, Vo ripple pico a pico |

Esses são os mesmos 9 valores que a Seção 11 do relatório precisa — anote-os já nesse formato:

```
Vo_medio = 
Vo_ripple_pp = 
IL_medio = 
diL_pp = 
IT_rms = 
ID_rms = 
IC_rms = 
```

## 3. Calculadora de perdas do FET (FET Losses Calculator)

Menu **Tools → FET Losses Calculator** (janela separada da topologia). Ela usa o modelo de perdas por carga de gate (mais preciso que o cálculo simplificado da Seção 7 — foi exatamente essa diferença que a Tarefa 01 observou entre o cálculo manual e o PSD5).

Preencha com os dados de datasheet do **IPP039N10N5** (Infineon, Rev. 2.0):

| Campo | Valor | Origem |
|---|---:|---|
| VDS | 36 V | Vin (tensão de bloqueio) |
| RDS(on) | 0,0039 Ω | datasheet, 25°C — **não** aplique o fator kT=1,7 aqui; deixe o PSD5 gerar um número independente pra comparar com a Seção 7, igual a Tarefa 01 fez |
| VGS (drive) | 10 V | acionamento padrão de gate assumido no relatório |
| Qgs | 24 nC | datasheet |
| Qgd | 15 nC (típico) | datasheet — se quiser o caso mais conservador, use 23 nC (máx) |
| Vmiller (plateau) | 4,5 V | datasheet |
| Coss | 830 pF (típico) | datasheet, @VDS=50V |
| Rg,total | 5 Ω *(assumido)* | não especificado na tarefa — é o resistor de gate + resistência do driver; qualquer valor razoável (2–10Ω) serve pra essa validação |
| fswitch | 50000 Hz | especificação |
| IFET,min | 7,533 A | = IL,min |
| IFET,max | 9,133 A | = IL,max |
| Qg,th (carga até o limiar) | *deixe em branco ou estime ~10 nC* | não consta no datasheet extraído; se o campo for obrigatório, use metade de Qgs como aproximação |
| tdead / VSD (diodo de corpo) | 0 / não se aplica | só relevante pra retificador síncrono — nosso freewheeling é o diodo externo D, não o corpo do MOSFET |

Depois de preencher, anote:

```
P_transistor = (Pcond + Pswitching + PCoss, valor total mostrado)
```

Se a calculadora também separar os termos (Pcond, Pswitching, PCoss, Pdriver), anote os 4 separados — é ainda melhor para comparar com a tabela da Seção 7.

## 4. Perda do diodo

Se a janela da topologia já mostrar a perda do diodo diretamente (alguns modelos do PSD5 reportam), anote como `P_diodo`. Se não mostrar, calcule manualmente com os valores de corrente que você já anotou no Passo 2:

$$
P_{diodo} \approx V_0 \cdot I_{D,med} + R_d \cdot I_{D,rms}^2
$$

com V₀=0,55V e Rd=4,5mΩ (valores já usados na Seção 8.2 do relatório, referentes ao STPS20H100C com ânodos em paralelo).

## 5. O que me mandar de volta

```
Vo_medio = 
Vo_ripple_pp = 
IL_medio = 
diL_pp = 
IT_rms = 
ID_rms = 
IC_rms = 
P_transistor = 
P_diodo = 
```

Se o PSD5 tiver separado as parcelas de perda do transistor (condução/comutação/Coss/driver), me manda também esses 4 valores — dá pra fazer uma comparação mais rica na Seção 11, no mesmo espírito da Tabela da Seção 9.2 da Tarefa 01 (cálculo teórico × simulação).

Screenshots das janelas de forma de onda (se puder tirar 1-2) ajudam bastante como figura complementar.

## 6. O que eu faço com isso

1. Preencho a tabela de comparação teórico × PSD5 da Seção 11, com Δ% de cada grandeza;
2. Se P_transistor vier bem menor que os 0,414 W calculados (efeito esperado, como na Tarefa 01 — o modelo de carga de gate costuma reduzir a perda de comutação estimada), atualizo a Seção 10 (térmico) com o valor simulado, deixando claro que ainda **não precisa de dissipador** (a folga só aumenta);
3. Escrevo a interpretação dos resultados;
4. Gero o `RELATORIO_VISUAL.html` e o PDF final, no mesmo padrão da Tarefa 01.
