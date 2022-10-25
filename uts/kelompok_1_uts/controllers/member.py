from kelompok_1_uts import db
from kelompok_1_uts.models.member import Member
from kelompok_1_uts.models.transaction import Transaction
from flask import flash, redirect, url_for

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
    
    member_transaction = Transaction.query.where(Transaction.member_id == id).all()
    if member_transaction:
        flash(
            f"Member {cur_member.name} tidak dapat dihapus karena terkait dengan data Transaksi",
            category="danger",
        )
        return redirect(url_for("member.show")) and False
    
    db.session.delete(cur_member)
    db.session.commit()