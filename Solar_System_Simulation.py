import pygame
import math
pygame.init()

WIDTH, HEIGHT = 3000, 1600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

ZOOM_SPEED = 0.1 # How much the zoom changes per key press
MIN_ZOOM = 0.5
MAX_ZOOM = 4.0

GAME_SURFACE = pygame.Surface((WIDTH, HEIGHT))

# Zoom variable
zoom_factor = 0.5

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

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 40 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600*24 # 1 day

    def compute_orbit_path(self):
        updated_points = []
        for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
        return updated_points
    
    def __init__(self, a, e, x, y, radius, color, mass):
        self.a = a
        self.e = e
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def set_elliptical_orbit(self, central_body):
        """
        Sets the planet's position at perihelion and velocity for an elliptical orbit.
        """
        G = Planet.G
        AU = Planet.AU
        M = central_body.mass

        # Perihelion distance
        r_p = self.a * AU * (1 - self.e)
        self.x = r_p
        self.y = 0

        # Velocity at perihelion (all tangential, along -y axis)
        v_p = math.sqrt(G * M * (1 + self.e) / (self.a * AU * (1 - self.e)))
        self.x_vel = 0
        self.y_vel = -v_p

    def draw(self, surface):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            self.orbit_path = self.compute_orbit_path()
            pygame.draw.lines(surface, self.color, False, self.orbit_path, 2)
        
        pygame.draw.circle(surface, self.color, (x, y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def input():
    global zoom_factor
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        # --- ZOOM INPUT ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                zoom_factor += ZOOM_SPEED
            elif event.key == pygame.K_q:
                # Zoom Out (Decrease zoom factor)
                zoom_factor -= ZOOM_SPEED
    
    # Clamp the zoom factor to prevent it from going too far
    zoom_factor = max(MIN_ZOOM, min(MAX_ZOOM, zoom_factor))

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 0, 0, 10, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    mercury = Planet(0.387, 0.2056, 0.387 * Planet.AU, 0, 4, GREY, 3.3010 * 10**23)
    mercury.y_vel = -47.87 * 1000

    venus = Planet(0.723, 0.0068, 0.723 * Planet.AU, 0, 8, LIGHT_BROWN, 4.8673 * 10**24)
    venus.y_vel = -35.02 * 1000

    earth = Planet(1.000, 0.0167, 1 * Planet.AU, 0, 8, BLUE, 5.9722 * 10**24)
    earth.y_vel = 29.78 * 1000

    mars = Planet(1.524, 0.0934, 1.524 * Planet.AU, 0, 4, RED, 6.4169 * 10**23)
    mars.y_vel = 24.007 * 1000

    jupiter = Planet(5.203, 0.0484, 5.203 * Planet.AU, 0, 12, BROWN, 1.8981 * 10**27)
    jupiter.y_vel = 13.07 * 1000

    saturn = Planet(9.582, 0.0542, 9.582 * Planet.AU, 0, 12, YELLOW, 5.6832 * 10**26)
    saturn.y_vel = 9.69 * 1000

    uranus = Planet(19.201, 0.0472, 19.201 * Planet.AU, 0, 8, LIGHT_BLUE, 8.6810 * 10**25)
    uranus.y_vel = 6.81 * 1000

    neptune = Planet(30.047, 0.0086, 30.047 * Planet.AU, 0, 8, DARK_BLUE, 1.0241 * 10**26)
    neptune.y_vel = 5.43 * 1000

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
    
    for planet in [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]:
        planet.set_elliptical_orbit(sun)

    while run:
        clock.tick(60)

        input()

        GAME_SURFACE.fill((0,0,0))
        for planet in planets:
            planet.update_position(planets)
            planet.draw(GAME_SURFACE)

        new_width = int(WIDTH * zoom_factor)
        new_height = int(HEIGHT * zoom_factor)
        scaled_surface = pygame.transform.smoothscale(GAME_SURFACE, (new_width, new_height))
        WIN.fill((50, 50, 50))
        x_offset = (WIDTH - new_width) // 2
        y_offset = (HEIGHT - new_height) // 2
        WIN.blit(scaled_surface, (x_offset, y_offset))
        
        pygame.display.update()

    pygame.quit()

main()