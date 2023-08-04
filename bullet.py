import pygame

from pygame.sprite import Sprite


class Bullet(Sprite):
    """这是一个子弹的类"""

    def __init__(self, ai_game):
        """在飞船当前位置创建一个子弹"""
        super().__init__()
        # 初始化子弹对象基本属性
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color

        # 在原点处生成一个子弹矩形，然后设置其位置为飞船顶部
        self.rect = pygame.Rect(0, 0, ai_game.settings.bullet_width, ai_game.settings.bullet_height)
        # 设置子弹位置与飞船顶部中间对齐
        self.rect.midtop = ai_game.ship.rect.midtop

        # 用浮点数来表示子弹的位置
        self.y = float(self.rect.y)

    def update(self):
        """子弹位置更新（向上移动）"""
        # 更新子弹准确位置
        self.y -= self.settings.bullet_speed
        # 更新子弹rect参数
        self.rect.y = self.y

    def draw_bullet(self):
        """绘制子弹到屏幕上"""
        pygame.draw.rect(self.screen, self.color, self.rect)
