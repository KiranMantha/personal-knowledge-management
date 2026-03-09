---
title: "Why I use Rollup, and not Webpack"
url: https://medium.com/p/e3ab163f4fd3
---

# Why I use Rollup, and not Webpack

[Original](https://medium.com/p/e3ab163f4fd3)

Press enter or click to view image in full size

![]()

# Why I use Rollup, and not Webpack

[![Paul Sweeney](https://miro.medium.com/v2/resize:fill:64:64/1*H-gZm2LZtr6xzfK8pAKVbQ.jpeg)](/@PepsRyuu?source=post_page---byline--e3ab163f4fd3---------------------------------------)

[Paul Sweeney](/@PepsRyuu?source=post_page---byline--e3ab163f4fd3---------------------------------------)

10 min read

·

May 5, 2020

--

6

Listen

Share

More

Complexity, frustration, bloated. Those are the first words that come to my mind whenever I see Webpack. Over the past several years, I’ve been building numerous web apps, from relatively simple apps to far more complex ones that require [scalable architectures](/@PepsRyuu/micro-frontends-341defa8d1d4). For the past couple of years in particular however, I’ve stopped using Webpack to develop them, opting instead to use Rollup as my primary bundler for apps.

Saying that alone might trigger a reaction from readers already. You might have heard of the old saying **“*Rollup for libraries, Webpack for apps*”**. You probably have several complaints, but they’re likely no longer applicable. The functionality gap between all of the bundlers has been narrowing over the years, and these days, it’s not so much functionality that matters, but rather the developer experience.

## Why do we use bundlers again?

Historically, bundlers have been used in order to support CommonJS files in the browser, by concatenating them all into a single file. Bundlers detected usages of `require()` and `module.exports` and wrap them all with a lightweight CommonJS runtime. Other benefits were allowing you to serve your app as a single file, rather than having the user download several scripts which can be more time consuming.

![]()

But browsers have changed a lot over the years. Browsers *natively* support ES Modules, and the vast majority of developers use ES Module syntax. Also HTTP/2 helps to speed up network performance via multiplexing. So why the need still?

Unfortunately, many third party libraries, even though they are written in ESM, are published to npm as CJS modules, so we still need to concatenate them. We also use bundlers so that they can resolve package identifiers, as well as package other type of assets such as CSS and images. A bundler can help transform assets into something more manageable than manually maintaining them.

![]()

With that in mind, let’s talk about the most popular bundlers.

## Webpack, Parcel, Rollup

Each of these bundlers are very similar these days in terms of functionality. They inspire each other to improve and are all pushing the JavaScript ecosystem forward and over time improving the developer experience. But while the objective may be similar, there are core differences with how they approach that objective, most of which comes down to preferences.

### **Webpack**

Webpack is one of the oldest bundlers, and was created in an era where CommonJS was the norm. At the time, developers wanted to reuse NodeJS modules in the browser, so tools like Browserify, which wasn’t designed to be a bundler, came onto the scene and decided that concatenating the modules was the best way to get them working in browser. Webpack extended this concept and also supported bundling all assets that go into a web app, including styles and images.

Over the years, Webpack added a bunch of other features that we now take for granted, such as dev servers with Hot Module Replacement, and code-splitting, drastically improving both the developer experience and the end-user experience.

![]()

In my opinion, because Webpack was one of the first bundlers, is heavily packed with features, and has to support swathes of legacy code and legacy module systems, it can make configuring Webpack cumbersome and challenging to use. Over the years, I’ve written package managers, compilers, and bundlers, and I still find configuring Webpack to be messy and unintuitive.

While Webpack has made some improvements in terms of defaults, if you need to do any sort of customisation, you have to start overriding those defaults and fighting against the bundler.

Press enter or click to view image in full size

![]()

Personally for me, this is incredibly hard to read. Regex everywhere, nested objects with different rules and configurations that are very intuitive, multiple loaders that resolve backwards, built in loaders having obscure issues that require using third party loaders in between, separation of plugins and loaders, and so on.

Aside from configuration, I’m also not satisfied with the output that Webpack generates. Every bundle Webpack produces, will always have the CommonJS runtime, and some modules will still require function scopes. I’ve also had plenty of issues with dynamic imports taking a variable instead of a string, and CSS loaders leaving empty function scopes.

Press enter or click to view image in full size

![]()

![]()

I care very much about the number of bytes I’m sending to my users, so this is a huge deterrent for me. For writing libraries, this is an automatic no. If every library had this extra code with it, you’d be shipping megabytes of JavaScript in no time at all. For apps, it’s not as significant to have this extra boilerplate, but **we should also care about how much JavaScript we’re sending** in every context, not just libraries.

### Parcel

Okay, so you might be thinking, if I hate configuration so much, how about zero configuration instead? Parcel popularised the idea of zero configuration for bundlers when it bounced into the ecosystem. Rather than having any config, it will determine how to behave based on your `index.html` file and generate files from that. It supports a wide variety of file types out of the box, **without you needing to do anything at all**. No need to configure any loaders for common file formats, including images and CSS.

![]()

**This works great for simple projects. However, it’s just not realistic when your working with larger scale projects.** In software development, there’s always a trade-off between generic code and optimisation. Optimisations usually are tailored specifically towards your project and your use case. In this case, if we want to optimise the code being sent to the end-user, we need to have configuration. Even the developers behind Parcel recognised this, and Parcel 2 [actually has configuration](https://github.com/parcel-bundler/parcel#parcelrc) with reasonable defaults.

![]()

As Parcel also provides a lot of defaults out of the box and built-in loaders, it means more overriding, and more fighting against the bundler rather than working with it. There’s nothing necessarily wrong with the zero-configuration approach though. Other projects such as `create-react-app` have been very successful in creating tooling where you can get up and running immediately, **and for beginners, I highly recommend using such projects.**

But as someone who’s very familiar with bundlers and wants to output the best possible and optimal code, it’s not for me.

### Rollup

While Webpack is focused on using CommonJS as its primary module system and converting everything to that, Rollup decided to take the opposite approach — **focusing on ES Modules instead**. One of the core differences between CommonJS and ES Modules, is that CJS is a dynamic module system. You have to call a function `require()` and pass exports to an object called `module.exports` . This is executed at runtime. ESM on the other hand, the `import` and `export` statements are treated as syntax and are parsed before the module is executed.

This might not seem like a lot initially, but it allows you to do some very interesting optimisations. **Because ESM is syntax, it’s very easy to statically analyze**. Without running any code, a tool can tell what modules are being imported and exported. This is also why dynamic `import()` isn’t really a function, but syntax.

Press enter or click to view image in full size

![]()

Rollup takes advantage of this to implement tree-shaking and scope-hoisting. Tree-shaking removes unused code, which we can determine via the imports, and scope-hoisting removes the need to wrap each module in a function scope because there’s no `require` or `module` objects that need to be passed in.

![]()

Rollup also does something very different compared to the other bundlers. **It only tries to achieve one simple goal: Bundle ES modules together and optimise the bundle.** It doesn’t understand node module imports, it doesn’t know what to do with CSS, it certainly can’t understand images. Instead, rather than trying to implement what it thinks is the best way to bundle different type of assets, it leaves that entirely up to the developer to decide.

Want to load node modules? You could use`@rollup/plugin-node-resolve` , but if that doesn’t satisfy you, you can use your own module resolver instead. The benefit of this approach is that rather than having these defaults and fighting against them, **it’s fully up to you to decide how to handle everything**. This is very useful for simplifying configuration, and for future-proofing. In my opinion, **configuring Rollup is far easier** than configuring for Webpack.

![]()

Rollup is not without its faults though. The biggest issue with Rollup is that it only provides one feature, **creating production bundles**. There’s not really any developer experience, apart from a couple of options like file watching and caching. It can’t produce development bundles, doesn’t provide a web server, and only reads relative ES modules by default.

But in my opinion, this isn’t actually a bad thing, instead, it provides an opportunity for us to fill in the gaps ourselves.

## Hot Module Replacement

When you talk about Rollup as an application development tool, this is probably one of the first issues that developers will bring up. Because Rollup doesn’t provide any web server, and it always generates a production bundle, it’s pretty much impossible for HMR to exist, or at least not efficiently. I’ve done extensive research into using the existing plugin API to see if it’s possible, and it’s just not feasible without running into significant performance hurdles.

For a bundler, creating a development bundle and experience is an entirely different problem from creating a production bundle that’s optimised. So rather than expecting Rollup to solve this problem, there’s nothing to stop third parties from solving it.

**At** [**JSDayIE 2019**](https://www.jsday.org/)**, I presented** [**Nollup**](https://github.com/PepsRyuu/nollup), a development bundler for Rollup that’s API compatible and can re-use the same configuration and plugins.

Press enter or click to view image in full size

![]()

Nollup provides a development server that reuses the same Rollup configuration and plugins, and also provides HMR. With a combination of Nollup and Rollup, I now have the developer experience I’m looking for, and also the ideal production bundles, with full control over how the pipeline operates making optimisations far easier.

## Third Party Libraries

Something to be aware of when you’re using any bundler: there’s very little consistency when it comes to how modules are packaged in NPM. It’s incredibly frustrating, especially considering many of us write modules these days using ESM. Here’s some various problems that come up:

* Modules using `require/module.exports` in very obscure ways which makes it hard for a bundler to detect dependencies.
* Modules pointing ESM to their source code causing a bundler to have to bundle several additional files instead of just one.
* Modules using non-standard JavaScript forcing you to add additional transpilation steps that you might not want to use.
* Modules using code that doesn’t exist in browsers such as `process.env.NODE_ENV` and forcing you to convert or polyfill it.

Press enter or click to view image in full size

![]()

Is this a problem for you or a problem for your bundler? While bundlers do try and simplify things as much as possible for you, you’re still going to have to be aware of what you’re importing. **To get the best performance possible out of a development setup, always look for packages that support ESM and have lightweight code.** Thankfully, there’s amazing sites like [pika.dev](https://www.pika.dev/) that help you find packages that support ESM.

## Conclusions

Even though Webpack is the dominating force for bundlers at the moment, times have changed a lot since it was released. There’s far more options than ever, and there’s developers constantly trying to innovate in the bundler space. **Some developers are even trying no bundler at all, although I remain skeptical about their usage for large app development.**

Many people recently are complaining about bundler performance. But I don’t think any tool is going to solve performance problems. Bundlers can try innovative ideas such as multi-threading and improved caching, but you’re always going to hit a limit. **If you’re having performance problems, it’s more likely because you’re not keeping tabs of what you’re importing, and haven’t considered splitting your project into multiple projects.**

For me, the main reason to choose a bundler is because of the developer experience it offers. Functionality is pretty much identical these days, except how you interface with that bundler. I don’t like the complexity of Webpack, or the abstraction provided by Parcel. I prefer simple tools that do simple things, but give you the power to enhance it. Consider a tool not because it’s what everyone else uses, but because you enjoy using it and it makes you productive, rather than being frustrated.

Thanks for reading!

**Links:** [**Twitter**](https://twitter.com/PepsRyuu)**,** [**Medium**](/@PepsRyuu)**,** [**Github**](https://github.com/PepsRyuu)