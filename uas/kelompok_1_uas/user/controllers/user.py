from kelompok_1_uas import db
from kelompok_1_uas.admin.models.user import User


def get_all():
    response = User.query.order_by(User.id.asc()).all()
    return response


def get(id):
    return db.get_or_404(User, id)


def create(User):
    db.session.add(User)
    db.session.commit()


def update(user):
    cur_user = db.get_or_404(User, user["id"])
    cur_user.name = user["name"]
    cur_user.address = user["address"]
    cur_user.phone = user["phone"]
    cur_user.date_of_birth = user["date_of_birth"]
    cur_user.occupation = user["occupation"]
    cur_user.email = user["email"]
    cur_user.password = user["password"]
    cur_user.sex = user["sex"]

    db.session.commit()


def delete(id):
    cur_user = db.get_or_404(User, id)
    db.session.delete(cur_user)
    db.session.commit()