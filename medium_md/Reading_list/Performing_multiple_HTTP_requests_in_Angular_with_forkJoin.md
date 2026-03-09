---
title: "Performing multiple HTTP requests in Angular with forkJoin"
url: https://medium.com/p/74f3ac166d61
---

# Performing multiple HTTP requests in Angular with forkJoin

[Original](https://medium.com/p/74f3ac166d61)

# Performing multiple HTTP requests in Angular with forkJoin

[![Swarna](https://miro.medium.com/v2/resize:fill:64:64/0*XJbKX7LMZCWcHjCJ.jpg)](/@swarnakishore?source=post_page---byline--74f3ac166d61---------------------------------------)

[Swarna](/@swarnakishore?source=post_page---byline--74f3ac166d61---------------------------------------)

1 min read

·

Jun 20, 2018

--

9

Listen

Share

More

## **Use case**

There are use cases where you need to make multiple HTTP requests (to same or different server) and you need to wait until you get responses from all the HTTP requests for rendering the view.

## **Solution**

**‘forkJoin’** is the easiest way, when you need to wait for multiple HTTP requests to be resolved

**‘forkJoin’** waits for each HTTP request to complete and group’s all the observables returned by each HTTP call into a single observable array and finally return that observable array.

The above example shows making three HTTP calls, but in a similar way, you can request as many HTTP calls as required.

As shown in the above code snippet, at the component level you subscribe to single observable array and save the responses separately.

ForkJoin official docs — <http://reactivex.io/rxjs/class/es6/Observable.js~Observable.html#static-method-forkJoin>

*If you liked this article, please* 👏 *below, so that other people can find it! :D*