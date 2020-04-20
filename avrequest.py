import requests
import pandas as pd
apikey = "0T4JN32CNRLAY45K"
url = "https://www.alphavantage.co/query?function="

dfCurrency = pd.read_csv("./data/currencies.csv")
dfCurrency = dfCurrency.set_index("currency code")
dfCrypto = pd.read_csv("./data/cryptocurrencies.csv")
dfCrypto = dfCrypto.set_index("currency code")

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

def get_exchange_rate(currency1, currency2):
	if (currency1 in dfCurrency.index and currency2 in dfCurrency.index):
		exchangeRate = requests.get(url + "CURRENCY_EXCHANGE_RATE&from_currency="+currency1+"&to_currency="+currency2+"&apikey="+apikey).json()["Realtime Currency Exchange Rate"]
		result = currency1 + " -> " + currency2 + ": " + exchangeRate["5. Exchange Rate"]
		return result
	else:
		invalid_currency = currency2
		if currency1 not in dfCurrency.index:
			invalid_currency = currency1
		return "Error: " + invalid_currency + " not in approved indexes"

def get_WMA(ticker):
	best_match = search(ticker)
	wma = requests.get(url + "WMA&symbol=" + best_match["1. symbol"] + "&interval=weekly&time_period=10&series_type=open&apikey=" + apikey).json()
	for time_stamp in wma["Technical Analysis: WMA"]:
		time_wma = time_stamp
		wma_value = wma["Technical Analysis: WMA"][time_wma]['WMA']
		break
	result = best_match["1. symbol"] + " (" + best_match["2. name"] + ") Weighted Weekly Moving Average is $" + wma_value + " for the week of " + time_wma
	return result

def get_BBANDS(ticker):
	bestMatch = search(ticker)
	bbands = requests.get(url + "BBANDS&symbol=" + bestMatch["1. symbol"] + "&interval=weekly&time_period=10&series_type=open&apikey=" + apikey).json()
	for timeStamp in bbands["Technical Analysis: BBANDS"]:
		timeBBANDS = timeStamp
		bbandsTime = bbands["Technical Analysis: BBANDS"][timeBBANDS]
		break
	result = bestMatch["1. symbol"] + " (" + bestMatch["2. name"] + ") Bollinger bands (BBANDS) values are: \n   Real Upper Band: " + bbandsTime["Real Upper Band"] + "\n   Real Middle Band: " + bbandsTime["Real Middle Band"] + "\n   Real Lower Band: " + bbandsTime["Real Lower Band"] + "\nfor the week of " + timeBBANDS
	return result

def get_CCI(ticker):
	bestMatch = search(ticker)
	cci = requests.get(url + "CCI&symbol=" + bestMatch["1. symbol"] + "&interval=weekly&time_period=10&series_type=open&apikey=" + apikey).json()
	for timeStamp in cci["Technical Analysis: CCI"]:
		timeCCI = timeStamp
		cciValue = cci["Technical Analysis: CCI"][timeCCI]["CCI"]
		break
	result = bestMatch["1. symbol"] + " (" + bestMatch["2. name"] + ") Commodity Channel Index is " + cciValue + " for the week of " + timeCCI
	return result

def get_rating(cryptocurrency):
	if cryptocurrency in dfCrypto.index:
		rating = requests.get(url + "CRYPTO_RATING&symbol="+cryptocurrency+"&apikey="+apikey).json()["Crypto Rating (FCAS)"]
		return rating["1. symbol"] + " (" + rating["2. name"] + ") has the following cryptocurrencies ratings: " + "\n   FCAS: " + rating["4. fcas score"] + " (" + rating["3. fcas rating"] + ")\n   Developer Score: " + rating["5. developer score"] + "\n   Market Maturity Score: " + rating["6. market maturity score"] + "\n   Utility Score: " + rating["7. utility score"]
	else:
		return "Error: " + cryptocurrency + " not in approved symbols"

def get_EMA(ticker):
	best_match = search(ticker)
	ema = requests.get(url + "EMA&symbol=" + best_match["1. symbol"] + "&interval=weekly&time_period=10&series_type=open&apikey=" + apikey).json()
	for time_stamp in ema["Technical Analysis: EMA"]:
		time_ema = time_stamp
		ema_value = ema["Technical Analysis: EMA"][time_ema]['EMA']
		break
	result = best_match["1. symbol"] + " (" + best_match["2. name"] + ") Exponential Weekly Moving Average is $" + ema_value + " for the week of " + time_ema
	return result
	
def get_OBV(ticker):
	best_match = search(ticker)
	obv = requests.get(url + "OBV&symbol=" + best_match["1. symbol"] + "&interval=weekly&apikey=" + apikey).json()["Technical Analysis: OBV"]
	result = ""
	i = 0
	for key in obv:
		result = result + key + ": " + obv[key]["OBV"] + "\n"
		i += 1
		if i >= 5: 
			break
	
	return result
	
def get_RSI(ticker, series):
	valid_series = ["closed", "open", "high", "low"]
	
	if series not in valid_series:
		return "Invalid series type " + series
	
	best_match = search(ticker)
	rsi = requests.get(url + "RSI&symbol=" + best_match["1. symbol"] + "&interval=weekly&time_period=60&series_type=" + series + "&apikey=" + apikey).json()
	result = ""
	i = 0
	for key in rsi["Technical Analysis: RSI"]:
		result = result + key + ": " + rsi["Technical Analysis: RSI"][key]["RSI"] + "\n"
		i += 1
		if i >= 5: 
			break
	
	return result
	
def get_STOCH(ticker):
	best_match = search(ticker)
	stoch = requests.get(url + "STOCH&symbol=" + best_match["1. symbol"] + "&interval=weekly&apikey=" + apikey).json()["Technical Analysis: STOCH"]
	result = ""
	i = 0
	for key in stoch:
		result = result + key + ":\n   SlowD: " + stoch[key]["SlowD"] + "\n   SlowK: " + stoch[key]["SlowK"] + "\n"
		i += 1
		if i >= 5: 
			break
	
	return result

def get_MACD(ticker):
	best_match = search(ticker)
	macd = requests.get(url + "MACD&symbol=" + best_match["1. symbol"] + "&interval=weekly&time_period=10&series_type=open&apikey=" + apikey).json()
	for time_stamp in macd["Technical Analysis: MACD"]:
		time_macd = time_stamp
		macd_value = macd["Technical Analysis: MACD"][time_macd]['MACD']
		break
	result = best_match["1. symbol"] + " (" + best_match["2. name"] + ") Weekly Moving Average Convergence/Divergence Value is $" + macd_value + " for the week of " + time_macd
	return result

def router(string):
	words = string.split(" ")

	if words[1] == "getQuote":
		return get_quote(words[2])
	elif words[1] == "getExchangeRate":
		return get_exchange_rate(words[2], words[3])
	elif words[1] == "getWMA":
		return get_WMA(words[2])
	elif words[1] == "search":
		return search(words[2])
	elif words[1] == "getBBANDS":
		return get_BBANDS(words[2])
	elif words[1] == "getCCI":
		return get_CCI(words[2])
	elif words[1] == "getRating":
		return get_rating(words[2])
	elif words[1] == "getEMA":
		return get_EMA(words[2])
  elif words[0] == "getOBV":
		return get_OBV(words[1].split("=")[1])
	elif words[0] == "getRSI":
		return get_RSI(words[1].split("=")[1], words[2].split("=")[1])
	elif words[0] == "getSTOCH":
		return get_STOCH(words[1].split("=")[1])
	elif words[1] == "getMACD":
		return get_MACD(words[2])
	else:
		return False

if __name__ == "__main__":
	print(router("getRating -symbol=BTC"))
