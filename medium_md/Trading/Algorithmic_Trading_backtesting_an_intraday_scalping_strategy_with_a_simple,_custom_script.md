---
title: "Algorithmic Trading: backtesting an intraday scalping strategy with a simple, custom script"
url: https://medium.com/p/fcd15642555
---

# Algorithmic Trading: backtesting an intraday scalping strategy with a simple, custom script

[Original](https://medium.com/p/fcd15642555)

# Algorithmic Trading: backtesting an intraday scalping strategy

[![An Rodriguez](https://miro.medium.com/v2/resize:fill:64:64/1*E6SYD2xn2_Jx10uq-TCedA.jpeg)](/@anrodz?source=post_page---byline--fcd15642555---------------------------------------)

[An Rodriguez](/@anrodz?source=post_page---byline--fcd15642555---------------------------------------)

4 min read

·

Jan 13, 2020

--

1

Listen

Share

More

This is the third article of a series I’ve been writing. If interested, you can start [here](/@mrodz/algorithmic-trading-algorithms-to-beat-the-market-200c61ad84fc).

## What is scalping?

In the trading world, “scalping” refers to taking many small profits as quickly as possible.

Press enter or click to view image in full size

![]()

[Investopedia](https://www.investopedia.com/articles/trading/05/scalping.asp) defines a scalper as someone that

> intends to take as many small profits as possible, without letting them evaporate. This is the opposite of the “let your profits run” mindset, which attempts to optimize positive trading results by increasing the size of winning

As mentioned in my [first article,](/@mrodz/algo-trading-algorithms-to-beat-the-market-ccad674258b0) the use of margin might be useful to further increase the profits (or losses) made with a scalping strategy.

Doing manual scalping might be a time-intensive and stressful activity. Keeping track of all the charts for the stocks you care about is a lot of work. And buying/selling many times a day can be time-consuming.

Imagine doing submitting all those BUY and SELL orders as seen in the figure above. Doing that manually, with many stocks, is virtually impossible.

A computer can do this hard work for you. Faster and better.

## Let a computer do the hard work for you

Algo Trading is a very handy and simple way to exploit the scalping strategy.

With Algo Trading, you can do a simple script that buys or sells a stock when certain conditions are met. This happens as frequently as you want: many times a day, a minute or whatever.

The idea is to build a script that buys and sells as many times as possible, making a small profit as often as possible.

Scalping is just a general mindset of what we want to do. But we still need some indicator or signal of when to buy or sell.

## The concept of “mean reversion”

Press enter or click to view image in full size

![]()

In case it’s not already clear by the image above, [Investopedia](https://www.investopedia.com/terms/m/meanreversion.asp) defines “mean reversion” as :

> Mean reversion is a theory used in finance that suggests that [asset](https://www.investopedia.com/terms/a/asset.asp) prices and historical returns eventually will revert to the long-run mean or average level of the entire dataset.

This means that the price of a stock will tend to “revert” to its average price.

If a price suddenly hikes, we would expect it to return to a lower value. Also, if a price suddenly drops we would expect it to return to a higher value.

We can use this idea to have buy signals. If the price of a stock crosses the average from a lower to a higher price, we might submit a Buy order.

The scalping strategy suggests selling as soon as the price of the stock is higher than the purchase price.

## Backtesting a scalping strategy

In my last article, [Algorithmic Trading: backtesting your algorithm](/@mrodz/algo-trading-backtesting-your-algorithm-bd6d7385c89c), I posted some sample code on how to download one year of data.

Also how we could backtest a simple “buy and hold” strategy over that year of data.

I’m going to share a script that allows you to backtest a scalping trading algorithm.

The idea of the script is to:

* Loop over all days of a given year.
* Calculate an N-point moving average of the close price.
* For every day, loop over the minute-by-minute data.
* If the open price changes from being below the average to above the average, we simulate a `buy`order.
* We sell as soon as the open price is greater than the `buy_price`.

If you already downloaded the data as shown in my previous article, the script copied below should work out-of-the-box.

With 2016 data, using AAPL it performs almost 3x better than a “Buy and Hold” strategy! From 9.9% to 30.2%. I call “market change” the change in the market price of the stock, and “wallet change” the performance of the algorithm.

```
AAPL - market change: 1.099  
AAPL - wallet change: 1.302
```

If you also download the data for FTEC and V and run the script using

```
SYMBOLS = ["AAPL", "V", "FTEC"]
```

you would also get good profits over a Buy and Hold strategy:

```
AAPL - market change %: 1.099  
AAPL - wallet change %: 1.302  
AAPL - num_transactions: 454  
...  
V - market change %: 1.032  
V - wallet change %: 1.049  
V - num_transactions: 290  
...  
FTEC - market change %: 1.145  
FTEC - wallet change %: 1.298  
FTEC - num_transactions: 390
```

But again, as I said in my first article, this same algorithm underperforms using data from 2019! : /

Also, I haven’t tested for a wider range of symbols.

I’ll do that in one of my next articles.

I also want to do a rolling profit analysis over this strategy with more stocks. My goal will be to determine if there’s a moment common to most stocks where the market started growing so much in 2019.

Any ideas? I’d be glad to read your ideas.