"""Numerical check of the paper's Lemma 1 (AQRE of the subsidised 10-round PD).

Stage game: (T,R,P,S) = (5,3,1,0), cooperation subsidy tau. Player i's logit response to an
opponent who cooperates with probability p is f(p) = 1/(1+exp(lam*(dU(p)-tau))),
dU(p) = p(T-R) + (1-p)(P-S). A logit QRE (symmetric or not) is p1 = f(p2), p2 = f(p1),
i.e. a fixed point of the increasing composite f(f(.)). Claims checked:
  (a) |f'| <= lam/4, so for lam < 4 the composite is a contraction: one QRE at every tau;
  (b) at tau = 0 the QRE is unique at every lam on the registered grid [1e-3, 1e3];
  (c) the bound is not vacuous: for large lam some tau in the chicken range has several QRE.
"""
import numpy as np

T, R, P, S = 5, 3, 1, 0


def f(p, lam, tau):
    return 1 / (1 + np.exp(np.clip(lam * (p * (T - R) + (1 - p) * (P - S) - tau), -700, 700)))


def n_qre(lam, tau, grid=200001):
    p = np.linspace(0, 1, grid)
    s = np.sign(f(f(p, lam, tau), lam, tau) - p)
    s = s[s != 0]                       # a root exactly on a grid point is one root
    return int(np.sum(s[:-1] != s[1:]))


taus = np.linspace(-2, 6, 161)
for lam in [0.0032, 0.0075, 0.154, 0.579, 1.0, 2.0, 3.0, 3.9]:
    counts = {n_qre(lam, t) for t in taus}
    assert counts == {1}, (lam, counts)
print("(a) lam < 4: exactly one logit QRE at every tau in [-2, 6]  -- OK")
for lam in np.logspace(-3, 3, 61):
    assert n_qre(lam, 0.0) == 1, lam
print("(b) tau = 0: exactly one QRE at every lam in [1e-3, 1e3]   -- OK")
multi = [(lam, t, n_qre(lam, t)) for lam in (5, 10, 50) for t in taus if n_qre(lam, t) > 1]
print("(c) several QRE for lam >= 4, e.g.", multi[:3])
assert multi
