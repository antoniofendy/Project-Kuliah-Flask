from flask import Blueprint

bp = Blueprint("user_errors", __name__)

from kelompok_1_uas.admin.errors import handlers
