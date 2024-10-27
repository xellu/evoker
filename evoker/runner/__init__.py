from ..logger import LoggingManager
from ..models.Theme import Colors
from ..ext import Keymap

import os
import time
import curses
import threading

logger = LoggingManager("Evoker.Runner")

class Runner:
    def __init__(self, pages):
        from .. import EVProject

        self.pages = pages
        if len(self.pages) == 0:
            raise ValueError("No pages provided")
        
        self.route = EVProject.get("evoker", {}).get("main", "/main")
        self.running = False
        
        self.screenX = os.get_terminal_size().columns
        self.screenY = os.get_terminal_size().lines
        
        self.sc = None
        
        self.fps = {
            "limit": EVProject.get("evoker", {}).get("maxFps", 60),
            
            "rate": 1 / EVProject.get("evoker", {}).get("maxFps", 60),
            "timeTaken": [1], #time taken to render last 10 frames
            
            "last": time.time(), #reset time for frame rate
            "frames": 0, #frames rendered in the last second
            "fps": 0, #frames per second
        }
        
        self.colors = { #color pairs
            #"BLUE_BLACK": index (fg: blue, bg: black)
            #"CYAN_YELLOW": index (fg: cyan, bg: yellow)
        }

    def get_page(self, route):
        for page in self.pages:
            if page.route == route:
                return page
        return None
    
    def apply_theme(self):
        #create a color pair for color combinations (colors)
        index = 0
        for c1name, c1 in Colors.items():
            for c2name, c2 in Colors.items():
                index += 1
                curses.init_pair(index, c1, c2)
                self.colors[f"{c1name}_{c2name}"] = index
        
    def color(self, fg, bg="BLACK"):
        return curses.color_pair(self.colors[f"{fg}_{bg}"])
        
    def redirect(self, route):
        self.route = route
        
    def run(self):
        self.running = True

        threading.Thread(target=curses.wrapper, args=(self.input_loop,)).start()
        curses.wrapper(self.render_loop)
        
    def render_loop(self, sc):
        logger.info("Starting runner render loop")

        curses.start_color()        
        self.apply_theme()

        curses.curs_set(0)
        self.sc = sc
        
        while True:
            start = time.time()
            
            if not self.running: break
            
            #update screen size
            self.screenX = os.get_terminal_size().columns
            self.screenY = os.get_terminal_size().lines
            # print(self.screenX, self.screenY)
            
            sc.erase()
        
            try:
                page = self.get_page(self.route)
                if not page:
                    raise ValueError(f"Page '{self.route}' not found")
                    
                page.on_render(self)
                
                sc.refresh()
            except Exception as e:
                sc.erase()
                
                sc.addstr(0,0, f"RENDER ERROR:", self.color("BLACK", "RED"))
                sc.addstr(1,0, f"{e}", self.color("RED"))
                logger.error(f"Error rendering page '{self.route}': {e}")
            
                sc.refresh()
                time.sleep(3)
            
            
            #calculate fps
            self.fps["frames"] += 1
            if time.time() - self.fps["last"] >= 1:
                self.fps["last"] = time.time()
                self.fps["fps"] = self.fps["frames"]
                self.fps["frames"] = 0
                
            #calculate time taken
            taken = time.time() - start
            self.fps["timeTaken"].append(taken)
            self.fps["timeTaken"] = self.fps["timeTaken"][-10:]
                
            #calculate sleep time
            sleep = self.fps["rate"] - taken
            if sleep > 0:
                time.sleep(sleep)
                
            #frame rate warning
            if taken > self.fps["rate"] * 1.5:
                # logger.warn(f"Rendering is taking too long: {int(taken*1000)}ms (max: {int(self.fps['rate']*1000)}ms)")
                logger.warn(f"Render process is falling behind! {int(taken*1000)}ms, max: {int(self.fps['rate']*1000)}ms")
            
        logger.info("Runner event loop stopped")
        
    def input_loop(self, sc):
        logger.info("Starting runner input loop")
        
        while True:
            if not self.running: break
            
            key = sc.getch()
            if Keymap.get(key) == "q":
                self.running = False
            
            try:
                page = self.get_page(self.route)
                if not page:
                    raise ValueError(f"Page '{self.route}' not found")
                
                page.on_input(key)
            except Exception as e:
                logger.error(f"Error processing input for page '{self.route}': {e}")
            
        logger.info("Runner input loop stopped")