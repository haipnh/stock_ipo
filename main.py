import pandas
from datetime import datetime, timedelta
import yfinance as yf

DEBUG = 0

def get_end_date_str(start_date, days_after=10):
    if DEBUG: print(start_date)
    # Date string format: yyyy-mm-dd
    date_object = datetime.strptime(start_date, '%Y-%m-%d').date()
    td = timedelta(days=days_after)
    return str(date_object+td)

def fetch_stock_data_from_yfinance(stock_symbol, start_date, end_date):
    tickerData = yf.Ticker(stock_symbol)
    tickerDf = tickerData.history(period='1mo', start=start_date, end=end_date)
    return tickerDf

def process_stock_data(tickerDf):
    # init
    result = []
    # get first 5 records
    df =  tickerDf.head(5)
    # get open price
    item = df.iloc[0]
    if DEBUG: print(item.keys())
    result.append(float(item.Open))
    # get next 4 days close price
    for i in range(1, 5):
        item = df.iloc[i]
        result.append(float(item.Close))
    
    return result


# batch processing
excel_data_df = pandas.read_excel('input.xlsx', sheet_name='Sheet1')

for idx in excel_data_df.index:
    # input
    symbol   = excel_data_df.loc[idx, "Symbol"]
    ipo_date = excel_data_df.loc[idx, "IPO_Date"]
    
    # get end_date
    end_date = get_end_date_str(ipo_date)
    if DEBUG: print(end_date)

    # get ticker dataframe
    tickerDf = fetch_stock_data_from_yfinance(symbol, ipo_date, end_date)

    # process the first 5 days after IPO
    prices = process_stock_data(tickerDf)

    excel_data_df.loc[idx, "Open_1"]  = prices[0]
    excel_data_df.loc[idx, "Close_2"] = prices[1]
    excel_data_df.loc[idx, "Close_3"] = prices[2]
    excel_data_df.loc[idx, "Close_4"] = prices[3]
    excel_data_df.loc[idx, "Close_5"] = prices[4]

    if DEBUG: print(excel_data_df.iloc[idx])

print(excel_data_df)
excel_data_df.to_excel('output.xlsx', float_format="%.6f", index=False)