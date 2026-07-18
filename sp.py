import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

# Başlangıç Parametreleri
L, m, g, theta_max = 2.0, 1.0, 9.81, np.pi/4
t = 0
running = True 

fig = plt.figure(figsize=(14, 7))
gs = fig.add_gridspec(1, 3, width_ratios=[1.5, 1.5, 1])
ax_pend = fig.add_subplot(gs[0])
ax_energy = fig.add_subplot(gs[1])
ax_text = fig.add_subplot(gs[2])

plt.subplots_adjust(bottom=0.35, right=0.95, wspace=0.3)

# 1. Sarkaç ve Büyütülmüş Gölge
ax_pend.set_xlim(-5, 5); ax_pend.set_ylim(-5, 1); ax_pend.set_aspect('equal')
ax_pend.grid(True)
line, = ax_pend.plot([], [], 'k-', lw=2)
ball, = ax_pend.plot([], [], 'ro', markersize=15)
# Gölge boyutu 8'den 15'e çıkarıldı
shadow, = ax_pend.plot([], [], 'ro', markersize=15, alpha=0.5) 
ax_pend.plot([-5, 5], [-5, -5], 'k-', lw=3)

# 2. Enerji Grafiği
ax_energy.set_xlim(0, 100); ax_energy.set_ylim(0, 50)
ek_line, = ax_energy.plot([], [], 'b-', label='Ek')
ep_line, = ax_energy.plot([], [], 'g-', label='Ep')
ax_energy.legend(loc='upper right')

# 3. Formül Paneli
ax_text.axis('off')
formula_text = ax_text.text(0.1, 0.5, '', fontsize=12, family='monospace', fontweight='bold')

# Slider'lar
s_L = Slider(plt.axes([0.15, 0.22, 0.2, 0.03]), 'L', 0.5, 5.0, valinit=L)
s_g = Slider(plt.axes([0.15, 0.17, 0.2, 0.03]), 'g', 1.6, 25.0, valinit=g)
s_m = Slider(plt.axes([0.15, 0.12, 0.2, 0.03]), 'm', 0.1, 5.0, valinit=m)
s_theta = Slider(plt.axes([0.6, 0.22, 0.2, 0.03]), 'Genlik', 0.1, 1.5, valinit=theta_max)
s_speed = Slider(plt.axes([0.6, 0.17, 0.2, 0.03]), 'Hız', 0.01, 0.3, valinit=0.1)

# Pause Butonu
btn_pause = Button(plt.axes([0.6, 0.10, 0.1, 0.05]), 'Durdur/Başlat')
def toggle_pause(event):
    global running
    running = not running
btn_pause.on_clicked(toggle_pause)

max_points = 100
ek_data, ep_data = [0.0]*max_points, [0.0]*max_points
x_data = np.arange(max_points)

def update(frame):
    global t
    if not running: return line, ball, shadow, ek_line, ep_line, formula_text
    
    L_c, g_c, m_c, th_c, dt = s_L.val, s_g.val, s_m.val, s_theta.val, s_speed.val
    omega = np.sqrt(g_c / L_c)
    theta = th_c * np.cos(omega * t)
    
    x, y = L_c * np.sin(theta), -L_c * np.cos(theta)
    line.set_data([0, x], [0, y])
    ball.set_data([x], [y])
    shadow.set_data([x], [-5]) 
    
    ep = m_c * g_c * L_c * (1 - np.cos(theta))
    e_tot = m_c * g_c * L_c * (1 - np.cos(th_c))
    ek = e_tot - ep
    
    ek_data.pop(0); ek_data.append(ek)
    ep_data.pop(0); ep_data.append(ep)
    ek_line.set_data(x_data, ek_data)
    ep_line.set_data(x_data, ep_data)
    
    T = 2 * np.pi * np.sqrt(L_c / g_c)
    formula_text.set_text(f"FORMÜL:\nT = 2π√(L/g)\n\nL = {L_c:.2f} m\ng = {g_c:.2f} m/s²\nm = {m_c:.2f} kg\nGenlik = {th_c:.2f} rad\n\nT = {T:.3f} s\n\nEk = {ek:.2f} J\nEp = {ep:.2f} J")
    t += dt
    return line, ball, shadow, ek_line, ep_line, formula_text

ani = FuncAnimation(fig, update, interval=30, blit=True, cache_frame_data=False)
plt.show()
