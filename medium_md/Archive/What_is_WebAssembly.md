---
title: "What is WebAssembly?"
url: https://medium.com/p/e1a06f856974
---

# What is WebAssembly?

[Original](https://medium.com/p/e1a06f856974)

# What is WebAssembly?

## What it is, and why it matters for the future of web development

[![Kenneth Reilly](https://miro.medium.com/v2/resize:fill:64:64/1*xTcq_5lX6WkLxQAR5KmrXg@2x.jpeg)](https://kennethreilly.medium.com/?source=post_page---byline--e1a06f856974---------------------------------------)

[Kenneth Reilly](https://kennethreilly.medium.com/?source=post_page---byline--e1a06f856974---------------------------------------)

6 min read

·

May 17, 2019

--

3

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3De1a06f856974&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fwhat-is-webassembly-e1a06f856974&source=---header_actions--e1a06f856974---------------------post_audio_button------------------)

Share

![]()

### What is WebAssembly?

WebAssembly has steadily gained popularity since the founding of the [WebAssembly Community Group](https://www.w3.org/community/webassembly/) back in 2015, but what exactly is it?

As defined by the authors at <https://webassembly.org>:

> “WebAssembly (abbreviated *Wasm*) is a binary instruction format for a stack-based virtual machine. Wasm is designed as a portable target for compilation of high-level languages like C/C++/Rust, enabling deployment on the web for client and server applications.”

WebAssembly provides a lean stack-based virtual machine that allows web applications to run at near-native speed, by utilizing a fast-loading binary format which can also be converted into a text format for debugging.

This is a radically different approach to front-end software development on the web, in contrast to the typical use of heavy JavaScript libraries with layers of compatibility workarounds for issues which may not even exist in five or ten years. [Four major browsers plus node have adopted it](https://webassembly.org/roadmap/), which is a huge step towards finally achieving cross-browser compatibility, with high performance web applications being the default rather than the exception.

### Why is WebAssembly Important?

If we look at [the history of JavaScript](https://medium.com/@benastontweet/lesson-1a-the-history-of-javascript-8c1ce3bffb17), originally called *Mocha*, it was first conceived to be a full web application language and not just for front-end UI only. It took nearly 20 years for this to take full effect with the widespread adoption of Node, which was by then a novel concept to almost everyone.

The reasons for this are primarily driven by marketing, as Sun was touting JavaScript as a companion language to Java, something which often seems to resonate within certain large-scale enterprise cultures which use Java as their primary application language and see web front-end as just the place to get data in and out of an application. However, not everything is a simple CRUD enterprise app. If all you have is a hammer, everything looks like a nail. Well, sometimes you don’t need a hammer, you might need a saw or a CNC laser.

WebAssembly is only the second language to be natively understood by web browsers, with the first having been caught up in endless waves of standards compliance issues, serious performance problems, conflicting notions of how to go about implementing solutions, and giant cumbersome frameworks that often [cause more problems than they solve](https://medium.com/@kennethreilly/what-is-technical-debt-4c087d30a056) in the long run. So, after a good 25 year run, it’s about time that at least *one* other language gets a shot at it.

### Architectural Overview

WebAssembly is a [*virtual instruction set architecture*](http://webassembly.github.io/spec/core/intro/introduction.html#scope) (virtual ISA), which effectively allows a skilled developer to build modules that load quickly and run nearly as fast as compiled C or C++, as if these functions were compiled directly into the web browser itself. WebAssembly files come in two different formats, which can be converted to and from each other:

* ***.wat*** file: a human-readable [S-Expression](https://en.wikipedia.org/wiki/S-expression) syntax file
* ***.wasm*** file: the machine-readable compiled binary file

Writing Web Assembly Text (***.wat***) files by hand is certainly an option, but it’s not the only one. Fortunately, there are many ways to generate and work with WebAssembly files. Here are just a few of them:

* A precompiled *C++ to WebAssembly* toolchain, [available here](https://webassembly.org/getting-started/developers-guide/)
* A TypeScript-to-WebAssembly compiler, [AssemblyScript](https://github.com/AssemblyScript/assemblyscript)
* The online WebAssembly notepad, [WasmExplorer](https://mbebenita.github.io/WasmExplorer/)
* The online IDE, [WebAssembly Studio](https://webassembly.studio/)
* [Many other compiler options](https://github.com/appcypher/awesome-wasm-langs)

More will be available as WebAssembly grows in popularity from widespread adoption by the authors of Chrome, Edge, Firefox, WebKit, and Node. It’s easy to see how this technology isn’t going away anytime soon and will likely have a very big impact on front-end development and web technologies as a whole.

### Performance Benchmarking

As with any cool new technology that hits the scene, before we get all excited and go jumping on the bandwagon to potentially nowhere, it’s important to ask this time-honored question: *why is this a good idea and should I bother?*

There is no shortage of information and discussion about performance issues surrounding web applications, especially when it comes to single-page web apps and larger front-end interfaces with heavy bolt-on dependencies. There are entire areas of concern within the software industry that center around the notion of solving performance issues which in reality have been self-induced by the choice of using some framework X or technology Y to make web apps, since everyone else was doing it and that was the cool thing right?

Let’s take a look at some benchmarks from [an excellent online tool](https://wasmboy.app/benchmark/) which is the subject of an article on [benchmarking WebAssembly using emulators](https://medium.com/@torch2424/webassembly-is-fast-a-real-world-benchmark-of-webassembly-vs-es6-d85a23f8e193):

Press enter or click to view image in full size

![]()

The above two graphs are the result of a WasmBoy benchmark test, ran using the game “Back to Color” which is a demo game with a variety of audio and graphical events designed to showcase the features of the GameBoy Color. The benchmark was performed in Safari, on a 2017 13" MacBook Pro.

[AssemblyScript](https://github.com/AssemblyScript/assemblyscript) compiled to WebAssembly is shown in blue, with the competitors being TypeScript compiled directly to ES6 (in yellow), and the Closure Compiler (in green). The test is useful in that the TypeScript logic for the emulator is essentially the same across the board, allowing us to test the performance difference between each of the compiler targets.

Note that these metrics are comparing apples-to-apples (to other efficienct tools) which means thatthe competitors are still high-performance ES6 implementations of a game emulator *and* *not your typical website JavaScript*. The difference in speed between a compiled WebAssembly application and a typical clunky framework app would likely be far greater.

In the top graph, the *time-to-run* per frame is displayed, which is the total amount of time required for drawing each frame (lower means faster). This time was far lower for WebAssembly than for either competitor.

The bottom graph displays the average frame throughput, or Frames Per Second. This metric shows where the different intro scenes of the first two thousand or so frames are taxing on each of the implementations of the emulator in different ways. On average, the WebAssembly version had a higher throughput than the others, especially for the intro animation.

### Next Steps

WebAssembly shows a lot of potential for bridging the gap between client and server components of web applications, which is especially important as we enter an age of distributed computing and open web standards. As more local sources of data and energy become available, leveraging the incredible power of modern personal computing devices will be an important step in the right direction towards a more accessible, productive, and entertaining future.

While this technology may not provide immediate returns for everyone who might consider using it, for those with a reason to adopt early there are huge advantages which will start to pay off right away. This is especially in the case of [AssemblyScript](https://github.com/AssemblyScript/assemblyscript), as it allows front-end developers to leverage an existing language that is likely more familiar to them than C++ or Rust for example.

With AssemblyScript, a front-end developer could, for example, migrate all performance-critical functions, such as tight loops for search algorithms or game AI, into an ultra-fast compiled binary format that runs almost as fast as a native application (and potentially faster depending on the programmer).

### Conclusion

For more information about WebAssembly, check out these resources:

* [WebAssembly Community Group](https://webassembly.org)
* [This great article on freeCodeCamp](https://medium.freecodecamp.org/get-started-with-webassembly-using-only-14-lines-of-javascript-b37b6aaca1e4)
* [Using the WebAssembly API, from Mozilla Dev Network](https://developer.mozilla.org/en-US/docs/WebAssembly/Using_the_JavaScript_API)

![]()

I hope you enjoyed this article on WebAssembly, a powerful and revolutionary new way to build web applications.

Thanks for reading!

> Kenneth Reilly ([8\_bit\_hacker](https://twitter.com/8_bit_hacker)) is CTO of [LevelUP](https://lvl-up.tech/)