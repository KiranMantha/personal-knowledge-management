---
title: "Mastering RxJS: operators and functions that can bite you when you don’t expect"
url: https://medium.com/p/cb2047cf5d4c
---

# Mastering RxJS: operators and functions that can bite you when you don’t expect

[Original](https://medium.com/p/cb2047cf5d4c)

# Mastering RxJS: operators and functions that can bite you when you don’t expect

[![Alexander Poshtaruk](https://miro.medium.com/v2/resize:fill:64:64/0*Jr0FPPwJYo2LNphW.)](/@alexanderposhtaruk?source=post_page---byline--cb2047cf5d4c---------------------------------------)

[Alexander Poshtaruk](/@alexanderposhtaruk?source=post_page---byline--cb2047cf5d4c---------------------------------------)

9 min read

·

Jul 18, 2019

--

3

Listen

Share

More

*The things you may not pay attention to but they are good to know*

Press enter or click to view image in full size

![]()

> [***AngularInDepth***](https://medium.com/angular-in-depth) ***is moving away from Medium.*** [***This article***](https://indepth.dev/mastering-rxjs-operators-and-functions-that-can-bite-you-when-you-dont-expect/)***, its updates and more recent articles are hosted on the new platform*** [***inDepth.dev***](https://indepth.dev/)

Press enter or click to view image in full size

![]()

> **Prerequisites:** You should be [familiar with RxJS](https://www.udemy.com/hands-on-rxjs-for-web-development/) and have some practical experience in using it.

### #1. [**fromFetch**](https://rxjs.dev/api/fetch/fromFetch) **function** vs [**ajax**](https://rxjs.dev/api/ajax/ajax) **const**

RxJS lib has two ways to wrap network request in Observable. And They have difference:

**fromFetch** function — uses [the Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) to make an HTTP request.

Press enter or click to view image in full size

![]()

**2. ajax** function — use XhrHttpRequest under the hood

Press enter or click to view image in full size

![]()

Both return Observable so we expect unfinished network request should be canceled on unsubscribe. Usually it works like that but there is small remark in the official documentation for [**fromFetch**](https://rxjs.dev/api/fetch/fromFetch):

> WARNING Parts of the fetch API are still experimental. `AbortController` is required for this implementation to work and use cancellation appropriately.
>
> Will automatically set up an internal [AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController) in order to teardown the internal `fetch` when the subscription tears down.

So ***beware*** if you use it in IE11 browser since [AbortController is not supported there](https://caniuse.com/#search=AbortController).

*\*Remark from* 

[*Nicholas Jamieson*](/u/d05557088657?source=post_page---user_mention--cb2047cf5d4c---------------------------------------)

*: there is a problem with the current implementation of `****fromFetch****`. See this* [*issue*](https://github.com/ReactiveX/rxjs/issues/4744)*.*

### #2. [forkJoin](https://rxjs.dev/api/index/function/forkJoin) vs [zip](https://rxjs.dev/api/index/function/zip)

There is a nice [tweet](https://twitter.com/thekiba_io/status/1131566351812890624) of 

[🦊 Reactive Fox 🚀](/u/73c42fbc4665?source=post_page---user_mention--cb2047cf5d4c---------------------------------------)

 “If you know Promise you already know RxJS”:

Press enter or click to view image in full size

![]()

So how it works:

1. We create many Observables that will do HTTP requests with **fromFetch** function.
2. **zip** function gets an array of such Observables and subscribes them causing HTTP requests to be performed.

Press enter or click to view image in full size

![]()

3. Zip waits until every argument Observable emit values with same index (index = 1 (or 0:) in our case) and emits an array of values .

4. Since all argument Observables produce only one value — so after all responses are fetched — zip produce array of responses.

You may think — everything is OK. And actually it is:) But only in this particular case. Why? because If you try to feed zip function with Observables that produce more then one value — you will get unexpected behavior (more then one emission or never-completed result Observable).

To prevent such possible drawbacks you can use **forkJoin** function.

**forkJoin** waits for all argument Observables to complete and then emit an array of last emitted values (to compare: **zip** emits an array of values with same emission index).

Press enter or click to view image in full size

![]()

Now our example will look like this:

Press enter or click to view image in full size

![]()

Now you are armed💪.

### #3. Using [materialize](https://rxjs.dev/api/operators/materialize), [dematerialize](https://rxjs.dev/api/operators/dematerialize) to mock delayed erred Observable

Say you have such function that makes a network request in Angular:

Press enter or click to view image in full size

![]()

Now to mock HttpClient successful response and emulate network latency you can provide such value:

Press enter or click to view image in full size

![]()

And you may think that to mock delayed erred response it is enough to do like this:

Press enter or click to view image in full size

![]()

But it will not work the way you expect. Once throwError produce error value — delay will be ignored and your error handler will be run immediately.

How to fix that? How to prevent error event to omit delay operator?

We can convert error emission to internal RxJS notification object and then return it back to a usual error with [**materialize**](https://rxjs.dev/api/operators/materialize) and [**dematerialize**](https://rxjs.dev/api/operators/dematerialize) operators.

Now our mock will look like this:

Press enter or click to view image in full size

![]()

You can read more about these operators in the official documentation [here](https://rxjs.dev/api/operators/materialize) and [here](https://rxjs.dev/api/operators/dematerialize).

### **#4 Using** [**timer**](https://rxjs.dev/api/index/function/timer) **function with one argument instead of of(0).pipe(delay(x))**

Previously If I had a need to emit once with initial delay i used such expression:

Press enter or click to view image in full size

![]()

It works well, but can we do it even better? Yes, with RxJS **timer** function. Timer definition looks like this:

> **timer(dueTime: number, period,** scheduler**)**

*duetime* — initial delay before starting emissions

*period* **—** The period of time between emissions of the subsequent numbers.

But what if I need to emit only once? Just use timer with one *dueTime* argument:

Press enter or click to view image in full size

![]()

*Do you like the article? You can find more interesting RxJS staff in my video-course “*[*Hands-on RxJS*](https://www.udemy.com/hands-on-rxjs-for-web-development/)*”. It may be interesting as for beginners (Section 1–3) as well as experiences RxJS developers (Sections 4–7). Buy it, watch it and leave comments and evaluations!*

[## Hands-On RxJS for Web Development | Udemy

### Harness the power of RxJS by solving real-life web tasks with Reactive programming; use Observables to code less

www.udemy.com](https://www.udemy.com/hands-on-rxjs-for-web-development/?source=post_page-----cb2047cf5d4c---------------------------------------)

### #5 [takeLast](https://rxjs.dev/api/operators/takeLast) with no param returns undefined

Once upon a time, I stepped on a rake by using [takeLast](https://rxjs.dev/api/operators/takeLast)() operator (RxJS ver 6.5.x). Just to remind you:

> **takeLast(count: number)**Waits until source is complete and then emits only the last `count` values emitted by the source Observable.

Somehow I expected that if applied without any param it returns 1 last value by default:

Press enter or click to view image in full size

![]()

But no — it returns undefined. To return 1 last value you should use it like this: *takeLast(1):*

Press enter or click to view image in full size

![]()

You can check this behavior in this [codepen](https://codepen.io/kievsash/pen/dEgyGX). Beware!

What can we do? Just open [an issue](https://github.com/ReactiveX/rxjs/issues/4851) and create a [pull-request](https://github.com/ReactiveX/rxjs/pull/4854) with fix🙃

### #6 from(fetch(url)) — eager vs defer(()=>from(fetch(url)) — lazy.

This tip came from another [tweet](https://twitter.com/jdjuan/status/1145966567341117441) of [Juan Herrera](https://twitter.com/jdjuan).

Press enter or click to view image in full size

![]()

OK, now let's go through it with explanations.

You know that Observables are lazy(do nothing until subscribed), Promises are eager (do everything when created) (more [here](https://itnext.io/promises-vs-observables-for-angularjs-to-angular-migration-1161afacef7e)).

Also, fetch returns Promise. This means that if we call ***fetch(‘url’)*** — network call will be performed at once. We can convert Promise to Observable with RxJS [from](https://rxjs.dev/api/index/function/from) the function but since fetch is called first — then anyway it will work in an eager way.

> **from(*fetch(‘url’)) //*** *will work in eager way*

So how to fix it? We can use RxJS [**defer**](https://rxjs.dev/api/index/function/defer) function.

> **defer(() => fetch(url)) //**will work in lazy way

One more note — in RxJS we already have special function that implements lazy fetch method —[**fromFetch**](https://rxjs.dev/api/fetch/fromFetch).

> **defer(() => fetch(url)) //**will work in lazy way  
> **fromFetch(url)** //do the same

If you take a look at *fromFetch* [sources](https://github.com/ReactiveX/rxjs/blob/6.x/src/internal/observable/dom/fetch.ts#L53) — you may observable how it implements deferred behavior.

Small hint 😎:

Press enter or click to view image in full size

![]()

Remember? We reviewed fromFetch in tip #1.

[![]()](http://eepurl.com/gHF0av)

### #7 [of](https://rxjs.dev/api/index/function/of)() == [EMPTY](https://rxjs.dev/api/index/const/EMPTY)

Typical [*switchMap*](https://rxjs.dev/api/operators/switchMap) operator example with the condition may look like:

Press enter or click to view image in full size

![]()

It works this way:

* [***interval***](https://rxjs.dev/api/index/function/interval) function generates incrementing numbers with some delay.
* switchMap callback checks if the emitted number is odd, if yes — it makes request wrapped in Observable and subscriber gets a result. If no — we return empty sequence constant — EMPTY (it completes at once).

Nothing special here. Recently I found out that we can us **of()** with no params to reach the same result. Now our example will look like:

Press enter or click to view image in full size

![]()

You can check yourself and play with it [here](https://codepen.io/kievsash/pen/ydrMre?editors=0010).

### #8 toPromise gives you the last value when Observable completes. Be careful when you use it with Subjects.

Angular2 subreddit sometimes brings [*interesting knowledge*](https://www.reddit.com/r/Angular2/comments/c8z8l4/issues_with_subjects_behaviorsubjectreplaysubject/) as well :-)

I will comment the code from this help request:

1. You have [WarehouseService](https://stackblitz.com/edit/behaviour-replay-subject-weird-behaviour-wmgqkg?file=index.ts), that provides some value with RxJS ***BehaviorSubject.*** As usual, we have some method getDefaultWarehouse there to get this Subject as Observable:

Press enter or click to view image in full size

![]()

2. Now we want to subscribe to emitted value and then use it with JS [***await***](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Async_await). So we need to convert Observable to Promise with [***toPromise()***](https://www.learnrxjs.io/operators/utility/topromise.html) method.

It will look like [this](https://stackblitz.com/edit/behaviour-replay-subject-weird-behaviour-wmgqkg?file=index.ts):

Press enter or click to view image in full size

![]()

So when DB is ready we emit row.defaultWarehouse value (see previous snippet) and in [index.ts](https://stackblitz.com/edit/behaviour-replay-subject-weird-behaviour-wmgqkg?file=index.ts) we await to get defWarehouse value.

But it never resolves. WHAT?

The reason is simple: RxJs method ‘toPromise()’ waits for your observable to complete. Since we use BehaviorSubject, that just emit value but don’t complete — toPromise will never be called.

You can solve it in two ways:

1. If WarehouseService should emit value with BevahiorSubject only once — then just complete it after emission:

Press enter or click to view image in full size

![]()

2. Or just subscribe to Observable to run a subsequent action.

Press enter or click to view image in full size

![]()

You can play with the code [here](https://stackblitz.com/edit/behaviour-replay-subject-weird-behaviour-wmgqkg?file=index.ts).

**More to read:**

1. [RxJs operator ‘toPromise’ waits for your observable to complete!](/@gparlakov/rxjs-operator-topromise-waits-for-your-observable-to-complete-e7a002f5dccb)

### #9 Different ways RxJS Subjects works after completion (Behavior, Replay, Async)

Recent [Angular-in-Depth 2019](https://angular-in-depth.org/) conference in Kyiv, Ukraine remind me about different behavior of RxJS [***BehaviorSubject***](https://rxjs.dev/api/index/class/BehaviorSubject), [***ReplaySubject***](https://rxjs.dev/api/index/class/ReplaySubject) and [***AsyncSubject***](https://rxjs.dev/api/index/class/AsyncSubject)after completion. Not to be very verbose — I just created a comparison table:

Press enter or click to view image in full size

![]()

You can play with it [here](https://codepen.io/kievsash/pen/ydrMre).

Press enter or click to view image in full size

![]()

**More to read and watch:**

1. Read 

   [Wojciech Trawiński](/u/9569ff590dd9?source=post_page---user_mention--cb2047cf5d4c---------------------------------------)

   ’s article “[*BehaviorSubject vs ReplaySubject(1) -beware of edge cases*](/javascript-everyday/behaviorsubject-vs-replaysubject-1-beware-of-edge-cases-b361153d9ccf)”.
2. Nice talk of [Michael Hladky](https://twitter.com/Michael_Hladky): “[*A deep dive into RxJS subjects*](https://www.youtube.com/watch?v=y2aBiA5N4h8)” at AiD conference.
3. “[Understanding RxJS BehaviorSubject, ReplaySubject and AsyncSubject](/@luukgruijs/understanding-rxjs-behaviorsubject-replaysubject-and-asyncsubject-8cc061f1cfc0)”.
4. All Angular-in-Depth conference 2019 talks [videos](https://www.youtube.com/channel/UCfiGD529EyGGA6fbQsl99BQ).

### #10 If we reassign Observable used in Angular template with asyncPipe — it will continue working.

Usually, Angular [*asyncPipe*](https://angular.io/api/common/AsyncPipe) usage looks something similar to this example:

Press enter or click to view image in full size

![]()

And we know that asyncPipe will handle all the Observable subscribe/unsubscribe activity to prevent memory leaks.

But what if we just re-assign **this.name** Observable with another Observable instance? Will AsyncPipe do unsubscription? Will it re-subscribe to a new Observable instance? Let's check it out!

1. I will add a button to re-assign this.name with new Observable instance.

Press enter or click to view image in full size

![]()

2. Also to check if AsyncPipe will unsubscribe I will create a copy of standard [Angular AsyncPipe from github](https://github.com/angular/angular/blob/master/packages/common/src/pipes/async_pipe.ts) and put it to our [demo Stackblitz project](https://stackblitz.com/edit/angular-jda28a) as custom Pipe.

Press enter or click to view image in full size

![]()

And added console.log to unsubscribe method to observe whether previous observable is unsubscribed.

![]()

Now, let's check what happens when Observable property is re-assigned.

Press enter or click to view image in full size

![]()

AS you can see — previous Observable is unsubscribed. Phew..we can sleep peacefully now!

You can check results in this [*Stackblitz playground*](https://stackblitz.com/edit/angular-jda28a).

### Conclusion

So, seems like you’ve become 10 gotcha’s richer 💰.

If you like this article — [**tweet about it**](https://clicktotweet.com/LoDz2) 🤓

Let’s keep in touch on [**Twitter**](https://twitter.com/El_Extremal).

Have your own tricky RxJS cases solved? Share in comments!

**Special thanks to** 

[**Nicholas Jamieson**](/u/d05557088657?source=post_page---user_mention--cb2047cf5d4c---------------------------------------)

**,** 

[**Lars Gyrup Brink Nielsen**](/u/f0e7507974eb?source=post_page---user_mention--cb2047cf5d4c---------------------------------------)

**,** 

[**Alex Okrushko**](/u/f7828ad40c7c?source=post_page---user_mention--cb2047cf5d4c---------------------------------------)

 **for reviewing this article!**