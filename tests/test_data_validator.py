import pandas as pd

from src.data_validator import validate_sales_data

def test_valid_records_are_accepted():
    # Arrange
    data = pd.DataFrame({
        "order_id": ["ORD001", "ORD002"],
        "order_date": ["2026-01-05", "2026-01-06"],
        "product_name": ["Laptop", "Mouse"],
        "category": ["Electronics", "Accessories"],
        "quantity": [1, 2],
        "unit_price": [50000, 500],
        "region": ["Hyderabad", "Bengaluru"],
        "customer_name": ["Ravi", "Arun"]
    })

    # Act
    valid_df, reject_df = validate_sales_data(data)
    # Assert
    assert len(valid_df) == 2
    assert len(reject_df) == 0
    assert valid_df["order_id"].tolist() == ["ORD001", "ORD002"]


def test_duplicate_order_ids_are_rejected():
    # Arrange
    data = pd.DataFrame({
        "order_id": ["ORD001", "ORD001"],
        "order_date": ["2026-01-05", "2026-01-06"],
        "product_name": ["Laptop", "Mouse"],
        "category": ["Electronics", "Accessories"],
        "quantity": [1, 2],
        "unit_price": [50000, 500],
        "region": ["Hyderabad", "Bengaluru"],
        "customer_name": ["Ravi", "Arun"]
    })

    # Act
    valid_df, reject_df = validate_sales_data(data)

    # Assert
    assert len(valid_df) == 1
    assert len(reject_df) == 1

    assert valid_df.iloc[0]["order_id"] == "ORD001"
    assert reject_df.iloc[0]["order_id"] == "ORD001"

    assert (
        reject_df.iloc[0]["rejected_reasons"]
        == "Duplicate order ID"
    )

def test_missing_customer_names_are_rejected():
    # Arrange
    data = pd.DataFrame({
        "order_id": ["ORD001", "ORD002"],
        "order_date": ["2026-01-05", "2026-01-06"],
        "product_name": ["Laptop", "Mouse"],
        "category": ["Electronics", "Accessories"],
        "quantity": [1, 2],
        "unit_price": [50000, 500],
        "region": ["Hyderabad", "Bengaluru"],
        "customer_name": [None, ""]
    })

    # Act
    valid_df, reject_df = validate_sales_data(data)

    # Assert
    assert len(valid_df) == 0
    assert len(reject_df) == 2

    assert all(
        reject_df["rejected_reasons"].str.contains(
            "Missing customer name"
        )
    )

def test_invalid_quantities_are_rejected():
    # Arrange
    data = pd.DataFrame({
        "order_id": ["ORD001", "ORD002", "ORD003", "ORD004"],
        "order_date": ["2026-01-05"] * 4,
        "product_name": ["Laptop", "Mouse", "Keyboard", "Monitor"],
        "category": ["Electronics"] * 4,
        "quantity": [0, -2, "invalid", None],
        "unit_price": [50000, 500, 1000, 2000],
        "region": ["Hyderabad"] * 4,
        "customer_name": ["Ravi", "Arun", "Kiran", "Suresh"]
    })

    # Act
    valid_df, reject_df = validate_sales_data(data)

    # Assert
    assert len(valid_df) == 0
    assert len(reject_df) == 4

    assert all(
        reject_df["rejected_reasons"].str.contains(
            "Invalid quantity"
        )
    )   

def test_invalid_unit_prices_are_rejected():
    # Arrange
    data = pd.DataFrame({
        "order_id": ["ORD001", "ORD002", "ORD003", "ORD004"],
        "order_date": ["2026-01-05"] * 4,
        "product_name": ["Laptop", "Mouse", "Keyboard", "Monitor"],
        "category": ["Electronics"] * 4,
        "quantity": [1, 2, 1, 3],
        "unit_price": [0, -500, "invalid", None],
        "region": ["Hyderabad"] * 4,
        "customer_name": ["Ravi", "Arun", "Kiran", "Suresh"]
    })

    # Act
    valid_df, reject_df = validate_sales_data(data)

    # Assert
    assert len(valid_df) == 0
    assert len(reject_df) == 4

    assert all(
        reject_df["rejected_reasons"].str.contains(
            "Missing or invalid unit price"
        )
    )   

def test_invalid_order_dates_are_rejected():
    # Arrange
    data = pd.DataFrame({
        "order_id": ["ORD001", "ORD002", "ORD003"],
        "order_date": ["invalid-date", None, "2026-01-05"],
        "product_name": ["Laptop", "Mouse", "Keyboard"],
        "category": ["Electronics", "Accessories", "Accessories"],
        "quantity": [1, 2, 1],
        "unit_price": [50000, 500, 1000],
        "region": ["Hyderabad", "Bengaluru", "Chennai"],
        "customer_name": ["Ravi", "Arun", "Kiran"]
    })

    # Act
    valid_df, reject_df = validate_sales_data(data)

    # Assert
    assert len(valid_df) == 1
    assert len(reject_df) == 2

    assert valid_df.iloc[0]["order_id"] == "ORD003"

    assert all(
        reject_df["rejected_reasons"].str.contains(
            "Invalid order date"
        )
    ) 

def test_multiple_rejection_reasons_are_recorded():
    # Arrange
    data = pd.DataFrame({
        "order_id": ["ORD001"],
        "order_date": ["2026-01-05"],
        "product_name": ["Laptop"],
        "category": ["Electronics"],
        "quantity": [-2],
        "unit_price": [0],
        "region": ["Hyderabad"],
        "customer_name": [None]
    })

    # Act
    valid_df, reject_df = validate_sales_data(data)

    # Assert
    assert len(valid_df) == 0
    assert len(reject_df) == 1

    reasons = reject_df.iloc[0]["rejected_reasons"]

    assert "Missing customer name" in reasons
    assert "Invalid quantity" in reasons
    assert "Missing or invalid unit price" in reasons

    assert reasons.count(";") == 2   


def test_validator_does_not_modify_original_dataframe():
    # Arrange
    data = pd.DataFrame({
        "order_id": ["ORD001", "ORD001"],
        "order_date": ["2026-01-05", "2026-01-06"],
        "product_name": ["Laptop", "Mouse"],
        "category": ["Electronics", "Accessories"],
        "quantity": [1, 2],
        "unit_price": [50000, 500],
        "region": ["Hyderabad", "Bengaluru"],
        "customer_name": ["Ravi", "Arun"]
    })

    original_data = data.copy(deep=True)

    # Act
    valid_df, reject_df = validate_sales_data(data)

    # Assert
    pd.testing.assert_frame_equal(data, original_data)