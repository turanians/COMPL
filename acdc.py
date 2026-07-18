import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons, RadioButtons

# --- Fiziksel Parametreler ve Kurulum ---
K = 2.0  
R = 10.0 
t = np.linspace(0, 2, 1000)

# 3 farklı panel alanı oluşturuyoruz: Voltaj, Lamba ve Devre Şeması
fig, (ax_volt, ax_bulb, ax_circuit) = plt.subplots(3, 1, figsize=(8, 9), gridspec_kw={'height_ratios': [3, 1, 2]})
plt.subplots_adjust(bottom=0.28, hspace=0.4)

# --- İlk Değerler ---
initial_f = 2.0
diode_on = False
source_type = 'AC'  # Varsayılan kaynak 'AC' (Jeneratör)

# --- Çizim Fonksiyonları ---
def draw_circuit_diagram(ax, diode_active, source):
    """Devre şemasını dinamik olarak çizer"""
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title("Devre Şeması", fontsize=11, fontweight='bold', pad=10)

    # Temel kablolar (Dörtgen hat)
    ax.plot([2, 2, 8, 8, 2], [1, 5, 5, 1, 1], color='black', lw=1.5)
    
    # 1. Güç Kaynağı (Sol Kol)
    ax.plot([2, 2], [1, 5], color='white', lw=3) # Mevcut çizgiyi gizle
    circle_source = plt.Circle((2, 3), 0.4, fill=False, color='black', lw=2)
    ax.add_patch(circle_source)
    if source == 'AC':
        # Sinüs dalgası sembolü (AC)
        sx = np.linspace(1.8, 2.2, 50)
        sy = 3 + 0.15 * np.sin((sx - 2) * 2 * np.pi / 0.4)
        ax.plot(sx, sy, color='black', lw=1.5)
        ax.text(1.2, 3, "AC (Jen.)", va='center', ha='right', fontsize=10)
    else:
        # Pil sembolü (DC)
        ax.plot([1.7, 2.3], [3.1, 3.1], color='black', lw=2) # Uzun çizgi +
        ax.plot([1.85, 2.15], [2.9, 2.9], color='black', lw=3) # Kısa kalın çizgi -
        ax.text(1.2, 3.2, "+", fontsize=12, va='center')
        ax.text(1.2, 3, "DC", va='center', ha='right', fontsize=10)

    # 2. Anahtar (Alt Kol - Açık/Kapalı gösterimi için sembolik kapalı çiziyoruz)
    ax.plot([4.5, 5.5], [1, 1], color='white', lw=3)
    ax.plot([4.5, 4.8], [1, 1], color='black', lw=2)
    ax.plot([4.8, 5.4], [1, 1.3], color='black', lw=2) # Anahtar kolu
    ax.plot([5.4, 5.5], [1, 1], color='black', lw=2)
    ax.text(5, 0.5, "Anahtar (Kapalı)", ha='center', fontsize=9)

    # 3. Diyot Bölümü (Üst Kol)
    ax.plot([4.5, 5.5], [5, 5], color='white', lw=3)
    if diode_active:
        # Diyot Üçgeni ve Çizgisi
        ax.polygon = plt.Polygon([[4.8, 4.7], [4.8, 5.3], [5.3, 5.0]], closed=True, fill=True, color='black')
        ax.add_patch(ax.polygon)
        ax.plot([5.3, 5.3], [4.7, 5.3], color='black', lw=2) # Katot çizgisi
        ax.plot([4.5, 4.8], [5, 5], color='black', lw=2)
        ax.plot([5.3, 5.5], [5, 5], color='black', lw=2)
        ax.text(5, 5.5, "Diyot", ha='center', fontsize=9)
    else:
        ax.plot([4.5, 5.5], [5, 5], color='black', lw=1.5) # Düz kablo
        ax.text(5, 5.3, "(Diyot Yok)", ha='center', color='gray', fontsize=9)

    # 4. Lamba (Sağ Kol)
    ax.plot([8, 8], [2.5, 3.5], color='white', lw=3)
    circle_lamba = plt.Circle((8, 3), 0.3, fill=False, color='black', lw=2)
    ax.add_patch(circle_lamba)
    # İçindeki X işareti
    ax.plot([7.8, 8.2], [2.8, 3.2], color='black', lw=1.5)
    ax.plot([7.8, 8.2], [3.2, 2.8], color='black', lw=1.5)
    ax.text(8.6, 3, "Lamba", va='center', fontsize=10)

