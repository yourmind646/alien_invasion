class Settings():
	""" Класс для хранения всех настроек игры Alien Invasion """

	def __init__(self):
		""" Инициализирует настройки игры """       
		# Параметры экрана
		self.screen_width = 1100
		self.screen_height = 600
		self.bg_color = (230, 230, 230)
		
		# Параметры корабля
		self.ship_limit = 3

		# Параметры пули
		self.bullet_width = 3
		self.bullet_height = 15        
		self.bullet_color = 255, 255, 255
		self.bullets_allowed = 3

		# Параметры пришельцев
		self.fleet_drop_speed = 5

		self.speedup_scale = 1.1

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		self.ship_speed_factor = 1
		self.bullet_speed_factor = 5
		self.alien_speed_factor = 0.5

		# fleet_direction = 1 обозначает движение вправо; а -1 - влево
		self.fleet_direction = 1

	def increase_speed(self):
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale