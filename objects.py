import math

import pygame as pg

k = 10 ** 9
E_not = 8.85 * 10 ** -12
Mew_not = 4 * math.pi * 10 ** -7


class Test_Charge:
    def __init__(self, coords: tuple, surface: pg.surface, radius=5, mass=1, charge=10 ** -3) -> None:
        self.pos = pg.Vector3(coords[0], coords[1], 0)
        self.surface = surface
        self.radius = radius
        self.mass = mass
        self.charge = charge
        self.vel = pg.Vector3(0, 0, 0)

    def update(self) -> None:
        self.pos += self.vel
        pg.draw.circle(self.surface, "Red", (self.pos[0], self.pos[1]), self.radius)

    def rect(self) -> object:
        return pg.draw.circle(self.surface, "Red", (self.pos[0], self.pos[1]), self.radius)

    def check(self):  # checks boundary
        if 0 < self.pos.x < 1000 and 0 < self.pos.y < 900:
            return True


class Electron:
    def __init__(self, coords: tuple, surface: pg.surface, radius=5, mass=9.1 * 10 ** -31,
                 charge=-1.6 * 10 ** -19) -> None:
        self.pos = pg.Vector3(coords[0], coords[1], 0)
        self.surface = surface
        self.radius = radius
        self.mass = mass
        self.charge = charge
        self.vel = pg.Vector3(0, 0, 0)

    def update(self) -> None:
        self.pos += self.vel
        pg.draw.circle(self.surface, "Green", (self.pos[0], self.pos[1]), self.radius)

    def rect(self) -> object:
        return pg.draw.circle(self.surface, "Green", (self.pos[0], self.pos[1]), self.radius)

    def check(self):  # checks boundary
        if 0 < self.pos.x < 1000 and 0 < self.pos.y < 900:
            return True


class Proton:
    def __init__(self, coords: tuple, surface: pg.surface, radius=5, mass=9.1 * 10 ** -31,
                 charge=1.6 * 10 ** -19) -> None:
        self.pos = pg.Vector3(coords[0], coords[1], 0)
        self.surface = surface
        self.radius = radius
        self.mass = mass
        self.charge = charge
        self.vel = pg.Vector3(0, 0, 0)

    def update(self) -> None:
        self.pos += self.vel
        pg.draw.circle(self.surface, "Yellow", (self.pos[0], self.pos[1]), self.radius)

    def rect(self) -> object:
        return pg.draw.circle(self.surface, "Yellow", (self.pos[0], self.pos[1]), self.radius)

    def check(self):  # checks boundary
        if 0 < self.pos.x < 1000 and 0 < self.pos.y < 900:
            return True


class Stationary_Charged_Particle:
    def __init__(self, surface: pg.surface, coords: tuple, radius: int, mass: float, charge: float) -> None:
        self.surface = surface
        self.radius = radius
        self.mass = mass
        self.charge = charge
        self.pos = pg.Vector3(coords[0], coords[1], 0)

    def update(self) -> None:
        pg.draw.circle(self.surface, "Blue", (self.pos[0], self.pos[1]), self.radius)

    def acting_field(self, acting_particle: Test_Charge or Electron or Proton) -> None:  # updates the pos of particle
        r_dist = acting_particle.pos - self.pos
        if r_dist.length() <= math.fabs(acting_particle.radius - self.radius):
            acting_particle.vel = pg.Vector3(0, 0, 0)
        else:
            field = ((k * self.charge) / r_dist.length() ** 2) * r_dist.normalize()
            force = field * acting_particle.charge
            acting_particle.vel += force / acting_particle.mass


class Parallel_Plate_Capacitor:
    def __init__(self, surface: pg.surface, coords: tuple, thickness: float, platelength: float,
                 charge_held: float) -> None:
        self.surface = surface
        self.center_pos = pg.Vector3(coords[0], coords[1], 0)
        self.thickness = thickness
        self.plate_length = platelength
        self.charge = charge_held
        self.capac = platelength * 1 * E_not / thickness
        self.field_enclosure = pg.Rect(self.center_pos[0] - (self.thickness / 2),
                                       self.center_pos[1] - self.plate_length / 2, self.thickness, self.plate_length)

    def update(self) -> None:
        pg.draw.line(self.surface, 'white',
                     [self.center_pos[0] - (self.thickness / 2),
                      self.center_pos[1] + self.plate_length / 2],
                     [self.center_pos[0] - self.thickness / 2,
                      self.center_pos[1] - self.plate_length / 2])  # left plate
        pg.draw.line(self.surface, 'white',
                     [self.center_pos[0] + (self.thickness / 2),
                      self.center_pos[1] + self.plate_length / 2],
                     [self.center_pos[0] + self.thickness / 2,
                      self.center_pos[1] - self.plate_length / 2])  # Right plate

    def collision(self, other: Test_Charge or Electron or Proton) -> bool:  # checks if non-static particle is present
        return self.field_enclosure.colliderect(other.rect())

    def acting_plate_field(self,
                           acting_particle: Test_Charge or Electron or Proton) -> None:  # updates the pos of particle
        potential = self.charge / self.capac
        dist_vect = (pg.Vector3(self.center_pos[0] - (self.thickness / 2), self.center_pos[1], 0) - pg.Vector3(
            self.center_pos[0] + (self.thickness / 2), self.center_pos[1], 0))
        field = (-potential / self.thickness) * dist_vect.normalize()
        force = field * acting_particle.charge  # force acting on particle
        acting_particle.vel += force / acting_particle.mass


