from flask import Blueprint

errorhandle_blue = Blueprint('errorhandle', __name__)
user_blue = Blueprint('user', __name__, url_prefix='/user')

from . import errorhandle
from . import user
