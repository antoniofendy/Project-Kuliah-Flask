from kelompok_1_uts import db


from kelompok_1_uts.models.transaction import Transaction
from kelompok_1_uts.models.payment import Payment
from kelompok_1_uts.models.payment import PaymentType
from kelompok_1_uts.models.transaction import TransactionStatus
from kelompok_1_uts.models.charge_rule import ChargeType
from kelompok_1_uts.models.payment import PaymentStatus


def get(id):
    transaction = db.session.get(Transaction, id)

    price = transaction.stock.price
    start = transaction.rental_start_date
    end = transaction.rental_end_date
    length = end - start
    print(type(length))
    print(length.days)

    total_price = price * length.days
    print(total_price)

    payment = Payment(
        transaction_id=transaction.id,
        transaction_type=PaymentType.PAYMENT,
        amount=total_price,
        status=PaymentStatus.UNPAID,
    )

    return payment


def pay(payment):
    db.session.add(payment)
    transaction = db.session.get(Transaction, payment.transaction_id)
    transaction.status = TransactionStatus.RENT

    db.session.commit()


def get_all():
    response = Payment.query.order_by(Payment.id).all()
    return response
