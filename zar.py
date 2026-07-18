import numpy as np
import matplotlib.pyplot as plt

# Toplam zar atma sayısı (Monte Carlo örneklem sayısı)
toplam_atis = 50000

# 1 ile 6 arasında (6 dahil) rastgele zar atışları üretiyoruz
zarlar = np.random.randint(1, 7, size=toplam_atis)

# Her atışta gelen zarın 3 olup olmadığını kontrol ediyoruz (True/False dizisi)
uc_geldi_mi = (zarlar == 3)

# Zaman içindeki olasılık gelişimini hesaplıyoruz (Kümülatif başarı / Atış sayısı)
kumulatif_uc_sayisi = np.cumsum(uc_geldi_mi)
atis_numaralari = np.arange(1, toplam_atis + 1)
olasilik_gelisimi = kumulatif_uc_sayisi / atis_numaralari

# --- GRAFİK ÇİZDİRME ---
plt.figure(figsize=(10, 5))

# Monte Carlo simülasyonunun çizdiği yol
plt.plot(atis_numaralari, olasilik_gelisimi, color='darkorange', linewidth=1.5, label='Monte Carlo Tahmini')

# Teorik olarak olması gereken gerçek çizgi (1/6)
plt.axhline(y=1/6, color='navy', linestyle='--', linewidth=2, label='Teorik Olasılık (1/6 ≈ 0.1666)')

plt.title(f"Monte Carlo Zar Simülasyonu (Son Tahmin: {olasilik_gelisimi[-1]:.4f})")
plt.xlabel("Atış Sayısı")
plt.ylabel("3 Gelme Olasılığı")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()

# Grafiğin ilk başlardaki dalgalanmasını daha iyi görmek için X eksenini logaritmik yapabiliriz
plt.xscale('log') 

plt.show()
