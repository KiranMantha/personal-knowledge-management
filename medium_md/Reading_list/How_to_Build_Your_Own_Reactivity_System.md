---
title: "How to Build Your Own Reactivity System"
url: https://medium.com/p/fc48863a1b7c
---

# How to Build Your Own Reactivity System

[Original](https://medium.com/p/fc48863a1b7c)

# How to Build Your Own Reactivity System

[![Matthew Dangerfield](https://miro.medium.com/v2/resize:fill:64:64/1*svZdjbDAswFDrlWCa2UULg.jpeg)](/@supermdguy?source=post_page---byline--fc48863a1b7c---------------------------------------)

[Matthew Dangerfield](/@supermdguy?source=post_page---byline--fc48863a1b7c---------------------------------------)

8 min read

·

Nov 9, 2017

--

4

Listen

Share

More

Press enter or click to view image in full size

![]()

*Want to learn about Vuex? Check out my* [*hands on course*](https://bit.ly/31v8NPq)*! . Message me to be an early reviewer and get it for free.*

A couple of months ago, I attended an in-person meetup at 

[Frontend Masters](/u/1b199ed2dfd?source=post_page---user_mention--fc48863a1b7c---------------------------------------)

 called *Vue.js Advanced Features from the Ground Up*. It was really awesome because we got to learn about 

[Vue.js](/u/9b930cf6db26?source=post_page---user_mention--fc48863a1b7c---------------------------------------)

 from its creator, 

[Evan You](/u/4f198f5f1f12?source=post_page---user_mention--fc48863a1b7c---------------------------------------)

. Instead of just teaching us how to use Vue, he showed us how to actually implement a few parts of it. Reactivity was the part that interested me the most, so, after the class, I dug into [Vue’s source code](https://github.com/vuejs/vue) to learn more about exactly how its reactivity system works. In this guide, I’ll explain how Vue’s reactivity system is implemented, and show how you to make your own working reactivity system.

## The Problem of Reactivity

What is reactivity? I really like how Evan explained it in his talk, so I’ll use his examples. Say you have a variable `a`**.**

```
let a = 3
```

Now, let’s say you have another variable `b`, such that `b = a * 3` .

```
let b = a * 3  
console.log(b) // 9
```

That’s working just fine. But what happens if you need to change `a`?

```
a = 5  
console.log(b) // 9
```

Even though `a` changed, `b`stayed the same. Why? Because you never changed `b`. If you want to make sure `b`is still `a * 3`, you’d have to do it like this:

```
a = 5  
b = a * 3  
console.log(b) // 15
```

Now, this is working, but it would be annoying to have to type out `b = a * 3` every time `a` changes. We could solve this problem by wrapping the update to `b` in a function

```
let b;  
function onUpdate() {  
  b = a * 3  
}let a = 3  
onUpdate()  
console.log(b) // 9a = 5  
onUpdate()  
console.log(b) // 15
```

But, this still isn’t a very nice way of doing things. While it’s not too problematic in this example, imagine if we had 10 different variables, that all had a potentially complex relation to another variable or variables. We’d need a separate `onUpdate()`method for each variable. Instead of this awkward and imperative API, it’d be nice to have a simpler, more declarative API that just does what we want it to do. Evan compared it to a spreadsheet, where we can update one cell and know that any cell that depends on the one we updated will automatically update itself.

![]()

## Solutions

The good thing is that people have already come up with a number of solutions to this reactivity problem. In fact, each of the three major web development frameworks provides a solution to reactivity:

1. **React’s State Management**: Create a function `setState()`, and use that whenever we need to update `a`. Then, inside `setState()`, call a render function that updates the view to display the proper value of `b`.
2. **Angular’s Dirty Checking**: Create a function `detectChanges()`, that runs through every property it’s tracking and checks if it’s changed since the last time it was checked. If it finds an updated property (e.g. `a`), then it updates every property that uses the updated property (e.g. `b`). Then, run the `detectChanges()`function every few milliseconds and whenever it’s logical.
3. **Vue’s reactivity system**: Add ES5 getters and setters to each tracked property. Whenever a tracked property is accessed, mark the function that accessed the property as a “subscriber”. Whenever the property is changed, notify each subscriber of the change.

We’re going to implement Vue’s reactivity system in pure JavaScript. Before we get into the code, let’s go into some more details about exactly what we’re building.

## What We’re Building

Press enter or click to view image in full size

![]()

We’re going to create a class, called ***Watcher***, that takes in two properties: a **value getter** and a **callback**. The value getter can be any function that has a return value. Example:

```
let a = 3  
const getter = () => a * 3
```

The getter will probably have **dependencies**, or variables it depends on to get its value. In the example above, `a` is the only dependency of the getter function. Getter functions can have multiple dependencies, though. For example, `() => x * y` has both `x`and `y`as dependencies.

Whenever a dependency of the getter function changes, we’ll automatically run the callback function, passing in the current value and the previous value. This callback can do anything, from just logging the value to displaying the value in a div.

Finally, we’ll create a `defineReactive()`function, that adds change detection to a property on an object. We’ll also create a `walk()` function that adds change detection to all properties on an object. This will allow properties of the object to be used as dependencies. We will implement this change detection the same way Vue does: by defining ES5 [getters and setters](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/get). While this approach does have some limitations (described in the [docs](https://vuejs.org/v2/guide/reactivity.html)), it’s an extremely efficient and simple way of getting reactivity, since the JavaScript engine is ultimately providing the change detection.

> **Footnote:** The unreleased [Vue 3 will use ES6 Proxies](https://blog.cloudboost.io/reactivity-in-vue-js-2-vs-vue-js-3-dcdd0728dcdf) instead of getters and setters, but I believe the rest of Vue’s reactivity system won’t change that much.

When we’re finished, we’ll have a general-purpose reactivity API. Here’s an example of its usage:

## Deps

The first step is to implement the ***Dep*** class. ***Dep,*** short for dependency, is a wrapper around a value. Our implementation will be directly based on [Vue’s ***Dep*** class](https://github.com/vuejs/vue/blob/dev/src/core/observer/dep.js). Each ***Dep*** instance maintains a list of subscribers, or `subs`, that all want to know whenever the dep’s value changes. These subscribers are instances of the ***Watcher*** class, which we will implement in the next section. Each ***Dep*** instance is responsible for calling each subscriber’s `update()`method whenever the dep’s value changes.

Even though ***Dep*** instances are responsible for alerting subscribers of changes to a value, each ***Dep*** instance doesn’t actually know what value it’s watching. So, it each ***Dep*** instance has a `notify()`method, which lets it know when its value changes. We’ll talk more about who calls `notify()` later, but for now just assume it gets called whenever the watched value changes. Here’s a working ***Dep*** implementation:

What is `Dep.target`, and when does it get a value? `Dep.target`is a ***Watcher*** instance that lets the ***Dep*** instance knowwho’s using its value*.* This is necessary because the ***Dep*** instance needs to register itself as a dependency of the target watcher. There are two functions, `pushTarget()`and `popTarget()`, that manage the current**Dep.target**. Here’s what these look like:

We’ll discuss these methods more in the next section.

## Watchers

According to the [source code](https://github.com/vuejs/vue/blob/be9ac624c81bb698ed75628fe0cbeaba4a2fc991/src/core/observer/watcher.js):

> A watcher parses an expression, collects dependencies, and fires callbacks when the expression value changes. This is used for both the $watch() api and directives.

The ***Watcher*** class takes in a **getter** **function** and a **callback function**, and stores an array of dependencies of the value computed by the getter function. It tracks the values of the dependencies, and runs the callback function whenever any of these dependencies change. Here’s an example:

```
let a = 5, b = 4const getter = () => a + b  
const callback = (val) => console.log(val)const watcher = new Watcher(getter, callback)a = 6 // 10 is logged to the console
```

In Vue’s code, the ***Watcher*** class has several methods, but, for our purposes, we just need to implement three of them:

1. `get()`*.* This method calls the getter function supplied in the constructor to figure out what the initial value is. Before it calls the getter, it sets itself as the current ***Dep*** target watcher, using the`pushTarget()`method. This makes it so all values used in the getter function will add the ***Watcher*** instance as a subscriber. This is important because the ***Watcher*** instance needs to be linked to its dependencies in some way so it can be notified whenever the value of one of its dependencies changes.
2. `addDep(dep)`*.*This method adds itself as a subscriber to the given dependency. This method is called by the *Dep#depend()* method, which we’ll discuss in more detail in the next section.
3. `update()`*.* This method calls the callback function supplied in the constructor with the old value and new value as arguments. It gets used when the *Dep#notify()* method calls `update` on each of its subscribers after its value changes.

Here’s the code for our ***Watcher*** class:

## `defineReactive()`

According to the [source code](https://github.com/vuejs/vue/blob/61187596b9af48f1cb7b1848ad3eccc02ac2509d/src/core/observer/index.js), `defineReactive()`“defines a reactive property on an Object”. This is done by adding getters and setters to a given property of a given object. Each property has a ***Dep*** instance associated with it. Whenever a reactive object’s property is accessed, the getter calls *Dep#depend(),* which adds the current target ***Watcher*** as a subscriber to the property’s ***Dep*** instance. Whenever the property is changed, the setter calls *Dep#notify()* which calls the *update()* method of each of the subscribers to the property’s ***Dep****.* Here’s *defineReactive()*, based on the source code:

## How it all works together

Now we’ve written each part of our reactivity system, but how does it all work? Each part of the system is so interconnected with all the other parts that it can be difficult to understand. Let’s walk step by step through what happens in an example usage of our ***Watcher*** class.

We’ll start by setting everything up:

```
const foods = { apple: 5 }// make foods reactive, register deps for each property  
walk(foods)// Instantiate the watcher, which takes a getter and a callback  
const foodsWatcher = new Watcher(() => foods.apple,  
                                 () => console.log('change')  
                                 )
```

First, the constructor for the ***Watcher*** class runs the following:

```
this.value = this.get()
```

Here’s *Watcher#get()*:

```
pushTarget(this) // Imported from dep.js  
const value = this.getter()  
popTarget() // Imported from dep.jsreturn value
```

First, it calls the `pushTarget()`function, which assigns `this`(the`foodsWatcher`) to `Dep.target`.Then, it calls `this.getter()`*,* the first function passed to the ***Watcher*** constructor. The getter for the `foodsWatcher`just returns the value of `foods.apple`. Since `foods.apple` was made reactive by `defineReactive()`*,* it will also run the reactive getter:

```
// adds Dep.target as a subscriber to the property's dep instance  
dep.depend()return value
```

This registers `foodsWatcher` as a subscriber to the ***Dep*** instance associated with `foods.apple` . So there’s now a connection between the `foodsWatcher` and `foods.apple`.

How is this helpful? Let’s say we change `foods.apple` .

```
foods.apple = 6
```

Doing this will call the setter on `foods.apple`. The setter runs `dep.notify()`, whichcalls `update()`on each of the dep’s subscribers. Since the `foodsWatcher` is a subscriber to the ***Dep*** instance, the `dep.notify()`call will trigger the update method on `foodsWatcher`. What does *Watcher#update()* do?

```
update() {  
  const value = this.get()  
  const oldValue = this.value  
  this.value = value  this.cb(value, oldValue)  
}
```

It updates its knowledge of the current value, and then calls the callback supplied in the constructor. Remember that the callback we specified was

```
() => console.log('change')
```

So, when we change `foods.apple`, our reactivity system will let us know! The cool thing is that this happened without any dirty checking every millisecond. It happened without us having to explicitly set the state. It just *worked*, without us having to think about it at all, just like a spreadsheet. That’s what makes Vue’s reactivity system so incredible.

If you want to see all the code for our reactivity system in one place, I made a [plunker](http://embed.plnkr.co/rMLS2Swq4mz0aXcxqDYA/) with a really cool demo. Thanks for reading!

## Resources

* The [Frontend Masters course](https://frontendmasters.com/live-event/vue-js-advanced-features-ground/) I went to (if you have a Frontend Masters subscription)
* Vue’s [docs on reactivity](https://vuejs.org/v2/guide/reactivity.html)
* A [talk Evan gave](https://www.dotconferences.com/2016/12/evan-you-reactivity-in-frontend-javascript-frameworks) in 2016 on reactivity
* Vue’s [source code](https://github.com/vuejs/vue/tree/dev/src/core/observer) (the ultimate reference)