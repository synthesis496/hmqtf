#Copyright © 2026 Chutiphong Bunloed
#All Rights Reserved.

import numpy as np
import hmqtf_product

def t_mirror():
p = hmqtf_product.HMQTF(d=8, C=0.0)
S = np.array([1, 0, 0, 0, 1, 1, 1, 0], dtype=complex)
return bool(np.allclose(S + p.mirror(S), 0))

def t_fold():
p = hmqtf_product.HMQTF(d=16, C=0.0)
S = np.random.rand(16)
return bool(np.allclose(p.fold(S), 0))

def t_conserve():
p = hmqtf_product.HMQTF(d=32, C=0.0)
S = np.random.rand(32)
return bool(np.isclose(p.conserve(S), 0))

def t_fib_sequence():
p = hmqtf_product.HMQTF(d=12)
expected = np.array([1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144])
return bool(np.allclose(p._fib, expected))

def t_phi_convergence():
p = hmqtf_product.HMQTF(d=30)
err = p.phi_convergence(25)
return bool(err[-1] < 1e-6)

def t_fermison_norm():
p = hmqtf_product.HMQTF(d=16)
norms = [np.linalg.norm(p.fermison(n)) for n in [0, 3, 7, 15]]
return bool(np.allclose(norms, 1.0))

def t_fermison_orthogonal():
p = hmqtf_product.HMQTF(d=8)
return bool(np.isclose(np.vdot(p.fermison(2), p.fermison(5)), 0.0))

def t_fermison_batch():
p = hmqtf_product.HMQTF(d=16)
S = p.fermison_batch([1, 3, 5, 7])
return bool(S.shape == (4, 16) and np.allclose(np.linalg.norm(S, axis=1), 1.0))

def t_limit_cycle():
p = hmqtf_product.HMQTF(d=8, a=-0.1, beta=1.0)
z = p.limit_cycle(1.0 + 1.0j, n_steps=500)
return bool(np.isfinite(z))

def t_limit_cycle_batch():
p = hmqtf_product.HMQTF(d=8, a=-0.1, beta=1.0)
z0 = np.array([1 + 1j, 2 + 2j, 0.5 + 0.5j])
z = p.limit_cycle_batch(z0, n_steps=300)
return bool(z.shape == (3,) and np.all(np.isfinite(z)))

def t_evolve_fast():
p = hmqtf_product.HMQTF(d=8, gamma=0.01)
rho0 = p.state_to_density(p.fermison(0))
rho = p.evolve_fast(rho0, n_steps=500, dt=0.001)
return bool(np.isclose(np.trace(rho).real, 1.0, atol=1e-6))

def t_evolve_accurate():
p = hmqtf_product.HMQTF(d=8, gamma=0.01)
rho0 = p.state_to_density(p.fermison(0))
rhos = p.evolve_accurate(rho0, t_end=0.5, n_points=20)
return bool(rhos.shape == (20, 8, 8))

def t_evolve_batch():
p = hmqtf_product.HMQTF(d=8, gamma=0.01)
S = p.fermison_batch([0, 2, 4])
rhos = p.evolve_batch(S, n_steps=200, dt=0.001)
return bool(rhos.shape == (3, 8, 8))

def t_purity():
p = hmqtf_product.HMQTF(d=8, gamma=0.01)
rho = p.state_to_density(p.fermison(3))
return bool(np.isclose(p.purity(rho), 1.0))

def t_entropy():
p = hmqtf_product.HMQTF(d=8, gamma=0.01)
rho = p.state_to_density(p.fermison(2))
return bool(np.isclose(p.entropy(rho), 0.0, atol=1e-10))

def t_fermion_number():
p = hmqtf_product.HMQTF(d=8)
rho = p.state_to_density(p.fermison(3))
return bool(np.isclose(abs(p.fermion_number(rho)), 1.0))

def t_commutator():
p = hmqtf_product.HMQTF(d=8)
return bool(np.isfinite(p.commutator_norm()))

def t_spectral_gap():
p = hmqtf_product.HMQTF(d=8, gamma=0.1)
return bool(np.isfinite(p.spectral_gap()))

def t_spectral_abscissa():
p = hmqtf_product.HMQTF(d=8, gamma=0.5, a=-0.1)
return bool(np.isfinite(p.spectral_abscissa()))

def t_save_load():
p = hmqtf_product.HMQTF(d=8)
path = "/tmp/hmqtf_test.pkl"
p.save(path)
p2 = hmqtf_product.HMQTF.load(path)
return bool(p2._d == 8)

def t_clone():
p = hmqtf_product.HMQTF(d=8, gamma=0.1)
p2 = p.clone(d=16, gamma=0.2)
return bool(p2._d == 16 and p._d == 8)

def t_fib_clock():
p = hmqtf_product.HMQTF(d=20, tau_0=1.0)
t_peak = p._fib_clock[5]
return bool(p.fib_clock(t_peak) > p.fib_clock(t_peak + 0.5))

def t_trace_distance():
p = hmqtf_product.HMQTF(d=8)
rho = p.state_to_density(p.fermison(1))
return bool(np.isclose(p.trace_distance(rho, rho), 0.0, atol=1e-10))

def t_stabilizer():
p = hmqtf_product.HMQTF(d=8, C=0.0)
rho = p.state_to_density(p.fermison(0))
return bool(np.isfinite(p.stabilizer(rho)))

def t_heff_eigenvalues():
p = hmqtf_product.HMQTF(d=8, gamma=0.1)
return bool(p.heff_eigenvalues().shape == (8,))

def t_infinite_extension():
p = hmqtf_product.HMQTF(d=8)
S = p.fermison(0)
ext = p.infinite_extension(S, levels=16)
return bool(ext.shape == (8, 16))

def t_diagnostics():
p = hmqtf_product.HMQTF(d=8, gamma=0.01)
rho = p.state_to_density(p.fermison(0))
d = p.diagnostics(rho)
keys = {'purity', 'entropy', 'fermion_number', 'stabilizer', 'trace', 'trace_error', 'hermiticity_error', 'min_eigenvalue', 'spectral_gap', 'spectral_abscissa', 'commutator_norm'}
return bool(keys.issubset(d.keys()))

def t_run():
p = hmqtf_product.HMQTF(d=8, gamma=0.01)
S = p.fermison(0)
res = p.run(S, n_steps=200, dt=0.001)
return bool('rho' in res and 'purity' in res)

def t_expected_energy():
p = hmqtf_product.HMQTF(d=8)
rho = p.state_to_density(p.fermison(2))
return bool(np.isfinite(p.expected_energy(rho)))

def t_effective_energy():
p = hmqtf_product.HMQTF(d=8)
rho = p.state_to_density(p.fermison(2))
return bool(np.isfinite(np.abs(p.effective_energy(rho))))

def run_all():
tests = [t_mirror, t_fold, t_conserve, t_fib_sequence, t_phi_convergence, t_fermison_norm, t_fermison_orthogonal, t_fermison_batch, t_limit_cycle, t_limit_cycle_batch, t_evolve_fast, t_evolve_accurate, t_evolve_batch, t_purity, t_entropy, t_fermion_number, t_commutator, t_spectral_gap, t_spectral_abscissa, t_save_load, t_clone, t_fib_clock, t_trace_distance, t_stabilizer, t_heff_eigenvalues, t_infinite_extension, t_diagnostics, t_run, t_expected_energy, t_effective_energy]
return [t() for t in tests]
