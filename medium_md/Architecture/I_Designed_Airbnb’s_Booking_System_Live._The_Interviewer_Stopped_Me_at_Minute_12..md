---
title: "I Designed Airbnb’s Booking System Live. The Interviewer Stopped Me at Minute 12."
url: https://medium.com/p/1b3228fb6c50
---

# I Designed Airbnb’s Booking System Live. The Interviewer Stopped Me at Minute 12.

[Original](https://medium.com/p/1b3228fb6c50)

Member-only story

# I Designed Airbnb’s Booking System Live. The Interviewer Stopped Me at Minute 12.

## *Not because I was wrong. Because I’d already answered the real question.*

[![The Speedcraft Lab](https://miro.medium.com/v2/resize:fill:64:64/1*Dm71ADP4pd4tz73U0uKtVw.png)](/@speedcraft21?source=post_page---byline--1b3228fb6c50---------------------------------------)

[The Speedcraft Lab](/@speedcraft21?source=post_page---byline--1b3228fb6c50---------------------------------------)

5 min read

·

Apr 27, 2026

--

7

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D1b3228fb6c50&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fbeyond-localhost%2Fi-designed-airbnbs-booking-system-live-the-interviewer-stopped-me-at-minute-12-1b3228fb6c50&source=---header_actions--1b3228fb6c50---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

## The two guests problem

Two guests. Same listing. Same dates. Their fingers hit the book button at the same instant. One booking succeeds. The other fails cleanly with “no longer available.” The guest sees a clear error, not a charged card and an empty calendar.

That outcome looks simple from the outside. It is not simple. It is the entire booking problem compressed into one moment, and the answer is not what most engineers reach for first.

## What most engineers reach for

The first instinct is sound and common. Open a transaction, lock the listing’s calendar row, check whether the requested dates are free, insert a booking row, commit. The database guarantees that two transactions cannot both succeed against the same row. Problem solved.

It works on paper. It works in a single region against a single database. It starts to crack the moment you add the things that real systems have. Network retries from flaky mobile clients. Global users hitting nearest regions. Background jobs writing to the same row. Wait. If the network just…