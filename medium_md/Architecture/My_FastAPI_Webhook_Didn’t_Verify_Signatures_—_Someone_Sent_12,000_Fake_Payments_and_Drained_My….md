---
title: "My FastAPI Webhook Didn’t Verify Signatures — Someone Sent 12,000 Fake Payments and Drained My…"
url: https://medium.com/p/889bdc33aee7
---

# My FastAPI Webhook Didn’t Verify Signatures — Someone Sent 12,000 Fake Payments and Drained My…

[Original](https://medium.com/p/889bdc33aee7)

Member-only story

# My FastAPI Webhook Didn’t Verify Signatures — Someone Sent 12,000 Fake Payments and Drained My Stripe Balance

[![Ramesh Kannan s](https://miro.medium.com/v2/resize:fill:64:64/1*JssWCulJ2QjIZrxszJns-Q.jpeg)](/@rameshkannanyt0078?source=post_page---byline--889bdc33aee7---------------------------------------)

[Ramesh Kannan s](/@rameshkannanyt0078?source=post_page---byline--889bdc33aee7---------------------------------------)

8 min read

·

Jun 28, 2026

--

7

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D889bdc33aee7&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40rameshkannanyt0078%2Fmy-fastapi-webhook-didnt-verify-signatures-someone-sent-12-000-fake-payments-and-drained-my-889bdc33aee7&source=---header_actions--889bdc33aee7---------------------post_audio_button------------------)

Share

I woke up to an email from Stripe that made my stomach drop.

*“Your account has been flagged for unusual activity. 12,473 successful charges in 6 hours. Total volume: $847,000. Please review your dashboard immediately.”*

I had not made 12,000 charges. I had not made 12 charges. My app was a small SaaS with 200 paying customers. Monthly recurring revenue of about $8,000. I was not even close to $847,000 in lifetime volume, let alone in 6 hours.

I opened the Stripe dashboard. The charges were real. Real Stripe charge objects. Real payment intents. Real successful status. But they were not from my customers. They were from a webhook. A webhook I built. A webhook I thought was secure.

Someone had sent 12,000 fake payment events to my FastAPI endpoint. My app believed every single one. It upgraded phantom accounts to premium. It sent welcome emails to nonexistent users. It triggered affiliate payouts for fake referrals. And because I had connected Stripe to my bank account for automatic payouts, $47,000 of real money had already left Stripe and hit my bank account.

The money was not mine. But it was in my account. And Stripe wanted it back.

Here is how a single missing line of code nearly destroyed my business.

## The Webhook That Looked Fine