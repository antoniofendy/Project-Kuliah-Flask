from kelompok_1_uts import db
from kelompok_1_uts.models.member import Member

def get_all():
    # response = db.session.execute(db.select(Staff).order_by(Staff.name)).scalars().all()
    response = Member.query.order_by(Member.id.asc()).all()
    return response

def create(Member):
    db.session.add(Member)
    db.session.commit()

def delete(id):
    cur_member = db.get_or_404(Member, id)
    db.session.delete(cur_member)
    db.session.commit()