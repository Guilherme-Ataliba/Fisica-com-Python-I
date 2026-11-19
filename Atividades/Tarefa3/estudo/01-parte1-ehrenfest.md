# Parte 1 — Gás de Ehrenfest: teoria e leitura dos gráficos

Números marcados **[medido]** vêm da reprodução exata das células (`SEED = 42`), em `04-numeros.md`.

## 1. O modelo

`N` partículas em duas urnas, A e B. `m(t)` conta as partículas em A. Em cada passo **uma**
partícula é sorteada uniformemente e muda de urna:

```
P(m → m−1) = m/N          (sorteou alguém de A)
P(m → m+1) = (N−m)/N      (sorteou alguém de B)
```

Duas leituras que valem para o texto:

- O passo é **±1**, então `m` tem a mesma paridade de `m₀ + t`. Isso importa na figura 3 (§5.3).
- O processo é **markoviano e reversível**: a taxa de A→B é proporcional a `m`, a de B→A a `N−m`.
  É essa dependência do estado que produz o puxão para `N/2` — não há campo externo nem
  "temperatura" aqui, só contagem.

## 2. A média: de onde sai `(1 − 2/N)^t`

Condicionando no estado atual:

```
⟨m_{t+1}⟩ = m + P(m+1)·(+1) + P(m−1)·(−1)
          = m + (N−m)/N − m/N
          = m·(1 − 2/N) + 1
```

O ponto fixo é `m* = N/2`: `N/2·(1−2/N) + 1 = N/2`. Com `x = m − N/2`, o termo constante some:

```
x_{t+1} = x_t·(1 − 2/N)   ⇒   ⟨x_t⟩ = x₀·λ₁^t,   λ₁ = 1 − 2/N
```

Voltando:

```
⟨m(t)⟩ = N/2 + (m₀ − N/2)·(1 − 2/N)^t
```

`λ₁ = 1 − 2/N = e^{−2/N + O(N⁻²)}` para `N` grande, ou seja **tempo característico `τ = N/2`
passos**. Frase para o relatório: *a média é uma exponencial com constante de tempo proporcional a
`N`; dobrar o número de partículas dobra o tempo de relaxação.*

Como `2/N` é a probabilidade de "acertar" uma partícula específica, `τ = N/2` tem leitura direta:
são necessários ~`N/2` sorteios para que uma dada partícula seja sorteada uma vez.

## 3. A variância: por que ela tem **dois** exponenciais

O segundo momento em torno do equilíbrio. Com `x = m − N/2`, o passo `Δx` vale `±1` com
probabilidades `1/2 ∓ x/N`:

```
⟨Δx⟩ = −2x/N ,      ⟨Δx²⟩ = 1
⟨x²_{t+1}⟩ = x² + 2x⟨Δx⟩ + ⟨Δx²⟩ = x²(1 − 4/N) + 1
```

O ponto fixo de `⟨x²⟩` é `1/(4/N) = N/4`:

```
⟨x_t²⟩ = N/4 + (x₀² − N/4)·λ₂^t ,      λ₂ = 1 − 4/N
```

E a variância é `⟨x²⟩ − ⟨x⟩²`, com `⟨x_t⟩ = x₀λ₁^t`:

```
Var[m(t)] = N/4 + (x₀² − N/4)(1 − 4/N)^t − x₀²(1 − 2/N)^{2t}
```

Três consequências que explicam o gráfico:

1. **`λ₂` é duas vezes mais rápido que `λ₁`** (`4/N` contra `2/N`), mas `λ₁² = (1−2/N)²` é
   *quase* igual a `λ₂` (para `N=100`: `0,9604` contra `0,96`). As duas exponenciais têm taxas
   quase idênticas; por isso a variância parece uma exponencial simples e **não** ultrapassa `N/4`.
2. No equilíbrio `Var → N/4`, o valor da binomial, independente de `m₀`.
3. A variância **começa em zero** (todos os sistemas iguais em `t=0`) e sobe. É o oposto da
   intuição de "flutuação diminui": aqui o sistema *ganha* flutuação porque a distribuição se
   abre.

