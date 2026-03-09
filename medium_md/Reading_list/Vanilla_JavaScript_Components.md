---
title: "Vanilla JavaScript Components"
url: https://medium.com/p/8d20c58b69f4
---

# Vanilla JavaScript Components

[Original](https://medium.com/p/8d20c58b69f4)

# Vanilla JavaScript Components

## Learn how to build Vanilla JS components that work today without polyfills

[![Mev-Rael](https://miro.medium.com/v2/resize:fill:64:64/1*eh0X5xsIhMEHSKJWohU0QA.jpeg)](/@mevrael?source=post_page---byline--8d20c58b69f4---------------------------------------)

[Mev-Rael](/@mevrael?source=post_page---byline--8d20c58b69f4---------------------------------------)

8 min read

·

Jan 2, 2017

--

5

Listen

Share

More

Press enter or click to view image in full size

![]()

Components are stand-alone, independent parts of the application which are responsible for handling only one job and don’t know about each other. We already have native components like forms, tables, images, but how we can add custom ones which just works?

## Current state with web components

Currently there is a [Web Components](https://www.w3.org/standards/techs/components#w3c_all) specification in development, which probably, someday will make a web component development standardized, however, it is still far away from being finished and adopted, doesn’t work without a polyfill or framework like Polymer. Apart from the polyfill, there is another problem — current implementation uses ES6 class syntactic sugar which already adds too much complexity altogether with prototypes and doesn’t allow to define properties. The specification also doesn’t tell us how to register custom attributes.

There are also many UI libraries and frameworks available already and the new one comes every day. From the most popular there are React.js and Vue.js. The problem with them is about the marketing hype, huge bundle size, too much extra complexity, “Reacts way” and many other points to mention.

> The most powerful JavaScript framework is JavaScript itself

Do we really need special tools, new language/syntax, new needless abstraction layers using more user device resources and time to handle that job? JavaScript was designed in 10 days to be used by a simple people, even designers, who could just make things done. No matter what you listen or read today — JavaScript still is the most powerful, easiest and flexible way to do the job it was created for and you don’t need a framework to build a modern production app. Yes, web trends evolved for last years, but JavaScript evolved together with them.

> The biggest problem with JavaScript community I see is people instead of learning JavaScript and software engineering are learning another tool.

## How then create JavaScript components?

One of the most powerful features of JavaScript language you won’t find in another one is an *Object literal notation*, simplicity and flexibility of creating and modifying objects. Use it. Here is how you create a component:

```
const Button = {  tagName: 'btn',  init(btn) {  
    btn.addEventListener('click', () => {  
      btn.textContent++;  
    });  
  },  getAll(container = document.body) {  
    return container.getElementsByTagName(this.tagName);  
  }};
```

As you can see it is just a simple JavaScript object. Moreover, I have found the *3rd Person pattern* or an *Object-Speaking pattern* without `new` and prototypes with the usage of the idea behind the *factory pattern* the simplest way of creating objects in JavaScript. Almost every method will receive a DOM element (component) as a 1st argument. You have only one global Button object which operates on all buttons in the DOM and this is your component. You never create any new instances and can access any button from any part of your code without the *Singleton pattern.*

## How were JavaScript components implemented for many years before the modern frameworks war?

For more than 10 years Vanilla JS components were implemented as jQuery plugins or stand-alone widgets. Basically, they were same simple JavaScript objects and functions. You imported one file and in most cases just called init() method. When component was inserted into DOM later, like a simple dropdown, you had to manually call init() on a new DOM element again yourself.

However, there were DOM events available we could use to listen for changes in the DOM like a new tag inserted, removed or attribute changed. So we could use them to call init() or deinit() automatically. The problem there was with a performance and because of that today we have a modern [**Mutation Observer API**](https://developer.mozilla.org/en/docs/Web/API/MutationObserver) which works on every modern platform and even in IE11.

You can initialize just one MutationObserver and listen for changes in the whole document.body, then register custom callbacks when, for example, new tag is inserted into DOM. Since Mutation Observer API and this algorithm requires a bit of logic to implement every time I have created a [**DOMObserver**](https://github.com/Mevrael/bunny/blob/master/src/DOMObserver.js) which can be used to handle that job with ease. Just call `DOMObserver.onInsert('tagname', callback)`.

## How to register custom attributes?

All DOM elements are also just an objects and it is possible to add new properties to any DOM element, i.e. document.body.myProperty = 1;

JavaScript has something called **Object Descriptors** or simply — getters and setters. Getters are called when you try to read a property of any object and Setters are called when you assign a new value to a property. Since all global objects are properties of the window you can execute some code anytime you just use a variable, i.e. this line of code `a;` may do something.

Let say we want to implement a simple counter. Whenever `btn.counter = 1` is executed a counter should have a new value and a `btn.counter` should return a current value. We also want to “register” a `counter` attribute so `<btn counter="6"></btn>` could define a default value.

To define getters and setters in JavaScript you have to use [Object.defineProperty()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty):

```
const attrVal = component.getAttribute(name);  
component['_' + name] = attrVal ? attrVal : defaultValue;  
onChange(component['_' + name]);Object.defineProperty(component, name, {  
  get() {  
    return component['_' + name]  
  },  
  set(val) {  
    component['_' + name] = val;  
    onChange(val);  
  }  
});
```

Now everything will work except changes in attribute, i.e. `btn.setAttribute('counter', 10)`won’t work. For that we will need to register a MutationObserver and listen for attribute changes. To make this job easier I have created a [DOMObserver.registerAttribute()](https://github.com/Mevrael/bunny/blob/master/src/DOMObserver.js#L87) method.

## What about a template/view/UI?

In a good software architecture business logic, of course, should be separated from the presentation logic. Each Component should not know about any data and should not have any side effects. Components are just plain objects — sets of pure functions connecting data with a DOM. In the example above Button is a Controller. For simple components, UI/View/DOM methods can be implemented in the same object. For larger objects, I would recommend separating UI from Controller also and make a ButtonUI object and inject it into Button.UI. In most cases, document.createElement() is the best approach for handling view layer.

However, sometimes we need to parse a template and import custom variables in it. Here is another technic used for many years: server returns some HTML templates hidden from the user, then JS parses those templates. From the Button point of view, I just call UI methods and don’t care about the implementation. Under the hood, it is always easy to replace the UI logic and template engine.

Today we have a `<template>` tag and there is no more need of hiding template contents. Browsers also remove all the content so no components would be initialized inside a template. For older platforms, polyfill can be used or just a `<div hidden>`. I am not going to write about different template engines, there are many of them and you may use any but I would recommend using the right tool for the right job. Sometimes you can just use old document.createElement(), sometimes you may write a simple parseTemplate() function and do a simple string.replace(). The common point here is I strongly would not recommend using a custom JSX or other syntax, or writing HTML or CSS in JavaScript (browser). Many years ago we have been writing all of them together but later we decided to separate them because of maintainability, single responsibility, and simplicity, especially in huge systems. When I am going to change a template of a UI component in a large production app I am searching for the specific template file which is used by a back-end. This also allowed us to share the same template in both front-end and back-end for many years.

The fastest, the most native and simplest way of defining HTML templates without any “server-side rendering” buzzwords is to render all the required HTML needed for the certain page request. Usually, all the templates are put at the bottom before the closing </body>, where today you may find also JS and SVG sprite.

It is also absolutely normal today to just generate HTML on the server like 10 years ago and append it in JS. GitHub, YouTube, and many other apps are still doing this because it is simple and fast.

To sum up this section I want to say that there is no “right way”, there is no only one technic or only one library or framework. Use the right tool for the right job, be flexible.

## What about a state?

“State” is another modern buzzword replaced data but I always will keep calling it data and no matter how you call your architecture pattern, it still is an MVC or inherits a 3-tier architecture, even React components uses MVC, M just became a “state”, V — render() and C — Component itself.

> The most powerful JavaScript function is Object.assign()

Let say we have same btn, counter and another customAttribute. Our data or a state is a data = {counter: 0, customAttribute: 0} which is stored in a DOM element directly. And to update our component all that we need to do is Object.assign(component, data).

Object.assign() will merge all objects together. All properties in the component object will be overridden by properties of data object but this approach, of course, will only work if we have defined component descriptors (getters and setters).

Talking about the data received from the server I am using same simple JavaScript API-speaking objects. Here is, for example, how I can change the state of a Like button to active when a server returns a successful result and in error case, nothing would happen, or base Api object could display a small alert in the corner of the screen:

```
CommentModel.like(commentId).then(() => {  
  Comment.UI.setLikeActive(commentId);  
});
```

## Combining all together

In the example above by using the current JavaScript features:

* Object literal notation
* Object descriptors
* Mutation Observer API (only if you want to automatically init components inserted into DOM after DOMContentLoaded)

and without using any 3rd party libraries or frameworks we created a custom modern component which can be re-used in absolutely every web application around the world.

We, of course, may create a core abstract Component object to make our life even easier and I have created an [experimental Component](https://github.com/mevrael/bunny#experimental-components-based-on-domobserver-mutation-observer) as a part of [**BunnyJS**](https://bunnyjs.com) **— modern JS and ES6 library, set of stand-alone Vanilla JS components which just works everywhere.** DataTables in 6kb, Form Validation in 6kb and mentioned Component+DOMObserver [component.min.js](https://unpkg.com/bunnyjs/dist/component.min.js) only 2.8kb. Not talking about the helpers/utils like BunnyDate, BunnyURL, BunnyFile, BunnyImage, DOM utils like onClickOutside(), accessible addEventKeyNavigation() and many others.

> After so many years we still don’t have a Vanilla JS components while we have over 9000 datepickers, dropdowns, datatables and other widgets coupled only to a jQuery or React or Angular or Vue or another framework’s of the day implementation.

BunnyJS is not a hype and it still may suck in some ways, however, if you would like to make JavaScript great again, any feedback or contributions would be very appreciated.

### If you liked this article please press the ❤ button, share the article and star the project on GitHub.

I hope this article will bring us more Vanilla JS components in the future.

> “Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away.”
>
> — Antoine de Saint-Exupery

## Useful links:

\_\_\_

[*Mev-Rael*](https://linkedin.com/in/mevrael) *is the founder, and CEO of* [*ATHENNO*](https://athenno.com) *— a modern startup, #JTBD and #ContinuousDiscovery E2E platform that makes entrepreneurship and commercial innovation accessible and successful to all on Earth | He is a Global UX, JTBD, Product, and Innovation Management Consultant for Startups | Author, Speaker | Philosopher-Warrior | Born Global Leader | A+ Player | ENTJ-A | Before that — an experienced software architect working with the Web and the Internet technologies for more than 10 years.*