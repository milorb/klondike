class Scene():

    def __init__(self, game):
        self.game = game
    
    def update(self):
        pass

    def draw(self):
        pass

    def on_exit(self, *args):
        pass

    def on_swap(self, *args):
        print("scene swapped")
