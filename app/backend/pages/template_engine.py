from fastapi.templating import Jinja2Templates

from app.backend.components.config import TEMPLATES_DIR


engine = Jinja2Templates(directory=TEMPLATES_DIR)
