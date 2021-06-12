import pygame

from ship import Ship

from pygame.sprite import Group

class Scoreboard():
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.Font("font/ubuntu.ttf", 24)
        self.ships = Group()
        self.prep_ships()

    def prep_score(self):
        score_str = "Current score: " + str(self.stats.score)
        self.score_img = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 10

    def prep_bscore(self):
        best_score_str = "Best score: " + str(self.stats.best_score)
        self.bscore_img = self.font.render(best_score_str, True, self.text_color, self.ai_settings.bg_color)

        self.bscore_rect = self.score_img.get_rect()
        self.bscore_rect.centerx = self.screen_rect.centerx
        self.bscore_rect.top = 10

    def prep_lvl(self):
        lvl_str = "LVL: " + str(self.stats.lvl)
        self.lvl_img = self.font.render(lvl_str, True, self.text_color, self.ai_settings.bg_color)

        self.lvl_rect = self.score_img.get_rect()
        self.lvl_rect.right = self.screen_rect.right - 20
        self.lvl_rect.top = 20 + self.score_rect.height

    def prep_ships(self):
        self.ships.empty()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        self.screen.blit(self.score_img, self.score_rect)

    def show_bscore(self):
        self.screen.blit(self.bscore_img, self.bscore_rect)

    def show_lvl(self):
        self.screen.blit(self.lvl_img, self.lvl_rect)

    def blit_ships(self):
        self.ships.draw(self.screen)