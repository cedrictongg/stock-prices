# Stock Buddy (Live)

You can add it onto your list of skills [here](https://smile.amazon.com/gp/product/B07DBW2J28?ie=UTF8&ref-suffix=ss_rw)!

## What it does

Stock Buddy is an Amazon Alexa Skill that allows users to fetch the latest stock information about a publicly traded company.

## How to use it

The invocation name is `stock buddy`. So with that, you can use the default `Alexa, open stock buddy`. From there, you can use the provided sample utterances: "stocks for Amazon" or "give me the stock information for Google". Stock Buddy will give the latest information regarding the companies.

If the stock market is closed or it is the weekend, the latest information will be returned automatically.
## How it works

In combination with the [Alpha Vantage API](https://www.alphavantage.co/support/#api-key) and [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), I was able to grab the stock ticker and use the API to retrieve the stock information. With that, I took the info and used [AWS Lambda](https://aws.amazon.com/lambda/) to host my code and use it as a server for the skill to retrieve information from. After getting the info, I was then able to format the information that let user's hear their request in an easily digestible fashion.

## Future Plans

 - Add a portfolio feature
 - Give the stock information to the entire portfolio
 - Support for Cryptocurrency
 - Exchange rates for different currencies
 - Return information for specific dates
