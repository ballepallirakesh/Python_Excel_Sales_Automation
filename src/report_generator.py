from pathlib import Path 
import pandas as pd 
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import logging
from src.logger_config import setup_logger

def format_excel_file(file_path):
    from openpyxl import load_workbook

    logger = setup_logger()
    file_path = Path(file_path)
    try:
        logger.info("Formatting Excel file: %s", file_path.name)

        workbook = load_workbook(file_path)

        header_fill = PatternFill(
            fill_type="solid",
            fgColor="1F4E78"
        )

        header_font = Font(
            bold=True,
            color="FFFFFF",
            size=11
        )

        thin_border = Border(
            bottom=Side(style="thin", color="D9E2F3")
        )

        for worksheet in workbook.worksheets:

            for cell in worksheet[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(
                    horizontal="center",
                    vertical="center"
                )

            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions

            for column_cells in worksheet.columns:
                max_length = 0
                column_letter = get_column_letter(
                    column_cells[0].column
                )

                for cell in column_cells:
                    if cell.value is not None:
                        max_length = max(
                            max_length,
                            len(str(cell.value))
                        )

                worksheet.column_dimensions[
                    column_letter
                ].width = min(max_length + 4, 35)

            for column_cells in worksheet.columns:
                header = str(column_cells[0].value).lower()

                if "revenue" in header or "price" in header:
                    for cell in column_cells[1:]:
                        cell.number_format = '₹#,##0.00'

            for row in worksheet.iter_rows(min_row=2):
                for cell in row:
                    cell.border = thin_border

            worksheet.row_dimensions[1].height = 25

        workbook.save(file_path)

        logger.info("Successfully formatted: %s", file_path.name)

    except Exception:
        logger.exception(
            "Failed to format Excel file: %s", file_path
        )
        raise

def generate_excel_reports(
    valid_df,
    rejected_df,
    category_summary,
    region_summary,
    product_summary,
    monthly_summary,
    output_dir="output"
):
    logger = setup_logger()

    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        valid_file = output_path / "cleaned_sales.xlsx"
        rejected_file = output_path / "reject_records.xlsx"
        report_file = output_path / "sales_report.xlsx"

        logger.info("Starting Excel report generation")

        valid_df.to_excel(valid_file, index=False)
        logger.info("Generated cleaned sales report")

        rejected_df.to_excel(rejected_file, index=False)
        logger.info("Generated rejected records report")
        
        logger.info("Writing sales summary report")
        with pd.ExcelWriter(
            report_file,
            engine="openpyxl"
        ) as writer:
            category_summary.to_excel(
                writer, sheet_name="category_summary", index=False
            )
            region_summary.to_excel(
                writer, sheet_name="region_summary", index=False
            )
            product_summary.to_excel(
                writer, sheet_name="product_summary", index=False
            )
            monthly_summary.to_excel(
                writer, sheet_name="monthly_summary", index=False
            )

        logger.info("Generated sales summary report")

        for file_path in [valid_file, rejected_file, report_file]:
            format_excel_file(file_path)
            logger.info("Formatted report: %s", file_path.name)

        logger.info("All Excel reports generated successfully")
        print("\nExcel reports generated successfully")
        print(f"Output folder: {output_path.resolve()}")

    except Exception:
        logger.exception("Failed to generate Excel reports")
        raise
