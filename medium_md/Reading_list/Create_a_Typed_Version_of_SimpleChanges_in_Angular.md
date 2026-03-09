---
title: "Create a Typed Version of SimpleChanges in Angular"
url: https://medium.com/p/451f86593003
---

# Create a Typed Version of SimpleChanges in Angular

[Original](https://medium.com/p/451f86593003)

# Create a Typed Version of SimpleChanges in Angular

[![Netanel Basal](https://miro.medium.com/v2/resize:fill:64:64/1*abTZV6gAiJNINYPHQUeOBg.png)](/@netbasal?source=post_page---byline--451f86593003---------------------------------------)

[Netanel Basal](/@netbasal?source=post_page---byline--451f86593003---------------------------------------)

3 min read

·

Dec 15, 2020

--

5

Listen

Share

More

Press enter or click to view image in full size

![]()

Angular calls the `ngOnChanges` method of a component or directive whenever it detects changes to the ***input properties***. The method receives a [SimpleChanges](https://angular.io/api/core/SimpleChanges) object of current and previous property values.

Unfortunately, the `SimpleChanges` interface isn’t fully typed out of the box; but no worries — in this article, we’ll see how we can build a typed version of it.

First, let’s create a component so that we’ll have something to work with:

Our first goal is to create a utility type that receives an `object` type, and returns all its properties which have a value that isn’t a `function`. Let’s break the task into two steps:

First, we need to *mark* all the functions by setting their value to the `never` type:

We loop over the component type’s keys. If the type of the value extends the `Function` type, we change it to `never`. Otherwise, we set it to be the key name.

Using the code above will give us the following result:

Press enter or click to view image in full size

![]()

Now we can move on to the next step, which is to extract the keys with value type that isn’t `Function`, using the resulting `MarkFunctionProperties` type:

We leverage the `keyof` operator to create a new type, which yields the type of permitted property names for `T`. The `keyof` operator will NOT return keys whose value type is `never`:

Press enter or click to view image in full size

![]()

Now that we have all the non-function holding keys, we can use the `Pick` utility to extract these properties from our component, since these are the ones we need for our interface:

Press enter or click to view image in full size

![]()

The last step is to create our desired interface, which will loop over the keys and return a typed version of `SimpleChanges`:

![]()

The only drawback is that we’ll also get autocompletion for other public properties in our component, but it’s better than nothing 😃

You can play with the code [here](https://ng-run.com/edit/79gNo9P0GehdqGPG7aJO).

## 🚀 **In Case You Missed It**

Here are a few of my open source projects:

* [**Akita**](https://github.com/datorama/akita): State Management Tailored-Made for JS Applications
* [**Spectator**](https://github.com/ngneat/spectator): A Powerful Tool to Simplify Your Angular Tests
* [**Transloco**](https://github.com/ngneat/transloco/)**:** The Internationalization library Angular
* error-tailer — Seamless form errors for Angular applications
* [**Forms Manager**](https://github.com/ngneat/forms-manager): The Foundation for Proper Form Management in Angular
* [**Cashew**](https://github.com/ngneat/cashew): A flexible and straightforward library that caches HTTP requests
* [**Error Tailor**](https://github.com/ngneat/error-tailor) — Seamless form errors for Angular applications

And [many](https://github.com/ngneat) more!

*Follow me on* [*Medium*](/@NetanelBasal/) *or* [*Twitter*](https://twitter.com/NetanelBasal) *to read more about Angular, Akita and JS!*