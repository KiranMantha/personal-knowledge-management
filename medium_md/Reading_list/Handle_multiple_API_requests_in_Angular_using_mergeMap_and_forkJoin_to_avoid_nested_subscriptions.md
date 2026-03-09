---
title: "Handle multiple API requests in Angular using mergeMap and forkJoin to avoid nested subscriptions"
url: https://medium.com/p/a20fb5040d0c
---

# Handle multiple API requests in Angular using mergeMap and forkJoin to avoid nested subscriptions

[Original](https://medium.com/p/a20fb5040d0c)

Member-only story

## Angular

# Handle multiple API requests in Angular using mergeMap and forkJoin to avoid nested subscriptions

## A guide on how to use `mergeMap` and `forkJoin` to avoid nested subscriptions when calling multiple APIs

[![Hoang Subin](https://miro.medium.com/v2/resize:fill:64:64/1*f3_OiQrKPejLLiJKAE4OjA.png)](https://ecmascript.medium.com/?source=post_page---byline--a20fb5040d0c---------------------------------------)

[Hoang Subin](https://ecmascript.medium.com/?source=post_page---byline--a20fb5040d0c---------------------------------------)

5 min read

·

Oct 14, 2019

--

17

Listen

Share

More

Press enter or click to view image in full size

![]()

In this article, I will introduce two techniques to handle multiple requests in Angular by using [mergeMap](https://www.learnrxjs.io/operators/transformation/mergemap.html) and [forkJoin](https://www.learnrxjs.io/operators/combination/forkjoin.html).

Contents:

1. Problem
2. `subscribe`
3. `mergeMap`
4. `forkJoin`
5. Combine `mergeMap` and `forkJoin`
6. Performance comparison of `subscribe` vs `mergeMap` and `forkJoin`

*For more content like this, check out* <https://betterfullstack.com>

## Problem

In the real world, we frequently call more than one API in our web applications. When you enter a page, you often make multiple requests to retrieve all the required data, and the results of some API requests are required for subsequent calls.

When we make multiple requests, it’s important to handle them effectively to maintain fast performance for your users while also writing good code.

I will demonstrate a simple project which will have 3 requirements by using a dummy API at <https://jsonplaceholder.typicode.com>:

1. Call the API to authenticate and retrieve user information
2. Based on the user information, we call one API to get all posts created by the user.
3. Based on the user information, we call one API to get all the albums created by the user.

`subscribe` is a common way to handle requests in Angular, but there are more effective methods. We will first solve our problem using `subscribe` and then improve on it using `mergeMap` and `forkJoin`

## Subscribe

Using this technique is quite simple. First, we call one API to get user info, and then we call the other two APIs. We do this in a nested subscription so we can use the results from the first API call.

Press enter or click to view image in full size

![]()

This technique is fine for 2 or 3 requests, but it is hard to read for more requests as your app grows. We would be required to create a lot of nested subscription. That is why we will use RxJS to handle multiple requests.

## MergeMap

This operator is best used when you wish to flatten an inner observable but want to manually control the number of inner subscriptions.

So when do we apply `mergeMap`?

When we need data from the first API request to make requests to the second API.

Press enter or click to view image in full size

![]()

Look at the source code above, we can see that second API needs the user ID from the first API to get data.

Note:

1. `flatMap` is an alias for `mergeMap`.
2. `mergeMap` maintains multiple active inner subscriptions at once, so it’s possible to create a memory leak through long-lived inner subscriptions.

## ForkJoin

This operator is best used when you have a group of observables and only care about the final emitted value of each. It means that `forkJoin` allows us to group multiple observables and execute them in parallel, then return only one observable.

When do we apply `forkJoin`?

We use it when API requests are independent. It means that they do not depend on each other to complete and can execute in parallel.

Press enter or click to view image in full size

![]()

## Combine mergeMap and forkJoin

In the real world, there are multiple API requests that depend on the result of another request. So let’s see how can we handle that case by using `mergeMap` and `forkJoin`.

Here is a sample to solve our problem:

Press enter or click to view image in full size

![]()

By using these functions, we avoided nested subscriptions and can split code into many small methods.

You have to replace `userId` inside `mergeMap` by `user` that return from `map` above.

## Performance comparison of subscribe vs mergeMap and forkJoin

The only difference I noticed is parsing HTML.

First, take a look at the parse HTML time by using nested subscription:

![]()

Then, look at parse HTML time by using `mergeMap` and `forkJoin`:

![]()

I tried to render the page many times to compare the result, and I discovered that the parse HTML time when using `mergeMap` and `forkJoin` is always faster than the time when using nested subscriptions, but the difference is pretty small (~100ms).

The important thing is knowing how to make the code more readable and maintainable.

## Summary

To sum it up, we can use RxJS to handle multiple requests in Angular. This helps us to write code that is more readable and maintainable. As an added bonus, we also see a slight performance increase by using our RxJS function compared to nested subscriptions.

I hope you found this article useful! You can follow me on [Medium](https://medium.com/@transonhoang). I am also on [Twitter](https://twitter.com/transonhoang). Feel free to leave any questions in the comments below. I’ll be glad to help out!

Check source code here.

[## multiple-request-handling - StackBlitz

### Starter project for Angular apps that exports to the Angular CLI

stackblitz.com](https://stackblitz.com/edit/multiple-request-handling?embed=1&file=src%2Fapp%2Fapp.component.ts&source=post_page-----a20fb5040d0c---------------------------------------)

[## Stories - Better FullStack

### Useful articles about JavaScript, Python, and Wordpress that help developers reduce time in development and increase…

betterfullstack.com](https://betterfullstack.com/stories/?source=post_page-----a20fb5040d0c---------------------------------------)

[## Coding Interview Questions | Skilled.dev

### A full platform where I teach you everything you need to land your next job and the techniques to…

skilled.dev](https://skilled.dev/?source=post_page-----a20fb5040d0c---------------------------------------)