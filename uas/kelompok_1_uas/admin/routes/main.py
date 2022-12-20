from flask import Blueprint, render_template

admin_main_bp = Blueprint(
    "admin_main",
    __name__,
    url_prefix="/admin",
    template_folder="../templates",
    static_folder="../static",
)


@admin_main_bp.route("/")
def index():
    print(admin_main_bp.root_path)
    return render_template("admin/index.html")
