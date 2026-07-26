---
title: "A quick tip on testing Observables 👀"
url: https://medium.com/p/e2fbdebef4c
---

# A quick tip on testing Observables 👀

[Original](https://medium.com/p/e2fbdebef4c)

# A quick tip on testing Observables 👀

[![Angel Nikolov](https://miro.medium.com/v2/resize:fill:64:64/1*OoA1Py3NcnodY2CozQZvQQ.png)](https://medium.com/@darkysharky?source=post_page---byline--e2fbdebef4c---------------------------------------)

[Angel Nikolov](https://medium.com/@darkysharky?source=post_page---byline--e2fbdebef4c---------------------------------------)

3 min read

·

May 17, 2018

--

1

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3De2fbdebef4c&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fa-quick-tip-on-testing-observables-e2fbdebef4c&source=---header_actions--e2fbdebef4c---------------------post_audio_button------------------)

Share

Test asynchronous Observables as if they were synchronous!

Press enter or click to view image in full size

![]()

If you have worked with Angular (2+) you must have used Observables. In fact, the implementation Angular uses — RxJs is tightly incorporated in the foundations of the framework itself for stuff like Routing and Http.

If you want to learn more about Observables and how to use them, you can refer to 

[Gerard Sans](https://medium.com/u/9530b046d2ac?source=post_page---user_mention--e2fbdebef4c---------------------------------------)

’s cool post about RxJs below.

[## Angular — Introduction to Reactive Extensions (RxJS)

### How to use observable sequences in AngularJS

medium.com](https://medium.com/google-developer-experts/angular-introduction-to-reactive-extensions-rxjs-a86a7430a61f?source=post_page-----e2fbdebef4c---------------------------------------)

We all know (I hope so) that we should test our code but we also know that testing async code could be cumbersome, especially when dealing with a complex subject like Observables.

For example, we could have the following method:

Here, we return a flat array and intentionally delay it by 500ms.

How are we going to test this?

Will this work? It’s obvious that it won’t, since our test runner would not know when to execute its assertions and will just exit, **before the 500ms delay has passed.**

To solve this, we can just use the **done** callback and instruct the test runner when to execute its assertions, like:

This will work, but for some reason you don’t like it, right? It’s a bit verbose, it has nesting and an extra callback to call every time.

### Can we do it better?

Of course we can, this is Javascript, you can do anything!

I present you a simple helper function which will receive a stream (Observable) and a skipTime. It will subscribe to the observable, assign it’s value to a local variable, **skip some time** and return the value.

**Wait, what?** **You can’t do that!**How does `jasmine.clock.tick()` work?

[## How jasmine clock works?

### I don’t want to read code for hours to find the relevant part, but I am curious how jasmine implements its clock. The…

stackoverflow.com](https://stackoverflow.com/a/28889643/1841820?source=post_page-----e2fbdebef4c---------------------------------------)

It basically mocks time-based APIs with custom functions which make those calls synchronous and also let you “progress” in time by `ticking`.

You will also need to install jasmine’s clock before each test and uninstall it after, like:

Ok, but how do I use that?

Cool, huh? Synchronous, linear, easy!

You can see more use-cases in the [ngx-cacheable](https://github.com/angelnikolov/ngx-cacheable)’s **tests** [here](https://github.com/angelnikolov/ngx-cacheable/blob/master/cacheable.decorator.spec.ts). Also if you haven’t read my previous article about the simple cache decorator, please do:

[## Improve your Angular app performance by using this simple Observable cache decorator 🎉

### When we were about to finish development of our applications in SwiftViews we noticed a pattern in all our…

medium.com](https://medium.com/@darkysharky/improve-your-angular-app-performance-by-using-this-simple-observable-cache-decorator-7d7ecea470d2?source=post_page-----e2fbdebef4c---------------------------------------)

P.S In the latest versions of Angular, you can also use NgZone’s `fakeAsync` + `tick` and get the same effect. However if you use Observables in a non-Angular project you wouldn’t need the overhead of zone.js in your tests, but if you test an angular app, maybe that will be the better choice.

![]()

Looking for a remote Frontend Job?  
Get notified when one is available! Subscribe now <https://www.remotefrontendjobs.com/>