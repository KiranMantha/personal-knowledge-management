---
title: "System Design Interview: How Would You Send 1 Million Notifications Without Overwhelming Your…"
url: https://medium.com/p/5a59b723127d
---

# System Design Interview: How Would You Send 1 Million Notifications Without Overwhelming Your…

[Original](https://medium.com/p/5a59b723127d)

Member-only story

# System Design Interview: How Would You Send 1 Million Notifications Without Overwhelming Your Servers?

[![Arvind Kumar](https://miro.medium.com/v2/resize:fill:64:64/1*qLgT62h04Vn1WA1vdYL9lg.png)](/?source=post_page---byline--5a59b723127d---------------------------------------)

[Arvind Kumar](/?source=post_page---byline--5a59b723127d---------------------------------------)

6 min read

·

Jun 20, 2026

--

31

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D5a59b723127d&operation=register&redirect=https%3A%2F%2Fcodefarm0.medium.com%2Fsystem-design-interview-how-would-you-send-1-million-notifications-without-overwhelming-your-5a59b723127d&source=---header_actions--5a59b723127d---------------------post_audio_button------------------)

Share

It’s Black Friday.

Your marketing team has prepared a promotional campaign.

At exactly midnight, they want to notify 1 million users.

The request sounds simple.

Until you realize that sending 1 million notifications instantly can overwhelm your application servers, notification providers, databases, and even downstream APIs.

Most engineers immediately say:

> *“Use Kafka.”*

That’s a good starting point.

But what happens when:

* Kafka consumers can’t keep up?
* Firebase rate limits you?
* A worker crashes halfway through processing?
* Notifications must be personalized?
* One campaign targets 100 million users instead of 1 million?
* Marketing suddenly wants delivery status tracking?

Let’s walk through a system design interview where those questions get explored.

> [Full story for non-members](/5a59b723127d?sk=8b603c93e9755d4bef83977ea7143469) | [E-Books on Java/Microservices/Springboot](https://codefarm.in/ebooks) | [Whatsapp Group](https://www.whatsapp.com/channel/0029VbBoxXI5q08aIWZsUE2X)

Press enter or click to view image in full size

![]()

> Watch short explanation video on…