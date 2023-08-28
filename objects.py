import math

import pygame as pg

k = 10 ** 9
E_not = 8.85 * 10 ** -12
Mew_not = 4 * math.pi * 10 ** -7


class Test_Charge:
    def __init__(self, coords: tuple, surface: pg.surface, radius=5, mass=10, charge=1) -> None:
        self.pos = pg.Vector2(coords[0], coords[1])
        self.surface = surface
        self.radius = radius
        self.mass = mass
        self.charge = charge
        self.vel = pg.Vector2(0, 0)

    def update(self) -> None:
        self.border_collision()
        self.pos += self.vel
        pg.draw.circle(self.surface, "Red", (self.pos[0], self.pos[1]), self.radius)

    def rect(self) -> object:
        return pg.draw.circle(self.surface, "Red", (self.pos[0], self.pos[1]), self.radius)

    def border_collision(self) -> None:
        if self.pos[0] >= self.surface.get_width() - self.radius:
            self.pos[0] = self.surface.get_width() - self.radius
            self.vel[0] *= -1
        if self.pos[0] <= self.radius:
            self.pos[0] = self.radius
            self.vel[0] *= -1
        if self.pos[1] >= self.surface.get_height() - self.radius:
            self.pos[1] = self.surface.get_height() - self.radius
            self.vel[1] *= -1
        if self.pos[1] <= self.radius:
            self.pos[1] = self.radius
            self.vel[1] *= -1


class Electron:
    def __init__(self, coords: tuple, surface: pg.surface, radius=3, mass=9.1 * 10 ** -31,
                 charge=-1.6 * 10 ** -19) -> None:
        self.pos = pg.Vector2(coords[0], coords[1])
        self.surface = surface
        self.radius = radius
        self.mass = mass
        self.charge = charge
        self.vel = pg.Vector2(0, 0)

    def update(self) -> None:
        self.border_collision()
        self.pos += self.vel
        pg.draw.circle(self.surface, "Green", (self.pos[0], self.pos[1]), self.radius)

    def rect(self) -> object:
        return pg.draw.circle(self.surface, "Green", (self.pos[0], self.pos[1]), self.radius)

    def border_collision(self) -> None:
        if self.pos[0] >= self.surface.get_width() - self.radius:
            self.pos[0] = self.surface.get_width() - self.radius
            self.vel[0] *= -1
        if self.pos[0] <= self.radius:
            self.pos[0] = self.radius
            self.vel[0] *= -1
        if self.pos[1] >= self.surface.get_height() - self.radius:
            self.pos[1] = self.surface.get_height() - self.radius
            self.vel[1] *= -1
        if self.pos[1] <= self.radius:
            self.pos[1] = self.radius
            self.vel[1] *= -1


class Proton:
    def __init__(self, coords: tuple, surface: pg.surface, radius=1, mass=1.67 * 10 ** -27,
                 charge=1.6 * 10 ** -19) -> None:
        self.pos = pg.Vector2(coords[0], coords[1])
        self.surface = surface
        self.radius = radius
        self.mass = mass
        self.charge = charge
        self.vel = pg.Vector2(0, 0)

    def update(self) -> None:
        self.border_collision()
        self.pos += self.vel
        pg.draw.circle(self.surface, "Yellow", (self.pos[0], self.pos[1]), self.radius)

    def rect(self) -> object:
        return pg.draw.circle(self.surface, "Yellow", (self.pos[0], self.pos[1]), self.radius)

    def border_collision(self) -> None:
        if self.pos[0] >= self.surface.get_width() - self.radius:
            self.pos[0] = self.surface.get_width() - self.radius
            self.vel[0] *= -1
        if self.pos[0] <= self.radius:
            self.pos[0] = self.radius
            self.vel[0] *= -1
        if self.pos[1] >= self.surface.get_height() - self.radius:
            self.pos[1] = self.surface.get_height() - self.radius
            self.vel[1] *= -1
        if self.pos[1] <= self.radius:
            self.pos[1] = self.radius
            self.vel[1] *= -1


class Stationary_Charged_Particle:
    def __init__(self, surface: pg.surface, coords: tuple, radius: int, mass: float, charge: float) -> None:
        self.surface = surface
        self.radius = radius
        self.mass = mass
        self.charge = charge
        self.pos = pg.Vector2(coords[0], coords[1])

    def update(self) -> None:
        pg.draw.circle(self.surface, "Blue", (self.pos[0], self.pos[1]), self.radius)

    def acting_field(self, acting_particle: Test_Charge or Electron or Proton) -> None:  # updates the pos of particle
        r_dist = acting_particle.pos - self.pos
        if r_dist.length() <= math.fabs(acting_particle.radius - self.radius):
            acting_particle.vel = pg.Vector2(0, 0)
        else:
            field = ((k * self.charge) / r_dist.length() ** 2) * r_dist.normalize()
            force = field * acting_particle.charge
            acting_particle.vel += force / acting_particle.mass


class Parallel_Plate_Capacitor:
    def __init__(self, surface: pg.surface, coords: tuple, thickness: float, platelength: float,
                 charge_held: float) -> None:
        self.surface = surface
        self.center_pos = pg.Vector2(coords[0], coords[1])
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
        dist_vect = (pg.Vector2(self.center_pos[0] - (self.thickness / 2), self.center_pos[1]) - pg.Vector2(
            self.center_pos[0] + (self.thickness / 2), self.center_pos[1]))
        field = (-potential / self.thickness) * dist_vect.normalize()
        force = field * acting_particle.charge  # force acting on particle
        acting_particle.vel += force / acting_particle.mass
