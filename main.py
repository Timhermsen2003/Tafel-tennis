import os, sys, pygame
from random import randint


class Score(pygame.sprite.Sprite):
    def __init__(self, font, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.pos = pos
        self.score = 0
        self.image = self.font.render(str(self.score), 0, (255, 255, 255))
        self.rect = self.image.get_rect(center=self.pos)

    def score_omhoog(self):
        self.score += 1

    def update(self):
        self.image = self.font.render(str(self.score), 0, (255, 255, 255))
        self.rect = self.image.get_rect(center=self.pos)



class Bal(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        #standaardwaarden voor de bal
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = pygame.Surface((10, 10)).convert()
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=self.pos)
        self.snelheid_x = 0
        self.snelheid_y = 0

    #beweeg bal in tegenovergestelde richting op de y as
    def verander_y(self):
        self.snelheid_y *= -1

    #beweeg bal in tegenovergestelde richting op de x as
    def verander_x(self):
        self.snelheid_x *= -1

    def start(self, snelheid_x, snelheid_y):
        self.snelheid_x = snelheid_x
        self.snelheid_y = snelheid_y

    def stop(self):
        self.snelheid_x = 0
        self.snelheid_y = 0

    #plaats de bal in het midden van het scherm
    def reset(self):
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.rect.move_ip(self.snelheid_x, self.snelheid_y)

class Betje(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        #standaardwaarden voor het betje
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((12, 30)).convert()
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)
        self.max_snelheid = 5
        self.snelheid = 0

    def beweeg_omhoog(self):
        self.snelheid = self.max_snelheid * -1

    def beweeg_omlaag(self):
        self.snelheid = self.max_snelheid * 1

    def stop(self):
        self.snelheid = 0

    def update(self):
        self.rect.move_ip(0, self.snelheid)


def main():
    #pygame starten
    pygame.init()

    #game scherm maken
    size = breedte, hoogte = 800, 600
    scherm = pygame.display.set_mode(size)
    pygame.display.set_caption('Tafel tennis')

    try:
        filename = os.path.join(
            os.path.dirname(__file__),
            'bestanden',
            'plaatjes',
            'background.png')
        background = pygame.image.load(filename)
        background = background.convert()
    except pygame.error as e:
        print ('Kan niet laden: ', filename)
        raise SystemExit(str(e))

    betje_links = Betje((breedte/6, hoogte/4))
    betje_rechts = Betje((5*breedte/6, 3*hoogte/4))
    bal = Bal((breedte / 2, hoogte / 2))



    try:
        filename = os.path.join(
            os.path.dirname(__file__),
            'bestanden',
            'fonts',
            'font.ttf')
        font = pygame.font.Font(filename, 90)
    except pygame.error as e:
        print ('Kan niet laden: ', filename)

    links_score = Score(font, (breedte/3, hoogte/8))
    rechts_score = Score(font, (2*breedte/3, hoogte/8))

    sprites = pygame.sprite.Group(
        betje_links, betje_rechts, bal, links_score, rechts_score)

    #zorg dat de game 60 keer per seconde ververst
    clock = pygame.time.Clock()
    fps = 60

    #zorg dat de betjes blijven bewegen, als je de knop ingedrukt houdt
    pygame.key.set_repeat(1, 17)

    bovenkant = pygame.Rect(0, 0, breedte, 5)
    onderkant = pygame.Rect(0, hoogte-5, breedte, 5)
    linkerkant = pygame.Rect(0, 0, 5, hoogte)
    rechterkant = pygame.Rect(breedte-5, 0, 5, hoogte)

    while 1:
        clock.tick(fps)

        betje_links.stop()
        betje_rechts.stop()

        for event in pygame.event.get():
            #als je de game afsluit, ook daadwerkelijk stoppen
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            #als je op w drukt, beweeg het linker betje omhoog
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                betje_links.beweeg_omhoog()
            #als je op s drukt, beweeg het linker betje omlaag
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                betje_links.beweeg_omlaag()
            #als je op pijltje omhoog drukt, beweeg het rechter betje omhoog
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                betje_rechts.beweeg_omhoog()
            #als je op pijltje omlaag drukt, beweeg het rechter betje omlaag
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                betje_rechts.beweeg_omlaag()
            #start de bal met bewegen
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bal.start(randint(1, 3), randint(1, 3))

        #check of de bal en het betje elkaar aanraken
        if bal.rect.colliderect(bovenkant) or bal.rect.colliderect(onderkant):
            bal.verander_y()
        elif (bal.rect.colliderect(betje_links.rect) or
                bal.rect.colliderect(betje_rechts.rect)):
            bal.verander_x()

        screen_rect = scherm.get_rect().inflate(0, -10)
        betje_links.rect.clamp_ip(screen_rect)
        betje_rechts.rect.clamp_ip(screen_rect)

        #als de bal buiten het scherm gaat, doe score omhoog, en reset de bal
        if bal.rect.colliderect(linkerkant):
            rechts_score.score_omhoog()
            bal.reset()
            bal.stop()
        #hezelfde voor de andere kant
        elif bal.rect.colliderect(rechterkant):
            links_score.score_omhoog()
            bal.reset()
            bal.stop()

        sprites.update()

        #zwarte achtergrond
        scherm.blit(background, (0, 0))
        #zorg dat alles op het scherm staat
        sprites.draw(scherm)
        pygame.display.flip()


#start de game loop
if __name__ == '__main__':
    main()