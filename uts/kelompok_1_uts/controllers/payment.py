from flask import flash
from kelompok_1_uts import db


from kelompok_1_uts.models.transaction import Transaction
from kelompok_1_uts.models.payment import Payment
from kelompok_1_uts.models.payment import PaymentType
from kelompok_1_uts.models.transaction import TransactionStatus
from kelompok_1_uts.models.charge_rule import ChargeType
from kelompok_1_uts.models.payment import PaymentStatus


def get(id, charge):
    transaction = db.session.get(Transaction, id)
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

    transaction.stock.qty = transaction.stock.qty + (
        1 if payment.transaction_type == PaymentType.CHARGE.name else 0
    )

    db.session.commit()


def get_all():
    response = Payment.query.order_by(Payment.id).all()
    return response


def delete(id):
    payment = db.session.get(Payment, id)

    if payment.transaction.status == TransactionStatus.RETURNED:

        if payment.transaction_type == PaymentType.PAYMENT:
            other_payment = (
                Payment.query.filter(Payment.transaction_id == payment.transaction_id)
                .filter(Payment.transaction_type == PaymentType.CHARGE)
                .first()
            )
            if other_payment:
                flash(
                    f"Data pembayaran {payment.id} tidak dapat dihapus karena terkait dengan pembayaran {other_payment.id}.",
                    category="danger",
                )
                return False

        payment.transaction.status = TransactionStatus.RENT
        payment.transaction.stock.qty = payment.transaction.stock.qty - 1
        flash(
            f"Data pembayaran berhasil dihapus dan pengembalian transaksi {payment.transaction.id} dibatalkan.",
            category="info",
        )
    elif payment.transaction.status == TransactionStatus.RENT:
        payment.transaction.status = TransactionStatus.UNPAID
        payment.transaction.stock.qty = payment.transaction.stock.qty + 1
        flash(
            f"Data pembayaran berhasil dihapus dan penyewaan transaksi {payment.transaction.id} dibatalkan.",
            category="info",
        )
    db.session.delete(payment)
    db.session.commit()

    return True
