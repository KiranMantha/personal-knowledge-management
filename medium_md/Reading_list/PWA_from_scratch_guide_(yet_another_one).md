---
title: "PWA from scratch guide (yet another one)"
url: https://medium.com/p/bdfa438b50aa
---

# PWA from scratch guide (yet another one)

[Original](https://medium.com/p/bdfa438b50aa)

# PWA from scratch guide (yet another one)

[![Yassine Benabbas](https://miro.medium.com/v2/resize:fill:64:64/2*UsVT877F998hH1bLvzEnCg.jpeg)](https://medium.com/@yostane?source=post_page---byline--bdfa438b50aa---------------------------------------)

[Yassine Benabbas](https://medium.com/@yostane?source=post_page---byline--bdfa438b50aa---------------------------------------)

12 min read

·

Apr 8, 2018

--

3

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dbdfa438b50aa&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fpwa-from-scratch-guide-yet-another-one-bdfa438b50aa&source=---header_actions--bdfa438b50aa---------------------post_audio_button------------------)

Share

![]()

Welcome to my guide for creating a PWA (progressive web app) from scratch. I hope that it will help you understand a little more service workers, Web App manifest and caching. Enjoy 🎓.

## Introduction

During the following sections, we are going build a very simple PWA from zero. The goal is to become familiar with the most important PWA concepts; the manifest and the service worker. We will not use any particular framework and will keep the code very concise. For the sake of simplicity, we will be using some ES6 features in the javascript.

Here are the main steps of this guide. Each one will be addressed in a different section:

* Preparing the app shell
* Adding a manifest
* Implementing Service Worker
* Caching

I hope that this guide will give you a glimpse of the benefits that you can get by adopting the PWA ideas. But before getting into the code, let’s prepare our workstation with the necessary elements.

## Requirements

We are going to use Visual Studio Code IDE along with these languages: HTML 5, CSS3 and EcmaScript 6. Here is the setup that I recommend for this tutorial:

* [Visual studio code or VS Code](https://code.visualstudio.com/)
* [Live server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer): it allows to run the current workspace on a local server with a single button click.
* Optionally, [JavaScript Snippet Pack](https://marketplace.visualstudio.com/items?itemName=akamud.vscode-javascript-snippet-pack) or any other extension that you prefer to use for web projects.
* A JSON API that is ready for use. Hopefully, there is a GitHub repository that categorizes some [public APIs](https://github.com/toddmotto/public-apis). In this guide, we are going to use [Jikan API](https://jikan.docs.apiary.io/#reference)
* Latest version of [Chrome](https://www.google.fr/chrome/) because we will be using its powerful PWA developer tools

Once everything is setup and ready, we can initialize the first lines of code.

## Project description and initialization

The PWA that we are going to build is a simple anime search app. It allows to display an anime given its **id**. The UI provides an input field and a button for entering an anime id and validating it. In addition to that, the history of the search results will also be presented.

The guide is split into different steps. The first step consists in building the app shell. Next, we will be adding a manifest that allows to add the PWA to home-screen. After that, a service worker will be added in order to cache the previous search responses. This will allow to display some results even in offline mode. The forth step consist in caching the history without relying on the service worker.

![]()

We are going to create the first files and first lines of code of our project. This allows to have some code running and also to verify our setup before digging into main dish 🍕.

Please follow these steps to get a minimal website:

* Create an empty folder that will contain our project
* Launch VSCode and open that folder
* Create a new HTML file
* Initialize the file with an HTML snippet (CTRL+SHIFT+P -> type snippet -> choose html)
* Add a **main.js** file and **main.css file** which we will use later

The html file should be similar to this one:

Let’s run this website on local server created using [Live server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer). Simply click on the **Go Live** button on the toolbar. You default browser should render your **index.html** as a blank page.

![]()

The serious stuff starts nows ✌️ with the app shell goodness.

## The app shell

The app shell is defined by [Addy Osmani](https://developers.google.com/web/fundamentals/architecture/app-shell) as:

> *The minimal HTML, CSS and JavaScript required to power the user interface and when cached offline can ensure instant, reliably good performance to users on repeat visits*

Here, I try to give a synthetic definition (excuse me if I’m wrong 😃):

*The app “shell” is the HTML, CSS and JS and media content of a PWA that is:*

* Sufficient for browsing online or offline
* Minimal
* Constant

Let me explain these points:

* Sufficient for browsing online or offline: the app shell should be designed in a such a that users can browser all of the content of the website whether online or offline. For me, this is the most important feature of an app shell.
* Minimal: the app shell is the content that is first loaded when we open a PWA. having a small and optimized app shell means faster load time and smaller caching.
* Constant: since we are going to use the PWA offline, we need to cache some html, css, js and media files to load the app. Having a base content that changes over time makes managing offline mode very complicated. Thus, I consider a good app shell to be constant.

In light of that explanation, the app shell will have a single HTML page with no hard coded anime content at all. The latter will be loaded from the internet or from the cache. The shell will also contain the javascript code that allows to load anime info from the network and maintain a search history. The last parts of our small app shell is a css file and the static assets.

Our app shell will be very small, constant (or static) and allow us to use take advantage of all the functionalities of our PWA whether offline or online.

Let’s go back to VS Code and add these content to the html page:

* A button and an input field.
* Two empty divs. One for displaying the result of the searched anime (with `id="main_anime"`) and another one for showing the history (with `id="history"`).

The html file should look like this. We should not change very soon which makes it a good app shell component.

Great, let’s also some css to get some **responsive** UI thanks to the `flex-wrap: wrap;` property.

The JavaScript part of our app shell will be evolving throughout the tutorial. But for now let’s do the basic things.

First of all, define the constants and the functions that will generate the html tags from a single anime object.

The `animeHistory` array allows to store the history of searched anime.

You can see here an example of an anime object provided by the Jikan API <https://api.jikan.me/anime/1000>. You can change the number at the end of the url to get a different anime. Beware that some id may return a 404. Here are some anime ids that succeed: 4524, 5672, 1 and 1000.

Here is the code that fetches an anime from the network when the user clicks on the button. The history and the DOM is updated when the response is successfully retrieved.

In the above code snippet, we use the `fetch` API to load content from the server and then display it on the main div and the history div. The `fetch` API is a simple way to do Ajax requests.

As you can see that there no manifest, no service worker and no cache. It is OK because the app shell is not yet finalized.

You can test the app right now. It is not yet PWA compliant but we will work on it in the next steps 😏.

## The PWA manifest

Our first step in the PWA world is adding a manifest file. Here is its definition from [MDN](https://developer.mozilla.org/en-US/docs/Web/Manifest):

> *The web app manifest provides information about an application (such as name, author, icon, and description) in a JSON text file.*

Adding a web manifest gives you other advantages. Here are some of them:

* They allow the user to add a bookmark on your home-screen or desktop
* It allows to display a simple splash-screen while the app is loaded

Since the web manifest is a plain JSON file, we can either write it manually or use a tool to generate it. We are going to use this [Web App Manifest Generator](https://tomitm.github.io/appmanifest/).

Press enter or click to view image in full size

![]()

Using the tool, try to generate the following `JSON` file or a similar one.

Put that JSON in a file called `manifest.json` and place it in the root of your website along the different icons. Maybe you can find your icons in [FLATICON](https://www.flaticon.com/).

We will also update the HTML head with the html generated by the tool. Of course the most important tag is `<link rel="manifest" href="manifest.json">`.

Let’s try to open the app on a mobile phone browser. Enter the url `MACHINE_IP:PORT`, tap the menu button of your browser and look for the option **Add to home screen.**

![]()

By choosing this option, you will end up with a link of you PWA on your home screen.

![]()

Next, tap on the shortcut. you will see a small loading screen. It can be customized using the `theme_color` and `icons` properties.

![]()

Right after that, the fullscreen PWA is shown with all its glory thanks to the `"display": "fullscreen"` option in the manifest.

![]()

Yaaaay ! The PWA is now added to my home-screen 😍. However, there is no caching yet 😒 (try to open the app in plane mode). Let’s deal with that in the next step 🚀.

## Adding a Service Worker

In this section, we are going to cache the static files as well as the responses of the anime that the user previously fetched. Please note that we will be persisting the history in this section.

In order to cache the responses of the requests made by the browser, we need to implement a proxy that intercepts them. In other words we will customize the behavior of the `fetch` calls by caching the response and presenting the cached content instead of the network content. The **proxy** that allows us to do that is called a **Service Worker**. It is accompanied with an API that allows to cache network responses which is the [**Cache API**](https://developer.mozilla.org/fr/docs/Web/API/Cache).

The service worker is basically a set of event handlers for some browser events that must be implemented in a separate file, often called **sw.js**. In order to use it, we need to first register it to the browser. Registration is done by calling `navigator.serviceWorker.register`.

Add the following function to the **main.js** file and add it to the `onload` event handler of your **index.html** page.

When the page reloads, you should see the following log line in the console of your browser.

> *Service worker registered [object ServiceWorkerRegistration]*

This means that the file **sw.js** specified in `let serviceWorker = await navigator.serviceWorker.register('/sw.js')` has been successfully registered as a service worker. You can confirm that by checking the **Applications** tab of the Chrome developer tools.

Press enter or click to view image in full size

![]()

*The application tab is a very useful tool for debugging your PWA. I invite you to play with its different menus.*

When developing a service worker, it is recommended to check the **Update on reload** checkbox. It makes chrome reinstall the Service Worker after each registration. Otherwise, when you register a new service worker, w will have to manually unregister the previous one before. So, please go ahead and check it.

Next, create a javascript file at the root folder called **sw.js** (or whatever name you specified to the register method). As explained above, the service worker is a set of event handlers that allow us to mainly provide caching behavior. With respect to that, we are going to implement two event handlers: **install** and **fetch**.

The first event is `install`. It is called once after a successful service worker **registration**. It is the best place to cache the app shell and all static content. We are going to use Cache API of the service worker to add those files as follows. Add the following code to sw.js.

Using the cache is pretty straightforward; we first `open` it and then `addAll` static files.

You can check that the files are successfully added by clicking on the **Cache Storage** on the left menu.

Press enter or click to view image in full size

![]()

Great, the files that I added earlier are all inside the cache storage. However, we just did half of the job because the cache is not loaded. In order to confirm that, click on the **offline** checkbox in the service worker menu. Refresh the page and … 😱 the web app fails to load.

To sum up, we added file to the cache but they were not loaded in offline mode. The problem is that we did not inform the browser to use them when the network call fails.

The remaining piece of the puzzle is the `fetch` event of the service worker. And as a bonus the `fetch` event handler that we are going to implement will also cache the API calls. This is possible because the event is called before any network request is emitted by the browser. When we handle this event, we can choose to load cached content, forge our response object or just get the network response.

Please add to following to the service worker.

Please note that the critical line of code is this one `event.respondWith(getCustomResponsePromise())`. It allows us to **override** the browser response with a `Promise` or `async` function that resolves to a `Response` instance. Without that call, the service worker would be nearly *useless*.

Basically, this event handler loads content from the Cache Storage. If the content is not available, we get it from the internet. This behavior is called a **Cache first strategy**. Other strategies are possible and you even make your own **fetch cats 😺** strategy.

Reload the page, do some anime searches and verify the cache storage. New elements should pop up there.

![]()

Next, check the **offline** checkbox and try opening the page again. Magnificent ! The page is loaded and we can even search for previously searched anime. It event works on my phone using plane mode. It’s magic 😍.

There is still a last thing to do which is caching the history. Since the it is an array and that is not built from a network response, we cannot use the Cache API and the service worker. The next part of this guide will show a way for caching outside of service workers.

## Caching the history

This section will show a technique to persist the `animeHhistory` array using the `localStorage` object. This object provides functions to store data and retrieve when the page is reloaded **even after closing the browsing windows**. Storing an entry is performed using `localStorage.setItem(key, entry)` and retrieving it is performed using `localStorage.getItem(key)`.

The caveat here is that this persistent storage works only with string values. So, we need to serialize/deserialize our array to/from a JSON string when storing/loading respectively. This is achieved thanks to `JSON.stringify(array)` and `JSON.parse(string)` functions.

In **main.js**, modify the `updateHistory` function as follows.

On to the final touch. Make the `onLoadAsync` function load the persisted history when the DOM is ready.

Don’t panic, we just added a function that loads the anime history from the local storage and called it in the `onLoadAsync` event handler. It is recommended to do it there since we want to update the DOM with the history as soon as the former is ready.

Press enter or click to view image in full size

![]()

Voilà, our small PWA shows the history when the page is loaded and is updated over time 🎆.

## Conclusion and going further

This guide was a practical introduction to the most PWA concepts. They are: the service worker and the manifest. We also learned how to use Crome dev tools to debug service workers. We just scratched the surface of these features and many more things can be done. Some improvements are:

* Add HTTPS which is mandatory for a PWA
* Implement a different caching strategy.
* Add server side rendering.

If you want to build a production PWA, I suggest you to use frameworks that support PWA or plugins for PWA if you use a CMS. Generally you don’t need to implement a service worker but it is interesting to know how it works.

The GitHub repository is available [here](https://github.com/yostane/pwa_from_scratch).

Happy coding :)

## Links

[Adding a Service Worker and Offline into your Web App](https://developers.google.com/web/fundamentals/codelabs/offline/)

[The App Shell Model](https://developers.google.com/web/fundamentals/architecture/app-shell)

[Progressive Web App tutorial — learn to build a PWA from scratch](https://www.youtube.com/watch?v=gcx-3qi7t7c)

[Manifeste des applications web](https://developer.mozilla.org/fr/docs/Web/Manifest)

[The Web App Manifest](https://developers.google.com/web/fundamentals/web-app-manifest/)

[HTML5 Web Storage](https://www.w3schools.com/html/html5_webstorage.asp)

[How do I store an array in localStorage?](https://stackoverflow.com/questions/3357553/how-do-i-store-an-array-in-localstorage?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa)