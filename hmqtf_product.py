#CopyRight (c)2026 Chutiphong Bunloed
#All Rights Reserved.

import numpy as np
from scipy import sparse
from scipy.integrate import solve_ivp
import pickle

class HMQTF:
slots = ('_d', '_gamma', '_hbar', '_tau_0', '_C', '_beta', '_a', '_phi', '_psi', '_sqrt5', '_fib', '_fib_clock', '_I', '_M', '_L', '_LdL', '_H', '_Heff', '_P', '_config')
def __init__(self, d=64, gamma=0.1, hbar=1.0, tau_0=1.0, C=0.0, beta=1.0, a=-0.1):
    self._config = {'d': d, 'gamma': gamma, 'hbar': hbar, 'tau_0': tau_0, 'C': C, 'beta': beta, 'a': a}
    self._d = d
    self._gamma = gamma
    self._hbar = hbar
    self._tau_0 = tau_0
    self._C = C
    self._beta = beta
    self._a = a
    self._sqrt5 = float(np.sqrt(5.0))
    self._phi = (1.0 + self._sqrt5) * 0.5
    self._psi = (1.0 - self._sqrt5) * 0.5
    self._fib = self._gen_fib()
    self._fib_clock = self._fib * self._tau_0
    self._I = sparse.identity(d, format='csr', dtype=complex)
    self._M = self._build_mirror()
    self._L = self._build_lheal()
    self._LdL = (self._L.conj().T @ self._L).tocsr()
    self._H = self._build_htotal()
    self._Heff = (self._H - 1j * self._hbar * self._LdL).tocsr()
    self._P = self._build_parity()

def _gen_fib(self):
    n = np.arange(self._d)
    return np.round((self._phi ** n - self._psi ** n) / self._sqrt5).real

def _build_mirror(self):
    return sparse.csr_matrix(np.fliplr(np.eye(self._d)))

def _build_lheal(self):
    rows = np.array([0, 1, 0])
    cols = np.array([2, 3, 4])
    data = np.full(3, np.sqrt(self._gamma), dtype=complex)
    return sparse.csr_matrix((data, (rows, cols)), shape=(self._d, self._d))

def _build_htotal(self):
    return (sparse.diags(np.ones(self._d - 1), 1) + sparse.diags(np.ones(self._d - 1), -1)).astype(complex).tocsr()

def _build_parity(self):
    return sparse.diags((-1.0) ** np.arange(self._d)).astype(complex).tocsr()

def mirror(self, S):
    return self._C - S[::-1]

def fold(self, S):
    return S + self.mirror(S)

def conserve(self, S):
    return np.sum(self.fold(S))

def anti_cascade_metric(self, S):
    return np.linalg.norm(self.fold(S))

def mirror_state(self, state):
    return self._M @ np.asarray(state, dtype=complex)

def parity_state(self, state):
    return self._P @ np.asarray(state, dtype=complex)

def infinite_extension(self, S, levels=32):
    base = np.asarray(S, dtype=complex)
    drive = self._phi ** np.arange(1, levels + 1)
    mirror = self._C - base[::-1]
    return np.einsum('i,j->ij', base, drive) + np.einsum('i,j->ij', mirror, drive[::-1])

def fib_clock(self, t):
    diffs = np.abs(t - self._fib_clock)
    return np.exp(-diffs ** 2 / 1e-6)

def fib_series(self, n_terms):
    return self._fib[:n_terms].astype(int)

def fib_ratio(self, n_terms):
    f = self._fib[:n_terms]
    return f[1:] / f[:-1]

def phi_convergence(self, n_terms):
    return np.abs(self.fib_ratio(n_terms) - self._phi)

def fermison(self, n):
    s = np.zeros(self._d, dtype=complex)
    s[n % self._d] = 1.0
    return s

def fermison_batch(self, indices):
    idx = np.asarray(indices) % self._d
    S = np.zeros((len(idx), self._d), dtype=complex)
    S[np.arange(len(idx)), idx] = 1.0
    return S

