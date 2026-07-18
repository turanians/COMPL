import numpy as np
import plotly.graph_objects as go
from scipy.linalg import expm

# --- 1. LATTICE (ÖRGÜ) PARAMETRELERİ ---
N_sites = 80          # Kristaldeki toplam atom (site) sayısı
sites = np.arange(N_sites)

# Tünelleme Matrisi (Hamiltonian) Kurulumu
H = np.zeros((N_sites, N_sites), dtype=complex)
t_hopping = 1.0       # Atomlar arası tünelleme/zıplama genliği

# Temel Hamiltonian: Komşu atomlar arası geçişler
for i in range(N_sites - 1):
    H[i, i+1] = -t_hopping
    H[i+1, i] = -t_hopping

# --- 2. ÖRGÜ ÜZERİNDE PERİYODİK POTANSİYEL ENGELLİ (BARİYER) ---
barrier_start = 35
barrier_end = 45
V_barrier = 2.5       # Yalıtkan bariyer bölgesi enerji seviyesi

for i in range(barrier_start, barrier_end):
    H[i, i] = V_barrier

# --- 3. BAŞLANGIÇ DALGA FONKSiyonu (Lattice Üzerinde Gauss Paketi) ---
site_0 = 15           # Elektronun başladığı atomun indeksi
sigma = 4.0           # Elektronun yayılım genişliği
k0 = 1.0              # Elektronun kristal içindeki dalga vektörü (Momenti)

psi = np.exp(-(sites - site_0)**2 / (2 * sigma**2)) * np.exp(1j * k0 * sites)
psi /= np.linalg.norm(psi)  # Normalizasyon

# --- 4. ZAMAN İLERLEMESİ VE VERİ TOPLAMA ---
dt = 0.4
steps = 120
history_prob = []

# Zaman ilerletme operatörü: U = exp(-i * H * dt)
U = expm(-1j * H * dt)

for step in range(steps):
    history_prob.append(np.abs(psi)**2)
    psi = U @ psi  # Dalga fonksiyonunu örgü üzerinde ilerlet

history_prob = np.array(history_prob)

# --- 5. PLOTLY İLE ETKİLEŞİMLİ 3D LATTICE GÖRSELLEŞTİRME ---
time_axis = np.arange(steps) * dt
X, Y = np.meshgrid(sites, time_axis)

fig = go.Figure(data=[go.Surface(
    z=history_prob, x=X, y=Y,
    colorscale='Viridis',
    colorbar=dict(title='Olasılık Yoğunluğu')
)])

# Potansiyel bariyer sınırlarını göstermek için kırmızı bir hat ekle
fig.add_trace(go.Scatter3d(
    x=[barrier_start, barrier_start, barrier_end, barrier_end, barrier_start],
    y=[0, time_axis[-1], time_axis[-1], 0, 0],
    z=[0, 0, 0, 0, 0],
    mode='lines',
    line=dict(color='red', width=5),
    name='Bariyer Bölgesi'
))

fig.update_layout(
    title='Lattice (Örgü) Üzerinde Kuantum Tünelleme Zamansal Evrimi',
    scene=dict(
        xaxis_title='Atom Konumu (Site Index)',
        yaxis_title='Zaman (t)',
        zaxis_title='Elektronun Orada Bulunma Olasılığı',
        camera=dict(eye=dict(x=1.5, y=-1.5, z=1.2))
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

# --- 6. GİTHUB VE TARAYICI ÇIKTILARI ---
# 1. Grafiği bilgisayarındaki yerel tarayıcıda (127.0.0.1) açar
print("Simülasyon yerel web sayfasında açılıyor...")
fig.show()

# 2. Aynı klasöre 'lattice_tunneling.html' adında bağımsız bir dosya kaydeder
print("GitHub için interaktif HTML dosyası kaydediliyor...")
fig.write_html("lattice_tunneling.html")
print("İşlem tamam! 'lattice_tunneling.html' dosyasını doğrudan GitHub repona yükleyebilirsin.")
