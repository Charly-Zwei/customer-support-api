from flask import Blueprint, send_file
from app.services.report_service import ReportService
from app.services.export_service import ExportService

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

@report_bp.get("/loyal-customers/export")
def export_loyal_customers():
    report = ReportService.get_loyal_customers_report()

    output = ExportService.loyal_customers_excel(report)

    return send_file(
        output,
        as_attachment=True,
        download_name="loyal_customers.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )