---
title: "Avoid ugly If/else blocks & make your code modular with Strategy"
url: https://medium.com/p/1c3364b2f920
---

# Avoid ugly If/else blocks & make your code modular with Strategy

[Original](https://medium.com/p/1c3364b2f920)

Member-only story

# Avoid ugly If/else blocks & make your code modular with Strategy

[![Iskander Samatov](https://miro.medium.com/v2/resize:fill:64:64/1*b_AR3kXt15EEVWqdIyOk8g.jpeg)](https://iskenxan.medium.com/?source=post_page---byline--1c3364b2f920---------------------------------------)

[Iskander Samatov](https://iskenxan.medium.com/?source=post_page---byline--1c3364b2f920---------------------------------------)

4 min read

·

Apr 21, 2019

--

11

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D1c3364b2f920&operation=register&redirect=https%3A%2F%2Fitnext.io%2Favoid-ugly-if-else-blocks-make-your-code-modular-with-strategy-1c3364b2f920&source=---header_actions--1c3364b2f920---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

New ES6 syntax is aimed at making our code more concise and clear. And it successfully accomplishes that goal: things like destructuring, string literals, spread operators, and etc. are all great tools for improving our code readability.

### Ugly if/else

One particular piece of syntax that is unlikely to ever change is if/else and switch statements. I don’t know about you, but I always found them to be the ugliest part of my code. However, it’s a terribly necessary evil that is impossible to avoid.

In business applications we almost always face a situation where we have to implement some kind of routing method that performs a variation of the certain action based on the condition. These methods usually end up having long and ugly if/else or switch statements. *(Payment options, email routing, multiple authentication providers, and etc.)*

In this post I want to share with you a pattern that I learned about recently myself and which I think can help you avoid some of those scenarios.

## Strategy

The pattern that I am talking about is called Strategy. This pattern was popularized by GoF ( [Gang of Four](https://en.wikipedia.org/wiki/Design_Patterns)) and is a great tool for adding mutable, interchangeable parts to certain pieces of your application logic.