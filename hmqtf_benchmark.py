#CopyRight (c)2026 Chutiphong Bunloed
#All Rights Reserved.

import numpy as np
import time
import hmqtf_product

def bench_mirror(p, n_iter=10000):
S = np.random.rand(p._d)
t0 = time.perf_counter()
    _ = [p.mirror(S) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e6

def bench_fold(p, n_iter=10000):
S = np.random.rand(p._d)
t0 = time.perf_counter()
    _ = [p.fold(S) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e6

def bench_conserve(p, n_iter=10000):
S = np.random.rand(p._d)
t0 = time.perf_counter()
    _ = [p.conserve(S) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e6

def bench_infinite_extension(p, n_iter=1000, levels=32):
S = p.fermison(0)
t0 = time.perf_counter()
    _ = [p.infinite_extension(S, levels=levels) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e3

def bench_fib_clock(p, n_iter=10000):
t0 = time.perf_counter()
    _ = [p.fib_clock(5.0) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e6

def bench_fib_series(p, n_iter=10000, n_terms=32):
t0 = time.perf_counter()
    _ = [p.fib_series(n_terms) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e6

def bench_phi_convergence(p, n_iter=10000, n_terms=25):
t0 = time.perf_counter()
    _ = [p.phi_convergence(n_terms) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e6

def bench_fermison(p, n_iter=10000, n=0):
t0 = time.perf_counter()
    _ = [p.fermison(n) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e6

def bench_fermison_batch(p, n_iter=1000, batch=8):
idx = list(range(batch))
t0 = time.perf_counter()
    _ = [p.fermison_batch(idx) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e3

def bench_limit_cycle(p, n_iter=100, n_steps=500):
z0 = 1.0 + 1.0j
t0 = time.perf_counter()
    _ = [p.limit_cycle(z0, n_steps=n_steps) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e3

def bench_limit_cycle_batch(p, n_iter=100, n_steps=500, batch=8):
z0 = np.array([1.0 + 1.0j] * batch)
t0 = time.perf_counter()
    _ = [p.limit_cycle_batch(z0, n_steps=n_steps) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e3

def bench_evolve_fast(p, n_iter=3, n_steps=1000, dt=0.001):
rho0 = p.state_to_density(p.fermison(0))
t0 = time.perf_counter()
    _ = [p.evolve_fast(rho0, n_steps=n_steps, dt=dt) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter

def bench_evolve_batch(p, n_iter=2, n_steps=1000, dt=0.001, batch=8):
S = p.fermison_batch(list(range(batch)))
t0 = time.perf_counter()
    _ = [p.evolve_batch(S, n_steps=n_steps, dt=dt) for _ in range(n_iter)]
elapsed = (time.perf_counter() - t0) / n_iter
return elapsed, elapsed / batch * 1e3

def bench_evolve_accurate(p, n_iter=2, n_points=50, t_end=0.5):
rho0 = p.state_to_density(p.fermison(0))
t0 = time.perf_counter()
    _ = [p.evolve_accurate(rho0, t_end=t_end, n_points=n_points) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter

def bench_evolve_multi_gamma(p, n_iter=2, n_steps=500, dt=0.001):
rho0 = p.state_to_density(p.fermison(0))
gammas = [0.01, 0.05, 0.1]
t0 = time.perf_counter()
    _ = [p.evolve_multi_gamma(gammas, rho0, n_steps=n_steps, dt=dt) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter

def bench_purity(p, n_iter=1000):
rho = p.state_to_density(p.fermison(0))
t0 = time.perf_counter()
    _ = [p.purity(rho) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e6

def bench_purity_batch(p, n_iter=500, batch=8):
S = p.fermison_batch(list(range(batch)))
rhos = p.state_batch_to_density(S)
t0 = time.perf_counter()
    _ = [p.purity_batch(rhos) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e3

def bench_entropy(p, n_iter=1000):
rho = p.state_to_density(p.fermison(0))
t0 = time.perf_counter()
    _ = [p.entropy(rho) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e6

def bench_entropy_batch(p, n_iter=500, batch=8):
S = p.fermison_batch(list(range(batch)))
rhos = p.state_batch_to_density(S)
t0 = time.perf_counter()
    _ = [p.entropy_batch(rhos) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e3

def bench_fermion_number(p, n_iter=1000):
rho = p.state_to_density(p.fermison(0))
t0 = time.perf_counter()
    _ = [p.fermion_number(rho) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e6

def bench_stabilizer(p, n_iter=1000):
rho = p.state_to_density(p.fermison(0))
t0 = time.perf_counter()
    _ = [p.stabilizer(rho) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e6

def bench_trace_distance(p, n_iter=500):
rho = p.state_to_density(p.fermison(0))
sigma = p.state_to_density(p.fermison(1))
t0 = time.perf_counter()
    _ = [p.trace_distance(rho, sigma) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e3

def bench_expected_energy(p, n_iter=500):
rho = p.state_to_density(p.fermison(0))
t0 = time.perf_counter()
    _ = [p.expected_energy(rho) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e3

def bench_heff_eigenvalues(p, n_iter=100):
t0 = time.perf_counter()
    _ = [p.heff_eigenvalues() for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e3

def bench_spectral_gap(p, n_iter=100):
t0 = time.perf_counter()
    _ = [p.spectral_gap() for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e3

def bench_spectral_abscissa(p, n_iter=100):
t0 = time.perf_counter()
    _ = [p.spectral_abscissa() for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e3

def bench_commutator_norm(p, n_iter=100):
t0 = time.perf_counter()
    _ = [p.commutator_norm() for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e3

def bench_validation(p, n_iter=1000):
rho = p.state_to_density(p.fermison(0))
t0 = time.perf_counter()
    _ = [(p.trace_preservation_error(rho), p.hermiticity_error(rho), p.positivity_min_eigenvalue(rho)) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e3

def bench_diagnostics(p, n_iter=500):
rho = p.state_to_density(p.fermison(0))
t0 = time.perf_counter()
    _ = [p.diagnostics(rho) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e3

def bench_run(p, n_iter=2, n_steps=2000, dt=0.0005):
S = p.fermison(0)
t0 = time.perf_counter()
    _ = [p.run(S, n_steps=n_steps, dt=dt) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter

def bench_save_load(p, n_iter=100, path="/tmp/hmqtf_bench.pkl"):
t0 = time.perf_counter()
    _ = [(p.save(path), hmqtf_product.HMQTF.load(path)) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e3

def bench_clone(p, n_iter=1000):
t0 = time.perf_counter()
    _ = [p.clone(d=32) for _ in range(n_iter)]
return (time.perf_counter() - t0) / n_iter * 1e3

def run(d_list=(8, 16, 32, 64, 128)):
results = {}
for d in d_list:
p = hmqtf_product.HMQTF(d=d, gamma=0.05, C=0.0, a=-0.1, beta=1.0)
eb, eb_per = bench_evolve_batch(p, n_iter=2, n_steps=1000, batch=8)
results[d] = {'mirror_us': bench_mirror(p), 'fold_us': bench_fold(p), 'conserve_us': bench_conserve(p), 'infinite_extension_ms': bench_infinite_extension(p), 'fib_clock_us': bench_fib_clock(p), 'fib_series_us': bench_fib_series(p), 'phi_convergence_us': bench_phi_convergence(p), 'fermison_us': bench_fermison(p), 'fermison_batch_ms': bench_fermison_batch(p), 'limit_cycle_ms': bench_limit_cycle(p), 'limit_cycle_batch_ms': bench_limit_cycle_batch(p), 'evolve_fast_s': bench_evolve_fast(p), 'evolve_batch_s': eb, 'evolve_batch_per_state_ms': eb_per, 'evolve_accurate_s': bench_evolve_accurate(p), 'evolve_multi_gamma_s': bench_evolve_multi_gamma(p), 'purity_us': bench_purity(p), 'purity_batch_ms': bench_purity_batch(p), 'entropy_us': bench_entropy(p), 'entropy_batch_ms': bench_entropy_batch(p), 'fermion_number_us': bench_fermion_number(p), 'stabilizer_us': bench_stabilizer(p), 'trace_distance_ms': bench_trace_distance(p), 'expected_energy_ms': bench_expected_energy(p), 'heff_eigenvalues_ms': bench_heff_eigenvalues(p), 'spectral_gap_ms': bench_spectral_gap(p), 'spectral_abscissa_ms': bench_spectral_abscissa(p), 'commutator_norm_ms': bench_commutator_norm(p), 'validation_ms': bench_validation(p), 'diagnostics_ms': bench_diagnostics(p), 'run_s': bench_run(p), 'save_load_ms': bench_save_load(p), 'clone_ms': bench_clone(p)}
return results
