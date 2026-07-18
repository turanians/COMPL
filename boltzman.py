import numpy as np
import matplotlib.pyplot as plt

# --- 1. Sabitler ve Enerji Aralığı ---
Ef = 1.0  # Fermi Enerji Seviyesi (Örn: 1.0 eV)
kB = 8.617333e-5  # eV/K cinsinden Boltzmann sabiti

# 0 ile 2 eV arasında 1000 farklı enerji noktası oluşturalım
E = np.linspace(0, 2.0, 1000)

# --- 2. Fermi-Dirac Fonksiyonu ---
def fermi_dirac(E, T, Ef):
    if T == 0:
        # Mutlak sıfırda (0 K) Ef'nin altı %100 dolu (1), üstü %0 doludur (0)
        return np.where(E < Ef, 1.0, 0.0)
    else:
        # T > 0 için standart Fermi-Dirac formülü
        return 1 / (np.exp((E - Ef) / (kB * T)) + 1)

# --- 3. Senaryoları Hesapla ---
f_0K = fermi_dirac(E, 0, Ef)       # Mutlak Sıfır (Buz gibi düzen)
f_300K = fermi_dirac(E, 300, Ef)   # Oda Sıcaklığı (Yumuşama başlıyor)
f_1500K = fermi_dirac(E, 1500, Ef) # Yüksek Sıcaklık (İyice gevşeyen düzen)

# --- 4. Grafik Çizimi ---
plt.figure(figsize=(10, 6))

plt.plot(E, f_0K, label='Mutlak Sıfır (0 K)', color='black', linewidth=3, linestyle='--')
plt.plot(E, f_300K, label='Oda Sıcaklığı (300 K)', color='forestgreen', linewidth=2)
plt.plot(E, f_1500K, label='Yüksek Sıcaklık (1500 K)', color='darkorange', linewidth=2)

# Tam Fermi seviyesindeki %50 olasılık noktasını işaretleyelim
plt.scatter([Ef], [0.5], color='red', s=100, zorder=5, label='Sabit Nokta (Olasılık = 0.5)')

# Grafik Süslemeleri
plt.title('Fermi-Dirac Dağılımı: Sıcaklığın Kuantum Düzenine Etkisi', fontsize=14, fontweight='bold')
plt.xlabel('Enerji (E) [eV]', fontsize=12)
plt.ylabel('Doluluk Olasılığı f(E)', fontsize=12)
plt.axvline(Ef, color='gray', linestyle=':', alpha=0.7)
plt.text(Ef + 0.02, 0.1, 'Fermi Enerjisi (Ef)', color='gray', fontsize=10)

plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=11)
plt.ylim(-0.05, 1.05)

plt.show()
