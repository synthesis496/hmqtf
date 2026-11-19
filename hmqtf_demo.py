#CopyRight (c)2026 Chutiphong Bunloed
#All Rights Reserved.

import numpy as np
import hmqtf_product

def demo():
p = hmqtf_product.HMQTF(d=64, gamma=0.05, C=0.0, a=-0.1, beta=1.0)
S = p.fermison(0)
result = p.run(S, n_steps=2000, dt=0.0005)
return {'purity': result['purity'], 'fermion_number': result['fermion_number'], 'stabilizer': result['stabilizer'], 'trace_error': result['trace_error'], 'spectral_gap': result['spectral_gap'], 'spectral_abscissa': result['spectral_abscissa'], 'commutator_norm': result['commutator_norm']}

def demo_batch():
p = hmqtf_product.HMQTF(d=32, gamma=0.05, C=0.0, a=-0.1, beta=1.0)
S = p.fermison_batch([0, 2, 4, 6, 8, 10, 12, 14])
rhos = p.evolve_batch(S, n_steps=1000, dt=0.0005)
return {'purity_batch': p.purity_batch(rhos).tolist(), 'fermion_batch': p.fermion_number_batch(rhos).tolist()}

def demo_infinite():
p = hmqtf_product.HMQTF(d=16, gamma=0.05)
S = p.fermison(0)
ext = p.infinite_extension(S, levels=32)
return {'extension_shape': ext.shape, 'extension_norm': float(np.linalg.norm(ext))}

def demo_limit_cycle():
p = hmqtf_product.HMQTF(d=8, a=-0.1, beta=1.0)
z0 = np.array([1 + 1j, 2 - 2j, 0.5 + 0.5j, -1 + 1j])
z_final = p.limit_cycle_batch(z0, n_steps=500)
return {'z_final_real': z_final.real.tolist(), 'z_final_imag': z_final.imag.tolist()}

def demo_fibonacci():
p = hmqtf_product.HMQTF(d=30)
return {'series': p.fib_series(15).tolist(), 'ratios': p.fib_ratio(15).tolist(), 'phi_error': p.phi_convergence(25).tolist()}

def run_all():
return {'main': demo(), 'batch': demo_batch(), 'infinite': demo_infinite(), 'limit_cycle': demo_limit_cycle(), 'fibonacci': demo_fibonacci()}