def state_to_density(self, state):
    s = np.asarray(state, dtype=complex)
    return np.outer(s, s.conj())

def state_batch_to_density(self, states):
    S = np.asarray(states, dtype=complex)
    return np.einsum('bi,bj->bij', S, S.conj())

def limit_cycle(self, z0, n_steps=500):
    z = complex(z0)
    for _ in range(n_steps):
        z = np.exp((self._a + 1j * self._beta) * z)
    return z

def limit_cycle_batch(self, z0_array, n_steps=500):
    z = np.asarray(z0_array, dtype=complex).copy()
    for _ in range(n_steps):
        z = np.exp((self._a + 1j * self._beta) * z)
    return z

def _lindblad_rhs(self, t, rho_flat):
    rho = rho_flat.reshape(self._d, self._d)
    comm = self._H @ rho - rho @ self._H
    diss = self._L @ rho @ self._L.conj().T - 0.5 * (self._LdL @ rho + rho @ self._LdL)
    return ((-1j / self._hbar) * comm + self._gamma * diss).flatten()

def evolve_accurate(self, rho0, t_end=1.0, n_points=100, rtol=1e-8, atol=1e-10):
    y0 = np.asarray(rho0).flatten().astype(complex)
    t_eval = np.linspace(0.0, t_end, n_points)
    sol = solve_ivp(self._lindblad_rhs, (0.0, t_end), y0, t_eval=t_eval, method='RK45', rtol=rtol, atol=atol)
    return sol.y.T.reshape(-1, self._d, self._d)

def evolve_fast(self, rho0, n_steps=1000, dt=0.001):
    rho = np.asarray(rho0, dtype=complex).copy()
    H = self._H
    L = self._L
    LdL = self._LdL
    g = self._gamma
    inv_h = -1j / self._hbar
    for _ in range(n_steps):
        comm = H @ rho - rho @ H
        diss = L @ rho @ L.conj().T - 0.5 * (LdL @ rho + rho @ LdL)
        rho = rho + dt * (inv_h * comm + g * diss)
        rho = rho / np.trace(rho).real
    return rho

def evolve_batch(self, states, n_steps=1000, dt=0.001):
    S = np.asarray(states, dtype=complex)
    rhos = np.einsum('bi,bj->bij', S, S.conj())
    H = self._H.toarray()
    L = self._L.toarray()
    LdL = self._LdL.toarray()
    Lc = L.conj().T
    inv_h = -1j / self._hbar
    g = self._gamma
    for _ in range(n_steps):
        comm = np.einsum('ij,bjk->bik', H, rhos) - np.einsum('bij,jk->bik', rhos, H)
        LrL = np.einsum('ij,bjk,kl->bil', L, rhos, Lc)
        anti = np.einsum('ij,bjk->bik', LdL, rhos) + np.einsum('bij,jk->bik', rhos, LdL)
        rhos = rhos + dt * (inv_h * comm + g * (LrL - 0.5 * anti))
        trace = np.einsum('bii->b', rhos).real
        rhos = rhos / trace[:, None, None]
    return rhos

def evolve_multi_gamma(self, gammas, rho0, n_steps=1000, dt=0.001):
    results = []
    for g in np.asarray(gammas):
        L = self._build_lheal_g(g)
        LdL = (L.conj().T @ L).tocsr()
        rho = np.asarray(rho0, dtype=complex).copy()
        for _ in range(n_steps):
            comm = self._H @ rho - rho @ self._H
            diss = L @ rho @ L.conj().T - 0.5 * (LdL @ rho + rho @ LdL)
            rho = rho + dt * ((-1j / self._hbar) * comm + g * diss)
            rho = rho / np.trace(rho).real
        results.append(rho)
    return np.array(results)

def _build_lheal_g(self, gamma):
    rows = np.array([0, 1, 0])
    cols = np.array([2, 3, 4])
    data = np.full(3, np.sqrt(gamma), dtype=complex)
    return sparse.csr_matrix((data, (rows, cols)), shape=(self._d, self._d))

