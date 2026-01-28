import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ctypes
import os
import hashlib

# --- SOVEREIGN CORE LOADING (RUST FFI) ---
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(script_dir, "libsphy_engine.so")

if not os.path.exists(lib_path):
    raise FileNotFoundError(f"Binary not found at: {lib_path}")

sphy_engine = ctypes.CDLL(lib_path)

# FFI Type Definitions
sphy_engine.calcular_incerteza_sphy.argtypes = [ctypes.c_double]
sphy_engine.calcular_incerteza_sphy.restype = ctypes.c_double

sphy_engine.hubble_fibonacci_expansion.argtypes = [ctypes.c_int32, ctypes.c_double, ctypes.c_double]
sphy_engine.hubble_fibonacci_expansion.restype = ctypes.c_double

class SPHYUniverse:
    def __init__(self):
        self.phi = (1 + 5**0.5) / 2
        self.h0 = 70.0      # Hubble Constant
        self.gamma = 1.0    # Gravitational Circulation Factor
        self.s_limit = 0.905842

    def simulate(self, points=500):
        s_range = np.linspace(0, 1.2, points)
        
        # 1. Uncertainty Depletion (Heisenberg vs SPHY Core)
        heisenberg_noise = [0.5 + np.random.normal(0, 0.05) for _ in s_range]
        sphy_deterministic = [sphy_engine.calcular_incerteza_sphy(s) for s in s_range]

        # 2. Geodesic Expansion (Hubble-Fibonacci Core)
        layers = np.arange(1, 13, dtype=np.int32)
        radii = [sphy_engine.hubble_fibonacci_expansion(n, self.gamma, self.h0) for n in layers]

        return s_range, heisenberg_noise, sphy_deterministic, layers, radii

# --- EXECUTION & VISUALIZATION ---
universe = SPHYUniverse()
s_range, noise, clean_data, layers, expansion = universe.simulate()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Uncertainty Depletion
ax1.plot(s_range, noise, 'r--', alpha=0.3, label='Scissor Operator (Heisenberg)')
ax1.plot(s_range, clean_data, 'b-', linewidth=2, label='SPHY Engine (Sovereign Phase)')
ax1.axvline(x=universe.s_limit, color='gold', linestyle=':', label='Golden S-Limit')
ax1.set_yscale('log')
ax1.set_title("Uncertainty Depletion via SPHY Sovereign Core")
ax1.set_xlabel("Sovereign Synchrony (S)")
ax1.set_ylabel("Uncertainty Magnitude (Δx · Δp)")
ax1.legend()

# Plot 2: Hubble-Fibonacci Expansion
ax2.stem(layers, expansion, linefmt='g-', markerfmt='go', basefmt=" ")
ax2.set_title("Geodesic Expansion: Hubble-Fibonacci Sequence")
ax2.set_xlabel("Fibonacci Layer (n)")
ax2.set_ylabel("Geodesic Radius (Rn)")

plt.tight_layout()
plt.show()

# --- EXPORT & SHA-512 SIGNATURE ---
csv_filename = "sphy_sovereign_proof.csv"
hash_filename = "sphy_sovereign_proof.sha512"

df_proof = pd.DataFrame({
    'layer': layers,
    'geodesic_radius': expansion,
    'tuned_v_loc': [universe.h0 * universe.phi for _ in layers]
})

# Save CSV
df_proof.to_csv(csv_filename, index=False)

# Generate SHA-512 Hash
with open(csv_filename, "rb") as f:
    file_bytes = f.read()
    sha512_hash = hashlib.sha512(file_bytes).hexdigest()

# Save Hash Signature
with open(hash_filename, "w") as f:
    f.write(sha512_hash)

print(f"\n{'='*50}")
print(f"✔ SPHY Motor Integration: SUCCESSFUL")
print(f"✔ Proof Dataset Generated: {csv_filename}")
print(f"✔ SHA-512 Signature Created: {hash_filename}")
print(f"✔ Digital Fingerprint: {sha512_hash[:16]}...{sha512_hash[-16:]}")
print(f"{'='*50}\n")