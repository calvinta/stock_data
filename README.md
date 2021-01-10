# stock_data
Download adjusted close price stock data from pandas-datareader web Yahoo Finance API.

The app takes a CSV file of ticker symbols listed in the rows of the first column and looks it up on the Yahoo Finance API.
Tickers must be in the first row without any gap rows with no symbol in order for the app to capture all listed symbols.

After the tickers have been stored in ticker_list, the app asks for the start and end date as well as the frequency.
Frequency is if you want daily, weekly, or monthly closing prices. The prices are then stored in a master_df dataframe after dropping the columns High, Low, Open,
Close, and Volume.

Each periods adjusted closing price is stored in a row under one column. The column name is renamed to the ticker symbol.

The program has an export button which allows the dataframe to be saved as a CSV file in the user's folder of choice.
