import requests
apikey = "0T4JN32CNRLAY45K"

def getQuote(ticker):
	search = requests.get("https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords="+ticker+"&apikey="+apikey).json()
	
	bestMatch = search["bestMatches"][0]
	
	quote = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol="+bestMatch["1. symbol"]+"&apikey="+apikey).json()
	
	midPrice = (float(quote["Global Quote"]["03. high"]) +
				float(quote["Global Quote"]["04. low"])) / 2 
	
	result = bestMatch["1. symbol"] + " (" + bestMatch["2. name"] + ") is at $" + str(midPrice)
	return result
	
def getExchangeRate(currency1, currency2):
	exchangeRate = requests.get("https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency="+currency1+"&to_currency="+currency2+"&apikey="+apikey).json()["Realtime Currency Exchange Rate"]
	
	#print(exchangeRate)
	
	result = currency1 + " -> " + currency2 + ": " + exchangeRate["5. Exchange Rate"]
	return result
	
if __name__ == "__main__":
	print(getExchangeRate("USD", "JPY"))