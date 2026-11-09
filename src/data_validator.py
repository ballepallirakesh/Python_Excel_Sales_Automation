import pandas as pd 

def validate_sales_data(df):
    validated_df=df.copy()
    rejected_reasons=[[] for _ in range(len(validated_df))]
    
    missing_order_id=(validated_df["order_id"].isna() | validated_df["order_id"].eq(""))
    duplicate_order_id=(validated_df["order_id"].duplicated(keep="first") &~missing_order_id)
    missing_customer=(validated_df["customer_name"].isna() | validated_df["customer_name"].eq(""))
    quantity=pd.to_numeric(validated_df["quantity"],errors="coerce")
    invalid_quantity=quantity.isna() | (quantity<=0)
    
    unit_price=pd.to_numeric(validated_df["unit_price"],errors="coerce")
    invalid_price=unit_price.isna()|(unit_price <=0)
    order_dates=pd.to_datetime(validated_df["order_date"],errors="coerce",format="mixed")
    invalid_date=order_dates.isna()
    
    validation_checks=[
        (missing_order_id, "Missing order ID"),
        (duplicate_order_id, "Duplicate order ID"),
        (missing_customer, "Missing customer name"),
        (invalid_quantity, "Invalid quantity"),
        (invalid_price, "Missing or invalid unit price"),
        (invalid_date, "Invalid order date"),
    ]
    
    for condition,reason in validation_checks:
        for index,is_invalid in enumerate(condition):
            if is_invalid:
                rejected_reasons[index].append(reason)
    
    validated_df["rejected_reasons"]=[";".join(reasons) for reasons in rejected_reasons]
    reject_df=validated_df[validated_df["rejected_reasons"]!=""].copy()
    valid_df=validated_df[validated_df["rejected_reasons"]==""].copy()
    
    print("Total_records:",len(validated_df))
    print("valid_records:",len(valid_df))
    print("reject_records:",len(reject_df))
    return valid_df, reject_df
    
if __name__=="__main__":
    from src.excel_reader import read_sales_files 
    from src.data_cleaner import clean_data 
    
    sales_df=read_sales_files()
    cleaned_df=clean_data(sales_df)
    valid_df, reject_df = validate_sales_data(cleaned_df)
    
    print("/n reject rows")
    print(reject_df[["order_id","rejected_reasons","source_file"]])
    print("/n valid rows")
    print(valid_df.head())