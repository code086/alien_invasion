import sys
from time import sleep

import pygame

import settings
import ship
from alien import Alien
from bullet import Bullet
from game_stats import GameStats


class AlienInvasion:
    """这是一个游戏类，用于创建游戏对象并管理游戏资源"""

    def __init__(self):
        """初始化类并创建资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = settings.Settings()
        # 设置全屏显示
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        self.settings.screen_size = (self.screen_width, self.screen_height)
        # 通过尺寸设置屏幕大小
        # self.screen = pygame.display.set_mode(self.settings.screen_size)
        pygame.display.set_caption(self.settings.screen_caption)
        # 创建用于存储游戏统计信息的实例
        self.stat = GameStats(self)
        # 创建飞船
        self.ship = ship.Ship(self)
        # 创建子弹编组
        self.bullets = pygame.sprite.Group()
        # 创建外星人编组
        self.aliens = pygame.sprite.Group()
        # 创建外星人编队
        self._create_fleet()

        # 游戏活动状态
        self.game_active = True

    def run_game(self):
        """运行游戏"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
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
        # 删除超出屏幕的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullets_aliens_collisions()

    def _check_bullets_aliens_collisions(self):
        """检查子弹和外星舰队的碰撞"""
        # 删除与外星人碰撞的子弹
        # 子弹碰撞外星人，同时删除子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        # 外星人全部被击落后删除所有子弹并创建新外星舰队
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _ship_hit(self):
        """响应飞船和外星人碰撞"""
        if self.stat.ship_left > 0:
            # 将ship_limit减1
            self.stat.ship_left -= 1
            # 清空子弹和外星舰队
            self.bullets.empty()
            self.aliens.empty()
            # 创建新的外星舰队和飞船，飞船居底部中间
            self._create_fleet()
            self.ship.center_ship()
            # 暂停 0.5 秒
            sleep(0.5)
        else:
            self.game_active = False

    def _check_aliens_bottom(self):
        """检查外星舰队是否达到屏幕底部"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen_height:
                self._ship_hit()
                break

    def _create_alien(self, x_position, y_position):
        """创建一个外星人"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _create_fleet(self):
        """创建一个外星舰队"""
        # 创建一个外星人
        alien = Alien(self)
        print(alien.x)
        print(alien.rect.x)
        # 获取外星人的宽度和高度
        alien_width, alien_height = alien.rect.size
        # 确定外星人位置的初始游标
        current_x, current_y = alien_width, alien_height

        # 根据屏幕宽度创建一排外星人
        while current_y < (self.screen_height - 3 * alien_height):
            while current_x < (self.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # 添加一行外星人后，重置x值，递增y值
            current_x = alien_width
            current_y += 2 * alien_height

    def _change_fleet_direction(self):
        """将外星人舰队向下移动，并改变他们的移动方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_speed * 10
        self.settings.alien_direction *= -1

    def _check_fleet_edge(self):
        """检查外星人舰队是否达到屏幕边缘并采取相应措施"""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break

    def _update_aliens(self):
        """更新外星人编组"""
        self._check_fleet_edge()
        self.aliens.update()
        # 检查外星舰队和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            # print("Ship hit!")
        # 检查外星舰队是否触底
        self._check_aliens_bottom()

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
