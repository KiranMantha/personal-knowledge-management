---
title: "Animate Dynamic Components in Angular"
url: https://medium.com/p/10681438bdd4
---

# Animate Dynamic Components in Angular

[Original](https://medium.com/p/10681438bdd4)

# Animate Dynamic Components in Angular

[![Netanel Basal](https://miro.medium.com/v2/resize:fill:64:64/1*abTZV6gAiJNINYPHQUeOBg.png)](/@netbasal?source=post_page---byline--10681438bdd4---------------------------------------)

[Netanel Basal](/@netbasal?source=post_page---byline--10681438bdd4---------------------------------------)

3 min read

·

Aug 7, 2018

--

3

Listen

Share

More

![]()

In this article, we’ll learn two different techniques to animate a dynamic component in Angular as it enters and leaves.

In the first example, we leverage pure CSS animations to create the animation effects. Let’s build a snack bar to demonstrate.

Press enter or click to view image in full size

![]()

Let’s start with the component.

The component implementation is straightforward. We expect to get the content as input and display it in the snack bar container.

Let’s add some styles.

Now, we can continue to create the functionality that will dynamically generate the snack bar component and append it to the body.

The `resolveComponentFactory()` method takes a component and returns a `ComponentFactory`. You can think of `ComponentFactory` as an object that knows how to create a component. Once we have a factory, we can use the `create()`method to create a `componentRef` instance, passing the current injector.

A `componentRef` exposes a reference to the native DOM element, which we then append to the body.

In this stage, we can call the `open()` method. The result — we’ll get a working snack bar with entering animation.

Press enter or click to view image in full size

![]()

Now, let’s move on to closing the snack bar. First, we need to add the closing animation.

Listen for the closing click event and apply the leaving animation to the snack bar element.

In this stage, we’ll see the leaving animation, but the component will still be visible. The key point here is to wait for the animation to end and then call the `componentRef.destroy()` method and remove the DOM element from the body.

To achieve this, we can use the browser `animationend` event — the `animationend` event occurs when a CSS animation is completed.

One of the properties of the `animationend` event is the name of the current animation. We can check to see if the current animation is the `snackbarOut` animation. If it is, we can emit the `afterClose` event.

Now, in the `open()` method, we can subscribe to the `afterClose` event and destroy the component, **but only after the animation ends**.

We can also take it further, change it to be auto dismissible and accept the animation duration from the consumer.

Our second example uses the same technique, but this time with Angular animations. I won’t expand on this too much, because it’s basically the same flow as the first example.

It’s just a matter of changing the animation state according to the component status, listening for the animation done event, and destroying the component.

Here is a full working example:

Press enter or click to view image in full size

![]()

## 👂🏻 **Last but Not Least, Have you Heard of Akita?**

Akita is a state management pattern that we’ve developed here in Datorama. It’s been successfully used in a big data production environment for over seven months, and we’re continually adding features to it.

Akita encourages simplicity. It saves you the hassle of creating boilerplate code and offers powerful tools with a moderate learning curve, suitable for both experienced and inexperienced developers alike.

I highly recommend checking it out.

[## 🚀 Introducing Akita: A New State Management Pattern for Angular Applications

### Every developer knows state management is difficult. Continuously keeping track of what has been updated, why, and…

netbasal.com](https://netbasal.com/introducing-akita-a-new-state-management-pattern-for-angular-applications-f2f0fab5a8?source=post_page-----10681438bdd4---------------------------------------)

*Follow me on* [*Medium*](/@NetanelBasal/) *or* [*Twitter*](https://twitter.com/NetanelBasal) *to read more about Angular, Akita and JS!*