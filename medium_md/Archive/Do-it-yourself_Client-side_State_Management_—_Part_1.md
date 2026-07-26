---
title: "Do-it-yourself: Client-side State Management — Part 1"
url: https://medium.com/p/31396d28177f
---

# Do-it-yourself: Client-side State Management — Part 1

[Original](https://medium.com/p/31396d28177f)

# Do-it-yourself: Client-side State Management — Part 1

[![Adi Levinshtein](https://miro.medium.com/v2/resize:fill:64:64/0*6VA-g8U5jCiRYMmx.)](https://medium.com/@adi.levinshtein?source=post_page---byline--31396d28177f---------------------------------------)

[Adi Levinshtein](https://medium.com/@adi.levinshtein?source=post_page---byline--31396d28177f---------------------------------------)

3 min read

·

Jul 26, 2018

--

1

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D31396d28177f&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fdo-it-yourself-client-side-state-management-part-1-31396d28177f&source=---header_actions--31396d28177f---------------------post_audio_button------------------)

Share

Flux and Redux have come with the concept of maintaining an **application state**, and they both use **actions** to make changes to that state. They require tight coupling between the UI and the state. There are different approaches and patterns regarding state management, and these two patterns provide a basis for lots of innovation.

When I came across an article named “Flux from Scratch” (see link below), it inspired me to go ahead and do it myself: **take the key concepts and implement them! See how they work! Make them better!**This article describes the first step I’ve taken.

I will try to make it work using simple and straightforward code, without any external libraries (except jQuery for UI-related features). In this series I will research and implement concepts like **Flux**, **Redux, Immutability**, **Observables**, **Stores**, **Actions**, **Dispatchers**… and anything else that will seem relevant.

![]()

## First Steps Goals

The application is based on the sample from the “Flux from Scratch” article, and I want to make some changes… so lets…

* Create RxJS-like **Observable** and **BehaviorSubject**
* Subscribe to state changes instead of specific actions
* Maintain a history of state changes and add an option to undo state changes

## Code

We’ll start with the *Observable* class. This class will maintain a list of subscribers in the store, and will handle the notification process when the value is changed.

Changing the value is done by calling the *.next()* method and providing a new value.  
Subscriptions are added by the *.subscribe()* method — they are simply callback functions that accept the value.

When you simplify it you get a pretty straight-forward class:

You’ll notice that *MyObservable doesn’t accept an initial value and it doesn’t keep the value anywhere. It’s just a pipe that sends out notifications.*

On the other hand, there’s a *BehaviorSubject*. This class allows you to set the values and subscribe to changes, but it also keeps the current value, and exposes the *.getValue()* method.

Here’s my implementation:

## Observable vs. BehaviorSubject

Note there are some key differences between the types, and these differences will determine which is relevant to our needs:

* *BehaviorSubject* must have an initial value were *Observable* may remain undefined until *next()* is called for the first time.
* When subscribing to a *BehaviorSubject*, the it will return the last value, while *Observable* will not.
* You can create an *Observable* from a *BehaviorSubject* using the .*asObservable*() to get a read-only observable.

## Subscriptions

We can now **subscribe** to store changes. Subscriptions can have a reference and then they can be removed when no longer needed. So we now have 2 new methods: *subscribe()* and *unsubscribe().*

Usage example:

## History

![]()

When updating the state object, we can maintain an history of changes and add support for the *undo()* method which in turn executes the *unto()* method in the *MyBehaviorSubject*.

## Bonus: Multiple Stores

Now that we have different objects that can handle themselves, we’ve paved the way to using multiple stores that can run independently by generating multiple dispatchers and multiple stores.

Press enter or click to view image in full size

![]()

## Conclusion

By using Observables we were able to change the classic pattern to a **reactive** pattern — a patterns to responds to state changes and not specific actions. Just imagine subscribing to all actions or just 10–15 per component when you scale up your application and add more and more complexity.

Once the store can “handle itself” and maintain it’s own information, we can maintain a history of changes, and support multiple stores (or multiple “states”) in a single application.

## What’s Next?

In the next article we’ll consider the use of *selectors* and the option to subscribe to specific portions of the state. And, of course, we’ll start adding *middleware* to get things organized.

```
Reference"Flux from Scratch" by Ryan Funduk  
https://ryanfunduk.com/articles/flux-from-scratch/Code:  
https://codepen.io/rfunduk/pen/oXZzVx
```

```
GitHub repository:  
https://github.com/justguy/FluxDemoRx
```