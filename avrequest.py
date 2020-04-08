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
	
if __name__ == "__main__":
	print(getQuote("AAPL"))