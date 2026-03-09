---
title: "Using Python and Robinhood to Build An Iron Condor Options Trading Bot"
url: https://medium.com/p/4a16e29649b0
---

# Using Python and Robinhood to Build An Iron Condor Options Trading Bot

[Original](https://medium.com/p/4a16e29649b0)

Member-only story

# Using Python and Robinhood to Build An Iron Condor Options Trading Bot

[![Melvynn Fernandez](https://miro.medium.com/v2/resize:fill:64:64/1*nhHvcm9umR5Ev3WaEBsdGg.jpeg)](/@mentormelv?source=post_page---byline--4a16e29649b0---------------------------------------)

[Melvynn Fernandez](/@mentormelv?source=post_page---byline--4a16e29649b0---------------------------------------)

4 min read

·

Feb 21, 2020

--

4

Listen

Share

More

Press enter or click to view image in full size

![]()

So I recently discovered the potential of revenue in options trading. My mind works very technically and noticed that trading strategies are nothing more but conditional statements. So I decided to create a simple iron condor trading strategy.

According to [OptionAlpha](https://optionalpha.com/members/video-tutorials/neutral-strategies/iron-condors), iron condor options trading strategy is the most profitable and low risk trading strategy to be used with options. I will use Python and Jupyter Notebook to place these option orders in Robinhood.

Let us first try to understand what an iron condor strategy is. For those who are familiar with options they are basically four option contracts. There are iron condors which can require all calls, all puts or the basic iron condor. For this example we will be using the base. Requiring to order a long put, short put, short call, and long call all at the same time. The best time to run this play is when we know that the stock we are ordering is expecting minimal movement up and down within a specific time frame.

Press enter or click to view image in full size

![]()

Most investors I know love running this play 30–45 days from expiration. This is the advantage of the time decay. They also run this play on index options rather than individual stocks because of the fact that indexes are not that volatile. But we can get more into logistics some other time, let’s focus on creating code that will work.

### What we need

For those who do not follow me, I have created two articles that will already help us in the first steps. So we need to [connect to Robinhood using Python](https://towardsdatascience.com/using-python-to-get-robinhood-data-2c95c6e4edc8). Create code that will [order options for us](https://towardsdatascience.com/how-to-use-python-to-buy-options-from-robinhood-8022bbcf3ddf). After all of the initial set up the actual iron condor strategy is very straightforward.

### Setup of iron condor

* We want the stock the stay in between strike price A (lower than stock price) and B (higher than stock price)
* Buy a put lower than strike price A
* Sell a put at strike price A
* Sell a call strike price B
* Buy a call higher than strike Price B
* All these contracts will have the same expiration date

### Writing code

First off let’s find a stock to mess around with. I went ahead and did some research and will be using Fitbit for our code. Fitbit had a jump around November but I believe that it will be moving sideways in the future. `robin_stocks` makes it simple to see which available options we can order. We just need to type in the stock symbol.

It will now output a DataFrame that looks like this:

So the main column we want to focus on from here is the `expiration_date` Let’s start with creating code that will find an expiration date 30 to 45 days from now. We will then use these dates to eliminate the existing option orders. We will now have a list of available options that would be perfect for our iron condor.

This next part now, I grab the current stock price and append it to a list I made out of the strike price column. I then sort the values in order to use the index value to pick the strike prices necessary for each order. Then out of the expiration dates, I am just going to pick the furthest one out of the 30–45 days from today.

For the following, I simply just place 4 different option orders and plug in all the necessary information. After all of that, we have successfully created Python code that executes an order for an iron condor!

Some of my other articles involving Python and Robinhood:

[## Using Python and Robinhood to Create a Simple Buy Low — Sell High Trading Bot

### So I have been messing with Robinhood lately and been trying to understand stocks. I am not a financial advisor or…

towardsdatascience.com](https://towardsdatascience.com/using-python-and-robinhood-to-create-a-simple-buy-low-sell-high-trading-bot-13f94fe93960?source=post_page-----4a16e29649b0---------------------------------------)

Code above can be found [here](https://www.patreon.com/posts/34200909) and please feel free to follow my trading journey [here](https://www.patreon.com/melvfnz).

I also have tutoring and career guidance available [here](https://square.site/book/8M6SR06V2RQRB/mentor-melv)!

Don’t forget to connect with me on [LinkedIn](https://www.linkedin.com/in/melvfernandez/) if you guys have any questions, comments or concerns!

***Note from Towards Data Science’s editors:*** *While we allow independent authors to publish articles in accordance with our* [*rules and guidelines*](https://towardsdatascience.com/questions-96667b06af5)*, we do not endorse each author’s contribution. You should not rely on an author’s works without seeking professional advice. See our* [*Reader Terms*](https://towardsdatascience.com/readers-terms-b5d780a700a4) *for details.*