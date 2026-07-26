---
title: "When a 2025 Math Finance Paper Taught Me to Time the Market Like an Options Hedger"
url: https://medium.com/p/d8bb29090edf
---

# When a 2025 Math Finance Paper Taught Me to Time the Market Like an Options Hedger

[Original](https://medium.com/p/d8bb29090edf)

Member-only story

# When a 2025 Math Finance Paper Taught Me to Time the Market Like an Options Hedger

[![Javier Santiago Gastón de Iriarte Cabrera](https://miro.medium.com/v2/resize:fill:64:64/1*WgVCI2ExLvGojne7AfMXGQ.jpeg)](/@jsgastoniriartecabrera?source=post_page---byline--d8bb29090edf---------------------------------------)

[Javier Santiago Gastón de Iriarte Cabrera](/@jsgastoniriartecabrera?source=post_page---byline--d8bb29090edf---------------------------------------)

23 min read

·

May 20, 2026

--

1

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dd8bb29090edf&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40jsgastoniriartecabrera%2Fwhen-a-2025-math-finance-paper-taught-me-to-time-the-market-like-an-options-hedger-d8bb29090edf&source=---header_actions--d8bb29090edf---------------------post_audio_button------------------)

Share

## I turned a pure-dual Bermudan option algorithm into a live MT5 EA — and here’s why the math actually makes sense for retail algo trading

*By Javier Santiago Gastón de Iriarte Cabrera· Algorithmic Trading & Quantitative Finance*

There’s a category of academic paper that looks, at first glance, completely useless for retail algo trading. Dense martingale notation, Snell envelopes, Doob–Meyer decompositions. The kind of paper where you need three cups of coffee just to parse the abstract.

Then you read it a second time and realise: **the core problem they’re solving is exactly the problem every discretionary trader faces every single day.**

When should I act? When should I wait?

That’s the **Optimal Stopping Problem** — and it’s the mathematical heart of *“A Pure Dual Approach for Hedging Bermudan Options”* by Aurélien Alfonsi, Ahmed Kebaier, and Jérôme Lelong, published in **Mathematical Finance** (2025, Vol. 35, pp. 745–759).

This article breaks down what the paper actually does, translates the key math into tradeable logic, and walks through a complete MT5 Expert Advisor implementation. Spoiler: with proper optimisation and additional directional filters, the excess reward signal can serve as the timing core of a genuinely profitable system.