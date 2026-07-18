import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- Fiziksel Parametreler ve Kurulum ---
# Faraday Kanunu: V(t) = N * B * A * w * sin(w * t)
# Burada w (açısal hız) = 2 * pi * f. Dolayısıyla V_max = Sabit * f olur.
K = 2.0  # Jeneratörün yapısal sabitleri (N * B * A * 2 * pi)
R = 10.0 # Lambanın direnci (Ohm)

# Zaman ekseni (0 - 2 saniye arası)
t = np.linspace(0, 2, 1000)

# Grafik penceresini ve alt grafikleri oluşturma
fig, (ax_volt, ax_bulb) = plt.subplots(2, 1, figsize=(8, 8), gridspec_kw={'height_ratios': [3, 1]})
plt.subplots_adjust(bottom=0.25, hspace=0.4)

# --- İlk Değerler ---
initial_f = 2.0 # Başlangıç frekansı (Hz)
w = 2 * np.pi * initial_f
V_max = K * initial_f
voltages = V_max * np.sin(w * t)

# --- Çizimler ---
# 1. Voltaj-Zaman Grafiği
line, = ax_volt.plot(t, voltages, lw=2, color='blue', label='İndüklenen Voltaj (V)')
ax_volt.set_xlim(0, 2)
ax_volt.set_ylim(-30, 30)
ax_volt.set_title("Jeneratör Voltaj - Zaman Grafiği (Faraday Kanunu)")
ax_volt.set_xlabel("Zaman (saniye)")
ax_volt.set_ylabel("Voltaj (Volt)")
ax_volt.grid(True)
ax_volt.legend(loc='upper right')

# 2. Lamba Parlaklığı Gösterimi (Efektif Değer/Güç Üzerinden)
# Lambayı temsil eden bir çember çiziyoruz
bulb_circle = plt.Circle((0.5, 0.5), 0.3, color='yellow', alpha=0.5)
ax_bulb.add_patch(bulb_circle)
ax_bulb.set_xlim(0, 1)
ax_bulb.set_ylim(0, 1)
ax_bulb.axis('off') # Eksenleri gizle
bulb_text = ax_bulb.text(0.5, 0.5, 'LAMBA', ha='center', va='center', fontsize=12, fontweight='bold')
ax_bulb.set_title("Ortalama Lamba Parlaklığı")

# Parlaklık Hesaplama Fonksiyonu
def calculate_brightness(f):
    # V_rms = V_max / sqrt(2)
    V_max_current = K * f
    V_rms = V_max_current / np.sqrt(2)
    Power = (V_rms ** 2) / R
    # Parlaklığı 0 ile 1 arasında scale etmek için normalizasyon (Maks frekans 10 kabul edildi)
    max_power = ((K * 10 / np.sqrt(2)) ** 2) / R
    alpha = min(Power / max_power, 1.0) # Matplotlib alpha değeri en fazla 1 olabilir
    return alpha, Power

# İlk parlaklığı ayarla
init_alpha, init_power = calculate_brightness(initial_f)
bulb_circle.set_alpha(init_alpha)

# --- Slider (Kaydırıcı) Ekleme ---
ax_freq = plt.axes([0.2, 0.1, 0.6, 0.03])
freq_slider = Slider(
    ax=ax_freq,
    label='Frekans (Hz) ',
    valmin=0.5,
    valmax=10.0,
    valinit=initial_f,
    valfmt='%1.1f Hz',
)

# --- Güncelleme Fonksiyonu ---
def update(val):
    f = freq_slider.val
    current_w = 2 * np.pi * f
    current_V_max = K * f
    
    # Voltaj grafiğini güncelle
    new_voltages = current_V_max * np.sin(current_w * t)
    line.set_ydata(new_voltages)
    
    # Lamba parlaklığını güncelle
    alpha, power = calculate_brightness(f)
    bulb_circle.set_alpha(alpha)
    bulb_text.set_text(f"LAMBA\nGüç: {power:.1f} W")
    
    # Grafiği yeniden çiz
    fig.canvas.draw_idle()

# Slider hareket ettiğinde update fonksiyonunu çağır
freq_slider.on_changed(update)

plt.show()
