---
title: "Algorithmic Trading with MACD and Python"
url: https://medium.com/p/fef3d013e9f3
---

# Algorithmic Trading with MACD and Python

[Original](https://medium.com/p/fef3d013e9f3)

# Algorithmic Trading with MACD and Python

## with the MACD cross strategy

[![Victor Sim](https://miro.medium.com/v2/resize:fill:64:64/1*DWtu0k55sDbZ2e72mU7qOA.jpeg)](/@victorsim14?source=post_page---byline--fef3d013e9f3---------------------------------------)

[Victor Sim](/@victorsim14?source=post_page---byline--fef3d013e9f3---------------------------------------)

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

Machine Learning trading works just fine for large hedge funds that make thousands of trades per day. However, private traders just don’t have the facilities to run machine learning models with millions of parameters on real time. This is why private algorithmic traders, use technical indicators to make automatic trades.

## What is MACD?

The technical indicator I will use today is MACD, Moving Average Convergence Divergence, is a momentum indicator, that shows the relationship between two moving averages. The MACD is calculated by subtracting the 26-period EMA from the 12-period EMA.

This MACD line is plotted on a signal line (9-period EMA). The intersections of these two lines are the signals of the MACD indicator. If the MACD indicator intersected into the signal line from below, it would be an uptrend. If the MACD indicator intersected from above the signal line, it would be a down-trend.

## Concept:

To be efficient when programming, it is necessary to create a general idea of how the program is supposed to work, in-order to have a clear goal in mind. This program should be able to plot the MACD signal and the MACD line, and make trades based on signals from the MACD indicator. A good program should also be able to evaluate the profitability of a trading strategy, so as to optimize it.

## The Code:

```
import yfinance  
import talib  
from matplotlib import pyplot as plt
```

These are the libraries that I will use for the program. yfinance is used to download financial data of shares, talib is used to calculate the values of the MACD indicator. Matplotlib is used to plot the data, to better understand how the technical indicator.

```
data = yfinance.download('NFLX','2016-1-1','2020-1-1')  
data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(data['Close'])  
fig = plt.figure()
```

This script downloads the data, and then it calculates the macd values such as the signal and the histogram that defines the trend.

Press enter or click to view image in full size

![]()

This is the graph of the two lines of the MACD indicator and the signal line. This is just to troubleshoot the program to make sure the indicator is working. As we can see, the indicator is clearly working, as the two lines intersect frequently.

```
def intersection(lst_1,lst_2):  
    intersections = []  
    insights = []  
    if len(lst_1) > len(lst_2):  
        settle = len(lst_2)  
    else:  
        settle = len(lst_1)  
    for i in range(settle-1):  
        if (lst_1[i+1] < lst_2[i+1]) != (lst_1[i] < lst_2[i]):  
            if ((lst_1[i+1] < lst_2[i+1]),(lst_1[i] < lst_2[i])) == (True,False):  
                insights.append('buy')  
            else:  
                insights.append('sell')  
            intersections.append(i)  
    return intersections,insightsintersections,insights = intersection(data["macd_signal"],data["macd"])
```

The intersection function uses a reasonably unconventional way of finding intersections:

1. If the value from list 1 is bigger than the value of the same index in list 2, store True. Else, store False.
2. Apply this function to an index of 1 greater. If the stored value is different, an intersection must have happened.

This is the only way to calculate intersections, as the intersection could have happened in between the real points, making it impossible to find similar points within the two lists.

We use this function to find the points of intersection and make a note of if the program would sell or buy the stock.

To make a stock trading program good, we must evaluate the profitability of the program.

```
profit = 0  
pat = 1  
for i in range(len(intersections)-pat):  
    index = intersections[i]  
    true_trade= None  
    if data['Close'][index] < data['Close'][index+pat]:  
        true_trade = 'buy'  
    elif data['Close'][index] > data['Close'][index+pat]:  
        true_trade = 'sell'  
    if true_trade != None:  
        if insights[i] == true_trade:  
            profit += abs(data['Close'][index]-data['Close'][index+1])   
        if insights[i] != true_trade:  
            profit += -abs(data['Close'][index]-data['Close'][index+1])
```

This program calculates the profitability by calculating the true\_trade, which stores the value of if the value went up or dropped. If the trade made matched the true\_trade variable, the trade was profitable. If the trade did not match, the trade lost.

When running the program, the profit was -288.26. What?

## What is happening?

I found this error and kept trying to mess with the patience value, that is how long after the intersection was made, the trade was made. All values were negative. When facing a problem like this, in which the polarity of the values are all wrong, one can easily change the polarity.

In this case, this is because the intersection order is incorrect! When we made the intersections, we did the opposite insights from the strategy we described! For example, if the MACD line intersected from above, the program would mark this as a increase in price! This would make all the trades that were supposed to be profitable, to become a loss!

By changing the intersection code to this:

```
def intersection(lst_1,lst_2):  
    intersections = []  
    insights = []  
    if len(lst_1) > len(lst_2):  
        settle = len(lst_2)  
    else:  
        settle = len(lst_1)  
    for i in range(settle-1):  
        if (lst_1[i+1] < lst_2[i+1]) != (lst_1[i] < lst_2[i]):  
            if ((lst_1[i+1] < lst_2[i+1]),(lst_1[i] < lst_2[i])) == (True,False):  
                insights.append('buy')  
            else:  
                insights.append('sell')  
            intersections.append(i)  
    return intersections,insightsintersections,insights = intersection(data["macd_signal"],data["macd"])
```

We gain a profit of 298 dollars!

## Conclusion:

I wrote another article about RSI, and that program only made 58 dollars with the same data. This program made 298 dollars, buying one share for each trade. Here are a few ways you can improve my program:

1. Tweak the patience variable

This variable is how long after the intersection,the trade will be made. Toy with this value, find a pattern, and optimize it to get better results.

2. Find the best share

For which stock does this algorithm work best? Test this program on different companies to evaluate.

## My links:

If you want to see more of my content, click this [**link**](https://linktr.ee/victorsi).