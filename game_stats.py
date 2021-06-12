# Отслеживание статистики
class GameStats():

    # Инициализирует статистику
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.game_active = False
        self.reset_stats()
        self.alien_score = 100
        self.lvl = 1

    # Инициализирует статистику, изменяющуюся в ходе игры
    def reset_stats(self):
        self.score = 0
        with open("cache/bs.cache", "r") as file_oblect:
            self.best_score = int(file_oblect.readline().strip())
        self.ships_left = self.ai_settings.ship_limit

    def increase_best_score(self):
        if self.best_score < self.score:
            self.best_score = self.score
        with open("cache/bs.cache", "w") as file_oblect:
            file_oblect.write(str(self.best_score).strip())