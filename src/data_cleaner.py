import pandas as pd 

def clean_data(df):
    cleaned_df=df.copy()
    
    cleaned_df.columns=(cleaned_df.columns.str.strip().str.lower())
    
    text_columns=[
        "order_id",
        "product_name",
        "category",
        "region",
        "customer_name"
    ]
    
    for column in text_columns:
        cleaned_df[column]=(
            cleaned_df[column].astype("string").str.strip().str.title()
        )
    cleaned_df["order_id"]=cleaned_df["order_id"].str.upper()
    return cleaned_df

if __name__=="__main__":
    from src.excel_reader import read_sales_files 
    sales_df=read_sales_files()
    cleaned_df=clean_data(sales_df)
    print("\n cleaned first five records")
    print(cleaned_df.head())
    print("\n Total records:",len(cleaned_df))
    