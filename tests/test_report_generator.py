import pytest
import pandas as pd
from src.report_generator import generate_excel_reports
from openpyxl import load_workbook
from src.report_generator import format_excel_file
def test_generate_excel_reports(tmp_path):
    # Arrange
    valid_df = pd.DataFrame({
        "order_id": ["ORD001", "ORD002"],
        "product_name": ["Laptop", "Mouse"],
        "quantity": [2, 3],
        "unit_price": [50000, 500]
    })

    rejected_df = pd.DataFrame({
        "order_id": ["ORD003"],
        "product_name": ["Keyboard"],
        "rejected_reasons": ["Invalid quantity"]
    })

    category_summary = pd.DataFrame({
        "category": ["Electronics"],
        "total_orders": [2],
        "total_quantity": [5],
        "total_revenue": [101500]
    })

    region_summary = pd.DataFrame({
        "region": ["Hyderabad"],
        "total_orders": [2],
        "total_quantity": [5],
        "total_revenue": [101500]
    })

    product_summary = pd.DataFrame({
        "product_name": ["Laptop", "Mouse"],
        "total_orders": [1, 1],
        "total_quantity": [2, 3],
        "total_revenue": [100000, 1500]
    })

    monthly_summary = pd.DataFrame({
        "month": ["January"],
        "total_orders": [2],
        "total_quantity": [5],
        "total_revenue": [101500]
    })

    output_dir = tmp_path / "reports"

    # Act
    generate_excel_reports(
        valid_df,
        rejected_df,
        category_summary,
        region_summary,
        product_summary,
        monthly_summary,
        output_dir
    )
    
    # Assert
    assert (output_dir / "cleaned_sales.xlsx").exists()
    assert (output_dir / "reject_records.xlsx").exists()
    assert (output_dir / "sales_report.xlsx").exists()   


def create_sample_reports(output_dir):
    valid_df = pd.DataFrame({
        "order_id": ["ORD001"],
        "product_name": ["Laptop"],
        "quantity": [2],
        "unit_price": [50000]
    })

    rejected_df = pd.DataFrame({
        "order_id": ["ORD002"],
        "rejected_reasons": ["Invalid quantity"]
    })

    category_summary = pd.DataFrame({
        "category": ["Electronics"],
        "total_orders": [1],
        "total_quantity": [2],
        "total_revenue": [100000]
    })

    region_summary = pd.DataFrame({
        "region": ["Hyderabad"],
        "total_orders": [1],
        "total_quantity": [2],
        "total_revenue": [100000]
    })

    product_summary = pd.DataFrame({
        "product_name": ["Laptop"],
        "total_orders": [1],
        "total_quantity": [2],
        "total_revenue": [100000]
    })

    monthly_summary = pd.DataFrame({
        "month": ["January"],
        "total_orders": [1],
        "total_quantity": [2],
        "total_revenue": [100000]
    })

    generate_excel_reports(
        valid_df,
        rejected_df,
        category_summary,
        region_summary,
        product_summary,
        monthly_summary,
        output_dir
    ) 

def test_sales_report_contains_expected_worksheets(tmp_path):
    # Arrange
    output_dir = tmp_path / "reports"
    create_sample_reports(output_dir)

    report_file = output_dir / "sales_report.xlsx"

    # Act
    workbook = load_workbook(report_file)

    # Assert
    expected_sheets = {
        "category_summary",
        "region_summary",
        "product_summary",
        "monthly_summary"
    }

    assert set(workbook.sheetnames) == expected_sheets

    workbook.close()

def test_excel_report_formatting(tmp_path):
    # Arrange
    output_dir = tmp_path / "reports"
    create_sample_reports(output_dir)

    report_file = output_dir / "sales_report.xlsx"

    # Act
    workbook = load_workbook(report_file)
    worksheet = workbook["category_summary"]

    # Assert

    # Header formatting
    assert worksheet["A1"].font.bold is True
    assert worksheet["A1"].font.color.rgb.endswith("FFFFFF")

    # Frozen header row
    assert worksheet.freeze_panes == "A2"

    # Auto-filter
    assert worksheet.auto_filter.ref == worksheet.dimensions

    # Column width
    assert worksheet.column_dimensions["A"].width > 0

    # Currency formatting
    assert worksheet["D2"].number_format == '₹#,##0.00'

    workbook.close()  

def test_all_generated_workbooks_are_formatted(tmp_path):
    # Arrange
    output_dir = tmp_path / "reports"
    create_sample_reports(output_dir)

    file_names = [
        "cleaned_sales.xlsx",
        "reject_records.xlsx",
        "sales_report.xlsx"
    ]

    # Act & Assert
    for file_name in file_names:
        workbook = load_workbook(output_dir / file_name)

        for worksheet in workbook.worksheets:
            assert worksheet.freeze_panes == "A2"
            assert worksheet.auto_filter.ref == worksheet.dimensions
            assert worksheet["A1"].font.bold is True

        workbook.close()   

def test_report_generation_fails_with_invalid_output_directory(tmp_path):
    # Arrange
    output_blocker = tmp_path / "reports"
    output_blocker.write_text("This is a file, not a directory")

    valid_df = pd.DataFrame()
    rejected_df = pd.DataFrame()
    category_summary = pd.DataFrame()
    region_summary = pd.DataFrame()
    product_summary = pd.DataFrame()
    monthly_summary = pd.DataFrame()

    # Act & Assert
    with pytest.raises(FileExistsError):
        generate_excel_reports(
            valid_df,
            rejected_df,
            category_summary,
            region_summary,
            product_summary,
            monthly_summary,
            output_blocker
        )

def test_format_excel_file_raises_error_for_missing_file(tmp_path):
    # Arrange
    missing_file = tmp_path / "nonexistent.xlsx"

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        format_excel_file(missing_file)