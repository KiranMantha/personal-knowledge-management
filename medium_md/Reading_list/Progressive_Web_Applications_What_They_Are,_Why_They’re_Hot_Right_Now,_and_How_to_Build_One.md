---
title: "Progressive Web Applications: What They Are, Why They’re Hot Right Now, and How to Build One"
url: https://medium.com/p/3c6c131f55d6
---

# Progressive Web Applications: What They Are, Why They’re Hot Right Now, and How to Build One

[Original](https://medium.com/p/3c6c131f55d6)

# Progressive Web Applications: What They Are, Why They’re Hot Right Now, and How to Build One

[![Jesse Swedlund](https://miro.medium.com/v2/resize:fill:64:64/1*0OSt6Oi-BeSyaEViYuHdQw.jpeg)](/@jesseswedlund?source=post_page---byline--3c6c131f55d6---------------------------------------)

[Jesse Swedlund](/@jesseswedlund?source=post_page---byline--3c6c131f55d6---------------------------------------)

9 min read

·

Dec 16, 2020

--

Listen

Share

More

Press enter or click to view image in full size

![]()

If you are a smartphone user (and who isn’t these days?), chances are that you’ve already been using progressive web applications (PWAs). That’s because PWAs look and feel remarkably like native applications and can be purchased or downloaded in the App Store or Google Play, just like any other native app. However, PWAs can also look and feel remarkably like a normal website, but with improved performance. So what exactly are they and why are industry giants like Twitter, Pinterest, and Starbucks making the switch?

Press enter or click to view image in full size

![]()

The big difference between a native app and a PWA is that a native app is a standalone program that runs on your device, while a PWA is a highly performant website that can be installed to feel just like a native app while covertly running in a fullscreen web browser window. Under the hood, you are essentially interacting with a website that is disguised as a native application. This means big performance benefits for users: PWAs take up less storage space than a native app and they cache important assets, meaning less of those time-consuming calls to the server.

Let’s take the example of a user with an older mid-level smartphone with a slow 3G network connection. On a traditional website, a browser has to make multiple calls to a server to retrieve everything it needs to render the initial view. This can take a surprisingly long time, especially if there are high resolution photos involved. In addition, if a user has to decide between deleting one application in order to install another, they will be less likely to download it, and therefore less likely to engage with the product. Twitter is a great case study: after converting their mobile website to a PWA (aka “Twitter Lite”), they went from being interactive on 3G in about 15 seconds of loading time to under 5 seconds! They saw a 76% increase in Tweets and a 2.7% increase in page views.

And there are potentially even bigger implications for application developers: you can now write a one-size-fits-all mobile application using only JavaScript, CSS, and HTML. Of course, other tools and frameworks like React will make your job a lot easier, but you no longer need to know React Native, Swift, Java, or Objective-C in order to provide an application experience to your users. Of course, PWAs have their limitations, and not every app idea is suited to use the PWA framework (such as apps that use Mapbox). In addition, [companies like Apple](https://johanronsse.be/2020/08/30/apple-doesnt-care-about-your-pwa-and-a-little-rant-about-holding-back-the-future-of-computing/) have put up some roadblocks for PWAs in favor of native applications. That being said, let’s get into how to build a PWA.

## Getting Set Up

These instructions will assume that you have a code editor and a way to launch your website on a local host with a development server.

First, let’s prime our main HTML document. Note that this HTML doc example is set up for Webpack to bundle my files and run a React app in the div with the ID of “app”.

```
<!DOCTYPE html>  
<html>  
  <head>  
    <meta charset=”utf-8" />  
    <meta name=”viewport” content=”width=device-width   
    initial-scale=1.0" />  
    <title>My App</title>  
    <link rel=”stylesheet” href=”/style.css” />  
    <link rel=”manifest” href=”/manifest.webmanifest” />  
    <script defer src=”/bundle.js”></script>  
    </head>  
    <body>  
    <div id=”app”></div>  
    </body>  
</html>
```

The important line of code here that stands out here is:

```
<link rel=”manifest” href=”/manifest.webmanifest” />
```

Similar to the way we are connecting to our stylesheet, here we are linking our manifest to our document. But what is a manifest you may ask?

## Manifest your Dreams

To make your web app installable, you need to create a web manifest file. A manifest is a JSON file containing information about your app, including what icons it should use when installing your app. **Create a file in your public folder called manifest.webmanifest** and paste in the following code:

```
{  
  “short_name”: “Your App Name”,  
  “name”: “Your App Name: The Best App Around!”,  
  “description”: “The app you’ve always needed and never knew it.”,  
  “icons”: [  
    {  
      “src”: “/images/logoSmall.png”,  
      “type”: “image/png”,  
      “sizes”: “192x192”  
    },  
    {  
      “src”: “/images/logoBig.png”,  
      “type”: “image/png”,  
      “sizes”: “512x512”  
    }  
  ],  
  “start_url”: “/”,  
  “background_color”: “#ffffff”,  
  “display”: “standalone”,  
  “scope”: “/”,  
  “theme_color”: “#808080”,  
  “shortcuts”: []  
}
```

Update the short\_name, name, and description to your liking. The icons are what will be used by a device when installing the app on its home screen or desktop. At the very least, you’ll need a 192x192 pixel logo and a 512x512 pixel logo. If you don’t have these ready to go, **visit** [**https://favicon.io/**](https://favicon.io/) **and create a logo and download the folder with your new logos. Create a folder in your public folder called “images”**, and put your 192 and 512 logos inside of it. Either rename the images “logoSmall.png” and “logoBig.png” or change the “src”: lines of code in the manifest to match up with the names of your icons. The background color is currently white and the theme color is gray. Feel free to change these to your liking as well.

There’s more you can do with your manifest, such as adding shortcuts or changing the display. For more information on customizing your manifest, check out this resource: <https://web.dev/add-manifest/>

## Get yourself a Service Worker

Press enter or click to view image in full size

![]()

A service worker is a script that runs in the background of your browser. It can allow for offline operations and improve performance through caching strategies and using idle time to load resources. A service worker script should be implemented in the head of your main HTML document.

Add the following code into your HTML, just under the bundle.js script.

```
<script>  
  if (‘serviceWorker’ in navigator) {  
    window.addEventListener(‘load’, () => {  
    navigator.serviceWorker.register(‘/service-worker.js’)  
    })  
  }  
</script>
```

This code will check to see if the browser supports a service worker and uses the window load event to register your service worker. Now, **create a service-worker.js file in your public folder.** Here is an example taken from [GoogleChrome’s github sample for a basic service worker](https://googlechrome.github.io/samples/service-worker/basic/) that you can paste into service-worker.js:

```
/*  
Copyright 2015, 2019, 2020 Google LLC. All Rights Reserved.  
 Licensed under the Apache License, Version 2.0 (the "License");  
 you may not use this file except in compliance with the License.  
 You may obtain a copy of the License at  
 http://www.apache.org/licenses/LICENSE-2.0  
 Unless required by applicable law or agreed to in writing, software  
 distributed under the License is distributed on an "AS IS" BASIS,  
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
 See the License for the specific language governing permissions and  
 limitations under the License.  
*/// Incrementing OFFLINE_VERSION will kick off the install event and force  
// previously cached resources to be updated from the network.  
const OFFLINE_VERSION = 1  
const CACHE_NAME = 'offline'  
// Customize this with a different URL if needed.  
const OFFLINE_URL = 'offline.html'self.addEventListener('install', event => {  
  event.waitUntil(  
    (async () => {  
      const cache = await caches.open(CACHE_NAME)  
      // Setting {cache: 'reload'} in the new request will ensure that the  
      // response isn't fulfilled from the HTTP cache; i.e., it will be from  
      // the network.  
      await cache.add(new Request(OFFLINE_URL, {cache: 'reload'}))  
    })()  
  )  
  // Force the waiting service worker to become the active service worker.  
  self.skipWaiting()  
})self.addEventListener('activate', event => {  
  event.waitUntil(  
    (async () => {  
      // Enable navigation preload if it's supported.  
      // See https://developers.google.com/web/updates/2017/02/navigation-preload  
      if ('navigationPreload' in self.registration) {  
        await self.registration.navigationPreload.enable()  
      }  
    })()  
  )  // Tell the active service worker to take control of the page immediately.  
  self.clients.claim()  
})self.addEventListener('fetch', event => {  
  // We only want to call event.respondWith() if this is a navigation request  
  // for an HTML page.  
  if (event.request.mode === 'navigate') {  
    event.respondWith(  
      (async () => {  
        try {  
          // First, try to use the navigation preload response if it's supported.  
          const preloadResponse = await event.preloadResponse  
          if (preloadResponse) {  
            return preloadResponse  
          }          // Always try the network first.  
          const networkResponse = await fetch(event.request)  
          return networkResponse  
        } catch (error) {  
          // catch is only triggered if an exception is thrown, which is likely  
          // due to a network error.  
          // If fetch() returns a valid HTTP response with a response code in  
          // the 4xx or 5xx range, the catch() will NOT be called.  
          console.log('Fetch failed; returning offline page instead.', error)          const cache = await caches.open(CACHE_NAME)  
          const cachedResponse = await cache.match(OFFLINE_URL)  
          return cachedResponse  
        }  
      })()  
    )  
  }  // If our if() condition is false, then this fetch handler won't intercept the  
  // request. If there are any other fetch handlers registered, they will get a  
  // chance to call event.respondWith(). If no fetch handlers call  
  // event.respondWith(), the request will be handled by the browser as if there  
  // were no service worker involvement.  
})
```

Also from Google’s basic service worker sample, here’s what this particular service worker does:

* Precaches the HTML, JavaScript, and CSS files needed to display this page offline. (Try it out by reloading the page without a network connection!)
* Cleans up the previously precached entries when the cache name is updated.
* Intercepts network requests, returning a cached response when available.
* If there’s no cached response, fetches the response from the network and adds it to the cache for future use.

You can confirm the service worker’s behavior by opening up the Application panel of Chrome’s DevTools. To learn more about Service workers, [check out this resource.](https://developers.google.com/web/fundamentals/primers/service-workers) There are many different tools to help build service workers and select caching strategies that are right for your app.

## Go Offline

One last thing you’ll need to do is to include an offline fallback HTML file. The service worker will cache this file and display it when the user is offline. This example is very simple, but there’s a lot you could do here to give your user offline functionality that can add a ton of value to your app.

In the public folder, create a file called offline.html and paste the following code into it:

```
<!DOCTYPE html>  
<html lang="en">  
  <head>  
  <meta charset="utf-8" />  
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />  
  <meta name="viewport" content="width=device-width,   
  initial-scale=1" />  
  <title>You are offline</title>  
  <style>  
    body {  
      font-family: helvetica, arial, sans-serif;  
      margin: 2em;  
    }  
    h1 {  
      font-style: italic;  
      color: #209cee;  
    }  
    p {  
    margin-block: 1rem;  
    }  
  </style>  
  </head>  
  <body>  
    <h1>You are offline</h1>  
    
    <p>Click the button below to try reloading.</p>  
    
    <button type="button">⤾ Reload</button>  
    <script>  
      document.querySelector('button').addEventListener('click', ()      
      => {  
      window.location.reload()  
      })  
    </script>  
  </body>  
</html>
```

I adapted this code from here: <https://web.dev/offline-fallback-page/>

![]()

Notice how the css styling and javascript is all included inline. That’s because your service worker needs to cache everything that it will be using for offline use. An all-in-one approach is the simplest way to achieve a single offline page. In order to do more, you’ll have to change the service worker to include whatever resources you would want for offline functionality.

## Install Your App!

If you did everything right, you should be able to launch your app onto a local host on chrome and see a small plus button inside of a circle at the end of your search bar. If you click on it, you should get a prompt to install the app onto your device!

![]()

Ahhh, bask in the glory of an installed PWA. Doesn’t that logo look awesome on your desktop?!

To learn how to do more with your PWA, such as creating an in-app button that prompts the user to install your app, I suggest checking out this amazing PWA resource. <https://web.dev/progressive-web-apps/>

## A Note on using HTTPS

In order for your PWA to work properly, you are required to use HTTPS. To learn more, [check out these docs.](https://developers.google.com/search/docs/advanced/security/https)

Thanks for reading and I wish you a great PWA journey!