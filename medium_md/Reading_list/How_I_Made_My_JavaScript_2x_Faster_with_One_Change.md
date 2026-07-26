---
title: "How I Made My JavaScript 2x Faster with One Change"
url: https://medium.com/p/d31a4a68ef67
---

# How I Made My JavaScript 2x Faster with One Change

[Original](https://medium.com/p/d31a4a68ef67)

Member-only story

# How I Made My JavaScript 2x Faster with One Change

[![Julia S](https://miro.medium.com/v2/resize:fill:64:64/1*Kfor2VjeoRT2-lfqPsmF8Q.png)](https://medium.com/@julias3?source=post_page---byline--d31a4a68ef67---------------------------------------)

[Julia S](https://medium.com/@julias3?source=post_page---byline--d31a4a68ef67---------------------------------------)

5 min read

·

Oct 11, 2025

--

4

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dd31a4a68ef67&operation=register&redirect=https%3A%2F%2Fjavascript.plainenglish.io%2Fhow-i-made-my-javascript-2x-faster-with-one-change-d31a4a68ef67&source=---header_actions--d31a4a68ef67---------------------post_audio_button------------------)

Share

## The one tweak that finally stopped my app from feeling like it was running through molasses

I’ll be honest — I used to think my JavaScript was *fine*. My app worked. The features shipped. The users weren’t *screaming*. That’s good enough, right?

> Wrong.

One day, while testing a new feature, I noticed something weird — a button click was lagging. Just by a fraction of a second. But that tiny delay was enough to make everything *feel* sluggish.

You know that “ugh” moment when a web app doesn’t respond immediately, and you click again thinking maybe you missed the button? Yeah, that.

So, I opened DevTools, expecting to find the usual suspects: too many network requests, a runaway interval, or some forgotten console logs clogging the arteries. But no.

The CPU profile pointed straight at my own code. My beautiful, “clean” JavaScript was the problem.

After hours of profiling, testing, and a few existential sighs, I made **one change** that made my code nearly *twice as fast*.

And it wasn’t caching, it wasn’t lazy loading, and it definitely wasn’t some obscure optimization from a Reddit thread.

> It was this:  
>  👉 **I stopped using** `Array.map()` **inside performance-critical loops.**

> Let me explain why that one tweak changed everything.