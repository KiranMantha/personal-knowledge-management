---
title: "Testing Observables in Angular"
url: https://medium.com/p/a2dbbfaf5329
---

# Testing Observables in Angular

[Original](https://medium.com/p/a2dbbfaf5329)

# Testing Observables in Angular

[![Netanel Basal](https://miro.medium.com/v2/resize:fill:64:64/1*abTZV6gAiJNINYPHQUeOBg.png)](/@netbasal?source=post_page---byline--a2dbbfaf5329---------------------------------------)

[Netanel Basal](/@netbasal?source=post_page---byline--a2dbbfaf5329---------------------------------------)

3 min read

·

Apr 4, 2018

--

14

Listen

Share

More

![]()

In this article, I’d like to talk about a misconception I’ve read in other articles about writing tests for observables in Angular.

Let’s examine this basic example we’re all familiar with.

We have data service that uses the Angular HTTP library to return cold observable.

Other articles around the web suggest that, in order to test the above component, we can create a stub service that returns an `of()` observable.

You run the code above. The test passes, and you are 👯 👯 👯 👯 👯

> That’s what I call cheating 🙈

By default, the `of()` observable is synchronous, so you’re basically making asynchronous code synchronous.

Let’s demonstrate this with a small add-on to our code.

We added a loading element that should be visible when the request begins but hidden when the subscription function is called. (i.e., the request finished successfully)

Let’s test it.

As you likely imagined, the above test will never pass. You will get the error:

> Expected null not to be null.

When we run `detectChanges()`, the `ngOnInit()` hook will run and execute the subscription function synchronously, causing the `isLoading` property to always be false. As a result, the test always fails.

You probably remember the old days, when we wrote tests in AngularJS and stub promises like this:

```
spyOn(todosService,'get').and.returnValue(deferred.promise);
```

The code above is completely valid — unlike observables, promises are always asynchronous.

Let me show you three ways to correct the above.

## Using defer()

Those who’d rather stick to promises can return a `defer()` observable that will return a promise with the data.

We use `defer()` to create a block that is only executed when the resulting observable is subscribed to.

## Using Schedulers

Schedulers influence the timing of task execution. You can change the default schedulers of some operators by passing in an extra scheduler argument.

The `async` scheduler schedules tasks asynchronously by setting them on the JavaScript event loop queue. This scheduler is best used to delay tasks in time or schedule tasks at repeating intervals.

You can read more about schedulers [here](https://blog.strongbrew.io/what-are-schedulers-in-rxjs/).

## Using jasmine-marbles

RxJS marble testing is an excellent way to test both simple and complex observable scenarios.

Marble testing uses a similar marble language to specify your tests’ observable streams and expectations.

This test defines a *cold* observable that waits two frames (`--`), emits a value (`x`), and completes (`|`). In the second argument, you can map the value marker (`x`) to the emitted value (`todos`).

Here are a few more resources to learn about marble testing:

1. The official [docs](https://github.com/ReactiveX/rxjs/blob/master/doc/writing-marble-tests.md).
2. [Marble testing Observable Introductio](/@bencabanes/marble-testing-observable-introduction-1f5ad39231c)n.
3. [RxJS Marble Testing: RTFM](https://blog.angularindepth.com/rxjs-marble-testing-rtfm-a9a6cd3db758)

*Follow me on* [*Medium*](/@NetanelBasal/) *or* [*Twitter*](https://twitter.com/NetanelBasal) *to read more about Angular, Vue and JS!*

## 👂🏻 Last but Not Least, Have you Heard of Akita?

Akita is a state management pattern that we’ve developed here in Datorama. It’s been successfully used in a big data production environment for over seven months, and we’re continually adding features to it.

Akita encourages simplicity. It saves you the hassle of creating boilerplate code and offers powerful tools with a moderate learning curve, suitable for both experienced and inexperienced developers alike.

I highly recommend checking it out.

[## 🚀 Introducing Akita: A New State Management Pattern for Angular Applications

### Every developer knows state management is difficult. Continuously keeping track of what has been updated, why, and…

netbasal.com](https://netbasal.com/introducing-akita-a-new-state-management-pattern-for-angular-applications-f2f0fab5a8?source=post_page-----a2dbbfaf5329---------------------------------------)