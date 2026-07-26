---
title: "JavaScript Symbols, Iterators, Generators, Async/Await, and Async Iterators — All Explained Simply"
url: https://medium.com/p/4003d7bbed32
---

# JavaScript Symbols, Iterators, Generators, Async/Await, and Async Iterators — All Explained Simply

[Original](https://medium.com/p/4003d7bbed32)

Member-only story

# JavaScript Symbols, Iterators, Generators, Async/Await, and Async Iterators — All Explained Simply

[![rajaraodv](https://miro.medium.com/v2/resize:fill:64:64/1*HIuWP_7gy9QvnssCalFT4g.png)](/?source=post_page---byline--4003d7bbed32---------------------------------------)

[rajaraodv](/?source=post_page---byline--4003d7bbed32---------------------------------------)

14 min read

·

May 11, 2018

--

67

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D4003d7bbed32&operation=register&redirect=https%3A%2F%2Frajaraodv.medium.com%2Fsome-of-javascripts-most-useful-features-can-be-tricky-let-me-explain-them-4003d7bbed32&source=---header_actions--4003d7bbed32---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

Some JavaScript (ECMAScript) features are easier to understand than others. `Generators` look weird — like pointers in C/C++. `Symbols` manage to look like both primitives and objects at the same time.

**These features are all inter-related and build on each other. So you can’t understand one thing without understanding the other.**

So in this article, I’ll cover `symbols`,`global symbols`,`iterators`, `iterables`, `generators` , `async/await` and `async iterators`. **I’ll explain “*why*” they are there in the first place and also show how they work with some useful examples.**

> This is relatively advanced subject, but it’s not rocket science. This article should give you a very good grasp of all these concepts.

**OK, let’s get started.🚀**

Press enter or click to view image in full size

![]()

## Symbols

In ES2015, a new (6th) datatype called `symbol` was created.

### WHY?

The three main reasons were:

### Reason #1 — Add new core-features with backward compatibility