def purity(self, rho):
    return float(np.real(np.trace(rho @ rho)))

def purity_batch(self, rhos):
    return np.einsum('bij,bji->b', rhos, rhos).real

def entropy(self, rho):
    eig = np.linalg.eigvalsh(rho)
    eig = eig[eig > 1e-12]
    return float(-np.sum(eig * np.log(eig)))

def entropy_batch(self, rhos):
    eig = np.linalg.eigvalsh(rhos)
    eig = np.clip(eig, 1e-12, None)
    return -np.sum(eig * np.log(eig), axis=-1)

def fermion_number(self, rho):
    return float(np.real(np.trace(rho @ self._P)))

def fermion_number_batch(self, rhos):
    return np.einsum('bij,ji->b', rhos, self._P.toarray()).real

def stabilizer(self, rho):
    return float(np.real(np.trace(rho @ self._M)))

def trace_distance(self, rho, sigma):
    diff = rho - sigma
    eig = np.linalg.eigvalsh(diff @ diff.conj().T)
    return float(0.5 * np.sum(np.sqrt(np.clip(eig, 0.0, None))))

def expected_energy(self, rho):
    return float(np.real(np.trace(rho @ self._H.toarray())))

def expected_energy_batch(self, rhos):
    return np.einsum('bij,ji->b', rhos, self._H.toarray()).real

def effective_energy(self, rho):
    return complex(np.trace(rho @ self._Heff.toarray()))

def heff_eigenvalues(self):
    return np.linalg.eigvals(self._Heff.toarray())

def spectral_gap(self):
    eig = np.sort(np.real(np.linalg.eigvals(self._Heff.toarray())))
    return float(eig[1] - eig[0])

def spectral_abscissa(self):
    return float(np.max(np.real(np.linalg.eigvals(self._Heff.toarray()))))

def commutator_norm(self):
    return float(np.linalg.norm((self._H @ self._M - self._M @ self._H).toarray()))

def trace_preservation_error(self, rho):
    return float(np.abs(np.trace(rho).real - 1.0))

def hermiticity_error(self, rho):
    return float(np.linalg.norm(rho - rho.conj().T))

def positivity_min_eigenvalue(self, rho):
    return float(np.min(np.linalg.eigvalsh(rho)))

def diagnostics(self, rho):
    return {'purity': self.purity(rho), 'entropy': self.entropy(rho), 'fermion_number': self.fermion_number(rho), 'stabilizer': self.stabilizer(rho), 'trace': float(np.trace(rho).real), 'trace_error': self.trace_preservation_error(rho), 'hermiticity_error': self.hermiticity_error(rho), 'min_eigenvalue': self.positivity_min_eigenvalue(rho), 'spectral_gap': self.spectral_gap(), 'spectral_abscissa': self.spectral_abscissa(), 'commutator_norm': self.commutator_norm()}

def save(self, path):
    with open(path, 'wb') as f:
        pickle.dump({'config': self._config}, f)
    return path

@classmethod
def load(cls, path):
    with open(path, 'rb') as f:
        state = pickle.load(f)
    return cls(**state['config'])

def clone(self, **overrides):
    cfg = dict(self._config)
    cfg.update(overrides)
    return HMQTF(**cfg)

def reconfigure(self, **overrides):
    cfg = dict(self._config)
    cfg.update(overrides)
    self.__init__(**cfg)
    return self

def run(self, S, n_steps=2000, dt=0.0005):
    rho0 = self.state_to_density(S)
    rho_final = self.evolve_fast(rho0, n_steps=n_steps, dt=dt)
    return {'rho': rho_final, 'purity': self.purity(rho_final), 'fermion_number': self.fermion_number(rho_final), 'stabilizer': self.stabilizer(rho_final), 'trace_error': self.trace_preservation_error(rho_final), 'spectral_gap': self.spectral_gap(), 'spectral_abscissa': self.spectral_abscissa(), 'commutator_norm': self.commutator_norm()}
