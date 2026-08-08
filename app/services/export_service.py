from io import BytesIO
import pandas as pd

class ExportService:
    """
    Handles data export operations.
    """

    @staticmethod
    def to_excel(report) -> BytesIO:
        """
        Converts report data into an Excel file.

        Args:
            report: Report rows to export.

        Returns:
            BytesIO: Excel file stored in memory.
        """
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

        dataframe = pd.DataFrame(data)
        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:
            dataframe.to_excel(
                writer,
                index=False,
                sheet_name="Loyal Customers"
            )

        output.seek(0)

        return output