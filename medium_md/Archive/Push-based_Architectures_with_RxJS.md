---
title: "Push-based Architectures with RxJS"
url: https://medium.com/p/81b327d7c32d
---

# Push-based Architectures with RxJS

[Original](https://medium.com/p/81b327d7c32d)

Member-only story

# Push-based Architectures with RxJS

[![Thomas Burleson](https://miro.medium.com/v2/resize:fill:64:64/1*M5Wlvf-rguXBUbWpOtXY1A.png)](/?source=post_page---byline--81b327d7c32d---------------------------------------)

[Thomas Burleson](/?source=post_page---byline--81b327d7c32d---------------------------------------)

9 min read

·

May 24, 2019

--

18

Listen

Share

More

… all this time you have been coding **wrong!**

Press enter or click to view image in full size

![]()

Before I can show you **HOW** to implement *Push-Based* architectures, I need to first describe **WHY** *Pull-Based* solutions are flawed… and **WHY** *Push-Based*systems are better.

Most developers learn to program, code, and build software architectures using traditional ***Pull-based*** approaches. In the world of web applications and asynchronous, rich user experiences this approach is flawed, rampant with myriad problems, and is fundamentally **wrong**.

## Traditional Pull-Based Solutions

With **Pull-based** architecture, the views will explicitly call service methods to force-reload (aka ‘pull’) the data. This is the traditional approach employed by most developers.

Press enter or click to view image in full size

![]()

Consider the simple function call `findAllUsers()` used to retrieve a list of users… here the code is pulling data to a view. If the user list subsequently changes, views (or services) must issue another pull request with `findAllUsers()`. But how do the views know when to issue another request?

> Notice I have not stated whether the data is currently in-memory or must be retrieved from the server. Nor have I asserted that the pull request is **synchronous** or **asynchronous**. Those are irrelevant here since this is still a **pull-based** approach.

Press enter or click to view image in full size

![]()

Now it is reasonable to load data or change data asynchronously… using async/await or Promises. Developers may even build a temporary 1-response Observable [*like HttpClient*] to access remote data.

But those data request are still a single, **1-x** **pull-request**. And Observables used this way are consider temporary streams; discarded after use/completion.

To design our system for long-term data flows, we could provide notification callbacks or even using polling (*AngularJS digest cycle*). These quickly become messy and [in some cases] even present performance issues.

And if our data is shared between multiple views then other HUGE architectural concerns must be considered:

* “How do 1…n views know when the data is updated?”
* “How do unrelated views get notified that new data is available?”
* “Should uncoupled view components poll for updated data?”
* “Why is my shared data changing? Who is changing the data when?”

## **Push-Based Architectures**

So how do we invert the paradigm and change our coding to use **Push-based** solutions and architectures?

Press enter or click to view image in full size

![]()

With RxJS and long-lived Observable streams, developers can implement architectures that **PUSH** data changes to all subscribers.

Views simply subscribe to desired data streams. When the datasource changes that desired data will be auto-pushed through the specified stream [*to 1…n subscribing, interested view components*].

> This approach to using permanent streams to push-data is a fundamental, HUGE paradigm shift from traditional pull-based architectures.

## Benefits

What are the benefits of designing and using **Push-based** architectures?

* State Management
* Immutability
* Performance
* Reactive Views

## State Management

With **Push-based** services, direct data access is prohibited. The *true* source of data is maintained within a virtual vault. The service itself provides an **API** that is intended to be used by the **view layer**.

Each Push-based service API has:

* ***Properties***: streams that will deliver data **whenever** that data changes.
* ***Methods***: to request changes to the data or request specific custom streams

The actual raw data is only available **after** it has been pushed through the stream(s).

This protected isolation centralizes all change management and business logic within the service itself and forces view components to simply react passively to incoming pushed-data.

## Immutability

With **Push-based** services, data (*aka state*) is always **immutable**. This effectively means that the data is read-only. Changes to the *inside properties* are not allowed.

Below is an example of *pagination* state and how developers would *update* an immutable object:

> When an immutable object needs to be modified then that object is cloned to a new instance with the desired properties/fields updated. After construction this object is also considered **immutable.**

With immutable, data change-detection using **deep comparisons** is not needed!

To detect changes, comparisons simply use `===` to determine if the data reference is a new instance. And when changes are detected, then the changed data is re-delivered through the streams to any subscribers.

*Immutability == fast change-detection == fast performance.*

## **Reactive Views**

With **Push-based** services that deliver data only through streams, developers are encouraged to create applications composed of *passive* view components. But what are ***passive*** views?

* Views that only render when the data arrives via a push-stream.
* Views that delegate user interactions to a non-view layer
* Views that require no business-logic testing
* Views that require minimal isolated UX testing

With **Push-based** services, Angular view components that are highly performant use both `ChangeDetectionStrategy.OnPush` and the `async` pipe with data delivered via streams.

> There are advanced patterns such as Redux or NgRx (etc) that provide all these features and more*.* We can, however, simply use RxJS and still build elegant, performant **push-based** solutions.

These concepts and issues impact developers in ALL technology platforms and frameworks and have huge impacts on developers of web applications. Whether the web app developer uses Angular, React, Vue.js, or another framework… Pull vs Push architectures affect everyone.

In the subsequent sections, let’s dive into **Angular** code to explore the concepts.

## Code Labs

In the following sections, let’s first build a simple **pull-based** service. Afterwards, we will then convert that same service into an elegant **push-based service**.

> Surprisingly, we will discover that our choice of Push-based or Pull-based architectures affects the UX. Push-based applications feel smoother and more intuitive. We will see this in the labs below…

Let’s use the online [**RandomUser**](https://randomuser.me/documentation#pagination) SaaS and build two (2) solutions: pull-based and push-based data architectures. We can then compare the implementations of **pull-based** vs **push-based** architectures.

## **A Search Application**

Consider an application UX where a view component displays search options and will render display a list of users found (based on the search options).

Press enter or click to view image in full size

![]()

As the user interacts with the view search options, the **search** and **pagesize** options will be used to re-query for new user data and — eventually — the view will re-render with the updated data.

## 1.1 Build a Pull-based UserFacade

Press enter or click to view image in full size

![]()

Since our service must provide state management, we first must define our state:

Our `UserFacade` is seemingly super easy to build

> … but actually has LOTs of potential problems that we will discuss later.

## 1.2 Streams in the UI

Our `UserFacade` publishes **output** streams that will be consumed/used by the UI. And our application also uses a *FormControl* stream `searchTerm$` to delegate search changes as **inputs** to the UserFacade.

Press enter or click to view image in full size

![]()

## 1.3 Pull-based Web App

Here is a full StackBlitz to explore the full source and the running application:

## 1.4 Impacts of Pull-Based Architecture

It is interesting to note that with Pull-Based architectures, it is easy to create horrible UX(es). When the user changes search criteria or pagesize, the `Load Users` button must be re-clicked.

> The application does not feel smooth nor smart! It feels blocky and modal. Uugh

**Danger**:

* **users**, **criteria**, and **pagination** are *writable and mutable*
* `criteria` and `pagination` can change without changes to `users`
* Data flows in all-directions is possible

**Caution**:

* `criteria` and `pagination` must be assigned before calls to `findAllUsers()`
* assignments to `criteria` and `pagination` should be validated
* `findAllUsers()` will return an observable AND assign to `users`

**Considerations**:

* If `criteria`, `pagination`, or `users` changes, **how are the views notified?**
* What about replay features so multiple calls to `findAllUsers()` can **share results?**

> And yes, there are work-arounds to the above issues. These, however, are intended to simply illustrate that Pull-Based architectures can easily lead to complex, subtle production problems.

Press enter or click to view image in full size

![]()

Let’s re-build our application using Push-Based architectures.

## 2.1 Data Flows: 1-Way

With Push-Based services our `UserFacade` can maintain and enforce 1-way data flows. External changes to state is **ONLY** allowed using API methods.

Press enter or click to view image in full size

![]()

> 1-way data flows ensure predictable data changes and data deliveries.

## 2.2 Designing APIs

With Push-based Facades developers should always design the API first; without initial concern for internal implementations. The goal is to design a minimal API that is useful for the view layers.

Press enter or click to view image in full size

![]()

> APIs are always stream-based and methods return either streams (*observables*) or `void.`

## 2.3 Define our API

After designing the API, implementing a definition is easy:

Press enter or click to view image in full size

![]()

> Notice ^ we still do not know HOW this will be **implemented**. That is the beauty of the API: it affords us the freedom to implement the internals **without** constraints.

## 2.4 Immutable State

Since the `UserFacade` will internal manage immutable state, let’s define those constructs and initialize values:

> These initialized values will also be used to populate UI controls with initial, startup values.

## 2.5 Internal Auto-Loads

Our `UserFacade` publishes streams for data deliver [to view components]. We can, however, use those same streams internally to auto-trigger calls to remote cloud services:

Press enter or click to view image in full size

![]()

> `combineWithLatest` is a powerful RxJS creation function that will use the outputs of 1..n *up-streams* to trigger *down-stream* logic.

## 2.6 Optimized Data-Delivery

Long-lived streams allow us to deliver data at any future time. And with careful stream construction, we can optimize the delivery through each stream to only emit data when that **specific** datasource has changed:

## 2.7 Aggregate Data-Delivery

We can also dramatically simplify view layer complexity and re-rendering by aggregating our streams into a single output stream.

Whenever any of the the individual streams (eg `pagination$` `users$`, etc) emit values, the `vm$` will re-emit an updated viewModel with current values.

> Credits to 
>
> [Sander Elias](https://medium.com/u/7e5276cf7946?source=post_page---user_mention--81b327d7c32d---------------------------------------)
>
>  and 
>
> [Deborah Kurata](https://medium.com/u/410e2ec02d13?source=post_page---user_mention--81b327d7c32d---------------------------------------)
>
>  for evangelizing this brilliant idea.

## 2.8 Push-based Web App

Here is the full source and live demo of our Push-based Angular web application:

## 2.9 Impacts of Push-Based Architecture

With Push-based architectures, our user experiences (UX) feels so smooth… as if it is smart and recognizes our intents.

Our view code is super clean, maintainable, and understandable.

Our `UserFacade` code has predictable data flows, central state management, and more…

**With our UX,**

* **Auto-search** for users for any criteria and pagination changes
* UI **auto-updates** for pagination or criteria changes
* UI Components are **passive**/reactive and re-render when `vm$` emits updated data.

**With our UI, we have**

* Full non-UI, business-layer **testing**
* e2e is simply for UI layouts and style regressions

## Next Steps

And with Push-based architectures, we can easily add NgRx later

Press enter or click to view image in full size

![]()

## PodCast

Check out my live **AngularAir** podcast with 

[Justin Schwartzenberger](https://medium.com/u/a9286c256648?source=post_page---user_mention--81b327d7c32d---------------------------------------)

, [**@**bonnster75](https://twitter.com/bonnster75), and 

[Mike Brocchi](https://medium.com/u/eae5913abcc1?source=post_page---user_mention--81b327d7c32d---------------------------------------)

. And thanks to 

[Elad Bezalel](https://medium.com/u/9ff7e3ae0ffd?source=post_page---user_mention--81b327d7c32d---------------------------------------)

 for wonderful UI design help on the demo applications.