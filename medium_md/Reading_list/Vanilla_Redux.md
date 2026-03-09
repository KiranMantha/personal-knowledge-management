---
title: "Vanilla Redux"
url: https://medium.com/p/e844628da6ff
---

# Vanilla Redux

[Original](https://medium.com/p/e844628da6ff)

# Vanilla Redux

[![Omer Goldberg](https://miro.medium.com/v2/resize:fill:64:64/1*LapJlOkgdM_Jn1aAKTo0HA.jpeg)](/@omergoldberg?source=post_page---byline--e844628da6ff---------------------------------------)

[Omer Goldberg](/@omergoldberg?source=post_page---byline--e844628da6ff---------------------------------------)

4 min read

·

May 8, 2017

--

4

Listen

Share

More

When teaching React and Redux, I find differentiating where one library’s functionality begins and the other ends is a source of confusion for students. The purpose of this post is to clarify Redux’s purpose, by implementing a simple counter application with Redux only and summarizing key parts of the core documentation. This is what we’ll be building:

![]()

Let’s start with giving a little background on **why we would use Redux**.

As the requirements for JavaScript single-page applications have become increasingly complicated, our code must manage more state than ever before. “State” can include a bunch of things such as (thanks Dan Abramov!)

> Server response
>
> Active routes, selected tabs
>
> Cached data

With the rise of ReactJS and the resurgence of functional programming paradigms, Redux has become an extremely popular choice for application state management.

The main reason for its rise in popularity is its strength when paired with React. Using both these libraries in an app, React will take care of rendering data / markup to the DOM, while Redux will act as “a predictable state container”. Don’t be scared by this term!

![]()

“Predictable state term” is just a fancy way of saying that Redux will help us manage our applications state by acting in a predictable manner when certain actions are triggered within our app. Before jumping into some code, let’s discuss Redux’s 3 principles.

## 3 Principles of Redux

1. **The entire state of the application will be represented by one JavaScript object. This is also referred to as the Javascript State Tree.**

![]()

2. **State tree is read only.** This means we will never directly manipulate values of our state tree. State will be updated / changed by dispatched actions (we’ll discuss this soon).

![]()

3. **The reducer function.** Inside a redux app there is one particular function that takes the previous state and the action being dispatched, and returns the next state of the application.

Let’s look at this flow visually:

![]()

Okay principles are a good thing to have, but how does this actually work?

Redux provides us with a createStore method. The store binds the 3 principles of redux with the following methods:

```
const store = createStore(<YOUR REDUCER FUNCTION HERE>)  
/*The reducer function should handle all possible actions and initialize the app state*/store.getState() /* Returns current application state */store.dispatch(<JS object>)  
/* Dispatch action to change app state. An action is a plain JS object that must have a 'type' key */store.subscribe(<CALLBACK FUNCTION>)   
/* Will be called after every store.dispatch(), so that we can update our app UI */
```

Now that we are familiar with the core Redux methods we can start building our app

![]()

Let’s check out the basic markup, set up with some event listeners for when we click on buttons:

## Application Architecture

Perfect, got the markup, now let’s reduxify (coined it first!) our app.

First question that pops into mind … What state will our app have? Well, it’s simply a counter, so the only thing we want to keep track of is the current value of the counter.

How can our application state change / be updated? Well, if the user clicks on a “+” button, we should increment the counter held in the app state, and if he clicks on the “-” button we should decrement accordingly.

Our reducer function is responsible for initializing the state, and updating based on dispatched actions. Let’s write it out.

```
function counter(state = 0, action) {  
 switch (action.type) {  
   case ‘INCREMENT’:  
     return state + 1  
   case ‘DECREMENT’:  
     return state — 1  
    default:  
     return state  
  }  
}
```

How should our UI be updated when an action is dispatched? The only thing that is updated is the text value of the div with the ‘value’ id. So our callback function to the store.subscribe method should look like:

```
function render() {  
 valueEl.innerHTML = store.getState().toString()  
}
```

All together this should look like:

In conclusion, Redux is a great library that helps us organize state and flow, by dispatching actions that reflect changes in our application. It can be used as a standalone library like in our example above, or in conjunction with libraries and frameworks such as React, Angular and more.

If you found this valuable feel free to follow me / reach out on Medium, [Github](https://github.com/Arieg419), [Linkedin](https://www.linkedin.com/in/omer-goldberg-680b40100/) or at arieg419@gmail.com ❤