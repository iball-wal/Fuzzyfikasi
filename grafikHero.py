import numpy as np
import matplotlib.pyplot as plt


hp = np.linspace(0, 100, 500)

def kurva_trapesium(x, a, b, c, d):
    res = np.zeros_like(x)

    # Kondisi Naik
    naik = (x >= a) & (x < b)
    if b > a:
        res[naik] = (x[naik] - a) / (b - a)

    # Kondisi Puncak
    puncak = (x >= b) & (x <= c)
    res[puncak] = 1
 
    # Kondisi Turun
    turun = (x > c) & (x <= d)
    if d > c:
        res[turun] = (d - x[turun]) / (d - c)

    return res


# ============================================================
#   Kritis : a=0,  b=0,  c=20, d=40
#   Sedang : a=20, b=40, c=60, d=80
#   Aman   : a=60, b=80, c=100, d=100
# ============================================================

mu_kritis = kurva_trapesium(hp, 0,  0,  20, 40)
mu_sedang = kurva_trapesium(hp, 20, 40, 60, 80)
mu_aman   = kurva_trapesium(hp, 60, 80, 100, 100)


# ============================================================
# VISUALISASI GRAFIK
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(hp, mu_kritis, "b", linewidth=2.5, label="Kritis (0-40)")
plt.plot(hp, mu_sedang, "g", linewidth=2.5, label="Sedang (20-80)")
plt.plot(hp, mu_aman,   "r", linewidth=2.5, label="Aman (60-100)")

plt.title(
    "Grafik Fungsi Keanggotaan HP Hero\nMobile Legends: Bang Bang",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("HP Hero (%)", fontsize=12)
plt.ylabel(r"Derajat Keanggotaan ($\mu$)", fontsize=12)
plt.legend()
plt.grid(True, linestyle="--", alpha=0.7)

plt.xlim(0, 100)
plt.ylim(0, 1.1)

plt.tight_layout()
plt.savefig(r'D:\UNSULBAR24\SEMESTER 4\KECERDASAN BUATAN\Dosen 2\Fuuz Keanggotaan\grafik_fuzzy_hp_hero_trapesium.png', dpi=150, bbox_inches='tight')
plt.show()