import pandas as pd
from src.sales_analyzer import calculate_revenue
from src.sales_analyzer import category_wise_sales
from src.sales_analyzer import region_wise_sales 
from src.sales_analyzer import top_sell_products 
from src.sales_analyzer import monthly_sales


def test_calculate_revenue():
    # Arrange
    data = pd.DataFrame({
        "order_id": ["ORD001", "ORD002"],
        "product_name": ["Laptop", "Mouse"],
        "quantity": [2, 3],
        "unit_price": [50000, 500]
    })

    # Act
    result = calculate_revenue(data)

    # Assert
    assert "revenue" in result.columns
    assert result["revenue"].tolist() == [100000, 1500]


def test_calculate_revenue_does_not_modify_original_dataframe():
    # Arrange
    data = pd.DataFrame({
        "order_id": ["ORD001"],
        "product_name": ["Laptop"],
        "quantity": [2],
        "unit_price": [50000]
    })

    original_data = data.copy(deep=True)

    # Act
    calculate_revenue(data)

    # Assert
    pd.testing.assert_frame_equal(data, original_data)   

def test_category_wise_sales():
    # Arrange
    data = pd.DataFrame({
        "order_id": ["ORD001", "ORD002", "ORD003", "ORD004"],
        "category": [
            "Electronics",
            "Accessories",
            "Electronics",
            "Accessories"
        ],
        "quantity": [2, 3, 1, 2],
        "revenue": [100000, 1500, 50000, 1000]
    })

    # Act
    result = category_wise_sales(data)

    # Assert
    assert len(result) == 2

    electronics = result[result["category"] == "Electronics"].iloc[0]
    accessories = result[result["category"] == "Accessories"].iloc[0]

    assert electronics["total_orders"] == 2
    assert electronics["total_quantity"] == 3
    assert electronics["total_revenue"] == 150000

    assert accessories["total_orders"] == 2
    assert accessories["total_quantity"] == 5
    assert accessories["total_revenue"] == 2500

    # Verify descending revenue order
    assert result.iloc[0]["category"] == "Electronics"


def test_region_wise_sales():
    # Arrange
    data = pd.DataFrame({
        "order_id": ["ORD001", "ORD002", "ORD003", "ORD004"],
        "region": [
            "Hyderabad",
            "Bengaluru",
            "Hyderabad",
            "Chennai"
        ],
        "quantity": [2, 3, 1, 4],
        "revenue": [100000, 30000, 50000, 20000]
    })

    # Act
    result = region_wise_sales(data)

    # Assert
    assert len(result) == 3

    hyderabad = result[result["region"] == "Hyderabad"].iloc[0]

    assert hyderabad["total_orders"] == 2
    assert hyderabad["total_quantity"] == 3
    assert hyderabad["total_revenue"] == 150000

    # Verify descending revenue order
    assert result.iloc[0]["region"] == "Hyderabad"
    assert result.iloc[1]["region"] == "Bengaluru"
    assert result.iloc[2]["region"] == "Chennai"

def test_top_sell_products():
    # Arrange
    data = pd.DataFrame({
        "order_id": ["ORD001", "ORD002", "ORD003", "ORD004"],
        "product_name": ["Laptop", "Mouse", "Laptop", "Keyboard"],
        "quantity": [2, 3, 1, 4],
        "revenue": [100000, 1500, 50000, 4000]
    })

    # Act
    result = top_sell_products(data)

    # Assert
    assert len(result) == 3

    laptop = result[result["product_name"] == "Laptop"].iloc[0]

    assert laptop["total_orders"] == 2
    assert laptop["total_quantity"] == 3
    assert laptop["total_revenue"] == 150000

    # Verify descending revenue order
    assert result.iloc[0]["product_name"] == "Laptop"
    assert result.iloc[1]["product_name"] == "Keyboard"
    assert result.iloc[2]["product_name"] == "Mouse"

from src.sales_analyzer import monthly_sales


def test_monthly_sales():
    # Arrange
    data = pd.DataFrame({
        "order_id": ["ORD001", "ORD002", "ORD003", "ORD004"],
        "order_date": [
            "2026-01-05",
            "2026-01-15",
            "2026-02-10",
            "2026-03-20"
        ],
        "quantity": [2, 3, 1, 4],
        "revenue": [100000, 30000, 50000, 20000]
    })

    # Act
    result = monthly_sales(data)

    # Assert
    assert len(result) == 3

    january = result[result["month"] == "January"].iloc[0]
    february = result[result["month"] == "February"].iloc[0]
    march = result[result["month"] == "March"].iloc[0]

    assert january["total_orders"] == 2
    assert january["total_quantity"] == 5
    assert january["total_revenue"] == 130000

    assert february["total_orders"] == 1
    assert february["total_revenue"] == 50000

    assert march["total_orders"] == 1
    assert march["total_revenue"] == 20000