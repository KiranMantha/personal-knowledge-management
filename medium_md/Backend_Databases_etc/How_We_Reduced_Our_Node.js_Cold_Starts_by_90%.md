---
title: "How We Reduced Our Node.js Cold Starts by 90%"
url: https://medium.com/p/145c73db7d9c
---

# How We Reduced Our Node.js Cold Starts by 90%

[Original](https://medium.com/p/145c73db7d9c)

Member-only story

# How We Reduced Our Node.js Cold Starts by 90%

[![Sachin Kasana](https://miro.medium.com/v2/resize:fill:64:64/1*IKlnY-B9CALn6-rfjTXFHQ.jpeg)](/@sachinkasana?source=post_page---byline--145c73db7d9c---------------------------------------)

[Sachin Kasana](/@sachinkasana?source=post_page---byline--145c73db7d9c---------------------------------------)

4 min read

·

May 28, 2026

--

2

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D145c73db7d9c&operation=register&redirect=https%3A%2F%2Fmedium.com%2Ffront-end-world%2Fhow-we-reduced-our-node-js-cold-starts-by-90-145c73db7d9c&source=---header_actions--145c73db7d9c---------------------post_audio_button------------------)

Share

Our Node.js APIs were fast.

Until they weren’t.

Everything looked fine during steady traffic, but after a few minutes of inactivity, the next request would suddenly take 2–3 seconds.  
[**non members can read here**](https://sachinkasana.medium.com/how-we-reduced-our-node-js-cold-starts-by-90-145c73db7d9c?sk=a52bcf98a57b1563a36b562ed0abc611)

The problem wasn’t the database.

It wasn’t the network either.

It was cold starts.

Press enter or click to view image in full size

![]()

And after profiling startup traces and analyzing dependency graphs, we realized something important:

> *Most cold start problems are architecture problems disguised as infrastructure problems.*

After simplifying our runtime, reducing dependencies, and changing how the app initialized, we reduced cold starts by nearly 90%.

Here’s exactly what worked.

## What Is a Cold Start?

A cold start happens when your application boots from scratch before serving a request.

This usually happens in:

* serverless functions
* autoscaled containers
* edge runtimes
* suspended microservices

Before handling the first request, Node.js must: