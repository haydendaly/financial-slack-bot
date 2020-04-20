import requests
import pandas as pd
apikey = "0T4JN32CNRLAY45K"
url = "https://www.alphavantage.co/query?function="

df = pd.read_csv("./data/currencies.csv")
df = df.set_index("currency code")

def search(ticker):
	search = requests.get(url + "SYMBOL_SEARCH&keywords="+ticker+"&apikey="+apikey).json()
	return search["bestMatches"][0]

def getQuote(ticker):
	bestMatch = search(ticker)
	quote = requests.get(url + "GLOBAL_QUOTE&symbol="+bestMatch["1. symbol"]+"&apikey="+apikey).json()
	midPrice = (float(quote["Global Quote"]["03. high"]) +
				float(quote["Global Quote"]["04. low"])) / 2
	result = bestMatch["1. symbol"] + " (" + bestMatch["2. name"] + ") is at $" + str(midPrice)
	return result

def getExchangeRate(currency1, currency2):
	if (currency1 in df.index and currency2 in df.index):
		exchangeRate = requests.get(url + "CURRENCY_EXCHANGE_RATE&from_currency="+currency1+"&to_currency="+currency2+"&apikey="+apikey).json()["Realtime Currency Exchange Rate"]
		result = currency1 + " -> " + currency2 + ": " + exchangeRate["5. Exchange Rate"]
		return result
	else:
		err = currency2
		if currency1 not in df.index:
			err = currency1
		return "Error: " + err + " not in approved indexes"

def getWMA(ticker):
	bestMatch = search(ticker)
	wma = requests.get(url + "WMA&symbol=" + bestMatch["1. symbol"] + "&interval=weekly&time_period=10&series_type=open&apikey=" + apikey).json()
	for timeStamp in wma["Technical Analysis: WMA"]:
		timeWMA = timeStamp
		wmaValue = wma["Technical Analysis: WMA"][timeWMA]['WMA']
		break
	result = bestMatch["1. symbol"] + " (" + bestMatch["2. name"] + ") Weekly Moving Average is $" + wmaValue + " for the week of " + timeWMA
	return result
	
def getOBV(ticker):
	bestMatch = search(ticker)
	obv = requests.get(url + "OBV&symbol=" + bestMatch["1. symbol"] + "&interval=weekly&apikey=" + apikey).json()["Technical Analysis: OBV"]
	result = ""
	i = 0
	for key in obv:
		result = result + key + ": " + obv[key]["OBV"] + "\n"
		i += 1
		if i >= 5: 
			break
	
	return result
	
def getRSI(ticker, series):
	valid_series = ["closed", "open", "high", "low"]
	
	if series not in valid_series:
		return "Invalid series type " + series
	
	bestMatch = search(ticker)
	rsi = requests.get(url + "RSI&symbol=" + bestMatch["1. symbol"] + "&interval=weekly&time_period=60&series_type=" + series + "&apikey=" + apikey).json()
	print(rsi)
	result = ""
	i = 0
	for key in rsi["Technical Analysis: RSI"]:
		result = result + key + ": " + rsi["Technical Analysis: RSI"][key]["RSI"] + "\n"
		i += 1
		if i >= 5: 
			break
	
	return result
	
def getSTOCH(ticker):
	bestMatch = search(ticker)
	stoch = requests.get(url + "STOCH&symbol=" + bestMatch["1. symbol"] + "&interval=weekly&apikey=" + apikey).json()["Technical Analysis: STOCH"]
	result = ""
	i = 0
	for key in stoch:
		result = result + key + ":\n   SlowD: " + stoch[key]["SlowD"] + "\n   SlowK: " + stoch[key]["SlowK"] + "\n"
		i += 1
		if i >= 5: 
			break
	
	return result

def router(string):
	words = string.split(" ")
	if words[0] == "getQuote":
		return getQuote(words[1].split("=")[1])
	elif words[0] == "getExchangeRate":
		return getExchangeRate(words[1].split("=")[1], words[2].split("=")[1])
	elif words[0] == "getWMA":
		return getWMA(words[1].split("=")[1])
	elif words[0] == "getOBV":
		return getOBV(words[1].split("=")[1])
	elif words[0] == "getRSI":
		return getRSI(words[1].split("=")[1], words[2].split("=")[1])
	elif words[0] == "getSTOCH":
		return getSTOCH(words[1].split("=")[1])
	else:
		return False

if __name__ == "__main__":
	print(router("getRSI -ticker=IBM -series=closed"))
