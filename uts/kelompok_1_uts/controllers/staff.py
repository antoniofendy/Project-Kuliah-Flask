from kelompok_1_uts import db
from kelompok_1_uts.models.staff import Staff


def create(staff):
    db.session.add(staff)
    db.session.commit()


def get_all():
    # response = db.session.execute(db.select(Staff).order_by(Staff.name)).scalars().all()
    response = Staff.query.order_by(Staff.id.asc()).all()
    return response
