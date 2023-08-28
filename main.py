from objects import *
import pygame as pg

pg.init()

screen = pg.display.set_mode((1000, 900))
clock = pg.time.Clock()

stat_count = 1  # count of static charged object
test_ch_count = 1  # count of test charge objects
electron_count = 0  # count of electron objects
proton_count = 0  # count of proton objects
capacitor_count = 0  # count of capacitors

stat_ch_part = {}  # collection of statically charged particles
test_ch = {}  # collection of test charges
electron_part = {}  # collection of electrons
proton_part = {}  # collection of protons
capacitors_objs = {}  # collection of capacitors

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            stat_count += 1
            # stat_ch_part[f'static_particle_{stat_count}']=Stationary_Charged_Particle(screen,pg.mouse.get_pos(),10,20,15*10**-6)

    screen.fill('black')
    '''for i in stat_ch_part.values(): #to draw the objects
        i.update()'''

    if len(stat_ch_part) >= 1 and len(test_ch) > 0:
        for i in stat_ch_part.values():
            for j in test_ch.values():
                i.acting_field(j)

    clock.tick(120)
    pg.display.flip()
