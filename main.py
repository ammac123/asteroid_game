import sys
import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player
from shot import Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_state, log_event

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable) # type: ignore
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    Shot.containers = (updatable, drawable, shots) # type: ignore

    Asteroid.containers = (asteroids, updatable, drawable) # type: ignore
    AsteroidField.containers = (updatable) # type: ignore
    asteroid_field = AsteroidField()

    dt = 0

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        updatable.update(dt)
        
        for _asteroid in asteroids:
            if player.collides_with(_asteroid):
                log_event("player_hit")
                print("Game over!")
                sys.exit(0)

        for _asteroid in asteroids:
            for _shot in shots:
                if _asteroid.collides_with(_shot):
                    log_event("asteroid_shot")
                    _shot.kill()
                    _asteroid.kill()

        for _drawable in drawable:
            _drawable.draw(screen)
        pygame.display.flip()

        # Limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
