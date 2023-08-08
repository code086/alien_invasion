import pygame


class Ship:
    """飞船类，管理飞船相关资源"""

    def __init__(self, ai_game):
        """初始化飞船并设定其初始位置"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图片并获取其外接矩形
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        # 使每艘新飞船置于屏幕底部中间位置
        self.rect.midbottom = self.screen_rect.midbottom

        # 飞船移动标志，默认False
        self.moving_right = False
        self.moving_left = False

        # 飞船的属性x，存储为浮点数
        self.x = float(self.rect.x)

        # 引入设置类，确定飞船移动速度
        self.settings = ai_game.settings

    def center_ship(self):
        """将飞船居中"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.x = float(self.rect.x)

    def update(self):
        """ 根据移动标识更新飞船位置"""
        if self.moving_right and self.screen_rect.right > self.rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
