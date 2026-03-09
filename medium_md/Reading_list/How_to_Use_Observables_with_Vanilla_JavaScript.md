---
title: "How to Use Observables with Vanilla JavaScript"
url: https://medium.com/p/aca40a7590ff
---

# How to Use Observables with Vanilla JavaScript

[Original](https://medium.com/p/aca40a7590ff)

Member-only story

## TIPS AND TRICKS

# How to Use Observables with Vanilla JavaScript

## No frameworks used, just pure vanilla JavaScript.

[![Ahmed Tarek](https://miro.medium.com/v2/resize:fill:64:64/1*Z2tMj5NgKsP9oKwwN0cJ6A.png)](https://medium.com/@eng_ahmed.tarek?source=post_page---byline--aca40a7590ff---------------------------------------)

[Ahmed Tarek](https://medium.com/@eng_ahmed.tarek?source=post_page---byline--aca40a7590ff---------------------------------------)

3 min read

·

Oct 20, 2021

--

2

Listen

Share

More

Press enter or click to view image in full size

![How to Use Observables and Subjects with Vanilla JavaScript (JS) without any frameworks or libraries. Best Practice Code Coding Programming Software Development Architecture Engineering]()

While working on a side project just for fun, I wanted to write a JavaScript script to call a REST API and eventually do some cool stuff on a webpage. It is purely vanilla JavaScript, with no fancy frameworks or even libraries being used.

First, I thought of using **Promises** for my calls and this was easy for me. I have done that a ton of times. However, it then hit me hard — why don’t I use **Observables?** I knew that vanilla JavaScript didn’t natively support Observables. But couldn’t I implement it myself? And that’s what I did.

[## Subscribe to Ahmed's Newsletter?

### Subscribe to Ahmed's newsletter 📰 to get best practices, tutorials, hints, tips, and many other cool things directly…

medium.com](https://medium.com/subscribe/@eng_ahmed.tarek?source=post_page-----aca40a7590ff---------------------------------------)

## This is how I thought things through

1. The Observable itself would be of a new object type called **Subject.**
2. This **Subject** object should expose the `subscribe` and `next` functions.
3. `subscribe` should be called by observers to subscribe to the observable stream of data.
4. `next` should be called by the **Subject** owner to push/publish new data whenever available.
5. Additionally, I wanted the **Subject** owner to be able to know whenever no observers were interested in its data. This would enable the **Subject** owner to decide if he still wanted to get the data or not.
6. Also, the **Subject** owner should be able to know whenever at least one observer started being interested in its data. This would give the **Subject** owner more control on its data flow and any related operations.
7. Now back to the **observer**. He should be able to **unsubscribe** from the **Subject** at any time.
8. This leads us to a new object type called **Subscription.**
9. This **Subscription** object should expose an `unsubscribe` function.
10. `unsubscribe` should be called by the **observer** whenever he wants to stop listening to the data stream coming from the **Subject**.

Following these rules, I came up with the following implementation.

## Implementation

### Subscription

Note that **Subscription** just notifies the **Subject** when the `unsubscribe` function is called.

### Subject

### Somewhere in the Subject Owner

### Somewhere in the Observer

That’s it, everything worked like a charm and I was proud of what I achieved.

So, the punch line is that coding in vanilla JavaScript is not always equal to writing boring code, you can make it much more fun 😃

## Hope you found this content useful. If you want to support:

▶ If you are not a **Medium** member yet, you can use [**my referral link**](https://medium.com/@eng_ahmed.tarek/membership) so that I can get a part of your fees from **Medium**, you don’t pay any extra.  
▶ Subscribe to [**my Newsletter**](https://medium.com/subscribe/@eng_ahmed.tarek) to get best practices, tutorials, hints, tips and many other cool things directly to your inbox.

## Other Resources

These are other resources you might find interesting.

[## How to Set JavaScript Promise Timeout

### Just don’t wait forever for a Promise to get fulfilled, you need to set your own terms.

javascript.plainenglish.io](/how-to-set-javascript-promise-timeout-7d51c87bc38e?source=post_page-----aca40a7590ff---------------------------------------)

[## Customize Webpage UI/Behavior with JavaScript UserScripts

### Even if you don’t own the Webpage, you can still attach your JavaScript UserScripts.

javascript.plainenglish.io](/how-to-customize-webpages-ui-behavior-using-javascript-userscripts-7b6a090e0135?source=post_page-----aca40a7590ff---------------------------------------)

[## How to Get Freelancer’s New Projects Notifications on your Slack Channel

### It is a matter of setting up a UserScript, which I will provide you with.

javascript.plainenglish.io](/how-to-get-freelancers-new-projects-notifications-on-your-slack-channel-69c9c74d3220?source=post_page-----aca40a7590ff---------------------------------------)

[## Build a Twitter Auto-Retweet Bot With Node.js and TypeScript

### Learn how to create a Twitter Bot to retweet any tweets with certain keywords or hashtags

betterprogramming.pub](https://betterprogramming.pub/twitter-auto-retweet-bot-with-node-js-and-typescript-4d6eaf24c0ab?source=post_page-----aca40a7590ff---------------------------------------)

[## Paging/Partitioning — Main Equations to Make it Easy

### Finally, this is your chance to understand paging/partitioning main equations and learn how to apply them in code.

levelup.gitconnected.com](https://levelup.gitconnected.com/paging-partitioning-main-equations-to-make-it-easy-44fe89d5290b?source=post_page-----aca40a7590ff---------------------------------------)

Hope you found reading this story as interesting as I found writing it.

*More content at* [***plainenglish.io***](http://plainenglish.io/)

*This article is also published on* [***Development Simply Put****.*](https://www.developmentsimplyput.com/post/how-to-use-observables-with-vanilla-javascript)