# İlk devre çizimi
draw_circuit_diagram(ax_circuit, diode_on, source_type)

# 2. Voltaj-Zaman Grafiği Ayarları
w = 2 * np.pi * initial_f
V_max = K * initial_f
voltages = V_max * np.sin(w * t)
line, = ax_volt.plot(t, voltages, lw=2, color='blue', label='Lamba Voltajı (V)')
ax_volt.set_xlim(0, 2)
ax_volt.set_ylim(-30, 30)
ax_volt.set_title("Devre Voltaj - Zaman Grafiği")
ax_volt.set_xlabel("Zaman (saniye)")
ax_volt.set_ylabel("Voltaj (Volt)")
ax_volt.grid(True)
ax_volt.legend(loc='upper right')

# 3. Lamba Parlaklığı Paneli
bulb_circle = plt.Circle((0.5, 0.5), 0.3, color='yellow', alpha=0.5)
ax_bulb.add_patch(bulb_circle)
ax_bulb.set_xlim(0, 1)
ax_bulb.set_ylim(0, 1)
ax_bulb.axis('off')
bulb_text = ax_bulb.text(0.5, 0.5, 'LAMBA', ha='center', va='center', fontsize=12, fontweight='bold')
ax_bulb.set_title("Ortalama Lamba Parlaklığı")

# Parlaklık ve Voltaj Hesaplama Fonksiyonu
def calculate_circuit(f, diode_active, source):
    V_max_current = K * f
    
    if source == 'AC':
        base_voltages = V_max_current * np.sin(2 * np.pi * f * t)
        if diode_active:
            final_voltages = np.where(base_voltages < 0, 0, base_voltages)
            V_rms = V_max_current / 2.0
        else:
            final_voltages = base_voltages
            V_rms = V_max_current / np.sqrt(2)
    else: # DC Modu (Sabit Voltaj)
        # DC voltajı anlaşılır olması için jeneratörün üretebileceği kararlı bir değere sabitleyelim
        V_dc = 15.0 
        if diode_active:
            # Diyot düz bağlı olduğu için DC akımı aynen geçirir
            final_voltages = np.full_like(t, V_dc)
            V_rms = V_dc
        else:
            final_voltages = np.full_like(t, V_dc)
            V_rms = V_dc
            
    Power = (V_rms ** 2) / R
    max_power = ((K * 10 / np.sqrt(2)) ** 2) / R
    alpha = min(Power / max_power, 1.0)
    
    return final_voltages, alpha, Power

# İlk hesabı uygula
init_volts, init_alpha, init_power = calculate_circuit(initial_f, diode_on, source_type)
bulb_circle.set_alpha(init_alpha)

# --- Arayüz Kontrolleri (Slider, Checkbox, Radio) ---
ax_freq = plt.axes([0.2, 0.18, 0.6, 0.03])
freq_slider = Slider(ax=ax_freq, label='AC Frekans (Hz) ', valmin=0.5, valmax=10.0, valinit=initial_f, valfmt='%1.1f Hz')

ax_check = plt.axes([0.15, 0.02, 0.25, 0.08])
check_button = CheckButtons(ax=ax_check, labels=['Diyot Var'], actives=[diode_on])

ax_radio = plt.axes([0.6, 0.02, 0.25, 0.08])
radio_button = RadioButtons(ax=ax_radio, labels=('AC (Jeneratör)', 'DC (Sabit Pil)'))

# --- Güncelleme Fonksiyonu ---
def update(val):
    global diode_on, source_type
    f = freq_slider.val
    
    # Yeni değerleri hesapla
    new_voltages, alpha, power = calculate_circuit(f, diode_on, source_type)
    
    # Grafikleri güncelle
    line.set_ydata(new_voltages)
    bulb_circle.set_alpha(alpha)
    bulb_text.set_text(f"LAMBA\nGüç: {power:.1f} W")
    
    # Devre şemasını güncelle
    draw_circuit_diagram(ax_circuit, diode_on, source_type)
    
    fig.canvas.draw_idle()

def toggle_diode(label):
    global diode_on
    diode_on = not diode_on
    update(None)

def change_source(label):
    global source_type
    if 'AC' in label:
        source_type = 'AC'
        ax_freq.set_visible(True) # DC modunda frekans anlamsız olduğu için gizle/göster yapabiliriz
    else:
        source_type = 'DC'
        ax_freq.set_visible(False)
    update(None)

# Olayları bağlama
freq_slider.on_changed(update)
check_button.on_clicked(toggle_diode)
radio_button.on_clicked(change_source)

plt.show()
