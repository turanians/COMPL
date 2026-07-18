import numpy as np
import matplotlib.pyplot as plt

# 1 Milyon foton fırlatıyoruz (Büyük sayı kuralımız)
N = 1000000

# Sezyum metalinin eşik enerjisi (İş fonksiyonu W0 = 2.14 eV)
W0 = 2.14

# Gelen fotonların enerjisini rastgele seçiyoruz (Görünür ışık ve UV arası: 1.0 eV ile 5.0 eV arası)
foton_enerjileri = np.random.uniform(1.0, 5.0, size=N)

# Kuantum Olasılık Fonksiyonu:
# Eğer foton enerjisi W0'dan küçükse koparma olasılığı KESİN OLARAK 0'dır.
# W0'dan büyükse, enerji arttıkça elektron koparma şansı (etkileşim ihtimali) artar (Basit bir kuantum verimlilik modeli)
koparma_olasiligi = np.where(foton_enerjileri > W0, 1 - np.exp(-(foton_enerjileri - W0)), 0)

# Monte Carlo zarlarını atıyoruz: Her foton için rastgele bir şans sayısı üretiyoruz
zar = np.random.rand(N)

# Eğer zar, o enerjideki koparma olasılığından küçükse elektron KOPTU (1), büyükse foton absorbe oldu veya yansıdı (0)
elektron_koptu_mu = (zar < koparma_olasiligi).astype(int)

# --- VERİ ANALİZİ ---
# Toplam fırlatılan 1 milyon fotondan yüzde kaçı en dıştaki elektronu koparabildi?
toplam_kopma_orani = np.mean(elektron_koptu_mu)
standart_sapma = np.std(elektron_koptu_mu)
hata_payi = standart_sapma / np.sqrt(N)

print("--- FOTOELEKTRİK MONTE CARLO SONUÇLARI ---")
print(f"Toplam Foton Sayısı        : {N}")
print(f"Genel Elektron Kopma Oranı : {toplam_kopma_orani:.5f} (Yani %{toplam_kopma_orani*100:.3f})")
print(f"Hesaplanan Hata Payı (±)   : {hata_payi:.5f}")
print("------------------------------------------")

# --- GRAFİK ÇİZDİRME (Enerjiye Karşı Kopma Olasılığı) ---
# Gerçek kuantum grafiğini görmek için veriyi görselleştirelim
plt.figure(figsize=(9, 5))
# Enerjileri küçük parçalara bölüp (binning) her enerji aralığındaki gerçek kopma oranını çizdirelim
ayrimlar = np.linspace(1.0, 5.0, 50)
kopanlar_grafik = []

for i in range(len(ayrimlar)-1):
    maske = (foton_enerjileri >= ayrimlar[i]) & (foton_enerjileri < ayrimlar[i+1])
    if np.sum(maske) > 0:
        kopanlar_grafik.append(np.mean(elektron_koptu_mu[maske]))
    else:
        kopanlar_grafik.append(0)

plt.plot(ayrimlar[:-1], kopanlar_grafik, 'o-', color='purple', label='Monte Carlo Verisi')
plt.axvline(x=W0, color='red', linestyle='--', label=f'Sezyum Eşik Enerjisi (W0 = {W0} eV)')
plt.title("Fotoelektrik Olay: Gelen Foton Enerjisine Karşı Elektron Kopma Olasılığı")
plt.xlabel("Gelen Foton Enerjisi (eV)")
plt.ylabel("Elektron Kopma Olasılığı P(Kopma)")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.show()
