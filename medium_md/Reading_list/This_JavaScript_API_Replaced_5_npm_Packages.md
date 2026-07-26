---
title: "This JavaScript API Replaced 5 npm Packages"
url: https://medium.com/p/ecbd8c2e62f3
---

# This JavaScript API Replaced 5 npm Packages

[Original](https://medium.com/p/ecbd8c2e62f3)

Member-only story

# This JavaScript API Replaced 5 npm Packages

## Most developers already have it installed.

[![Tushar Kanjariya](https://miro.medium.com/v2/resize:fill:64:64/2*lSBGQKdOUsG8qNMLANgd1w.jpeg)](/@TusharKanjariya?source=post_page---byline--ecbd8c2e62f3---------------------------------------)

[Tushar Kanjariya](/@TusharKanjariya?source=post_page---byline--ecbd8c2e62f3---------------------------------------)

6 min read

·

May 13, 2026

--

5

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Decbd8c2e62f3&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40TusharKanjariya%2Fthis-javascript-api-replaced-5-npm-packages-ecbd8c2e62f3&source=---header_actions--ecbd8c2e62f3---------------------post_audio_button------------------)

Share

I used to install a formatting library in almost every JavaScript project.

> [Read Free](/@TusharKanjariya/this-javascript-api-replaced-5-npm-packages-ecbd8c2e62f3?sk=6874b209c65abfa20450c0c3e7e661b6) for non-members.

Dates? Install moment.js.

Relative time? Install date-fns.

Currencies and commas? Install numeral.js.

I added moment.js to a project last year.

It was around 73KB. For one date format.

I didn’t know the JavaScript Intl API existed. And I’d been writing JavaScript for years.

The JavaScript Intl API is a zero-dependency, fully browser-native internationalization engine built into every modern browser and Node.js runtime.

It formats dates, times, relative time (“3 days ago”), numbers, currencies, and lists without a single npm install.

Most developers are still reaching for moment.js, date-fns, or numeral.js to do things JavaScript can already do natively.

Here’s what it actually covers.

Press enter or click to view image in full size

![]()

### What Is the JavaScript Intl API, Exactly?

`Intl` is a global object (built-in JavaScript object for internationalization). It’s been in browsers since 2012 and has…