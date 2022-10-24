from kelompok_1_uts import db


from kelompok_1_uts.models.transaction import Transaction
from kelompok_1_uts.models.payment import Payment
from kelompok_1_uts.models.payment import PaymentType
from kelompok_1_uts.models.transaction import TransactionStatus
from kelompok_1_uts.models.charge_rule import ChargeType
from kelompok_1_uts.models.payment import PaymentStatus


def get(id, charge):
    transaction = db.session.get(Transaction, id)
    print(id)
    price = transaction.stock.price
    start = transaction.rental_start_date
    end = transaction.rental_end_date
    length = end - start

    total_price = price * length.days

    payment_type = PaymentType.PAYMENT

    if charge:
        payment_type = PaymentType.CHARGE
        amount = float(transaction.charge_rule.amount)
        type_ = transaction.charge_rule.type

        if type_ == ChargeType.NOMINAL:
            total_price = amount * length.days
        else:
            ratio = amount / 100
            total_price = total_price * ratio * length.days

    to_pay = total_price

    payment = Payment(
        transaction_id=transaction.id,
        transaction_type=payment_type,
        amount=to_pay,
        status=PaymentStatus.UNPAID,
    )

    return payment


def pay(payment):
    db.session.add(payment)
    transaction = db.session.get(Transaction, payment.transaction_id)
    transaction.status = (
        TransactionStatus.RENT
        if payment.transaction_type == PaymentType.PAYMENT.name
        else TransactionStatus.RETURNED
    )

    db.session.commit()


def get_all():
    response = Payment.query.order_by(Payment.id).all()
    return response
