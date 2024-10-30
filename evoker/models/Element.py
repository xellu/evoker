class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Element:
    def __init__(self, app, pos: Position, content, element, focused=False):
        self.app = app
        self.pos = pos
        self.content = str(content)
        self.element = element
        
        self.focused = focused
        
        self.attributes = {
            "x": self.pos.x,
            "y": self.pos.y,
            "fg": "WHITE",
            "bg": "BLACK"
        }
        self._id = self.elementsget("id")
        
    def on_render(self, sc):
        sc.addstr(self.pos.y, self.pos.x, self.content)
        
    def on_input(self, key):
        print(key)