---
title: "TradingView JS API Integration Tutorial: Introduction"
url: https://medium.com/p/5e4809d9ef36
---

# TradingView JS API Integration Tutorial: Introduction

[Original](https://medium.com/p/5e4809d9ef36)

# TradingView JS API Integration Tutorial: Introduction

[![Jon Church](https://miro.medium.com/v2/resize:fill:64:64/1*mMoQzenwQ3z5qGpUl67f2A.jpeg)](/@jonchurch?source=post_page---byline--5e4809d9ef36---------------------------------------)

[Jon Church](/@jonchurch?source=post_page---byline--5e4809d9ef36---------------------------------------)

2 min read

·

Jun 8, 2018

--

3

Listen

Share

More

> **This series is a work in progress, and I will be finishing this guide, covering more TradingView features, as well as enhancing the existing posts. I hope to make this process easier for everyone, so your feedback is greatly welcomed!**

[TradingView](http://www.tradingview.com) is the most popular tool for Crypto Charting, many exchanges and sites integrate their free [Charting Library](https://www.tradingview.com/HTML5-stock-forex-bitcoin-charting-library/) to provide a powerful charting interface that traders are familiar with.

However, the process of getting up and running with the charting library is confusing and poorly documented. This is evidenced by the large number of similar issues submitted to the project.

**My goal with this tutorial series is to show you how I went about setting this up myself, using CryptoCompare as a free source of price data.**

* [Part 1](/@jonchurch/tradingview-charting-library-js-api-setup-for-crypto-part-1-57e37f5b3d5a) focuses on setting up the Chart widget, introducing you to the TradingView JS API, and setting up a static chart.

[## TradingView Charting Library JS API Setup for Crypto: Part 1

### Check out the Introduction to this tutorial series, if you haven’t already. This is a convoluted process, so please…

medium.com](/@jonchurch/tradingview-charting-library-js-api-setup-for-crypto-part-1-57e37f5b3d5a?source=post_page-----5e4809d9ef36---------------------------------------)

* Part 2 expands on part 1 and implements realtime updates to the chart data using websockets

[## TradingView Charting Library JS API Setup for Crypto: Realtime Chart Updates

### In part 2 of this TradingView JS API Example Guide, we will be implementing Realtime price updates on the chart. Make…

medium.com](/@jonchurch/tv-part-2-b8c2d4211f90?source=post_page-----5e4809d9ef36---------------------------------------)

## Before you begin

The charting library, although available for free for both commercial and public use, is a private github project which you must apply for access to.

In the tutorial, I do not provide you with the charting library files, because their license agreement prohibits me from doing so 😭😭

**To actually implement this tutorial yourself, you will need to** [**apply for access**](https://www.tradingview.com/HTML5-stock-forex-bitcoin-charting-library/) **to the Charting Library, and then copy it into the** `/public/` **directory within the project.**

In the meantime, feel free to follow along to learn about what is involved. Sadly, even the documentation is only available to those who have access to the [Charting Library github repo](https://github.com/tradingview/charting_library). You will see a 404 if you’re not authorized

## Where’s the Code?

You can checkout the repo for all steps of this tutorial here:

[## jonchurch/tradingview-js-api-tutorial

### Contribute to tradingview-js-api-tutorial development by creating an account on GitHub.

github.com](https://github.com/jonchurch/tradingview-js-api-tutorial?source=post_page-----5e4809d9ef36---------------------------------------)