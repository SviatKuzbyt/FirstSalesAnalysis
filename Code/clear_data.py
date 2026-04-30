import pandas as pd

# Configuration
MAX_LOSS_PERCENT = 5.0
INPUT_FILE = "./Data/retail_sales.csv"
OUTPUT_FILE = "./Data/clear_retail_sales.csv"

try:
    # 1. Loading data and handling missing value markers
    df = pd.read_csv(INPUT_FILE, na_values=['NaN', 'NaN?', 'nan', 'null', 'Nan', 'Null'])
    initial_rows = len(df)
    current_loss = 0.0

    # 2. Cleaning missing data (NaN)
    nan_mask = df.isna().any(axis=1)
    nan_count = nan_mask.sum()
    nan_percent = (nan_count / initial_rows) * 100

    print(f"Summary 1\t| Missing values: {nan_count}, Total: {initial_rows}, Percent: {nan_percent:.4f}%")

    if nan_percent <= (MAX_LOSS_PERCENT - current_loss):
        print(f"Action 1\t| Removing missing data (within {MAX_LOSS_PERCENT}% limit)")
        df = df.dropna().copy()
        current_loss += nan_percent
    else:
        print("Error\t| Too many missing values. Analysis aborted.")
        exit()

    # 3. Cleaning anomalies (Profit > Sales or Quantity < 0)
    sales_anomaly = df['Profit'] > df['Sales']
    quantity_anomaly = df['Quantity'] < 0
    anomaly_mask = sales_anomaly | quantity_anomaly
    
    anomaly_count = anomaly_mask.sum()
    anomaly_percent = (anomaly_count / initial_rows) * 100

    print(f"Summary 2\t| Sales anomalies: {sales_anomaly.sum()}, Quantity anomalies: {quantity_anomaly.sum()}, Total anomalies: {anomaly_count}, Percent: {anomaly_percent:.4f}%")

    if anomaly_percent <= (MAX_LOSS_PERCENT - current_loss):
        print(f"Action 2\t| Removing anomalies (within {MAX_LOSS_PERCENT}% limit)")
        df = df[~anomaly_mask].copy()
        current_loss += anomaly_percent
    else:
        print("Error\t| Too many anomalies. Analysis aborted.")
        exit()

    # 4. Formatting dates and handling conversion errors
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    date_err_mask = df['Date'].isna()
    date_err_count = date_err_mask.sum()
    date_err_percent = (date_err_count / initial_rows) * 100

    print(f"Summary 3\t| Invalid dates: {date_err_count}, Percent: {date_err_percent:.4f}%")

    if date_err_percent <= (MAX_LOSS_PERCENT - current_loss):
        print(f"Action 3\t| Removing invalid dates (within {MAX_LOSS_PERCENT}% limit)")
        df_final = df[~date_err_mask].copy()

        # 5. Saving the result
        df_final.to_csv(OUTPUT_FILE, index=False)
        print("Action 4\t| Processed data saved successfully")
    else:
        print("Error\t| Too many date errors. Analysis aborted.")

except Exception as e:
    print(f"Unexpected error\t| {e}")