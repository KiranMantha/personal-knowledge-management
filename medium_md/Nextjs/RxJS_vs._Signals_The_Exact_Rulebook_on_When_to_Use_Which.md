---
title: "RxJS vs. Signals: The Exact Rulebook on When to Use Which"
url: https://medium.com/p/dac9dd4196d9
---

# RxJS vs. Signals: The Exact Rulebook on When to Use Which

[Original](https://medium.com/p/dac9dd4196d9)

Member-only story

Featured

# RxJS vs. Signals: The Exact Rulebook on When to Use Which

## Signals did not kill RxJS. They just fired it from the wrong job. Here is the definitive architectural guide on how to mix synchronous state with asynchronous streams.

[![CodePulse](https://miro.medium.com/v2/resize:fill:64:64/1*-m88m64nDyJ3ZdciwOuzgg.png)](https://ganeshlawand2002.medium.com/?source=post_page---byline--dac9dd4196d9---------------------------------------)

[CodePulse](https://ganeshlawand2002.medium.com/?source=post_page---byline--dac9dd4196d9---------------------------------------)

4 min read

·

Mar 17, 2026

--

1

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Ddac9dd4196d9&operation=register&redirect=https%3A%2F%2Fjavascript.plainenglish.io%2Frxjs-vs-signals-the-exact-rulebook-on-when-to-use-which-dac9dd4196d9&source=---header_actions--dac9dd4196d9---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

The Angular community was divided at the time of the announcement of Signals. There were some members who rejoiced in what they perceived to be the demise of RxJS; however, others were fearful of having to rewrite their entire codebase. Both of these sentiments were misguided.

The point is this: RxJS was never intended for use as a library for managing state. We have been forcing it into this role since it has been the only reactive primitive in Angular for several years. We have abused the use of BehaviorSubject to store different primitive types such as strings or booleans, resulting in an ugly mess of subscriptions, memory leaks, and the dreaded ExpressionChangedAfterItHasBeenCheckedError.

Signals solve the issue of managing state while RxJS remains king of handling asynchronous events. To build a modern Angular app (without Zones) you must stop thinking of them as competitors and think of them as a pipeline instead.