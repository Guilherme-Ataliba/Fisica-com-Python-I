# Parte 2 — Trocas cinéticas e a distribuição de Boltzmann

Números marcados **[medido]** vêm da reprodução exata das células (`SEED = 42`), em `04-numeros.md`.

## 1. O modelo

`N = 1000` partículas com energias `w_i ≥ 0`. A cada passo de tempo:

1. sorteiam-se duas partículas `i` e `j` e um número `ε ~ U[0,1]`;
2. calcula-se `Δw = (1−ε)w_i − ε w_j`;
3. as energias passam a `w_i' = w_i − Δw` e `w_j' = w_j + Δw`.

O passo de tempo é **uma colisão** (o intervalo médio entre colisões), não um "tempo físico":
é por isso que a escala relevante nas figuras é `t/N` = **colisões por partícula**.

## 2. O que a regra faz, em uma linha de álgebra

Substituindo `Δw`:

```
w_i' = w_i − (1−ε)w_i + εw_j = ε·(w_i + w_j)
w_j' = w_j + (1−ε)w_i − εw_j = (1−ε)·(w_i + w_j)
```

Duas leituras que resolvem metade das questões:

- **A energia do par é exatamente conservada:** `w_i' + w_j' = w_i + w_j`. Como as outras partículas
  não são tocadas, `E = Σw` é constante em **todo** passo — não só no equilíbrio.
- **A troca é uma combinação convexa:** para `ε ∈ [0,1]`, `w_i'` e `w_j'` são frações de
  `w_i + w_j`, logo **nunca negativas**. A condição `w' ≥ 0` do roteiro é, para esta regra,
  automaticamente satisfeita: medido, **0 colisões rejeitadas em 10 000 passos** **[medido]**.
  A checagem no código (`if w[i]-delta_w >= 0 and w[j]+delta_w >= 0`) nunca dispara — ela protegeria
  outras regras de troca, não esta.

Detalhe que vale mencionar se você quiser mostrar rigor: se o sorteio der `i == j`, a atualização
sequencial do código soma `−Δw` e `+Δw` na mesma partícula e nada acontece (a colisão é
descartada na prática). Nas 10 000 colisões medidas isso ocorreu 9 vezes **[medido]**. É
justamente o comportamento correto — dois números iguais não formam um par.

## 3. Por que o atrator é a exponencial

O sistema troca energia, mas não a perde nem a ganha: `E` fixo. Entre todas as distribuições `f(w)`
de uma variável não-negativa com média fixa, a de **entropia máxima** é

```
f(w) = β·e^{−βw} ,      β = 1/⟨w⟩
```

(a demonstração com multiplicadores de Lagrange é a parte A da tarefa). A dinâmica de troca é
simétrica sob `(i,j,ε) ↔ (j,i,1−ε)`, que é a condição de balanço detalhado que faz dessa
exponencial o estado estacionário.

**O ponto central para o relatório:** a energia total fixa a **média** `⟨w⟩`, e a média fixa `β`.
Nada mais. Como `E` é constante, `β` é o mesmo em todos os instantes — inclusive em `t = 0`.
O que a simulação faz não é *esfriar* nem *aquecer* o gás: é **manter o mesmo `β` e mudar a forma da
distribuição**. Medido: `⟨w⟩ = 0,9944` em `t = 0` **e** em `t = 10⁵`; `β = 1,0057` **[medido]**.

A distribuição inicial `U[0,2]` já tem `⟨w⟩ = 1` — a média certa e a forma errada. É por isso que a
curva teórica é a mesma nos seis painéis e só o histograma se move em direção a ela.

## 4. A figura: seis histogramas (`part2-histogramas`)

Densidades de `w` em `t = 0, 10, 10², 10³, 10⁴, 10⁵`, 48 bins de largura `0,125` em `[0,6]`,
sobrepostas à curva `βe^{−βw}` com `β = 1,0057` calculado da média **final**. Cada título mostra a
energia total do instante.

- **`t = 0`:** uniforme, densidade `1/2` até `w=2` e zero depois. A curva de Boltzmann é muito mais
  alta perto de `w=0` (`f(0) ≈ 1`) e cai exponencialmente.
- **`t = 10`:** praticamente idêntico ao inicial — 10 colisões mexem em ~20 das 1000 partículas.
  Você pode dizer literalmente: *"em `t=10` o sistema ainda não começou"*.
- **`t = 10²`:** já aparece a queda em `w` grande, mas o miolo ainda é chato.
- **`t = 10³`:** a forma exponencial está estabelecida; `L1 = 0,20`, ou seja ~10% da massa
  deslocada em cada sentido (`L1/2` é a distância de variação total).
- **`t = 10⁴` e `t = 10⁵`:** indistinguíveis entre si e da curva — o regime estacionário.
- **`E = 994,36` em todos os seis painéis** é a prova numérica da conservação (é o mesmo número que
  o `print` da célula de inicialização).

