import numpy as np

# Sabitler (Gerçek Fizik Değerleri)
h_c = 1240  # Planck sabiti (h) ile ışık hızının (c) çarpımının eV*nm cinsinden değeri

# Sezyum metalinin eşik enerjisi (eV)
W0 = 2.14  

# 1 Milyon foton fırlatıyoruz (Büyük sayı)
N = 1000000

# Metale 300 nm (Ultraviyole) ile 800 nm (Kızılötesi) arasında rastgele dalga boylarında fotonlar gönderiyoruz
dalga_boylari = np.random.uniform(300, 800, size=N)

# Planck Formülü: E = h*c / lambda
foton_enerjileri = h_c / dalga_boylari

# Kuantum olasılığı: Enerji W0'dan büyükse koparma şansı var
kopma_olasiligi = np.where(foton_enerjileri > W0, 1 - np.exp(-(foton_enerjileri - W0)), 0)

# Monte Carlo zarı atılıyor
zar = np.random.rand(N)
elektron_koptu_mu = (zar < kopma_olasiligi).astype(int)

# --- BİLİMSEL VERİ ANALİZİ ---
kopan_elektron = np.sum(elektron_koptu_mu)
hata_payi = np.std(elektron_koptu_mu) / np.sqrt(N)

print("--- MASAL DEĞİL MATEMATİK SONUÇLARI ---")
print(f"Fırlatılan Toplam Foton: {N}")
print(f"Kopan Toplam Elektron : {kopan_elektron}")
print(f"Kopma Oranı (Olasılık) : {kopan_elektron/N:.5f} ± {hata_payi:.5f}")
print("---------------------------------------")
