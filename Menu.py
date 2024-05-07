import pygame as pg


class Menu:
    def __init__(self):
        self.disp = pg.display.set_mode((900,900))

        self.screen = pg.Surface((300,300))
        self.screen.set_colorkey((255,0,0))

        x= pg.Vector3(0,0,50)
        y= pg.Vector3(0,5)

        keys = []

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                if event.type == pg.KEYDOWN:
                    keys.append(event.key)

                if event.type == pg.KEYUP:
                    keys.remove(event.key)

            if pg.K_m in keys:
                print('yes')
                self.disp.blit(self.screen, (200,200))

            print(x.cross(y))

            pg.display.flip()

    def update(self):
        return self.screen

Menu()