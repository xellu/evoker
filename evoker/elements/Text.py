from ..models.Element import Element, Position

class Text(Element):
    def __init__(self, app, pos: Position, content, element, focused=False):
        self.app = app
        self.pos = pos
        self.content = str(content)
        self.element = element
        
        self.attributes = {
            "x": self.pos.x,
            "y": self.pos.y,
            "fg": "WHITE",
            "bg": "BLACK",
            "width": len(self.content),
        }
        
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
        color = self.app.color(self.attributes["fg"].upper(), self.attributes["bg"].upper())
        # if self.focused:
        #     color = self.app.color(self.attributes["bg"].upper(), self.attributes["fg"].upper())

        width = self.attributes['width']
        content = self.content
        
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
        
    def on_input(self, key):
        # print(key)
        pass