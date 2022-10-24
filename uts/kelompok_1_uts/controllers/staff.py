from kelompok_1_uts import db
from kelompok_1_uts.models.staff import Staff

def create(staff):
    db.session.add(staff)
    db.session.commit()


def update(staff):
    cur_staff = db.get_or_404(Staff, staff["id"])
    cur_staff.name = staff["name"]
    cur_staff.phone = staff["phone"]
    cur_staff.address = staff["address"]
    cur_staff.picture = staff["picture"]

    db.session.commit()


def delete(id):
    cur_staff = db.get_or_404(Staff, id)
    db.session.delete(cur_staff)
    db.session.commit()


def get(id):
    return db.get_or_404(Staff, id)


def get_all():
    # response = db.session.execute(db.select(Staff).order_by(Staff.name)).scalars().all()
    response = Staff.query.order_by(Staff.id.asc()).all()
    return response
