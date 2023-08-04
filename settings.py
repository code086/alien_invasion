class Settings:
    """管理游戏中相关设置"""

    def __init__(self):
        """初始化配置资源"""
        # 设置屏幕尺寸
        self.screen_size = (1200, 800)
        # 设置屏幕说明文字
        self.screen_caption = "Alien Invasion"
        # 设置背景颜色
        self.bg_color = (230, 230, 230, 230)
        # 设置帧率控制（每秒60次循环）
        self.clock_tick = 60
        # 设置飞船速度
        self.speed = 1.5

        # 设置子弹相关参数
        self.bullet_color = (60, 60, 60)
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_speed = 2.0
        self.bullet_allowed = 3
