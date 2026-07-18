import numpy as np
import matplotlib.pyplot as plt

# --- 1. SİMÜLASYON PARAMETRELERİ (Genişletilmiş Aralık: 20-110 Derece) ---
# Cihaz hassasiyeti için 0.1 derece adımlarla 901 veri noktası tarıyoruz
two_theta = np.linspace(20, 110, 901)

# Kübik NiO için 20° ile 110° arasındaki TÜM karakteristik Miller indeksleri ve pikleri
pikler = {
    37.2: {'hkl': '(111)', 'intensity': 60},
    43.3: {'hkl': '(200)', 'intensity': 100}, # En güçlü ana karakteristik pik
    62.9: {'hkl': '(220)', 'intensity': 75},
    75.4: {'hkl': '(311)', 'intensity': 15},
    79.4: {'hkl': '(222)', 'intensity': 12},
    96.4: {'hkl': '(400)', 'intensity': 16}, # Yüksek açılı yeni pik
    108.4: {'hkl': '(420)', 'intensity': 9}   # Yüksek açılı yeni zayıf pik
}

fwhm_termal = 0.4 
y_saf = np.zeros_like(two_theta)

# --- 2. FİZİKSEL MODELLEME (Debye-Waller ve Gauss Profili) ---
for center, info in pikler.items():
    # Debye-Waller Etkisi: Yüksek açılarda termal titreşimin piki baskılaması
    titresim_baskisi = np.exp(-0.001 * (center**2)) 
    efektif_siddet = info['intensity'] * titresim_baskisi
    
    # Matematiksel Gauss Kırınım Eğrisi
    pik_sinyali = efektif_siddet * np.exp(-0.5 * ((two_theta - center) / (fwhm_termal / 2.355))**2)
    y_saf += pik_sinyali

# Cihazın okuduğu stabil taban sinyali
y_saf += 0.1

# --- 3. ELİT VE TEMİZ GRAFİK TASARIMI (CORPORATE LIGHT) ---
plt.figure(figsize=(12, 6), facecolor='#ffffff')
ax = plt.gca()
ax.set_facecolor('#ffffff')

# Kurumsal Lacivert Çizgi ile XRD Datası
plt.plot(two_theta, y_saf, color='#1e3a8a', lw=1.5, label='Filtrelenmiş XRD Tarama Verisi (20 kV)')

# Miller İndekslerini (hkl) İlgili Piklerin Tepesine Yazdırma
for center, info in pikler.items():
    idx = np.argmin(np.abs(two_theta - center))
    plt.text(center, y_saf[idx] + 3, info['hkl'], 
             ha='center', va='bottom', fontsize=9, color='#1e293b', fontweight='bold')

# Grafik Giydirmeleri ve Modern Dokunuşlar
plt.title("Kübik Nikel Oksit (NiO) Genişletilmiş Toz XRD Spektrumu (20° - 110°)", color='#0f172a', fontsize=13, fontweight='bold', pad=20)
plt.xlabel("Kırınım Açısı 2θ (Derece)", color='#475569', fontsize=10, labelpad=10)
plt.ylabel("Şiddet / Yoğunluk (A.U.)", color='#475569', fontsize=10, labelpad=10)

# Eksen çizgilerini sadeleştirme
for spine in ax.spines.values():
    spine.set_color('#cbd5e1')

ax.tick_params(colors='#475569', labelsize=9)
ax.grid(True, color='#f1f5f9', linestyle='-', lw=1.5) # İnce hafif kılavuz çizgileri

plt.xlim(20, 110)
plt.ylim(0, 115)
plt.legend(facecolor='#ffffff', edgecolor='#cbd5e1', loc='upper right', fontsize=10)

plt.tight_layout()
print("20°-110° Geniş Tarama Grafiği Başarıyla Üretildi.")
plt.show()
