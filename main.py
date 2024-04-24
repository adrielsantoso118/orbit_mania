import pygame
import orbit_mania
import random
import time

class AppMain:
    def __init__(self):
        pygame.init()
        self.world = orbit_mania.World(800, 600)
    
    def run(self):

        pygame.quit()

if __name__ == "__main__":
    app = AppMain()
    app.run()