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

def getQuote(ticker):
	bestMatch = search(ticker)
	quote = requests.get(url + "GLOBAL_QUOTE&symbol="+bestMatch["1. symbol"]+"&apikey="+apikey).json()
	midPrice = (float(quote["Global Quote"]["03. high"]) +
				float(quote["Global Quote"]["04. low"])) / 2
	result = bestMatch["1. symbol"] + " (" + bestMatch["2. name"] + ") is at $" + str(midPrice)
	return result

def getExchangeRate(currency1, currency2):
	if (currency1 in dfCurrency.index and currency2 in dfCurrency.index):
		exchangeRate = requests.get(url + "CURRENCY_EXCHANGE_RATE&from_currency="+currency1+"&to_currency="+currency2+"&apikey="+apikey).json()["Realtime Currency Exchange Rate"]
		result = currency1 + " -> " + currency2 + ": " + exchangeRate["5. Exchange Rate"]
		return result
	else:
		err = currency2
		if currency1 not in dfCurrency.index:
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

def getBBANDS(ticker):
	bestMatch = search(ticker)
	bbands = requests.get(url + "BBANDS&symbol=" + bestMatch["1. symbol"] + "&interval=weekly&time_period=10&series_type=open&apikey=" + apikey).json()
	for timeStamp in bbands["Technical Analysis: BBANDS"]:
		timeBBANDS = timeStamp
		bbandsTime = bbands["Technical Analysis: BBANDS"][timeBBANDS]
		break
	result = bestMatch["1. symbol"] + " (" + bestMatch["2. name"] + ") Bollinger bands (BBANDS) values are: \n   Real Upper Band: " + bbandsTime["Real Upper Band"] + "\n   Real Middle Band: " + bbandsTime["Real Middle Band"] + "\n   Real Lower Band: " + bbandsTime["Real Lower Band"] + "\nfor the week of " + timeBBANDS
	return result

def getCCI(ticker):
	bestMatch = search(ticker)
	cci = requests.get(url + "CCI&symbol=" + bestMatch["1. symbol"] + "&interval=weekly&time_period=10&series_type=open&apikey=" + apikey).json()
	for timeStamp in cci["Technical Analysis: CCI"]:
		timeCCI = timeStamp
		cciValue = cci["Technical Analysis: CCI"][timeCCI]["CCI"]
		break
	result = bestMatch["1. symbol"] + " (" + bestMatch["2. name"] + ") Commodity Channel Index is " + cciValue + " for the week of " + timeCCI
	return result

def getRating(cryptocurrency):
	if cryptocurrency in dfCrypto.index:
		rating = requests.get(url + "CRYPTO_RATING&symbol="+cryptocurrency+"&apikey="+apikey).json()["Crypto Rating (FCAS)"]
		return rating["1. symbol"] + " (" + rating["2. name"] + ") has the following cryptocurrencies ratings: " + "\n   FCAS: " + rating["4. fcas score"] + " (" + rating["3. fcas rating"] + ")\n   Developer Score: " + rating["5. developer score"] + "\n   Market Maturity Score: " + rating["6. market maturity score"] + "\n   Utility Score: " + rating["7. utility score"]
	else:
		return "Error: " + cryptocurrency + " not in approved symbols"



def router(string):
	words = string.split(" ")
	if words[0] == "getQuote":
		return getQuote(words[1].split("=")[1])
	elif words[0] == "getExchangeRate":
		return getExchangeRate(words[1].split("=")[1], words[2].split("=")[1])
	elif words[0] == "getWMA":
		return getWMA(words[1].split("=")[1])
	elif words[0] == "search":
		return search(words[1].split("=")[1])
	elif words[0] == "getBBANDS":
		return getBBANDS(words[1].split("=")[1])
	elif words[0] == "getCCI":
		return getCCI(words[1].split("=")[1])
	elif words[0] == "getRating":
		return getRating(words[1].split("=")[1])
	else:
		return False

if __name__ == "__main__":
	print(router("getRating -symbol=BTC"))
