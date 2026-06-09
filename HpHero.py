# Fungsi Linear Naik
def linear_naik(x, a, b):
    if x <= a:
        return 0
    elif a < x < b:
        return (x - a) / (b - a)
    else:
        return 1


# Fungsi Linear Turun
def linear_turun(x, a, b):
    if x <= a:
        return 1
    elif a < x < b:
        return (b - x) / (b - a)
    else:
        return 0


# Fungsi Segitiga
def segitiga(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)
    else:
        return 0


# ===========================
# Pengujian
# ===========================

hp_hero = 35

print(f"Analisis Fuzzy HP Hero ML: {hp_hero}")

# Derajat keanggotaan
miu_rendah = linear_turun(hp_hero, 20, 40)
miu_sedang = segitiga(hp_hero, 30, 50, 70)
miu_tinggi = linear_naik(hp_hero, 60, 80)

print(f"HP Rendah : {round(miu_rendah, 2)}")
print(f"HP Sedang : {round(miu_sedang, 2)}")
print(f"HP Tinggi : {round(miu_tinggi, 2)}")


# Penentuan agresivitas
hasil = {
    "Main Aman": miu_rendah,
    "Main Normal": miu_sedang,
    "Main Barbar": miu_tinggi
}

keputusan = max(hasil, key=hasil.get)

print(f"\nKeputusan : {keputusan}")
print(f"Nilai Keyakinan : {round(hasil[keputusan], 2)}")