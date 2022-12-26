import pandas
import yfinance as yf

DEBUG = 0

def fetch_stock_data_from_yfinance(stock_symbol):
    tickerData = yf.Ticker(stock_symbol)
    info = tickerData.info
    tickerDf = tickerData.history(period='max')
    return info, tickerDf

def process_stock_data(tickerDf):
    # init
    result = {}

    # get first 5 records
    df =  tickerDf.head(5)

    # get IPO date
    ipo_date_raw = df.index[0].to_pydatetime()
    result.update({'IPO_Date': ipo_date_raw.strftime('%Y-%m-%d')})
    result.update({'IPO_Timezone': str(ipo_date_raw.tzinfo)})

    # get IPO open price
    item = df.iloc[0]
    if DEBUG: print(item.keys())
    result.update({'Open_1': float(item.Open)})

    # get next 4 days close price
    for i in range(1, 5):
        key = 'Close_{}'.format(i+1)
        item = df.iloc[i]
        result.update({key: float(item.Close)})
    
    return result


# batch processing
excel_data_df = pandas.read_excel('input.xlsx', sheet_name='Sheet1')

for idx in excel_data_df.index:
    # input
    symbol   = excel_data_df.loc[idx, 'Symbol']

    # get ticker dataframe
    info, tickerDf = fetch_stock_data_from_yfinance(symbol)

    # get company's info
    excel_data_df.loc[idx, 'Name']      = info['longName']
    
    # process the first 5 days after IPO
    stock_data = process_stock_data(tickerDf)

    excel_data_df.loc[idx, 'IPO_Date']      = stock_data['IPO_Date']
    excel_data_df.loc[idx, 'IPO_Timezone']  = stock_data['IPO_Timezone']

    excel_data_df.loc[idx, 'Open_1']  = str(stock_data['Open_1'])
    excel_data_df.loc[idx, 'Close_2'] = str(stock_data['Close_2'])
    excel_data_df.loc[idx, 'Close_3'] = str(stock_data['Close_3'])
    excel_data_df.loc[idx, 'Close_4'] = str(stock_data['Close_4'])
    excel_data_df.loc[idx, 'Close_5'] = str(stock_data['Close_5'])

    if DEBUG: print(excel_data_df.iloc[idx])

print(excel_data_df)
excel_data_df.to_excel('output.xlsx', index=False)