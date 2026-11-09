
import pandas as pd

from src.data_cleaner import clean_data

def test_clean_text_columns():
    # Arrange
    data = pd.DataFrame({
        "order_id": [" ord001 "],
        "product_name": [" keyboard "],
        "category": [" accessories "],
        "region": [" hyderabad "],
        "customer_name": [" rakesh "]
    })

    # Act
    result = clean_data(data)
    
    # Assert
    assert result.loc[0, "order_id"] == "ORD001"
    assert result.loc[0, "product_name"] == "Keyboard"
    assert result.loc[0, "category"] == "Accessories"
    assert result.loc[0, "region"] == "Hyderabad"
    assert result.loc[0, "customer_name"] == "Rakesh"


def test_cleaner_does_not_modify_original_dataframe():
    # Arrange
    data = pd.DataFrame({
        "order_id": [" ord001 "],
        "product_name": [" keyboard "],
        "category": [" accessories "],
        "region": [" hyderabad "],
        "customer_name": [" rakesh "]
    })

    original_data = data.copy(deep=True)

    # Act
    result = clean_data(data)

    # Assert
    pd.testing.assert_frame_equal(data, original_data)

    assert result.loc[0, "order_id"] == "ORD001"
    
def test_cleaner_preserves_missing_values():
    # Arrange
    data = pd.DataFrame({
        "order_id": ["ORD001"],
        "product_name": [None],
        "category": ["electronics"],
        "region": ["hyderabad"],
        "customer_name": [None]
    })

    # Act
    result = clean_data(data)

    # Assert
    assert pd.isna(result.loc[0, "product_name"])
    assert pd.isna(result.loc[0, "customer_name"])

    assert result.loc[0, "category"] == "Electronics"
    assert result.loc[0, "region"] == "Hyderabad"