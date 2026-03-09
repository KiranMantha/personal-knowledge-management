---
title: "How to Build a Double-Entry Ledger"
url: https://medium.com/p/f69edcea825d
---

# How to Build a Double-Entry Ledger

[Original](https://medium.com/p/f69edcea825d)

# Double-Entry Bookkeeping in Ledger Systems

[![Fatih Altuntaş](https://miro.medium.com/v2/resize:fill:64:64/1*Q73lkga_ozOBocu7SLVPnA.jpeg)](/@altuntasfatih42?source=post_page---byline--f69edcea825d---------------------------------------)

[Fatih Altuntaş](/@altuntasfatih42?source=post_page---byline--f69edcea825d---------------------------------------)

6 min read

·

Sep 17, 2025

--

2

Listen

Share

More

Press enter or click to view image in full size

![]()

While migrating our ledger from **PostgreSQL** to [**TigerBeetle**](https://tigerbeetle.com/), I had to **fully understand double-entry bookkeeping** — since our entire ledger system relies on it.

Most resources I found were too abstract or academic, so I wrote this post with real-world cases and implementation-ready ideas.

Let’s quickly cover the key definitions before jumping into real case.

## What is Ledger ?

A ledger is a record-keeping system that tracks all financial transactions within a platform.It’s not just a balance table — it tracks how money moves, not just how much is there.

> *Think of it as the brain of your financial system.*

Ledger ≠ Balance Table

A **balance table** just shows current values. But a **ledger** shows **how** you got there.

## 📚 What Is Double-Entry Bookkeeping?

At its core, **double-entry bookkeeping** is an accounting method where **every transaction affects at least two accounts**:

➡️ One account is **debited**, and  
➡️ Another account is **credited**.

To maintain consistency, the **total value of debits must always equal the total value of credits so equation is following:**

**sum(debits) = sum(credits)**

> Think of it like this: *Money never just appears or disappears — it always* ***moves from one account to another****.*

For example, if a user deposits $100 into your platform, that money comes **from** the external cash account and **goes into** the user’s balance account — one is debited, the other is credited.

**Why it matters:**

* ✅ **Balanced** — every inflow has an outflow
* 🔍 **Traceable** — audit every transaction path
* 🔐 **Secure** — catches inconsistencies or unauthorized edits

Every transaction is recorded as a **two-sided journal entry** — the foundation of reliable financial software used by banks, wallets, and gaming platforms.

## 🎯 Real Business Case

Let’s say we’re building a ledger system for a iGaming platform. Customers can:

* **Deposit** → Top up money to system for playing
* **Withdraw** → Transfer money back to their bank
* **Bet** → Lock money in a game
* **Win** → Receive winnings

Each action is recorded as a double-entry transaction: every event affects two internal accounts through a **debit** and **credit** entry.

## 📊 What Are Assets, Liabilities, and Equity?

These are the **three core building blocks** of any accounting system — including your ledger.

Every account in your system must be categorized as **one of these types**, and this classification helps maintain the integrity and logic of the ledger.

### Assets : What the platform owns

Things the company controls that have value which could **that provide future economic benefit**.  
In our iGaming platform , this includes:

* Cash received from users (held in bank or PSP)

Assets are **debit-positive** accounts.

* ➕ **To increase** an asset, you **debit** it
* ➖ **To decrease** an asset, you **credit** it

### Liabilities– What the Platform Owes

Liabilities are **obligations to others** — typically, user balances that can be withdrawn or used for bets.

**Examples:**

* What you owe to each user (their available wallet balance,could be bonus which given to customer)
* Locked funds from active bets

In the context of a ledger system, liabilities are the **credit-positive** accounts:

* ➕ **To increase a liability**, you **credit** it  
  (e.g. when a user deposits or wins money)
* ➖ **To decrease a liability**, you **debit** it  
  (e.g. when a user withdraws, loses a bet)

### What Is Equity?

**Equity** represents the platform’s **net value** — what the business **keeps or earns** after subtracting all liabilities from its assets.

> *📐* ***Formula:****Equity = Assets — Liabilities*

Examples:

* Profits from game spreads, commissions, or service fees
* Starting capital injected into the system at initialization.

Equity accounts are **credit-positive**, just like liabilities.

* ➕ **To increase equity** (e.g. revenue, commission), you **credit** the account
* ➖ **To decrease equity** (e.g. refund, loss, bonus cost and), you **debit** the account

> *Think of “****Debit****” and “****Credit****” not as good/bad or plus/minus — they always depend on account type.It is kinda trick*

## 🏗️ Ledger Design

*N*ow that the basics are clear, let’s build the actual ledger.Each account must be classified as either an **Asset**, **Liability**, or **Equity**.

We’ll define internal account types that handle all user and system transactions.Here’s how I structured them:

Press enter or click to view image in full size

![]()

> *⚠️In production systems, accounts are typically split by* ***currency*** *(e.g., USD, EUR). We’ll simplify by using just dollars ($) in this example.*

## Lets start

Now that we’ve defined our account types and operations, let’s build the ledger from scratch.

I’ll walk through a complete scenario — from capital injection to multiple users depositing, betting, winning, and withdrawing — to cover all key cases.

**Operation 1:**10.000 $ capital injection via bank, To record this transaction in the ledger, we create the following entries:

* **Debit** cash:external10,000(asset *↑ — cash received*)
* **Credit** system-1:capital 50(equity *↑ — injected money*)

Press enter or click to view image in full size

![]()

This reflects the platform receiving real cash (increasing assets) and recognizing it as capital funding (increasing equity).The ledger remains balanced.

**Operation 2:**User-1 deposit to system 50$ to play games so transaction compose of following entries:

* **Debit** cash:external50(asset *↑ — cash received*)
* **Credit** user-1:balance 50(liability *↑ — amount owned to user*)

Press enter or click to view image in full size

![]()

Platform receives cash and now owes $50 to the user.

**Operation 3:**  
User-2 deposit to system 30$ to play games, so transaction compose of following entries:

* **Debit** cash:external30(asset *↑ — cash received*)
* **Credit** user-2:balance 30(liability *↑ — amount owned to user*)

Press enter or click to view image in full size

![]()

**Operation 4:**User-1 places a 10$ bet on game-90, so transaction compose of following entries:

* **Debit** user-1:balance10(liability *↓ — reduce user’s available game*)
* **Credit** game-90:bet\_pool 10 (liability *↑ — hold the stake for the game*)

Press enter or click to view image in full size

![]()

This records the $10 being moved from the user’s balance to the internal game pool. The platform now holds the funds, but hasn’t earned them yet.

* The platform doesn’t owe the $10 to the user anymore
* But it hasn’t earned it as revenue either

Depending on the outcome:

* If the user **loses**, the amount is recognized as **revenue**
* If the user **wins**, it’s **refunded**, or a larger payout is made

**Operation 5:**User-1 Bet resolved, platform earn $10 which move from game pool to platform revenue with following entries:

* **Debit** game-90:bet\_pool 10(liability *↓ — release the held bet* )
* **Credit** system:revenue 10(equity *↑ — earn the revenue*)

Press enter or click to view image in full size

![]()

**Operation 6:**User-2 places a 30$ bet on game-80, so transaction compose of following entries:

* **Debit** user-2:balance30(liability *↓ — reduce user’s available game*)
* **Credit** game-80:bet\_pool 30 (liability *↑ — hold the stake for the game*)

Press enter or click to view image in full size

![]()

**Operation 7:**User-2’s bet on game-80 is resolved — they win $90. Refund the $30 stake and add $60 winnings to their balance. The transaction is composed of the following entries:

* **Debit** game-80:bet\_pool 30 *(liability ↓ — release the held bet)*
* **Debit** system:revenue 60 *(equity ↓ — payout cost)*
* **Credit** user-2:balance 30 *(liability ↑ — refund stake)*
* **Credit** user-2:balance 60 *(liability ↑ — winnings)*

Press enter or click to view image in full size

![]()

Although **system:revenue** is negative, the overall equity remains positive due to the **system:capital** account.

**Operation 8:**User-2 withdraws 90$ and so transaction compose of followings entries:

* **Debit** user-2:balance 60 *(liability ↓ —reduce amount owned)*
* **Credit** cash:external 30 *(asset ↓ — cash leaves the platform)*

Press enter or click to view image in full size

![]()

This pays out $90 and clears User-2’s liability balance.

## Summary

This article explained **double-entry bookkeeping** using a real iGaming example. We walked through assets, liabilities, and equity — and modeled key operations like deposits, bets, wins, and withdrawals with clear journal entries.

## What’s Next

In the next story, i will implement this model using [**TigerBeetle**](https://tigerbeetle.com/)databasein **Elixir**.