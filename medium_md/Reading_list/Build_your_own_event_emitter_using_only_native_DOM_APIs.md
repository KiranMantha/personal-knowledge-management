---
title: "Build your own event emitter using only native DOM APIs"
url: https://medium.com/p/b064aa2df09e
---

# Build your own event emitter using only native DOM APIs

[Original](https://medium.com/p/b064aa2df09e)

# Build your own event emitter using only native DOM APIs

## Using EventTarget and CustomEvent, we can create our own event emitter, no library needed

[![Cameron Nokes](https://miro.medium.com/v2/resize:fill:64:64/1*R1sVOkLuy9wy-sZ51fQypg.jpeg)](/@ccnokes?source=post_page---byline--b064aa2df09e---------------------------------------)

[Cameron Nokes](/@ccnokes?source=post_page---byline--b064aa2df09e---------------------------------------)

3 min read

·

Nov 2, 2019

--

Listen

Share

More

Press enter or click to view image in full size

![]()

> *Originally published at* [*https://cameronnokes.com*](https://cameronnokes.com/blog/build-your-own-event-emitter-using-only-native-dom-apis/)*.*

The Event emitter pattern (maybe better said as the [observer pattern](https://en.wikipedia.org/wiki/Observer_pattern)) is a bedrock in the JavaScript ecosystem. It’s a well-known, useful pattern for decoupling concerns in an application. Many codebases I’ve worked on use a library such as [eventemitter3](https://github.com/primus/eventemitter3) or [mitt](https://github.com/developit/mitt). But did you know that you can technically use built-in DOM APIs to get the same functionality, no library needed? 🤯

To accomplish this, we’ll use `EventTarget` and `CustomEvent`.

```
let eventEmitter = new EventTarget(); eventEmitter.addEventListener('my-event', console.log); eventEmitter.dispatchEvent(  
  new CustomEvent('my-event', { detail: 123 })  
);   
eventEmitter.removeEventListener('my-event', console.log);
```

That’s it. I know, it’s a little verbose, but that can be changed. The API should probably be familiar to you, but let’s go over what everything does.

## `EventTarget`

This is a core DOM API that other DOM classes like `Element`, `Window`, or `XMLHttpRequest` inherit from. We can leverage it in our own code as well and inherit from it: `class MyClass extends EventTarget { ... }`. When we construct our own `EventTarget`, all event dispatched through it are done synchronously like node.js or other libraries but unlike the DOM, which emits events asynchronously.

## `CustomEvent`

`CustomEvent` is basically identical to the `Event` class (base class used by the DOM to emit `ClickEvent` s, etc) except that it allows us to attach custom data to it. So here we specify the event name and data attached to it:

```
new CustomEvent('my-event', {   
  detail: 123   
});
```

`detail` can be anything you want, even another object. Sort of a strange API but that's how it was designed. If you don't have any additional information to dispatch along with your event, you can just use `new Event('my-event')` instead. If you want to go crazy, note that you can also extend `CustomEvent` and pass your subclass to `EventTarget`.

## Making a nicer API

In a small amount of code, we can adapt it to a more common node.js style API:

If I was to use this pattern in an application that’s more than a one-off project, I’d consider encapsulating it like this just in case I needed to swap out the implementation later.

## The pros and cons

By using `EventTarget`, you get some interesting functionality for free that you don't get with most libraries:

* Events can be canceled via the familiar `event.preventDefault()`. This means that if one event handler cancels the event, any subsequent handlers are *not* called. This ability is configurable with the `cancelable` property passed to the `CustomEvent` constructor (see above).
* `once` functionality (mitt doesn't have this) -- an event handler is removed once it is called once.
* Duplicate events handlers aren’t added. For example, if I add the same callback listener and options multiple times, it’s only registered once. This can help prevent memory leaks for you automatically.
* Sense of superiority that you didn’t bloat your bundle with yet another npm package.

Some downsides though:

* verbose
* lots of DOM related stuff around bubbling and DOM elements that don’t apply when using it like this
* no IE support, and ironically, lots of legacy IE properties like `srcElement` and `returnValue`
* can’t ever manually manipulate the event listener list or have a method like `prependEventListener`

Well, this was fun. There’s a lot of interesting corners of the DOM API that are fun to explore. Even if you never use this in actual code, I think knowing about it leads to a deeper understanding of the DOM, which is valuable.