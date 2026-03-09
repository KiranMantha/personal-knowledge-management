---
title: "Algorithmic Trading with RSI using Python"
url: https://medium.com/p/f9823e550fe0
---

# Algorithmic Trading with RSI using Python

[Original](https://medium.com/p/f9823e550fe0)

# Algorithmic Trading with RSI using Python

## Using talib and yfinance

[![Victor Sim](https://miro.medium.com/v2/resize:fill:64:64/1*DWtu0k55sDbZ2e72mU7qOA.jpeg)](/@victorsim14?source=post_page---byline--f9823e550fe0---------------------------------------)

[Victor Sim](/@victorsim14?source=post_page---byline--f9823e550fe0---------------------------------------)

4 min read

·

Sep 17, 2020

--

3

Listen

Share

More

Press enter or click to view image in full size

![]()

Machine Learning is computationally intensive, as the algorithm is not deterministic and therefore must be constantly tweaked over time. However, technical indicators are much quicker, as the equations do not change. This therefore improves their ability to be used for real-time trading.

Here is the [github repo](http://motriael.com/6QX2) (ads).

## What is RSI?

To create a program that uses RSI, we must first understand the RSI indicator. RSI is an acronym of Relative Strength Index. It is a momentum indicator, that uses the magnitude of price changes, to evaluate if a security is overbought or oversold.

If the RSI value is over 70, the security is considered overbought, if the value is lower than 30, it is considered to be oversold. Overbought refers that the bubble created from the buying might pop soon, and therefore the price will drop. This creates a strong entry point.

However, good practice is to make a selling order, only when the RSI value intersects the overbought line, as this is a more conservative approach. At least to guessing when the RSI will reach the highest point.

## Concept:

This program seeks to use the talib (technical analysis) library to implement the intersection between the RSI line and the oversold and overbought line. The bulk of the program does not come from programming the indicator (as it has been created in the library), but rather the implementation of how the oversold and overbought regions can be used to make trades.

## The Code:

```
import yfinance  
import talib  
from matplotlib import pyplot as plt
```

These are the prerequisites for the program. Yfinance is used to download stock data, talib is to calculate the indicator values. Matplotlib of course is to plot the data as a graph.

```
data = yfinance.download('NFLX','2016-1-1','2020-1-1')  
rsi = talib.RSI(data["Close"])
```

This script accesses the data and also calculates the rsi values, based on these two equations:

*RSIstep1*​=100−[100/(1+Average loss/Average gain​)]

*RSIstep2*​=100−[100/(1+Average average loss∗13+Current loss/Previous average gain∗13+Current gain​)​]

```
fig = plt.figure()  
fig.set_size_inches((25, 18))  
ax_rsi = fig.add_axes((0, 0.24, 1, 0.2))  
ax_rsi.plot(data.index, [70] * len(data.index), label="overbought")  
ax_rsi.plot(data.index, [30] * len(data.index), label="oversold")  
ax_rsi.plot(data.index, rsi, label="rsi")  
ax_rsi.plot(data["Close"])  
ax_rsi.legend()
```

This plot shows all the overbought and oversold territories, along with the RSI values calculated for each value of recorded closing price of the stock. This gives a good visualization of the stock data

Press enter or click to view image in full size

![]()

This is the resultant graph. We can see the RSI value fluctuating between the different sections, as time goes on. The good thing about RSI is that it is relative. This means the strength of the signal is relative not to the actual value, but the relationship of past values.

## The Missing Step:

Usually, the articles stop here. They end after giving the preliminary code of the stock trading program. It is necessary to go further and truly evaluate the stock trading program, based on the profitability of the program. This is why I will hand in the program.

```
section = None  
sections = []  
for i in range(len(rsi)):   
    if rsi[i] < 30:  
        section = 'oversold'  
    elif rsi[i] > 70:  
        section = 'overbought'  
    else:  
        section = None  
    sections.append(section)
```

This script records the sections in which every point falls in. It is either in the overbought, oversold or the None region, which refers to in between the two lines.

```
trades = []  
for i in range(1,len(sections)):  
    trade = None  
    if sections[i-1] == 'oversold' and sections[i] == None:  
        trade = True  
    if sections[i-1] == 'overbought' and sections[i] == None:  
        trade = False  
    trades.append(trade)
```

This script integrates the basic strategy for RSI trading. The trading strategy is when the value leaves the overbought and oversold sections, it makes the appropriate trade. For example, if it leaves the oversold section, a buy trade is made. If it leaves the overbought section, a sell trade is made.

```
acp = data['Close'][len(data['Close'])-len(trades):].values  
profit = 0  
qty = 10  
for i in range(len(acp)-1):  
    true_trade = None  
    if acp[i] < acp[i+1]:  
        true_trade = True  
    elif acp[i] > acp[i+1]:  
        true_trade = False  
    if trades[i] == true_trade:  
        profit += abs(acp[i+1] - acp[i]) * qty  
    elif trades[i] != true_trade:  
        profit += -abs(acp[i+1] - acp[i]) * qty
```

This script uses the trades made by the program to calculate the profit or the loss from each trade. This gives the best evaluation of the program, as it targets exactly the variable to look for. The qty variable calculates how many shares are bought.

After running the program, the profit calculated is:

```
Profit : $58.3
```

## Conclusion:

As a matter of fact, a profit of 58.3 dollars is actually not a very good investment, when considering the risk to reward ratio. There are quite a few ways you can improve my program:

1. Tweak the patience variable

This variable is how long after the RSI value, the trade will be made. Toy with this value, find a pattern, and optimize it to get better results.

2. Find the best company

For which stock does this algorithm work best? Test this program on different companies to evaluate.

## My links:

If you want to see more of my content, click this [**link**](https://linktr.ee/victorsi).