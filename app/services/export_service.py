from io import BytesIO
import pandas as pd
from app.models import Customer

class ExportService:
    """
    Handles data export operations.
    """

    @staticmethod
    def _to_excel(data: list[dict], sheet_name: str) -> BytesIO:
        """
        Converts report data into an Excel file.

        Args:
            report: Report rows to export.

        Returns:
            BytesIO: Excel file stored in memory.
        """
        
        dataframe = pd.DataFrame(data)
        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:
            dataframe.to_excel(
                writer,
                index=False,
                sheet_name=sheet_name
            )

        output.seek(0)

        return output
    @staticmethod
    def loyal_customers_excel(report) -> BytesIO:
        data = [
            {
            "Document Type": row.document_type,
            "Document Number": row.document_number,
            "First Name": row.first_name,
            "Last Name": row.last_name,
            "Email": row.email,
            "Phone": row.phone,
            "Total Amount": row.total_amount
            }
            for row in report
        ]

        return ExportService._to_excel(data, "Loyal Customers")
    @staticmethod
    def customer_excel(customer: Customer) -> BytesIO:
        data = [
            {
                "Document Type": customer.document_type.name,
                "Document Number": customer.document_number,
                "First Name": customer.first_name,
                "Last Name": customer.last_name,
                "Email": customer.email,
                "Phone": customer.phone
            }
        ]

        return ExportService._to_excel(data, "Customer")