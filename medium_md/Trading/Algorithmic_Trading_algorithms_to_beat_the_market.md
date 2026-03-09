---
title: "Algorithmic Trading: algorithms to beat the market"
url: https://medium.com/p/200c61ad84fc
---

# Algorithmic Trading: algorithms to beat the market

[Original](https://medium.com/p/200c61ad84fc)

# Algorithmic Trading: algorithms to beat the market

[![An Rodriguez](https://miro.medium.com/v2/resize:fill:64:64/1*E6SYD2xn2_Jx10uq-TCedA.jpeg)](/@anrodz?source=post_page---byline--200c61ad84fc---------------------------------------)

[An Rodriguez](/@anrodz?source=post_page---byline--200c61ad84fc---------------------------------------)

6 min read

·

Feb 4, 2020

--

Listen

Share

More

During 2019, the stock market grew. A lot.

Take for example an [ETF](https://www.investopedia.com/terms/e/etf.asp) I like: FTEC (Fidelity MSCI Information Technology Index):

During 2019, FTEC’s price grew from $49.35 to $72.48: a staggering almost 50% growth!

That’s almost double the growth of the standard-bearer S&P500 that grew “only” around 30%.

Stocks like APPL (Apple Inc.) grew even more, over 90%!

Put neatly:

```
S&P 500: 30%  
FTEC: 50%  
V: 41%  
AAPL: 90%
```

Press enter or click to view image in full size

![]()

It’s easy to check it out using [finance.yahoo.com](https://finance.yahoo.com/chart/MA#eyJpbnRlcnZhbCI6ImRheSIsInBlcmlvZGljaXR5IjoxLCJ0aW1lVW5pdCI6bnVsbCwiY2FuZGxlV2lkdGgiOjMuOTcyMzMyMDE1ODEwMjc3LCJ2b2x1bWVVbmRlcmxheSI6dHJ1ZSwiYWRqIjp0cnVlLCJjcm9zc2hhaXIiOnRydWUsImNoYXJ0VHlwZSI6ImxpbmUiLCJleHRlbmRlZCI6ZmFsc2UsIm1hcmtldFNlc3Npb25zIjp7fSwiYWdncmVnYXRpb25UeXBlIjoib2hsYyIsImNoYXJ0U2NhbGUiOiJsaW5lYXIiLCJwYW5lbHMiOnsiY2hhcnQiOnsicGVyY2VudCI6MSwiZGlzcGxheSI6Ik1BIiwiY2hhcnROYW1lIjoiY2hhcnQiLCJ0b3AiOjB9fSwic2V0U3BhbiI6eyJtdWx0aXBsaWVyIjoxLCJiYXNlIjoieWVhciIsInBlcmlvZGljaXR5Ijp7InBlcmlvZCI6MSwiaW50ZXJ2YWwiOiJkYXkifSwibWFpbnRhaW5QZXJpb2RpY2l0eSI6dHJ1ZSwiZm9yY2VMb2FkIjp0cnVlfSwibGluZVdpZHRoIjoyLCJzdHJpcGVkQmFja2dyb3VkIjp0cnVlLCJldmVudHMiOnRydWUsImNvbG9yIjoiIzAwODFmMiIsImV2ZW50TWFwIjp7ImNvcnBvcmF0ZSI6eyJkaXZzIjp0cnVlLCJzcGxpdHMiOnRydWV9LCJzaWdEZXYiOnt9fSwiY3VzdG9tUmFuZ2UiOm51bGwsInN5bWJvbHMiOlt7InN5bWJvbCI6Ik1BIiwic3ltYm9sT2JqZWN0Ijp7InN5bWJvbCI6Ik1BIn0sInBlcmlvZGljaXR5IjoxLCJpbnRlcnZhbCI6ImRheSIsInRpbWVVbml0IjpudWxsLCJzZXRTcGFuIjp7Im11bHRpcGxpZXIiOjEsImJhc2UiOiJ5ZWFyIiwicGVyaW9kaWNpdHkiOnsicGVyaW9kIjoxLCJpbnRlcnZhbCI6ImRheSJ9LCJtYWludGFpblBlcmlvZGljaXR5Ijp0cnVlLCJmb3JjZUxvYWQiOnRydWV9fSx7InN5bWJvbCI6IkFBUEwiLCJzeW1ib2xPYmplY3QiOnsic3ltYm9sIjoiQUFQTCJ9LCJwZXJpb2RpY2l0eSI6MSwiaW50ZXJ2YWwiOiJkYXkiLCJ0aW1lVW5pdCI6bnVsbCwic2V0U3BhbiI6eyJtdWx0aXBsaWVyIjoxLCJiYXNlIjoieWVhciIsInBlcmlvZGljaXR5Ijp7InBlcmlvZCI6MSwiaW50ZXJ2YWwiOiJkYXkifSwibWFpbnRhaW5QZXJpb2RpY2l0eSI6dHJ1ZSwiZm9yY2VMb2FkIjp0cnVlfSwiaWQiOiJBQVBMIiwicGFyYW1ldGVycyI6eyJjb2xvciI6IiNhZDZlZmYiLCJ3aWR0aCI6MiwiaXNDb21wYXJpc29uIjp0cnVlLCJjaGFydE5hbWUiOiJjaGFydCIsInN5bWJvbE9iamVjdCI6eyJzeW1ib2wiOiJBQVBMIn0sInBhbmVsIjoiY2hhcnQiLCJhY3Rpb24iOm51bGwsInNoYXJlWUF4aXMiOnRydWUsInN5bWJvbCI6IkFBUEwiLCJnYXBEaXNwbGF5U3R5bGUiOiJ0cmFuc3BhcmVudCIsIm5hbWUiOiJLNThVTkRNSUFSIiwib3ZlckNoYXJ0Ijp0cnVlLCJ1c2VDaGFydExlZ2VuZCI6dHJ1ZSwiaGVpZ2h0UGVyY2VudGFnZSI6MC43LCJvcGFjaXR5IjoxLCJoaWdobGlnaHRhYmxlIjp0cnVlLCJ0eXBlIjoibGluZSIsInN0eWxlIjoic3R4X2xpbmVfY2hhcnQifX0seyJzeW1ib2wiOiJWIiwic3ltYm9sT2JqZWN0Ijp7InN5bWJvbCI6IlYifSwicGVyaW9kaWNpdHkiOjEsImludGVydmFsIjoiZGF5IiwidGltZVVuaXQiOm51bGwsInNldFNwYW4iOnsibXVsdGlwbGllciI6MSwiYmFzZSI6InllYXIiLCJwZXJpb2RpY2l0eSI6eyJwZXJpb2QiOjEsImludGVydmFsIjoiZGF5In0sIm1haW50YWluUGVyaW9kaWNpdHkiOnRydWUsImZvcmNlTG9hZCI6dHJ1ZX0sImlkIjoiViIsInBhcmFtZXRlcnMiOnsiY29sb3IiOiIjNzJkM2ZmIiwid2lkdGgiOjIsImlzQ29tcGFyaXNvbiI6dHJ1ZSwiY2hhcnROYW1lIjoiY2hhcnQiLCJzeW1ib2xPYmplY3QiOnsic3ltYm9sIjoiViJ9LCJwYW5lbCI6ImNoYXJ0IiwiYWN0aW9uIjoiYWRkLXNlcmllcyIsInNoYXJlWUF4aXMiOnRydWUsInN5bWJvbCI6IlYiLCJnYXBEaXNwbGF5U3R5bGUiOiJ0cmFuc3BhcmVudCIsIm5hbWUiOiJLNThVWU1KMVgxIiwib3ZlckNoYXJ0Ijp0cnVlLCJ1c2VDaGFydExlZ2VuZCI6dHJ1ZSwiaGVpZ2h0UGVyY2VudGFnZSI6MC43LCJvcGFjaXR5IjoxLCJoaWdobGlnaHRhYmxlIjp0cnVlLCJ0eXBlIjoibGluZSIsInN0eWxlIjoic3R4X2xpbmVfY2hhcnQifX0seyJzeW1ib2wiOiJTUFkiLCJzeW1ib2xPYmplY3QiOnsic3ltYm9sIjoiU1BZIn0sInBlcmlvZGljaXR5IjoxLCJpbnRlcnZhbCI6ImRheSIsInRpbWVVbml0IjpudWxsLCJzZXRTcGFuIjp7Im11bHRpcGxpZXIiOjEsImJhc2UiOiJ5ZWFyIiwicGVyaW9kaWNpdHkiOnsicGVyaW9kIjoxLCJpbnRlcnZhbCI6ImRheSJ9LCJtYWludGFpblBlcmlvZGljaXR5Ijp0cnVlLCJmb3JjZUxvYWQiOnRydWV9LCJpZCI6IlNQWSIsInBhcmFtZXRlcnMiOnsiY29sb3IiOiIjZmY4MGM1Iiwid2lkdGgiOjIsImlzQ29tcGFyaXNvbiI6dHJ1ZSwiY2hhcnROYW1lIjoiY2hhcnQiLCJzeW1ib2xPYmplY3QiOnsic3ltYm9sIjoiU1BZIn0sInBhbmVsIjoiY2hhcnQiLCJhY3Rpb24iOiJhZGQtc2VyaWVzIiwic2hhcmVZQXhpcyI6dHJ1ZSwic3ltYm9sIjoiU1BZIiwiZ2FwRGlzcGxheVN0eWxlIjoidHJhbnNwYXJlbnQiLCJuYW1lIjoiSzU4VVlUVTNMQiIsIm92ZXJDaGFydCI6dHJ1ZSwidXNlQ2hhcnRMZWdlbmQiOnRydWUsImhlaWdodFBlcmNlbnRhZ2UiOjAuNywib3BhY2l0eSI6MSwiaGlnaGxpZ2h0YWJsZSI6dHJ1ZSwidHlwZSI6ImxpbmUiLCJzdHlsZSI6InN0eF9saW5lX2NoYXJ0In19LHsic3ltYm9sIjoiRlRFQyIsInN5bWJvbE9iamVjdCI6eyJzeW1ib2wiOiJGVEVDIn0sInBlcmlvZGljaXR5IjoxLCJpbnRlcnZhbCI6ImRheSIsInRpbWVVbml0IjpudWxsLCJzZXRTcGFuIjp7Im11bHRpcGxpZXIiOjEsImJhc2UiOiJ5ZWFyIiwicGVyaW9kaWNpdHkiOnsicGVyaW9kIjoxLCJpbnRlcnZhbCI6ImRheSJ9LCJtYWludGFpblBlcmlvZGljaXR5Ijp0cnVlLCJmb3JjZUxvYWQiOnRydWV9LCJpZCI6IkZURUMiLCJwYXJhbWV0ZXJzIjp7ImNvbG9yIjoiI2ZmYmQ3NCIsIndpZHRoIjoyLCJpc0NvbXBhcmlzb24iOnRydWUsImNoYXJ0TmFtZSI6ImNoYXJ0Iiwic3ltYm9sT2JqZWN0Ijp7InN5bWJvbCI6IkZURUMifSwicGFuZWwiOiJjaGFydCIsImFjdGlvbiI6ImFkZC1zZXJpZXMiLCJzaGFyZVlBeGlzIjp0cnVlLCJzeW1ib2wiOiJGVEVDIiwiZ2FwRGlzcGxheVN0eWxlIjoidHJhbnNwYXJlbnQiLCJuYW1lIjoiSzU4VVoyTTdHSSIsIm92ZXJDaGFydCI6dHJ1ZSwidXNlQ2hhcnRMZWdlbmQiOnRydWUsImhlaWdodFBlcmNlbnRhZ2UiOjAuNywib3BhY2l0eSI6MSwiaGlnaGxpZ2h0YWJsZSI6dHJ1ZSwidHlwZSI6ImxpbmUiLCJzdHlsZSI6InN0eF9saW5lX2NoYXJ0In19XSwic3R1ZGllcyI6eyJ2b2wgdW5kciI6eyJ0eXBlIjoidm9sIHVuZHIiLCJpbnB1dHMiOnsiaWQiOiJ2b2wgdW5kciIsImRpc3BsYXkiOiJ2b2wgdW5kciJ9LCJvdXRwdXRzIjp7IlVwIFZvbHVtZSI6IiMwMGIwNjEiLCJEb3duIFZvbHVtZSI6IiNGRjMzM0EifSwicGFuZWwiOiJjaGFydCIsInBhcmFtZXRlcnMiOnsid2lkdGhGYWN0b3IiOjAuNDUsImNoYXJ0TmFtZSI6ImNoYXJ0In19fX0%3D).

Compare that with 2016, it’s a completely different picture.

```
S&P 500: 12%  
FTEC: 15%  
V: 3.1%  
AAPL: 10%
```

Press enter or click to view image in full size

![]()

It is evident that 2019 was a very good year for the stock market and for the “buy and hold strategy”.

I was thinking about this today and I decided to compare the performance of my algorithm between the years 2019 and 2016.

I couldn’t beat the market with data from 2019, but my algorithm did quite well with data from 2016 (luck? skill?).

Running the same algorithm against data from 2016, my algorithm had an edge of about 10% on average over the market.

When I saw this, I could finally understand why my trading algorithm never beat the market. It’s hard to beat the 2019 performance of the stock market.

People mostly refer to “the market” as the return shown by the S&P 500 index ( [Standard and Poor’s 500 Index](https://www.investopedia.com/terms/s/sp500.asp)).

As most of you know, the S&P 500 is

> *a market-capitalization-weighted index of the 500 largest U.S. publicly traded companies. The index is widely regarded as the best gauge of large-cap U.S. equities.*

Basically, this means that S&P500 is a good indicator of how well the stock market is doing as a whole.

Some say that to make a profit with an automated trading algorithm you would basically need to come up with a way of “predicting the market”.

I would say that this is partially true but at the same time somewhat misleading.

It’s true that in order to make a profit you need to know when to buy and when to sell. But it’s misleading to call this “predicting the market” as if one were [an oracle](https://www.investopedia.com/terms/o/oracleofomaha.asp), or if one pretended to read the future with a magic crystal ball.

For example, some would argue that if the price of a stock increases steadily as a straight line, the only way to make money would be to “buy and hold”.

This is partially true.

If the price of a stock increases steadily as a straight line, there are no moments where the price can be considered low relative to the mean since the price is always increasing.

To reap the maximum profit, the best strategy would be to buy at the beginning and sell at the end (whenever you wish to enter or exit the market) and be “exposed” to the stock the longest possible time.

## Margin trading

However, another useful strategy, in this case, would be to “ buy on margin”:

> *Buying on margin is the act of borrowing money to buy securities. The practice includes buying an asset where the buyer pays only a percentage of the asset’s value and borrows the rest from the bank or broker. The broker acts as a lender and the securities in the investor’s account act as collateral.*

Margin is basically borrowing money from your broker using your securities as collateral.

In this example, using margin could multiply your winnings simply by buying more with money you initially don’t have. HOWEVER, it could also multiply the losses. It can be seen as an amplifier.

If you buy stocks on margin and sell them before the market closes, then you don’t pay any interest on the loan (at least this is true when using [Alpaca](https://alpaca.markets/)). Alpaca is a great algorithmic broken that treats algorithms as first-class citizens.

Alpaca offers annual fees for margin loans as low as 3.75%. However, you only have to pay this interest if you borrow overnight.

For example, if you borrow $5,000 overnight, you end up paying a $0.52 surplus over the loan.

If your stock ends up making 10%, you pay 3.75% for the loan and pocket the rest 6.25%.

As a more meaningful example, if you would have bought $100 of an S&P ETF (like VOO or SPY) you would have made $12. If you use margin to buy 4 times this amount (and kept the loan a whole year), that is, $400, you would have made a profit of:

```
net_profit = profit — margin_interest  
           = $12x4  - $400 x 3.75%   
           = $48    - $15   
           = $33
```

This is a profit of 33% instead of 12%. Almost 3x better (33%/12%).

Historically, S&P500 has made, on average, 7% a year.

Again, bear in mind that *the same way your winnings can be multiplied, it’s equally true for your losses.*

That is, if your stock loses $1, you actually lose $2 due to margin PLUS the interest (assuming 2x margin). If you are using a 4x margin and the stock drops 25% you lose it all.

Although this is not common, not long ago we all know it happened. And it might happen again. Granted it was not all during a single trading session (but it might be in the future!).

Press enter or click to view image in full size

![]()

I am not a financial advisor. So take this as a warning and do it at your own risk.

## Mean reversion

Although there are countless strategies, many revolve against the concept of mean reversion:

> *Mean reversion is a theory used in finance that suggests that asset prices and historical returns eventually will revert to the long-run mean or average level of the entire dataset.*

There are also many ‘indicators’ that promise to tell you when to buy or sell, or what the market trend is.

A very basic indicator is made by calculating the “standard deviation” of the random price fluctuations or volatility of the stock.

The indicator named “Bollinger bands” uses the standard deviation.

The standard deviation is easily calculated with, for example, [Pandas](https://pandas.pydata.org/):

> *Pandas is a fast, powerful, flexible and easy to use open-source data analysis and manipulation tool, built on top of the Python programming language.*

We’ll be using Pandas in future articles. I’ll share some simple code to get started with algorithmic trading.

I don’t think any indicator or strategy is a silver bullet (“[Nobody has cracked it. Period.](https://hackernoon.com/https-medium-com-supernova-the-truth-nobody-wants-to-tell-you-about-ai-for-trading-5d29a297ee93)”).

It’s pretty obvious because if these strategies or indicators were magical and openly disclosed, then most algorithmic traders would already be rich or making a ton of money.

Also, if these strategies or indicators were so good, it’s hard to think they would be openly available on the internet.

## A good trading platform

If you are looking for a very good Algorithmic Trading platform, where code is a first-class citizen, I would certainly recommend [Alpaca](https://alpaca.markets/).

They are truly a platform dedicated mostly to algorithmic trading. You can also buy/sell stocks on their online platform. They offer margin. Also, they have neat integrations, for example with TradingView.

Alpaca also offers a very nice paper trading account. The paper account trading lets you trade as if you had a live account, but with “fake” or “paper” money. You can test your algorithms posting buy/sell orders, etc. and have a peek on how your algorithm would do in a real-world scenario.

But I find more useful doing very simple custom baked “backtesting” scripts. Backtesting is testing your algorithm using historical data.

But remember the mantra:

> *Past Performance Is No Guarantee of Future Results.*

## A backtesting script

I recently did a basic backtesting script using Alpaca, downloading data for free from [Polygon.io](https://polygon.io/) and coded it in Python. In fact, over time I’ve done a couple. It isn’t hard.

My custom backtesting script basically loops over the data and simulates the decision making on when to buy or sell. It also keeps track of the transactions (buy and sell prices). In the end, I like to know how much money the algorithm would have made or lost.

In my next article, I’ll share some code to download historical minute data using Alpaca and do a simple backtest for the “Buy and Hold” strategy.

In the third part of this series, we’ll build on our code and work on a scalping script, that even gives good results with 2016 data.

I might also later write about some other strategies I’ve tried, and provide code snippets that some might find useful. Stay tuned.

See you next time!