---
title: "Do we still need JavaScript frameworks?"
url: https://medium.com/p/42576735949b
---

# Do we still need JavaScript frameworks?

[Original](https://medium.com/p/42576735949b)

# Do we still need JavaScript frameworks?

[![Luke Joliat](https://miro.medium.com/v2/resize:fill:64:64/1*_S-Tu790FV5CBNlcHUAG7A.jpeg)](/@lcjfifty?source=post_page---byline--42576735949b---------------------------------------)

[Luke Joliat](/@lcjfifty?source=post_page---byline--42576735949b---------------------------------------)

9 min read

·

Feb 4, 2019

--

30

Listen

Share

More

Press enter or click to view image in full size

![]()

As a web developer, I try to assess my toolbox regularly and determine if I can do without this or that tool. Recently, I have been investigating just how easy it is to develop a complex front end application without a front end framework.

### **What is a JavaScript framework?**

Put simply, a JavaScript framework is a tool that you can leverage to develop advanced web applications, especially SPAs.

Back in the day, web developers would implement front end logic by relying heavily on vanilla JS and jQuery. But, as front end applications became more and more complex, the tools rose to meet that complexity.

Press enter or click to view image in full size

![]()

The frameworks that are popular today have a few core commonalities. Most front end frameworks/libraries, from Vue to React, provide some combination of the following:

* Synchronization of state and view
* Routing
* A Template System
* Reusable components

### **Are Frameworks still necessary?**

It depends on how you stress the word *necessary.* Many would argue that front end frameworks are not and never have been necessary. They’re very useful tools, though.

So the question is: are frameworks today’s jQuery? Will the problems they solve be addressed by changes like those to the DOM API?

![]()

It’s hard to say, but advances in native JS, the web component spec, and easily configurable build tools, have made developing a SPA without a framework as easy as it has ever been.

To examine this further, I developed a single page application using only vanilla JavaScript, native Web Components, and Parcel. There were a handful of pitfalls and difficulties along the way that highlighted the strengths of JS frameworks.

At the same time, once I passed the initial hurdles, I was surprised by how simple it was to create a single page application with just vanilla JS.

### Overview

The application is simple. It is a recipes application with basic CRUD capabilities. The user can create, edit, delete, favorite, and filter a list of recipes.

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

### Components

Creating a web component is also straightforward. You create a class that extends `HTMLElement` (or `HTMLParagraphElement` and so on), and then use that class to define a custom element.

You can also make use of lifecycle hooks such as *connectedCallback, disconnectedCallback, attributeChangedCallback.*

### Routing

The routing for the recipes application is also quite simple. Given a navigation event, I set the application’s content to the corresponding web component.

Initially, I was using an npm package called Vanilla JS Router. With the [browser history API](https://developer.mozilla.org/en-US/docs/Web/API/History), it isn’t all that complex to implement your own in less than 100 lines of code! Note: I am not implementing really complex logic such as route guards.

That is a quick summary. I want to keep this article to a reasonable length. I may write a follow-up post with a more thorough explanation of the application. I implemented some fun features like infinite scrolling, a custom drag and drop uploader, and more!

## Retrospective

After creating the application, I took some time to think about the pros and cons of the whole process from start to finish. I’ll start with the bad news.

## Cons

### The spec is still in flux

![]()

The web component spec is both old and new. It has been around for a lot longer than I had originally thought. *Web Components were* [*introduced by Alex Russell*](https://en.wikipedia.org/wiki/Web_Components#cite_note-16) *at Fronteers Conference 2011 for the first time.* However, the push behind web components has really grown in the past year or two. As such, there is still a lot of turmoil in the spec. For instance, HTML imports have been abandoned, though most of the documentation/resources still reference them.

### Testing

![]()

There aren’t a lot of dedicated resources for testing native web components out there. There are some promising tools such as [skatejs ssr](https://github.com/skatejs/skatejs/tree/master/packages/ssr) and the [web component tester](https://github.com/Polymer/tools/tree/master/packages/web-component-tester) from Polymer. But these tools are really meant for use with their respective libraries. This presents some difficulties for use with native web components.

### Change Detection

Having an underlying system that automatically keeps the view in sync with the data model is incredible. It is what drew many to Angular and other frameworks in the first place.

Keeping state in sync with the view is not so difficult at a small scale. But it can get out of control very quickly, and you find yourself adding tons of event listeners and query selectors.

Press enter or click to view image in full size

![]()

### The Shadow DOM

I am really torn about the shadow DOM. On one hand, I love the idea of encapsulation. It is a sensible design pattern, makes your style cascade more manageable, simplifies your concerns, and so on. However, it also presents problems when you do want certain things to penetrate that encapsulation (such as a shared style sheet), and there are ongoing debates about [the best way of doing this.](https://www.smashingmagazine.com/2016/12/styling-web-components-using-a-shared-style-sheet/)

### Generating DOM structures

Part of the magnificence of frameworks/libraries like Angular and React is that they are masters of their DOMain. That is, they are excellent at efficiently rendering and re-rendering structures in the DOM. From the [Angular University blog](https://blog.angular-university.io/why-angular-angular-vs-jquery-a-beginner-friendly-explanation-on-the-advantages-of-angular-and-mvc/):

> *Angular is not generating HTML and then passing it to the browser to have it parsed, instead Angular is generating DOM data structures directly!*

Angular for example, unlike jQuery, renders DOM data structures directly. That is, instead of passing HTML to the browser to be parsed, and then rendered into DOM data structures. This is more performant as it eliminates that parsing step. The Virtual DOM is also quite useful, as they prevent you from re-rendering everything each time you need to update your view.

## Pros

On the other hand, there are some undeniable benefits to developing applications this way:

### Bundle Size

The final product can be (emphasis on *can*) so much smaller and more compact than anything developed with a modern framework. For example, the final build of my fully featured recipes app was less than half the size of a fresh Angular build.

![]()

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Note: These are the updated, optimized bundle sizes.

### Understanding

![]()

If you’ve only really developed with a framework and its CLI, it can be a great exercise to make a web application without extra tools. As someone who wants to achieve a certain level of mastery (to the extent that it’s possible) of web development, it has been essential for me to get more hands-on experience with build tools, browser APIs, design patterns, etc.

### Performance

![]()

What these front end frameworks and libraries are doing behind the scenes is amazing. However, you can pay a performance price if you decide to use any of them; there is no such thing as a free lunch. There are many potential performance drags at scale: whether it’s wasted re-renders, redundant listeners, deep object comparison, or unnecessary and large DOM manipulations. You can cut out a lot of complexity here by implementing things from scratch.

The Angular and React teams seem aware of these pitfalls, and have provided things like *shouldUpdate* method overrides and *onPush* ChangeDetection as a means of further optimizing performance.

### Simplicity and code ownership

![]()

You take a risk whenever you bring in 3rd party code. This risk is reduced with tried and tested libraries/frameworks, but never truly eliminated. If you can get away with writing code yourself or with your team, you can reduce that risk and maintain a codebase that you know in and out.

### Notes and interesting tidbits

I had a blast working with Parcel. It felt a bit more limited than Webpack at times when trying to work around certain edge cases, but I found the, ‘zero config’ tag line to hold true, for the most part.

It is also clear to me that many label React a ‘library’ and Vue a ‘progressive’ framework. While I understand the reasons for this, I think React, Vue and Angular solve many of the same problems. Thus, I am considering them all together under the term ‘frameworks.’

Why not use Stencil or Polymer? I wanted to avoid the use of packages, libraries, and frameworks as much as possible. I wanted to see how far web standards had risen to meet modern development (aside from build tools).

There are I’m sure many other ways of developing a SPA or front end application in general without a major framework or library, I tried one way here, and I’d love to hear about others!

## Summary

A great heuristic for the decision to use or not use a framework is what I call, “the tipping point.” There comes a point as your application grows, where you end up creating your own framework in order to reuse functionality and structure. For example, you have a bunch of forms and you want to create reusable logic for reactive validation.

If you end up at this point, you have to decide whether or not it is worth investing the time in creating systems to accomplish what you can quickly accomplish with a framework or library. There will be different tipping points depending on what your time constraints or budget constraints are, but frameworks are still very relevant given the right scenarios.

That said, much of what frameworks do will probably become easier to do with smaller libraries and/or native code as time goes on. Take my application as an example. At the same time, if the large frameworks and libraries remain versatile they may morph, adapt, and stick around. If not, they may end up like jQuery — a tool of the past for the most part.

## Conclusion

In conclusion, there are promising ways of developing complex front end applications without frameworks. However, the spec for things like web components is still evolving and there are kinks to be worked out. The frameworks still do a lot of amazing things and can make development much smoother.

At this time, as far as I can tell, the pros of using a framework often outweigh the cons. However, if frameworks do not start solving new problems and continuing to evolve, they will eventually fade away.

## Resources

[## Angular For Beginners Guide: Why Angular? The Top Benefits

### Note: This post is part of the ongoing Angular for Beginners series, here is the complete series: Angular For Beginners…

blog.angular-university.io](https://blog.angular-university.io/why-angular-angular-vs-jquery-a-beginner-friendly-explanation-on-the-advantages-of-angular-and-mvc/?source=post_page-----42576735949b---------------------------------------)

[## Comparison with Other Frameworks - Vue.js

### Vue.js - The Progressive JavaScript Framework

vuejs.org](https://vuejs.org/v2/guide/comparison.html?source=post_page-----42576735949b---------------------------------------#Runtime-Performance-1)

[## Optimizing Performance - React

### Internally, React uses several clever techniques to minimize the number of costly DOM operations required to update the…

reactjs.org](https://reactjs.org/docs/optimizing-performance.html?source=post_page-----42576735949b---------------------------------------)

[## Web Components

### As developers, we all know that reusing code as much as possible is a good idea. This has traditionally not been so…

developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/Web_Components?source=post_page-----42576735949b---------------------------------------)

[## The deepest reason why modern JavaScript frameworks exist

### I’ve seen many, many people using a modern framework like React, Angular or Vue.js blindly. These frameworks provide…

medium.com](/dailyjs/the-deepest-reason-why-modern-javascript-frameworks-exist-933b86ebc445?source=post_page-----42576735949b---------------------------------------)

[## Styling Web Components Using A Shared Style Sheet

### Web components are an amazing new feature of the web, allowing developers to define their own custom HTML elements…

www.smashingmagazine.com](https://www.smashingmagazine.com/2016/12/styling-web-components-using-a-shared-style-sheet/?source=post_page-----42576735949b---------------------------------------)