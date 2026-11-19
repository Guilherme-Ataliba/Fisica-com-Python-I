"""Sonda da Parte 2: a checagem de nao-negatividade dispara? Quanto tempo ate o equilibrio?

Usa a mesma colisao do notebook (inclusive o caso i == j) e mede a distancia L1
entre o histograma de energias e a curva de Boltzmann em funcao do tempo.

    python3 sonda_p2.py
"""

import numpy as np

SEED = 42
N = 10**3

rng = np.random.default_rng(SEED)
w = rng.uniform(0, 2, N)
E0 = w.sum()
beta = 1 / w.mean()

bins = np.linspace(0, 6, 49)
centros = 0.5 * (bins[1:] + bins[:-1])
largura = bins[1] - bins[0]
f_teo = beta * np.exp(-beta * centros)

TEMPOS = {100, 200, 300, 500, 700, 1000, 1500, 2000, 3000, 5000, 10000}

L1, rejeitadas, iguais = {}, 0, 0

for t in range(1, max(TEMPOS) + 1):
    i, j = rng.integers(N, size=2)
    if i == j:
        iguais += 1
    epsilon = rng.random()
    delta_w = (1 - epsilon) * w[i] - epsilon * w[j]

    if w[i] - delta_w >= 0 and w[j] + delta_w >= 0:
        w[i] -= delta_w
        w[j] += delta_w
    else:
        rejeitadas += 1

    if t in TEMPOS:
        h, _ = np.histogram(w, bins=bins, density=True)
        L1[t] = np.abs(h - f_teo).sum() * largura

print(f"N = {N}   E0 = {E0:.4f}   <w> = {w.mean():.4f}   beta = {beta:.4f}")
print(f"colisoes rejeitadas pela checagem: {rejeitadas}")
print(f"sorteios com i == j: {iguais}")
print(f"E final = {w.sum():.4f}   deriva = {w.sum() - E0:.2e}")
print()
print("     t   t/N    L1")
for t in sorted(L1):
    print(f"{t:6d}  {t/N:4.2f}  {L1[t]:.3f}")
