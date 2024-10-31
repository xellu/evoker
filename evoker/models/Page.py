from os import PathLike
from bs4 import BeautifulSoup

from ..elements import elements
from ..models.Element import Position
from ..ext import Keymap, Events

class Page:
    def __init__(self, path: PathLike):
        """
        Initialize a Page object.
        
        Args:
            path (PathLike): The path to the page file.
            
        Attributes:
            config (dict): The configuration of the page.
            path (PathLike): The path to the page file. (e.g. src/main.ev)
            route (str): The route of the page. (e.g. /main)
            source (str): The source of the page.
            runnable (Runnable): The runnable object of the page.
        """
        
        self.config = {
            "title": "Evoker App"
        }
        
        self.path = path
        self.route = path.replace("src", "").replace(".ev", "")
        self.source = open(self.path, "r", encoding="utf-8").read()
        self.runnable = None
        
        self.tab_index = 0
        self.element_count = 0
        
        self.bs = BeautifulSoup(self.source, "html.parser")
        self.body = self.bs.find("body")
        
        self.eventer = Events.EventBus()
        self.elements = None
        
    def on_render(self, app):
        """
        Render the page.
        
        Args:
            app (Runner): The runner object.
            
        Returns:
            None
        """
        
        #set bg color
        if self.body and "bg" in self.body.attrs:
            color = self.body.attrs["bg"].upper()
            app.sc.bkgd(" ", app.color(color, color))
        
        #parse the elements
        y = 0
        if self.elements is None:
            self.elements = []
            
            for tag in self.bs.find_all():
                # elements.get(tag.name, Element)(app, Position(0, y), tag.text, tag.name).on_render(app.sc)
                # y += 1
                el = elements.get(tag.name)
                if not el: continue
                
                el = el.copy()
                el["instance"] = el['class'](app, Position(0, y), tag.text, tag, False)
                el["id"] = tag.get("id")
                el["classNames"] = tag.get("class")
                self.elements.append(el)
                
                y += 1
              
        focusable = 0         
        for tag in self.elements:
            tag['instance'].focused = focusable == self.tab_index 
            tag['instance'].on_render(app.sc)
            
            if tag['focusable']:
                focusable += 1
                
        self.element_count = focusable

                        
    def on_input(self, key):
        """
        Handle input events.
        
        Args:
            app (Runner): The runner object.
            
        Returns:
            None
        """
        
        if Keymap.get(key) == "tab":
            self.tab_index += 1
            if self.tab_index >= self.element_count:
                self.tab_index = 0
                        
            # print(self.tab_index)
        else:
            focusables = []
            for tag in self.elements:
                if tag['focusable']:
                    focusables.append(tag)
                    
            focusables[self.tab_index]['instance'].on_input(key)
            
    def on_load(self):
        self.eventer = Events.EventBus()
        
        print(f"Page '{self.route}' loaded")
        
    def on_unload(self): 
        self.eventer.trigger("unload")
        
        print(f"Page '{self.route}' unloaded")