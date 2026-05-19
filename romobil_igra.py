import pygame
import random
import sys

# 1. Inicijalizacija
pygame.init()
SIRINA, VISINA = 500, 700
zaslon = pygame.display.set_mode((SIRINA, VISINA))
pygame.display.set_caption("Romobil Rush")
sat = pygame.time.Clock()

# Boje (RGB)
BOJA_CESTE = (50, 50, 50)
BOJA_TRAVE = (34, 139, 34)
BOJA_LINIJE = (255, 255, 255)
BOJA_ROMOBILA = (0, 191, 255)
BOJA_KOTACA = (20, 20, 20)
BOJA_NOVCOCA = (255, 215, 0)
BOJA_RUPE = (100, 40, 0)
BOJA_TEKSTA = (255, 255, 255)

# 2. Definiranje objekata
romobil_sirina = 40
romobil_visina = 70
romobil_x = SIRINA // 2 - romobil_sirina // 2
romobil_y = VISINA - 120
romobil_brzina = 6

prepreka_sirina, prepreka_visina = 60, 30
prepreka_x = random.randint(80, SIRINA - 80 - prepreka_sirina)
prepreka_y = -100

novcic_radijus = 12
novcic_x = random.randint(80, SIRINA - 80 - novcic_radijus)
novcic_y = -300

brzina_svijeta = 5
bodovi = 0
zivoti = 3
igra_gotova = False

# Funkcija za tekst koja koristi isključivo ugrađeni Pygame font (neće se smrznuti)
def prikazi_tekst(poruka, x, y, velicina=24, boja=BOJA_TEKSTA):
    izvor_fonta = pygame.font.Font(None, velicina)
    tekst_povrsina = izvor_fonta.render(poruka, True, boja)
    zaslon.blit(tekst_povrsina, (x, y))

# 3. Glavna petlja igre
while True:
    # OGRANIČENJE FPS-a na samom početku petlje (sprječava preopterećenje grafičke)
    sat.tick(60)

    # Rukovanje događajima (Mora se izvršiti kako prozor ne bi bio crn/zamrznut)
    for dogadjaj in pygame.event.get():
        if dogadjaj.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if dogadjaj.type == pygame.KEYDOWN:
            if dogadjaj.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if dogadjaj.key == pygame.K_SPACE and igra_gotova:
                romobil_x = SIRINA // 2 - romobil_sirina // 2
                prepreka_y = -100
                novcic_y = -300
                bodovi = 0
                zivoti = 3
                brzina_svijeta = 5
                igra_gotova = False

    if not igra_gotova:
        # Kontrole romobila
        tipke = pygame.key.get_pressed()
        if tipke[pygame.K_LEFT] and romobil_x > 70:
            romobil_x -= romobil_brzina
        if tipke[pygame.K_RIGHT] and romobil_x < SIRINA - 70 - romobil_sirina:
            romobil_x += romobil_brzina

        # Kretanje objekata
        prepreka_y += brzina_svijeta
        novcic_y += brzina_svijeta

        if prepreka_y > VISINA:
            prepreka_y = -50
            prepreka_x = random.randint(70, SIRINA - 70 - prepreka_sirina)
            bodovi += 1
            if bodovi % 5 == 0:
                brzina_svijeta += 0.5

        if novcic_y > VISINA:
            novcic_y = -50
            novcic_x = random.randint(70, SIRINA - 70 - novcic_radijus)

        # Provjera sudara (Hitbox)
        romobil_rect = pygame.Rect(romobil_x, romobil_y, romobil_sirina, romobil_visina)
        prepreka_rect = pygame.Rect(prepreka_x, prepreka_y, prepreka_sirina, prepreka_visina)
        novcic_rect = pygame.Rect(novcic_x - novcic_radijus, novcic_y - novcic_radijus, novcic_radijus * 2, novcic_radijus * 2)

        if romobil_rect.colliderect(prepreka_rect):
            zivoti -= 1
            prepreka_y = -100
            prepreka_x = random.randint(70, SIRINA - 70 - prepreka_sirina)
            if zivoti <= 0:
                igra_gotova = True

        if romobil_rect.colliderect(novcic_rect):
            bodovi += 5
            novcic_y = -100
            novcic_x = random.randint(70, SIRINA - 70 - novcic_radijus)

    # 4. Crtanje grafike (Sve ide na ekran)
    zaslon.fill(BOJA_TRAVE)
    pygame.draw.rect(zaslon, BOJA_CESTE, (60, 0, SIRINA - 120, VISINA))
    
    # Linije na cesti
    for i in range(0, VISINA, 40):
        pygame.draw.line(zaslon, BOJA_LINIJE, (60, i), (60, i + 20), 3)
        pygame.draw.line(zaslon, BOJA_LINIJE, (SIRINA - 60, i), (SIRINA - 60, i + 20), 3)

    if not igra_gotova:
        # Rupa i novčić
        pygame.draw.ellipse(zaslon, BOJA_RUPE, (prepreka_x, prepreka_y, prepreka_sirina, prepreka_visina))
        pygame.draw.circle(zaslon, BOJA_NOVCOCA, (novcic_x, novcic_y), novcic_radijus)

        # Romobil
        pygame.draw.rect(zaslon, BOJA_ROMOBILA, (romobil_x + 15, romobil_y + 10, 10, 50))
        pygame.draw.line(zaslon, BOJA_ROMOBILA, (romobil_x, romobil_y + 15), (romobil_x + 40, romobil_y + 15), 4)
        pygame.draw.line(zaslon, BOJA_ROMOBILA, (romobil_x + 20, romobil_y + 15), (romobil_x + 20, romobil_y + 30), 4)
        pygame.draw.circle(zaslon, BOJA_KOTACA, (romobil_x + 20, romobil_y + 12), 6)
        pygame.draw.circle(zaslon, BOJA_KOTACA, (romobil_x + 20, romobil_y + 58), 6)

        # Statistika
        prikazi_tekst(f"Bodovi: {bodovi}", 10, 10, 24)
        prikazi_tekst(f"Zivoti: {zivoti}", 10, 40, 24)
    else:
        prikazi_tekst("KRAJ IGRE", SIRINA // 2 - 80, VISINA // 2 - 60, velicina=36, boja=(255, 0, 0))
        prikazi_tekst(f"Ukupno bodova: {bodovi}", SIRINA // 2 - 95, VISINA // 2, velicina=24)
        prikazi_tekst("Pritisni RAZMAK za novu igru", SIRINA // 2 - 145, VISINA // 2 + 50, velicina=20, boja=(0, 255, 0))

    # Korištenje update() umjesto flip() za bolju kompatibilnost grafičkih kartica
    pygame.display.update()