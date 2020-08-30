#This program downloads the daily adj close stock price from yahoo finance
#and stores in the same path as this python file.
#Can also define frequency of data to replicate Yahoo Finance
#written by Calvin Tam on 8/23/2020

import pandas as pd
import pandas_datareader as web
from datetime import datetime

print('This program allows you to enter in each stock manually or import from')
print('a file named ticker_list.csv.')

choose_option = input('Type 0 to manually enter ticker symbols or 1 to import file: ')
choose_option = int(choose_option)

#test to see if 0 or 1 was entered and loop until user chooses either or enters a string
while choose_option != 1 and choose_option != 0:
	choose_option = int(input('Please enter either a 0 or 1: '))


def get_dates():
	start_year = int(input('Enter start year: '))
	start_month = int(input('Enter start month: '))
	start_day = int(input('Enter in start day: '))
	end_year = int(input('Enter in end year: '))
	end_month = int(input('Enter in end month: '))
	end_day = int(input('Enter in end day: '))

	start = datetime(start_year, start_month, start_day)
	end = datetime(end_year, end_month, end_day)

	return start, end

def get_adj_close(ticker_list):
	i = 0
	while i < len(ticker_list):
		try:
			df = web.DataReader(ticker_list[i], 'yahoo', start = start, end = end)
			df = df.drop(columns = ['High', 'Low', 'Open', 'Close', 'Volume']) #only want adj close price
			df = df.rename(columns={'Adj Close': ticker_list[i]}) #replace adj close column with ticker symbol
			if i == 0:
				master_df = df
			else:
				master_df = master_df.merge(df, on= 'Date', how = 'left')
		except:
			print('No information for ticker symbol ', ticker_list[i])
			i = i + 1 #added this to stop infinite loop
			continue
		i = i + 1

	return master_df


#user chooses to enter ticker symbols manually
if choose_option == 0:
	n = int(input('\nEnter in # of stock symbols to look up: '))
	freq = (input('Enter frequency (ie. m, w, d): '))

	#get ticker from user
	ticker_list = []
	for x in range(n):
		ticker_list.append(input('Enter ticker symbol: '))

	print(ticker_list)

	#get start and end year, month, day from user
	start, end = get_dates()

	master_df = get_adj_close(ticker_list)

	master_df = master_df.groupby(pd.Grouper(freq = freq)).mean()

	#export to same folder as python file as csv file
	master_df.to_csv(r'stock_data.csv')
	print('Export complete as stock_data.csv.')

else:
	freq = (input('Enter frequency (ie. m, w, d): '))

	stock_df = pd.read_csv('ticker_list.csv', header = None)
	ticker_list = []
	for rows in stock_df.iloc[:, 0]:
		ticker_list.append(rows)

	print(ticker_list)

	#get start and end year, month, day from user
	start, end = get_dates()

	master_df = get_adj_close(ticker_list)

	master_df = master_df.groupby(pd.Grouper(freq = freq)).mean()

	#export to same folder as python file as csv file
	master_df.to_csv(r'stock_data.csv')
	print('Export complete as stock_data.csv.')

