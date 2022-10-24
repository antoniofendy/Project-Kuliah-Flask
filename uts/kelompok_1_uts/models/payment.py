from kelompok_1_uts import db
import enum


class PaymentType(enum.Enum):
    PAYMENT = "Pembayaran"
    CHARGE = "Denda"


class PaymentStatus(enum.Enum):
    UNPAID = "Belum Dibayar"
    PAID = "Dibayar"


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(
        db.Integer, db.ForeignKey("transaction.id"), nullable=False
    )
    transaction_type = db.Column(db.Enum(PaymentType), nullable=False)
    status = db.Column(
        db.Enum(PaymentStatus), nullable=False, default=PaymentStatus.UNPAID
    )
    amount = db.Column(db.Integer)
