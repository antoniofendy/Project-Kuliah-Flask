from flask import Blueprint

bp = Blueprint(
    "admin_errors",
    __name__,
    url_prefix="/admin",
    template_folder="../templates",
    static_folder="../../static",
)


from kelompok_1_uas.admin.errors import handlers
