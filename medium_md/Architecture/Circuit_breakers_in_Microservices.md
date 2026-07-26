---
title: "Circuit breakers in Microservices"
url: https://medium.com/p/d1c3d4fee5e3
---

# Circuit breakers in Microservices

[Original](https://medium.com/p/d1c3d4fee5e3)

Member-only story

# Circuit Breakers in Microservices

## Approach to prevent cascaded failures in microservices

[![Mohit Malhotra](https://miro.medium.com/v2/resize:fill:64:64/1*9W20_hKct7Zmz4TtDhiirw.png)](https://mohit-malhotra.medium.com/?source=post_page---byline--d1c3d4fee5e3---------------------------------------)

[Mohit Malhotra](https://mohit-malhotra.medium.com/?source=post_page---byline--d1c3d4fee5e3---------------------------------------)

6 min read

·

Dec 4, 2023

--

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dd1c3d4fee5e3&operation=register&redirect=https%3A%2F%2Faws.plainenglish.io%2Fcircuit-breakers-in-microservices-d1c3d4fee5e3&source=---header_actions--d1c3d4fee5e3---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

As microservices architecture is all about having collection of multiple micro sized separately deployable services which co-ordinate together to comprise as software system. Splitting the system is into individual services is still the easier part but managing co-ordination is hell of a job.

For a resilient and highly available system, handling failures in these services gracefully without impacting the whole system is a necessity.

## What is the problem ?

Assume an **orders service** handles request from the user placing a new order. The user tries to make the payment and **orders service** communicates with **payment service** to check the status before confirming the order. Now **payment service** goes down due to lack of resources such as cpu or memory. Ideally **order services** must be running with multiple threads (or async requests) which are trying to invoke the **payment service** APIs. These **payment service** APIs takes too long to respond and hence more and more orders get stuck waiting for response and eventually it will lead to failures in **order service**.