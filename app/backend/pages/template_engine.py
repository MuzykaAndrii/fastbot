from fastapi.templating import Jinja2Templates

from app import config


engine = Jinja2Templates(directory=config.TEMPLATES_DIR)
