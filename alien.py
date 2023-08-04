import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    """这是外星人类"""

    def __init__(self, ai_game):
        """初始化外星人，并设置其基本属性"""
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        # 加载外星人图片，并获取其rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        # 设置外星人位置，初始为屏幕左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # 储存外星人准确位置
        self.x = float(self.rect.x)

