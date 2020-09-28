class Player: 
    def __init__(self, symbol):
        self.symbol = symbol 
        self.positions = set() 

    def add_pos(self, pos):
        self.positions.add(pos)