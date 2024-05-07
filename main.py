from objects import *
import pygame as pg

pg.init()

screen = pg.display.set_mode((1000, 900))
clock = pg.time.Clock()

objs = []  # list of all objects

stat_count = 0  # count of static charged object
test_ch_count = 0  # count of test charge objects
electron_count = 0  # count of electron objects
proton_count = 0  # count of proton objects
capacitor_count = 0  # count of capacitors
current_wire_count = 0  # count of wires

stat_ch_part = {}  # collection of statically charged particles
acting_parts = {}  # collection of all acting particles
capacitors_objs = {}  # collection of capacitors
wire_objs = {}  # collection of wires

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        if event.type == pg.MOUSEBUTTONDOWN:  # keys to deploy physical quantities
            stat_count += 1
            stat_ch_part[f'static_particle_{stat_count}'] = Stationary_Charged_Particle(screen, pg.mouse.get_pos(), 10,
                                                                                        20, 1 * 10 ** -5)
            objs.append(stat_ch_part[f'static_particle_{stat_count}'])

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_c:
                capacitor_count += 1
                capacitors_objs[f'Capacitor_{capacitor_count}'] = Parallel_Plate_Capacitor(screen, pg.mouse.get_pos(),
                                                                                           700, 500, 2 * 10 ** -9)
                objs.append(capacitors_objs[f'Capacitor_{capacitor_count}'])

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_t:
                test_ch_count += 1
                acting_parts[f'Test_charge_{test_ch_count}'] = Test_Charge(pg.mouse.get_pos(), screen)
                objs.append(acting_parts[f'Test_charge_{test_ch_count}'])

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                electron_count += 1
                acting_parts[f'Electron_particle_{electron_count}'] = Electron(pg.mouse.get_pos(), screen)
                objs.append(acting_parts[f'Electron_particle_{electron_count}'])

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                proton_count += 1
                acting_parts[f'Proton_particle_{proton_count}'] = Proton(pg.mouse.get_pos(), screen)
                objs.append(acting_parts[f'Proton_particle_{proton_count}'])

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_b:
                current_wire_count += 1
                wire_objs[f'Current_wire_{current_wire_count}'] = Current_wire(pg.mouse.get_pos(), screen)
                objs.append(wire_objs[f'Current_wire_{current_wire_count}'])

    screen.fill('black')

    if len(acting_parts) >= 1:
        iterated = []
        for test_charge in acting_parts:  # arbitrary particle in all acting particles

            if acting_parts[test_charge].check():  # primary constraint to check if particle1 within bounds

                for other_charge in acting_parts:  # mutual acting force on each particle

                    if other_charge != test_charge:

                        if acting_parts[other_charge].check():  # primary constraint to check if particle2 within bounds

                            if (test_charge, other_charge) not in iterated and (
                                    other_charge, test_charge) not in iterated:  # to prevent many iterations

                                acting_force(acting_parts[test_charge], acting_parts[other_charge])  # calculates force
                                iterated.append((test_charge, other_charge))

                if stat_count >= 1:  # when a stat_charge present
                    for i in stat_ch_part.values():
                        i.acting_field(acting_parts[test_charge])

                if capacitor_count >= 1:  # when a capacitor present
                    for i in capacitors_objs.values():
                        if i.collision(acting_parts[test_charge]):
                            i.acting_plate_field(acting_parts[test_charge])

                if current_wire_count >= 1:  # when a current wire present
                    for i in wire_objs.values():
                        i.acting_mag_field(acting_parts[test_charge])

    for i in objs:  # to draw all objects
        if i in acting_parts.values():
            if not i.check():
                objs.remove(i)

        i.update()

    clock.tick(360)
    pg.display.flip()
