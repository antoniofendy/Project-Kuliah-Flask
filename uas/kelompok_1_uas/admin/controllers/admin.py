from kelompok_1_uas import db
from kelompok_1_uas.admin.models.admin import Admin


def get_all():
    # response = db.session.execute(db.select(Staff).order_by(Staff.name)).scalars().all()
    response = Admin.query.order_by(Admin.id.asc()).all()
    return response


def get(id):
    return db.get_or_404(Admin, id)


def create(Admin):
    db.session.add(Admin)
    db.session.commit()


def update(admin):
    cur_admin = db.get_or_404(Admin, admin["id"])
    cur_admin.name = admin["name"]
    cur_admin.phone = admin["phone"]
    cur_admin.address = admin["address"]

    db.session.commit()


def delete(id):
    cur_admin = db.get_or_404(Admin, id)
    db.session.delete(cur_admin)
    db.session.commit()
