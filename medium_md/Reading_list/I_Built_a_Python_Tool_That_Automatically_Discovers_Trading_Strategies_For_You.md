---
title: "I Built a Python Tool That Automatically Discovers Trading Strategies For You"
url: https://medium.com/p/1f48b4d54578
---

# I Built a Python Tool That Automatically Discovers Trading Strategies For You

[Original](https://medium.com/p/1f48b4d54578)

Member-only story

# I Built a Python Tool That Automatically Discovers Trading Strategies For You

## Stop building strategies by hand. Let the machine find the combinations worth testing.

[![Kryptera](https://miro.medium.com/v2/resize:fill:64:64/1*OvL-lQO-0x15jAockFDYWQ@2x.jpeg)](/@Kryptera?source=post_page---byline--1f48b4d54578---------------------------------------)

[Kryptera](/@Kryptera?source=post_page---byline--1f48b4d54578---------------------------------------)

5 min read

·

May 19, 2026

--

6

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D1f48b4d54578&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40Kryptera%2Fi-built-a-python-tool-that-automatically-discovers-trading-strategies-for-you-1f48b4d54578&source=---header_actions--1f48b4d54578---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

> **Get the Bundle:** [**Simple Indicators Strategy Generator — Python Code Bundle**](https://kryptera.gumroad.com/l/luhjn)
>
> **Free Version Here:** [**Simple Indicators Strategy Generator — Python Code Bundle (Lite / Free Version)**](https://kryptera.gumroad.com/l/qlmvfl)

I want to tell you about a small Python prototype I built that has quietly become one of the most useful tools in my trading workflow.

The idea started from a simple frustration.

Every time I wanted to test a new strategy idea, I had to go through the same slow process. Pick an indicator. Decide what condition to use. Write the signal logic. Run the backtest. Look at the result. Adjust something. Run it again. It worked, but it was slow — and I was always making the decisions based on what I already thought I knew. There was no real exploration happening.

So I asked myself: what if the tool just tried combinations on its own?

## What It Does

The **Simple Indicator Strategy Generator** is a Python script that automatically assembles random indicator conditions into trading strategies and tests whether they work — without you…