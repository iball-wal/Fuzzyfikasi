import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# INPUT NILAI (bisa diubah sesuai kebutuhan)
# ============================================================

X_HP   = 25
X_GOLD = 3500

# ============================================================
# FUNGSI KEANGGOTAAN TRAPESIUM
# ============================================================

def trapesium(x, a, b, c, d):
    if x <= a:
        return 0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x <= c:
        return 1
    elif c < x < d:
        return (d - x) / (d - c)
    else:
        return 0

# ============================================================
# STEP 1 — FUZZIFIKASI
# ============================================================

print("=" * 55)
print("STEP 1 — FUZZIFIKASI")
print("=" * 55)

# a. HP Hero
print(f"\na. Nilai HP Hero = {X_HP}%\n")

mu_kritis = trapesium(X_HP, 0, 0, 20, 40)
mu_sedang = trapesium(X_HP, 20, 40, 60, 80)
mu_aman   = trapesium(X_HP, 60, 80, 100, 100)

print(f"   μ_kritis({X_HP}) = (40-{X_HP}) / (40-20) = {40-X_HP}/20 = {mu_kritis}")
print(f"   μ_sedang({X_HP}) = ({X_HP}-20) / (40-20) = {X_HP-20}/20 = {mu_sedang}")
print(f"   μ_aman({X_HP})   = 0 (diluar kurva)")

# b. Selisih Gold
print(f"\nb. Selisih Gold = {X_GOLD}\n")

mu_defisit  = trapesium(X_GOLD, -5000, -5000, -2000, 0)
mu_seimbang = trapesium(X_GOLD, -2000, 0, 0, 2000)
mu_unggul   = trapesium(X_GOLD, 0, 2000, 5000, 5000)

print(f"   μ_defisit({X_GOLD})  = 0 (diluar kurva)")
print(f"   μ_seimbang({X_GOLD}) = 0 (diluar kurva)")
print(f"   μ_unggul({X_GOLD})   = 1 (berada di antara b dan c)")

# c. Tingkat Agresivitas (Output) — rumus monoton Tsukamoto
print(f"\nc. Tingkat Agresivitas (Output):\n")
print("   μ_defensif(z) = (20-z) / (40-20),  20 ≤ z ≤ 40")
print("   μ_netral(z)   = (z-20) / (40-20),  20 ≤ z ≤ 40")
print("   μ_agresif(z)  = (z-40) / (60-40),  40 ≤ z ≤ 60")

# ============================================================
# STEP 2 — PEMBENTUKAN RULE
# ============================================================

print("\n" + "=" * 55)
print("STEP 2 — PEMBENTUKAN RULE")
print("=" * 55)

rules = [
    (1, mu_kritis, mu_defisit,  "Defensif"),
    (2, mu_kritis, mu_seimbang, "Defensif"),
    (3, mu_kritis, mu_unggul,   "Netral"),
    (4, mu_sedang, mu_defisit,  "Defensif"),
    (5, mu_sedang, mu_seimbang, "Netral"),
    (6, mu_sedang, mu_unggul,   "Agresif"),
    (7, mu_aman,   mu_defisit,  "Netral"),
    (8, mu_aman,   mu_seimbang, "Agresif"),
    (9, mu_aman,   mu_unggul,   "Agresif"),
]

print(f"\n   {'Rule':<6} {'α (MIN)':<10} {'Output'}")
print(f"   {'-'*30}")
for r, v_hp, v_gold, output in rules:
    alpha = min(v_hp, v_gold)
    print(f"   {r:<6} {alpha:<10} {output}")

# ============================================================
# STEP 3 — MESIN INFERENSI TSUKAMOTO
# ============================================================

print("\n" + "=" * 55)
print("STEP 3 — MESIN INFERENSI TSUKAMOTO")
print("=" * 55)

hasil_z = []
for r, v_hp, v_gold, output in rules:
    alpha = min(v_hp, v_gold)

    if output == "Defensif":
        # fase turun: (20-z)/(40-20) = alpha → z = 20 - alpha*(40-20)
        z = 20 - alpha * (40 - 20)
        print(f"\n   Rule {r}: Min({v_hp};{v_gold}) = {alpha}")
        print(f"   μ_defensif(z) = (20-z)/(40-20) = {alpha}  →  z{r} = {z}")

    elif output == "Netral":
        # fase naik: (z-20)/(40-20) = alpha → z = 20 + alpha*(40-20)
        z = 20 + alpha * (40 - 20)
        print(f"\n   Rule {r}: Min({v_hp};{v_gold}) = {alpha}")
        print(f"   μ_netral(z) = (z-20)/(40-20) = {alpha}  →  z{r} = {z}")

    elif output == "Agresif":
        # fase naik: (z-40)/(60-40) = alpha → z = 40 + alpha*(60-40)
        z = 40 + alpha * (60 - 40)
        print(f"\n   Rule {r}: Min({v_hp};{v_gold}) = {alpha}")
        print(f"   μ_agresif(z) = (z-40)/(60-40) = {alpha}  →  z{r} = {z}")

    hasil_z.append((r, alpha, output, z))