class Current_wire:
    def __init__(self, coords: tuple, surface: pg.Surface, current=2*10**10, length=1000):
        self.center_pos = pg.Vector3(coords[0], coords[1], 0)
        self.surface = surface
        self.current = current
        self.length = length
        self.bottom = pg.Vector3(self.center_pos.x + self.length / 2, self.center_pos.y + self.length / 2, 0)
        self.top = pg.Vector3(self.center_pos.x - self.length / 2, self.center_pos.y - self.length / 2, 0)

    def update(self) -> None:
        pg.draw.line(self.surface, (0, 255, 255),
                     (self.center_pos.x , self.center_pos.y + (self.length / 2)),
                     (self.center_pos.x , self.center_pos.y - (self.length / 2)))

    def collision(self, acting_part: Electron or Proton or Test_Charge):  # To confirm position of particle
        if self.top.y < acting_part.pos.y < self.bottom.y:
            return 0

    def acting_mag_field(self, acting_part: Electron or Proton or Test_Charge):
        if self.collision(acting_part) == 0:  # When within the wire range
            perpend_dist_x = (acting_part.pos - self.center_pos).x
            perpend_dist_y = (acting_part.pos - self.center_pos).y

            if acting_part.pos.y < self.center_pos.y:  # When above the center position
                sin_1 = ((acting_part.pos - self.top).magnitude() / ((self.length / 2) - perpend_dist_y)) ** -1
                sin_2 = ((acting_part.pos - self.top).magnitude() / ((self.length / 2) + perpend_dist_y)) ** -1

                mag_field = pg.Vector3(0, 0, -1 * (Mew_not / (4 * math.pi)) * (self.current / perpend_dist_x) * (
                        sin_1 + sin_2))
                mag_force = (acting_part.vel.cross(mag_field)) * acting_part.charge
                acting_part.vel += mag_force / acting_part.mass

            if acting_part.pos.y > self.center_pos.y:  # when bellow the center position

                sin_1 = ((acting_part.pos - self.top).magnitude() / ((self.length / 2) + perpend_dist_y)) ** -1
                sin_2 = ((acting_part.pos - self.top).magnitude() / ((self.length / 2) - perpend_dist_y)) ** -1

                mag_field = pg.Vector3(0, 0, -1 * (Mew_not / (4 * math.pi)) * (self.current / perpend_dist_x) * (
                        sin_1 + sin_2))
                mag_force = (acting_part.vel.cross(mag_field)) * acting_part.charge
                acting_part.vel += mag_force / acting_part.mass

            if acting_part.pos.y == self.center_pos.y:  # at center position
                sin_1 = ((acting_part.pos - self.top).magnitude() / (self.length / 2)) ** -1
                sin_2 = ((acting_part.pos - self.top).magnitude() / (self.length / 2)) ** -1

                mag_field = pg.Vector3(0, 0, -1 * (Mew_not / (4 * math.pi)) * (self.current / perpend_dist_x) * (
                        sin_1 + sin_2))
                mag_force = (acting_part.vel.cross(mag_field)) * acting_part.charge
                acting_part.vel += mag_force / acting_part.mass


def acting_force(acting_particle1: Test_Charge or Electron or Proton,
                 acting_particle2: Test_Charge or Electron or Proton) -> None:
    if acting_particle1.check() and acting_particle2.check():
        r_dist12 = acting_particle1.pos - acting_particle2.pos
        r_dist21 = acting_particle2.pos - acting_particle1.pos
        f21 = (k * acting_particle2.charge * acting_particle1.charge / (r_dist21.length()) ** 2) * r_dist21.normalize()
        f12 = (k * acting_particle2.charge * acting_particle1.charge / (r_dist12.length()) ** 2) * r_dist12.normalize()
    else:
        f21 = pg.Vector2(0, 0)
        f12 = pg.Vector2(0, 0)

    acting_particle1.vel += f12 / acting_particle1.mass
    acting_particle2.vel += f21 / acting_particle2.mass
