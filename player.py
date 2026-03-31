import pygame
from constants import (
    PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, 
    PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, LINE_WIDTH
    )
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH) # type: ignore

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)

        # Shooting
        if self.shot_cooldown > 0:
            self.shot_cooldown -= dt
        if keys[pygame.K_SPACE]:
            if self.shot_cooldown <= 0:
                self.shoot()
                self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius   # type: ignore
        b = self.position - forward * self.radius - right # type: ignore
        c = self.position - forward * self.radius + right # type: ignore
        return [a, b, c]
    
    def shoot(self):
        shot = Shot(self.position.x, self.position.y) # type: ignore
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED