import os
from .models.Page import Page
from .models.Config import ProjectJson

from .ext.Config import ConfigManager
from .logger import LoggingManager

from .parser import EVParse
from .runner import Runner

logger = LoggingManager("Evoker.Core")

EVProject = ConfigManager("project.json", template=ProjectJson)

def build() -> list[Page] | None:
    logger.info("Building Evoker App")

    pages = build_dir(EVProject.get("evoker", {}).get("source", "src"))   

    logger.ok(f"Build Succeeded")
    return pages

def build_dir(path) -> list[Page] | None:
    pages = []
    for file in os.listdir(path):
        if os.path.isdir(f'{path}/{file}'):
            pages += build_dir(f'{path}/{file}')
            continue
        
        if not file.endswith(".ev"): continue
        
        page = Page(f"{path}/{file}")
        
        try:
            page.runnable = EVParse.compose(page)
            page.config = EVParse.configure(page)
            pages.append(page)
        except Exception as err:
            logger.error(err)
            logger.error("Build Failed")
            return
        
    return pages
    
def run():
    pages = build()
    for p in pages:
        logger.info(f"{p.route} ------------")
        logger.info(f"path: {p.path}")
        logger.info(f"config: {p.config}")
        logger.info(f"scripts: {vars(p.runnable).get('script')}")
        logger.info(f"body: {vars(p.runnable).get('body')}")
    
    try:
        runner = Runner(pages)
    except Exception as err:
        logger.error(err)
        logger.error("Run Failed")
        return
    
    runner.run()
    

logger.info(f"Initialized Evoker Project: {EVProject.get('project', {}).get('name', 'Evoker')} v{EVProject.get('project', {}).get('version', '0.0.1')}")