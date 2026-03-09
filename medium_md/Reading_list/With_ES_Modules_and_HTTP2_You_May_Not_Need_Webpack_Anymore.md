---
title: "With ES Modules and HTTP/2 You May Not Need Webpack Anymore"
url: https://medium.com/p/d25f04870284
---

# With ES Modules and HTTP/2 You May Not Need Webpack Anymore

[Original](https://medium.com/p/d25f04870284)

# With ES Modules and HTTP/2 You May Not Need Webpack Anymore

## It’s time to fully embrace import/export

[![Joe Honton](https://miro.medium.com/v2/resize:fill:64:64/1*l7MKzaAQf9CUiPD56f9CDA.png)](/@joehonton?source=post_page---byline--d25f04870284---------------------------------------)

[Joe Honton](/@joehonton?source=post_page---byline--d25f04870284---------------------------------------)

8 min read

·

Jan 15, 2020

--

2

Listen

Share

More

Press enter or click to view image in full size

![JavaScript modules over multiplexed streams]()

*With JavaScript modules fully supported in every major browser, savvy developers can now deliver production-ready apps without Webpack.*

Front-end Web developers are on the cusp of a new way of putting their apps into production. The need for transpilers and bundlers is disappearing now that browsers finally have support for `import` and `export` using ECMA-262 standards-compliant modules.

Until now the final outlier, Microsoft Edge, was holding us back from deploying ES modules in the wild. Today, with the release of Chromium-based Edge 76, every major browser supports the new module standard. This has huge implications for how we build and deploy our code.

To understand my point of view, allow me to share some backstory highlights.

Getting to where we are today has been a long road, traversing a bumping landscape of performance analyzers, task runners, transpilers, bundlers, and a major overhaul of the HTTP protocol.

## The Yahoo! Era

In 2005, Yahoo published an article that would go on to become something of a front-end bible. Looking back from today’s constellation of stars, Yahoo appears to be a dimly lit speck of dust. But in a Time magazine ranking of “The 15 Most Influential Websites of All Time”, Yahoo! comes in at number seven.

The article that caused all the commotion was titled “Best Practices for Speeding Up Your Web Site.” At the top of that list was its golden rule to *minimize HTTP requests*. The advice it dispensed for how to accomplish that was unequivocal: Combine all of your scripts into a single file.

At that time, combining your scripts was an easy commandment to follow. Most of what we wrote were simple event listeners that manipulated the user interface. More sophisticated websites might occasionally write a function that fired an `XMLHttpRequest` to retrieve data.

Either way, regardless of what we wrote during this era, it was all placed in the global scope. So when our websites evolved to have ever greater interactivity, the use of global scoping became increasingly problematic. How do you name a function that iterates over a list of things, and how do you keep that name separate from others that are similar? Names like `iterateThing1()` and `iterateThing2()`would not be unheard of.

During this era, I had one client whose entire 20,000 line codebase was in one file. Every developer on the team was working on it at the same time! Something had to give.

## The AMD and CommonJS Era

As programmers, we weren’t encountering anything new here. Defining local namespaces has been a common need that every major programming language has had to grapple with. And modularizing code at the file level has been the solution in almost every case. Unfortunately for JavaScript developers at this time, the language had not yet matured enough to allow this.

Solutions at the application level arrived instead, in the form of the asynchronous module definition (AMD) spec, and the `RequireJS` implementation of it. With this solution, everything within a file was wrapped in its own context, isolating its functions and variables from the outside, effectively preventing name clashes. Each file was a unit unto itself. In order to use that unit, the developer would choose what to make visible to the outside world by wrapping the target with a `define()` function. And any other unit that wanted to access it, would do so using a `require()` function.

While this was happening on the front end, Node.js was busy wrangling with the same problem on the back end. Their solution was the CommonJS module system. In that system, the developer would choose what to make visible to the outside world through the declaration of a `module.exports` statement. Any other unit that wanted to access those exports would do so with a `require` statement.

Two different solutions to the same problem.

Fast forward to 2015 when ECMAScript’s TC39 committee got into the fray and officially announced new language features that directly addressed the need for modular code. Modules, they announced, would have first-class language support through two new keywords: `import` and `export`. This put an end to the argument.

But announcing something and implementing it are two different things. It wasn’t until late 2017 that the first implementation arrived in the Chrome browser. It would take another two and a half years for `import/export` to be fully supported across all the major browsers.

The full story of AMD, CommonJS, and ES Modules doesn’t need to be recounted here. But the consequences resulting from the protracted rollout of `import/export` are important to my story. The fallout has been that developers wanting the benefits of modular code have had to choose: either write using the older module syntax or write with the new syntax and *transpile* it back to the old syntax for deployment.

For my projects, I chose to write with the new syntax. And in order to deploy code to production, I used a purpose-built CLI tool, that I called [eximjs](https://hub.readwritetools.com/tasks/eximjs.blue), which converted `import` and `export` statements into CommonJS statements. When I wrote that tool, I thought that it would have a short life. I had no expectation that I'd be using it for five years!

## The Bundler Era

Seeing what the future held in store for them, many projects chose to get ahead of the inevitable by using transpilers. Babel became the undisputed champion in this field. It solved the module syntax problem perfectly, while also providing polyfills and shims for the other new features announced by TC39.

In order to make this work, front-end developers began walking away from the simple *scripting* workflows that they had grown up with, and started moving towards a *build process*. That drove the need for task runners: tools that could operate as a sequence of steps. Initially, Grunt and Gulp fulfilled this need. We used them to establish build processes that transpiled, linted, tested, and minified source code files whenever they changed.

Modularized architectures became a reality and developers went all in. The namespace problem had been solved.

It was the DevOps guys who first noticed that this new approach created its own set of problems. Or rather, it resurfaced the old problem that Yahoo had so carefully identified all those years ago. Lots of little files meant lots of HTTP requests, which meant longer load times. But we weren’t going to stop designing modular architectures just for that. We needed a different approach.

The new approach came in the form of bundlers. The task runners we had been using were replaced by new tools that parsed our JavaScript and determined its dependencies. Those dependent modules were concatenated into a bundle and sent down the wire in a single HTTP request. DevOps was happy.

Everybody retooled their build process, dropping task runners and replacing them with bundlers like Browserify or Webpack. Soon after, competition arrived in the form of Parcel, which relieved much of the configuration overhead needed by Webpack, and Rollup, which concentrated on isomorphic JavaScript and the desire to bundle ES Modules.

Over time, many interesting problems have been solved by bundlers. For example, *tree-shaking* and *chunking* were major improvements to the build process. At the other end, in the browser, *code splitting* and *lazy loading* were significant optimizations for bundles arriving at their target. Today, the bundler toolscape is alive and well, and performance improvements related to bundle size and caching are underway.

But there’s something amiss in all this. The original problem was HTTP’s head of line blocking problem, so carefully called out by Yahoo. Then it became the namespace problem as our applications became more sophisticated. Then it became the language deficiency problem as we waited for TC39 to precisely specify how the new module loader was supposed to work. And in the interim, it became the bundler performance problem as we tried to balance all the competing needs for faster transpilation, on-demand loading, and caching.

## The 2020 Era

But let’s take a breather and reexamine these problems in the broader context of the full Web stack. In particular, let’s look at them in the context of HTTP.

Even while the module drama was unfolding, a solution to our original performance problem was arriving in the guise of HTTP/2. This update to the classic Web protocol that we all know so well provides two major improvements that are important to my story: persistent connections and multiplexed streams.

Here’s how it works. With HTTP/2 the request for an HTML document opens a connection between the browser and the server, which stays open until everything that’s needed has arrived. Moreover, as the browser discovers what it needs (images, fonts, scripts, styles) it requests them without pausing or waiting for the response to be completely fulfilled. This works because the new protocol has multiplexed streams, so all of these requests can be in motion simultaneously. In brief, the head of line blocking problem becomes moot.

Now allow me to briefly digress. Upon hearing about HTTP/2, I naturally looked for a web server that supported the new protocol together with the Node.js libraries I was writing. I wasn’t happy with anything I saw at the time. That became my catalyst for creating the [Read Write Serve](https://hub.readwritetools.com/enterprise/rwserve.blue?utm_term=TheRolloutOfModulesIsComplete) HTTP/2 Server. Today, I use this server on every new project, and I can attest to the new protocol’s advantages. Persistent connections and multiplexed streams deliver as advertised.

This new protocol relates directly to my tenet, that bundlers will soon become a relic of the past. Since HTTP/2 so beautifully accommodates many files, there’s no need for applications to separately handle any part of that optimization.

The advantages afforded by HTTP/2 together with native ES Modules are manifold:

* Transpilation is no longer necessary when JavaScript `import` and `export` language statements are used.
* Source maps are no longer required for debugging because source code is not mangled by the transpiler.
* No complicated heuristics are needed to guess at optimal chunk boundaries because chunks aren’t a thing.
* No administrative code is needed for splitting bundles because modules arrive as discrete named files.
* No lazy loading optimizer is needed because the browser requests scripts and resources only when it needs them.
* No tree shaking is needed because the browser only requests the dependents it discovers.
* Caching by the browser, server, and content delivery network can all fully utilize HTTP’s `cache-control`, `if-none-match`, and `etag` headers, saving network bandwidth and improving throughput.
* File compression can be fine-tuned by the DevOps staff using the best approach available for each mime-type.

Compared to HTTP/1.1 with bundlers, HTTP/2 with native ES Modules is a clear winner. In short, source code files can go directly to production, without all the code slinging madness that we’ve created for ourselves.

We’ve been treating JavaScript like a compiled language for so long that we’ve forgotten that it’s actually an interpreted language. Yes, we may still want to use linters and minifiers, to keep things tidy, but all the other manglers are just counter-productive.

In brief, if you have any influence over your team’s choice of build tools, now is a good time to rethink exactly why you need Webpack.

Keeping it simple is the smarter way to succeed.