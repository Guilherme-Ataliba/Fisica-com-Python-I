# Parte 3 — Paramagneto estocástico: teoria e leitura dos gráficos

Números marcados **[medido]** vêm da reprodução exata das células (`SEED = 42`), em `04-numeros.md`.

## 1. O modelo

`N` spins `sᵢ = ±1`, magnetização `M = Σsᵢ`, e `m = M/N`. A cada passo:

1. sorteia-se uma partícula (probabilidade `1/N` cada);
2. o spin dela **troca de sinal** (`↑→↓` ou `↓→↑`).

Como `N↑ = (N+M)/2` e `N↓ = (N−M)/2`:

```
P(M → M−2) = N↑/N = (N+M)/2N = (1+m)/2
P(M → M+2) = N↓/N = (N−M)/2N = (1−m)/2
```

**O passo é ±2, não ±1.** Isso tem uma consequência que você vai precisar na §5.3: a paridade de
`M` é **invariante** — `M ≡ N (mod 2)` sempre, para qualquer `t`. Um sistema com `N = 500` só
visita magnetizações pares.

## 2. A Eq. (11): a demonstração pedida

**(a) Valor médio no passo seguinte.** Partindo da Eq. (8):

```
⟨M_{t+1}⟩ = (M+2)·(N−M)/2N + (M−2)·(N+M)/2N
```

Expandindo os dois numeradores:

```
(M+2)(N−M) = MN − M² + 2N − 2M
(M−2)(N+M) = MN + M² − 2N − 2M
soma       = 2MN − 4M
```

Logo

```
⟨M_{t+1}⟩ = (2MN − 4M)/2N = M·(1 − 2/N)
```

**(b) O mesmo resultado pelo desvio.** Dividindo por `N` e escrevendo `m = M/N`:

```
⟨Δm⟩ = (+2/N)·(1−m)/2 + (−2/N)·(1+m)/2 = (1−m)/N − (1+m)/N = −2m/N
```

que é `⟨m_{t+1}⟩ − m_t`, o mesmo resultado. **Esta versão é a que vale usar no relatório**: é
curta, não tem álgebra para errar, e a leitura física é imediata — o desvio médio é proporcional ao
desvio atual, com sinal contrário, e se anula quando `m = 0`. É por isso que `m = 0` é o ponto fixo:
todo estado perto dele é empurrado de volta.

**(c) Recorrência e solução.** `⟨m_{t+1}⟩ = (1−2/N)⟨m_t⟩` e a esperança é linear, então

```
⟨m_t⟩ = m₀·(1 − 2/N)^t
```

**(d) Interpretação física.** `(1−2/N)^t = e^{−t/τ}` com `τ = N/2`: sem campo externo, a
magnetização média decai exponencialmente para zero, com tempo característico que **cresce
linearmente com `N`**. O estado final não tem ordem magnética — é o paramagneto. Note que a
"memória" da condição inicial persiste por `~N/2` passos: cada partícula precisa ser sorteada uma
vez para "esquecer" o `m₀`.

## 3. A variância: a segunda exponencial

Condicionando em `m` e usando `⟨Δm⟩ = −2m/N`, `⟨(Δm)²⟩ = 4/N²`:

```
⟨m²_{t+1}⟩ = m² + 2m⟨Δm⟩ + ⟨(Δm)²⟩ = m²(1 − 4/N) + 4/N²
```

O ponto fixo é `(4/N²)/(4/N) = 1/N`, logo

```
⟨m_t²⟩ = 1/N + (m₀² − 1/N)·(1 − 4/N)^t
Var(m_t) = 1/N + (m₀² − 1/N)(1−4/N)^t − m₀²(1−2/N)^{2t}
```

Duas taxas de novo (`4/N` e `2/N`), e o resultado central:

```
Var(m) → 1/N       σ_m → 1/√N
```

**Por que `1/N`:** no equilíbrio os spins são independentes e equiprováveis, então `M` é soma de
`N` variáveis `±1` independentes, `Var(M) = N`, e `Var(m) = N/N² = 1/N`. É a **lei dos grandes
números** agindo: a flutuação relativa `σ_m/|m|` some, mas a flutuação absoluta é `1/√N`.

## 4. A mesma cadeia da Parte 1

Com `m_s = 2·m_A/N − 1` na urna (Parte 1):

