import pygame
import math

class World():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))

        # Load images
        self.background_image = pygame.image.load("background.png")
        self.planet_image = pygame.image.load("planet.png")
        self.player_image = pygame.image.load("player.png")
        self.obstacle_image = pygame.image.load("obstacle.png")
        self.explosion_image = pygame.image.load("explosion.png")

        # Application
        pygame.display.set_caption("Orbit Mania")

class Planet():
    def __init__(self, image, center):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=center)

    def draw_orbit(self, screen, radius, color):
        pygame.draw.circle(screen, color, self.rect.center, radius, width=1)

class Player():
    pass

class Obstacle():
    pass