---
title: "I Handed ChatGPT $100 to Trade Stocks — Here’s What Happened in 2 Months."
url: https://medium.com/p/ca1dfeb92edb
---

# I Handed ChatGPT $100 to Trade Stocks — Here’s What Happened in 2 Months.

[Original](https://medium.com/p/ca1dfeb92edb)

Member-only story

# I Handed ChatGPT $100 to Trade Stocks — Here’s What Happened in 2 Months.

[![Civil Learning](https://miro.medium.com/v2/resize:fill:64:64/1*C7yKQA2alY8DVjVu35-fCg.png)](/@civillearning?source=post_page---byline--ca1dfeb92edb---------------------------------------)

[Civil Learning](/@civillearning?source=post_page---byline--ca1dfeb92edb---------------------------------------)

4 min read

·

Sep 3, 2025

--

272

Listen

Share

More

## What happens when you let a chatbot play Wall Street? It’s up 29% while the S&P 500 lags at 4%.

I’ve lost count of how many times I’ve seen those spammy ads online: *“Our AI knows the next hot stock, subscribe now!”* It always feels like a scam, so I ignore them.

But the idea stuck in my head. What if I actually let ChatGPT pick stocks for me? Not fake backtests. Not cherry-picked screenshots. Real Money, real trades.

So I tried it. Two months later, here’s where things stand:

* ChatGPT’s portfolio: **+29.22%**
* S&P 500: **+4.11%**

I’m not saying it’s the new Warren Buffett. But it didn’t crash and burn either.

This whole thing’s based on Nathan B. Smith’s GitHub project, where he’s testing if ChatGPT can pick winning micro-cap stocks — those tiny companies worth less than $300 million.

## Why Let a Bot Pick Stocks?

You’re scrolling, and another ad pops up screaming, “AI will make you rich with stocks!”

Nathan saw those too and thought, “Yeah, right.”

But then he got curious.

Could ChatGPT actually outsmart the market?

Not some scammy app, but a legit test with $100 he could afford to lose.

He kicked it off in June 2025, focusing on micro-caps — small, risky stocks with big upside (or big crashes).

The plan? Let ChatGPT decide what to buy or sell, track everything on GitHub, and see if it beats the S&P 500 or Russell 2000.

He places trades himself, but the AI’s the boss, with rules like “sell if it drops 10%” to avoid a total bust. It runs till December 2025, and it’s all out in the open — no smoke and mirrors.

Why’s this fun? AI’s everywhere — writing emails, editing photos. But handling real money? That’s next-level. It’s like letting your dog pick lottery numbers, except this dog’s got data and brains.

Press enter or click to view image in full size

![]()

## How It Goes Down

The setup’s dead simple, like making a sandwich. Here’s the gist:

* **Daily Data**: Nathan grabs stock prices, volumes, and market info every trading day and saves it in a CSV on GitHub. Keeps things honest.
* **AI’s Turn**: He feeds ChatGPT the data and asks, “What’s the move?” It picks micro-caps to buy or sell.
* **Weekend Vibes**: On weekends, ChatGPT digs deeper, rethinking the whole portfolio and hunting for new ideas.
* **Real Deal**: Nathan makes the trades in a real account. Stop-losses keep losses in check.
* **Charts and Logs**: Results go into CSVs, and a script draws graphs to see if the AI’s beating the market.

The code’s not rocket science. There’s a script called `trading_script.py` that updates the portfolio. Think of it like checking your piggy bank. Here’s a quick peek at the idea (full code’s on GitHub):

```
import pandas as pd  # Like a spreadsheet on steroids  
import yfinance as yf  # Gets stock prices free  
  
# Grab yesterday's portfolio  
try:  
    portfolio = pd.read_csv('my_stocks.csv')  
except:  
    cash = float(input("How much you starting with? "))  
    portfolio = pd.DataFrame({'Cash': [cash]})  
# Check today's prices  
stocks = ['LIL', 'TINY']  # AI picks these  
prices = yf.download(stocks, period='1d')['Close']  
# Update what you've got  
for stock in stocks:  
    if stock in portfolio.columns:  
        portfolio[stock] = portfolio[stock] * prices[stock]  # What's it worth now?  
# Add it up  
total = portfolio.sum().iloc[0]  
print(f"Your stash: ${total:.2f}")  
# Save it  
portfolio.to_csv('my_stocks.csv')
```

Run that, copy the numbers, and tell ChatGPT, “Yo, what should I trade?” It’s like asking a buddy for a hot tip, but smarter.

![]()

Then there’s `Generate_Graph.py` to see how you’re doing. It plots your portfolio against the S&P 500. Check this out:

```
import matplotlib.pyplot as plt  
import pandas as pd  
import yfinance as yf  
  
# Your data  
data = pd.read_csv('my_stocks.csv')  
your_cash = data['Total_Equity'] / 100  # Start at $100  
# S&P 500  
sp500 = yf.download('^GSPC', start='2025-06-30')['Close']  
sp_cash = sp500 / sp500.iloc[0]  # Start at 1  
# Make a chart  
plt.plot(your_cash, label='AI's Game', color='purple')  
plt.plot(sp_cash, label='S&P 500', color='gray')  
plt.title('AI vs. The Big Dogs')  
plt.legend()  
plt.show()
```

Run it with `python Generate_Graph.py --start-equity 100`, and you get a chart. If the purple line’s above grey, your AI’s winning.

## The Tools: No Fancy Lab Needed

This runs on basic stuff:

* **Python**: The engine.
* **Pandas + yFinance**: For data and prices.
* **Matplotlib**: Draws cool graphs.
* **ChatGPT-4o**: The stock-picking genius.

You need Python 3.11+, Wi-Fi, and a tiny bit of storage for CSVs. Set it up like this:

```
python -m venv coolenv  
source coolenv/bin/activate  # Windows: coolenv\Scripts\activate  
pip install pandas yfinance matplotlib
```

## How’s It Doing?

By late August 2025, the portfolio’s up 29.22% since June. The S&P 500? Just 4.11%. It’s even crushing the Russell 2000. Week 4 was nuts — the charts look like a rocket launch.

You can see every trade in the GitHub CSVs: profits, losses, the works. Logs keep it real. But fair warning: micro-caps are wild. One bad pick, and poof, gains gone.

## Wanna Try It?

The repo’s got a “Start Your Own” folder with templates. Clone it, play around, and ask ChatGPT for stock picks. Steps:

1. Install the stuff (see above).
2. Run `trading_script.py --file "my_stocks.csv"`.
3. Tell ChatGPT the numbers and get trade ideas.
4. Trade in your account.
5. Plot with `Generate_Graph.py`.

The repo is open on GitHub:  
 👉 [ChatGPT Micro-Cap Experiment](https://github.com/LuckyOne7777/ChatGPT-Micro-Cap-Experiment?utm_source=chatgpt.com)

All you need is Python, the internet, and some patience.