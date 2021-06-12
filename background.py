import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load("images/bg.jpg")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = 0, 0