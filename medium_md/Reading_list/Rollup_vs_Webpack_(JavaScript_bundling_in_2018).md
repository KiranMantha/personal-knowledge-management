---
title: "Rollup vs Webpack (JavaScript bundling in 2018)"
url: https://medium.com/p/b35758a2268
---

# Rollup vs Webpack (JavaScript bundling in 2018)

[Original](https://medium.com/p/b35758a2268)

# Rollup vs Webpack (JavaScript bundling in 2018)

[![Luke Boyle](https://miro.medium.com/v2/resize:fill:64:64/1*rpnrZxAj776AsuUbpZqDIQ.png)](/@3stacks?source=post_page---byline--b35758a2268---------------------------------------)

[Luke Boyle](/@3stacks?source=post_page---byline--b35758a2268---------------------------------------)

4 min read

·

Feb 22, 2018

--

5

Listen

Share

More

![]()

Although tooling standards have begun to stabilise in JavaScript land, there’s still a bit of confusion around the right tool for the job. This is a somewhat detailed comparison between Rollup and Webpack. Let’s start by comparing their respective configuration files.

## Configuration

### rollup.config.js

### webpack.config.js

Quick differences to note:

Rollup has node polyfills for import/export, whereas webpack doesn’t

Rollup has support for relative paths, whereas webpack does not, so we either use path.resolve or path.join

Rollup requires you have modules set to false on es2015 presets, because it will process modules as ES2015 if it can and do scope hoisting magic before transpiling the module.

Let’s take a very simple example:

### some-file.js

### index.js

What would you expect the output of this be?

This is arguably where Rollup shines. For simpler modules, it returns a very efficiently transformed, minimal bundle, whereas Webpack has a lot of magic™ included in the bundle.

### bundle.rollup.js — ~245 bytes

### bundle.webpack.js — ~4108 bytes

In the Webpack bundle, the actual imports occur on around line ~100. If you navigate to this point, you will see that the actual module code is **mostly** the same (below), with the biggest difference being that in the Webpack bundle, each module is wrapped in a function which can be internally invoked. This is why Webpack bundles are considered to be ‘safer’ for larger/more complex applications.

A lot of the mess is removed in production mode builds and the bundle size.

So, how do you tell which one is right for you? In recent history, the conventional wisdom has been:

> ***“Use webpack for apps, and Rollup for libraries”***

However, it’s becoming more difficult to justify this as a rule. Webpack enhancements have really levelled the playing field in terms of general bundling efficiency, and Rollup recently added [code splitting](/rollup/rollup-now-has-code-splitting-and-we-need-your-help-46defd901c82) (the major lacking features between the two).

To make a real life parallel, I’d compare this bundler battle to the product design theory called the “Kano model”. The Kano model essentially states that “over time, delightful innovation becomes another basic need”.

Take for example the arrow on the fuel gauge of a car to indicate which side to face the fuel pump (figure 1). When the idea was conceived, it was considered to be a great innovation, however, now it is simply an expectation amongst users.

![]()

To see the real differentiating features, we have to go back to the wild west of 2016.

## Rollup (circa 2016)

### Pros:

* Tree shaking (live code inclusion / dead code elimination)
* esnext:main entry in package.json to import es2015+ (renamed to ‘module’)
* Scope hoisting
* Simple API

### Cons:

* Limited support for alternative file type loading (css, images etc)
* No code splitting

## Webpack (circa 2016)

### Pros:

* Advanced support for CSS/HTML/image loading
* Code splitting
* Hot module replacement for super fast dev builds

### Cons:

* No tree shaking
* No Scope hoisting
* No native support for ES2015+ modules
* Complicated API

A lot has changed since then (the above is not an exhaustive list, and both of the libraries have additional pros and cons I couldn’t possibly list), and both libraries have taken cues from one another. The community surrounding both libraries has also grown which has helped accelerate the implementation of novel features.

## Rollup (now) — What’s changed?

* Rich ecosystem of plugins for file loading/dev servers
* Code splitting (Added 8th of Feb 2018 after a 2 year wait! 🎉🎉)

## Webpack (now) — What’s changed?

* Tree shaking & ES2015+ module support (Added in Webpack 2)
* Scope hoisting (Added in Webpack 3)
* Support for esnext:main / module

In my opinion, you should still probably prefer Rollup for libraries, but the option of using Rollup for large apps is much more realistic now. One thing’s for sure, both Webpack and Rollup are here to stay. I’d say the main reason for the staying power of these two libraries is the amazing internal teams and the unending effort they put into maintaining them and answering issues and StackOverflow questions.

For a more detailed comparison of the internals of the two libraries, Rich Harris (creator of Rollup) has a great writeup [here](/webpack/webpack-and-rollup-the-same-but-different-a41ad427058c).

## BONUS: A challenger approaches

[Parcel](https://parceljs.org/) is a new and interesting bundler that has many of the same features as Rollup and Webpack (e.g. code splitting and asset loading), but the big feature it’s touting is a zero-configuration get up and go solution for bundling. If you were around in the community in 2015, you’d remember the infamous blog post [“JavaScript Fatigue”](/@ericclemmons/javascript-fatigue-48d4011b6fc4). One of the points the author makes is our tooling was just a mess, and it was. The world hadn’t decided which tools we should be using so most of my projects were a mixture of Gulp, browserify (with babelify) and getting started was never easy.

With Parcel, the selling point is that you have an index.html file which points to a JavaScript entry, and you can just run `parcel index.html` and have a fancy dev server running in moments. It also brags that it has blistering fast bundle speeds (though their comparison table omits a Rollup comparison, so I can only assume they are similar).

If Parcel proves to have the staying power as Webpack/Rollup, I’m sure we’ll see many of the zero configuration features bubble to the surface in those libraries.