# Hyper-Mirror Quantum Theory Field (HMQTF)

**Inventor:** Chutiphong Bunloed (Buriram, Thailand)  
**ORCID:** [0009-0003-4295-7521](https://orcid.org)  
**Email:** synthesis496@gmail.com  

---

## Overview

**HMQTF** is a measurement-free, passive autonomous qudit error correction framework based on open quantum systems (Lindblad master equation), non-uniform Fibonacci time modulation, anti-cascade mirror-folding symmetry, and dissipative limit cycles.

## Repository Structure

- **`hmqtf_product.py`** — Core `HMQTF` engine implementing sparse/batch Lindblad evolution, Fibonacci clock modulation, mirror-parity operators, limit-cycle dynamics, and spectral diagnostics.
- **`hmqtf_demo.py`** — Quick-start demonstrations covering single/batch evolution, infinite extensions, limit cycles, and golden-ratio convergence.
- **`hmqtf_test.py`** — 30-function unit test suite verifying algebraic invariants, trace preservation, hermiticity, and spectral bounds.
- **`hmqtf_benchmark.py`** — High-precision execution timing and dimensional scaling benchmarks (\(d = 8\) to \(128\)).

## Requirements & Quick Start

```bash
pip install numpy scipy
```

Run the demo, unit tests, or benchmarks directly:

```python
import hmqtf_demo
import hmqtf_test
import hmqtf_benchmark

print(hmqtf_test.run_all())       # Run all 30 verification tests
print(hmqtf_demo.run_all())       # Run functional demonstrations
print(hmqtf_benchmark.run())      # Run dimensional scaling benchmarks
```

## Citation

Chutiphong. (2026). synthesis496/hmqtf: update full (Version v2.2.1) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.24369802

## License

Licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.



