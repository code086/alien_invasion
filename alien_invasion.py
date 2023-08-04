import sys

import pygame

import settings
import ship
from alien import Alien
from bullet import Bullet


class AlienInvasion:
    """这是一个游戏类，用于创建游戏对象并管理游戏资源"""

    def __init__(self):
        """初始化类并创建资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = settings.Settings()
        # 设置全屏显示
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_size = (self.screen.get_rect().width, self.screen.get_rect().height)
        # 通过尺寸设置屏幕大小
        # self.screen = pygame.display.set_mode(self.settings.screen_size)
        pygame.display.set_caption(self.settings.screen_caption)

        # 创建飞船
        self.ship = ship.Ship(self)
        # 创建子弹编组
        self.bullets = pygame.sprite.Group()
        # 创建外星人编组
        self.aliens = pygame.sprite.Group()
        # 创建外星人编队
        self._create_fleet()

    def run_game(self):
        """运行游戏"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(self.settings.clock_tick)

    def _check_events(self):
        """相应鼠标键盘等事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """按下按键响应"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """释放按键响应"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """发射一颗子弹"""
        if self.settings.bullet_allowed > self.bullets.__len__():
            bullet = Bullet(self)
            self.bullets.add(bullet)

    def _update_bullets(self):
        self.bullets.update()
        """删除已消失的子弹"""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        # 生成外星人并加入外星人编队
        alien = Alien(self)
        self.aliens.add(alien)

    def _update_screen(self):
        """更新屏幕，把子弹、飞船和外星人绘制到屏幕上"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
