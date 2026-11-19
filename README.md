# HMQTF

A Python numerical simulation package for studying finite-dimensional quantum-system dynamics. The repository's main `HMQTF` class creates basis states and density matrices, implements Lindblad-style evolution, computes diagnostic observables, and includes utilities related to Fibonacci sequences and limit-cycle dynamics.

> **Scope:** This README describes what the current code implements. It does not claim that the simulation has been scientifically, experimentally, or physically validated as a quantum-error-correction mechanism.

**Inventor:** Chutiphong Bunloed (Buriram, Thailand)  
**ORCID:** [0009-0003-4295-7521](https://orcid.org/0009-0003-4295-7521)  
**Email:** synthesis496@gmail.com

## Repository Structure

- `hmqtf_product.py` — the core `HMQTF` class and numerical implementation
- `hmqtf_demo.py` — demonstrations for state evolution, batching, infinite extensions, limit cycles, and Fibonacci calculations
- `hmqtf_test.py` — Boolean verification functions; `run_all()` runs the available checks
- `hmqtf_benchmark.py` — benchmark functions for operations, evolution, diagnostics, persistence, and dimension scaling

## Implemented Features

The `HMQTF` constructor accepts `d`, `gamma`, `hbar`, `tau_0`, `C`, `beta`, and `a`.

The implementation provides:

- Basis-like states through `fermison()` and batched states through `fermison_batch()`
- Pure density-matrix conversion through `state_to_density()` and `state_batch_to_density()`
- Mirror, fold, conservation, anti-cascade, mirror-state, and parity-state operations
- Fibonacci sequence generation, Fibonacci-clock Gaussian peaks, Fibonacci ratios, and convergence estimates for the golden ratio
- Finite-step Euler evolution in `evolve_fast()`
- RK45 trajectory integration through SciPy `solve_ivp()` in `evolve_accurate()`
- Batched evolution in `evolve_batch()` and multi-gamma evolution in `evolve_multi_gamma()`
- Purity, entropy, fermion number, stabilizer, trace distance, expected/effective energy, spectral, and commutator diagnostics
- Configuration serialization through `save()` and `load()`
- Independent parameter overrides through `clone()` and in-place updates through `reconfigure()`

## Installation

Python with NumPy and SciPy is required:

```bash
python -m pip install numpy scipy
```

Run the commands below from the repository root.

## Basic Example

```python
import hmqtf_product

model = hmqtf_product.HMQTF(d=8, gamma=0.05)
state = model.fermison(0)
result = model.run(state, n_steps=2000, dt=0.0005)

print("purity:", result["purity"])
print("fermion number:", result["fermion_number"])
print("trace error:", result["trace_error"])
```

Run the included demonstrations:

```bash
python -c "import hmqtf_demo; print(hmqtf_demo.run_all())"
```

Run the verification functions:

```bash
python -c "import hmqtf_test; r=hmqtf_test.run_all(); print(r); print(f'{sum(r)}/{len(r)} passed')"
```

`run_all()` in `hmqtf_test.py` returns a list of Boolean values. These are direct Python assertions/functions, not a pytest test suite.

Run the benchmark entry point:

```bash
python -c "import hmqtf_benchmark; print(hmqtf_benchmark.run())"
```

## Constructor Parameters

| Parameter | Default | Purpose |
|---|---:|---|
| `d` | `64` | Hilbert-system dimension |
| `gamma` | `0.1` | Dissipation strength |
| `hbar` | `1.0` | Effective Planck constant used in the evolution equation |
| `tau_0` | `1.0` | Scale applied to Fibonacci-clock times |
| `C` | `0.0` | Offset used in mirror/fold operations |
| `beta` | `1.0` | Imaginary coefficient in the limit-cycle update |
| `a` | `-0.1` | Real coefficient in the limit-cycle update |

## Numerical Methods

- `evolve_fast()` applies an explicit Euler update and renormalizes the trace after every step.
- `evolve_accurate()` flattens the density matrix and integrates the Lindblad right-hand side with `solve_ivp(method='RK45')`.
- `evolve_batch()` computes batch density matrices and evolution with NumPy array operations.
- `evolve_multi_gamma()` runs independent evolutions for a supplied sequence of gamma values.
- `entropy()` removes eigenvalues smaller than `1e-12` before computing the von Neumann entropy.
- `save()` stores only the constructor configuration, not the full runtime state.

## Interpretation Notes

The function names and diagnostics should be read according to their implemented calculations:

- A finite `trace_preservation_error`, `hermiticity_error`, or eigenvalue result is a numerical check, not a proof of physical fault tolerance.
- `mirror()`, `fold()`, `conserve()`, `stabilizer()`, and `anti_cascade_metric()` implement specific algebraic operations in this package; their presence does not independently establish a physical correction theorem.
- The implementation constructs a Lindblad-type jump operator using `sqrt(gamma)` and also multiplies the dissipative term by `gamma` in its evolution methods. Users should verify the intended convention before assigning a physical interpretation to gamma.
- The repository does not include a dependency manifest or packaging metadata; NumPy and SciPy must be installed manually.
- Benchmark results are hardware- and environment-dependent. This README does not present unmeasured benchmark numbers as established performance guarantees.

## Citation

Chutiphong. (2026). synthesis496/hmqtf: update full (Version v2.2.1) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.24369802

## License

GNU Affero General Public License v3.0 (AGPL-3.0). See `LICENSE` for the complete terms.
