import pygame
import sys
import time

# Pygame'i başlat
pygame.init()

# --- AYARLAR VE SABİTLER ---
HÜCRE_BOYUTU = 40
HARİTA_GENİŞLİK = 15
HARİTA_YÜKSEKLİK = 15

PENCERE_GENİŞLİK = HARİTA_GENİŞLİK * HÜCRE_BOYUTU
PENCERE_YÜKSEKLİK = (HARİTA_YÜKSEKLİK * HÜCRE_BOYUTU) + 100 # Yazılar ve süre için ekstra alan

# Renkler
RENK_ARKA_PLAN = (240, 240, 240)
RENK_DUVAR = (44, 62, 80)
RENK_YOL = (255, 255, 255)
RENK_UYARI = (231, 76, 60)
RENK_YAZI = (51, 51, 51)
RENK_KAZANDI = (39, 174, 96)
RENK_SURE = (41, 128, 185)

# Fontlar
font_kucuk = pygame.font.SysFont("Arial", 16, bold=True)
font_buyuk = pygame.font.SysFont("Arial", 22, bold=True)

# Pencereyi Oluştur
ekran = pygame.display.set_mode((PENCERE_GENİŞLİK, PENCERE_YÜKSEKLİK))
pygame.display.set_caption("Ali Selim'in Labirent Macerası 🐤")
saat = pygame.time.Clock()

