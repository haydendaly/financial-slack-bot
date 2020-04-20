# Process Overview
# Iteration Summaries:
## First Iteration:
For the first iteration, our focus was around getting the foundations down of the bot in order to further expand upon it during the second iteration. Our tasks were distributed as such:
### Hayden:
As a trader, I want to be able to get the weighted moving average of a ticker (3)
As a developer, I want to be able to take a string input from Slack and break it down into commands (5)
### Scott:
As a trader, I want to be able to see the exchange rate between two currencies (3)
As a trader, I want to be able to get the quote of a ticker (3)
### Bruno:
As the backend developer, I want to have a Flask app to expose endpoints for the Slack API (8)
As a trader, I want to be able to speak to a Slackbot (8)
### Reflection:
We finished our work for this iteration timely and were happy with the outcome of it. We learned that we did not need to use Flask in order to structure the bot and just used the Slack built in Python library. We had three meetings over the sprint: one at the beginning to determine tasks, one to reflect upon tasks during progress to see where we could mutually aid one another, and one at the end to review progress and test the bot.
## Second Iteration:
For the second iteration, our focus was building on the foundations of the bot structured in the first iteration. This is where we added most of the features structured around the AlphaVantage API. Much to our surprise, a lot of the mathematical models we wanted to implement, they already had support for in their API. We started our second iteration by meeting over Zoom and determining tasks for the iteration. We decided to put the tasks in our group chat and then migrated them to GitHub when we actually did the work. We worked throughout the sprint and had one meeting for pair programming in the middle in which we shared screens. We had a meeting on the last day of the sprint to commit and merge all of the work accordingly so there wouldn’t be any conflicts. Our tasks were distributed as such:
### Hayden:
As a trader, I want to be able to search for ticker symbols (3)
As a trader, I want to be able to get the fundamental crypto asset score to a crypto project (5)
As a trader, I want to be able to get the commodity channel index (CCI) values of a symbol (3)
As a trader, I want to be able to get the Bollinger bands (BBANDS) values of a symbol (3)
### Scott: 
As a trader, I want to be able to get the stochastic oscillator (STOCH) values of a symbol (5)
As a trader, I want to be able to get the relative strength index (RSI) of a symbol (3)
As a trader, I want to be able to get the on balance volume (OBV) values of a symbol (3)
### Bruno:
As a developer, I want to be able to use a readme file in order to deploy the slack bot for development (3)
As a user on Slack, I want to be able to see all available commands (8)
As a trader, I want to be able to get the exponential moving average (EMA) of a symbol (3)
As a trader, I want to be able to get the moving average convergence / divergence (MACD) of a symbol (3)
### Reflection:
We think waiting till the last minute to commit and merge all of our changes seemed stressful. We were all used to working on projects alone so did a lot of our changes locally and didn’t really utilize the Kanban board in the manner it was supposed to be used. Reflecting upon the project, we think our major areas for improvement would be to distribute our commits over the sprint rather than waiting till the end to commit and merge all the work. Lastly, upon building this project, the team realizes the potential of a bot like this and wants to implement it within the Slack Bot “Marketplace”. The group plans on having a third, informal iteration where they flesh it out a bit for deployment. Plans surround using a robust amount API keys (so the limit surpasses 500) and deploying the Slack bot on a Heroku instance as originally intended for global use.
## Demo:
<INSERT URL>
