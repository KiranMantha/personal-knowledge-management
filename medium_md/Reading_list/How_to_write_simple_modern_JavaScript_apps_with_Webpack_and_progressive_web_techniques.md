---
title: "How to write simple modern JavaScript apps with Webpack and progressive web techniques"
url: https://medium.com/p/a30354eab214
---

# How to write simple modern JavaScript apps with Webpack and progressive web techniques

[Original](https://medium.com/p/a30354eab214)

# How to write simple modern JavaScript apps with Webpack and progressive web techniques

[![Anurag Majumdar](https://miro.medium.com/v2/resize:fill:64:64/1*hUChU0coEQIqI4pCYCjQ4A.jpeg)](/@anurag.majumdar?source=post_page---byline--a30354eab214---------------------------------------)

[Anurag Majumdar](/@anurag.majumdar?source=post_page---byline--a30354eab214---------------------------------------)

12 min read

·

Feb 26, 2019

--

5

Listen

Share

More

![]()

Have you thought about making modern JavaScript applications with the simplest setup possible for your next project?

If so, you have come to the right place!

JavaScript frameworks exist to help us build applications in a generalized way with most of the common features. But most of the applications may not need all the powerful features of a framework. It may be overkill to just use a framework for specific requirements (especially small to medium scale projects).

Today I am going to show an approach to how you can use modern features and build your own customized Web Applications. You can also build your own framework on top of the sample applications if you want to. That is purely optional. The power of Vanilla JavaScript enables us to follow our own coding style irrespective of the tools used.

## What We Need

Before starting out, let us quickly skim through the features we need.

### Architectural Planning

To ensure fast loading and consistent experiences, we’ll use the following patterns:

* Application Shell Architecture
* PRPL (**P**ush, **R**ender, **P**re-cache, **L**azy loading) pattern

### Build Setup

We need a good custom build setup, so we will be using Webpack with the following requirements:

* ES6 & Dynamic Imports support
* SASS & CSS support
* Custom development & production setup
* Custom Service Worker Build

### Bare Minimum JavaScript Features

We will be touching on minimal JavaScript features to get us off the ground and produce the output we require. I will show you how we can use existing JavaScript ES6 features in our day to day vanilla applications. Here they are:

* ES6 Modules
* Dynamic Imports
* Object Literal Syntax Or ES6 Class Syntax
* ES6 Arrow Functions
* ES6 Template Literals

At the end of this article there is a sample application demo along with its source code on GitHub. Let’s dig deeper, shall we? 🙌

## Architectural Planning

The advent of **Progressive Web Applications** has helped bring new architectures in order to make our first paint more effective. Combining **App Shell** and **PRPL** patterns can result in consistent responsiveness and app-like experiences.

### What is App Shell & PRPL?

**App Shell** is an architectural pattern for building **Progressive Web Applications** where you ship the minimal **critical resources**in order to load your site. This basically consists of all the necessary resources for the first paint. You may cache the critical resources as well using a service worker.

**PRPL** refers to the following:

* **P**ush critical resources (especially using HTTP/2) for the initial route.
* **R**ender the initial route.
* **P**re-cache remaining routes or assets.
* **L**azy load portions of an application as and when required (especially when required by a user).

### What Do These Architectures Look Like In Code?

The **App Shell** and **PRPL** pattern are both used together to achieve the best practices.

The App shell looks somewhat like the following piece of code:

You can see that the application shell consists of the bare minimum markup as a skeleton.

**Lines 9–82**: Critical styles have been introduced into markup to ensure direct parsing of CSS instead of linking it to another file.

**Lines 89–96**: Main application shell markup; these areas will be later manipulated by JavaScript (especially, the contents inside the main tag of line 93).

**Line 99**: This is where the scripts come into play. The **async** attribute helps in not blocking the parser while the scripts get downloaded.

The app shell also enforces **Push** & **Render** stages of the **PR**PL pattern. This happens when HTML is parsed by the browser to form pixels on the screen. It readily finds all the critical resources. Also, the **critical scripts** are responsible for showing the **initial route** by DOM manipulation (**Render**).

However, if we do not use a Service worker to cache the shell, it won’t be of any use for future reloads and performance benefits.

The following code snippet shows a service worker which caches the shell and all the static assets required for the application.

**Lines 4–17**: The install event of service workers helps to cache all the static assets. Here, you can cache the app shell resources (CSS, JavaScript, images, etc.) for the first route (as per App shell). Also, you can cache the remainder of the assets of the application ensuring the whole app can run offline too. This caching of static assets apart from the main app shell ensures the **Pre-cache** stage of the PR**P**L pattern.

**Lines 19–38:** The activate event is the place for cleaning up of unused caches.

**Lines 40–63**: These lines of code help in fetching resources from the cache if they are in cache or go to network. Also, if a network call is made, then the resource is not in cache and put into a new separate cache. This scenario helps to cache all dynamic data for an application.

All in all, most of the parts of the architecture have been covered. The only part left is the **Lazy loading** stage of the PRP**L** pattern. I will discuss this with regards to JavaScript.

## Our Build Setup

What is a good architectural structure without a build setup? Webpack to the rescue. There are other tools like Parcel, Rollup etc. out there, but whatever concepts we apply to Webpack can be applied to any such tool.

I will map the concepts used to the plugins so that you can get hold of the basics used for setting up of the workflow. This is the most important step to getting started with a good reusable build config for your own application for the future.

I know how difficult it is for developers like us to configure Webpack or any tool for that matter from scratch. The following article was an inspiration which helped me to create my own build setup:

[A tale of Webpack 4 and how to finally configure it in the right way. Updated.](https://hackernoon.com/a-tale-of-webpack-4-and-how-to-finally-configure-it-in-the-right-way-4e94c8e7e5c1)

Do refer to the above link if you get stuck anywhere with the build setup. For now let us check out the concepts required for the build.

### ES6 & Dynamic Imports support

**Babel** is a popular transpiler which is there to help us with transpiling ES6 features down to ES5. We will need the following packages to enable babel working with webpack:

* @babel/core
* @babel/plugin-syntax-dynamic-import
* @babel/preset-env
* babel-core
* babel-loader
* babel-preset-env

Here is a sample babelrc for reference:

During babel setup, we need to feed the following **2nd line** in presets to enable babel to transpile ES6 down to ES5 and the **3rd line** inplugins to enable the dynamic import support with Webpack.

Here is how babel is used with Webpack:

**Lines 10–17**: The babel loader is used to set up the babel transpilation process in webpack.config.js. For simplicity, the other parts of the config have been eliminated or commented out.

### SASS & CSS Support

For setting up SASS and CSS you need the following packages:

* sass-loader
* css-loader
* style-loader
* MiniCssExtractPlugin

Here is how the config looks like:

**Lines 17–25**: This is the area where the loaders are registered.

**Lines 29–31**: Since we are using a plugin to extract a CSS file, we are using the **MiniCssExtractPlugin** here.

### Custom Development & Production Setup

This is the most important section of the build process. We all know that we need a development and production build setup for developing applications and also deploying the final distributable to the web.

Here are the packages that will get used:

* **clean-webpack-plugin**: For cleanup of the dist folder contents.
* **compression-webpack-plugin**: For gzipping the dist folder file contents.
* **copy-webpack-plugin**: For copying static assets, files or resources from application source to dist folder.
* **html-webpack-plugin**: For creating an index.html file in the dist folder.
* **webpack-md5-hash**: For hashing application source files in the dist folder.
* **webpack-dev-server**: For running a local development server.

Here is the final Webpack config file:

**Lines 9–77:** The entire webpack config is a function which takes two arguments. Here I have used the **argv** i.e., the arguments sent while running the webpack or webpack-dev-server commands.

The below image shows the scripts section in package.json.

Press enter or click to view image in full size

![]()

Accordingly, if we run **npm run build** it will trigger a production build, and if we run **npm run serve** it will trigger a development flow with a local development server.

**Lines 44–77**: These lines show how the plugins and the development server config needs to be setup.

**Lines 59–66**: These lines are any resources or static assets which need to be copied over from the application source.

### Custom Service Worker Build

Since we all know how tedious it is to write the names of all the files again for caching, I made a custom service worker build script for catching hold of the files in the **dist** folder and then adding them as contents of the cache in the service worker template. Finally, the service worker file will get written to the **dist** folder.

The concepts regarding the service worker file we talked about will be the same. Here is the script in action:

**Lines 8–18**: This is the place where all the contents of the dist folder are captured as an array **staticAssetsCacheFiles.**

**Lines 22–85**: This is the service worker template we talked about before. The concepts are exactly the same, just that we are introducing variables into the template so that we can reuse the service worker template and make it handy for future use. This template was also required since we needed to add **dist** folder contents to the cache as per **line 33**.

**Lines 87–90**: Finally, a new service worker file will get written to the **dist** folder along with its contents from the service worker template **serviceWorkerScript**.

The command to run the above script is **node build-sw** and it should be run after **webpack --mode production** is done.

This service worker build script really helped me a lot in caching files easily. I am currently using this for my own side projects due to its simplicity and great ease of tackling the caching problem.

If you guys want to use a library for Progressive Web Application related features, you can go for [Workbox](https://developers.google.com/web/tools/workbox/). This library does some real neat stuff and has amazing features which you can take control of.

### Final Look At The Packages

Here is a sample package.json file with all dependencies:

Remember that Webpack gets updated frequently, and changes keep happening in the community with new plugins replacing existing ones. So it is important to keep a note of the concepts required for a build setup rather than the actual packages used.

## JavaScript Features

We all have a choice: either to write our own framework for certain features to be used by our application such as change detection, routing, storage patterns, redux etc, or pull already existing packages for such features.

Now I’ll speak about the bare minimum features required in order to structure the layout of our application and get it going. Later on you can add your own frameworks or packages to the application.

### ES6 Modules

We will use ES6 import and export statements and treat each file as an ES6 module. This feature is commonly used by popular frameworks like Angular and React and is pretty handy. With the power of our Webpack config, we can fully utilize the power of import and export statements.

### Object Literal Syntax Or ES6 Class Syntax

Building components is a very important part of our application. We can choose to go with the latest web standards like Web Components too, but to keep things simple we can go ahead and use object literal syntax or ES6 class syntax.

The only thing with class syntax is that we need to instantiate it and then export it. So to keep things even simpler, I went ahead with object literal syntax for component architecture.

**Lines 4–32:** We export an object called **AppComponent** which is immediately available for use in other parts of our application.

You can go ahead and use ES6 class syntax or standard Web Components too and achieve a more declarative way of writing code here. For simplicity’s sake, I chose to write the demo application in a more imperative approach.

### Dynamic Imports

Remember I talked about missing out on the “L” of the **PRPL** pattern? Dynamic import is the way to go ahead and lazy load our components or modules. Since we used the **App Shell** and **PRPL** together to cache the shell and other route assets, dynamic imports import the lazy component or module from the cache instead of the network.

Note that if we only used **App Shell** architecture, the remaining assets of the application i.e., the contents of **chunks** folder, would not have been cached.

**Lines 15–19:** Refer to App Component code; this is the place where dynamic imports shine. If we click on a button having the class **btn-todo,** then only this **TodoModule** gets loaded. By the way, **TodoModule** is just another JavaScript file which consists of a set of object components.

### ES6 Arrow Functions & ES6 Template Literals

Arrow functions should be used especially where we want to make sure of the **this** keyword inside the function, which should refer to the surrounding context where the arrow function is declared. Apart from that, these functions really help in creating neat shorthand syntax.

The above example is a template function defined as an arrow function which accepts a model and returns an HTML string consisting of the model data in it. String interpolation is carried out with the help of **ES6 template literals**. The real benefit of template literals is **multi-line strings** and **interpolation** of model data into the string.

Here’s a micro tip for handling component templating and generation of reusable components: use the **reduce** function to accumulate all HTML strings as per the following example:

The above piece of code does a great deal of work indeed. Simple yet intuitive. It does follow a little inspiration from the frameworks out there.

**Lines 1–19**: This is a sample model array on which the reduce function can run in order to give the reusable template feature.

**Line 53:** This line does all the magic in generating multiple reusable components into one HTML string. The reduce function takes in the accumulator as the first argument, and each value of the array as the second argument.

Thanks to these simple features, we already have an application structure in place. The best way to learn a feature is to put it in action they say, so here we are. 😎

## Application Demo

Congratulations on reaching here!

This post covered a lot of features indeed and getting hold of all the concepts and techniques will take some time.

Here is a demo of the to-do application built with all the features as discussed in this article. [Click here](https://vanilla-todos-pwa.firebaseapp.com/) to visit the site.

Press enter or click to view image in full size

![]()

[Click here](https://github.com/anurag-majumdar/vanilla-todos-pwa) for the link to GitHub repository. Feel free to clone the repository and go through the code for a better understanding of the conceptual examples mentioned in the article.

## Sample Production App

The production site is a portfolio which was designed, developed and engineered from scratch using the exact features as specified in this article. The **Single Page Application** is broken down into custom **modules** and **components**.

The flexibility and power that comes with **Vanilla JavaScript** is something unique and does help in producing some astonishing results.

[Click here](http://www.anurag-majumdar.com) to go to the site. Here is the site in action:

Press enter or click to view image in full size

![]()

Do visit the site to get a feel for it. The colors are not accurately produced in the demo here. The engineering put into this site produced the following results:

Press enter or click to view image in full size

![]()

Never scored a perfect 100 before in any subject. 🙏

## Conclusion

There are several projects we might like to build using Vanilla JavaScript instead of frameworks in order to achieve certain results quickly. I wrote this article to help developers use a simple custom setup to build their future projects.

The best part about the Vanilla framework is that developers have the freedom to shape their engineering thought patterns according to various use cases. Be it Imperative or Declarative style of programming, creating or using of latest existing features. As long as we produce consistent and performant applications with good code maintainability, our job is done for the day.

Happy hacking! 😄

## Other Posts By Me

Find me at [https://medium.com/@anurag.majumdar](/@anurag.majumdar)

### ➥ Web Development

* [Progressive Web App Shell: The Key To Loading Your Site Under 1 Second!](/udacity-google-india-scholars/build-your-own-reusable-app-shell-from-scratch-7823f65e1fbd)
* [“Super” and “Extends” In JavaScript ES6 — Understanding The Tough Parts](/beginners-guide-to-mobile-web-development/super-and-extends-in-javascript-es6-understanding-the-tough-parts-6120372d3420)
* [Introduction To Polyfills & Their Usage](/beginners-guide-to-mobile-web-development/introduction-to-polyfills-their-usage-9cd6db4b1923)

### ➥ Life Event

* [Udacity’s Google Mobile Web Scholarship Challenge and its glorious effects!](/@anurag.majumdar/udacitys-google-mobile-web-scholarship-challenge-and-its-glorious-effects-9cd4979f5053)