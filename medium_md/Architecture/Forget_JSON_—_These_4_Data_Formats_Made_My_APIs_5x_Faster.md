---
title: "Forget JSON — These 4 Data Formats Made My APIs 5x Faster"
url: https://medium.com/p/a43a7b3935d6
---

# Forget JSON — These 4 Data Formats Made My APIs 5x Faster

[Original](https://medium.com/p/a43a7b3935d6)

Member-only story

# Text vs Binary: How Dropping JSON Squeezed 5x More Throughput From Our APIs

[![The Thread Whisperer](https://miro.medium.com/v2/resize:fill:64:64/1*1OJwhDGJkOyNc7-ya2TA7w.jpeg)](/@maahisoft20?source=post_page---byline--a43a7b3935d6---------------------------------------)

[The Thread Whisperer](/@maahisoft20?source=post_page---byline--a43a7b3935d6---------------------------------------)

6 min read

·

Jun 7, 2026

--

25

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Da43a7b3935d6&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40maahisoft20%2Fforget-json-these-4-data-formats-made-my-apis-5x-faster-a43a7b3935d6&source=---header_actions--a43a7b3935d6---------------------post_audio_button------------------)

Share

**I was proud of my API. Then I benchmarked it.**

Press enter or click to view image in full size

![]()

Three years of clean architecture, well-named routes, solid error handling — and my response times were quietly killing the user experience. Not because of bad logic. Not because of slow databases. Because of JSON.

It was a Monday standup. Someone from the product team pulled up a dashboard and said, “Why does this page feel so sluggish?” I had no answer.

I nodded along, said I would look into it, and spent the next three days staring at code that looked perfectly fine. The bug was not in my code. It was in my assumptions.

That weekend cost me sleep. It also changed how I think about performance forever.

**TL;DR — What This Article Covers**

JSON is slow at scale because it converts structured data into text and back on every single request. These four formats — Protobuf, MessagePack, Avro, and FlatBuffers — solve that at the wire level. Use JSON at your public edges. Use these formats everywhere machines talk to machines.

## The Problem Nobody Talks About

JSON is comfortable. It is readable. Your browser console loves it. Your teammates can open it in Notepad and understand it.