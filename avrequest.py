import requests
import pandas as pd
apikey = "0T4JN32CNRLAY45K"
url = "https://www.alphavantage.co/query?function="

df = pd.read_csv("./data/currencies.csv")
df = df.set_index("currency code")

def search(ticker):
	search = requests.get(url + "SYMBOL_SEARCH&keywords="+ticker+"&apikey="+apikey).json()
	return search["bestMatches"][0]

def get_quote(ticker):
	best_match = search(ticker)
	quote = requests.get(url + "GLOBAL_QUOTE&symbol="+best_match["1. symbol"]+"&apikey="+apikey).json()
	mid_price = (float(quote["Global Quote"]["03. high"]) +
				float(quote["Global Quote"]["04. low"])) / 2
	result = best_match["1. symbol"] + " (" + best_match["2. name"] + ") is at $" + str(mid_price)
	return result

def get_exchange_rate(currency_1, currency_2):
	if (currency_1 in df.index and currency_2 in df.index):
		exchange_rate = requests.get(url + "CURRENCY_EXCHANGE_RATE&from_currency="+currency_1+"&to_currency="+currency_2+"&apikey="+apikey).json()["Realtime Currency Exchange Rate"]
		result = currency_1 + " -> " + currency_2 + ": " + exchange_rate["5. Exchange Rate"]
		return result
	else:
		invalid_currency = currency_2
		if currency_1 not in df.index:
			invalid_currency = currency_1
		return "Error: " + invalid_currency + " not in approved indexes"

def get_WMA(ticker):
	best_match = search(ticker)
	wma = requests.get(url + "WMA&symbol=" + best_match["1. symbol"] + "&interval=weekly&time_period=10&series_type=open&apikey=" + apikey).json()
	for time_stamp in wma["Technical Analysis: WMA"]:
		time_WMA = time_stamp
		wma_value = wma["Technical Analysis: WMA"][time_WMA]['WMA']
		break
	result = best_match["1. symbol"] + " (" + best_match["2. name"] + ") Weekly Moving Average is $" + wma_value + " for the week of " + time_WMA
	return result

def router(text):
	if text[0] == "getQuote":
		return get_quote(text[1].split("=")[1])
	elif text[0] == "getExchangeRate":
		return get_exchange_rate(text[1].split("=")[1], text[2].split("=")[1])
	elif text[0] == "getWMA":
		return get_WMA(text[1].split("=")[1])
	else:
		return False

if __name__ == "__main__":
	print(router("getWMA -ticker=IBM"))
