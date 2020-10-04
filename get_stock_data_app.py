# This program downloads the daily adj close stock price from yahoo finance
# and stores in the same path as this python file.
# Can also define frequency of data to replicate Yahoo Finance
# written by Calvin Tam on 9/28/2020

import pandas as pd
import pandas_datareader as web
from datetime import datetime, date
import tkinter as tk
from tkinter import filedialog, Text
import os


# Start of GUI code
window = tk.Tk()
window.title("Get Stock Data")
window.geometry("760x400") # W x H

# Section for functions
def open_file():
	global filename
	filename = filedialog.askopenfilename(initialdir = '/Documents', title = 'Select File', filetypes = (('CSV Files','*.csv'), ('All Files', '*')))
	show_file_imported.config(text = 'File imported is ' + filename)

def get_adj_close():
	stock_df = pd.read_csv(filename, header = None)
	ticker_list = []
	for rows in stock_df.iloc[:, 0]:
		ticker_list.append(rows)
	
	i = 0
	while i < len(ticker_list):
		try:
			df = web.DataReader(ticker_list[i], 'yahoo', start = start_date_entry.get(), end = end_date_entry.get())
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

	master_df = master_df.groupby(pd.Grouper(freq = v.get())).mean()

	#export to same folder as python file as csv file
	master_df.to_csv(r'stock_data.csv')
	done_label.config(text = 'Export complete as stock_data.csv.')


# Section for widgets
tk.Label(window,
		 text = 'Import a CSV file with ticker symbols to download adjusted close prices.').pack(anchor = tk.W,
		 																						 padx = 10,
																								 pady = 5)
import_button = tk.Button(window, text = 'Import tickers from file', command = open_file)
import_button.pack(anchor = tk.W, padx = 10)

show_file_imported = tk.Label(window, text = '', fg = 'blue')
show_file_imported.pack(anchor = tk.W, padx = 10, pady = 5)


tk.Label(window, text = 'Enter in a start date in the format yyyy-mm-dd:').pack(anchor = tk.W, padx = 10)
start_date_entry = tk.Entry(window)
start_date_entry.pack(anchor = tk.W, padx = 10)

tk.Label(window, text = 'Enter in an end date in the format yyyy-mm-dd:').pack(anchor = tk.W, padx = 10)
end_date_entry = tk.Entry(window)
end_date_entry.pack(anchor = tk.W, padx = 10)


v = tk.StringVar()
v.set(-1) # so none of the radiobuttons are selected during start up
freq_options = [("Daily","d"), ("Weekly","w"), ("Monthly","m")]

tk.Label(window, text = 'Choose the frequency:',
				 anchor = tk.W).pack(anchor = tk.W, padx = 10, pady = 5)

for frequency, letter in freq_options:
	freq_buttons = tk.Radiobutton(window, 
				   text = frequency, 
				   padx = 5, 
				   variable = v, 
				   value = letter)
	
	freq_buttons.pack(side = tk.TOP, anchor = tk.W, padx = 10)


execute_button = tk.Button(window, text = 'Execute', command = get_adj_close)
execute_button.pack(anchor = tk.W, padx = 10, pady = 5)

done_label = tk.Label(window, text = '', fg = 'green')
done_label.pack(anchor = tk.W, padx = 10)


window.mainloop()