Valores de `Var(t)` com `N=100, x₀=−50` (tabela para citar):

| `t` | 0 | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|---|
| `Var` teórica | 0 | 6,56 | 14,92 | 22,78 | 24,93 | 25,00 |

## 4. O equilíbrio: contagem e limite gaussiano

No equilíbrio cada partícula está em A ou B **independentemente** com probabilidade `1/2`, então

```
P(m) = C(N, m) / 2^N            (binomial exata, para todo N)
⟨m⟩ = N/2 ,    Var = N/4 ,    σ = √N/2
```

Para `N` grande, `C(N,m)/2^N` é dominada por um fator gaussiano: escrevendo `m = N/2 + z√N/2`,

```
P(m) ≈ (1/√(2π·N/4)) · exp( −(m − N/2)² / (2·N/4) )
```

O ponto que costuma faltar no relatório: **o equilíbrio não é um número, é uma distribuição de
largura `√N/2`**. O sistema "vai para `N/2`" no sentido de que a *média* vai, mas cada realização
fica oscilando numa faixa de largura `√N/2` — que cresce com `N`, embora a largura *relativa*
`1/√N` diminua. É a mesma distinção entre lei dos grandes números (a média) e teorema central do
limite (a forma da flutuação) que você usou na Parte 3.

## 5. Figura a figura

### 5.1 Animação (`part1-animacao`, `N = 60`, 200 passos)

- **O que está na tela:** dois retângulos, um ponto por partícula, título com "Passo `t`: `k`
  partículas na urna A".
- **O que se vê:** em `t=0`, 60 pontos em A e nenhum em B. Nos primeiros passos a urna A esvazia
  rápido e as duas se equalizam; depois o número oscila em torno de 30.
- **Números:** `N/2 = 30`; `τ = N/2 = 30` passos, então em `t = 200 = 6,7τ` o sistema está
  relaxado (desvio esperado da média: `(m₀−N/2)λ₁^200 = 30·(1−2/60)^200 = 30·e^{−6,9} ≈ 0,03`).
- **O que escrever:** a relaxação é rápida e **não** é monotônica — o número de partículas em A
  chega perto de 30 e passa a flutuar; o estado final é estacionário *em distribuição*, não
  congelado.
- **Pegadinha:** a animação tem 60 partículas e 200 passos porque é ilustrativa. Não use a
  animação para medir expoentes; para isso existem as figuras 2 e 3.

### 5.2 Média e variância, `M = 2000` e `M = 10000` (`part1-momentos`)

Quatro painéis: coluna 1 média, coluna 2 variância; linha 1 com `M = 2000` réplicas, linha 2 com
`M = 10000`. Pontos pretos = simulação, linha cheia vermelha = teoria, tracejado laranja = valor
assintótico (`N/2` e `N/4`). `N = 100`, `m₀ = 0`, `t` até 400.

- **Eixo x:** passo de tempo, `0…400 = 8τ`.
- **Média:** sobe de 0 a 50 e satura. Em `t = τ = 50` a curva já percorreu **63%** do caminho
  (31,8 de 50) **[medido]**: `1 − λ₁^50 = 0,636`. Em `2τ`: 87%; em `3τ`: 95%; em `5τ`: 99,4%.
  Use essa tabela para justificar "por que 400 passos bastam".
- **Variância:** sobe de 0 a 25 e satura, sem ultrapassar 25.
- **Por que as duas linhas de baixo são melhores:** o estimador de variância com `M` réplicas tem
  ruído `≈ Var·√(2/(M−1))` = **0,79** para `M=2000` e **0,35** para `M=10000` **[calculado]**.
  É exatamente o que se vê: no painel de 2000 réplicas o desvio da variância chega a **+1,33** em
  `t=179` e **−2,29** em `t=129`, e termina em `24,26` no `t=400` (teoria 25,00); com 10000
  réplicas os mesmos extremos caem para `+0,51` e `−0,99`, terminando em `24,48` **[medido]**.
  Note que o desvio muda de sinal: é ruído, não um viés sistemático.
