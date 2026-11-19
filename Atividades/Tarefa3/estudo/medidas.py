"""Reproduz o codigo exato das celulas do notebook e registra os numeros usados no documento."""
from pathlib import Path

import numpy as np
from scipy.stats import binom, norm

SEED = 42


# ---------- PARTE 1 ----------
def ehrenfest(N, m0, t_max, M, seed=SEED):
    rng = np.random.default_rng(seed)
    m = np.empty((t_max + 1, M), dtype=np.int32)
    m[0] = m0
    for t in range(t_max):
        sorteou_A = rng.random(M) < m[t] / N
        m[t + 1] = m[t] + np.where(sorteou_A, -1, 1)
    return m


def media_teorica(N, m0, t):
    return N / 2 + (m0 - N / 2) * (1 - 2 / N) ** t


def variancia_teorica(N, m0, t):
    x0 = m0 - N / 2
    return N / 4 + (x0**2 - N / 4) * (1 - 4 / N) ** t - x0**2 * (1 - 2 / N) ** (2 * t)


out = []
out.append("# Numeros medidos (reproducao das celulas do notebook, SEED = 42)\n")

# 1.1 momentos
N, m0, t_max = 100, 0, 400
t = np.arange(t_max + 1)
res = {}
for M in (2000, 10000):
    tr = ehrenfest(N, m0, t_max, M)
    res[M] = (tr.mean(axis=1), tr.var(axis=1))
    out.append(f"## P1 momentos: N={N}, m0={m0}, M={M}")
    for tt in (0, 10, 50, 100, 200, 400):
        out.append(
            f"  t={tt:4d}  media_sim={res[M][0][tt]:.3f} teoria={media_teorica(N,m0,tt):.3f}"
            f"  var_sim={res[M][1][tt]:.4f} var_teo={variancia_teorica(N,m0,tt):.4f}"
        )
    out.append(f"  ruido esperado da variancia amostral = Var*sqrt(2/(M-1)) = {25*np.sqrt(2/(M-1)):.3f}")
    out.append("")

# 1.2 equilibrio
M_eq = 5000
Ns = [10, 100]
out.append("## P1 equilibrio")
equilibrio = {}
for N in Ns:
    tr = ehrenfest(N, 0, 20 * N, M_eq)
    instantes = np.arange(20 * N, 10 * N, -(N + 1))
    amostras = np.concatenate([tr[tt] for tt in instantes])
    equilibrio[N] = amostras
    out.append(f"  N={N}: instantes={instantes.tolist()} (n={len(instantes)}) amostras={len(amostras)}")
    ks = np.arange(N + 1)
    cont = np.bincount(amostras, minlength=N + 1)
    esp = len(amostras) * binom.pmf(ks, N, 0.5)
    chi2 = ((cont - esp) ** 2 / esp).sum()
    out.append(f"    chi2={chi2:.1f}  gl={N}  chi2/gl={chi2/N:.3f}  (esperado ~1)")
    out.append(f"    media={amostras.mean():.3f} (N/2={N/2})  var={amostras.var():.3f} (N/4={N/4})")
    out.append(f"    pico contagem={cont.max()}  esperado={esp.max():.1f}")
out.append("")

# ---------- PARTE 2 ----------
def colisao(w, rng):
    i, j = rng.integers(len(w), size=2)
    epsilon = rng.random()
    delta_w = (1 - epsilon) * w[i] - epsilon * w[j]
    if w[i] - delta_w >= 0 and w[j] + delta_w >= 0:
        w[i] -= delta_w
        w[j] += delta_w


def simular(w, tempos, rng):
    amostras = {0: w.copy()}
    for tt in range(1, tempos[-1] + 1):
        colisao(w, rng)
        if tt in tempos:
            amostras[tt] = w.copy()
    return amostras


