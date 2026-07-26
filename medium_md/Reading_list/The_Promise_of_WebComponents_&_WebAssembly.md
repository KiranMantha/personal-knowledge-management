---
title: "The Promise of WebComponents & WebAssembly"
url: https://medium.com/p/ad26af56fcf1
---

# The Promise of WebComponents & WebAssembly

[Original](https://medium.com/p/ad26af56fcf1)

# The Promise of WebComponents & WebAssembly

[![Matas Ubarevicius](https://miro.medium.com/v2/resize:fill:64:64/0*A6RQkGcAt55nu3oC.)](https://medium.com/@matasubarevicius?source=post_page---byline--ad26af56fcf1---------------------------------------)

[Matas Ubarevicius](https://medium.com/@matasubarevicius?source=post_page---byline--ad26af56fcf1---------------------------------------)

7 min read

·

Mar 20, 2018

--

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dad26af56fcf1&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fthe-promise-of-webcomponents-webassembly-ad26af56fcf1&source=---header_actions--ad26af56fcf1---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

> [Click here to share this article on LinkedIn »](/the-promise-of-webcomponents-webassembly-ad26af56fcf1?utm_source=medium_sharelink&utm_medium=social&utm_campaign=buffer)

## The signs of change

Even though many of us would agree to name the **Javascript fatigue** a real disease, web platform seems to be the only environment that actually succeeds in managing challenges of juggling between the complexity, flexibility and stability in system design at the massive world wide scale. The node package manager (npm) at this point of writing offers 650,000 building blocks of reusable javascript code to developer community. These blocks come in various sizes and shapes as small functions, libraries or fully fledged frameworks. And while this digital ecosystem comes with it’s challenges, developers are getting used to working with such a malleable and very rich substance. But what if this scale is just the tip of an iceberg…

I’m always excited about the future that every new standard of the web platform offers to developers, but I believe that holistic analysis of **WebComponents** and **WebAssembly** in particular can shed some light on the general trend which will make the web a very different place in the near future. The purpose of this article is to speculate on this future and to imagine how life of the web developer will change when the **promise** of these two technologies will be fulfilled.

In a nutshell both of these standards are revolutionary enough to each deserve a decent book. **Frameworkless WebComponents** have potential to reshape and simplify application design in the same way that the npm packages helped many developers in solving everyday problems that range from mundane date conversions to complex machine learning calculations. **Languageless WebAssembly** as compilation target offers new levels of expression and speed, never before seen on the browser or, to that matter, any other web stack. Even though currently these ideas are fresh and still lack adoption they both will fuel each others advancement.

## WebComponent importance

Some 4 years ago numerous Javascript frameworks such as Angular and React chose to use components as a primary units when structuring UI code. This pattern helped to reason about increasingly complex single page applications. Somewhere around that time W3C started working on a new standard called [WebComponents](https://www.w3.org/standards/techs/components#w3c_all). With the rise of libraries such as Polymer and Stencil in 2017 we began seeing some of the real power of this technology. Suddenly developers were able to invest their time in framework agnostic way of building reusable UI parts for their applications. No matter what you use now, be it Angular, React or Vue - everyone can adapt this model. Step by step it removes friction through many layers of existing projects. Companies such as Ionic were already able to cash in when making libraries of high quality elements for websites that resemble native iOS and Android controls. You can find their story in the following video:

Currently [WebComponents.org](https://www.webcomponents.org/) offers around 1000 different ui building blocks that can be integrated and reused in projects around the world. This number is destined to grow and expand into numerous high quality controls, UI elements or fully fledged applications that can interoperate easily with hosting applications. HTML and CSS being lingua franca for UX design in isolated WebComponents will make web platform and applications be even more competitive when compared to native OS solutions. But while WebComponent pattern is a good answer to architectural problems we were facing in our projects, web platform till now still lacked answers to fundamental performance issues when compared to native apps. This is where WebAssembly is stepping in to lead the way… Like a big way… Really big…

## Wasm

If tomorrow you will be stepping through the code in your developer tools window don’t panic when presented the code that looks like this:

```
(module  
  (func (param $lhs i32) (param $rhs i32) (result i32)  
    get_local $lhs  
    get_local $rhs  
    i32.add))
```

You probably hit the library that decided to optimise its’ code to work faster and be smaller in size. This library was compiled to WebAssembly (**wasm** for short) and served to your browser as a regular static javascript file would have been. Even though wasm compiles to binary format, while using [conversion tools](http://webassembly.org/getting-started/advanced-tools/) we can still make it readable to humans. If the code above looks totally unfamiliar to you — go check this MDN website for more information [“Understanding Webassembly Text Format”](https://developer.mozilla.org/en-US/docs/WebAssembly/Understanding_the_text_format). Also check this g[ithub WebAssembly repository](https://github.com/WebAssembly/design/blob/master/BinaryEncoding.md) to learn more about the binary encodings of wasm. If this isn’t enough check this video from [Jay Phelps](https://twitter.com/_jayphelps?lang=en):

Till now Javascript was the only kid in the block when it came to language choice on the browser. Other languages like Java tried, but failed to enter the picture while running in a separate VM. And while Javascript is great, expressive and very dynamic language it has it’s shortfalls when it comes to performance, static types and size. [Webassembly.org](http://webassembly.org/) offers this definition to Wasm:

> WebAssembly (abbreviated *Wasm*) is a binary instruction format for a stack-based virtual machine. Wasm is designed as a portable target for compilation of high-level languages like C/C++/Rust, enabling deployment on the web for client and server applications.

This means that languages like C#, TurboScript, Elm and many more will be offering wasm as compilation target. This is a nice article from [Scott Hanselman](https://twitter.com/shanselman?lang=en) called [.NET and WebAssembly is The Future of the Frontend](https://www.hanselman.com/blog/NETAndWebAssemblyIsThisTheFutureOfTheFrontend.aspx) where he states that WebAssembly is here to stay. While .NET is definitely not the only future for the frontend, it’s a good candidate for people who would prefer writing full-stack applications in C#, VB or even F#…

## The “Tower of Babel” is collapsing

Like it or not this new standard will cause explosion in languages that will be used on the web. This is not to say that Javascript will be obsolete, it only means that in the near future we will have much more options to choose from. Developers who work on general purpose libraries and frameworks will benefit because they will be able to package more features to the same size bundle. And the users of such modules will benefit because their infrastructure will become lightweight and hopefully optimised to run much faster.

The need for new languages existed for a while now in the browser world. During the last three years we saw explosion in supersets of Javascript like [Typescript](http://www.typescriptlang.org/), [Reason M](https://reasonml.github.io/)L or [Elm](http://elm-lang.org/). These languages all promise to improve scalability, developer experience and stability of Javascript code. There’s no need to be surprised that WebAssembly was accepted quite positively by both frontend and backend communities to bring these targets to even higher level.

## But where’s the Revolution?

While it’s really exciting, freedom to speak any language on the web is not really what makes WebAssembly a killer feature of the platform. Executing your code in close to native speeds will change what our websites will look like. For the first time in history browsers will be able to compete with native OS on performance. WebAssembly will implement consistent multithreading model. And if you think webworkers were an improvement, wait till you get your hands dirty with the client running on the threadripping processors or any other future marvel invention of the humankind.

With fundamental client performance limitations removed Pandoras’ box gets opened— games, raytracing and physics engines, 3D CAD applications, serious simulation libraries will finally be able to enter the browser space. This also has real potential to revive VR & AR on the web. Here’s the link to [Epic Zen Garden Demo](https://s3.amazonaws.com/mozilla-games/ZenGarden/EpicZenGarden.html) you can use for inspiration. Don’t forget, it’s actual game-like interactive experience, not a pre-rendered movie playing. Check this [IEEE Spectrum article by Luke Wagner](https://spectrum.ieee.org/computing/software/webassembly-will-finally-let-you-run-highperformance-applications-in-your-browser) for more details on high performance applications that will be made available by wasm. If that isn’t enough — this is promised to influence IOT world in similar if not more serious ways. Node 8 LTS with its V8 engine and Microsofts’ ChakraCore are already supporting wasm as well. For more info check this video from [Ben Smith](https://twitter.com/binjimint?lang=en):

Of course there are still challenges remaining and lots of practical things missing in WebAssembly like garbage collection or exception handling. You can find the [post MVP feature list here](http://webassembly.org/docs/future-features/). Also if you’re interested you can check this blog post for a nice [summary of this technology from The New Stack](https://thenewstack.io/ready-web-assembly-revolution/). There are also [people concerned about implications of proprietary binary code running through WebAssembly](https://news.ycombinator.com/item?id=10487713) that will make it hard to read other peoples’ code. But the fact that v1.0 is already released and all major browser vendors have agreed on this spec indicates that there’s no turning back now from all the fun we will have in the coming years.

## Where does it all leave us…

So how are the WebComponents related to WebAssembly and how will they help push the adoption further? Well, both of these standards offer a modular abstraction layer to frontend stacks. Imagine combining the WebComponents that render CAD content on WebGL in VR with the WebComponents that are optimised for multithreaded simulations in wasm with the WebComponents that are meant to create unique UI controls with the WebComponents… with the WebComponents… round and round it goes.

This modular system of fast interlinked WebComponents running wasm code is what will drive the future of web development in the near future. The management of information flow between those components will still be a challenge, but with libraries such as [Redux](https://redux.js.org/) and [Apollo GraphQL](https://www.apollographql.com/) we are on a good path to finding a solution for that. Combine this with the possibility to write frontend code with statically typed languages and web platform will suddenly be running on steroids. 650,000 npm packages in this context seem like a very humble beginning indeed.

In general these new standards alone can probably grow javascript fatigue into the more general web dullness, but it is a good thing. The faster we’ll get on with it the earlier we’ll enjoy new possibilities opened by these standards. In the meantime webpack is now supporting WebAssembly with the [wasm-loader](https://github.com/ballercat/wasm-loader) and with just a few right [polyfills](https://github.com/webcomponents/webcomponentsjs) we can get WebComponents working on our websites. So let’s enjoy and innovate the future.