# --- LABİRENT HARİTASI ---
harita = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 4, 1],
    [1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Oyun Değişkenlerini Sıfırlama Fonksiyonu (RESET)
def oyunu_sifirla():
    global civciv_x, civciv_y, oyun_bitti, durum_mesaji, mesaj_rengi, yakinlarda_tuzak_var, baslangic_zamani, gecen_sure, son_yon
    civciv_x, civciv_y = 1, 1
    oyun_bitti = False
    durum_mesaji = "Yön tuşları: Hareket | SPACE: Zıpla | R: Yeniden Başlat"
    mesaj_rengi = RENK_YAZI
    yakinlarda_tuzak_var = False
    baslangic_zamani = time.time()
    gecen_sure = 0
    son_yon = (0, 1) # Varsayılan olarak aşağı

def tuzak_kontrol(x, y):
    """Civcivin 1 kare çevresinde tuzak (4) var mı kontrol eder."""
    kontroller = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
    for k_x, k_y in kontroller:
        if 0 <= k_y < HARİTA_YÜKSEKLİK and 0 <= k_x < HARİTA_GENİŞLİK:
            if harita[k_y][k_x] == 4:
                return True
    return False

# İlk açılışta oyunu kur
oyunu_sifirla()

# Yanıp sönme efekti için zamanlayıcı
yazi_gorunur = True
YAZI_FLIP_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(YAZI_FLIP_EVENT, 400)

# --- ANA OYUN DÖNGÜSÜ ---
while True:
    if not oyun_bitti:
        gecen_sure = round(time.time() - baslangic_zamani, 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == YAZI_FLIP_EVENT:
            yazi_gorunur = not yazi_gorunur

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                oyunu_sifirla()
                continue

            if not oyun_bitti:
                dx, dy = 0, 0
                tusa_basildi = False
                
                if event.key == pygame.K_UP:
                    dy = -1; son_yon = (0, -1); tusa_basildi = True
                elif event.key == pygame.K_DOWN:
                    dy = 1;  son_yon = (0, 1);  tusa_basildi = True
                elif event.key == pygame.K_LEFT:
                    dx = -1; son_yon = (-1, 0); tusa_basildi = True
                elif event.key == pygame.K_RIGHT:
                    dx = 1;  son_yon = (1, 0);  tusa_basildi = True

                # Normal Hareket
                if tusa_basildi:
                    yeni_x = civciv_x + dx
                    yeni_y = civciv_y + dy
                    if harita[yeni_y][yeni_x] != 1:
                        civciv_x, civciv_y = yeni_x, yeni_y

                # SPACEBAR - Zıplama (Baktığı yöne 2 kare)
                elif event.key == pygame.K_SPACE:
                    zipla_x = civciv_x + (son_yon[0] * 2)
                    zipla_y = civciv_y + (son_yon[1] * 2)

                    if 0 <= zipla_y < HARİTA_YÜKSEKLİK and 0 <= zipla_x < HARİTA_GENİŞLİK:
                        if harita[zipla_y][zipla_x] != 1:
                            civciv_x, civciv_y = zipla_x, zipla_y
                            durum_mesaji = "Hop! Duvarın üzerinden zıpladın! 🦘"
                        else:
                            durum_mesaji = "Oraya zıplayamazsın, arkası duvar! 🛑"

                # Sonuç Kontrolleri
                if harita[civciv_y][civciv_x] == 4:
                    durum_mesaji = f"Tuzağa bastın! Süre: {gecen_sure}sn. Sıfırlamak için R'ye bas! 💥"
                    mesaj_rengi = RENK_UYARI
                    oyun_bitti = True
                    yakinlarda_tuzak_var = False

                elif harita[civciv_y][civciv_x] == 3:
                    durum_mesaji = f"Tebrikler Ali Selim! Rekorun: {gecen_sure}sn! R'ye bas! 🎉"
                    mesaj_rengi = RENK_KAZANDI
                    oyun_bitti = True
                    yakinlarda_tuzak_var = False
                
                else:
                    yakinlarda_tuzak_var = tuzak_kontrol(civciv_x, civciv_y)

    # --- EKRANA ÇİZME ---
    ekran.fill(RENK_ARKA_PLAN)

    # Labirenti Çiz
    for y in range(HARİTA_YÜKSEKLİK):
        for x in range(HARİTA_GENİŞLİK):
            dikdortgen = pygame.Rect(x * HÜCRE_BOYUTU, y * HÜCRE_BOYUTU, HÜCRE_BOYUTU, HÜCRE_BOYUTU)
            if harita[y][x] == 1:
                pygame.draw.rect(ekran, RENK_DUVAR, dikdortgen)
            else:
                pygame.draw.rect(ekran, RENK_YOL, dikdortgen)
            pygame.draw.rect(ekran, (220, 220, 220), dikdortgen, 1)

            if harita[y][x] == 3:
                misir_yazi = font_buyuk.render("🌽", True, (0,0,0))
                ekran.blit(misir_yazi, (x * HÜCRE_BOYUTU + 8, y * HÜCRE_BOYUTU + 5))

    # Civcivi Çiz
    civciv_yazi = font_buyuk.render("🐤", True, (0,0,0))
    ekran.blit(civciv_yazi, (civciv_x * HÜCRE_BOYUTU + 8, civciv_y * HÜCRE_BOYUTU + 5))

    # --- ARAYÜZ VE SÜRE PANELİ ---
    # 1) Tuzak Uyarısı
    if yakinlarda_tuzak_var and yazi_gorunur:
        uyari_yazi = font_buyuk.render("DİKKAT ALİ SELİM TUZAK VAR! ⚠️", True, RENK_UYARI)
        uyari_rect = uyari_yazi.get_rect(center=(PENCERE_GENİŞLİK // 2, PENCERE_YÜKSEKLİK - 75))
        ekran.blit(uyari_yazi, uyari_rect)

    # 2) Zaman Çizelgesi
    sure_yazi = font_kucuk.render(f"SÜRE: {gecen_sure} sn", True, RENK_SURE)
    ekran.blit(sure_yazi, (20, PENCERE_YÜKSEKLİK - 40))

    # 3) Durum Mesajı
    durum_render = font_kucuk.render(durum_mesaji, True, mesaj_rengi)
    durum_rect = durum_render.get_rect(center=(PENCERE_GENİŞLİK // 2 + 60, PENCERE_YÜKSEKLİK - 40))
    ekran.blit(durum_render, durum_rect)

    pygame.display.flip()
    saat.tick(30)
