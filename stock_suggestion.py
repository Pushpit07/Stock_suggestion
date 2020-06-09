import requests
import json
import yfinance as yf
import time
import matplotlib.pyplot as plt
import datetime
import os

print("\n" * 2)
width = os.get_terminal_size().columns
print("Level 1".center(width))
print()
print("GET Request".center(width))
print()


#GET request begins
URL = "https://sheet.best/api/sheets/c4004fdb-71a4-479c-866f-9f810072a9b3"

X_API_KEY_ENDPOINT1 = "YX%d6$7waWCQ#G6u8$@BlC%WQ!WPJAGsy3_vl4N9XB7C9Mo23cP56Jl!HZrQhsW6"

param = dict(key=X_API_KEY_ENDPOINT1)

received_data = requests.get(URL, params=param)
#GET request ends



#printing the json 
unformatted_json = received_data.json()

formatted_json = json.dumps(unformatted_json, indent=2)
print(formatted_json)
print("\n" * 2)

#storing the ticker and price in arrays
dat = json.loads(formatted_json)
ticker_array = []
price_array = []

for i in range(len(dat)):
	ticker_array.append(dat[i]["ticker"])
	price_array.append(dat[i]["purchasePrice"])



#POST request begins
print("POST Request".center(width))
print("\n")

current_milli_time = int(round(time.time() * 1000))

API_ENDPOINT = "https://sheet.best/api/sheets/fec49be9-d3f0-4a08-bc38-5104ef9a2faf"

X_API_ENDPOINT_KEY = "F5%wnQP97E6ffD_RVzef!!3z-C@ue#uU#%RO0masY_uYPIM3R10$m2Ebrl0qKSPI"

headers = {"X-Api-Key": X_API_ENDPOINT_KEY}



ticker_lower = []
for i in range(len(ticker_array)):
	ticker_lower.append(ticker_array[i].lower())


average = []
for i in range(len(ticker_lower)):
	ticker_lower[i] = yf.Ticker(ticker_array[i])
	hist = ticker_lower[i].history(period="1mo")

	sum = 0

	for i in hist["Close"]:
		sum += i

	average.append(round(sum/len(hist["Close"]),2))
	

final_data = []
for i in range(len(ticker_array)):
	data_to_send = dict(name="pushpit", ticker=ticker_array[i], purchasePrice=int(price_array[i]) , average=average[i], shouldSell="true" if (int(average[i])>int(price_array[i])) else "false" , createdAt=current_milli_time)
	final_data.append(data_to_send)

formatted_data1 = json.dumps(final_data, indent=2)
print(formatted_data1)

for i in range(len(final_data)):
	response1 = requests.post(API_ENDPOINT, data=final_data[i], headers=headers)	
#POST request ends


print("Level 2".center(width))
print("Visualization".center(width))
print()
#Plotting the graph
answer = 'Y'

while answer == 'y' or answer == 'Y':
	print("\n" * 2)
	print("Please input the number of the ticker for which you want to see the graph: ")
	print()
	print("(1) MSFT")
	print("(2) HUBS")
	print("(3) CRM")
	print("(4) WORK")
	print("(5) GOOGL")
	print()
	print("Choice: ", end="")
	choice = input()
	plot_ticker = dat[int(choice) - 1]["ticker"]

	newtime = yf.download(plot_ticker, start = "2019-06-06", end = "2020-05-06")
	newtime1 = yf.download(plot_ticker, start = "2020-05-06", end = "2020-06-06")

	datee = datetime.datetime.fromtimestamp(
	        	int(dat[int(choice) - 1]["purchasedAt"])//1000.0
	    	).strftime('%Y-%m-%d %H:%M:%S')

	newtime['Close'].plot()
	newtime1['Adj Close'].plot()
	plt.xlabel("Date")
	plt.ylabel("Close")
	plt.title("Price data for "+dat[int(choice) - 1]["ticker"])
	plt.ylim(ymin=0)
	plt.vlines(x=datee[:7], ymin=0, ymax=2000, linestyles='dashed', label='Buy date')
	plt.hlines(y=average[int(choice) - 1], xmin="2019-06-06", xmax="2020-06-06", colors='red', linestyles='dotted', label='One month average')
	plt.legend()
	plt.show()

	print("\n")
	print("Do you want to see the graph for any other stock? Type 'y' or 'Y' if YES, or any other key if NO")
	answer = input()












