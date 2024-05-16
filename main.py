import pygame
import math
import random
import time
import orbit_mania

class AppMain:
    def __init__(self):
        pygame.init()
        self.world = orbit_mania.World(800, 600)
        self.planet = orbit_mania.Planet(self.world.planet_image, (self.world.width // 2, self.world.height // 2))
        self.fuel_bar = orbit_mania.FuelBar(self.world, 100, 10, 10)
        self.player = orbit_mania.Player(self.world.player_image, self.planet, self.world.shield_image, self.fuel_bar)
        self.obstacles = pygame.sprite.Group()
        self.energy_packets = pygame.sprite.Group()
        self.stopwatch = pygame.time.Clock()
        self.start_time = time.time()
        self.last_obstacle_time = 0
        self.last_packet_time = 0
    
    def format_time(self, elapsed_time):
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        return "{:02}:{:02}".format(minutes, seconds)

    def add_obstacle(self):
        x = random.randint(self.world.width, self.world.width * 2)
        y = random.randint(0, self.world.height)
        speed = random.randint(1, 2)
        obstacle = orbit_mania.Obstacle(self.world.obstacle_image, x, y, speed, self.world)
        self.obstacles.add(obstacle)

    def add_energy_packet(self):
        if len(self.energy_packets) < 5:
            random_radius = random.choice([125, 225])
            random_angle = random.randint(0, 35) * 10 # random_angle = 0, 10, ..., 350
            x = self.planet.rect.centerx + random_radius * math.cos(math.radians(random_angle))
            y = self.planet.rect.centery + random_radius * math.sin(math.radians(random_angle))
            energy_packet = orbit_mania.EnergyPacket(self.world.energy_packet_image, x, y, self.fuel_bar)
            self.energy_packets.add(energy_packet)
    
    def run(self):
        # Game initialization
        running = True
        game_ended = False

        # Game loop
        while running:
            elapsed_time = time.time() - self.start_time

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        if self.player.radius <= 126:
                            self.player.radius = 125
                            self.player.change_radius(225)
                        elif self.player.radius >= 224:
                            self.player.radius = 225
                            self.player.change_radius(125)
                    if event.key == pygame.K_s:
                        self.player.activate_shield()
                        self.world.activate_shield_sound.play()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_s:
                        self.player.deactivate_shield()

            # Update number of obstacles
            if time.time() - self.last_obstacle_time >= 3:
                self.add_obstacle()
                self.last_obstacle_time = time.time()
            
            # Update number of energy packets
            if time.time() - self.last_packet_time >= 5:
                self.add_energy_packet()
                self.last_packet_time = time.time()

            # Update objects
            self.player.update()
            self.obstacles.update()
            self.energy_packets.update()
            if self.player.shield_active == True:
                self.fuel_bar.update(-0.2)
            else:
                self.fuel_bar.update(-0.05)

            # Energy refill condition
            energy_collisions = pygame.sprite.spritecollide(self.player, self.energy_packets, True)
            for packet in energy_collisions:
                self.world.energy_packet_sound.play()
                self.fuel_bar.update(20) # Increase fuel by 20 when collecting an energy packet
            
            # Game over condition
            if pygame.sprite.spritecollide(self.player, self.obstacles, True) and not self.player.shield.active:
                game_ended = True
            if self.fuel_bar.current_fuel <= 0:
                game_ended = True
            
            if game_ended == True:
                # Stop background music
                pygame.mixer.music.stop()

                # Game over explosion effect
                explosion_rect = self.world.explosion_image.get_rect(center=self.player.rect.center)
                self.world.screen.blit(self.world.explosion_image, explosion_rect)             

                # Clear screen
                pygame.display.flip()
                pygame.time.wait(500)
                self.world.screen.blit(self.world.background_image, (0, 0))

                # Game over sound
                self.world.game_over_sound.play()

                # Game over text
                game_over_text = self.world.large_font.render("GAME OVER", True, pygame.color.Color("white"))
                text_rect = game_over_text.get_rect(center=(self.world.width // 2, self.world.height // 2))
                self.world.screen.blit(game_over_text, text_rect)

                # Last time text
                last_time_text = self.world.small_font.render("Last Time: " + self.format_time(elapsed_time), True, pygame.color.Color("white"))
                last_time_rect = last_time_text.get_rect(center=(self.world.width // 2, self.world.height // 2 + 50))
                self.world.screen.blit(last_time_text, last_time_rect)
                
                pygame.display.flip()
                pygame.time.wait(4000) # 4 seconds
                break

            # Draw objects
            self.world.screen.blit(self.world.background_image, (0, 0))
            self.planet.draw_orbit(self.world.screen, 125, pygame.color.Color("white"))
            self.planet.draw_orbit(self.world.screen, 225, pygame.color.Color("white"))
            self.world.screen.blit(self.planet.image, self.planet.rect)
            if self.player.shield.active:
                shield_rect = self.player.shield.image.get_rect(center=self.player.rect.center)
                self.world.screen.blit(self.player.shield.image, shield_rect)
            self.world.screen.blit(self.player.image, self.player.rect)
            self.obstacles.draw(self.world.screen)
            self.energy_packets.draw(self.world.screen)
            
            # Draw fuel bar text
            fuel_bar_text = self.world.small_font.render("Fuel", True, (255, 255, 255))
            text_rect = fuel_bar_text.get_rect(topleft=(self.fuel_bar.x + 10, self.fuel_bar.y))
            self.world.screen.blit(fuel_bar_text, text_rect)

            # Draw fuel bar icon
            fill_width = int(self.fuel_bar.width * (self.fuel_bar.current_fuel / self.fuel_bar.max_fuel))
            pygame.draw.rect(self.world.screen, self.fuel_bar.border_color, (self.fuel_bar.x + 10, self.fuel_bar.y + 30, self.fuel_bar.width, self.fuel_bar.height), 3)
            pygame.draw.rect(self.world.screen, self.fuel_bar.fill_color, (self.fuel_bar.x + 10, self.fuel_bar.y + 30, fill_width, self.fuel_bar.height))
            
            # Draw stopwatch text
            time_text = self.world.large_font.render(self.format_time(elapsed_time), True, (255, 255, 0))
            time_rect = time_text.get_rect(topright=(self.world.width - 10, 10))
            self.world.screen.blit(time_text, time_rect)

            pygame.display.flip()
            self.stopwatch.tick(60)

        pygame.quit()

if __name__ == "__main__":
    app = AppMain()
    app.run()
