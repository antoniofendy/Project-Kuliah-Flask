from kelompok_1_uts import db
from kelompok_1_uts.models.member import Member

def get_all():
    # response = db.session.execute(db.select(Staff).order_by(Staff.name)).scalars().all()
    response = Member.query.order_by(Member.id.asc()).all()
    return response

def get(id):
    return db.get_or_404(Member, id)

def create(Member):
    db.session.add(Member)
    db.session.commit()

def update(member):
    cur_member = db.get_or_404(Member, member["id"])
    cur_member.name = member["name"]
    cur_member.gender = member["gender"]
    cur_member.birth = member["birth"]
    cur_member.address = member["address"]
    cur_member.phone = member["phone"]
    cur_member.email = member["email"]

    db.session.commit()

def delete(id):
    cur_member = db.get_or_404(Member, id)
    db.session.delete(cur_member)
    db.session.commit()