---
title: "Understanding rxjs Subjects"
url: https://medium.com/p/339428a1815b
---

# Understanding rxjs Subjects

[Original](https://medium.com/p/339428a1815b)

Member-only story

# Understanding rxjs Subjects

[![Luuk Gruijs](https://miro.medium.com/v2/resize:fill:64:64/1*oo57MR_29jXb9o4GuFsPIw.jpeg)](/?source=post_page---byline--339428a1815b---------------------------------------)

[Luuk Gruijs](/?source=post_page---byline--339428a1815b---------------------------------------)

2 min read

·

Apr 17, 2018

--

32

Listen

Share

More

Rxjs is great. It helps you with composing and subscribing to data streams. You probably do this a lot with “plain” Observables. Rxjs however offers a multiple classes to use with data streams, and one of them is a Subject.

If you think you understand Observables, read on! Else i suggest you to read more about it in my other article: [Understanding, creating and subscribing to observables in Angular](https://medium.com/@luukgruijs/understanding-creating-and-subscribing-to-observables-in-angular-426dbf0b04a3).

Press enter or click to view image in full size

![]()

## Subjects

A Subject is like an Observable. It can be subscribed to, just like you normally would with Observables. It also has methods like `next()`, `error()` and `complete()` just like the observer you normally pass to your Observable creation function.

The main reason to use Subjects is to multicast. An Observable by default is unicast. Unicasting means that each subscribed observer owns an independent execution of the Observable. To demonstrate this:

While Observables are unicast by design, this can be pretty annoying if you expect that each subscriber receives the same values. Subjects can help us overcome this issue. As mentioned before, Subjects can multicast. Multicasting basically means that one Observable execution is shared among multiple subscribers.

Subjects are like EventEmitters, they maintain a registry of many listeners. When calling subscribe on a Subject it does not invoke a new execution that delivers data. It simply registers the given Observer in a list of Observers.

## So how to use Subjects to multicast

Multicasting is a characteristic of a Subject. You don’t have to do anything special to achieve this behaviour. This is a small multicast demonstration:

Nice! Now i got two subscriptions getting the same data. This however is not all that Subjects can do.

Whereas Observables are solely data producers, Subjects can both be used as a data producer and a data consumer. By using Subjects as a data consumer you can use them to convert Observables from unicast to multicast. Here’s a demonstration of that:

We pass our Subject to the subscribe function and let it take the values that come out of the Observable (data consuming). All the subscribers to that Subject will then all immediately receive that value.

## Conclusion

If you ever encounter the scenario where your Observable subscriptions receive different values, use Subjects. Subjects will make sure each subscription gets the exact same value as the Observable execution is shared among the subscribers. Subjects come in different flavours, i will soon write about their differences.

## We are hiring!

We are hiring: <https://jobs.founda.com/backend-developer/en>