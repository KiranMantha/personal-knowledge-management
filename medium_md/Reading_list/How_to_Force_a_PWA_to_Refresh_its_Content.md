---
title: "How to Force a PWA to Refresh its Content"
url: https://medium.com/p/fef2c6ff3591
---

# How to Force a PWA to Refresh its Content

[Original](https://medium.com/p/fef2c6ff3591)

# How to Force a PWA to Refresh its Content

[![Kevin Basset](https://miro.medium.com/v2/resize:fill:64:64/1*wwzMirzqEaaVwuk_ncW22g.jpeg)](https://kevinbasset.medium.com/?source=post_page---byline--fef2c6ff3591---------------------------------------)

[Kevin Basset](https://kevinbasset.medium.com/?source=post_page---byline--fef2c6ff3591---------------------------------------)

5 min read

·

Dec 17, 2021

--

2

Listen

Share

More

One of the most common questions we get asked at [Progressier](https://progressier.com/?ref=medium20211217) pertains to client-side caching. *How does one ensure a PWA always displays up-to-date data and assets while also making good use of caching?*

Press enter or click to view image in full size

![]()

Although a PWA often looks and feels like a native app, from a technical perspective it really just works like any other website. When one opens a page, it loads assets (images, scripts, stylesheets…) and data (user data, product data…). These resources are fetched from the network and then used by the browser.

Enter the [HTTP cache](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching) mechanism. In order to make loading websites faster, browsers cache these resources. On the initial load, an image will come from your server. On the following load, it may come from the cache instead. So if you update it in the meantime, the browser may display a stale version of that image. How can you prevent that?

## The Versioning Trick

Versioning is probably the easiest way to force the browser to load a resource from your server. When you update a resource, add a parameter to the URL of the resource wherever your request in your code. For example, edit your client-side code to request`domain.com/data.json?version=2` instead of `domain.com/data.json?version=1`.

A browser will see these two URLs and consider them completely different assets. So it won't use a cached version of the former when the page explicitly requests the latter. A good practice is to append a version number (or any other query strings, really) to key resources in your build process, so you don’t have to do that manually every time you make a change.

## The Cache-Control Header

When a server responds to a HTTP request successfully, it returns the asset itself (a JavaScript file, an image, a CSV file…) but it also sends headers — parameters that tell the browser what they are allowed or not allowed to do with the resource.

One of these headers is the [Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control) header. It exists specifically so you can tell the browser how a particular resource should be cached (or not) and revalidated (or not).

If you control the server that responds to the request, you can set different `Cache-Control`headers and tell the browser how it should treat each particular resource. For instance, set the value of the `Cache-Control` header to `no-cache`to forbid the browser to cache the resource at all.

Of course, this method only works with resources that you own — not third-party scripts, CSS libraries, Google fonts or images hosted somewhere else.

## The Network First Strategy

Truth be told, the [HTTP Cache](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching) mechanism is a bit antiquated. With it, all you can really tell the browser is whether or not a resource should be cached and until when.

There is another caching mechanism called the [Cache API](https://app.intercom.com/). And it’s available in [service workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers). [Progressier](https://progressier.com) uses that API for its caching strategy maker. You can define very specific rules for each type of resources without having to write a single line of code.

Press enter or click to view image in full size

![Example a caching strategy that covers all resources]()

With the *Network First* strategy, resources will always be fetched from the network exclusively (so an error will be thrown if the network is somehow unavailable, e.g. if the user or the server go offline).

Of course, most of the time, you’ll want to be more specific and apply that strategy to resources that are mission critical and use more caching-friendly strategies for less essential resources ([Stale-While-Revalidat](https://intercom.help/progressier/en/articles/5703064-what-s-a-caching-strategy)e for example).

## The Fake Reload Button

With the first three methods, you’re essentially telling the browser whether a particular resource should be retrieved from the cache or the network when the page is loaded.

But once installed, opening a PWA may not always trigger a new page reload. You can launch a PWA from your home screen, do what you have to do with it, then launch another app, and go back to the PWA the next day.

If you haven’t closed the app or turned off your phone in the meantime, it will not reload the page — instead it will simply allow you to continue your session where you left off. If you, the app owner, updated resources in the meantime, then the user may still be using stale resources. How can you force the PWA to refresh its content then?

When we launched [The Coronavirus App](https://progressier.com/#story) in January 2020, users were very demanding when it came to data freshness. We updated data every 15 minutes automatically, so it was absolutely critical to not let users see stale data (or we would receive tons of angry emails!).

But rather than wait for actual updates, we used a simple trick: when the user had spent more than half an hour on the page, we would present them with an option to reload the page (which they had no other choice but click) and fetch resources again. It looked like this:

![]()

Giving the illusion that something is happening is a powerful UX concept. In our case, the purpose was two-fold: make it look like the app was updated constantly (which it actually was — just not in a synchronized manner with that fake reload button) and avoid showing stale data.

## Conclusion

So there you go. Three different caching methods to ensure your PWA stays updated and one little UX trick.

The versioning trick is probably the easiest way to go about this — and it works universally, whether you own the requested resources or not.

And if that’s not feasible easily in your build process, you can either use the Cache-Control header (for resources you own) or the Service Worker method to granularly define caching behaviors.

What do you think? Do you use other methods to keep your PWA updated?

*More content at* [***plainenglish.io***](http://plainenglish.io/)***.*** *Sign up for our* [***free weekly newsletter here***](http://newsletter.plainenglish.io/)***.***