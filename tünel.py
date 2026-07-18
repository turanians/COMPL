import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.sparse.linalg import spsolve
from scipy.sparse import diags

# --- 1. GLOBAL PARAMETRELER VE FİZİKSEL BİRİMLER ---
L = 100.0           # Simülasyon evreninin toplam boyutu
Nx = 1000           # Uzay adım sayısı
x = np.linspace(0, L, Nx)
dx = x[1] - x[0]    # Uzay adım boyutu

Nt = 1000           # Toplam zaman adım sayısı
dt = 0.1            # Zaman adım boyutu

# Fiziksel Sabitler (İndirgenmiş birimler, m=h_bar=1 gibi)
hbar = 1.0
mass = 1.0

# Bariyer Özellikleri (NameError hatasını çözmek için global yapıldı)
barrier_width = 5.0      # Bariyerin genişliği
barrier_height = 1.5     # Bariyerin yüksekliği
barrier_position = 50.0   # Bariyerin merkez konumu

# --- 2. POTANSİYEL BARİYER VE DALGA PAKETİ TANIMI ---
def get_potential(x):
    potential = np.zeros_like(x)
    potential[(x > barrier_position - barrier_width/2) & 
              (x < barrier_position + barrier_width/2)] = barrier_height
    return potential

V = get_potential(x)

# Gelen Dalga Paketi Tanımı (Gauss Paketi)
x0 = 20.0           # Paketin başlangıç konumu
sigma0 = 3.0        # Paketin genişliği
k0 = 2.0            # Paketin ortalama dalga vektörü (Hızı)

# Başlangıç Dalga Fonksiyonu ve Normalizasyonu
psi_0 = np.exp(-(x - x0)**2 / (2 * sigma0**2)) * np.exp(1j * k0 * x)
norm_0 = np.sqrt(np.sum(np.abs(psi_0)**2) * dx)
psi = psi_0 / norm_0


# --- 3. CRANK-NICOLSON MATRİSLERİNİN KURULMASI ---
alpha = (1j * hbar * dt) / (4 * mass * dx**2)

A_main = np.ones(Nx) + 2 * alpha
A_off = -alpha * np.ones(Nx - 1)
A_mat = diags([A_main, A_off, A_off], [0, 1, -1], format='csc')


def advance_time(psi_current, V, dt, dx, hbar, mass, A_mat):
    """Dalga fonksiyonunu bir zaman adımı (dt) kadar ileri taşır."""
    # Kinematik adım (Crank-Nicolson)
    b_part_kin = np.conj(A_mat) @ psi_current
    psi_mid = spsolve(A_mat, b_part_kin)
    
    # Potansiyel adım (Split-Operator)
    pot_operator = np.exp(-1j * V * dt / hbar)
    psi_next = pot_operator * psi_mid
    
    return psi_next


# --- 4. GÖRSELLEŞTİRME VE ANİMASYON ---
fig, (ax_psi, ax_pot) = plt.subplots(2, 1, sharex=True, figsize=(10, 8))
plt.subplots_adjust(hspace=0.05)

# Üst Grafik: Dalga Fonksiyonu ve Olasılık Yoğunluğu
line_psi_real, = ax_psi.plot(x, np.real(psi), 'r-', alpha=0.6, label='Re(psi)')
line_prob, = ax_psi.plot(x, np.abs(psi)**2, 'b-', lw=2.5, label='Olasılık Yoğunluğu (|psi|^2)')
time_text = ax_psi.text(0.02, 0.95, '', transform=ax_psi.transAxes)

ax_psi.set_ylabel('Genlik / Olasılık')
ax_psi.set_ylim(-0.25, 0.35)
ax_psi.grid(True, alpha=0.3)
ax_psi.legend(loc='upper right')
ax_psi.set_title('Kuantum Tünelleme Simülasyonu')

# Alt Grafik: Potansiyel Bariyer ve Enerji
E_kinetic = (hbar * k0)**2 / (2 * mass)
ax_pot.plot(x, V, 'k-', lw=3, label='Potansiyel Bariyer (V)')
ax_pot.axhline(E_kinetic, color='g', linestyle='--', label=f'Gelen Parçacık Enerjisi (E = {E_kinetic:.2f})')

ax_pot.set_xlabel('Konum (x)')
ax_pot.set_ylabel('Enerji')
ax_pot.set_ylim(0, barrier_height * 1.5) # Buradaki NameError hatası düzeltildi
ax_pot.grid(True, alpha=0.3)
ax_pot.legend(loc='upper left')

# Animasyon Güncelleme Fonksiyonu
def update(frame, psi, V, dt, dx, hbar, mass, A_mat):
    # Performans için her karede 5 zaman adımı ilerle
    for _ in range(5): 
        psi = advance_time(psi, V, dt, dx, hbar, mass, A_mat)
    
    prob = np.abs(psi)**2
    line_psi_real.set_ydata(np.real(psi))
    line_prob.set_ydata(prob)
    
    # Anlık tünelleme olasılığı hesabı
    barrier_end_index = Nx // 2 + int((barrier_width/2) / dx)
    transmission_prob = np.sum(prob[barrier_end_index:]) * dx
    time_text.set_text(f'Zaman (t): {frame * dt * 5:.1f} | Tünelleme Olasılığı: %{transmission_prob*100:.1f}')

    return line_psi_real, line_prob, time_text

print("Simülasyon penceresi açılıyor...")
ani = FuncAnimation(fig, update, frames=Nt//5, fargs=(psi, V, dt, dx, hbar, mass, A_mat),
                    interval=20, blit=True)

plt.tight_layout()
plt.show()
