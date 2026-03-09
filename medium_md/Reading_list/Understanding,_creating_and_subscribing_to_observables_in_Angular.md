---
title: "Understanding, creating and subscribing to observables in Angular"
url: https://medium.com/p/426dbf0b04a3
---

# Understanding, creating and subscribing to observables in Angular

[Original](https://medium.com/p/426dbf0b04a3)

Member-only story

# Understanding, creating and subscribing to observables in Angular

[![Luuk Gruijs](https://miro.medium.com/v2/resize:fill:64:64/1*oo57MR_29jXb9o4GuFsPIw.jpeg)](/?source=post_page---byline--426dbf0b04a3---------------------------------------)

[Luuk Gruijs](/?source=post_page---byline--426dbf0b04a3---------------------------------------)

5 min read

·

Aug 19, 2017

--

61

Listen

Share

More

When version 2 of Angular came out, it introduced us to observables. The Observable isn’t an Angular specific feature, but a new standard for managing async data that will be included in the ES7 release. Angular uses observables extensively in the event system and the HTTP service. Getting your head around observables can be quite a thing, therefore i’m here to explain it the easy way.

Press enter or click to view image in full size

![]()

## Observables

> Observables are lazy collections of multiple values over time.

yeah, right…well, actually it’s pretty easy:

1. **Observables are lazy**  
   You could think of lazy observables as newsletters. For each subscriber a new newsletter is created. They are then only send to those people, and not to anyone else.
2. **Observables can have multiple values over time**  
   Now if you keep that subscription to the newsletter open, you will get a new one every once and a while. The sender decides when you get it but all you have to do is just wait until it comes straight into your inbox.

If you come from the world of promises this is a key difference as promises always return only one value. Another thing is that observables are cancelable. If you don’t want your newsletter anymore, you unsubscribe. With promises this is different, you can’t cancel a promise. If the promise is handed to you, the process that will produce that promise’s resolution is already underway, and you generally don’t have access to prevent that promise’s resolution from executing.

## Push vs pull

A key thing to understand when using observables is that observables push. Push and pull are two different ways that describe how a *data producer* communicates with the *data consumer*.

**Pull**When pulling, the data consumer decides when it get’s data from the data producer. The producer is unaware of when data will be delivered to the consumer.

Every javascript function uses the pull. The function is a Producer of data, and the code that calls the function is consuming it by “pulling” out a *single* return value from its call.

**Push**When pushing, it works the other way around. The data producer (the creator of the newsletter) decides when the consumer (the subscriber to the newsletter) gets the data.

Promises are the most common way of push in JavaScript today. A promise (the producer) delivers a resolved value to registered callbacks (the consumers), but unlike functions, it is the promise which is in charge of determining precisely when that value is “pushed” to the callbacks.

Observables are a new way of pushing data in JavaScript. An observable is a Producer of multiple values, “pushing” them to subscribers.

## Observables in Angular

If you start using Angular you will probably encounter observables when setting up your HTTP requests. So let’s start there.

We have now created a simple HttpClient with a fetchUsers method that returns an observable. We probably like to display the users in some sort of list, so let’s do something with this method. Since this method returns an observable we have to subscribe to it. In Angular we can subscribe to an observable in two ways:

**Manner 1:**  
We subscribe to an observable in our template using the async pipe. The benefit of this is that Angular deals with your subscription during the lifecycle of a component. Angular will automatically subscribe and unsubscribe for you. Don’t forget to import the “CommonModule” into your module, as the async pipe will be exposed from that.

Please note the dollar sign. Using the dollar sign in the name of a variable that is an observable, is considered best practice. This way it’s easy to identify if your variable is an observable or not.

**Manner 2:**  
We subscribe to the observable ourselves using the actual `subscribe()` method. This can be handy if you would first like to do something with the data before displaying it. The downside is that you have to manage the subscription yourself.

As you can see the template logic is quite similar, the component logic can actually become much different en more complex if you go for manner 2. In general i would recommend to choose manner 1. As this is the most easy and you don’t have to manually manage your subscriptions. Keeping your subscriptions open while not using them is a memory leak and therefore not good.

## Creating an observable yourself

Now that you know how to deal with common observables that are given to you by Angular, it’s good to know how you create an observable yourself. The simplest version looks like this:

As you can see in the example observables are **created** by using the `new Observable()` call, then **subscribed** to by an observer, **executed** by calling the `next()` and **disposed** by calling `unsubscribe()`.

**Creating observables**Creating observables is easy, just call the `new Observable()` and pass along one argument which represents the observer. Therefore i usually call it “observer” as well.

**Subscribing to observables**Remember, observables are lazy. If you don’t subscribe nothing is going to happen. It’s good to know that when you subscribe to an observer, each call of `subscribe()` will trigger it’s own independent execution for that given observer. Subscribe calls are not shared among multiple subscribers to the same observable.

**Executing observables**The code inside an observables represents the execution of the observables. On the parameter that was given when creating the observable there are three functions available to send data to the subscribers of the observable:

* “next”: sends any value such as Numbers, Arrays or objects to it’s subscribers.
* “error”: sends a Javascript error or exception
* “complete”: does not send any value.

Calls of the next are the most common as they actually deliver the data to it’s subscribers. During observable execution there can be an infinite calls to the `observer.next()`, however when `observer.error()` or `observer.complete()` is called, the execution stops and no more data will be delivered to the subscribers.

**Disposing observables**Because observable execution can run for an infinite amount of time, we need a way to stop it from executing. Since each execution is run for every subscriber it’s important to not keep subscriptions open for subscribers that don’t need data anymore, as that would mean a waste of memory and computing power.

When you subscribe to an observable, you get back a subscription, which represents the ongoing execution. Just call `unsubscribe()`to cancel the execution.

## Conclusion

This post should give you a better understanding of how observables actually work. To get even more out of observables the next step is to understand the power of Rxjs and all the helper functions they provide. Rxjs alone could cover multiple posts which i will write about later. If you want to get one step further. Checkout my post about rxjs subjects: <https://hackernoon.com/understanding-rxjs-subjects-339428a1815b>

## We are hiring!

We are hiring: <https://jobs.founda.com/backend-developer/en>