```
P(m_A → m_A−1) = m_A/N = (1+m_s)/2
```

que é **exatamente** a regra do paramagneto. Ou seja, as duas partes simulam a mesma cadeia de
Markov em variáveis diferentes (`M = 2m_A − N`), e é por isso que `λ₁ = 1−2/N` e `λ₂ = 1−4/N`
aparecem nas duas. As constantes de equilíbrio mudam só pela mudança de unidade:

```
Var(m_A) = N/4   →   Var(M) = 4·(N/4) = N   →   Var(M/N) = 1/N
```

Vale uma frase no relatório: *o paramagneto é o gás de Ehrenfest reescrito em spins; a física é a
mesma, o que muda é a escala.*

## 5. Figura a figura

### 5.1 `part3-momentos` — relaxação para `m=0` e flutuação

`N = 500`, `2000` réplicas, `t` até `2000 = 8τ`, `m₀ = 1; 0,5; −0,5; −1`. Linha cheia =
simulação (média entre réplicas), tracejado = teoria.

- **Painel esquerdo (média):** quatro exponenciais, as de `m₀>0` decaindo e as de `m₀<0` subindo,
  todas rumo a 0. O tracejado teórico **coincide** com a linha cheia (só aparece nas bordas, onde o
  tracejado sobressai): a concordância é no nível de 10⁻³. Em `t = τ = 250`: `⟨m⟩ = 0,3676` medido
  contra `0,3671` teórico (`= e^{−1}`) **[medido]**. Em `t = 2000 = 8τ`: `−0,0006`, `+0,0001`,
  `+0,0005`, `+0,0006` — ruído de média, do tamanho `1/√(N·R) = 0,0447/44,7 = 0,001`
  **[medido e calculado]**.
- **Painel direito (variância):** as quatro curvas partem de 0 e sobem para `1/N = 0,002`, sem
  diferenciar `m₀` no fim (medido: 0,00199 / 0,00194 / 0,00206 / 0,00199 **[medido]**). O
  `m₀` controla **só o começo** da variância (quanto maior `|m₀|`, mais tempo a variância leva
  para "esquecer" — o termo `m₀²λ₁^{2t}`), não o patamar.
- **O que escrever:** a média relaxa com `τ = N/2` e a variância **satura em `1/N`**, o mesmo valor
  para todas as condições iniciais; a informação de `m₀` desaparece, primeiro da variância (taxa
  `4/N`) e depois da média (taxa `2/N`).
- **Pegadinha:** a variância sobe. Não é intuitivo, mas é consequência de o sistema partir de um
  estado *sem* flutuação (`t=0`, todas as réplicas idênticas) e ganhar flutuação conforme explora
  os estados.

### 5.2 `part3-N` — dependência com `N` (`N = 5, 50, 500`, `m₀ = 1`)

- **Painel esquerdo (média):** as três curvas são a mesma exponencial em escalas de tempo
  diferentes: `τ = 2,5 / 25 / 250` passos. `N=5` cai para 0 em ~5 passos; `N=500` leva ~1150
  passos para chegar a 1% de `m₀` **[calculado: `t = ln(100)/(2/N)`]**. Depois disso, cada curva é
  ruído em torno de 0.
- **Painel direito (variância):** os patamares são `1/N = 0,2 / 0,02 / 0,002` (as linhas pontilhadas
  marcam exatamente esses valores). Medido em `t=2000`: `0,2096 / 0,0195 / 0,0020` **[medido]**.
- **O que escrever:** `N` não muda a *forma* da relaxação, muda a **escala de tempo** (`∝ N`) e a
  **largura da flutuação** (`∝ 1/√N`). Com `N` grande o sistema demora mais para relaxar, mas
  flutua menos quando chega lá. É o compromisso típico de sistemas estatísticos, e é o oposto do
  que a intuição de "mais partículas = mais rápido" sugere.
- **Detalhe do `N=5`:** com 5 spins, `m` só assume 6 valores (`±1; ±0,6; ±0,2`), então a variância
  salta para o patamar em ~2 passos e a "curva" é um degrau. O ruído no painel esquerdo do `N=5`
  também é o maior, porque a média de 2000 réplicas de uma variável com `σ = 0,447` tem ruído
  `0,01`: visível na escala do gráfico.

### 5.3 `part3-Pm-histogramas` — distribuição estacionária

