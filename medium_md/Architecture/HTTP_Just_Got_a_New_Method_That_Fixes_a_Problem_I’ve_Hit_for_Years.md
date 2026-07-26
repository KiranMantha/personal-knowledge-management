---
title: "HTTP Just Got a New Method That Fixes a Problem I’ve Hit for Years"
url: https://medium.com/p/f82909d35fb4
---

# HTTP Just Got a New Method That Fixes a Problem I’ve Hit for Years

[Original](https://medium.com/p/f82909d35fb4)

Member-only story

# HTTP Just Got a New Method That Fixes a Problem I’ve Hit for Years

## A simple look at the HTTP QUERY method and the hack it finally replaces.

[![Tushar Kanjariya](https://miro.medium.com/v2/resize:fill:64:64/2*lSBGQKdOUsG8qNMLANgd1w.jpeg)](/@TusharKanjariya?source=post_page---byline--f82909d35fb4---------------------------------------)

[Tushar Kanjariya](/@TusharKanjariya?source=post_page---byline--f82909d35fb4---------------------------------------)

6 min read

·

Jul 9, 2026

--

4

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Df82909d35fb4&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40TusharKanjariya%2Fhttp-just-got-a-new-method-that-fixes-a-problem-ive-hit-for-years-f82909d35fb4&source=---header_actions--f82909d35fb4---------------------post_audio_button------------------)

Share

For more than 25 years, sending a big search query over HTTP left me with two bad choices.

> [Read Free](/@TusharKanjariya/http-just-got-a-new-method-that-fixes-a-problem-ive-hit-for-years-f82909d35fb4?sk=7f63ed475f627cf3832c084b040c1c8b) for non-members.

Either squeeze everything into the URL and hope it doesn’t become too long.

Or send it as a POST request, even though you’re not actually creating or updating anything.

But now, that finally changed.

The IETF published **RFC 10008**. It defines a brand-new **HTTP QUERY method**.

In plain terms: a request that carries a body, like POST does, but that is still safe to retry and safe to cache, the way GET is.

But the more I read about it, the more I realized it quietly fixes one of the oldest problems I’ve run into while designing APIs.

Press enter or click to view image in full size

![HTTP QUERY Method Explained | Tushar Kanjariya]()

### What Was Actually Broken

GET is the right method for reading data. It’s safe. It’s repeatable. Every cache and CDN on the planet already knows how to handle it.

The catch? GET has no body. Everything has to go in the URL.