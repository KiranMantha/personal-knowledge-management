---
title: "Different ways to achieve encapsulation in JavaScript(ES6)"
url: https://medium.com/p/7cb938e83f2d
---

# Different ways to achieve encapsulation in JavaScript(ES6)

[Original](https://medium.com/p/7cb938e83f2d)

Member-only story

# Different ways to achieve encapsulation in JavaScript(ES6)

[![Iskander Samatov](https://miro.medium.com/v2/resize:fill:64:64/1*b_AR3kXt15EEVWqdIyOk8g.jpeg)](https://iskenxan.medium.com/?source=post_page---byline--7cb938e83f2d---------------------------------------)

[Iskander Samatov](https://iskenxan.medium.com/?source=post_page---byline--7cb938e83f2d---------------------------------------)

4 min read

·

May 18, 2019

--

7

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D7cb938e83f2d&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fdifferent-ways-to-achieve-encapsulation-in-javascript-es6-7cb938e83f2d&source=---header_actions--7cb938e83f2d---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

JavaScript is a powerful language full of different paradigms that let you write interesting and flexible code. However, at the same time it lacks some of the basic structural features the other languages have. By far one of the biggest anomalies of JavaScript is it’s inability to natively support encapsulation.

The scoping system was introduced with TypeScript, which is a superset of JavaScript. But unfortunately its not a clear victory yet since, while it does give you a warning, TypeScript code still compiles and runs even when you access the private variables.

Nevertheless, people came up with ways to achieve encapsulation using other features of the language. And in this post I’m going over the most widely used ones.

## Easy way

The easiest way to achieve pseudo-encapsulation would be to prefix your private member with a special symbol that indicates the private scope to the client. It is a common convention to use the `_` symbol as a prefix. Of course this won't actually prevent anyone from accessing your private variables so we won't go in too much detail here.

## Factory functions and closures

Simply put, factory functions are functions used to create new instances of the object. Factory…