`6000` réplicas rodando até `t = 4N` (relaxado: `4N = 8τ`), histograma dos **dois últimos passos**
concatenados (`2×6000 = 12 000` amostras). Barras = simulação, curva = gaussiana de média 0 e
`σ = 1/√N`.

- **`N = 5`:** só **6 barras** — são os 6 valores possíveis de `m` (`M = ±5, ±3, ±1`), não uma
  gaussiana. A gaussiana (`σ = 0,447`) passa por cima, mas o histograma é **discreto**: as
  probabilidades são `1/32, 5/32, 10/32` para `|m| = 1; 0,6; 0,2`. Teste contra `Binomial(5,1/2)`:
  `χ² = 1,4` com 5 graus de liberdade **[medido]** — compatível.
- **`N = 50`:** gaussiana já muito boa; `σ` medido `0,1403` contra `1/√50 = 0,1414`;
  `χ² = 38,4` com 26 g.l. contra a binomial (**[medido]**; o valor é alto, mas as 12 000 amostras
  vêm de 6000 cadeias correlacionadas, então o `χ²` não é um teste calibrado).
- **`N = 500`:** barras finas e nítidas, `σ` medido `0,0451` contra `0,0447`; colapso perfeito na
  gaussiana. `xlim` do painel é `±0,179 = ±4/√N`.
- **O que escrever:** `P(m)` é **binomial** para todo `N` (contagem de configurações: `P(M) = C(N,(N+M)/2)/2^N`) e vira **gaussiana** quando `N` cresce, pelo TCL. `N=5` é a prova de que "binomial" e "gaussiana" não são a mesma coisa: a forma discreta é visível; `N=500` é a prova de que o limite funciona na prática.
- **Pegadinha de binagem:** a magnetização anda de `2/N` em `2/N`. Se você escolher bins de largura
  `1/N` (metade), **metade das barras fica vazia** e o histograma parece "listrado" — é artefato de
  binagem, não física. O código usa `2/N`, que é o certo: cada barra contém exatamente um estado
  possível.

## 6. As quatro questões de 5.2 (rascunho para você reescrever)

### 1. Evolução da magnetização média. E a longo prazo?

`⟨m_t⟩` decai exponencialmente, `⟨m_t⟩ = m₀(1−2/N)^t`, com tempo característico `τ = N/2`. A longo
prazo a magnetização média tende a **zero**: sem campo externo, o paramagneto não tem ordem e as
duas orientações ficam igualmente prováveis. Duas ressalvas que valem ponto: (i) o decaimento é
assintótico, nunca exatamente zero em tempo finito; (ii) uma **trajetória individual** não vai a
zero — ela continua oscilando em torno de zero, dentro de uma faixa de largura `1/√N`. Quem vai a
zero é a média sobre o ensemble. Medido: em `t = 8τ` as médias estão em `±0,0006` **[medido]**.

### 2. Simulação contra solução analítica: semelhanças, diferenças, papel de `N`

- **Semelhanças:** forma funcional idêntica (exponencial), mesmo `τ = N/2`, mesmo limite `m=0`, e
  a concordância é quantitativa em todo o intervalo — em `t = τ`, `0,3676` contra `0,3671`
  **[medido]**.
- **Diferenças:** são de dois tipos, e nenhuma é erro da teoria.
  1. **Ruído estatístico:** a média simulada de `R` réplicas flutua com `1/√(N·R)`; com
     `N=500, R=2000` isso é `0,001` **[calculado]**. É o que sobra depois da relaxação (as médias
     finais não são exatamente zero).
  2. **Discretização:** `m` só assume `N+1` valores, então a "exponencial" é uma escada. Para
     `N=5` são 6 degraus — visivelmente diferente de uma curva contínua. Para `N=500`, 501 degraus
     já parecem contínuos.
- **O que isso revela sobre `N`:** a Eq. (11) é **exata para qualquer `N`** (é uma média de cadeia
  de Markov, não uma aproximação de campo médio). `N` não controla a validade da equação, controla
  (i) a **escala de tempo** `τ = N/2`, (ii) a **granularidade** de `m` e (iii) a **largura** das
  flutuações `1/√N`. Dizer que "a teoria vale melhor para `N` grande" é impreciso: o que melhora
  com `N` é a *aparência contínua* da curva e a *pequenez relativa* das flutuações.

