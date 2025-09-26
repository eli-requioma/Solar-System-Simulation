import pygame
import math
pygame.init()

WIDTH, HEIGHT = 1500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255,255,255)
ORANGE = (242,131,32)
GREY = (141,138,136)
LIGHT_BROWN = (244,219,196)
BLUE = (70, 139, 172)
RED = (232,57,54)
BROWN = (166,112,92)
YELLOW = (243,206,136)
LIGHT_BLUE = (208,236,240)
DARK_BLUE = (70,104,166)

class Planet:
    AU = 149.6e6 * 1000 #distance from sun in meters
    G = 6.67426e-11
    SCALE = 15 / AU #approx smaller scale of AU 
    TIMESTEP = 3600 * 24 # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass #in kg

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        pygame.draw.circle(win, self.color, (x,y), self.radius)

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 4, ORANGE, 1.98892 * 10**30) #the sun
    sun.sun = True

    #the planets:
    mercury = Planet(0.387 * Planet.AU, 0, 1, GREY, 3.3010 * 10**23)
    venus = Planet(0.723 * Planet.AU, 0, 2, LIGHT_BROWN, 4.8673 * 10**24)
    earth = Planet(1 * Planet.AU, 0, 2, BLUE, 5.9722 * 10**24)
    mars = Planet(1.524 * Planet.AU, 0, 1, RED, 6.4169 * 10**23)
    jupiter = Planet(5.203 * Planet.AU, 0, 3, BROWN, 1.8981 * 10**27)
    saturn = Planet(9.582 * Planet.AU, 0, 3, YELLOW, 5.6832 * 10**26)
    uranus = Planet(19.201 * Planet.AU, 0, 2, LIGHT_BLUE, 8.6810 * 10**25)
    neptune = Planet(30.047 * Planet.AU, 0, 2, DARK_BLUE, 1.0241 * 10**26)

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.draw(WIN)

    pygame.quit()

main()