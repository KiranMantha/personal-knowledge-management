---
title: "Manage Action Flow in @ngrx with @ngrx/effects"
url: https://medium.com/p/1fda3fa06c2f
---

# Manage Action Flow in @ngrx with @ngrx/effects

[Original](https://medium.com/p/1fda3fa06c2f)

# Manage Action Flow in @ngrx with @ngrx/effects

[![Anonymous](https://miro.medium.com/v2/resize:fill:64:64/1*mQc4HKPJno__5LkmgFIjLg.png)](/@tui2tone?source=post_page---byline--1fda3fa06c2f---------------------------------------)

[Anonymous](/@tui2tone?source=post_page---byline--1fda3fa06c2f---------------------------------------)

4 min read

·

Aug 20, 2017

--

5

Listen

Share

More

@ngrx is a state management for your Angular application. It like a Redux. You can find a more detail from [State Management in Angular with @ngrx](https://blog.nextzy.me/state-management-in-angular-with-ngrx-da57e59c7c89). In that article, we show you how to manage a state in the application with @ngrx/store, but the most application is more complex than changing a state by trigger only one action and finish an action flow, some “**Action**” have a flow to trigger other action later. For example, when you request an HTTP request to call an API, you should have a 3 state in the application called “Loading”, “Success” and “Failed”. After you have trigger loading action, then wait for http response and then trigger success or failed action later. You can manage this flow with **@ngrx/effects**.

Press enter or click to view image in full size

![]()

In Redux, we use a middleware to manage Action flow. For example, we want to trigger some action when this action was called or http request flow, we call a middleware and the middleware will handle flow for us. But in **@ngrx,** there is no middleware pattern defined, @ngrx has provided a side effect of action by **subscribing** **an action**, and when this action was called, this function will be triggered too. There call this library a **@ngrx/effects**.

## @ngrx/effects

In @ngrx/store state management flow, when the action was triggered, a reducers process a data and put into “**Store**”. “View” will subscribe data from the store and get data to display in an application.

Press enter or click to view image in full size

![]()

**@ngrx/effects** is a side model of the store. **Effects** subscribe an action, when Action was triggered, an effect function will trigger too. You can do an async task from here, HTTP request, connect API to query data from the database and then trigger another Action to save a response into “**Store**”.

Press enter or click to view image in full size

![]()

When you get an HTTP response from HTTP request and need to update this data into a “**Store**”. The only way you can do that from the effect is triggered another “**Action**”. We cannot directly get into a reducers or store. So you need to define an action for this event. For example, when application initialized, we called an action to load a todo list call “**getTodo**” and update a state to loading variable. And then the effect was called, we make an HTTP request to get a todo list and after we get an HTTP response, we trigger an action called “**getTodoSuccess**” or “**getTodoFailed**” base on HTTP status code that we received. That action has to update a todo list into a “Store”.

Press enter or click to view image in full size

![]()

## Start Coding

We get to start from existing code in the previous article, you can view a source code from <https://github.com/tui2tone/ngrx-example>.

Install a @ngrx/effect via npm or yarn

```
npm install @ngrx/effects --save
```

First, we need to define an action of getting todo list flow from HTTP request in actions folders with 3 actions called “getTodo”, “getTodoSuccess” and “getTodoFailed”.

Then create reducers for process a data from those actions. Change “isLoading” to true in getTodo state and when trigger getTodoSuccess return a todo list data to “Store”.

In effects, we create an effect with subscribe getTodo action and delay for 2 seconds, then call a getTodoSuccess action and with todo list data.

In the real-world example, we will use HTTP request to get a todo list, here is a little example to do this thing with HttpClient from Angular.

A return Action from “mergeMap” is an array. So, you can return multiple actions that you want just like this.

Finally, initialize an EffectsModule in the Angular module.

![]()

## Get Data from Store in Effects

In effects, we can get a data from store to use in “mergeMap” function. For example, if your HTTP request requires a userId and we store it in “Store”, we can get this userId value and send it with HTTP request in effects module.

First, import a store’s state into an effect via the constructor, then use “**withLatestFrom**” operator to get a data in “Store”. Parameters in a mergeMap function will change into an array including 2 objects, assign them to a variable. The first object is a parameter from the payload and we assign to “payload” and a second one is from a store, we will assign to a “store” variable. After that, you can get a value in store via store variable like this.

You can view all source code from here. <https://github.com/tui2tone/ngrx-effect-example>

## **References**

* **@ngrx/effects** <https://github.com/ngrx/platform/blob/master/docs/effects/README.md>
* **NgRX Effect Example** <https://github.com/tui2tone/ngrx-effect-example>