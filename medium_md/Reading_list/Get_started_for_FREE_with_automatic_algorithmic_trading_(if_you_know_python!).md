---
title: "Get started for FREE with automatic algorithmic trading (if you know python!)"
url: https://medium.com/p/3ce481fe23fc
---

# Get started for FREE with automatic algorithmic trading (if you know python!)

[Original](https://medium.com/p/3ce481fe23fc)

# Get started for FREE with automatic algorithmic trading (if you know python!)

[![Patrick Collins](https://miro.medium.com/v2/resize:fill:64:64/1*58RJmDZ0jCcszWF2Lt92EA.png)](/?source=post_page---byline--3ce481fe23fc---------------------------------------)

[Patrick Collins](/?source=post_page---byline--3ce481fe23fc---------------------------------------)

4 min read

·

Sep 24, 2019

--

1

Listen

Share

More

The internet has a lot of information…

Which is fantastic, but it can be quite overwhelming.

Press enter or click to view image in full size

![]()

Choosing a platform to start your [automated trading](https://www.investopedia.com/articles/trading/11/automated-trading-systems.asp) can be a really confusing task, and also pretty daunting to even get started. I’m here to tell you that anyone with some software knowledge you can get started — sorry yants (You Are Not Technical), this one isn’t for you. **The beginners who know some coding, this is for you**. But there are tools out there where you can build an automated trading platform *without knowing any code* (that information isn’t here)*.*

For those of you who don’t know what auto trading is, it’s basically a combination of algo-trading ([brief summary of algorithmic trading)](https://www.investopedia.com/articles/active-trading/101014/basics-algorithmic-trading-concepts-and-examples.asp) and automation of the live execution (basically a robot performs the trades)

> Algo-Trading + Auto-Execution = **Auto-Trading**

It basically means you auto trade when certain criteria that you have laid out are met. For example, you want to automatically buy a share of apple whenever they launch a new product, and sell a share whenever they launch a product that is a copy of the last product. This would be your trading strategy, and a computer could definitely do that much faster than you could (getting the data for that would be a little trickier…)

It would be great if we didn’t even have to do it manually, and it would just work when we sleep. That’s exactly what automated trading is

So let’s go over a quick getting started bit. Here are the tools you’ll need to start. To make it simple, I’ll focus just on stocks you can get on the exchanges.

## 1. The algo-trading

Right: In order to auto trade, you have to have an idea on what you want to auto trade. Lucky for us, there are plenty of tools to start. The main one I want to focus on is [Quantopian](https://www.quantopian.com/).

Press enter or click to view image in full size

![]()

If you’re in the space at all you’ve for sure heard of Quantopian. They have fantastic tutorials to [backtest](https://www.investopedia.com/terms/b/backtesting.asp) your ideas and build them out. They run off python and use the python notebook framework for their research purposes. It takes a little ramp-up to learn, but once you get the hang of it you can try out almost anything you want. You can even upload your own data sets and add live feeds! (Self-plug to my company [Alpha Vantage](https://www.alphavantage.co) where you can get raw data!)

Now Quantopian has a lot of paid features as well, but just to get started, all you have to do is sign up, and right away you can begin testing whatever you want. If you’re a TOTAL beginner, this is even better since the tutorials are literally step-by-step. If you’ve been around the block, this is great too since you can just learn the tools and start plugging away.

Why this for your backtesting and strategy building tool? That’s simple.

Quantopian is simple. Simple and powerful. I like simple. Really easy to use and integratable. Some other tools like Q[uant Connect](https://www.quantconnect.com/), are also good sources, but Quantopian (to me) seems to be the bread and butter.

## 2. The auto-execution

The next bit you’ll need is something to start auto executing. This is where I have spent a LOT of time. Searching for a brokerage with the best API for auto-trading. A brokerage is where you can actually trade on your strategy that you toiled over so hard.

Now you’ll need an API key from a brokerage, so you can just drop a quick: account.trade(“buy”, “aapl”, 10) or whatever your strategy does. Most brokerages have API keys (Ally, thinkorswim, interactive brokers, tradier), however, for you free to play beginners, [Alpaca](https://alpaca.markets/) seems to be the best choice out there, since they have commission-free trading — you can even test out your algorithms live with their paper trading.

Press enter or click to view image in full size

![]()

These guys are developer-focused, another reason I like them the best. Robinhood has a similar style in the fact that they are commission-free, but they are not geared towards developers and automated trading, and the API they have is not supported or outdated. This auto trading we are talking about and want to do is Alpaca’s bread and butter.

## Next steps…

So that’s pretty much it, at the top level, most simple, bare bones of it, that’s all you need. A place to test and create, and a place to execute. 2 tools, and you can start going.

There are a TON more tools to help you along on this journey, and building up more and more tools will come along. Maybe you’ll want to save your data, and get more data, or post your data on an application — see [Alpha Vantage](https://www.alphavantage.co/) again. Maybe you want to store your data and don’t know how to or where? Check out [MongoDB](https://www.mongodb.com/) and the [Man AHL wrapper](https://github.com/manahl/arctic). Maybe you want better charting and interactive charts — see T[radingView](https://www.tradingview.com/). Get into crypto, options, futures, more technical analysis, the list goes on and on.

But that’s about it, literal bare bones to get you started.

I’m looking for any feedback to though! From all my days of researching (and what I’ve used myself), this seems to be the simplest starting point. Let me know what you think!