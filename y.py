import numpy as np
import matplotlib.pyplot as plt

def initialize_lattice(N):
    return np.random.choice([-1, 1], size=(N, N))

def metropolis_step(lattice, beta):
    N = lattice.shape[0]
    x = np.random.randint(0, N)
    y = np.random.randint(0, N)
    current_spin = lattice[x, y]
    
    # Periyodik Sınır Şartları
    neighbors_sum = (lattice[(x + 1) % N, y] + 
                     lattice[(x - 1) % N, y] + 
                     lattice[x, (y + 1) % N] + 
                     lattice[x, (y - 1) % N])
    
    dE = 2 * current_spin * neighbors_sum
    
    if dE <= 0 or np.random.rand() < np.exp(-dE * beta):
        lattice[x, y] *= -1
        
    return lattice

def calculate_magnetization(lattice):
    # Ortalama mıknatıslanma: tüm spinlerin toplamının atom sayısına bölümü
    return np.abs(np.mean(lattice))

# --- MONTE CARLO SİMÜLASYON PARAMETRELERİ ---
N = 32          # Hesaplama hızlı olsun diye matrisi 32x32 yapıyoruz
mc_steps = 100000 # Her sıcaklık için atılacak toplam Monte Carlo adımı

# İnceleyeceğimiz Sıcaklık Değerleri (Lattice T = 1.0 ile 4.0 arası)
# Teorik olarak kritik sıcaklık Tc ~ 2.269 olmalıdır.
temperatures = np.linspace(1.0, 4.0, 30)
magnetizations = []

print("Monte Carlo Simülasyonu başladı. Sıcaklıklar taranıyor...")

for T in temperatures:
    beta = 1.0 / T
    lattice = initialize_lattice(N)
    
    # 1. Aşama: Sistemin o sıcaklıktaki denge durumuna (equilibrium) gelmesini sağla
    # İlk 60.000 adımı veriye dahil etmiyoruz (Burn-in / Thermalization)
    for step in range(int(mc_steps * 0.6)):
        lattice = metropolis_step(lattice, beta)
        
    # 2. Aşama: Dengeye gelen sistemden veri topla
    total_mag = 0
    sample_count = 0
    for step in range(int(mc_steps * 0.4)):
        lattice = metropolis_step(lattice, beta)
        # Her 100 adımda bir ölçüm al (otokorelasyonu azaltmak için)
        if step % 100 == 0:
            total_mag += calculate_magnetization(lattice)
            sample_count += 1
            
    # O sıcaklıktaki ortalama manyetizasyonu kaydet
    avg_mag = total_mag / sample_count
    magnetizations.append(avg_mag)
    print(f"Sıcaklık: {T:.2f} K -> Ortalama Manyetizasyon: {avg_mag:.4f}")

# --- GRAFİK ÇİZDİRME ---
plt.figure(figsize=(8, 5))
plt.plot(temperatures, magnetizations, 'o-', color='crimson', label='Monte Carlo Verisi')
plt.axvline(x=2.269, color='blue', linestyle='--', label='Teorik Kritik Sıcaklık (Tc ≈ 2.27)')
plt.title("Ising Modeli: Sıcaklığa Karşı Manyetizasyon (Faz Geçişi)")
plt.xlabel("Sıcaklık (T)")
plt.ylabel("Ortalama Manyetizasyon (|M|)")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.show()
