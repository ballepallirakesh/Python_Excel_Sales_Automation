from pathlib import Path 
import pandas as pd 
from src.logger_config import setup_logger
logger=setup_logger()
REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "product_name",
    "category",
    "quantity",
    "unit_price",
    "region",
    "customer_name"
]

def read_sales_files(input_dir="input"):
    folder = Path(input_dir)

    logger.info("Starting Excel file reading")

    try:
        if not folder.exists():
            raise FileNotFoundError(
                f"Input directory does not exist: {folder}"
            )

        if not folder.is_dir():
            raise NotADirectoryError(
                f"Input path is not a directory: {folder}"
            )

        excel_files = sorted(folder.glob("*.xlsx"))

        if not excel_files:
            raise FileNotFoundError(
                f"No Excel files found in: {folder}"
            )

        dataframes = []

        for file in excel_files:
            logger.info("Reading file: %s", file.name)

            try:
                df = pd.read_excel(file)
            except Exception as error:
                raise ValueError(
                    f"File is corrupted or unreadable: {file.name}"
                ) from error

            df.columns = df.columns.astype(str).str.strip().str.lower()

            missing_columns = [
                column for column in REQUIRED_COLUMNS
                if column not in df.columns
            ]

            if missing_columns:
                raise ValueError(
                    f"{file.name} is missing columns: {missing_columns}"
                )

            df["source_file"] = file.name
            dataframes.append(df)

            logger.info(
                "Successfully read %s | Records: %d",
                file.name,
                len(df)
            )

        combined_df = pd.concat(dataframes, ignore_index=True)

        logger.info(
            "Successfully merged %d files | Total records: %d",
            len(excel_files),
            len(combined_df)
        )

        return combined_df

    except Exception:
        logger.exception("Excel reading process failed")
        raise


if __name__ == "__main__":
    sales_df = read_sales_files()

    print("\nFirst five records:")
    print(sales_df.head())

    print("\nTotal records:", len(sales_df))
