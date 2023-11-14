from app.db.dal import BaseDAL
from app.users.models import User


class UserDAL(BaseDAL):
    model = User