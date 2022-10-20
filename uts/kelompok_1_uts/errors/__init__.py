from flask import Blueprint

bp = Blueprint("errors", __name__)

from kelompok_1_uts.errors import handlers
