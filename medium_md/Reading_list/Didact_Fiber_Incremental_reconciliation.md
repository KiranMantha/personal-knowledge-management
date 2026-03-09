---
title: "Didact Fiber: Incremental reconciliation"
url: https://medium.com/p/b2fe028dcaec
---

# Didact Fiber: Incremental reconciliation

[Original](https://medium.com/p/b2fe028dcaec)

![]()

# Didact Fiber: Incremental reconciliation

[![Rodrigo Pombo](https://miro.medium.com/v2/resize:fill:64:64/1*lJ3fWONmPl2rX1QMolsanA.jpeg)](/@pomber?source=post_page---byline--b2fe028dcaec---------------------------------------)

[Rodrigo Pombo](/@pomber?source=post_page---byline--b2fe028dcaec---------------------------------------)

14 min read

·

Oct 19, 2017

--

11

Listen

Share

More

**[Update] This post is based on React before hooks, there’s** [**a new improved post**](https://pomb.us/build-your-own-react) **where we build everything from scratch including hooks, concurrent mode, fibers, etc.**

This story is part of a [series where we write our own version of React](https://engineering.hexacta.com/didact-learning-how-react-works-by-building-it-from-scratch-51007984e5c5), but since we are going to rewrite most of the old code anyway, I’ll *tl;dr* it for you:

> TL;DR of the series so far: We are writing a React clone to understand what React does under the hood. We call it Didact. To keep our code simple we focus only on React main features. First we covered how to render elements and make JSX work. We wrote the reconciliation algorithm to re-render only the stuff that changed between updates. And then we added class components and `setState()`.

Now React 16 is out, and with it a new internal architecture that required a rewrite of most of React’s code.

This means that some long-awaited features — that were hard to develop with the old architecture — were shipped.

It also means that most of the code we have written on this series is now worthless 😛.

In this post we are going to rewrite most of the code from the didact series to follow React 16 new architecture. We’ll try to mirror the structure, variables and function names from the React codebase. We’ll skip everything we don’t need for our public API:

* `Didact.createElement()`
* `Didact.render()` (only DOM rendering)
* `Didact.Component` (with `setState()` but not `context` or life cycle methods)

If you want to jump ahead and see the code working you can go to the [updated demo](https://codepen.io/pomber/pen/veVOdd) or visit the [github repository](https://github.com/hexacta/didact).

Let me explain why we need to rewrite the old code.

### Why Fiber

> This won’t offer the full picture of React Fiber. If you want to know more about it, please check this [list of resources](https://github.com/koba04/react-fiber-resources).

When the browser’s main thread is kept busy running something for a long time, critical brief tasks have to wait an unacceptable amount of time to get done.

To showcase this problem I made a [little demo](https://pomber.github.io/incremental-rendering-demo/react-sync.html). In order to keep the planets spinning, the main thread needs to be available for an instant every 16ms or so. If the main thread is blocked doing other stuff for, let’s say 200 ms, you’ll notice the animation missing frames and the planets frozen until the main thread is free again.

What makes the main thread so busy that can’t spare some microseconds on keeping the animation smooth and the UI responsive?

Remember the [reconciliation code](https://engineering.hexacta.com/didact-instances-reconciliation-and-virtual-dom-9316d650f1d0)? Once it starts reconciling it doesn’t stop. If the main thread needs to do anything else it will have to wait. And, **because it depends a lot on recursive calls, it’s hard to make it pausable.** That’s why we are going to rewrite it using a new data structure that will allow us to replace the recursive calls with loops.

### Scheduling micro-tasks

We’ll need to split up the work into smaller pieces, run those pieces for a short period of time, let the main thread do higher priority stuff, and come back to finish the work if there’s anything pending.

We’ll do this with the help of `requestIdleCallback()` function. It queues a callback to be called the next time the browser is idle and includes a `deadline` parameter describing how much time available we have for our code:

The real work happens inside the `performUnitOfWork` function. We need to write our reconciliation code there. The function should run a piece of the work and then returns all the information it needs to resume the work the next time.

To track those pieces of work we will use fibers.

### The fiber data structure

We will create a fiber for each component we want to render. The `nextUnitOfWork` will be a reference to the next fiber we want to work on. `performUnitOfWork` will work on that fiber and return a new one until all the work is finished. Bear with me, I’ll explain this in detail later.

How does a fiber look like?

It’s a plain old JavaScript object.

We’ll use the `parent`, `child`, and `sibling` properties to build a tree of fibers that describes the tree of components.

The `stateNode` will be the reference to the component instance. It could be either a DOM element or an instance of a user defined class component.

For example:

![]()

In the example we can see the three different kind of components we will support:

* The fibers for `b`, `p`, and `i` represent **host components**. We will identify them with the `tag` `HOST_COMPONENT`. The `type` for these fibers will be a string (the tag of the html element). The `props` will be the attributes and event listeners of the element.
* The `Foo` fiber represents a **class component**. Its `tag` will be `CLASS_COMPONENT` and the `type` a reference to the user defined class extending `Didact.Component`.
* The fiber for `div` represents the **host root**. It’s similar to a host component because it has a DOM element as the `stateNode` but being the root of the tree it will receive special treatment. The `tag` for this fiber will be `HOST_ROOT`. Note that the `stateNode` of this fiber is the DOM node passed to `Didact.render()`.

Another important property is `alternate`. We need it because most of the time we will have two fiber trees. **One tree will correspond to the things we’ve already rendered to the DOM, we’ll call it the *current* tree or the *old* tree. The other is the tree we build when we work on a new update (a call to** `setState()` **or** `Didact.render()`**), we’ll call this tree the *work-in-progress* tree.**

The work-in-progress tree won’t share any fiber with the old tree. Once we finished building the work-in-progress tree and made the needed DOM mutations, the work-in-progress tree becomes the *old* tree.

So we use `alternate` to link the work-in-progress fibers with their corresponding fibers from the oldtree. A fiber and its `alternate` share the same `tag`, `type` and `stateNode`. Sometimes — when we are rendering new stuff — fibers won’t have an `alternate`.

Finally, we have the `effects` list and `effectTag`. When we find a fiber in the work-in-progress tree that requires a change to the DOM we will set the `effectTag` to `PLACEMENT`, `UPDATE` or `DELETION`. To make it easier to commit all the DOM mutations together we keep a list of all the fibers (from the fiber sub-tree) that have an `effectTag` listed in `effects`.

That was probably too much information at once, don’t worry if you didn’t follow, we’ll see the fiber trees in action very soon.

### Didact call hierarchy

To get an idea of the flow of the code we are going to write take a look at this diagram:

![]()

We’ll start from `render()` and `setState()` and follow the flow ending at `commitAllWork()`.

### Old code

I told you that we are going to rewrite most of the code, but let’s first review the code that we are not rewriting.

In [Element creation and JSX](https://engineering.hexacta.com/didact-element-creation-and-jsx-d05171c55c56) we wrote the [code for](https://gist.github.com/pomber/2bf987785b1dea8c48baff04e453b07f) `createElement()`, the function used by transpiled JSX. We don’t need to change it, we’ll keep using the same elements. If you don’t know about elements, `type`, `props` and `children`, please review the old post.

In [Instances, reconciliation and virtual DOM](https://engineering.hexacta.com/didact-instances-reconciliation-and-virtual-dom-9316d650f1d0) we wrote `updateDomProperties()` for updating the DOM properties of a node. I also extracted the code for creating DOM elements to `createDomElement()`. You can see both functions in this [dom-utils.js gist](https://gist.github.com/pomber/c63bd22dbfa6c4af86ba2cae0a863064).

In [Components and state](https://engineering.hexacta.com/didact-components-and-state-53ab4c900e37) we wrote the `Component` base class. Let’s change it so `setState()` calls `scheduleUpdate()`, and `createInstance()` saves a reference to the fiber on the instance:

Starting with this code and nothing else let’s rewrite the rest from scratch.

![]()

Besides `Component` class and `createElement()`, we’ll have two public functions: `render()` and `setState()`, and we saw that `setState()` just calls `scheduleUpdate()`.

`render()` and `scheduleUpdate()` are similar, they receive a new update and queue it:

We’ll use the `updateQueue` array to keep track of the pending updates. Every call to `render()` or `scheduleUpdate()` pushes a new update to the `updateQueue`. The update information in each of the updates is different and we’ll see how we use it later in `resetNextUnitOfWork()`.

After pushing the update to the queue, we trigger a deferred call to `performWork()`.

![]()

Here’s where we use the `performUnitOfWork()` pattern that we saw earlier.

`requestIdleCallback()` calls the target function with a deadline as an argument. `performWork()` takes that deadline and pass it to `workLoop()`. After `workLoop()` returns, `performWork()` checks if there’s pending work. If there is, it schedules a new deferred call to itself.

`workLoop()` is the function that keeps an eye on the time. If the deadline is too close, it stops the work loop and leaves `nextUnitOfWork` updated so it can be resumed the next time.

> We use `ENOUGH_TIME` (a 1ms constant, same as [React’s](https://github.com/facebook/react/blob/b52a5624e95f77166ffa520476d68231640692f9/packages/react-reconciler/src/ReactFiberScheduler.js#L154)) to check if `deadline.timeRemaining()` is enough to run another unit of work or not. If `performUnitOfWork()` takes more than that, we will overrun the deadline. The deadline is just a suggestion from the browser, so overrunning it for a few milliseconds is not that bad.

`performUnitOfWork()` will build the work-in-progress tree for the update it’s working on and also find out what changes we need to apply to the DOM. **This will be done incrementally, one fiber at a time.**

When `performUnitOfWork()` finishes all the work for the current update, it returns null and leaves the pending changes to the DOM in `pendingCommit`. Finally, `commitAllWork()` will take the `effects` from `pendingCommit` and mutate the DOM.

Note that `commitAllWork()` is called outside of the loop. The work done on `performUnitOfWork()` won’t mutate the DOM so it’s OK to split it. On the other hand, `commitAllWork()` will mutate the DOM, it should be done all at once to avoid an inconsistent UI.

We still haven’t seen where the first `nextUnitOfWork` comes from.

![]()

The function that takes an update and convert it to the first `nextUnitOfWork` is `resetNextUnitOfWork()`:

`resetNextUnitOfWork()` starts by pulling the first update from the queue.

If the update has a `partialState` we store it on the fiber that belongs to the instance of the component, so we can use it later when we call component’s `render()`.

Then we find the root of the *old* fiber tree. If the updates comes from the first time `render()` was called, we won’t have a root fiber so `root` will be `null`. If it comes from a subsequent call to `render()`, we can find the root on the `_rootContainerFiber` property of the DOM node. And if the update comes from a `setState()`, we need to go up from the instance fiber until we find a fiber without `parent`.

Then we assign to `nextUnitOfWork` a new fiber. **This fiber is the root of a new work-in-progress tree**.

If we don’t have an *old* root, the `stateNode` will be the DOM node received as parameter in the `render()` call. The `props` will be the `newProps` from the update: an object with a `children` property that has the elements — the other parameter of `render()`. The `alternate` will be `null`.

If we do have an *old* root, the `stateNode` will be the DOM node from the previous root. The `props` will be again `newProps` if not `null`, or else we copy the `props` from the *old* root. The `alternate` will be the *old* root.

We now have the root of the work-in-progress tree, let’s start building the rest of it.

![]()

`performUnitOfWork()` walks the work-in-progress tree.

We call `beginWork()` — to create the new children of a fiber — and then return the first child so it becomes the `nextUnitOfWork`.

If there isn’t any child, we call `completeWork()` and return the `sibling` as the `nextUnitOfWork`.

If there isn’t any `sibling`, we go up to the parents calling `completeWork()` until we find a `sibling` (that we’ll become the `nextUnitOfWork`) or until we reach the root.

Calling `performUnitOfWork()` multiple times will go down the tree creating the children of the first child of each fiber until it finds a fiber without children. Then it moves right doing the same with the siblings. And the it moves up doing the same with the uncles. (For a more vivid description try render some components on [fiber-debugger](http://fiber-debugger.surge.sh/))

![]()

`beginWork()` does two things:

* create the `stateNode` if we don’t have one
* get the component children and pass them to `reconcileChildrenArray()`

Because both depend on the type of component we are dealing with, we split it in two: `updateHostComponent()` and `updateClassComponent()`.

`updateHostComponent()` handles host components and also the root component. It creates a new DOM node if it needs to (only one node, without children and without appending it to the DOM). **Then it calls** `reconcileChildrenArray()` **using the child elements from the fiber** `props`**.**

`updateClassComponent()` deals with class component instances. It creates a new instance calling the component constructor if it needs to. **It updates the instance’s** `props` **and** `state` **so it can call the** `render()` **function to get the new children.**

`updateClassComponent()` also validates if it makes sense to call `render()`. This is a simple version of `shouldComponentUpdate()`. If it looks like we don’t need to re-render, we just clone the current sub-tree to the work-in-progress tree without any reconciliation.

Now that we have the `newChildElements`, we are ready to create the child fibers for the work-in-progress fiber.

![]()

This is the heart of the library, where the work-in-progress tree grows and where we decide what changes we will do to the DOM on the commit phase.

Before starting we make sure `newChildElements` is an array. (Unlike the previous reconciliation algorithm, this one works always with arrays of children, this means we can now return arrays on component’s `render()` function)

Then we start comparing the children from the old fiber tree with the new elements (we compare fibers to elements). The children from the old fiber tree are the children of `wipFiber.alternate`. The new elements are the ones we got from the `wipFiber.props.children` or from calling `wipFiber.stateNode.render()`.

Our reconciliation algorithm works by matching the first old fiber (`wipFiber.alternate.child`) with the first child element (`elements[0]`), the second old fiber (`wipFiber.alternate.child.sibling`) to the second child element (`elements[1]`) and so on. For each `oldFiber`-`element` pair:

* If the `oldFiber` and the `element` have the same `type`, good news, it mean we can keep the old `stateNode`. We create a new fiber based on the old one. We add the `UPDATE` `effectTag`. And we append the new fiber to the work-in-progress tree.
* If we have an `element` with a different `type` to the `oldFiber` or we don’t have an `oldFiber` (because we have more new children than old children), we create a new fiber with the information we have in the `element`. Note that this new fiber won’t have an `alternate` and won’t have a `stateNode` ( the `stateNode` we’ll be created in `beginWork()`). The `effectTag` for this fiber is `PLACEMENT`.
* If the `oldFiber` and the `element` have a different `type` or there isn’t any `element` for this `oldFiber` (because we have more old children than new children) we tag the `oldFiber` for `DELETION`. Given that this fiber is not part of the work-in-progress tree, we need to add it now to the `wipFiber.effects` list so we don’t lose track of it.

> Unlike React, we are not using keys to do the reconciliation, so we won’t know if a child moved from it’s previous position.

![]()

`updateClassComponent()` has a special case where we take a shortcut and clone the old fiber sub-tree to the work-in-progress tree instead of doing the reconciliation.

`cloneChildFibers()` clones each of the `wipFiber.alternate` children and appends them to the work-in-progress tree. We don’t need to add any `effectTag` because we are sure that nothing changed.

![]()

In `performUnitOfWork()`, when a `wipFiber` doesn’t have new children or when we already completed the work of all the children, we call `completeWork()`.

`completeWork()` first updates the reference to the fiber related to the instance of a class component. (To be honest, this doesn’t really need to be here, but it has to be somewhere)

Then it build a list of `effects`. This list will contain all the fibers from the work-in-progress sub-tree that have any `effectTag` (it also contains the fibers from the old sub-tree with the `DELETION` `effectTag`). The idea is to accumulate in the root `effects` list all the fibers that have an `effectTag`.

Finally, if the fiber doesn’t have a `parent`, we are at the root of the work-in-progress tree. So we have completed all the work for this update and collected all the effects. We assign the root to `pendingCommit` so `workLoop()` can call `commitAllWork()`.

![]()

There’s one last thing we need to do: mutate the DOM.

`commitAllWork()` first iterates all the root `effects` calling `commitWork()` on each one. `commitWork()` checks the `effectTag` of each fiber:

* If it is a `PLACEMENT` we look for the parent DOM node and then simply append the fiber’s `stateNode`.
* If it is an `UPDATE` we pass the `stateNode` together with the old props and the new props and let `updateDomProperties()` decide what to update.
* If it is a `DELETION` and the fiber is a host component, it’s easy, we just call `removeChild()`. But if the fiber is a class component, before calling `removeChild()` we need to find all the host components from the fiber sub-tree that need to be removed.

Once we finished with all the effects, we can reset `nextUnitOfWork` and `pendingCommit`. The work-in-progress tree stops being the work-in-progress tree and becomes the old tree, so we assign its root to `_rootContainerFiber`. After that, we are done with the current update and we are ready to start the next one 🚀.

### Running Didact

If you want to put all together and expose only the public API you can do something like this:

Or you can play with the [updated version of the demo](https://codepen.io/pomber/pen/veVOdd) from the previous posts. All this code is also available at [Didact’s repository](https://github.com/hexacta/didact) and [npm](https://unpkg.com/didact).

### What’s next?

Didact is missing a lot of React’s features, but I’m particularly interested in scheduling the updates according to priorities:

So the next post may go that way.

That’s all! If you like it, don’t forget to clap 👏, [follow me on twitter](https://twitter.com/pomber), leave a comment, and all that stuff.

Thanks for reading.

> I build things at [Hexacta](http://www.hexacta.com/?hil=).
>
> If you had any idea or project we can help with, [write us](http://www.hexacta.com/contact/?hil=).