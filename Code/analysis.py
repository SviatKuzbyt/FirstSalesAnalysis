import pandas as pd
import matplotlib.pyplot as plt

def build_diagram(df1, title, df2=None):
    plt.figure(figsize=(10, 6))
    df1.plot(kind='line', label='Sales' if df2 is not None else None)
    if df2 is not None:
        df2.plot(kind='line', label='Profit')
        plt.legend()
    plt.title(title)
    plt.ylabel('Revenue')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

FILE = "./Data/clear_retail_sales.csv"

try:
    # Load and prepare data
    df_retail = pd.read_csv(FILE)
    df_retail['Date'] = pd.to_datetime(df_retail['Date'])

    # Data analysis
    df_days_sales = df_retail.groupby("Date")["Sales"].sum().round(2)
    df_month_sales = df_retail.groupby(df_retail["Date"].dt.to_period('M'))['Sales'].sum().round(2)

    df_categories_sales = df_retail.groupby("Category")["Sales"].sum().round(2)
    df_categories_profit = df_retail.groupby("Category")["Profit"].sum().round(2)

    pivot_sales_category = pd.pivot_table(
        df_retail, 
        index='Region', 
        columns='Category', 
        values='Sales', 
        aggfunc='mean'
    ).round(2)

    # Visualization
    action = input("Show diagrams? (y/n): ").lower()
    if action == 'y':
        build_diagram(df_month_sales, 'Total Sales by Month')
        build_diagram(df_days_sales, 'Total Sales by Days')
        build_diagram(df_categories_sales, 'Total Sales and Profit by Category', df_categories_profit)

    # Display numerical results
    action = input("Show results? (y/n): ").lower()
    if action == 'y':
        print("\nTable 1 | Sales by Month")
        print(df_month_sales)

        print("\nTable 2 | Sales by Category")
        print(df_categories_sales)

        print("\nTable 3 | Profit by Category")
        print(df_categories_profit)

        print("\nTable 4 | Pivot: Mean Sales per Category")
        print(pivot_sales_category)
        print()

    # Export to Excel
    action = input("Save results? (y/n): ").lower()
    if action == 'y':
        with pd.ExcelWriter("./Data/retail_report.xlsx") as writer:
            df_days_sales.to_excel(writer, sheet_name='Sales by Days')
            df_month_sales.to_excel(writer, sheet_name='Sales by Months')
            df_categories_sales.to_excel(writer, sheet_name='Sales by Categories')
            df_categories_profit.to_excel(writer, sheet_name='Profit by Categories')
            pivot_sales_category.to_excel(writer, sheet_name='Pivot Sales Category')

        print("Results were saved successfully")
        
except Exception as e:
    print(f"Unexpected error | {e}")