# ============================================================
# STEP 4 — DEFUZZIFIKASI
# ============================================================

print("\n" + "=" * 55)
print("STEP 4 — DEFUZZIFIKASI")
print("=" * 55)

# Hanya ambil rule yang aktif (alpha > 0)
aktif = [(r, a, o, z) for r, a, o, z in hasil_z if a > 0]

print("\n   1. Hitung α × z setiap rule:")
total_az = 0
total_a  = 0
for r, alpha, output, z in aktif:
    az = alpha * z
    print(f"      α{r} × z{r} = {alpha} × {z} = {az}")
    total_az += az
    total_a  += alpha

print(f"\n   2. Jumlah α × z = {total_az}")
print(f"   3. Jumlah α     = {total_a}")

z_star = total_az / total_a
print(f"\n   4. Z* = {total_az} / {total_a} = {z_star}")

print("\n" + "=" * 55)
print("   HASIL AKHIR")
print("=" * 55)
print(f"   Nilai Z* = {z_star}")
if z_star <= 40:
    print(f"   Kategori = NETRAL (20–40)")
elif z_star <= 60:
    print(f"   Kategori = AGRESIF (40–60)")
else:
    print(f"   Kategori = AGRESIF")
print("=" * 55)

# ============================================================
# VISUALISASI GRAFIK
# ============================================================

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Fuzzy Tsukamoto — Agresivitas Mobile Legends', fontsize=13, fontweight='bold')

# HP Hero
x = np.linspace(0, 100, 500)
axes[0].plot(x, [trapesium(i, 0, 0, 20, 40) for i in x],     'r',  lw=2, label='Kritis')
axes[0].plot(x, [trapesium(i, 20, 40, 60, 80) for i in x],   'g',  lw=2, label='Sedang')
axes[0].plot(x, [trapesium(i, 60, 80, 100, 100) for i in x], 'b',  lw=2, label='Aman')
axes[0].axvline(X_HP, color='black', linestyle='--', lw=1.5, label=f'X={X_HP}%')
axes[0].set_title('HP Hero')
axes[0].set_xlabel('HP (%)')
axes[0].set_ylabel('μ')
axes[0].legend()
axes[0].grid(True, linestyle='--', alpha=0.5)
axes[0].set_ylim(0, 1.1)

# Selisih Gold
x = np.linspace(-5000, 5000, 500)
axes[1].plot(x, [trapesium(i, -5000,-5000,-2000,0) for i in x], 'r',      lw=2, label='Defisit')
axes[1].plot(x, [trapesium(i, -2000,0,0,2000) for i in x],      'orange', lw=2, label='Seimbang')
axes[1].plot(x, [trapesium(i, 0,2000,5000,5000) for i in x],    'g',      lw=2, label='Unggul')
axes[1].axvline(X_GOLD, color='black', linestyle='--', lw=1.5, label=f'X={X_GOLD}')
axes[1].set_title('Selisih Gold')
axes[1].set_xlabel('Gold')
axes[1].set_ylabel('μ')
axes[1].legend()
axes[1].grid(True, linestyle='--', alpha=0.5)
axes[1].set_ylim(0, 1.1)

# Output Agresivitas (monoton Tsukamoto)
x = np.linspace(20, 60, 500)
mu_def_out = [(20 - i) / (40 - 20) if 20 <= i <= 40 else 0 for i in x]
mu_net_out = [(i - 20) / (40 - 20) if 20 <= i <= 40 else 0 for i in x]
mu_agr_out = [(i - 40) / (60 - 40) if 40 <= i <= 60 else 0 for i in x]

axes[2].plot(x, mu_def_out, 'r',      lw=2, label='Defensif')
axes[2].plot(x, mu_net_out, 'orange', lw=2, label='Netral')
axes[2].plot(x, mu_agr_out, 'g',      lw=2, label='Agresif')
axes[2].axvline(z_star, color='black', linestyle='--', lw=2, label=f'Z*={z_star}')
axes[2].set_title('Output Tingkat Agresivitas')
axes[2].set_xlabel('Agresivitas')
axes[2].set_ylabel('μ')
axes[2].legend()
axes[2].grid(True, linestyle='--', alpha=0.5)
axes[2].set_ylim(0, 1.1)

plt.tight_layout()
plt.savefig('fuzzy_tsukamoto_hasil.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nGrafik disimpan: fuzzy_tsukamoto_hasil.png")