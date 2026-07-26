---
title: "A TC39 Proposal for Signals"
url: https://medium.com/p/f0bedd37a335
---

# A TC39 Proposal for Signals

[Original](https://medium.com/p/f0bedd37a335)

# A TC39 Proposal for Signals

[![EisenbergEffect](https://miro.medium.com/v2/resize:fill:64:64/1*Bp1EaHBSSYW4gwO_DbKmDA.jpeg)](/?source=post_page---byline--f0bedd37a335---------------------------------------)

[EisenbergEffect](/?source=post_page---byline--f0bedd37a335---------------------------------------)

14 min read

·

Apr 1, 2024

--

8

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Df0bedd37a335&operation=register&redirect=https%3A%2F%2Feisenbergeffect.medium.com%2Fa-tc39-proposal-for-signals-f0bedd37a335&source=---header_actions--f0bedd37a335---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

In August of last year, [I mentioned that I wanted to begin pursuing a potential standard for *signals* in TC39](/the-future-of-native-html-templating-and-data-binding-5f3e52fda259). Today, I’m happy to share that [a v0 draft of such a proposal](https://github.com/proposal-signals/proposal-signals) is publicly available, along with [a spec-compliant polyfill](https://github.com/proposal-signals/proposal-signals/tree/main/packages/signal-polyfill).

## What are signals?

A signal is a data type that enables one-way data flow by modeling cells of state and computations derived from other state/computations. The state and computations form an acyclic graph, where each node has other nodes that derive state from its value (sinks) and/or that contribute state to its value (sources). A node may also be tracked as “clean” or “dirty”.

But what does all that mean? Let’s look at a simple example.

Imagine we have a *counter* we want to track. We can represent that as state:

```
const counter = new Signal.State(0);
```

We can read the current value with `get()`:

```
console.log(counter.get()); // 0
```

And we can change current value with `set()`:

```
counter.set(1);  
console.log(counter.get()); // 1
```

Now, let’s imagine that we want to have another signal that indicates whether our counter holds an even number or not.

```
const isEven = new Signal.Computed(() => (counter.get() & 1) == 0);
```

Computations aren’t writable, but we can always read their latest value:

```
console.log(isEven.get()); // false  
counter.set(2);  
console.log(isEven.get()); // true
```

In the above example, `isEven` has `counter` as a *source* and `counter` has `isEven` as a *sink.*

We can add another computation that provides the parity of our counter:

```
const parity = new Signal.Computed(() => isEven.get() ? "even" : "odd");
```

Now we have `parity` with `isEven` as a *source* and `isEven` with `parity` as a *sink (*remember that`isEven` already has`counter` as a *source)*. As a result, we can change the original `counter` and the state will flow unidirectionally to `parity`.

```
counter.set(3);  
console.log(parity.get()); // odd
```

Everything we’ve done so far seems like it could be done through normal function composition. But if implemented that way, without signals, there would be no source/sink graph behind the scenes. So, why do we want that graph? What is it doing for us?

Recall that I mentioned signals can be “clean” or “dirty”. When we change the value of `counter`, it becomes *dirty*. Because we have a graph relationship, we can then mark all the sinks of `counter` (potentially) dirty as well, and all their sinks, and so on and so forth.

**There’s an important detail to understand here.** The signal algorithm is not a *push* model. Making a change to `counter` does not eagerly push out an update to the value of `isEven` and then via the graph, an update to `parity`. It is also not a pure *pull* model. Reading the value of `parity` doesn’t always compute the value of `parity` or `isEven`. Rather, when `counter` changes, it pushes *only the change in the dirty flag* through the graph. Any potential re-computation is delayed until a specific signal’s value is *explicitly pulled.*

**We call this a “push then pull” model.** Dirty flags are eagerly updated (pushed) while computations are lazily evaluated (pulled).

There are a number of advantages that arise out of combining an acyclic graph data structure with a “push then pull” algorithm. Here are a few:

* `Signal.Computed` is automatically memoized. If the source values haven’t changed, then there’s no need to re-compute.
* Unneeded values aren’t re-computed even when sources change. If a computation is dirty but nothing reads its value, then no re-computation occurs.
* False or “over updating” can be avoided. For example, if we change `counter` from 2 to 4, yes, it is dirty. But when we pull the value of `parity` its computation will not need to re-run, because `isEven`, once pulled, will return the same result for 4 as it did for 2.
* We can be notified when signals become dirty and choose how to react.

These characteristics turn out to be very important when efficiently updating user interfaces. To see how, we can introduce a fictional `effect` function that will invoke some action when one of its sources becomes dirty. For example, we could update a text node in the DOM with the `parity`:

```
effect(() => node.textContent = parity.get());  
// The effect's callback is run and the node's text is updated with "odd"  
// The effect watches the callback's source (parity) for dirty changes.  
  
counter.set(2);  
// The counter dirties its sinks, resulting in the effect being  
// marked as potentially dirty, so a "pull" is scheduled.  
// The scheduler begins to re-evaluate the effect callback by pulling parity.  
// parity begins to evaluate by pulling isEven.  
// isEven pulls counter, resulting in a changed value for isEven.  
// Because isEven has changed, parity must be re-computed.  
// Because parity has changed, the effect runs and the text updates to "even"  
  
counter.set(4);  
// The counter dirties its sinks, resulting in the effect being  
// marked as potentially dirty, so a "pull" is scheduled.  
// The scheduler begins to re-evaluate the effect callback by pulling parity.  
// parity begins to evaluate by pulling isEven.  
// isEven pulls counter, resulting in the same value for isEven as before.  
// isEven is marked clean.  
// Because isEven is clean, parity is marked clean.  
// Because parity is clean, the effect doesn't run and the text is unaffected.
```

Hopefully this brings some clarity to what a signal is, and an understanding of the significance of the combination of the acyclic source/sink graph with its “push then pull” algorithm.

## Who has been working on this?

Late in 2023 I partnered with [Daniel Ehrenberg](https://x.com/littledan?s=20), [Ben Lesh](https://twitter.com/benlesh), and [Dominic Gannaway](https://twitter.com/trueadm) to try to round up as many signal library authors and maintainers of front-end frameworks as we could. Anyone who expressed an interest was invited to help us begin to explore the feasibility of signals as a standard.

We started with a survey of questions and one-on-one interviews, looking for common themes, ideas, use cases, semantics, etc. We didn’t know whether there was even a common model to be found. To our delight, we discovered that there was quite a bit of agreement from the start.

Over the last 6–7 months, detail after detail was poured over, attempting to move from general agreement to the specifics of data structures, algorithms, and an initial API. You may recognize a number of the libraries and frameworks that have provided design input at various times throughout the process so far: [Angular](https://angular.io/), [Bubble](https://bubble.io/), [Ember](https://emberjs.com/), [FAST](https://www.fast.design/), [MobX](https://mobx.js.org/), [Preact](https://preactjs.com/), [Qwik](https://qwik.dev/), [RxJS](https://rxjs.dev/), [Solid](https://www.solidjs.com/), [Starbeam](https://www.starbeamjs.com/), [Svelte](https://svelte.dev/), [Vue](https://vuejs.org/), [Wiz](https://blog.angular.io/angular-and-wiz-are-better-together-91e633d8cd5a), and more…

It’s quite a list! And I can honestly say, looking back at my own work in Web Standards over the last ten years, this is one of the most amazing collaborations I’ve had the honor to be a part of. It’s a truly special group of people with exactly the type of collective experience that we need to continue to move the web forward.

> **IMPORTANT**: If we missed your library or framework, there’s still plenty of opportunity to get involved! Nothing is set in stone. We’re still at the beginning of this process. Scroll down to the section titled “How can I get involved in the proposal?” to learn more.

## What is in the signals proposal?

The proposal, [which can be found on GitHub](https://github.com/proposal-signals/proposal-signals), includes:

* Background, motivation, design goals, and an FAQ.
* A proposed API for creating both state and computed signals.
* A proposed API for watching signals.
* Various additional proposed utility APIs, such as for introspection.
* A detailed description of the various signal algorithms.
* A spec-compliant polyfill covering all the proposed APIs.

The signals proposal does not include an `effect` API, since such APIs are often deeply integrated with rendering and batch strategies that are highly framework/library dependent. However, the proposal does seek to define a set of primitives and utilities that library authors can use to implement their own effects.

On that note, the proposal is designed in such a way as to recognize that there are two broad categories of signal users:

* Application developers
* Library/framework/infrastructure developers

APIs that are intended to be used by application developers are exposed directly from the `Signal` namespace. These include `Signal.State()` and `Signal.Computed()`. APIs which should rarely if ever be used in application code, and more likely involve subtle handling, typically at the infrastructure layer, are exposed through the `Signal.subtle` namespace. These include `Signal.subtle.Watcher` , `Signal.subtle.untrack()`, and the introspection APIs.

> **ASIDE**: Haven’t seen something like the idea of the `subtle` namespace in JavaScript before? [Checkout Crypto.subtle](https://developer.mozilla.org/en-US/docs/Web/API/Crypto/subtle).

Press enter or click to view image in full size

![]()

*We interrupt this blog post on signals to remind you of* [*the Web Component Engineering course*](https://bluespire.com/p/web-component-engineering)*, trusted by giants such as Adobe, Microsoft, Progress, and Reddit. If you want to learn modern UI engineering, get up to speed on dozens of Web Standards, and even see how signals can be integrated with Web Components, this is the course for you. Group rates for teams and PPP pricing available upon request.*

*Now, back to your regularly scheduled program…*

## As an app dev, how do I use signals?

Many of today’s popular component and rendering frameworks are already using signals. Over the coming months, we hope that framework maintainers will experiment with re-platforming their systems on top of the signals proposal, providing feedback along the way, and helping us prove out whether it is possible to leverage a potential signals standard.

If this were to work out, many app developers would use signals through their chosen component framework; their patterns wouldn’t change. However, their framework would then be more interoperable (reactive data interoperability), smaller (signals are built in and don’t need to ship as JS), and hopefully faster (native signals as part of the JS runtime).

Library authors would then be able to write code using signals that works natively with any component or rendering library that understands the standard, reducing the fragmentation in the web ecosystem. Application developers would be able to build model/state layers that are decoupled from their current rendering technology, giving them more architectural flexibility and the ability to experiment with and evolve their view layer without re-writing their entire application.

So, let’s say you are a developer that wants to create a library using signals, or who wants to build an application state layer on these primitives. What would that code look like?

Well, we’ve seen a bit of it already, when I explained the basics of signals through the `Signal.State()` and `Signal.Computed()` APIs above. These are the two primary APIs that an application developer would use, if not using them indirectly through a framework’s API. They can be used by themselves to represent stand-alone reactive state and computations or in combination with other JavaScript constructs, such as classes. Here’s a `Counter` class that uses a signal to represent its internal state:

```
export class Counter {  
  #value = new Signal.State(0);  
  
  get value() {  
    return this.#value.get();  
  }  
  
  increment() {  
    this.#value.set(this.#value.get() + 1);  
  }  
  
  decrement() {  
    if (this.#value.get() > 0) {  
      this.#value.set(this.#value.get() - 1);  
    }  
  }  
}  
  
const c = new Counter();  
c.increment();  
console.log(c.value);
```

One particularly nice way to use signals is in combination with decorators. We can create a `@signal` decorator that turns an accessor into a signal as follows:

```
export function signal(target) {  
  const { get } = target;  
  
  return {  
    get() {  
      return get.call(this).get();  
    },  
  
    set(value) {  
      get.call(this).set(value);  
    },  
      
    init(value) {  
      return new Signal.State(value);  
    },  
  };  
}
```

Then we can use it to reduce boilerplate and improve readability of our `Counter` class like this:

```
export class Counter {  
  @signal accessor #value = 0;  
  
  get value() {  
    return this.#value;  
  }  
  
  increment() {  
    this.#value++;  
  }  
  
  decrement() {  
    if (this.#value > 0) {  
      this.#value--;  
    }  
  }  
}
```

There are many more ways to use signals, but hopefully these examples provide a good starting point for those who want to experiment at this state.

> **ASIDE**: Some users of particular signal libraries may not approve of my use of the following code above `this.#value.set(this.#value.get() + 1)`. In some signal implementations, this can cause an infinite loop when used within a computed or an effect. This does not cause a problem in the current proposal’s computed, nor does it cause a problem in the example effect demonstrated below. Should it cause a loop though? Or should it throw? What should be the behavior? This is an example of the many types of details that need to be worked through in order to standardize an API like this.

## As a library/infra dev, how do I integrate signals?

We hope that maintainers of view and component libraries will experiment with integrating this proposal, as well as those who create state management and data-related libraries. A first integration step would be to update the library’s signals to use `Signal.State()` and `Signal.Computed()` internally instead of their current library-specific implementation. Of course this isn’t enough. A common next step would be to update any `effect` or equivalent infrastructure. As I mentioned above, the proposal doesn’t provide an `effect` implementation. Our research showed that this was too connected to the details of rendering and batching to standardize at this point. Rather, the `Signal.subtle` namespace provides the primitives that a framework can use to build its own effects. Let’s take a look at the implementation of a simple `effect` function that batches updates on the microtask queue.

```
let needsEnqueue = true;  
  
const w = new Signal.subtle.Watcher(() => {  
  if (needsEnqueue) {  
    needsEnqueue = false;  
    queueMicrotask(processPending);  
  }  
});  
  
function processPending() {  
  needsEnqueue = true;  
      
  for (const s of w.getPending()) {  
    s.get();  
  }  
  
  w.watch();  
}  
  
export function effect(callback) {  
  let cleanup;  
    
  const computed = new Signal.Computed(() => {  
    typeof cleanup === "function" && cleanup();  
    cleanup = callback();  
  });  
    
  w.watch(computed);  
  computed.get();  
    
  return () => {  
    w.unwatch(computed);  
    typeof cleanup === "function" && cleanup();  
  };  
}
```

The `effect` function begins by creating a `Signal.Computed()` out of the user-provided callback. It can then use the `Signal.subtle.Watcher` to watch the computed’s sources. To enable the watcher to “see” the sources, we need to execute the computed at least once, which we do by calling `get()`. You may also notice that our `effect` implementation supports a basic mechanism for callbacks to provide cleanup functions as well as a way to stop watching, via the returned function.

Looking at the creation of the `Signal.subtle.Watcher`, the constructor takes a callback that will be invoked synchronously whenever any of its watched signals becomes dirty. Because a `Watcher` can watch any number of signals, we schedule processing of all dirty signals on the microtask queue. Some basic guard logic ensures that scheduling only happens once, until the pending signals are handled.

In the `processPending()` function, we loop over all the signals that the watcher has tracked as pending and re-evaluate them by calling `get().` We then ask the watcher to resume watching all its tracked signals again.

That’s the basics. Most frameworks will handle queuing in a way that’s integrated with their rendering or component system, and they’ll likely make other implementation changes in order to support the working model of their system.

### Other APIs

Another API that’s likely to be used in infrastructure is the `Signal.subtle.untrack()` helper. This function takes a callback to execute and ensures that signals read within the callback will not be tracked.

I feel the need to remind readers: the `Signal.subtle` namespace designates APIs that should be used with care, and mostly by framework or infrastructure authors. Using something like `Signal.subtle.untrack()` incorrectly or carelessly can mess up your application in ways that are difficult to track down.

With that said, let’s look at a legitimate use of this API.

Many view frameworks have a way to render a list of items. Typically, you pass the framework an array and a “template” or fragment of HTML that it should render for each item in the array. As an application developer, you want any interaction with that array to be tracked by the reactivity system so that your list’s rendered output will stay in sync with your data. But what about the framework itself? It must access the array in order to render it. If the framework’s access of the array were tracked by the dependency system, that would create all sorts of unnecessary connections in the graph, leading to false or over updating…not to mention the likelihood of performance problems and strange bugs. The `Signal.subtle.untrack()` API provides the library author with a simple way to handle this challenge. As an example, let’s look at a small bit of code from [SolidJS](https://www.solidjs.com/) that renders arrays, which I’ve slightly modified to use the proposed standard. We won’t look at the whole implementation. I’ve cut most of the code out for simplicity. Hopefully, looking at the high-level outline will help explain the use case.

```
export function mapArray(list, mapFn, options = {}) {  
  let items = [],  
      mapped = [],  
      len = 0,  
    /* ...other variables elided... */;  
  
  // ...elided...  
  
  return () => {  
    let newItems = list() || [], // Accessing the array gets tracked  
        i,  
        j;  
      
    // Accessing the length gets tracked  
    let newLen = newItems.length;  
  
    // Nothing in the following callback will be tracked. We don't want our  
    // framework's rendering work to affect the signal graph!  
    return Signal.subtle.untrack(() => {  
      let newIndices,  
          /* ...other variables elided... */;  
  
      // fast path for empty arrays  
      if (newLen === 0) {  
        // ... read from the array; not tracked ...  
      }  
      // fast path for new create  
      else if (len === 0) {  
        // ... read from the array; not tracked ...  
      } else {  
        // ... read from the array; not tracked ...  
      }  
  
      return mapped;  
    });  
  };  
}
```

Even though I’ve elided the bulk of Solid’s algorithm, you can see how the main body of work is done within an untracked block of code that accesses the array.

There are additional APIs within the `Signal.subtle` namespace which you can explore at your leisure. Hopefully, the above examples help to demonstrate the kinds of scenarios this part of the proposal is designed for.

## How can I get involved in the proposal?

Just jump in! [Everything is on GitHub](https://github.com/proposal-signals/proposal-signals). You’ll find the proposal in the root of the repo, and the polyfill in the `packages` folder. You can also [chat with us on Discord](https://discord.gg/5pguaYDvsb).

Here are a few ideas for how you can get started contributing:

* Try out signals within your framework or application.
* Improve the documentation/learning materials for signals.
* Document use cases (whether it’s something the API supports well or not).
* Write more tests, e.g., by porting them from other signal implementations.
* Port other signal implementations to this API.
* Write benchmarks for signals, both synthetic and real-world application ones.
* File issues on polyfill bugs, your design thoughts, etc.
* Try developing reactive data structures/state management abstractions on top of signals.
* Implement signals natively in a JS engine (behind a flag/in a PR, not shipped!)

There are also a variety of issues that have already been created to track ongoing areas of debate, potential modifications to algorithms, additional APIs, use cases, polyfill bugs, etc. Please take a look at those and see which ones you can provide insights on. If you are a framework or library author, we really want you to help us understand any scenarios or use cases that you think would pose a challenge for the current proposal.

## What’s next?

We’re still at the beginning of this effort. In the next few weeks [Daniel Ehrenberg](https://x.com/littledan?s=20) (Bloomberg) and [Jatin Ramanathan](https://twitter.com/JatinRamanathan) (Google/Wiz) will bring the proposal before TC39, seeking Stage 1. Stage 1 means that that proposal is under consideration. Right now, we’re not even there yet. You can think of signals as being at Stage 0. [The earliest of the early.](https://tc39.es/process-document/) After presenting at TC39, we’ll continue to evolve the proposal based on feedback from that meeting, and in line with what we hear from folks who get involved through GitHub.

Our approach is to take things slow and to prove ideas out through prototyping. We want to make sure that we don’t standardize something that no one can use. We’ll need your help to achieve this. With your contributions as described above, we believe we’ll be able to refine this proposal and make it suitable for all.

I believe a signal standard has tremendous potential for JavaScript and for the Web. It’s been exciting to work with such a great set of folks from the industry who are deeply invested in reactive systems. Here’s to more future collaboration and a better web for all. 🎊