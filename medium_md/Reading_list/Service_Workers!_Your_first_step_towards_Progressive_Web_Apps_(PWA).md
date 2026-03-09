---
title: "Service Workers! Your first step towards Progressive Web Apps (PWA)"
url: https://medium.com/p/e4e11d1a2e85
---

# Service Workers! Your first step towards Progressive Web Apps (PWA)

[Original](https://medium.com/p/e4e11d1a2e85)

Member-only story

## JavaScript

# Service Workers! Your first step towards Progressive Web Apps (PWA)

[![Uday Hiwarale](https://miro.medium.com/v2/resize:fill:64:64/1*B4PQwnTacbDmtJgKYY7CzA.jpeg)](/@thatisuday?source=post_page---byline--e4e11d1a2e85---------------------------------------)

[Uday Hiwarale](/@thatisuday?source=post_page---byline--e4e11d1a2e85---------------------------------------)

19 min read

·

Apr 4, 2018

--

5

Listen

Share

More

Press enter or click to view image in full size

![]()

In my previous blog…

[## Achieving multi-threading (parallel programming) in JavaScript using Web Workers

### JavaScript is single threaded language but multi threading (parallel programming) can be achieved in JavaScript using…

medium.com](/@thatisuday/achieving-parallelism-in-javascript-using-web-workers-8f921f2d26db?source=post_page-----e4e11d1a2e85---------------------------------------)

I talked about Web Workers. They give us a medium to do most **heavy lifting** operations within **background** thread. This has enormous applications as you have seen and we should use them whenever we can.

But web workers have many limitations. They were designed to do only one thing and that is, to act as a **load balancer for the main thread**. Only the threads which creates web workers can use them. If you want multiple threads (pages in different browser tabs) to access same workers at the same time, then you need to use **Shared Worker**, which is not supported in all browsers. Also, dedicated or shared workers do not have access to the properties and belongings of main thread.

This is where **Service Workers** come into play. Service workers are just like web workers but **they can be accessed by many main threads** (*running in different browser tabs*) at the same time. Sadly only one service worker is allowed per **scope** (we will talk about scope later, it’s just a **URL Path**) on the browser.

Unlike web workers, where a web worker is coupled with main thread, once service worker is started by main thread, it does not get killed even when that thread dies or when browser is closed. Not only that, **some network requests coming from main thread goes through service worker**. Hence service worker acts like **man in middle** who has authority to transform network request and response. This has many applications, as you can cache web pages and/or web assets and return this cached data back instead of transmitting request over network.

Service workers have access to **Cache API** ([*https://developer.mozilla.org/en-US/docs/Web/API/Cache*](https://developer.mozilla.org/en-US/docs/Web/API/Cache)) and **Fetch API** ([*https://developer.mozilla.org/en-US/docs/Web/API/Fetch\_API*](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)). Service workers are used widely also to store data in **IndexedDB** for **offline data persistence**. Internet went crazy over browser implementation of push notifications. This has became possible because of service workers as **they live even when browser dies**. **Background sync** is a new web API supported by service workers that lets you defer actions until the user has stable internet connectivity. This is useful for ensuring that whatever the user wants to send, is actually sent.

Press enter or click to view image in full size

![]()

Seems like service workers are pretty amazing and they are kinda big deal. Even though service workers are not implemented in all browsers, but they are being considered for future releases in some of the non-supported browsers. You can keep track of browser compatibility using <https://jakearchibald.github.io/isserviceworkerready/> website, to know about which browsers support service workers and its web APIs. So why are we waiting? Let’s get down to technical spec and start working on our first service worker.

As we know, web workers are created using `Worker` interface or constructor. Service workers are created using `ServiceWorker` interface and it inherits properties from `Worker` interface. Hence **service workers can do what web workers can do**. But JavaScript does let you create service workers using `ServiceWorker` constructor, as service workers are very difficult to manage on your own, as you will see later why.

Hence, service worker’s internal implementation is abstracted from the user and browser gives you clean API to work them with instead in `Navigator` object using `navigator.serviceWorker`. The `navigator.serviceWorker` read-only property returns the `ServiceWorkerContainer` object. The `ServiceWorkerContainer` interface of the **ServiceWorker API** provides an object representing the service worker as an overall unit in the network ecosystem, including facilities to register, unregister and update service workers, and access the state of service workers and their registrations.

As we are on the topic of discussing about service worker’s internal implementation, there are few things you must know while creating a service worker and how they are different from web workers.

Service workers can only work on secure connections, that means **HTTPS**. This is because as service workers are very powerful and they can do serious damage to your system or network if been tampered with by man-in-middle. But in development, you can use local server as **localhost** is exempted from this restriction.

Like web workers, a service worker creations also require one external JavaScript file URL. This file must be on either localhost or on secure server.

**Scope** is very important in service workers. Unlike web workers where one main thread can create unlimited web workers, only one service worker can exist per scope and their existence is independent from the main thread. Using this property, service workers can be accessed by many tabs in the browser at the same time.

Let’s create a project structure like we did in ***previous blog*** and write our very own service worker.

```
service-workers  
|_ main.js  
|_ index.html  
|_ sw.js
```

***sw.js*** in above project is service worker script file which will be implemented by ***main.js*** inside ***index.html***. Let’s see how we can create a service worker in ***main.js*** script.

First of all, you need to make sure if user’s browser support service workers. You can verify that by using `'serviceWorker' in navigator === true` check. If service workers are supported in the browser, then you might want to create service worker when all other scripts in the page are finished executed. You can use `window.onload` event for this one.

Service worker API is **Promise** based. You must know how to use promises in JavaScript and they are very easy to understand. The syntax to create service worker is as below

```
var p = navigator.serviceWorker.register(SW_URL, [options]);
```

`register` function on `serviceWorker` downloads the service worker script from URL `SW_URL` and executes it. `options` is optional extra configuration for service worker which is a JavaScript object and supports `scope` key of string value. This returns a **promise** `p` which resolves if service worker file is downloaded and executed successfully. You can use `then` and `catch` methods on it. `then` callback function receives **registration** object which contains information about service worker and API interface for other services. `catch` callback function receives **Error** information if any error occurs while service worker’s installation.

Let’s see a practical example.

Alternatively, you can use following syntax as well.

`navigator.serviceWorker.ready` returns a promise and always resolve. If there are multiple service workers registered for an origin, then which service worker will control client page will depend on the scope of the service worker. You should read this ([*https://stackoverflow.com/a/41707357/2790983*](https://stackoverflow.com/a/41707357/2790983)) answer on Stack Overflow to get better understanding of this. We will discuss scope in a bit, then it will be clear to you.

When you host project using `live-server` (*read previous blog for this*), and access ***index.html***, above program will print below output to the console.

```
Service worker successfully registered on scope http://127.0.0.1:8080/
```

Let’s discuss about this **scope**. We discussed how service workers are different from web workers as only one service worker can exist per **scope**. A web page sends many network requests for files and data white user use interacting with it. **Scope** is nothing but a **URL path**. Any requests that starts with this URL path will be **intercepted** by service worker. For example, if scope of service worker is `/` then any requests like `/index.html`, `/main.js`, `/users`, `/assets/logo.png` or any requests that starts with `/` (**URL Prefix**) will be intercepted by this service worker.

**Scope of a service worker depends on where the service worker file is located**. So in above ***main.js*** file, since we are fetching service worker file ***sw.js*** from `/sw.js` URL, `/` is the **scope** of service worker. **You can say it is the directory of service worker file**. Service worker will only intercept requests with URL that starts with scope. If you want service worker to listen to requests that starts with `/users` prefix **ONLY** then host ***sw.js*** file like `.register('/users/sw.js')` or use `.register('/sw.js', {scope: './users'})` where *scope option* is path suffix relative to ***sw.js*** file.

> There will be a case when you want to put all your service workers in one directory, let’s say `/workers` but then those service workers will have `/workers/` scope. To avoid this, **sw.js** must be served with a response header `Service-Worker-Allowed: /` where value of this header is the scope of this service worker (here `/`). Using up levels like `.register('/workers/sw.js', {scope: '../'})` is not allowed.

**Scope** is linked with domain/origin. You can not create a service worker that intercepts request for other origins. If you try to register a service worker from origin which is different from origin of service worker file ***sw.js***, then error will be thrown like `The origin of the provided scriptURL ('https://cdn.example.com/sw.js') does not match the current origin`.

> To avoid this, there is a trick <https://developers.google.com/web/updates/2016/09/foreign-fetch> but I really don’t recommend doing that, try to simplify your application.

**Let’s see how service workers can be implemented.** A service worker has many life cycle events. Most important are `install` and `activate` events. We listen to these events just like `message` event in web workers, and that is using `addEventListener` method.

> I advice you to use **incognito window** to test this application because a service worker is installed and activated only once. I will explain this phenomenon later. Relaunch incognito window if you don’t see any console log.

In your console log, you will see following output.

First, when service worker is downloaded and executed, we get the promise callback for that in ***main.js*** using `register` function as you saw. Once service worker is registered successfully, installation of service worker starts. Installation occurs only once per **scope**. If a service worker is already present in the browser for that scope, then **installation will skip unless we are trying to installed new or modified service worker**. If there is even a byte difference between already installed and currently installing service worker script file, then browser will install new service worker.

While installation, `install` event will trigger. We can listen to this event inside `install` event handler. We can also block installation of service worker for some time to do some housekeeping work like cache important files or store some data in IndexDB database. **Install event only saves service worker script in browser**. After installation, service worker script is kept it for **pending activation**. Activation of service workers depends on some conditions which needs to be met. **After activation, browser will start using service worker**.

If a service worker is not installed before for a scope, then after its installation, `activate` event is trigger. Web pages which might send network requests this service worker, that are already opened in **new** tabs (*other than current*), will not use service worker unless they are refreshed or relaunched (as they don’t *service worker implementation*).

If a service worker is already installed for a scope, then neither `install` nor `activate` event will trigger. Hence you don’t have to worry about installing same service worker again and again.

If service worker is already installed for a scope but is new or modified, then `install` event is triggered but **service worker won’t be activated unless all the tabs (pages) which are using old service worker are relaunched**.

You can also block service worker’s activation in `activate` event handler. This is a great place to remove old cached files or remove expired database entries. **Once a service worker is activated, it will start intercepting network requests**.

> You can verify above events by checking console log.

**Google Chrome** provides great interface for service workers. Using this tool, you can see which service workers are running currently and which are pending for activation. Also, you can stop or restart service workers manually. It also provides tools to send push messages or sync calls for testing purpose.

> While in development, you should check checkbox **Update on reload** inside **Application > Service Workers** (inside Chrome Developer Tools) to update service workers on page refresh. This will save time and effort of closing browser again and again.

Press enter or click to view image in full size

![]()

So far, we understood how to install and start a service worker. Now it’s time to use it for practical applications like network requests modifications and caching.

### 1. Network Requests Interceptor

Any network requests in browser that starts with the scope of a service worker will pass through that service worker. Service workers can intercept these request in **fetch** event handler. If this event handler is not present in service worker, these requests will bypass.

Press enter or click to view image in full size

![]()

**fetch** event receives an event object which contains all information about the request like URL destination, payload etc. We can modify these requests and forward them to the network. When response comes, we can modify the response object and return it to caller. Let’s see how that works.

I am going to remove `install` and `update` event handlers from ***sw.js***, just to focus on `fetch` event only. Also, download any image or google logo ([*https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google\_2015\_logo.svg/272px-Google\_2015\_logo.svg.png*](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/272px-Google_2015_logo.svg.png)) and save it under `assets` folder inside the project with `logo.png` filename. Then embed that image inside ***index.html*** like below.

```
<img src="./assets/logo.png"/>
```

We wrote above code so that our ***index.html*** page sends a network request for ***logo.png*** file which will go through service worker as request URL of this file falls under service worker’s scope which is `/`.

Let’s now add `fetch` event handler to ***sw.js*** service worker.

```
self.addEventListener('fetch', function(event){  
    console.log(event.request);  
});
```

Once you refresh the page, you will see following console logs.

Our service worker intercepted three requests, for `/index.html`, `/main.js` and `/assets/logo.png`, as all of them fall under service worker’s **scope** which is `/`.

> But if you can’t see request for **index.html** in the log, then duplicate the current tab and check **console log** of other tab when current tab is refreshed. If you are wondering why other page’s console is printing the log, then read this blog again to understand where service worker lives.

You can see other information like *headers* and *body* by expanding **Request** object in console log. In above example, **event** object is read copy and any writes done on it won’t affect the request. Hence we need to use **API methods** provided by **event** object to make changes to the request and response. One of such requests is `event.respondWith`. `respondWith` method takes a **promise** which upon resolution (*success or failure*) should contain **valid response data** which service worker will send back to thread who sent the request. Hence when we use this method, it becomes our responsibility to send the request to the network and get proper (*valid*) response. Let’s see how that works.

```
// sw.jsself.addEventListener('fetch', function(event){  
    event.respondWith(  
        fetch(event.request)  
    );  
});
```

In above code, we are using **fetch** web API ([*https://developer.mozilla.org/en-US/docs/Web/API/Fetch\_API*](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)) which is available in global scope of service worker. We could have used `self.fetch` but it is redundant. We passed `event.request` object to `fetch` function which will return a promise. This promise will resolve if server response is successful else it will reject. Once that promise is resolved or rejected (*which will be done by fetch API itself*), `respondWith` method will return response back to the thread who requested it. Using this simple code, we can make modifications to request and response.

```
// sw.jsself.addEventListener('fetch', function(event){  
    event.respondWith(  
        new Promise((resolve, reject) => {  
            var req = modify(event.request); // modify request  
              
            // send network request  
            fetch(req)  
            .then((r) => resolve(modify(r))) // modify response  
            .catch(e => reject(e));  
        })  
    );  
});
```

When we use `fetch`, by default, requests won't contain credentials such as cookies. Use `{credentials: 'include'}` option in `fetch(URL, [options])` syntax. You learn more about these options from <https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/fetch>.

### 2. Caching and Offline Access

Caching involves offline storage of objects which are key-value pairs of **Request** and **Response**. The **Cache** interface provides a storage mechanism for these object that are cached.

The **CacheStorage** interface represents the storage for **Cache** objects. The **caches** read-only property of gives clean API to work with **CacheStorage** in current context. This object enables functionality such as storing assets for offline use, and generating custom responses to requests.

If you type **Cache**, **CacheStorage** and **window.caches** or **caches** in your browsers console, you can see if your browser supports them.

In layman’s term, **Cache is a container for Request-Response key-value pair objects**. Multiple of such objects can exists with same Request key. Cache object has a **unique reference id** or `cacheName` which can be used to store different versions of cached objects. **CacheStorage** tracks **Cache** objects and provide API for **CRUD** operations.

**caches** API can be accessed from ***window*** context or ***service worker*** context. Hence we can cache response of network requests and use them when needed. It gives us following API methods

* `caches.match(request, options)`  
  Checks if a given `request` is a key in any of the **Cache** objects that the **CacheStorage** object tracks, and returns a Promise that resolves to that match.
* `caches.has(cacheName)`  
  Returns a Promise that resolves to `true` if a Cache object matching the `cacheName` exists. `cacheName` is the key for **CacheStorage** object.
* `caches.open()`  
  Returns a Promise that resolves to the **Cache** object matching the `cacheName` (a new cache is created if it doesn’t already exist.)
* `caches.delete()`  
  Finds the **Cache** object matching the `cacheName`, and if found, deletes the **Cache** object and returns a Promise that resolves to `true`. If no **Cache** object is found, it returns false.
* `caches.keys()`  
  Returns a Promise that will resolve with an array containing `cacheName` corresponding to all of the named **Cache** objects tracked by the **CacheStorage**. Use this method to iterate over a list of all the **Cache** objects.

In some of the above methods, we get **Cache** object in return. **Cache** object also provide API methods to do operations such as adding cache entries. Below, `cache` is an instance of **Cache**.

* `cache.match(request, options)`  
  Returns a Promise that resolves to the response associated with the first matching request in the **Cache** object.
* `cache.matchAll(request, options)`  
  Returns a Promise that resolves to an array of all matching requests in the **Cache** object.
* `cache.add(request)`Takes a URL, retrieves it and adds the resulting response object to the given cache.
* `cache.addAll(requests)`  
  Takes an array of URLs, retrieves them, and adds the resulting response objects to the given cache.
* `cache.put(request, response)`  
  Takes both a request and its response and adds it to the given cache. `response` is a stream.
* `cache.delete(request, options)`  
  Finds the **Cache** entry whose key is the request, returning a Promise that resolves to true if a matching Cache entry is found and deleted. If no Cache entry is found, the promise resolves to false.
* `cache.keys(request, options)`  
  Returns a Promise that resolves to an array of Cache keys.

So far we understood basic API details of Cache API, now let’s implement it inside service worker.

We are going to create a new project structure just to demonstrate caching.

```
service-workers  
|_ index.html  
|_ styles.css  
|_ main.js  
|_ sw.js  
|_ assets  
   |_ logo.png
```

For now, let’s keep content of service worker file ***sw.js*** empty.

If you host above project using `live-server`, you will see output like below.

![]()

Now, our mission is to cache all static files like `index.js`, `style.css`, `logo.png` and `main.js` so that when browser sends requests for these files again, we can serve them from the cache.

We can do this in service worker’s **install** event. As we know install event is triggered only once and hence makes it a great place to cache these files. When service worker will activate, we will already have these cached files to serve from.

We will have to **block installation of service worker** until all files are caches. That can be done using `event.waitUntil` method. Like `event.respondWith` method, this method also takes a **Promise**. Let’s see how that works.

```
// sw.jsvar cacheName = 'WWW-EXAMPLE-COM-V1';var filesToCache = [  
    '/',                // index.html  
    '/main.js',  
    '/styles.css',  
    '/assets/logo.png'  
];self.addEventListener('install', function(event) {  
    event.waitUntil(  
        caches.open(cacheName)  
        .then(function(cache) {  
            console.info('[sw.js] cached all files');  
            return cache.addAll(filesToCache);  
        })  
    );  
});
```

In above ***sw.js*** service worker file, we created a `cacheName` variable to store unique name for **Cache** object. In `filesToCache` array, we are storing path of files which needed to be cached. Inside service worker’s **install** event handler, we are blocking installation by using `event.waitUntil` method which takes a Promise.

If you refer to API methods of **Cache** and **CacheStorages**, `caches.open` or `self.caches.open` takes `cacheName` which is unique id of **Cache** object. If **Cache** object with id `cacheName` does not exist, it will create one and return a Promise. In `then` callback, we are returning a Promise to chain using `cache.addAll` method which takes array of URLs to fetch responses from network. `cache.addAll` method will sent network requests and save responses to the `cache` which is a **Cache** object.

If all files are cached successfully, then installation of service worker will be successful. If even one file failed to download or cache, then installation of service worker will fail. Hence, you should not make a long list of cache files and make sure they will be always available over network.

You can execute `caches.keys().then(r => console.log(r))` code on your browser’s console to check if **Cache** object was created.

Just for fun, simulate offline network by checking **offline** checkbox inside Developer Tools’s **Network** tab. Once you reload the server, you will see below screen.

![]()

Since we successfully cached static files, now it’s time to use them. As we know, using **fetch** event we can intercept network requests which fall under the scope of service worker. We are going to return cached responses if request received in `fetch` event handler contains in cache storage. Since all our assets are cached, we can provide full access to website **offline**. Add below code to ***sw.js*** file.

```
// sw.js...self.addEventListener('fetch', function(event) {  
    event.respondWith(  
        caches.match(event.request)  
        .then(function(response) {  
            if(response){  
                return response  
            }            // not in cache, return from network  
            return fetch(event.request, {credentials: 'include'});  
        })  
    );  
});
```

`event.respondWith` will block request going over network. As it takes a Promise, we can use `caches.match` method which takes a **Request** objects (*we are using* `event.request`) and returns a promise. This promise will be resolved if **CacheStorage** contains response associated with this request. Inside `then` callback, we get a cached Response object `response` and we can return it to the caller. This `response` can be empty if cached entry is missing. In that case, using `fetch` API, we have to make network request and response will be served from it (*this won’t be cached*).

Now again go back to your browser with **offline network access still on**, and reload the page. You can see now that the website is working even when there is no internet connectivity. This is possible because responses are served from cache. This is very powerful stuff to make progressive web apps.

Press enter or click to view image in full size

![]()

There is one problem through. When a cache is missing, we have to make network request, but response from that network request it not cached. That means when we make same request again, it still propagates over the network. To avoid this, we need to cache response from that request.

Here is a ***sw.js*** file with caching improvement.

`cache.put` is used to cache entry manually using Request and Response objects. We are doing caching operation in background because we want to return response as quickly as possible to improve user experience.

Let’s say that we have modified all our static files which are (*could be*) cached on user’s browser. That means want to remove these cached files from user’s browser and replace with new ones. This is where **activate** event is useful.

What we can do is update service worker file ***sw.js***, which will cause install event to trigger. Inside install event, we will rename `cacheName` to newer version. This will create new **Cache** object inside `install` event handler. When this new service worker is activated, we can delete old **Cache** object in `activate` event handler.

```
// sw.jsvar cacheName = 'WWW-EXAMPLE-COM-V2';...  
...self.addEventListener('activate', function(event) {  
    event.waitUntil(  
        caches.keys()  
        .then(function(cacheNames) {  
            return Promise.all(  
                cacheNames.map(function(cName) {  
                    if(cName !== cacheName){  
                        return caches.delete(cName);  
                    }  
                })  
            );  
        })  
    );  
});
```

In above modifications of ***sw.js***, we have incremented cache version in `cacheName`. This will definitely make service worker new (*bytes change*) and browser will re-install service worker by firing **install** event. We haven’t changed `install` event handler implementation as we want service worker to cache files again from the network (*which are now modified*). But in the `activate` event handler, we blocked the activation of service worker until all old cached responses are deleted.

We used `event.waitUntil` to block activation phase of service worker. This method takes a promise, hence we used `caches.keys` which returns a Promise. Upon resolution, it will contains ids of **Cache** objects or `cacheName` array. Inside `then` callback, we returned another promise using `Promise.all` method which takes an array of promises and resolves when all promises are resolved. Using `.map` function on `cacheNames`, we can return this array of promises. `caches.delete` function takes `cacheName` and returns a promise which will be resolved when **Cache** object with this id is deleted.

Above example will successfully delete old cached files when service worker is activated. We are deleting old cached files in `activate` event and not in `install` event handler because if done that then other web pages still using older service worker will get empty cached objects. This can also break your application if some non-cacheable resources depends on resources that are cacheable.

I guess we are done with caching part of service workers but there are many more thing that we can do to improve our application.

* You can cache files which a website does not use for example `offline-index.html`, `offline-styles.css` and others for offline viewing. These files can be used when user does not have network connectivity. Approach for doing this would be to cache these files in `install` event handler with `cache.put` method. Then inside `fetch` event handler, you can serve these files when `fetch` promise rejects due to no internet connectivity.
* You can also cache inline responses using **Response** constructor function. This way, you can minimize network load but it will increase size of your service worker file.

I advice you to check Mozilla documentation for **Cache** and **CacheStorage** interface even when I have added their API methods information. Caching is not only limited to service worker and you can take control of it from `window` context as well. Chrome Developer Tools provides great UI to see cached resources under **Application > Cache Storage** tab.

Press enter or click to view image in full size

![]()

There are few libraries which provide great API for writing service workers in few lines of code. You should check out some of the following libraries.

* <https://googlechromelabs.github.io/sw-toolbox/>
* <https://github.com/GoogleChromeLabs/sw-precache>
* <https://developers.google.com/web/tools/workbox/>
* <https://www.talater.com/upup/>

In next blog, we will talking about offline data persistence which is very important concept in designing **progressive web apps**.

[## IndexedDB! Your second step towards Progressive Web Apps (PWA)

### Single page applications demands data to be loaded from a web service. This data then gets injected into DOM by the…

medium.com](/@thatisuday/indexeddb-your-second-step-towards-progressive-web-apps-pwa-dcbcd6cc2076?source=post_page-----e4e11d1a2e85---------------------------------------)

Press enter or click to view image in full size

![]()

![]()