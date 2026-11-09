
from src.logger_config import setup_logger

from src.excel_reader import read_sales_files
from src.data_cleaner import clean_data
from src.data_validator import validate_sales_data

from src.sales_analyzer import (
    calculate_revenue,
    category_wise_sales,
    region_wise_sales,
    top_sell_products,
    monthly_sales
)

from src.report_generator import generate_excel_reports


def main():
    logger = setup_logger()

    try:
        logger.info("Sales automation started")

        # Step 1: Read Excel files
        sales_df = read_sales_files()
        logger.info("Excel reading completed")

        # Step 2: Clean data
        cleaned_df = clean_data(sales_df)
        logger.info("Data cleaning completed")

        # Step 3: Validate data
        valid_df, rejected_df = validate_sales_data(cleaned_df)

        logger.info(
            "Data validation completed | Valid: %d | Rejected: %d",
            len(valid_df),
            len(rejected_df)
        )

        # Step 4: Calculate revenue
        revenue_df = calculate_revenue(valid_df)
        logger.info("Revenue calculation completed")

        print("\nSales data with revenue:")
        print(
            revenue_df[
                ["order_id", "product_name", "quantity",
                 "unit_price", "revenue"]
            ].head()
        )

        print("\nTotal sales revenue:")
        print(revenue_df["revenue"].sum())

        # Step 5: Generate sales summaries
        category_summary = category_wise_sales(revenue_df)
        region_summary = region_wise_sales(revenue_df)
        product_summary = top_sell_products(revenue_df)
        monthly_summary = monthly_sales(revenue_df)

        logger.info("Sales analysis completed")

        print("\nCategory-wise sales:")
        print(category_summary)

        print("\nRegion-wise sales:")
        print(region_summary)

        print("\nTop-sell products:")
        print(product_summary)

        print("\nMonthly sales:")
        print(monthly_summary)

        # Step 6: Generate Excel reports
        generate_excel_reports(
            valid_df,
            rejected_df,
            category_summary,
            region_summary,
            product_summary,
            monthly_summary
        )

        logger.info("Sales automation completed successfully")

    except Exception:
        logger.exception("Sales automation failed")
        print("\nSales automation failed. Check logs/automation.log")
        raise


if __name__ == "__main__":
    main()
