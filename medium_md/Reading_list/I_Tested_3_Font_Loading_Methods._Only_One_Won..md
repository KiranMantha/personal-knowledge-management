---
title: "I Tested 3 Font Loading Methods. Only One Won."
url: https://medium.com/p/6f3486a8c763
---

# I Tested 3 Font Loading Methods. Only One Won.

[Original](https://medium.com/p/6f3486a8c763)

Member-only story

# I Tested 3 Font Loading Methods. Only One Won.

## The fastest one wasn’t what I expected

[![Tushar Kanjariya](https://miro.medium.com/v2/resize:fill:64:64/2*lSBGQKdOUsG8qNMLANgd1w.jpeg)](/@TusharKanjariya?source=post_page---byline--6f3486a8c763---------------------------------------)

[Tushar Kanjariya](/@TusharKanjariya?source=post_page---byline--6f3486a8c763---------------------------------------)

6 min read

·

Apr 27, 2026

--

3

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D6f3486a8c763&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40TusharKanjariya%2Fi-tested-3-font-loading-methods-only-one-won-6f3486a8c763&source=---header_actions--6f3486a8c763---------------------post_audio_button------------------)

Share

My Largest Contentful Paint (LCP) dropped by **400ms**.

I didn’t buy a faster server. I didn’t change my JavaScript framework. I didn’t even touch my images.

> [Read free](/@TusharKanjariya/i-tested-3-font-loading-methods-only-one-won-6f3486a8c763?sk=fe85866daca6f04d6ae13e35742beb24) for non-members.

I changed one thing: **how I loaded fonts**.

Press enter or click to view image in full size

![I Tested 3 Font Loading Methods. Only One Won. | Tushar Kanjariya]()

### Why Your Fonts Are Slowing You Down (More Than You Think)

Most developers never think twice about fonts.

You pick one from Google Fonts, paste the two `<link>` tags into your `<head>`, and move on. It takes 30 seconds and it works.

But “works” and “performs” are very different things.

Web font loading performance is one of the most overlooked contributors to slow LCP scores and I say that because I missed it for two years on a project I was actively optimizing.

**For Example:**Let’s say your page has a hero heading in a custom font, a paragraph below it, and a nav bar at the top.

Here’s what actually happens when Google Fonts CDN loads that font:

1. Browser parses your HTML
2. Browser finds your Google Fonts `<link>` tag