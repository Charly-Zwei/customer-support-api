from flask import Blueprint
from app.services.report_service import ReportService

report_bp = Blueprint("reports", __name__, url_prefix="/reports")

@report_bp.get("/loyal-customers")
def get_loyal_customers():
    report = ReportService.get_loyal_customers_report()

    return [
        {
            "document_type": row.document_type,
            "document_number": row.document_number,
            "first_name": row.first_name,
            "last_name": row.last_name,
            "email": row.email,
            "phone": row.phone,
            "total_amount": str(row.total_amount)
        }
        for row in report
    ], 200