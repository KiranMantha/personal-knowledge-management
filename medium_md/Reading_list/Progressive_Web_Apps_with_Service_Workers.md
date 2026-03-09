---
title: "Progressive Web Apps with Service Workers"
url: https://medium.com/p/887e80abf9ef
---

# Progressive Web Apps with Service Workers

[Original](https://medium.com/p/887e80abf9ef)

# Progressive Web Apps with Service Workers

## In this post we will discuss *Progressive Web Apps* and *Service Workers*. How can they help modern-day mobile web users, and how are we experimenting with them at Booking.com? We will share some challenges we’ve encountered, as well as some of our learnings.

[![Jesse Yang](https://miro.medium.com/v2/resize:fill:64:64/0*9gr2K2rZtMiw42vl.JPG)](/@ktmud?source=post_page---byline--887e80abf9ef---------------------------------------)

[Jesse Yang](/@ktmud?source=post_page---byline--887e80abf9ef---------------------------------------)

10 min read

·

Apr 21, 2016

--

Listen

Share

More

![]()

## What is a Progressive Web App?

A Progressive Web App (PWA) is a term [Google coined](https://developers.google.com/web/progressive-web-apps) to describe its prospect of app-like web experiences, in which web pages are able to offer many features once deemed app-only — connectivity control, push notifications, home screen icons, and the like.

Before this initiative, some of the features in discussion were already available for mobile web users (although to a limited extend):

* Add to home[1](https://developer.apple.com/library/ios/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html)screen[2](https://developer.chrome.com/multidevice/android/installtohomescreen)(requires manual actions)
* Fullscreen mode[3](https://www.html5rocks.com/en/mobile/fullscreen/)
* Application Cache for offline access[4](https://alistapart.com/article/application-cache-is-a-douchebag)
* Notifications API[5](https://developer.mozilla.org/en-US/docs/Web/API/Notifications_API/Using_the_Notifications_API)

Web pages, however, are still not the first choice, when it comes to delivering the best possible experience on a mobile device (despite being more discoverable in search engines and potentially saving the nuisance of downloading and installing megabytes, especially important for first-time visitors and visitors in 2G/3G connections). All too often do we see websites adding banners or interstitial popups[6](https://www.theguardian.com/technology/2015/sep/02/google-punish-sites-for-using-interstitial-adverts), begging users to download their apps, even going so far as to drop their mobile version completely[7](https://www.quora.com/Why-is-Flipkart-going-app-only-1)(only to be resurrected[8](https://tech-blog.flipkart.net/2015/11/progressive-web-app/)5 months later). The justifying arguments that recur: native apps run more smoothly and have better means to re-engage with customers, and the web environment simply lacks graceful fallbacks in flaky network conditions.

A Progressive Web App addresses all these issues except the rendering performance part. Building a Progressive Web App does not force you to drastically change your current front-end architecture or the way your work; it only gives you a set of tools to enhance the web experience *progressively*. At the end of the day, you’ll be able to have:

* A home screen icon that opens the website in fullscreen
* Native dialogs to let users add your app to their home screens with one click
* A fast and always-usable site even in flaky network connections
* Push notifications just like native apps

Most of these features are made possible by service workers.

## What is a Service Worker?

> *Service workers essentially act as proxy servers that sit between web applications, and between the browser and network (when available). They are intended to (amongst other things) enable the creation of effective offline experiences, intercepting network requests and taking appropriate action based on whether the network is available and updated assets reside on the server. They will also allow access to push notifications and background sync APIs. —* [*MDN*](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)

In short, a service worker is an asynchronous background thread that takes control of all network requests in a page.

## Quick Facts

* Service Workers run in a different context, thus have no access to DOM elements or JavaScript variables in the main thread
* For security reasons the client page (the main thread) must be in https and the service worker script must be in the same origin, but all requests originated from that page can be intercepted by service workers even if they are not in https or served from a different domain
* A [CacheStorage](https://developer.mozilla.org/en-US/docs/Web/API/CacheStorage) is provided in the worker so that you can store server responses (including headers and response body) locally, and serve them to future requests.
* Server responses can be forged at the client side if necessary.
* Everything is asynchronous, and most APIs return a [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)

## Browser support

For now, only Chrome, Firefox and Opera have adequate support for service workers. For mobile devices, that means only Android is supported. Since features like homescreen icons and push notifications are integrated in the OS, the whole *Progressive Web App* initiative really depends on how enthusiastic OS vendors are about it.

Regarding service workers, Apple’s attitude is:

> *People think they want it, some of them actually do want it. We should probably do it.*[*9*](https://trac.webkit.org/wiki/FiveYearPlanFall2015)

(it seems, then, we won’t wait for too long before service workers are available in iPhones.)

For a detailed compatibility table of all features of service workers, check out this document: [Is ServiceWorker ready?](https://jakearchibald.github.io/isserviceworkerready/)

## What can Service Workers do?

The ServiceWorker API provides very granular methods for developers to intercept requests, to cache and forge responses, opening doors for all kinds of interesting activities like:

* Offline access to certain pages (an order confirmation, an e-ticket, etc)
* Precaching assets based on predictions of next user actions (predictions do not rely on service workers per se, but cache manageable can be more programmable with service workers. You can even introduce an expiration time or the [LRU](https://en.wikipedia.org/wiki/Cache_algorithms#LRU) algorithm if you want)
* Serving a cached version when it takes too long to load some resources
* Rewriting URLs to always be requested with a canonical url[10](https://en.wikipedia.org/wiki/Canonicalization)

Check the [Offline Cookbook](https://jakearchibald.com/2014/offline-cookbook/#serving-suggestions-responding-to-requests) for more details about the caching strategies.

In addition, service workers are also used for arranging background communication with servers (think of it as a “service”). Features like [push notifications](https://developer.mozilla.org/en/docs/Web/API/Push_API), [background sync](https://github.com/WICG/BackgroundSync/blob/master/explainer.md), [task scheduler](https://www.w3.org/TR/task-scheduler/) all depends on service workers in some extend.

## Service Workers in Action

Now, let’s get our hands dirty and get to grips with the service worker in action.

## Registration

Since service workers run in a different context, you’ll need to put the code for the worker in a separate file, then register it in the client page:

```
if ('serviceWorker' in navigator) {  
  navigator.serviceWorker.register('service-worker.js', { scope: './' }).then(function() {  
    if (navigator.serviceWorker.controller) {  
        console.log('The service worker is currently handling network operations.');  
    } else {  
        console.log('Failed to register.');  
    }  
  });  
}
```

This snippet registers a service worker with the file `service-worker.js`. Once registered, code in this file will be able to control all requests originated from any page within the `scope` parameter.

By default, the `scope` is the base location of the service worker script. For example, if you registered "/static/js/serviceworker.js", then the default scope would be "/static/js/". The script itself must be within the same origin as the client page, so it's not possible to serve service worker scripts with CDNs in different domains. But it *is* possible to override the scope to be outside of the script's base location:

```
navigator.serviceWorker.register('/scripts/service-worker.js', { scope: '/' })
```

This code enables the service worker to control all pages under the root path of the origin (`{ scope: '/' }`). But you'll need to add an extra response header `Service-Worker-Allowed` to make it work.

For instance, in an nginx configuration, it can be done like this:

```
Server {  
  
    listen www.example.com:443 ssl;  
  
    ...  
  
    location /scripts/service-worker.js {  
        add_header 'Service-Worker-Allowed' '/';  
    }  
}
```

(Note that this header is added for the service worker script itself, not the page it was registered to.)

## Inside the worker

Once registered, a service worker will reside in the background intercepting all requests originated from its client pages and staying active until being unregistered.

The script runs in a context called `ServiceWorkerGlobalScope`[11](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope). Several global variables and methods are available in this context:

* **clients** — Information about client pages, used to claim control over them
* **registration** — Represents the state of the registration
* **cache** — The CacheStorage object in which you can store server responses
* **skipWaiting()** — Allowing registration to process from waiting to active state
* **fetch(..)** — Part of the GlobalFetch API, also available in the main thread
* **importScripts(..)** — Import JS scripts synchronously, ideal for loading a service worker library

The Google Chrome team has provided a nice high-level library[12](https://github.com/GoogleChrome/sw-toolbox)to help you handle service worker tasks. It ships with a router for expressively applying common caching patterns to different resources, as well as a toolkit for precaching and namespaced cache management. It is highly recommended to use this library if you want to build something production-ready; it saves you a lot of work and is also a good start for you to get familiar with basic concepts in a ServiceWorker. Check out the [recipes](https://github.com/GoogleChrome/sw-toolbox/tree/master/recipes) for example usages.

If you are really after the details, refer to MDN [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API) document and pay extra attention to `CacheStorage`[13](https://developer.mozilla.org/en-US/docs/Web/API/CacheStoragerage), and `FetchEvent`[14](https://developer.mozilla.org/en-US/docs/Web/API/FetchEvent).

## Service Workers at Booking.com

Press enter or click to view image in full size

![]()

At Booking.com, we are always open to new technologies, and encourage any innovation that improves customer satisfaction. We are currently working closely with the PWA advocate team from Google on applying some of the core features of Progressive Web Apps to our mobile website to see where it helps our customers.

Having service workers installed for users is relatively easy — you simply need them to be using a supported browser (currently this means using Chrome in Android). The real challenge, however, lies in how to introduce meaningful features while carefully measuring the impact. At Booking.com, we do every customer-facing project in A/B test experiments, and try to achieve things in the “smallest viable steps.” The purpose is to ship the *right* things as *fast* as we can. Even for something as holistic as a Progressive Web App, we work in small steps in order to tackle issues one by one, and learn things quickly.

We have gathered some important learnings on this topic. What follows are some of the learnings we found which might be interesting to the general public.

## Caching Strategy Examples

The Offline Cookbook[15](https://github.com/mkruisselbrink/ServiceWorker/blob/foreign-fetch/foreign_fetch_explainer.md) summarized a few caching strategies for different use cases.

* **cacheFirst** — Serve cache if it exists, requests will still fire, and new responses will update the cache
* **cacheOnly** — Respond with the cache only, never fire the actual request
* **networkFirst** — Always try fetching from the network first and save the latest successful response into the cache, which will be served when the network fails
* **networkOnly** — Never uses local cache

Let’s see some examples of how to apply each of them in real life.

For static files that never change, we can safely serve them with “cacheFirst”:

```
toolbox.router.get(/static\/(css|js|images|img)\//,  
    toolbox.cacheFirst, {  
       cache: { name: 'static-files' }  
    }  
);
```

They seldom change and even if they do, we would’ve updated the URLs. One might ask, *what’s the use of this technique if we already set the expiration date in the headers?* A service worker gives you more granular control over how much cache you want to store and when to expire them. For instance, `sw-toolbox` provides very easy configurations for maxEntries[16](https://jakearchibald.com/2014/offline-cookbook/#serving-suggestions-responding-to-requests)and maxAgeSeconds[17](https://github.com/GoogleChrome/sw-toolbox#cachemaxentries-number).

For ordinary HTML documents, we can use “networkFirst”:

```
toolbox.router.get(/\/(confirmation|mybooking|myreservations)/i,   
    toolbox.networkFirst, {  
        networkTimeoutSeconds: 10,  
        cache: { name: 'booking-confirm' }  
    }  
);
```

We configured the `networkTimeoutSeconds` parameter here. If it is acceptable to show this page to offline visitors, then it must be also acceptable to offer the cached version for users with very slow network connections and save them some waiting time. But of course, the length of the timeout seconds depends on your type of business and the common connectivity quality of your users.

For requests used for user behavior data collection, you might want to use “networkOnly”:

```
toolbox.router.any(/www.google-analytics.com/, toolbox.networkOnly);
```

There’s no point to return cache for a tracking request, right? If the request fails, it fails. If you want, you can even monitor the status of a tracking request, and resend it when it fails. This won’t be possible if (somehow) the cache in service workers kicks in.

## Local Shortcuts

Wouldn’t it be nice if users can save a permanent link in bookmarks which will always redirect them to the last booking confirmation they saw?

Let’s add a custom handler for the confirmation page:

```
toolbox.router.get("/confirmations/(.*)", function(request, values, options) {  
    var url = request.url;  
    var promise = toolbox.networkFirst(request, values, options);  
    var confirmationId = values[0];   
    if (confirmationId) {  
        // when the request finishes  
        promise.then(function(response) {  
            if (!response || response.status !== 200) return;  
            self.caches.open('last-confirmation').then(function(cache) {  
                // save a 302 Redirect response to "/confirmation"  
                var redirectResponse = new Response('Redirecting', {  
                    status: 302,  
                    statusText: 'Found',  
                    headers: {  
                        Location: url  
                    }  
                });  
                cache.put('/confirmation', redirectResponse);  
            });  
        });  
    }  
    return promise;  
}, {  
    networkTimeoutSeconds: 10,  
    cache: {  
        name: 'confirmations',  
    }  
});  
  
toolbox.router.get('/confirmation', toolbox.cacheOnly, {  
    cache: {  
        name: 'last-confirmation'  
    }  
});
```

Each time users visit a confirmation page, we will return the response as normal, with the strategy “networkFirst”. But in addition to that, we forge a 302 redirect response locally, pointing to the current url, then save the fake response in a cache storage named `last-confirmation` with URL key `/confirmation`.

We’ve also added a rule in the router for this path and this cache storage, so that the next time users visit the URL “/confirmation”, they will always be redirected to the last confirmation page they visited.

The forged response was put into a separate cache storage namespace, and is served with strategy `cacheOnly`. Because, apparently, the URL is only valid locally. We certainly don't want to mix it with normal requests.

## The Secure Domain Problem

To protect users’ data, all parts of our booking process and user account management pages are served via HTTPS, under a separate domain — “secure.booking.com”, instead of “www.booking.com"—the one used for public content such as the Search Results and Hotel Details page.

You can’t register one service worker across two different domains however, even if they are subdomains of the same root domain. And (for now at least) there’s no way to let two service workers communicate with each other.

What if you want to pre-cache assets for `secure.booking.com` when users are still in `www.booking.com`, or the other way around? We have a lot of people jumping between two domains, especially when they are making a reservation. Also, with important functionalities spread across different domains, a service worker for one single domain simply cannot offer an uninterrupted offline experience.

Because of this, we are unifying all basic functionalities under one domain and this will give users full HTTPS access to their whole Booking.com journey. Meanwhile, experts of the Service Worker Specs group are working on a new API called “foreign fetch”[15](https://github.com/mkruisselbrink/ServiceWorker/blob/foreign-fetch/foreign_fetch_explainer.md), which will give service workers authorities to intercept any requests for resources within their scopes (as defined when they were registered). These requests may be originated from any page, even if the page is under another domain.

## Final Thoughts

The ServiceWorker API targets a long-standing problem for the mobile web — connectivity. It has the potential to make user experience bearable even when connectivity is bad. It empowers modern web apps with the ability to engage users in more intimate ways, and definitely increases web apps’ competitiveness over native ones.

The vision of Progressive Web App is nice, but for a large-scale website steering at a very high speed, you can’t implement everything and ship them in one go. Constantly experimenting, learning, and improving things with small steps, is the key to success.

## Resources

1. [Progressive Web Apps](https://developers.google.com/web/progressive-web-apps)
2. [Service Worker Spec](https://www.w3.org/TR/service-workers/)
3. [ServiceWorker API doc on MDN](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
4. [Service Worker Debugging](https://www.chromium.org/blink/serviceworker/service-worker-faq)
5. [Recipes 1](https://github.com/GoogleChrome/samples/tree/gh-pages/service-worker)
6. [Recipes 2](https://davidwalsh.name/offline-recipes-service-workers)
7. [Demos by W3C web mobile group](https://github.com/w3c-webmob/ServiceWorkersDemos)

Would you like to be a Developer at Booking.com? [Work with us](https://workingatbooking.com/vacancies/?filter-searchphrase=developer)!