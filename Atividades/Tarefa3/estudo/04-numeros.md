# Números medidos — origem de cada valor citado nos documentos

Todos os números dos documentos `01`, `02` e `03` saem de dois scripts desta pasta, que reproduzem
o código das células do notebook **sem alterar o notebook**:

```bash
.venv/bin/python Atividades/Tarefa3/estudo/medidas.py     # -> numeros.txt
.venv/bin/python Atividades/Tarefa3/estudo/sonda_p2.py    # -> sonda_p2.txt
```

`medidas.py` reproduz `ehrenfest`, `colisao/simular` e `simular` exatamente como estão nas células,
com `SEED = 42`, e imprime os valores usados. Saídas gravadas nesta pasta: `numeros.txt` (65
linhas, ~10 s de execução) e `sonda_p2.txt` (~0,5 s).

Status de cada medida, para não confundir o que foi rodado com o que foi deduzido:

| Classe | O que é |
|---|---|
| **medido** | número impresso por `medidas.py`/`sonda_p2.py`, rodando o código do notebook |
| **calculado** | valor fechado de uma fórmula (por exemplo `Var·√(2/(M−1))`), sem simulação |
| **teórico** | vem da Eq. do PDF (`⟨m_t⟩`, `Var`, `β = 1/⟨w⟩`) |

## Parte 1

`N = 100`, `m₀ = 0`, `t_max = 400`.

| `t` | média sim (M=2000) | média teórica | var sim (M=2000) | var teórica | var sim (M=10000) |
|---|---|---|---|---|---|
| 0 | 0,000 | 0,000 | 0,0000 | 0,0000 | 0,0000 |
| 10 | 9,156 | 9,146 | 1,4557 | 1,4408 | 1,4442 |
| 50 | 31,827 | 31,792 | 14,2401 | 14,9184 | 14,7671 |
| 100 | 43,269 | 43,369 | 21,1396 | 22,7842 | 22,5185 |
| 200 | 48,992 | 49,121 | 25,2359 | 24,9311 | 24,9113 |
| 400 | 50,082 | 49,985 | 24,2573 | 25,0000 | 24,4845 |

Desvios medidos da variância em relação à teoria: `M=2000` → máximo `+1,33` (`t=179`), mínimo
`−2,29` (`t=129`), final `−0,74`; `M=10000` → `+0,51`, `−0,99`, `−0,52`. Ruído esperado do
estimador (`calculado`): `0,79` e `0,35`. Desvio da média (`medido`): rms `0,109` e `0,039`;
esperado `0,112` e `0,050`.

Equilíbrio (`M_eq = 5000`, 10 instantes espaçados de `N+1` → 50 000 amostras):

| N | instantes | média | var | pico sim | pico esperado |
|---|---|---|---|---|---|
| 10 | 200 … 101 | 5,005 | 2,492 | 12 467 | 12 305 |
| 100 | 2000 … 1091 | 49,971 | 24,998 | 4 070 | 3 980 |

## Parte 2

`N = 1000`, `w₀ ~ U(0,2)`, `SEED = 42`.

| grandeza | valor |
|---|---|
| `E` inicial e final | 994,3557 (deriva `0,00e+00`) |
| `⟨w⟩` em todos os instantes | 0,9944 |
| `β = 1/⟨w⟩` | 1,0057 |
| colisões rejeitadas pela checagem (10⁴ passos) | **0** |
| sorteios com `i == j` (10⁴ passos) | 9 |

`L1` histograma × Boltzmann: `0,564` (t=0), `0,565` (10), `0,500` (10²), `0,204` (10³), `0,136`
(10⁴), `0,140` (10⁵). Sonda fina: `0,436` (200), `0,408` (300), `0,317` (500), `0,263` (700),
`0,154` (1500), `0,162` (2000), `0,136` (3000), `0,141` (5000) — platô em ~0,14, que é o piso de
ruído com 1000 partículas (interpretação, sustentada pelo fato de não cair de 10⁴ para 10⁵).

## Parte 3

`N = 500`, 2000 réplicas, `t_max = 2000` (`= 8τ`), `τ = N/2 = 250`.

| `m₀` | `⟨m⟩(τ)` sim | `⟨m⟩(τ)` teórico | `⟨m⟩(2000)` | `Var(2000)` sim | `Var` teórica |
|---|---|---|---|---|---|
| +1 | 0,3676 | 0,3671 | −0,0006 | 0,00199 | 0,00200 |
| +0,5 | 0,1839 | 0,1836 | +0,0001 | 0,00194 | 0,00200 |
| −0,5 | −0,1838 | −0,1836 | +0,0005 | 0,00206 | 0,00200 |
| −1 | −0,3676 | −0,3671 | +0,0006 | 0,00199 | 0,00200 |

Dependência com `N` (`m₀ = 1`): `Var(2000)` = `0,2096 / 0,0195 / 0,0020` para `N = 5 / 50 / 500`
(contra `1/N` = `0,2 / 0,02 / 0,002`); máxima variância observada `0,2204`, `0,0219`, `0,0021`.
Máxima desvio-padrão do ruído de média esperado: `1/√(N·R) = 0,001` para `N=500`.

`P(m)` estacionário (`t = 4N`, 6000 réplicas, dois últimos passos → 12 000 amostras):

| N | distintos | `σ` medido | `1/√N` | `⟨m⟩` | `χ²` vs binomial |
|---|---|---|---|---|---|
| 5 | 6 | 0,44422 | 0,44721 | +0,00067 | 1,4 (5 g.l.) |
| 50 | 27 | 0,14032 | 0,14142 | −0,00481 | 38,4 (26 g.l.) |
| 500 | 83 | 0,04507 | 0,04472 | −0,00045 | — |

Tempos de relaxação (`calculado`, `t = ln 100 / ln λ`): 1% de `m₀` em **9 / 113 / 1149** passos para
`N = 5 / 50 / 500` (`3,6τ / 4,5τ / 4,6τ`); variância a 99% do patamar em **3 / 55 / 573** passos.

## Limitações destas medidas

- **Uma semente** (`SEED = 42`), como no notebook. As diferenças entre simulação e teoria citadas
  são comparadas com o ruído esperado para aquela mesma semente, não com uma distribuição sobre
  sementes.
- O `χ²` contra a binomial **não é um teste calibrado** neste desenho: as amostras concatenadas de
  vários instantes vêm das mesmas réplicas, logo são correlacionadas. Os valores servem de
  consistência grosseira, não de `p`-valor.
- Os números de `L1` no platô dependem da largura de bin (0,125) e de `N`; são comparáveis entre
  instantes, não entre experimentos diferentes.
- `medidas.py` reproduz a *lógica* das células, não os bytes: se uma célula mudar, os números
  mudam. `numeros.txt` registra a saída da versão aqui arquivada.
