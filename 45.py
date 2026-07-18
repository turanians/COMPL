import numpy as np
import matplotlib.pyplot as plt

# --- 1. KRİSTAL PARAMETRELERİ & KOORDİNATLARIN TANIMLANMASI ---
# Kafes parametresi a = 0.417 nm. FCC yapısında atomların birim hücre içi konumları:
KAFES_SABITI = 0.417  # nm

# Kesirsel Koordinatlar (Fractional Coordinates)
# Nikel (Ni) atomları FCC köşe ve yüzey merkezlerinde yer alır
ni_koordinatlar = np.array([
    [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0],
    [1.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 1.0], # Köşeler
    [0.5, 0.5, 0.0], [0.5, 0.0, 0.5], [0.0, 0.5, 0.5],                  # Alt/Ön/Sol yüzey merkezleri
    [0.5, 0.5, 1.0], [0.5, 1.0, 0.5], [1.0, 0.5, 0.5]                   # Üst/Arka/Sağ yüzey merkezleri
])

# Oksijen (O) atomları oktahedral boşluklarda (kenar merkezleri ve tam merkezde) yer alır
o_koordinatlar = np.array([
    [0.5, 0.5, 0.5],                                                     # Tam iç merkez
    [0.5, 0.0, 0.0], [0.0, 0.5, 0.0], [0.0, 0.0, 0.5],                  # Eksen kenar merkezleri
    [1.0, 0.5, 0.0], [1.0, 0.0, 0.5], [0.5, 1.0, 0.0],
    [0.0, 1.0, 0.5], [0.5, 0.0, 1.0], [0.0, 0.5, 1.0],
    [1.0, 1.0, 0.5], [1.0, 0.5, 1.0], [0.5, 1.0, 1.0]                   # Diğer kenar merkezleri
])

# --- 2. 3D KRİSTAL GRAFİK TASARIMI (CORPORATE LIGHT) ---
fig = plt.figure(figsize=(13, 6), facecolor='#ffffff')

# Sol Taraf: 3 Boyutlu Birim Hücre Çizimi
ax_3d = fig.add_subplot(121, projection='3d')
ax_3d.set_facecolor('#ffffff')

# Nikel Atomlarını Çiz (Asil Metalik Yeşil - Büyük Küreler)
ax_3d.scatter(ni_koordinatlar[:,0], ni_koordinatlar[:,1], ni_koordinatlar[:,2], 
              s=180, color='#059669', edgecolors='#047857', alpha=0.9, label='Nikel ($Ni^{2+}$)')

# Oksijen Atomlarını Çiz (Kurumsal Canlı Mavi - Orta Küreler)
ax_3d.scatter(o_koordinatlar[:,0], o_koordinatlar[:,1], o_koordinatlar[:,2], 
              s=120, color='#0284c7', edgecolors='#0369a1', alpha=0.9, label='Oksijen ($O^{2-}$)')

# Kübik Birim Hücre Çerçeve Çizgilerini Çizme
cerceve_noktalari = [0, 1]
for x in cerceve_noktalari:
    for y in cerceve_noktalari:
        ax_3d.plot([x, x], [y, y], [0, 1], color='#cbd5e1', linestyle='-', lw=1.2)
        ax_3d.plot([x, x], [0, 1], [y, y], color='#cbd5e1', linestyle='-', lw=1.2)
        ax_3d.plot([0, 1], [x, x], [y, y], color='#cbd5e1', linestyle='-', lw=1.2)

# 3D Eksen Ayarları
ax_3d.set_title("NiO Birim Hücre Yapısı (Kübik FCC)", color='#0f172a', fontsize=12, fontweight='bold', pad=10)
ax_3d.set_xlabel("X Ekseni (Kesirsel)", color='#475569', fontsize=9)
ax_3d.set_ylabel("Y Ekseni (Kesirsel)", color='#475569', fontsize=9)
ax_3d.set_zlabel("Z Ekseni (Kesirsel)", color='#475569', fontsize=9)
ax_3d.view_init(elev=20, azim=45) # En net kristal açısı
ax_3d.legend(loc='upper left', frameon=True, facecolor='#ffffff', edgecolor='#cbd5e1', fontsize=9)

# Sağ Taraf: hkl Düzlemleri ve Karakterizasyon Bilgi Paneli
ax_text = fig.add_subplot(122)
ax_text.axis('off') # Eksen çizgilerini gizle, saf metin alanı yap

rapor_metni = (
    "  KÜBİK NiO METRİK VE hkl ANALİZ RAPORU\n"
    "=========================================\n\n"
    f"• Uzay Grubu: Fm-3m (No. 225)\n"
    f"• Kafes Sabiti (a): {KAFES_SABITI} nm\n"
    "• Kristal Simetrisi: Yüzey Merkezli Kübik\n\n"
    "Karakteristik Kırınım Düzlemleri (hkl):\n"
    "-----------------------------------------\n"
    " [hkl]   |   2θ Açısı   |  Göreceli Şiddet\n"
    "-----------------------------------------\n"
    " (111)   |    37.2°     |  [||||||        ]  60%\n"
    " (200)   |    43.3°     |  [||||||||||||  ] 100% (Zirve)\n"
    " (220)   |    62.9°     |  [|||||||||     ]  75%\n"
    " (311)   |    75.4°     |  [||            ]  15%\n"
    " (222)   |    79.4°     |  [|             ]  12%\n"
    " (400)   |    96.4°     |  [||            ]  16%\n"
    " (420)   |   108.4°     |  [|             ]   9%\n\n"
    " Mühendislik Notu:\n"
    " FCC kırınım kuralı gereği (h,k,l) indekslerinin\n"
    " tamamı çift ya da tamamı tek olmak zorundadır.\n"
    " Bu yüzden (200) düzlemi en yüksek atomik yoğunluğa\n"
    " ve en kusursuz yapıcı girişime (%100) sahiptir."
)

ax_text.text(0.05, 0.95, rapor_metni, transform=ax_text.transAxes,
             fontsize=9.5, fontfamily='monospace', color='#0f172a', va='top',
             bbox=dict(boxstyle='round,pad=1', facecolor='#f8fafc', edgecolor='#e2e8f0'))

plt.tight_layout()
print("3D Kristal Modeli ve hkl Matrisi Hazırlandı...")
plt.show()
