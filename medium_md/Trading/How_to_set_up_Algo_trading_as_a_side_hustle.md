---
title: "How to set up Algo trading as a side hustle"
url: https://medium.com/p/b32372c79727
---

# How to set up Algo trading as a side hustle

[Original](https://medium.com/p/b32372c79727)

Member-only story

# How to set up Algo trading as a side hustle

[![Jerry He](https://miro.medium.com/v2/resize:fill:64:64/1*bIWSJtXHvYZ428NkTkOA7A.jpeg)](/@jerryhe.trader?source=post_page---byline--b32372c79727---------------------------------------)

[Jerry He](/@jerryhe.trader?source=post_page---byline--b32372c79727---------------------------------------)

9 min read

·

Sep 13, 2021

--

7

Listen

Share

More

## Week 1

![]()

For many decades, professional traders have had absolute advantage over the regular folks, but in 2020, the reddit phenomenon has shown that, in many cases, the regular folks can win and make a fortune doing so, as a portion of Gabe Plotkin’s $4.5 billion loss surely went to some real reddit traders.

As a former professional high frequency trader (XR), I often think about how as an individual trader can day trade the market using open source software and no-fee retail brokerages. In fact, I would go so far as to claim there is NEVER better availability of open source software tools to do just that. 2021 may just be the year for work-from-home Algo traders.

There are a lot of stock trading websites that offer advice on what to buy, but I can find very few that outlines clearly documented approach that can actually day trade profitably; hence my motivation to take up the pen and put this information out there. You might be able to find a couple of data science blogs that claims to teach Algo trading, but their data source is usually woefully inadequate (e.g. daily or hourly stock info from yahoo) and not based on equity futures data at the sub-1-second scale which is the preferred timescale of my own Algo trading strategies. They don’t seem to be aware that live streaming level II market book for equities and level I for futures is now available to non-professional traders for free.

Just to clarify, by non-professional, I do not mean novice or inexperienced. The nonprofessional status is purely a legal designation where we’re not FINRA-registered or working at a financial firm. One major advantage to a nonprofessional algorithmic trader is zero-fee trading!! Here is an example trading pipeline written in python

· Futures LEVEL I market data from TDAmeritrade

· Major sector ETF SPDR level II market data streaming from TDAmeritrade

· Options straddle strategy on Robinhood

This medium article is not just for people who are looking for gold in hobbyist Algo trading space but also those who want to do it out of intellectual curiosity and want to contribute to the community.

**Motivation**

Since 2020, social media has seen an explosion of financial advice for the young investor. From buying bitcoin, Nvidia, meme stocks, to buying deep value covid victim stocks like airlines, cruises, or mall-based retail. For me, I have never had the stomach for HODL’ing anything except Nvidia; I’d much prefer a less volatile income stream ranging from 0 to $500 daily, and using statistics along the way is just icing on the cake.

Of course, algo trading has its own significant risks too. Few people will remember Knights Capital Group, which lost $440 million in 45 minutes. Hence, if you are just starting to get into algo trading, it is very important to start with a limited brokerage like Robinhood, so you can’t accidentally fire off level III options trades, or short stocks, both of which are not allowed on Robinhood anyways. The no-fee aspect of Robinhood also helps if your algo accidentally fires off thousands of trades before you can stop it. Furthermore, it is very important to have an object-oriented approach to applying hard risk limits to your trading. My old mentor at XR used to say that losing money while developing your trade is paying “tuition”, but for younger folks like us it is important to keep that tuition small to minuscule.

The goal of my approach make a few hundred dollars a day as passive income using python, TDAmeritrade/Robinhood, and avoid any trading fees when possible. Robinhood offers no fee options trading, however, TDAmeritrade offers level II market data as well as Level I futures market data through a streaming API. My code will be using the market data from TDAmeritrade but the options trade will be executed on the Robinhood platform. I’m not just taking advantage of TDAmeritrade because I use multiple strategies and many strategies can only be executed on TDAmeritrade (e.g. shorting stocks); thereby incurring some trading fees and ease my conscience. The important takeaway here is that professional traders pay lots of $$$ for faster access to the same data, we as nonprofessional traders are getting it for free, and that can be a competitive advantage by itself.

**The strategy**

The options straddle strategies are appropriately low-risk strategies for a new algo trader looking to make $$$ carefully. It is also a very appropriate strategy IMHO for the trading week starting Sep 13 as the S&P 500 had a rare down week and next week’s market direction can go either way depending on who you ask. BofA, Morgan Stanley and now Goldman are downright negative on the U.S. stock market whereas Tom Lee, Brian Belski, and others are still very bullish. I say let the true believers of the “everything rally” battle it out with the big money managers who thinks stagflation are coming. Our strategy will be more likely to be profitable if the two sides are evenly matched with no clear winner.

I will illustrate two simple, and relatively low risk strategy trading SPY and XLU respectively. Equities trading starts at 9:30am, and the first 20 minutes are heavily influenced by passive inflow/outflow (e.g. ETFs and mutual funds). Hence there is plenty of room to do some sub-1-second momentum trading. The gist of trading idea is

If the momentum of the stock at 9:30am is upwards -> buy 2 calls *eagerly*, buy 1 put *patiently*

If the momentum of the stock at 9:30am is downwards -> buy 1 call *patiently*, buy 2 puts *eagerly*

The momentum approach can be wrong sometimes; for example, on Friday Sep 10th, the clearly positive momentum in SPY in the first minute of trading reversed decisively 9:31am, but over many trading days that tend to be the exception rather than the rule. The scenario of Friday the Sep 10th can salvaged; however, if we code our algorithm to take profits eagerly or partially hedge when momentum turns. Alas this is one of many cases where our home setup will not be fast enough to compete with professional algo traders, but it can still cut losses faster than liquidating manually on the Robinhood app.

With that in mind, let’s complete the strategy, WLOG

1. If the momentum of the stock at 9:30am is upwards -> buy 2 calls *eagerly*, buy 1 put *patiently*

2. At 10:30am, if all 3 options are filled, then take profit on 1 of the options *patiently* (if there is any profit)

3. For the rest of the day, manually trade out of the remaining positions or convert to spreads as you watch the market

With any luck, you can be done with trading by 11am and go back to your day job.

For clarification*, eagerly* does not mean sending a market order, since the bid-ask spread can be very wide. For a variety of reasons, I will only be advising sending limit orders in all my algo trading medium articles.

I will define *patiently* as waiting until 9:50am or later, and then sending an order at the lowest traded price of the option of the trading day so far. If your momentum indicator is wrong, the worst-case scenario would be losing $$ equal to the sum of the premium of the 2 options. In some scenario, maybe no orders get filled, in which case our PnL is 0.

Without loss of generality (WLOG), let’s play out the scenario where the momentum indicator is saying the stock is on the way up. For SPY, we set the strike price of the call option equal to the overnight futures high; for XLU, we set the strike price of the call option equal to the previous trading day session high. A better way would be to incorporate the VIX futures trajectory into setting the strike price but I won’t go there for this article.

We will be using *redis* as the means of communication between the python process **T** that streams market data from TDAmeritrade, and the python process **R** that trades on Robinhood. In particular, python process **T** should be keeping track of lowest option trade price for the patient leg of the straddle for all possible strike prices that process **R** would want to trade at 9:50am.

**Installation**

First install latest miniconda python3.9 for your OS, and then execute the following package installations

```
pip install aioredis  
pip install robin_stocks  
pip install selenium  
pip install tda-api  
pip install apscheduler
```

**TDAmeritrade.py**

You will need to register a developer account with TDAmeritrade first via <https://developer.tdameritrade.com> . After you register you will need to create an app (I suggest using <http://localhost:8080> as callback URL) and then find the API key(i.e. token). You will need to download the appropriate chromedriver for your version of Google Chrome from [here](https://www.barrons.com/articles/microsoft-stock-earnings-cloud-51634745606) and then change the code here on line to your Download directory. The first run of this script will prompt you to login using your TDAmeritrade password on a selenium-controlled Google chrome; it will create *token.pickle* in your working directory. Once you have that file, you will not need selenium anymore (should probably uninstall it and remove it from the script).

You will need to download and install redis and run redis. If you’re on Windows 10, I recommend using [Memurai](https://www.memurai.com/get-memurai), which I tested and seem to be compatible with aioredis.

I should also note that for serious algo traders you should be using memory mapped file as means of communication between **TDAmeritrade.py**and **Robinhood.py**, but that is beyond the scope of this article since that’s not cross platform (e.g. doesn’t work well for Windows) and involves using C++ for some of the more CPU-intensive computations.

You can read the full pseudocode [on github](https://github.com/xiangjerryhe/algo_trading/blob/main/week1/TDAmeritrade.py) , the main part of this python process is in the read\_stream function, where you can see we subscribe to level 2 book data on not only the ETF we trade (SPY, XLU), but also related stocks/ETFs. For example, XLU is highly correlated with XLRE, so a direction change in XLRE could predict a direction change in XLU (as it did on Sep 10th). We also subscribe to the treasury futures as that can be a predictor for direction of XLU on the open.

**Robinhood.py**

For the Robinhood python process, we will use the *run\_at* function to time the different stages of our strategy. At the open, we execute one leg of our straddle starting at 9:30am and 5 seconds. I realize that it is not correct to call it a straddle if there are 2 options on one leg, but since we’re expected to take off an option after 10:30am, hopefully ending up with a straddle, I will keep using this term. Another advantage of using asyncio is to receive messages of momentum change from redis and act immediately to clear out positions without blocking.

Most of the computationally intensive functions are being done in the other python process and important momentum and option price info are being written into Redis. This process is the one that performs the trading accordingly to current holdings and values of certain keys on Redis. You can read the full pseudocode [on github](https://github.com/xiangjerryhe/algo_trading/blob/main/week1/TDAmeritrade.py).

**Conclusion**

I will be trading this very strategy starting Sep 13 (even with the redis set up) and reporting its performance on my personal website. I understand some of you might be disappointed that I didn’t post all the code; legally speaking, I cannot give financial advice. I’m aware lots of people on the web flaunt SEC/FINRA rules but I’d like to stick to providing guidance on the software data infrastructure part of work-from-home algo trading. With that in mind, I’d also like to state that past performance is not a reliable indicator of future performance and any market outlook or trading strategies expressed in this article regarding XLU and SPY are provided solely to complement the python code and data infrastructure. Once I am familiar with all the legal nuances of financial blogging (maybe some of you can comment on it and education me on this), I will consider posting all the code on my personal website or in an e-book. I hope this article will help people get into developing algo strategies for their personal finance.

**Spoiler Alert**

Next week, for the follow up article, I can write about any number of things, let me know in the comments section what you’d like to see, here are some thoughts

· Discussion of training a model for outputting the aforementioned momentum indicators

· Implement back testing of Algo strategies on historical data

· A partial lock-in-profit add-on variation for SPY straddle trading using SPXL and SPXS

· SMH & EWY pair trading strategy with a twist

· Memory mapped file implementation (to replace redis)

· How to set this up on Google Cloud or AWS (for those with slow home internet connection)