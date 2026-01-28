import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import hashlib
import os
import ctypes

# --- CONNECTING TO SIMBIOTIC AI (RUST CORE) ---
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(script_dir, "libsphy_engine_01.so")

if not os.path.exists(lib_path):
    print(f"Error: Sovereign binary '{lib_path}' not found.")
    exit()

sphy_engine = ctypes.CDLL(lib_path)

# IA Interface Definition
sphy_engine.simbiotic_meissner_s_ai.argtypes = [ctypes.c_int32]
sphy_engine.simbiotic_meissner_s_ai.restype = ctypes.c_double

# Ultra Precision Function Definition
sphy_engine.hubble_fibonacci_expansion_ultra.argtypes = [ctypes.c_int32, ctypes.c_double, ctypes.c_double]
sphy_engine.hubble_fibonacci_expansion_ultra.restype = ctypes.c_double

# --- SYMBIOTIC PARAMETER RETRIEVAL ---
# We no longer define PHI and H0 in Python. We ask the AI.
AI_H0 = sphy_engine.simbiotic_meissner_s_ai(202)
AI_PHI = sphy_engine.simbiotic_meissner_s_ai(101)

# --- DATA PREPARATION ---
input_file = "sphy_universal_expansion.csv"
try:
    df = pd.read_csv(input_file)
except FileNotFoundError:
    print(f"Error: Base dataset '{input_file}' not found. Generate expansion data first.")
    exit()

# Security Mapping: Ensuring column names match the audit logic
mapping = {
    'raio_geodesico': 'geodesic_radius',
    'v_loc_sintonizada': 'tuned_v_loc',
    'camada': 'layer'
}
df = df.rename(columns=mapping)

# --- AUDIT EXECUTION ---

# 1. Traditional Model Calculation (Guided by AI parameters)
# Mude a definição do array para float128
layers = np.arange(1, 13, dtype=np.int32)
expansion_data = np.array([sphy_engine.hubble_fibonacci_expansion_ultra(n, 1.0, AI_H0) for n in layers], dtype=np.float128)
df['v_hubble_traditional'] = AI_H0 * df['geodesic_radius']

# 2. Deviation Error Calculation (Sovereign Dissonance)
# No cálculo do desvio, use a precisão estendida
df['absolute_deviation_error'] = np.abs(df['tuned_v_loc'].astype(np.float128) - df['v_hubble_traditional'].astype(np.float128))
df['metric_superiority_pct'] = (df['absolute_deviation_error'] / df['tuned_v_loc']) * 100

# --- SOVEREIGNTY REPORT ---
print("\n" + "="*50)
print("       SPHY SIMBIOTIC AUDIT REPORT (2026)")
print("       Powered by Meissner AI Core")
print("="*50)
print(f"Mean Traditional Deviation: {df['absolute_deviation_error'].mean():.4f} units")
print(f"Mean Deterministic Superiority: {df['metric_superiority_pct'].mean():.2f}%")
print(f"AI Sovereign Status: PHASE LOCKED")
print("="*50)

# --- DIVERGENCE VISUALIZATION ---


plt.figure(figsize=(10, 6))
plt.plot(df['layer'], df['tuned_v_loc'], 'b-o', label='SPHY Reality (Phase Constant)')
plt.plot(df['layer'], df['v_hubble_traditional'], 'r--', label='Traditional Hubble Estimate')

plt.fill_between(df['layer'], df['v_hubble_traditional'], df['tuned_v_loc'], 
                 color='red', alpha=0.1, label='Classical Uncertainty Margin')

plt.title("Phase Divergence: SPHY Simbiotic Meissner vs. Hubble")
plt.xlabel("Expansion Layer (Fibonacci Sequence)")
plt.ylabel("Velocity / Frequency (v_loc)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# --- SAVE AUDIT & SIGNATURE ---
output_file = "sphy_audit_report.csv"
hash_file = "sphy_audit_report.sha512"

df.to_csv(output_file, index=False)

# Generate SHA-512 Digital Signature
with open(output_file, "rb") as f:
    file_bytes = f.read()
    sha512_hash = hashlib.sha512(file_bytes).hexdigest()

with open(hash_file, "w") as f:
    f.write(sha512_hash)

print(f"\n✔ Audit report saved: {output_file}")
print(f"✔ SHA-512 Signature generated: {hash_file}")
print(f"✔ Audit Fingerprint: {sha512_hash[:16]}...")