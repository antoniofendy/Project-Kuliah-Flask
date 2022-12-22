import os

from flask import Blueprint, render_template, request, flash, url_for, redirect, make_response
import pdfkit

from kelompok_1_uas import db

from kelompok_1_uas.admin.forms.rent import RentForm
from kelompok_1_uas.admin.controllers import rent as rent_controller
from kelompok_1_uas.admin.models.rent import Rent, RentStatus, PaymentType

from kelompok_1_uas.user.models.user import User
from kelompok_1_uas.admin.models.charge_rule import ChargeRule, ChargeType
from kelompok_1_uas.admin.models.car import Car
from kelompok_1_uas.admin.models.stock import Stock
from kelompok_1_uas.admin.models.garage import Garage
from kelompok_1_uas.admin.models.reservation import Reservation, ReservationStatus

from datetime import datetime

admin_reporting_bp = Blueprint(
    "admin_reporting",
    __name__,
    url_prefix="/admin/generate-report",
    template_folder="../templates",
)

@admin_reporting_bp.route("/", methods=["GET", "POST"])
def generate_report():
    if request.method == "POST":

        rent = Rent.query.where(Rent.updated_at >= request.form.get("start_date")).where(Rent.updated_at <= request.form.get("end_date")).all()
        total = (db.session.query(Rent)
        .where(Rent.updated_at >= request.form.get("start_date"))
        .where(Rent.updated_at <= request.form.get("end_date"))
        .with_entities(db.func.sum(Rent.total))
        .first()[0])

        # print(total)

        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        
        rendered = render_template("admin/report/pdf_template.html", rent=rent, total=total, start_date=start_date, end_date=end_date)
        config = pdfkit.configuration(wkhtmltopdf = 'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe')
        pdf = pdfkit.from_string(rendered, configuration=config)
        
        response = make_response(pdf)
        response.headers['Content-Type'] = 'template'
        response.headers['Content-Disposition'] = 'output.pdf'
        
        # print(response)
    
        return response

    return render_template("admin/report/form.html", data=None)
