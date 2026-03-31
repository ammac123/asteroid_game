import random
import pygame
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from circleshape import CircleShape
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius) -> None:
        super().__init__(x, y, radius)
        self.mass = radius ** 3

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        split_angle = random.randint(20, 50)
        asteroid_1_velocity = self.velocity.rotate(split_angle) # type: ignore
        asteroid_2_velocity = self.velocity.rotate(-split_angle) # type: ignore
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        axis = (asteroid_1_velocity - asteroid_2_velocity).normalize()
        offset = axis * new_radius
        asteroid_1 = Asteroid(self.position.x + offset.x, self.position.y + offset.y, new_radius) # type: ignore
        asteroid_2 = Asteroid(self.position.x - offset.x, self.position.y - offset.y, new_radius) # type: ignore
        asteroid_1.velocity = asteroid_1_velocity * 1.2
        asteroid_2.velocity = asteroid_2_velocity * 1.2

    def collision(self, other):
        if not isinstance(other, Asteroid):
            return
        if self.position == other.position:
            return
        relative_velocity = self.velocity - other.velocity
        normal = (self.position - other.position).normalize() # type: ignore
        vel_along_normal = normal.dot(relative_velocity)
        if vel_along_normal > 0:
            return
        impulse = (2 * vel_along_normal) / (self.mass + other.mass)

        self.velocity -= impulse * other.mass * normal * 1.2
        other.velocity += impulse * self.mass * normal * 1.2