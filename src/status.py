class Status:
    def __init__(self):
        self.agent = None
        self.enemy = None
        self.map = None

    def game_end(self):
        return self.agent.pos == self.enemy.pos