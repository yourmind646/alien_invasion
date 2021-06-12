import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from background import Background

import game_functions as gf

try:
	pygame.mixer.music.load("sfx/bg_music.mp3")
except:
	pass

def run_game():
	# Инициализирует pygame, settings и объект экрана.
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")

	button = Button(ai_settings, screen, "Play")

	# Создание корабля, группы пуль и группы пришельцев
	ship = Ship(ai_settings, screen)
	bullets = Group()
	aliens = Group()

	stats = GameStats(ai_settings)

	sb = Scoreboard(ai_settings, screen, stats)

	bg = Background()

	# Создание флота пришельцев
	gf.create_fleet(ai_settings, screen, ship, aliens)

	# Запуск основного цикла игры.
	while True:
		gf.check_events(ai_settings, screen, ship, bullets, stats, button, aliens, sb)

		if stats.game_active:
			ship.update()

			gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats)

			gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb)

		gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, button, sb, bg)
try:
	pygame.mixer.music.play(-1)
except:
	pass
run_game()