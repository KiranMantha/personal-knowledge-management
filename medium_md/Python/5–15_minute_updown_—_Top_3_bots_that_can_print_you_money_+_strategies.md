---
title: "5–15 minute up/down — Top 3 bots that can print you money + strategies"
url: https://medium.com/p/9a815fb64afd
---

# 5–15 minute up/down — Top 3 bots that can print you money + strategies

[Original](https://medium.com/p/9a815fb64afd)

# **5–15 minute up/down — Top 3 bots that can print you money + strategies**

[![Moonsat](https://miro.medium.com/v2/resize:fill:64:64/1*2sX8H4-ftwrKEU1134O5wQ.png)](/?source=post_page---byline--9a815fb64afd---------------------------------------)

[Moonsat](/?source=post_page---byline--9a815fb64afd---------------------------------------)

7 min read

·

Feb 18, 2026

--

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D9a815fb64afd&operation=register&redirect=https%3A%2F%2Fmoonsat.medium.com%2F5-15-minute-up-down-top-3-bots-that-can-print-you-money-strategies-9a815fb64afd&source=---header_actions--9a815fb64afd---------------------post_audio_button------------------)

Share

![]()

> ***In this article:*** *how it works, why it’s blowing up, pros/cons, strategies, and Top 3 successful bots in this markets*

Imagine staring at BTC price action, knowing you have exactly 300 seconds to decide: Up or Down? — That’s the new reality on Polymarket. This isn’t just another market — it’s turning prediction trading into something closer to scalping Bets resolve every 300 seconds via Chainlink oracles, pulling prices from Coingecko/Binance — perfect for scalpers

![]()

> *Media like Yahoo Finance calls it “gamification of trading,” while BeInCrypto highlights bot potential. But the real story? Whales printing stacks.Enter our three stars:*

* 0x1d00341343e339…: $190,586 profit since Jan 2026.
* PBbot1 (“happy making”): $140,953 since Dec 2025.
* gabagool22: $824,341 since Oct 2025, with 620k views.

These profiles scream automation: thousands of predictions, steady profit curves, and high-volume trades. We’ll dissect them, decode their on-chain secrets, apply betting math like Kelly Criterion for sizing, and explore “profit guarantees” for timing. **Main takeaway**: Success here is strategy + bots, not luck. DYOR, but let’s unpack how they win.

## Top 3 Bots: Profile Overviews & Profit Curves

These wallets joined recently but racked up massive P/L through relentless 5-min/15-min bets. All focus on crypto volatility, with BTC leading, followed by ETH/SOL/XRP.

* **0x1d00341343e339…:** Joined Jan 2026, 27.3k views, $190,586 all-time P/L. Positions ~$17–29k, biggest win $13.7k, 4,924 predictions. Graph shows consistent upward grind — no big drawdowns.
* **PBbot1:** Joined Dec 2025, 33.8k views, $140,953 P/L. Positions ~$5.8k, biggest $5.5k, 8,192 predictions. Bio “happy making” hints at bot joy. Smooth curve, high trade count.
* **gabagool22:** Joined Oct 2025, 620k views (viral!), $824,341 P/L. Positions ~$21k, biggest $4.7k, 26k predictions. Longest runner, massive scale.

![]()

These curves scream systematic trading — likely bots scanning for mispriced odds in real-time.

## Decoding the Wallets: Technical Analysis with On-Chain Tools

> *To uncover their secrets, we need to decode these wallets beyond Polymarket profiles. Drawing from advanced on-chain analysis techniques*

Here’s how to pull raw transaction data and stats. This reveals entry/exit timing, average prices, and volumes — key to spotting bot patterns.

**Step-by-Step Decoding Guide** Use Dune Analytics or Etherscan for raw txs, then Python scripts for aggregation. Here’s adapted code to decode a wallet like these (run in a Python env with [web3.py](https://web3.py/)

and pandas):

**1. Fetch Transactions:** Use Etherscan API or web3 to get tx history for the wallet address.

```
from web3 import Web3  
import pandas as pd  
import requests  
  
# Replace with actual address, e.g., '0x1d00341343e339...'  
wallet_address = 'WALLET_ADDRESS_HERE'  
api_key = 'YOUR_ETHERSCAN_API_KEY'  # Get free from Etherscan  
  
url = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&sort=asc&apikey={api_key}"  
response = requests.get(url)  
txs = pd.DataFrame(response.json()['result'])  
txs['value'] = txs['value'].astype(float) / 10**18  # Convert wei to ETH/USDC
```

**2. Filter Polymarket Interactions:** Look for txs to Polymarket contracts (e.g., 0x4bFb41d5B3570DeFbefd03C39a9AcedE6C1163ce for trades).

```
polymarket_contracts = ['0x4bFb41d5B3570DeFbefd03C39a9AcedE6C1163ce']  # Add more if needed  
poly_txs = txs[txs['to'].isin(polymarket_contracts)]
```

**3. Calculate Stats:** Aggregate buys/sells, avg prices, volumes.

```
# Group by market (use 'input' decoding for market IDs - requires ABI)  
from web3 import Web3  
w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))  # Polymarket on Polygon  
  
# Example ABI snippet for trade decoding (simplified)  
abi = [{'name': 'trade', 'inputs': [{'name': 'marketId', 'type': 'uint256'}, {'name': 'direction', 'type': 'bool'}]}]  # Full ABI from explorer  
  
decoded = []  
for tx in poly_txs.to_dict('records'):  
    input_data = tx['input']  
    decoded_tx = w3.eth.contract(abi=abi).decode_function_input(input_data)  
    decoded.append(decoded_tx)  
  
# Now aggregate: avg price, total volume, P/L per market  
poly_df = pd.DataFrame(decoded)  
stats = poly_df.groupby('marketId').agg({'value': 'sum', 'direction': 'count', 'price': 'mean'})  # Adapt 'price' from decoded  
print(stats)  # Output: Total amount, avg price, buy/sell volume
```

> ***This script outputs detailed stats:*** *total staked, average entry prices (e.g., 31¢–59¢ for BTC Downs in 0x1d00…), volumes (6–7k shares), and biases.*

For PBbot1, it shows consistent small wins; gabagool22 has massive scales. Running this reveals bot-like timing — entries seconds after market open, suggesting API automation. Pro tip: Sandbox scripts, use dummy wallets first to avoid risks.

## Deep Dive: Trade Patterns & Biases Across the Wallets

All three favor BTC (60–70% trades), with ETH/SOL/XRP for diversification. High shares (1k–7k+) indicate confidence in edges.

* **0x1d00…:** Down bias (31¢–59¢ entries, $4.9k–$7.2k wins). Mixes Up/Down but leans Down in flat ranges. Small losses (-$21–$240) show tight risk control.
* **PBbot1:** Balanced mix (45¢–62¢), strong ETH Downs ($440–$1.5k). 8k predictions scream bot — consistent, low-variance wins.
* **gabagool22:** Volume king (1–3k shares), Down heavy (33¢–71¢). Big wins ($1.3k–$2.8k), few reds (-$186). Viral views suggest it’s a followed legend. They aren’t “lucky degen gamblers.” They’re three completely different philosophies of algorithmic trading.

## 2. PBot1 — The House (Market Maker & Spread Trader)

![]()

**Profile:** [https://polymarket.com/@PBot1](https://polymarket.com/@PBot1?r=goldminer11)

* All‑time PnL: around **$140k+**
* Thousands of short‑horizon BTC/ETH “Up or Down” bets
* Average entry: **45–49¢**, very rarely paying above 50¢

**What the trades tell us:**

PBot1 almost never pays full “fair value” for a binary outcome. Instead, they sit in the order book and let people come to them.

* They post **limit bids on both sides** (Up and Down) slightly below the mid price, usually in the mid‑40s.
* When impatient traders smash market orders, PBot1 gets filled at a discount.
* In many windows they end up holding **both legs** at ~47–48¢ each: Total cost ≈ **$0.95–0.96** Guaranteed payout at expiry: **$1.00** Locked‑in edge: **3–5%** per cycle, before fees.

They are not trying to predict whether BTC goes up or down in the next 5 minutes. They are monetizing **other people’s impatience** and the fact that most users hate waiting for limit orders.

**Key idea:** he rent liquidity to everyone else and collect a small tax on almost every flip.

## 3. gabagool22 — The Hybrid Bot (Spread First, Direction Second)

**Profile:** [https://polymarket.com/@gabagool22](https://polymarket.com/@gabagool22?r=goldminer11)

![]()

* All‑time PnL: **$830k+**
* 26k+ predictions, active since October 2025
* Constant flow of BTC/ETH/XRP/SOL Up/Down positions

**What the latest trades show:**

He often holds **both Up and Down** around the same time buckets.

* Many entries sit in the **47–52¢** zone — the sweet spot for collecting a 3–5% edge if both sides fill.
* The ROI on winners frequently lands in the **+18–110%** range, which matches buying near 48–52¢ and getting paid $1 at expiry.

So instead of being a pure “quant directional” trader, gabagool22 looks like a **hybrid between a market‑maker and a directional quant.**

**Layer 1: Spread Farming (same core as PBot1)**

* Places resting bids on both sides (Up and Down) slightly below mid, typically in the high‑40s.
* f both legs get filled, total cost is around **$0.95–0.96**, with a guaranteed $1 payout at settlement.
* This reproduces the classic **4–5% risk‑free spread** whenever the book gives him both fills.

This gives him a stable, casino‑style base edge: he effectively rents liquidity to everyone who uses market orders.

**Layer 2: Directional Overlays (where the quant edge appears)**

On top of the spread game, you see occasional **heavy, one‑sided bets** at much higher prices — 60–78¢ on a single direction (for example, “Up 76¢”, “Up 78¢” on BTC).

Those entries don’t make sense for a neutral market maker; they only make sense if:

* He runs a model that says “this side is massively underpriced even at 70–80% implied odds”, and
* He’s willing to stack size on top of his neutral base because the probability edge is big enough.

So the most realistic description is:

> *gabagool22 plays the* ***same 4–5% spread game*** *as PBot1 most of the time, but when his model screams “strong bias,” he stops being neutral and* ***leans hard into the favored side*** *with extra size.*

**Key idea:** gabagool22 isn’t choosing between arbitrage *or* prediction — he **layers** them:

* First, he gets paid like the house (spread farming).
* Then, when the odds are clearly wrong, he also gets paid like a sharp (directional edge).

## How to Replicate This Whale Strategy (Safely)

* **Decode & Copy:** Use the script above on top profiles — filter for high-win-rate Down biases in ranges.
* **Bot Setup:** Clawdbot or custom Python for auto-entries on 40–60% odds.
* **Size with Kelly:** Calc f\* per bet, fractional for safety.
* **Time with Guarantees:** EV checks before entry; diversify BTC/ETH.
* **Risks:** Fees (2–5%), addiction — limit sessions, 1% bankroll max.

## Conclusion & CTA

> *These three bots ($190k–$824k) succeed via high-volume, Down-biased 5-min plays, Kelly-sized bets, and EV-guaranteed timing. Decode wallets, apply math — and you could print too. But volatility reks fast; start small. Try decoding a whale on Polymarket today.*

If you are ready to trade, jump on trading now: https://polymarket.com