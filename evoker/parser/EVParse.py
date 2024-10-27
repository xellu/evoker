from ..models.Page import Page
from ..models.Runnable import Runnable
from ..logger import LoggingManager

import bs4
import time

logger = LoggingManager("Evoker.Parser")

def compose(page: Page):
    start_time = time.time()
    logger.info(f"Starting to compose page '{page.path}'")

    bs = bs4.BeautifulSoup(page.source, "html.parser")
    source = Runnable()

    #validate page structure
    # config = bs.find("config")
    scripts = bs.find("script")
    body = bs.find("body")

    if not body:
        raise LookupError(f"Page '{page.path}' is missing body")

    #parse scripts
    logger.info("Processing attached scripts")
    if scripts:
        indent_offset = 0
        new_script = ""
        #calculate indentation offset
    
        for ln in scripts.text.splitlines():
            if ln.strip() == "":
                continue

            indent_offset = len(ln) - len(ln.lstrip())
            break
        
        for ln in scripts.text.splitlines():
            new_script += ln[indent_offset:] + "\n"
        
        source.script = new_script

    #parse body
    logger.info("Processing page body")
    source.body = body.prettify()

    logger.ok(f"Page '{page.path}' was composed within {time.time()-start_time:.2f}s")

    return source

def configure(page: Page):
    #parse config
    logger.info("Processing page configuration")
    
    bs = bs4.BeautifulSoup(page.source, "html.parser")
    config = bs.find("config")

    if config:
        for setting in config.find_all("setting"):
            name = setting.get_attribute_list("for")[0]
            value = setting.get_attribute_list("value")[0]

            if name is None or value is None:
                logger.warn(f"Invalid config declaration in '{page.path}' ({name=}, {value=})")
                continue
        
            page.config[name] = value
            
    logger.ok(f"Page '{page.path}' configuration processed")
    return page.config