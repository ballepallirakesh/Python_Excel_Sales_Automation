import pandas as pd
import pytest
from src.excel_reader import read_sales_files

def test_read_multiple_excel_files(tmp_path):
    # Arrange: create two sample Excel files
    january_data = pd.DataFrame({
        "order_id": ["ORD001"],
        "order_date": ["2026-01-05"],
        "product_name": ["Laptop"],
        "category": ["Electronics"],
        "quantity": [1],
        "unit_price": [50000],
        "region": ["Hyderabad"],
        "customer_name": ["Ravi"]
    })

    february_data = pd.DataFrame({
        "order_id": ["ORD002", "ORD003"],
        "order_date": ["2026-02-05", "2026-02-06"],
        "product_name": ["Mouse", "Keyboard"],
        "category": ["Accessories", "Accessories"],
        "quantity": [2, 1],
        "unit_price": [500, 1000],
        "region": ["Bengaluru", "Chennai"],
        "customer_name": ["Arun", "Kiran"]
    })

    january_data.to_excel(
        tmp_path / "january.xlsx",
        index=False
    )

    february_data.to_excel(
        tmp_path / "february.xlsx",
        index=False
    )

    # Act: read and combine both Excel files
    result = read_sales_files(tmp_path)

    # Assert: verify the results
    assert len(result) == 3
    assert "source_file" in result.columns
    assert result["order_id"].tolist() == [
        "ORD002",
        "ORD003",
        "ORD001"
    ]
    assert result["source_file"].nunique() == 2
    assert set(result["source_file"]) == {
        "january.xlsx",
        "february.xlsx"
    }

def test_missing_input_directory(tmp_path):
    missing_folder = tmp_path / "missing_folder"

    with pytest.raises(FileNotFoundError):
        read_sales_files(missing_folder)

def test_empty_input_directory(tmp_path):
    empty_folder = tmp_path / "empty_folder"
    empty_folder.mkdir()

    with pytest.raises(
        FileNotFoundError,
        match="No Excel files found"
    ):
        read_sales_files(empty_folder)  

def test_missing_required_columns(tmp_path):
    # Arrange: create an Excel file with incomplete columns
    incomplete_data = pd.DataFrame({
        "order_id": ["ORD001"],
        "product_name": ["Laptop"]
    })

    incomplete_data.to_excel(
        tmp_path / "incomplete.xlsx",
        index=False
    )

    # Act and Assert
    with pytest.raises(
        ValueError,
        match="is missing columns"
    ):
        read_sales_files(tmp_path)   
        
def test_corrupted_excel_file(tmp_path):
    # Arrange: create an invalid Excel file
    corrupted_file = tmp_path / "corrupted.xlsx"
    corrupted_file.write_text(
        "This is not a valid Excel workbook"
    )

    # Act and Assert
    with pytest.raises(
        ValueError,
        match="File is corrupted or unreadable"
    ):
        read_sales_files(tmp_path)