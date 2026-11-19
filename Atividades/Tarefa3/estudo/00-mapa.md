# Mapa da Tarefa 3 — o que cada parte pede e o que cada gráfico tem de mostrar

> Documento de estudo. Não é o relatório: é o material de onde você tira a explicação dos
> gráficos e as respostas de 5.2. Todos os números marcados **[medido]** vieram de rodar
> exatamente o código das células, com `SEED = 42`, e estão reunidos em `04-numeros.md`.
> Onde há interpretação, está dito "interpretação".

## 1. As três partes são três cadeias de Markov

| Parte | Modelo | Variável | Passo por unidade de tempo | PDF |
|---|---|---|---|---|
| 1 | Gás de Ehrenfest (duas urnas) | `m` = partículas na urna A | ±1 | `task_3_1_2026_2.pdf` |
| 2 | Trocas cinéticas | `w_i` = energia da partícula `i` | par de energias trocado | `task_3_2_2026_2.pdf` |
| 3 | Paramagneto estocástico | `M` = soma dos spins | ±2 | `task_3_3_2026_2.pdf` |

Cada implementação é uma **cadeia de Markov**: o próximo estado depende só do estado atual e de um
sorteio. É por isso que os gráficos têm sempre a mesma anatomia — uma média que relaxa e uma
distribuição que se estabiliza — e é por isso que a teoria de cada parte é uma equação de
recorrência para a média mais uma para o segundo momento.

## 2. A estrutura que se repete (é isto que explica os três primeiros gráficos)

Em toda parte com dois estados, escrevendo `x = variável − valor de equilíbrio`:

```
⟨x_t⟩ = x₀ · λ₁^t            λ₁ = 1 − 2/N     ← média
E[x_t²] = eq + (x₀² − eq) λ₂^t   λ₂ = 1 − 4/N   ← segundo momento
Var = E[x_t²] − ⟨x_t⟩²        ← diferença de dois exponenciais
```

- **λ₁** controla a média: `1/λ₁` passos, ou seja `τ = N/2` passos para decair por `e`.
- **λ₂** controla o segundo momento: decai **duas vezes mais rápido** (`4/N` contra `2/N`).
- O equilíbrio tem largura `∝ 1/√N` e não depende de `m₀`.

A consequência prática para o texto: **a variância não é uma exponencial simples** enquanto a média
ainda não chegou ao equilíbrio; ela é a diferença de duas exponenciais de taxas quase iguais. Se você
tentar descrever a variância como "`1 − e^{−t/τ_v}`", o ajuste não fecha.

## 3. Parte 1 e Parte 3 são a mesma cadeia

Substituindo `m_s = 2·m_A/N − 1` na regra do gás de Ehrenfest (urna A com `m_A` partículas):

```
P(m_A → m_A − 1) = m_A/N  =  (1 + m_s)/2      ← exatamente a regra do paramagneto
```

Ou seja: **o paramagneto é o gás de Ehrenfest escrito na variável spin**, com `M = 2·m_A − N`.
Isso explica por que as duas partes têm `λ₁ = 1 − 2/N` e `λ₂ = 1 − 4/N`: é a mesma cadeia.

As constantes de equilíbrio mudam só porque a variável muda:

```
urna:        Var(m_A) = N/4                (binomial)
spin:        Var(M)   = 4·Var(m_A) = N     (M = 2m_A − N)
magnetização: Var(m)  = Var(M)/N² = 1/N    (m = M/N)
```

Então `N/4` (urna) e `1/N` (magnetização) são o mesmo resultado em duas unidades: partículas
contra magnetização por spin. Confira sempre qual é a variável antes de comparar.

## 4. A Parte 2 é de outra família

Não há dois estados: há energias contínuas trocadas aos pares. A quantidade conservada é `E = Σwᵢ`
e o atrator é a **exponencial** `f(w) = βe^{−βw}` com `β = 1/⟨w⟩`. O análogo do "`λ^t`" aqui é o
tempo medido em **colisões por partícula**, não em passos de tempo.

## 5. Checklist: o que cada figura tem de provar

| Figura | Célula | Tem de mostrar | Não pode mostrar |
|---|---|---|---|
| Animação das urnas | `part1-animacao` | partículas inicialmente todas em A, espalhando até `N/2` | afirmar que o sistema "para" — ele flutua |
| Média e variância (2×2) | `part1-momentos` | simulação sobre a curva; patamar em `N/2` e `N/4` | ruído de réplicas lido como desvio de teoria |
| Distribuição de equilíbrio | `part1-equilibrio` | barras sobre `Binomial(N,1/2)`; gaussiana boa para `N=100` | que a binomial "vira" gaussiana em `N=10` |
| Seis histogramas de energia | `part2-histogramas` | uniforme → exponencial, `E` constante | que `β` muda com o tempo (ele é fixo) |
| Relaxação de `⟨m_t⟩` e `σ²` | `part3-momentos` | quatro `m₀` colapsando em `m=0`; `σ² → 1/N` | que `⟨m⟩` chega a zero exatamente |
| Dependência com `N` | `part3-N` | `τ ≃ N/2`; ruído final `≃ 1/√N` | que `N=5` converge "mais devagar" |
| `P(m)` estacionário | `part3-Pm-histogramas` | gaussiana `σ = 1/√N`; `N=5` discreto | barras vazias alternadas (largura de bin errada) |

## 6. Como ler este material

- `01-parte1-ehrenfest.md` — teoria da média/variância/equilíbrio e as três figuras.
- `02-parte2-trocas-cineticas.md` — conservação, Boltzmann, as seis figuras, as 4 questões.
- `03-parte3-paramagneto.md` — Eq. (11), as três figuras, as 4 questões de 5.2.
- `04-numeros.md` — todas as medidas, com o comando que as reproduz.