N2 = 10**3
rng = np.random.default_rng(SEED)
w = rng.uniform(0, 2, N2)
TEMPOS = [0, 10, 100, 1_000, 10_000, 100_000]
amostras = simular(w, TEMPOS, rng)
beta = 1 / amostras[TEMPOS[-1]].mean()
out.append("## P2")
out.append(f"  E_total inicial={994.3557:.4f} (do print da celula)  E_final={amostras[TEMPOS[-1]].sum():.4f}")
out.append(f"  <w> inicial={w.mean():.4f}  <w> final={amostras[TEMPOS[-1]].mean():.4f}  beta={beta:.4f}")
out.append(f"  beta da condicao inicial (1/1) = {1/w.mean():.4f}")
grid = np.linspace(0, 6, 400)
for tt in TEMPOS:
    a = amostras[tt]
    h, edges = np.histogram(a, bins=np.linspace(0, 6, 49), density=True)
    c = 0.5 * (edges[1:] + edges[:-1])
    f = beta * np.exp(-beta * c)
    l1 = np.abs(h - f).sum() * (edges[1] - edges[0])
    out.append(f"  t={tt:6d}  E={a.sum():.4f}  <w>={a.mean():.4f}  L1(hist,Boltzmann)={l1:.3f}")
out.append("")

# ---------- PARTE 3 ----------
def simular3(N, m0, t_max, replicas, seed=SEED):
    rng = np.random.default_rng(seed)
    n_up = int(round(N * (1 + m0) / 2))
    s = np.full((N, replicas), -1)
    s[:n_up] = 1
    magnetizacao = np.empty((t_max + 1, replicas))
    magnetizacao[0] = s.sum(axis=0)
    colunas = np.arange(replicas)
    for tt in range(t_max):
        i = rng.integers(N, size=replicas)
        magnetizacao[tt + 1] = magnetizacao[tt] - 2 * s[i, colunas]
        s[i, colunas] *= -1
    return magnetizacao


def mag_media(N, m0, t):
    return m0 * (1 - 2 / N) ** t


def mag_var(N, m0, t):
    return 1 / N + (m0**2 - 1 / N) * (1 - 4 / N) ** t - m0**2 * (1 - 2 / N) ** (2 * t)


N3, REP, T3 = 500, 2000, 2000
out.append("## P3 momentos (N=500, 2000 replicas, t_max=2000)")
for m0 in (1, 0.5, -0.5, -1):
    m = simular3(N3, m0, T3, REP) / N3
    media, var = m.mean(axis=1), m.var(axis=1)
    out.append(f"  m0={m0:+.1f}: media(250)={media[250]:.4f} teo={mag_media(N3,m0,250):.4f}"
               f" | media(2000)={media[2000]:+.4f} | var(2000)={var[2000]:.5f} teo={mag_var(N3,m0,2000):.5f}")
out.append(f"  tau=N/2={N3/2}  1/N={1/N3}  1/sqrt(N)={1/np.sqrt(N3):.4f}")
out.append("")

out.append("## P3 dependencia com N (m0=1, 2000 replicas)")
for N in (5, 50, 500):
    m = simular3(N, 1, T3, REP) / N
    media, var = m.mean(axis=1), m.var(axis=1)
    out.append(f"  N={N:3d}: media(10)={media[10]:+.4f} teo={mag_media(N,1,10):.4f}"
               f" | media(2000)={media[2000]:+.4f} | var(2000)={var[2000]:.5f} | 1/N={1/N:.5f}")
    out.append(f"          var max={var.max():.5f} em t={var.argmax()}")
out.append("")

out.append("## P3 P(m) estacionario (t=4N, 6000 replicas, dois ultimos passos)")
for N in (5, 50, 500):
    a = simular3(N, 1, 4 * N, 6000)[-2:].ravel() / N
    out.append(f"  N={N:3d}: n={a.size}  media={a.mean():+.5f}  std={a.std():.5f}  1/sqrt(N)={1/np.sqrt(N):.5f}")
    vals, cont = np.unique(np.round(a, 6), return_counts=True)
    out.append(f"          valores distintos={vals.size} (2N+1={2*N+1})  exemplo={vals[:6].tolist()}")
    if N <= 50:
        k = np.round((vals + 1) * N / 2).astype(int)
        p = binom.pmf(k, N, 0.5) * a.size
        chi2 = ((cont - p) ** 2 / p).sum()
        out.append(f"          chi2 vs Binomial({N},1/2)={chi2:.1f} gl={vals.size-1}")
out.append("")

saida = Path(__file__).with_name("numeros.txt")
saida.write_text("\n".join(out))
print("\n".join(out))
print(f"\n[gravado em {saida}]")
