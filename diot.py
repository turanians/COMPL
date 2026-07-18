import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons

# --- Fiziksel Parametreler ve Kurulum ---
K = 2.0  # Jeneratörün yapısal sabitleri
R = 10.0 # Lambanın direnci (Ohm)
t = np.linspace(0, 2, 1000)

# Grafik penceresini oluşturma
fig, (ax_volt, ax_bulb) = plt.subplots(2, 1, figsize=(8, 8), gridspec_kw={'height_ratios': [3, 1]})
plt.subplots_adjust(bottom=0.3, hspace=0.4)

# --- İlk Değerler ---
initial_f = 2.0
w = 2 * np.pi * initial_f
V_max = K * initial_f
voltages = V_max * np.sin(w * t)

# Diyot başlangıçta YOK (False)
diode_on = False

# --- Çizimler ---
# 1. Voltaj-Zaman Grafiği
line, = ax_volt.plot(t, voltages, lw=2, color='blue', label='Lamba Üzerindeki Voltaj (V)')
ax_volt.set_xlim(0, 2)
ax_volt.set_ylim(-30, 30)
ax_volt.set_title("Jeneratör ve Diyot Devresi Voltaj - Zaman Grafiği")
ax_volt.set_xlabel("Zaman (saniye)")
ax_volt.set_ylabel("Voltaj (Volt)")
ax_volt.grid(True)
ax_volt.legend(loc='upper right')

# 2. Lamba Parlaklığı Gösterimi
bulb_circle = plt.Circle((0.5, 0.5), 0.3, color='yellow', alpha=0.5)
ax_bulb.add_patch(bulb_circle)
ax_bulb.set_xlim(0, 1)
ax_bulb.set_ylim(0, 1)
ax_bulb.axis('off')
bulb_text = ax_bulb.text(0.5, 0.5, 'LAMBA', ha='center', va='center', fontsize=12, fontweight='bold')
ax_bulb.set_title("Ortalama Lamba Parlaklığı")

# Parlaklık Hesaplama Fonksiyonu (Diyot Durumuna Göre)
def calculate_brightness(f, diode_active):
    V_max_current = K * f
    
    if diode_active:
        # Diyot varsa voltajın negatif kısımları sıfır olur.
        # Yarım dalga doğrultucu için V_rms = V_max / 2 olur.
        V_rms = V_max_current / 2.0
    else:
        # Diyot yoksa normal AC: V_rms = V_max / sqrt(2)
        V_rms = V_max_current / np.sqrt(2)
        
    Power = (V_rms ** 2) / R
    
    # Parlaklığı 0-1 arasına scale etmek için normalizasyon (Maks frekans 10 kabul edildi)
    max_power_no_diode = ((K * 10 / np.sqrt(2)) ** 2) / R
    alpha = min(Power / max_power_no_diode, 1.0)
    return alpha, Power

# İlk parlaklığı ayarla
init_alpha, init_power = calculate_brightness(initial_f, diode_on)
bulb_circle.set_alpha(init_alpha)

# --- Slider (Frekans) Ekleme ---
ax_freq = plt.axes([0.2, 0.15, 0.6, 0.03])
freq_slider = Slider(ax=ax_freq, label='Frekans (Hz) ', valmin=0.5, valmax=10.0, valinit=initial_f, valfmt='%1.1f Hz')

# --- Checkbox (Diyot Butonu) Ekleme ---
ax_check = plt.axes([0.4, 0.02, 0.2, 0.05])
# Tek seçenekli bir buton grubu oluşturuyoruz
check_button = CheckButtons(ax=ax_check, labels=['Diyot Var'], actives=[diode_on])

# --- Güncelleme Fonksiyonu ---
def update(val):
    global diode_on
    f = freq_slider.val
    current_w = 2 * np.pi * f
    current_V_max = K * f
    
    # Temel AC voltaj dalgası
    new_voltages = current_V_max * np.sin(current_w * t)
    
    # Eğer diyot aktifse negatif voltajları 0 yap (Yarım dalga doğrultma)
    if diode_on:
        new_voltages = np.where(new_voltages < 0, 0, new_voltages)
    
    # Grafiği güncelle
    line.set_ydata(new_voltages)
    
    # Lamba parlaklığını ve gücü güncelle
    alpha, power = calculate_brightness(f, diode_on)
    bulb_circle.set_alpha(alpha)
    bulb_text.set_text(f"LAMBA\nGüç: {power:.1f} W")
    
    fig.canvas.draw_idle()

# Diyot butonuna basıldığında tetiklenecek fonksiyon
def toggle_diode(label):
    global diode_on
    diode_on = not diode_on
    update(None)

# Olay dinleyicilerini bağlama
freq_slider.on_changed(update)
check_button.on_clicked(toggle_diode)

plt.show()
