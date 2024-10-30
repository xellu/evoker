from ..models.Element import Element, Position
from ..ext import Keymap

class Fps(Element):
    def __init__(self, app, pos: Position, content, element, focused=False):
        self.app = app
        self.pos = pos
        self.content = f"FPS: {self.app.fps["fps"]} | Frames: {self.app.fps["frames"]} | Avg: {(sum(self.app.fps["timeTaken"])/len(self.app.fps["timeTaken"]))*1000:.4f}ms"
        self.element = element
        
        self.focused = focused
        
        self.attributes = {
            "x": self.pos.x,
            "y": self.pos.y,
            "fg": "WHITE",
            "bg": "BLACK",
            "width": len(self.content),
        }
        
        self._id = self.element.get("id")
        self.page = 0 #0-2
        
        self.parse_attributes()
        
    def parse_attributes(self):
        for key in self.attributes.keys():
            if key in self.element.attrs:
                match type(self.attributes[key]).__name__:
                    case "int":
                        self.attributes[key] = int(self.element.attrs[key])
                    case "float":
                        self.attributes[key] = float(self.element.attrs[key])
                    case _:
                        self.attributes[key] = self.element.attrs[key]
        
        
    def on_render(self, sc):
        color = self.app.color(self.attributes["fg"].upper(), self.attributes["bg"].upper())
        if self.focused:
            color = self.app.color(self.attributes["bg"].upper(), self.attributes["fg"].upper())

        match self.page:
            case 0:
                content = f"FPS: {self.app.fps["fps"]} | Frames: {self.app.fps["frames"]} | Avg: {(sum(self.app.fps["timeTaken"])/len(self.app.fps["timeTaken"]))*1000:.4f}ms"
            case 1:
                content = f"Time Taken {self.app.fps["timeTaken"][-1]*1000:.4f}ms | Rate: {self.app.fps["rate"]*1000:.4f}ms"
            case 2:
                content = f"Limit: {self.app.fps["limit"]} | Last: {self.app.fps["last"]:.0f}"
        width = len(content)
        
        #prevent overflow
        if width > self.app.screenX:
            width = self.app.screenX    
        if self.attributes['x'] + width > self.app.screenX:
            width = self.app.screenX - self.attributes['x']
            
        #prevent content overflow
        if len(content) > width:
            content = content[:width-3] + "..."
            
        content = content.ljust(width)
        sc.addstr(self.attributes['y'], self.attributes['x'], content, color)
        
        #fps warn testing
        # import time
        # time.sleep(0.05)
        
    def on_input(self, key):
        if Keymap.get(key) == "enter":
            self.page = (self.page + 1) % 3