import pandas as pd 

def calculate_revenue(df):
    sales_df=df.copy()
    
    sales_df["revenue"]=(sales_df["quantity"]*sales_df["unit_price"])
    return sales_df   

def category_wise_sales(df):
    category_summary=(
        df.groupby("category")
        .agg(
            total_orders=("order_id","count"),
            total_quantity=("quantity","sum"),
            total_revenue=("revenue","sum")
        )
    .reset_index()
    .sort_values("total_revenue",ascending=False)
    )
    return category_summary

def region_wise_sales(df):
    region_summary=(
        df.groupby("region")
        .agg(
            total_orders=("order_id","count"),
            total_quantity=("quantity","sum"),
            total_revenue=("revenue","sum")
        )
    .reset_index()
    .sort_values("total_revenue",ascending=False)
    )
    return region_summary

def top_sell_products(df):
    product_summary=(df.groupby("product_name")
                    .agg(
                        total_orders=("order_id","count"),
                        total_quantity=("quantity","sum"),
                        total_revenue=("revenue","sum")
                    )
                    .reset_index()
                    .sort_values("total_revenue",ascending=False))
    return product_summary

      
def monthly_sales(df):
    monthly_df=df.copy()
    monthly_df["order_date"]=pd.to_datetime(monthly_df["order_date"],errors="coerce")
    
    monthly_df["month"]=monthly_df["order_date"].dt.strftime("%B")
    
    monthly_summary=(monthly_df.groupby("month")
                     .agg(
                         total_orders=("order_id","count"),
                         total_quantity=("quantity","sum"),
                         total_revenue=("revenue","sum")
                     )
                    .reset_index()
                    )
    return monthly_summary