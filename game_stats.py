class GameStats:
    """跟踪游戏统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats()
        # 最高分记录
        self.high_score = 0

        self.level = 1

    def reset_stats(self):
        """初始化游戏运行期间可变化的统计信息"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
