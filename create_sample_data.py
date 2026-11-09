from pathlib import Path 
import pandas as pd 

INPUT_DIR=Path("input")
INPUT_DIR.mkdir(exist_ok=True)

january_sales=[
    [f"ORD{i:03}","2026-01-05","laptop","electronics",1,55000,"Hyderabad","Ravi"]
    for i in range(1,11)
    
]

february_sales=[["ORD011","2026-02-02","mouse","accessories",2,500,"Bengaluru","Arjun"],
                ["ORD012", "2026-02-04", "Keyboard", "Accessories", 1, 1200, "Hyderabad", "Kiran"],
                ["ORD013", "2026-02-06", "Monitor", "Electronics", 1, 12000, "Chennai", "Suresh"],
                ["ORD014", "2026-02-08", "Laptop", "Electronics", 1, 60000, "Pune", "Priya"],
                ["ORD015", "2026-02-10", "Mouse", "Accessories", 3, 450, "Hyderabad", None],
                ["ORD016", "2026-02-12", "Laptop", "Electronics", 2, 52000, "Bengaluru", "Anil"],
                ["ORD017", "2026-02-14", "Keyboard", "Accessories", -2, 1000, "Chennai", "Ravi"],
                ["ORD018", "2026-02-16", "Monitor", "Electronics", 2, 11000, "Pune", "Manoj"],
                ["ORD019", "2026-02-18", "Mouse", "Accessories", 1, 500, "Bengaluru", "Divya"],
                ["ORD020", "2026-02-20", "Laptop", "Electronics", 1, None, "Hyderabad", "Kiran"],]

march_sales=[["ORD001", "2026-03-01", "Laptop", "Electronics", 1, 55000, "Hyderabad", "Ravi"],
            ["ORD021", "2026-03-03", "Mouse", "Accessories", 2, 500, "Bengaluru", "Arjun"],
            ["ORD022", "2026-03-05", "Monitor", "Electronics", 1, 12000, "Chennai", "Suresh"],
            ["ORD023", "2026-03-07", " Keyboard ", "Accessories", 1, 1200, "Hyderabad", "Priya"],
            ["ORD024", "2026-03-09", "Mouse", "Accessories", "invalid", 450, "Pune", "Anil"],
            ["ORD025", "2026-03-11", "Laptop", "Electronics", 1, 60000, "Bengaluru", "Ravi"],
            ["ORD026", "2026-03-13", "Keyboard", "Accessories", 2, 1000, "Chennai", "Manoj"],
            ["ORD027", "2026-03-15", "Monitor", "Electronics", 1, 11000, "Pune", "Divya"],
            ["ORD028", "2026-03-17", "Mouse", "Accessories", 3, 500, "Hyderabad", "Kiran"],
            ["ORD029", "2026-03-19", "Laptop", "Electronics", 1, 52000, "Bengaluru", "Suresh"],]

columns=[
    "order_id",
    "order_date",
    "product_name",
    "category",
    "quantity",
    "unit_price",
    "region",
    "customer_name"
]

#convert data into dataframes
sales_files={
    "sales_january.xlsx":pd.DataFrame(january_sales,columns=columns),
    "sales_february.xlsx":pd.DataFrame(february_sales,columns=columns),
    "sales_march.xlsx":pd.DataFrame(march_sales,columns=columns)
}

for filename,dataframe in sales_files.items():
    filepath=INPUT_DIR/filename 
    dataframe.to_excel(filepath,index=False)
    print(f"created:{filepath} | Records:{len(dataframe)}")

print("\n All sample Excel files generated successfully")