# Instruções de Simulação - Conversor Buck

## Arquivo: `simulacao_buck.cir`

Este netlist SPICE contém o circuito completo do conversor Buck especificado no relatório.

**Especificações:**
- Vin = 36 V
- Vout = 12 V (esperado)
- fs = 100 kHz
- L = 100 µH, C = 100 µF
- MOSFET: IRLZ44N
- Diodo: MUR860 (padrão) ou MBR20100CT (para comparação)

---

## Opção 1: Simulação no PSIM (Recomendado)

### 1. Instalação
- Baixe o PSIM em: https://www.powersimtech.com/products/psim/
- Versão gratuita disponível com licença de 30 dias ou de estudante

### 2. Importar o netlist

1. Abra o **PSIM**
2. Menu: **File → Import → SPICE Netlist**
3. Selecione `simulacao_buck.cir`
4. O PSIM converterá automaticamente para seu formato (.psimsch)

### 3. Configurar simulação

1. Menu: **Simulation → Simulation Settings**
2. **Time Settings:**
   - Start time: 0 s
   - End time: 100 µs
   - Step time: 10 ns
3. **Solver:** Odeint (ou padrão)
4. Clique **OK**

### 4. Rodar simulação

1. Clique no ícone **"Run Simulation"** (ou Ctrl+Shift+R)
2. Aguarde ~5–10 segundos
3. A janela de gráficos abrirá automaticamente

### 5. Interpretar resultados

**Gráficos principais:**

- **Tensão de saída (nó 4):** Deve estar em ~12 V com ondulação de 10 mV pico-pico
- **Corrente no indutor (nó 3 para 0):** Onda triangular entre 7,9 e 8,7 A
- **Tensão sobre o MOSFET (nó 3 para 0):** Pulso quadrado entre 0 V e 36 V

**Medições automáticas:**

O arquivo já inclui `.meas` para extrair:
- Vₒ_avg: média da tensão de saída
- Iₒ_avg: média da corrente de saída
- IL_max, IL_min: picos de corrente no indutor

Esses valores aparecem na janela de **Output** ou no log da simulação.

---

## Opção 2: Simulação no LTspice (Gratuito)

### 1. Instalação
- Baixe o LTspice em: https://www.analog.com/en/design-center/design-tools-and-calculators/ltspice-simulator.html
- Instale normalmente

### 2. Abrir o netlist

1. Abra o **LTspice**
2. Menu: **File → Open**
3. Selecione `simulacao_buck.cir`

### 3. Ajustes necessários

O arquivo está em formato SPICE padrão. Se houver erros:

- Verifique a linha `.model` — LTspice pode precisar de modelos específicos
- Para MUR860 e MBR20100CT, os modelos simplificados no arquivo devem funcionar

### 4. Rodar simulação

1. Menu: **Simulate → Run**
2. Ou clique no ícone de execução (play button)
3. Aguarde a simulação

### 5. Ver gráficos

- Clique em um nó para plotar sua tensão
- Clique em um componente para plotar sua corrente
- Use **Edit → Undo** para desfazer

---

## Comparação de Diodos

Para trocar entre **MUR860** e **MBR20100CT**:

### No PSIM:
1. Abra o arquivo `simulacao_buck.cir` em um editor de texto
2. Localize a linha:
   ```
   Dd1 0 3 MUR860_model
   ```
3. Troque para:
   ```
   Dd1 0 3 MBR20100CT_model
   ```
4. Salve e reimporte no PSIM

### No LTspice:
1. Mesma edição acima
2. Reabra o arquivo
3. Rode a simulação

**Resultado esperado:**
- MUR860: Queda de tensão ~1,2 V, perdas maiores
- MBR20100CT: Queda de tensão ~0,85 V, perdas menores

---

## Validação com o Relatório

Compare os resultados da simulação com a **Tabela 5** do relatório:

| Grandeza | Cálculo (Relatório) | Simulação (esperado) |
|---|---:|---:|
| Razão cíclica | 33,33 % | ~35 % (com queda de diodo) |
| Corrente média | 8,333 A | 8,3 A |
| Δiₗ,ₚₚ | 0,800 A | 0,75–0,85 A |
| Iₗ,ₘᵢₙ | 7,933 A | 7,9 A |
| Iₗ,ₘₐₓ | 8,733 A | 8,7 A |
| Δvₒ,ₚₚ | 10,0 mV | 9–12 mV |

Diferenças < 5% indicam consistência entre cálculo manual e simulação.

---

## Troubleshooting

**Problema:** Erro "modelo não encontrado"
- **Solução:** Os modelos estão simplificados no arquivo. Se necessário, baixe modelos precisos dos datasheets dos fabricantes (Infineon, onsemi).

**Problema:** Simulação muito lenta
- **Solução:** Aumente o `step time` de 10 ns para 100 ns ou 1 µs.

**Problema:** Gráficos não aparecem
- **Solução:** Adicione pontos de medição manualmente clicando nos nós/componentes.

---

## Próximos Passos

1. **Extraia os dados** de Vₒ, Iₓ, Iₐ da simulação
2. **Compare com a Tabela 5** — pequenas diferenças são normais
3. **Documente os resultados** no Apêndice A do relatório
4. **Validação térmica:** Use as correntes RMS (Iq_rms, Id_rms) para recalcular dissipadores se necessário

---

## Contato / Dúvidas

Consulte o Apêndice A do relatório para mais detalhes sobre interpretação dos resultados.
