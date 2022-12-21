from flask import Blueprint

bp = Blueprint("user_errors", __name__)

from kelompok_1_uas.errors import handlers