- **Média também tem ruído:** `σ/√M = 5/44,7 = 0,11` (2000 réplicas) e `0,05` (10000). O desvio
  quadrático médio medido foi `0,109` e `0,039` **[medido]** — bate com a previsão.
- **O que escrever:** a média é reconstruída com precisão visivelmente melhor que a variância com
  o mesmo número de réplicas — não porque a teoria da variância esteja errada, mas porque
  **estimar uma variância é mais difícil que estimar uma média** (o ruído relativo é `√(2/M)`
  contra `1/√M`). Aumentar `M` melhora as duas.
- **Pegadinha:** não diga que o desvio da variância em relação à teoria "desaparece quando `t`
  cresce". Ele não desaparece: ele é ruído do estimador, do mesmo tamanho em todo `t`, e só cai
  com `M`.

### 5.3 Distribuição de equilíbrio (`part1-equilibrio`, `N = 10` e `N = 100`)

Duas réplicas de `5000` simulações rodando até `t = 20N`, amostradas em **10 instantes** espaçados
de `N+1` passos, entre `10N` e `20N` (ou seja, de `10τ` a `20τ`: já relaxado), total **50 000**
amostras por painel. Barras = histograma; pontos vermelhos = `Binomial(N,1/2)`; tracejado =
gaussiana de média `N/2` e variância `N/4`.

- **`N = 10`:** só 11 valores possíveis, barras largas e discretas. Pico em `m=5` com contagem
  `12 467` contra `12 305` esperados **[medido]**; média `5,005` (esperado 5), variância `2,492`
  (esperado 2,5). A gaussiana passa perto, mas o ajuste é apenas razoável — com 11 barras a
  comparação é visual, e a binomial é o modelo certo.
- **`N = 100`:** barras quase contínuas, pico em 50 com `4 070` contra `3 980` **[medido]**;
  média `49,971`, variância `24,998`. Aqui a gaussiana é indistinguível da binomial na escala do
  gráfico.
- **Por que 10 instantes espaçados de `N+1`:** `N+1` é ímpar e a cada passo a paridade de `m`
  inverte. Amostrar em passos de `N+1` garante **5 instantes pares e 5 ímpares**, então o
  histograma cobre os `N+1` valores. Se o espaçamento fosse par, metade das barras sairia vazia e
  o histograma apareceria "listrado" — é um artefato de amostragem, não física.
- **O que escrever:** a distribuição de equilíbrio é binomial (contagem de `C(N,m)` configurações
  equiprováveis) e o limite `N` grande é gaussiano pelo TCL. `N=10` já obedece à binomial; o que
  `N=10` **não** faz bem é parecer gaussiana — é essa a mensagem do painel esquerdo.
- **Limitação honesta (pode ir no relatório):** as 50 000 amostras não são independentes — cada
  uma das 5000 réplicas contribui com 10 valores correlacionados. Por isso um teste `χ²` formal com
  `N` graus de liberdade não é válido aqui (a contagem de `graus de liberdade` pressupõe amostras
  independentes). A validação do painel é a comparação de média e variância com `N/2` e `N/4`, que
  fecha em três algarismos, mais a forma visual.

## 6. Erros comuns nesta parte

| Erro | Correção |
|---|---|
| "a variância tende a `N/2`" | tende a `N/4`; `N/2` é a média |
| "o sistema converge para `m = N/2`" | a **média** converge; cada trajetória flutua com `σ = √N/2` |
| "`(1−2/N)^t` é aproximação" | é exata para a média, para todo `N` |
| "o histograma deu binomial porque `N` é grande" | é binomial para **todo** `N`; o TCL só muda a forma aparente |
| "a variância acompanha a exponencial da média" | ela tem taxa `4/N`, o dobro; e é diferença de duas exponenciais |
| ler ruído de réplicas como desvio da teoria | compare o desvio com `0,79` (`M=2000`) antes de concluir |
