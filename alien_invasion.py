import sys
# Contains modules to monitor for events to exit the game
from time import sleep

import pygame
# Contains gaming modules

from settings import Settings
# Class to manage the screen color and size
from game_stats import GameStats

from ship import Ship
# Class to manage the ship image and actions
from bullet import Bullet
# Class to manage the aliens
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Start game ion active state
        self.game_active = True

        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
    
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
            self.clock.tick(60)
                
    def _check_events(self):
        """ Watch for and respond to keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN: 
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keydown_events(self, event):
        """ Respond to key presses. """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """ Check to see if the key is no longer pressed. """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False     
                    
    def _fire_bullet(self):
        """ Create bullets and add them to the group. """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """ Update postions and remove bullets of the screen. """
        
        # Update positions
        self.bullets.update()

        # Remove bullets that are off the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """ Respond to collisions"""
        # Check to see if any bullets hit the aliens and remove.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
   
    def _ship_hit(self):
        """Respond to the ship being hit"""
        # Decrement number of ships left
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1
        
            # Get rid of anmy remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
            
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep (0.5)

        else:
            self.game_active = False

    def _update_aliens(self):
        """ Chekc for edges and update the positions of the Aliens"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check to see if aliens hit bottom of screen
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """ Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        """ Drop the fleet and change direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _check_aliens_bottom(self):
        """ Check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat same as hit
                self._ship_hit()
                break

    def _create_fleet(self):
        """ Create the fleet ofg aliens."""
        # Create fleet of aliens in rows and add more until there is no room left.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width) - 2 * alien_width:
                self._create_alien(current_x,current_y)
                current_x += 2 * alien_width

            # Finish row and rest x and increment y
            current_x = alien_width
            current_y += 2 * alien_height    

    def _create_alien(self, x_position,y_position):
            """ Create an alien in the row"""
            new_alien = Alien(self)
            new_alien.x = x_position
            new_alien.rect.x = x_position
            new_alien.rect.y = y_position
            self.aliens.add(new_alien)
    
    def _update_screen(self):
        """ Update images on the screen and flip to new screen. """
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        pygame.display.flip()

        
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()