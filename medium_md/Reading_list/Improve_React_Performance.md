---
title: "Improve React Performance"
url: https://medium.com/p/61a10e741edb
---

# Improve React Performance

[Original](https://medium.com/p/61a10e741edb)

Member-only story

# Improve React Performance

## By eliminating unnecessary renders

[![Bowei](https://miro.medium.com/v2/resize:fill:64:64/1*2s7k5AoOmK5jWVuhRhRz9w.jpeg)](/@boweihan?source=post_page---byline--61a10e741edb---------------------------------------)

[Bowei](/@boweihan?source=post_page---byline--61a10e741edb---------------------------------------)

7 min read

·

Oct 18, 2018

--

4

Listen

Share

More

My team recently spent some time making performance improvements to a data-reporting front-end we build and maintain at [Vena Solutions](https://venasolutions.com/). The application is built entirely in React and has grown to the point where we are starting to notice sluggish performance in certain views and features — especially those tasked with rendering many sub-components (lists and trees). It turns out that most of our issues were the result of sub-optimal key usage and avoidable component re-rendering.

This article highlights some optimizations we used to eliminate unnecessary re-rendering and improve the performance of our React application.

## **Pre-Optimization — Don’t Abuse Keys!**

> Keys can turn your application into a rendering jackhammer.

Press enter or click to view image in full size

![]()

Keys are an essential prop when iteratively rendering collections of elements. React uses them to keep track of elements in collections and poor choices for keys — keys that are not **stable, predictable and unique** — can lead to inefficient or even incorrect rendering behaviour. Examples of potentially suboptimal keys include timestamps (an unstable key that will always force a render), array indices (an unpredictable key that may not always map back to the same element) and duplicated keys.

Press enter or click to view image in full size

![]()

There are a time and a place to use keys (e.g. when dealing with lists) but it is also quite easy to **misuse** keys. Our data-reporting front-end had situations where keys were used to forcibly re-render **non-iterated components** in cases where render behaviour is poorly understood or when third-party libraries are involved.

Press enter or click to view image in full size

![]()

The key prop causes React to discard the entire component instance and DOM subtree every time the value of the key changes. Removing instances of misused keys is a necessary pre-optimization because it makes it very hard to apply any further optimizations.

## Optimization **— Use PureComponent**

> Use PureComponent when you have performance issues and have determined that a specific component was re-rendering too often, but its props and/or state are shallowly equal— Dan Abramov

The **PureComponent** base class was added to React in version 15.3.0 and provides a simple render optimization out of the box. A regular **Component** will render whenever it receives new props or state but a **PureComponent** will perform a shallow comparison of props and state and only render if there is a difference. The initial quote from Dan Abramov says it all — use PureComponent if you notice rendering happening even though props and state have not changed. These are avoidable renders and can be slowing your application down significantly!

I used [create-react-app](https://github.com/facebook/create-react-app) to scaffold a very simple demonstration of the impact of PureComponent [here](https://github.com/boweihan/react-performance-demo). The application renders a custom List component that iteratively creates a long list of custom ListItem components (20000 to be exact).

Press enter or click to view image in full size

![]()

The render button triggers a `setState` operation that simply passes back the same state. The performance of this application when simply extending **Component** is shown below. The colours in the flame graph indicate that all components are being re-rendered even though there is no difference in state and props. Pay close attention to the `Render duration` field on the flame graph as you continue reading.

Press enter or click to view image in full size

![]()

The render takes almost a second even though nothing new is applied to the page! Let’s now have ListItem extend **PureComponent**instead of **Component***.* The ListItems now do not re-render (you can tell because they are greyed out).

Press enter or click to view image in full size

![]()

219 ms — getting there. Let’s now have List extend **PureComponent**as well*.* We can tell from the flame graph that the application is now smart enough to only re-render the app component itself after `setState`.

Press enter or click to view image in full size

![]()

Simply changing the base classes to be **PureComponent** and avoiding unnecessary re-renders was enough for a 100x performance improvement! This example may seem a tad trivial but re-rendering components when there are no changes to props or state is very common in applications that do not keep a keen eye on performance.

A great way to monitor your application for avoidable renders is to install an npm package called [why-did-you-update](https://github.com/maicki/why-did-you-update) which will monitor and log avoidable component renders straight into your browser console at runtime. My first use of this tool was quite an eye-opener…

Press enter or click to view image in full size

![]()

**PureComponent**is great when all you care about is shallow prop and state changes but there are cases when it doesn’t quite cut it — namely when…

1. Component render state is dependent on nested state/props.
2. State or props contains objects that are being re-created with the same properties (PureComponent uses `===` which compares **object references rather than actually comparing object properties** and since two different object instances will never satisfy strict equality the PureComponent will always re-render even if the object properties and values are the exact same!).
3. Certain properties on state or props are changing but do not affect the render state of the component (irrelevant props could be those that are passed through to child components).

Thankfully, we have options.

## Optimization**—** ShouldComponentUpdate

> I’d just like to take a moment and thank #react for #shouldComponentUpdate ❤ — some person on twitter

**ShouldComponentUpdate** is a React component lifecycle method that determines whether or not a component should continue its render lifecycle. The method is called right before render. (You can find it in the `Updating` block on the React LifeCycle Cheat Sheet).

Press enter or click to view image in full size

![]()

**PureComponent** and **Component** actually implement this method under the hood in order to achieve selective rendering. I’ll start by providing some code samples which hopefully make it pretty clear what this method should do.

### *Component* implementation:

### PureComponent implementation:

The [shallowEqual implementation](https://github.com/facebook/fbjs/blob/master/packages/fbjs/src/core/shallowEqual.js) used in the above source code can be found on Facebook’s Github page.

ShouldComponentUpdate provides the flexibility for you to choose exactly **when** and **why** your components should update.

Back to Vena’s data-reporting application…a particularly poor area of performance involved a tree view component which we found was re-rendering entire subtrees instead of just the nodes affected by an update. The component is a tad complex and was producing a bloated flame graph for an operation which only updates the state of a single top-level node.

Press enter or click to view image in full size

![]()

This performance is acceptable for small trees but the user experience is unbearable for larger trees. The majority of these renders are avoidable. The data for each node is nested in nature so we can’t simply rely on **PureComponent** to sort out our render issues and instead have to implement a custom shouldComponentUpdate method.

This change means that the nodes are now rendered on an **as-needed basis** and the component render count is effectively O(1) instead of O(N) with respect to the tree. The updated flame graph looks like this:

Press enter or click to view image in full size

![]()

That’s a 328x improvement! ShouldComponentUpdate makes these optimizations possible.

## There’s more…

The three performance areas covered in this post — *keys, PureComponent, and ShouldComponentUpdate* — are just the tip on the iceberg of potential performance improvements. We are conceptually solving caching problems and there are a few other areas to implement rendering improvements that come to mind:

* Using [recompose](https://github.com/acdlite/recompose) to add selective rendering behaviour to your functional components.
* Memoizing computationally intensive electors with [reselect](https://github.com/reduxjs/reselect) (for Redux).
* Lazy loading components and virtualizing lists. Libraries such as [react-virtualized](https://github.com/bvaughn/react-virtualized) can help.
* Caching with service workers

At Vena, we were able to solve most of our immediate issues by tackling the highlighted areas but we’re ready for the next challenge as we continue to scale!

[## Frontend at Scale

### Articles related to the scaling of frontend processes, teams, and technology. Follow to stay up to date!

medium.com](https://medium.com/frontend-at-scale?source=post_page-----61a10e741edb---------------------------------------)