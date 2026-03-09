---
title: "Reactive Web Design: The secret to building web apps that feel amazing"
url: https://medium.com/p/b5cbfe9b7c50
---

# Reactive Web Design: The secret to building web apps that feel amazing

[Original](https://medium.com/p/b5cbfe9b7c50)

# Reactive Web Design: The secret to building web apps that feel amazing

[![Owen Campbell-Moore](https://miro.medium.com/v2/resize:fill:64:64/1*xAZlL1PB1ygB78Ni0DRA9w.jpeg)](/@owencm?source=post_page---byline--b5cbfe9b7c50---------------------------------------)

[Owen Campbell-Moore](/@owencm?source=post_page---byline--b5cbfe9b7c50---------------------------------------)

5 min read

·

Apr 3, 2017

--

13

Listen

Share

More

In the last year I’ve observed **two subtle techniques** being used by some developers that take a web app from feeling slow and janky to highly reactive and polished.

I believe these techniques are important enough that they need a name: **Reactive Web Design**.

In summary, reactive web design is a set of techniques that can be used to build sites that always feel fast and responsive to user input regardless of the network speed or latency.

As web developers and framework authors, I believe finding ways to make these patterns default in everything we build is a top priority for improving UX and perceived performance on the web.

## Technique 1: Instant loads with skeleton screens

When used well, this technique is almost never noticed, but has a huge impact on perceived performance of a site.

Interestingly, the technique is used by almost all native apps and makes them feel very reactive even on terrible networks, but it is almost never used on the web!

*Opportunity this way lies!*💡

In short, skeleton screens ensure that whenever the user taps any button or link, the page reacts immediately by transitioning the user to that new page and then *loading in content to that page* as the content becomes available.

![]()

Skeleton screens are a key *perceived performance* technique as they make applications *feel* much faster, dramatically reducing the number of moments where the user is left wondering:

> What is going on? Is it even loading? Did I tap it right? *🤔*

[Flipkart.com](http://www.flipkart.com) is a rare example of a website that makes use of this approach. Browsing through categories or tapping on products therefore feels lightning fast, even when the actual results take a few seconds to load:

![]()

When this technique is used best, content that is already available such as thumbnails or article titles can be re-used to improve the perceived performance even further, making loads feel truly instant.

![]()

### Testing sites with skeleton screens

Testing how well sites use this technique is easy: simply use Chrome network emulation to make the network as slow as possible and then click around a site. If it is doing this well, the site will still feel snappy and responsive to your input.

![]()

## Technique 2: “Stable loads” via predefined sizes on elements

You know that feeling where a website is jumping around while you’re trying to use it? You’re just trying to read an article and the text keeps moving around? That’s what we call an “unstable load”, and we need to ***burn it with fire*** 🔥🔥🔥.

![]()

Unstable loads make websites hard to interact with, and makes them feel… well… *Unstable!*

![]()

Unstable loads are caused by images and ads embedded into a page but not including any sizing information. By default the browser only knows the size of these once they have loaded, so as soon as an image loads in, **THUNK!**,the whole page slides down 😡.

To prevent this, all <img> tags on a page must proactively include the dimensions of the image they will contain.

In many cases images used on certain pages are always the same size and so their size can simply be included in the HTML template, but in some cases the size of images is dynamic and thus their size should be calculated when the image is uploaded then templated into the HTML when it is created.

```
<!-- Always include sizes on images to prevent unstable loads -->  
<img src='/thumbnail.png' style='width: 100px; height: 84px'>
```

The same is true for ads, often a culprit when it comes to unstable loads. Wherever possible, create a div that will contain an ad, and in your templating set it to be sized with your best guess at how big this ad will be.

Note that unstable loads are at their worst on slow networks as you have just settled into reading content when suddenly it jumps, and you can *never quite be sure that you’re safe*.

## Putting it all together

I’ve build a small demo site at [reactive.surge.sh](http://reactive.surge.sh) to demonstrate the difference between conventional and reactive web design.

### Conventional article loading

![]()

### Loading an article with reactive web design

![]()

## Wrapping up

The slower the network is, the worse the user experience becomes when page transitions block on the network and pages jump around for extended periods.

With **Reactive Web Design** we can make our experience feel snappy and responsive (“Responsive Design” as a name was already taken, d’oh!) even on slow and painful networks.

I’d love to hear about data from the community on the effect of perceived performance on KPIs such as engagement and revenue!

Additionally, I’d encourage framework and library authors to consider how to make skeleton screens and stable loads the default, also known as the [*pit of success*](https://blog.codinghorror.com/falling-into-the-pit-of-success/)*.*

If you have thoughts about this, please tweet me [@owencm](https://twitter.com/owencm), and if you enjoyed this please give it a ♥!

*P.S. be sure to check out the demo site* [*reactive.surge.sh*](http://reactive.surge.sh) *on a mobile device for it’s full glory!*