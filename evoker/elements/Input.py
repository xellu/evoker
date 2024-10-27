from ..models.Element import Element, Position
from ..ext import Keymap

import time

class Input(Element):
    def __init__(self, app, pos: Position, content, element, focused=False):
        self.app = app
        self.pos = pos
        self.content = ""
        self.placeholder = element.attrs.get("placeholder", "")
        self.element = element
        
        self.attributes = {
            "x": self.pos.x,
            "y": self.pos.y,
            "fg": "BLACK",
            "bg": "WHITE",
            "focused": "BLUE",
            "width": len(self.placeholder) if len(self.placeholder) > 16 else 16,
        }
        self.focused = focused
        
        self.parse_attributes()
        
    def parse_attributes(self):
        for key in self.attributes.keys():
            if key in self.element.attrs:
                match type(self.attributes[key]).__name__:
                    case "int":
                        try: #convert to char length
                            self.attributes[key] = int(self.element.attrs[key])
                        except: #convert to percentage
                            self.attributes[key] = int(self.app.screenX * (int(self.element.attrs[key].replace("%", ""))/100))
                    case "float":
                        self.attributes[key] = float(self.element.attrs[key])
                    case _:
                        self.attributes[key] = self.element.attrs[key]
        
        
    def on_render(self, sc):
        color = self.app.color(self.attributes["fg"].upper(), self.attributes["focused" if self.focused else "bg"].upper())

        width = self.attributes['width']
        
        sc.addstr(self.attributes['y'], self.attributes['x'], " "*width, color)
        
        content = self.content if self.content or self.focused else self.placeholder
        if self.focused:
            content += "_" if self.focused and time.time() % 1 > 0.5 else " " #blinking cursor
                
        if len(content) > width:
            while len(content) > width+3:
                content = content[1:]
                
            content = "..." + content[-width+3:]
        
        #prevent overflow
        if width > self.app.screenX:
            width = self.app.screenX    
        if self.attributes['x'] + width > self.app.screenX:
            width = self.app.screenX - self.attributes['x']
            
        #prevent content overflow
        # if len(content) > width:
        #     content = content[:width-3] + "..."
            
        content = content.ljust(width)
        sc.addstr(self.attributes['y'], self.attributes['x'], content, color)
        
    def on_input(self, key):
        match Keymap.get(key):
            case "enter":
                pass
            case "backspace":
                self.content = self.content[:-1]
            case "ctrl_backspace":
                self.content = ""
            case _:
                self.content += Keymap.get_char(key)