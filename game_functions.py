import sys
import pygame

from bullet import Bullet
from alien import Alien

from time import sleep

pygame.mixer.init()

sfx_ship_dead = pygame.mixer.Sound("sfx/ship_dead.mp3")
sfx_alien_dead = pygame.mixer.Sound("sfx/alien_dead.mp3")
sfx_alien_dead.set_volume(0.1)
sfx_ship_dead.set_volume(0.3)

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	""" Обработка нажатия клавиши """
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()

def check_keyup_events(event, ship):
	""" Обработка отпускания клавиши """
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets, stats, button, aliens, sb):
	""" Обрабатывает нажатия клавиш и события мыши """
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, button, ship, aliens, bullets, mouse_x, mouse_y, sb)

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sb):
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False)

		stats.reset_stats()
		stats.game_active = True

		sb.prep_ships()

		aliens.empty()
		bullets.empty()

		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

def fire_bullet(ai_settings, screen, ship, bullets):
	""" Выпускает пулю, если не достигнут лимит """
	# Создает новую пулю и добавляет её в группу
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def update_screen(ai_settings, screen, stats, ship, aliens, bullets, button, sb, bg):
	"""Обновляет изображения на экране и отображает новый экран"""
	# При каждом проходе цикла перерисовывает экран
	screen.fill(ai_settings.bg_color)
	screen.blit(bg.image, bg.rect)

	# Перернисовывает пули позади корабля и пришельцов
	for bullet in bullets.sprites():
		bullet.draw_bullet()

	sb.prep_score()
	sb.show_score()

	sb.prep_bscore()
	sb.show_bscore()

	sb.prep_lvl()
	sb.show_lvl()

	sb.blit_ships()

	# Отрисовка корабля
	ship.blitme()

	# Отрисовка пришельцев
	aliens.draw(screen)

	if not stats.game_active:
		button.draw_button()

	# Отображение последнего прорисованного экрана
	pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets, stats):
	# Обновление позиции пули
	bullets.update()

	# Избавление от пуль, которые вышли за пределы игрового окна
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats):
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		sfx_alien_dead.play()
		stats.score += stats.alien_score
		stats.increase_best_score()

	if len(aliens) == 0:
		bullets.empty()
		ai_settings.increase_speed()
		stats.lvl += 1
		create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings, alien_width):
	""" Вычисление количества пришельцев в ряду """
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (alien_width * 2))

	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	""" Определение количества рядов, помещающихся на экране """
	available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height)) - 1

	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x

	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number

	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	""" Создает флот пришельцев """
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			# Создание пришельца и размещение его в ряду
			create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
	""" Обновляет позиции всех пришельцев во флоте """
	aliens.update()
	check_fleet_edges(ai_settings, aliens)

	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)

	check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
	if stats.ships_left > 0:
		# Уменьшение ships_left
		stats.ships_left -= 1
		sb.prep_ships()
		# Очистка пришельцев и пуль
		aliens.empty()
		bullets.empty()

		# Создание нового флота и размещение корабля в центре
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		# Пауза + zvuk
		sfx_ship_dead.play()
		sleep(2)
	else:
		sfx_ship_dead.play()
		sleep(2)
		stats.game_active = False
		stats.score = 0
		stats.lvl = 1
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
			break