### 3. Como as flutuações (variância) se comportam no tempo, e como dependem de `N`?

- No tempo: partem de zero e crescem até saturar em `1/N`; a forma é a diferença de duas
  exponenciais (`4/N` e `2/N`). Sobem porque o ensemble começa perfeitamente ordenado e vai
  ocupando estados diferentes; saturam porque a distribuição binomial se estabiliza. O tempo para
  saturar é `~2,3τ` para 99% **[calculado: 573 passos com N=500]**, ou seja metade do tempo da
  média, coerente com a taxa `4/N` ser o dobro de `2/N`.
- Com `N`: o **patamar cai como `1/N`** (`0,2 → 0,02 → 0,002` **[medido]**), então o desvio-padrão
  cai como `1/√N`. É a lei dos grandes números: quanto mais spins, menor a flutuação da
  magnetização por spin. Mas o *tempo* para chegar lá cresce como `N` — as duas coisas caminham em
  sentidos opostos e são a mesma física (cada spin é sorteado uma vez a cada `N` passos).

### 4. Forma de `P(m)` no estacionário × TCL e lei dos grandes números

- **`P(m)` é binomial exata** (contagem de configurações com `N↑` spins up), simétrica em torno de
  0, com `Var(m) = 1/N`.
- **TCL:** `M = Σsᵢ` é soma de `N` variáveis independentes, identicamente distribuídas, com média 0
  e variância 1. O teorema garante que `M/√N` tende a uma normal padrão; equivalentemente
  `m = M/N` tende a `N(0, 1/N)`. É exatamente a curva vermelha dos três painéis. Os requisitos que
  você deve nomear: independência (no equilíbrio os spins são independentes), mesma distribuição,
  variância finita. Medido: `σ = 0,4442 / 0,1403 / 0,0451` contra `1/√N = 0,4472 / 0,1414 / 0,0447`
  **[medido]**.
- **Lei dos grandes números:** `m → 0` em probabilidade, porque a largura `1/√N` some quando
  `N→∞`. É a versão "a flutuação desaparece"; o TCL é a versão "como ela desaparece" (com que
  forma e com que taxa `1/√N`). Vale escrever as duas juntas: **a LLN diz que `m` fica perto de 0;
  o TCL diz que o afastamento residual é gaussiano de largura `1/√N`.**
- **Onde o TCL ainda não vale:** `N=5`. São 6 valores possíveis e a gaussiana é uma aproximação
  ruim (compare a altura das barras com a curva no painel esquerdo). É o contraexemplo que o
  roteiro pede para você identificar.

## 7. Defeito encontrado no caderno (para você decidir se corrige)

A célula `part3-Pm-dados` traz o comentário:

```python
# Dois tempos consecutivos: assim m cobre as duas classes de M possíveis, e não só
# metade dos valores que a magnetização pode assumir.
```

**Isso está errado.** Neste modelo `M` varia de `±2` por passo, então a paridade de `M` é
**invariante** (`M ≡ N mod 2`): só existe **uma** classe de valores possíveis, `N+1` estados ao
todo. O comentário descreve a situação do gás de Ehrenfest (Parte 1), onde o passo é `±1` e a
paridade alterna — lá sim é preciso amostrar em passos ímpares para cobrir as duas paridades.

Concatenar os dois últimos passos continua sendo útil (dobra as amostras e reduz o ruído do
histograma), mas o motivo escrito é falso. Sugestão: trocar por algo como *"dois últimos passos:
o dobro de amostras para o histograma"*.

## 8. Erros comuns nesta parte

| Erro | Correção |
|---|---|
| "a magnetização vai a zero" (trajetória) | a **média** vai a zero; a trajetória oscila com `σ = 1/√N` |
| "a variância diminui no tempo" | ela **cresce**, de 0 até `1/N` |
| "`⟨m⟩` obedece Eq. (11) só para `N` grande" | é exata para todo `N`; `N` muda `τ`, granularidade e largura |
| "`σ = 1/N`" | `σ = 1/√N`; a **variância** é `1/N` |
| "`N=5` converge mais rápido, logo está mais perto do equilíbrio" | converge em menos passos porque `τ` é menor, mas a flutuação relativa é enorme |
| "o histograma ficou listrado, a simulação tem bug" | largura de bin diferente de `2/N` |