Distância `L1` entre histograma e curva (medida, soma de `|h − f|·Δw`):

| `t` | 0 | 10 | 10² | 10³ | 10⁴ | 10⁵ |
|---|---|---|---|---|---|---|
| `L1` | 0,564 | 0,565 | 0,500 | 0,204 | 0,136 | 0,140 |

Sonda mais fina **[medido]**: `0,44` em `t=200`, `0,41` em `300`, `0,32` em `500`, `0,26` em `700`,
`0,20` em `10³`, `0,15` em `1,5·10³`, e platô de `0,13–0,14` a partir de `3·10³`.

- **Como ler a tabela:** a convergência é rápida em **colisões por partícula** — `t/N = 1` já dá
  `L1 = 0,20`, e `t/N ≈ 3` chega ao piso. Não use `t` cru para dizer "demora muito": diga
  "~3 colisões por partícula".
- **Por que o `L1` para em ~0,14 e não em zero:** com 1000 partículas em 48 bins, o próprio
  histograma tem ruído de contagem; o piso de `0,13–0,14` é esse ruído, não desvio da teoria. A
  prova é que ele **não** diminui de `10⁴` para `10⁵` (0,136 → 0,140). **Interpretação**, com o
  número medido ao lado.

## 5. As quatro questões de 5.2

### 1. Como a distribuição evolui do início ao fim?

- Sai de uma **uniforme em `[0,2]`** (todas as energias do mesmo tamanho são igualmente prováveis,
  nada acima de 2) e vai para uma **exponencial decrescente**, com muito mais partículas de baixa
  energia e uma cauda longa.
- A mudança é **monotônica na forma** e essencialmente terminada em `3·10³` passos.
- A média **não muda** (`0,9944` do começo ao fim): o que muda é a dispersão — a distribuição se
  "entorta" em torno da mesma média. Vale dizer: a uniforme e a exponencial com `β=1` têm a mesma
  média e entropias diferentes; a dinâmica escolhe a de maior entropia.

### 2. Comparação com a curva teórica: o que concluir sobre a convergência?

- Nos instantes iniciais (`t = 0, 10, 10²`) a divergência é grande (`L1 ≈ 0,50–0,56`).
- Em `t = 10³` a forma já é exponencial (`L1 = 0,20`) e em `t ≥ 3·10³` o histograma é
  indistinguível da curva (`L1 ≈ 0,14`, que é o piso de ruído).
- Conclusão: **a convergência para o equilíbrio é real e verificável**, e o critério objetivo é a
  distância `L1` cair de ~0,56 para o piso de ruído e **parar de cair**.
- Cuidado com a frase "converge exatamente": com um número finito de partículas o histograma é
  sempre uma amostra finita da exponencial, com ruído `∝ 1/√N`; o que converge é a distribuição,
  não o histograma particular.

### 3. A energia total se conserva? Justifique pela regra de atualização.

Sim, exatamente, e a prova é de uma linha:

```
E' = w_i' + w_j' = (w_i − Δw) + (w_j + Δw) = w_i + w_j = E
```

As demais partículas não são alteradas, então a soma global é constante. Na simulação isso aparece
como `E = 994,36` em todos os seis painéis, e o valor não muda nem no último algarismo **[medido]**.
O que a colisão faz é **redistribuir** energia, nunca criar ou destruir.

### 4. Por que a condição `w ≥ 0` é importante?

Três respostas, em ordem de força:

1. **Física:** `w` é energia cinética; não existe negativo. Permitir `w < 0` seria modelar outra
   coisa.
2. **Matemática:** `f(w) = βe^{−βw}` só é normalizável em `[0,∞)`. Em `(−∞,∞)` a integral diverge,
   então o próprio estado de equilíbrio deixaria de existir (esta é a resposta que já está no
   notebook, e está correta).
3. **Para esta regra específica:** a condição é **automaticamente satisfeita**, porque
   `w_i' = ε(w_i+w_j)` e `w_j' = (1−ε)(w_i+w_j)` com `ε ∈ [0,1]`. A checagem do código nunca
   dispara (0 rejeições em 10 000 colisões **[medido]**). Vale escrever isso: mostra que você
   entendeu *por que* o roteiro pede a condição, e que ela seria necessária para outras regras de
   troca (por exemplo, se `ε` pudesse sair de `[0,1]`).

## 6. Erros comuns nesta parte

| Erro | Correção |
|---|---|
| "`β` aumenta com o tempo até o equilíbrio" | `β = 1/⟨w⟩` é fixo desde `t=0`; a forma muda, a média não |
| "o histograma converge para a curva" | a distribuição converge; o histograma flutua em torno dela |
| "a colisão conserva energia porque a checagem impede negativos" | conserva por construção (`+Δw` e `−Δw`), a checagem é outra coisa |
| "`t = 10⁵` mostra melhor que `t = 10⁴`" | os dois são o mesmo regime; a diferença é ruído |
| contar passos em vez de colisões por partícula | use `t/N` para falar de rapidez |
