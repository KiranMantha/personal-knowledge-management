---
title: "JavaScript: Vanilla Single Page Applications (SPA)"
url: https://medium.com/p/1b29b43ea475
---

# JavaScript: Vanilla Single Page Applications (SPA)

[Original](https://medium.com/p/1b29b43ea475)

# JavaScript: Vanilla Single Page Applications (SPA)

## Build an SPA without any frameworks, bells, or whistles

[![Santiago García da Rosa](https://miro.medium.com/v2/resize:fill:64:64/1*D5L3sfr7p-q3Yd-H1zXXIg.jpeg)](/@santiagogarcadarosa?source=post_page---byline--1b29b43ea475---------------------------------------)

[Santiago García da Rosa](/@santiagogarcadarosa?source=post_page---byline--1b29b43ea475---------------------------------------)

6 min read

·

Nov 8, 2017

--

12

Listen

Share

More

![]()

This blog is a continuation of a series of articles that I started creating to try to explain how JavaScript deals, at a lower level, with some of the features of some of the multiple frameworks and libraries that we have out there.

Before, we created a [two-way binding with Vanilla script](/frontend-fun/js-vanilla-two-way-binding-5a29bc86c787), now we are going to implement an SPA functionality with plain JavaScript but, of course, before going through the actual implementation, let’s talk a little bit about SPAs…

## What Is an SPA (Single Page Application)?

The main idea behind an SPA is to dynamically load content into the current page without loading an entire page from the server. You kind of get a desktop application feel.

All the HTML, JavaScript, and CSS may be retrieved from the server with the first load of the application, instead of getting everything over and over again with each load like a non-SPA would do.

Another important point is that the main page or content never reloads, but you still have different URLs and browser history through the use of location hash or the HTML5 history API.

In the examples, we are going to use and explain the location hash but both of them are quite simple to use and understand.

## Why SPA?

Let’s mention some advantages of using SPAs:

* Performance**.** SPA diminishes the necessity of the browser to perform requests to the server, which impacts the velocity of our application and the user experience.
* Better UX.Since the velocity of the application is improved, the user iteration flows and feels better.

Of course, there are also disadvantages, let’s mention some:

* Heavy first load. Since the first load of the app may be loading a bunch of resources, it might feel slow.
* JS must be enabled.This maybe sounds dumb because everyone has JavaScript enabled in their browsers, but if someone turns it off then an SPA is worthless.
* Security.SPAs are less secure since it enables hackers to perform cross-site scripting.

It is not necessary to add, but I am going to do it anyway. If you implement an SPA in the wrong way, all the advantages are lost.

Let’s have some fun and let’s go through an example…

## Creating a Simple SPA

The idea is to implement a simple single page application using Vanilla script with a location hash approach.

### Folder structure

![]()

* `js`. This is where the JavaScript implementation is located.
* `views`. This is where the HTML for the routes is.
* `index.html.` This is the main HTML of our app. It is going to load the scripts and set the container to render the routes’ HTML.

### Index HTML

As we mention before, this is the main HTML of our app, it is going to load the JS we need, add the menu links, and also set the container element to render the routes’ HTML.

![]()

* We are creating two menu options linked to `#home` and `#about` (the hash is needed since we are going to use location hash).
* The `div` with the `id` set to `app` is where we are going to render the HTML associated with the active route.
* Finally, we load the scripts that we are going to use.

### About and home HTML

We don’t really care about the content of these files, so one only contains a `div` with a `Home` text and the other a `div` with an `About` text.

The idea is to load one by default (as a default route) and the other if needed. As we mentioned before, they are located in the `views` folder.

### Route JS

This JavaScript is going to provide a constructor to our `Route`s and also a couple of functionalities.

![]()

We have three params:

* `name`. Is the name of our route, we are going to use it to check if the route is the active one.
* `htmlName`. Is the name of the HTML to load with the route.
* `default`. `True` if the route is the default route of our app.

And it has two functions:

* `constructor`. This is just a constructor function.
* `isActiveRoute`. A function provided by each route to check if it’s the active one. It receives the actual window location.

### Router JS

This friend is the one that contains most of the magic. Let’s take a look at the code and then we are going to explain it.

![]()

![]()

So, let’s start digging into this JS.

It only receives one param:

* `routes`. It is an array containing the routes of our app.

It has another property:

* `rootElem`. It is the root element of our application. The place where other HTML gets rendered.

Finally, it has four functions:

* `constructor`. This is just a constructor function. It is executed only one time in the creation of `Router`.
* `init`.This function creates a listener to the `hashchange` event of window. First, it sets a callback to that listener to execute the function `hasChanged` and finally, it executes it for the first time (this is going to allow us to execute a default route). Now, every time the location hash changes, the listener that we just created is executed. This function is executed only one time in the creation of `Router`.
* `hasChanged`.This function has two main responsibilities, both related to performing the correct `Route` load. If the window location changes then it is going to load the correct active `Route` and call another function to load its HTML, if the window location is empty, it is going to load the default `Route`. This function receives two params, one is the scope of the `Router` instance and the other is the routes.
* `goToRoute`.This function has the responsibility of getting and loading the correct HTML for the active route. It receives the HTML name that it has to load and finally perform a request to get it.

This is all we need to have a simple SPA implementation working.

### Initialization of routes and Router

Finally, let’s see how we start the router in the app.js file.

![]()

This script is executing an `init` function that instantiates the `Router` and provides two `Route`s, setting `home` as the default one.

Implementation: [GitHub](https://github.com/SantiagoGdaR/vanilla-spa).

## Conclusion

The idea of this article, as we mentioned at the beginning, is to show an approach to implement an SPA router with the objective of getting a basic idea of how this feature could be addressed by a library or framework.

I hope you enjoyed it!