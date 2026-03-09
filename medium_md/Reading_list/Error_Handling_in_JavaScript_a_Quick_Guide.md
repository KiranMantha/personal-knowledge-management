---
title: "Error Handling in JavaScript: a Quick Guide"
url: https://medium.com/p/54b954427e47
---

# Error Handling in JavaScript: a Quick Guide

[Original](https://medium.com/p/54b954427e47)

Member-only story

# Error Handling in JavaScript: a Quick Guide

## Is There a Right Way to Get Stuff Wrong?

[![Bret Cameron](https://miro.medium.com/v2/resize:fill:64:64/1*-FkK2sZyRsMrzogxihEZyA.jpeg)](/@bretcameron?source=post_page---byline--54b954427e47---------------------------------------)

[Bret Cameron](/@bretcameron?source=post_page---byline--54b954427e47---------------------------------------)

9 min read

·

Oct 10, 2019

--

4

Listen

Share

More

![]()

There is no such thing as perfect code. Even if there was, our users will always find surprising ways to break what once seemed like perfectly watertight code and attempt to do things that we don’t want them to! How do we control these perilous situations? Using errors!

In this article, we’ll look into error handling in JavaScript. We’re specifically talking about runtime errors — sometimes called execution errors. These are the errors that occur while our programming is running: if they’re not caught, then they’ll typically crash our programs, something we usually want to avoid! By the end of the article, you’ll have seen several different approaches to error handling in JavaScript, as well as several ways to extend JavaScript’s built-in `Error` to make it more useful.

But first, a thorny question…

## Should I use throw, return or console.error?

This is the question that inspired me to write this article. I wanted to know the best practices around when we should `throw` an error, when we should use `return` , and when `console.error` should come in.

Even if you’re new to JavaScript, you should have a decent understanding of `return` . You may not have encountered `console.error` or `console.exception`, but these are also easy to grasp: they’re essentially `console.log` — except, in eye-popping red!

But what about the `throw` statement? This is the keyword used to throw an exception, an event which disrupts the normal flow of our program’s instructions. And this is the key characteristic which distinguishes `throw` from `return`: after a function *throws* an exception, the runtime system will try to find a way to handle the exception. In other words, throw will look additional actions to take. By contrast, `return` will simply finish the execution of a function.

## Using throw without a try ... catch statement

On to our first example. What happens if we `throw` an error without a `try ... catch` statement? I’ll adapt a simple example [from MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/throw):

```
function getRectArea(width, height) {  
  if (isNaN(width) || isNaN(height)) {  
    throw new Error("Parameter is not a number!");  
  };  
  return width * height;  
};console.log(getRectArea('abc', 123));
```

If we run the code above, the funciton will output the same thing, regardless of whether we `throw` or `return` the error.

There is a difference, though. If there is no `catch` statement, `throw` will log to the console by default and it will prevent our program from continuing execution. If we use `return` , this won’t happen, and we have to specifically call `console.log` to see whatever our function has returned.

## Using throw with a try ... catch statement

Now, let’s add in a `try ... catch` statement. This statement will attempt to run our `getRectArea` function, but if that fails, it will perform the actions specified in the `catch` block:

```
function getRectArea(width, height) {  
  if (isNaN(width) || isNaN(height)) {  
    throw new Error("Parameter is not a number!");  
  };  
  return width * height;  
};try {  
  getRectArea('abc', 123);  
} catch (e) {  
  console.error(e);  
};
```

In this example, *only* `throw` will trigger the `catch` block. (We cannot replace is with `return` and get the same logic to execute). If there is no `catch` block, `throw` will stop the program and log the error to the console.

So, when should we use `throw` ? If an error is not expected in normal operation (that is to say, it occurs rarely), then that is the best time to reach for `throw` . It is almost always the easiest — and, sometimes, the fastest — way to catch rare exceptions, because the program will immediately execute the relevant `catch` statement.

## Common exceptions: a case when throw might not be unnecessary

So, when would we consider returning or logging an error instead of throwing it? For some errors, which are predictable and occur commonly, using `throw` could, in fact, often be significantly slower than the alternatives.

Later in the article, we’ll create a new error type called `RequiredInputError` . This will help other developers working on our project understand and locate the error, but — as this error could be quite common — we don’t want to unnecessarily slow our users’ experience by immediately reaching for `throw` .

### Solution 1

If our use-case was really that simple, we wouldn’t need to `return` the error either. We could just return, say, a boolean and log the error to the console. For example:

```
function isBlank(input) {  
  if (input) return false;  
  console.error(new Error('A required field is blank.'));  
  return true;  
}
```

### Solution 2

This works fine. But in a larger, more complex project, it may make sense to return the error and store the error-handling logic (including `console.error`) somewhere else. Here’s a basic example of what that might look like:

```
function isBlank(input) {  
  if (input) return false;  
  return new Error('A required field is blank.');  
};const input = "";if (isBlank(input) instanceof Error) {  
  console.error(isBlank(input));  
};
```

## Returning errors in promises

Another scenario in which it is better to choose `return` over `throw` is when using asynchronous code — namely, inside a `Promise` . If we try to `throw` an `Error` inside a `Promise`, there may be occasions where it is not caught correctly, depending on the structure of the code. That’s why promises have their own specific `catch` statement.

For Promises, it’s advised to use the `reject` and `resolve` methods (which return whatever’s inside the parentheses), and then to use `Promise.prototype.catch()` for any additional error handling.

Here’s a simple example of that in action — a function which asynchronously checks whether a user’s input is blank and, if it is, returns an `Error` :

```
async function isBlankAsync(input) {  
  return new Promise((resolve, reject) => {  
    if (!input) reject(new Error('A validation error'));  
    resolve(input);  
  });  
};isBlankAsync()  
  .catch(e => console.error(e));
```

## Understanding the Error object

In every example above, we used the `Error` object to store a particular error message. We didn’t have to do that: just as `return` can return any type of object, we could also `throw` a string, object or anything else!

But, as far as I can tell, there are two reasons to reach for the `Error` object, rather than just throwing (or returning) a string:

1. The `Error` object is the conventional way of describing errors, so this is what libraries, frameworks and other developers expect, and so it makes your code more readable and accessible.
2. The `Error` object contains additional information — primarily, the “error stack” — which is really useful when it comes to debugging. The error stack traces which functions were called, in what order, from which line and file, and with what arguments: everything you’re used to seeing below the main error message.

## Error properties and methods

Here’s a simple example of the generic `Error` object.

```
const err = new Error("Incorrect file type provided");
```

By default, our `Error` has two properties:

* a `name` — in this case, `"Error"`
* a `message` — in this case, `"Incorrect file type provided"`

On top of that, we have the `toString` method, which prints you the `name` and the `message` together. There are a handful of additional properties and methods, but these are mostly specific to Firefox, so they’re not recommended in production!

For the remainder of this article, we’ll look into three ways we can extend the basic `Error` object into something that’s more useful — at least, in specific situations.

## Creating a TypeError Class

So, what if we wanted to extend the `Error` object? JavaScript comes with several more specific error-types built-in. One of them is a `TypeError` , used when a value is not of the expected type. But let’s say we wanted to create our own `TypeError` with more functionality.

Let’s say we wanted a `TypeError` that, by default, told us which type a variable was supposed to be and which type it actually is. Our constructor should take a `value` and a `type` . Then, unless a message is provided, we’ll create a default message that makes any type differences clear. We’ll be using ES6+ classes, and all of the logic can go in the `constructor`:

```
class TypeError extends Error {  
  constructor(value, type, ...params) {  
    super(...params);  
      
    if (Error.captureStackTrace) {  
      Error.captureStackTrace(this, TypeError);  
    };this.name = 'TypeError';  
    this.typeRequired = type;  
    this.typeSupplied = typeof value;  
    this.value = value;if (!this.message && this.typeRequired !== this.typeSupplied) {  
      this.message = `The value ${this.value} has type "${this.typeSupplied}", but it should have type "${this.typeRequired}".`;  
    };  
  };  
};
```

First, we call `super(...params)` to pass the default arguments (like `message`) to the parent `Error` object.

Next, we check to see whether the `Error` object has a `captureStackTraceMethod` . If it does, we should call it, as that will provide our class with a `stack` property. (Generally, if `captureStackTraceMethod` , the stack is provided by default).

Finally, we create `name` , `typeRequired` and `typeSupplied` properties. If a `message` isn’t provided and the `typeSupplied` is not identical to the `typeRequired` , we send a default message. That’s it!

Paste in the code above and try calling `new TypeError("10", "number")` . In some environments, like Node.js, you’ll see the whole error object. To make sure you’re only seeing the stack, call `new TypeError("10", "number").stack` .

## Creating a RequiredInputError Class

Now, we’ll have a look at communicating our error to end-users. Obviously, they don’t want or need as much information as a developer does.

What if we wanted to log an error to the console *and* send a short error message to our end-users? There are lots of ways to achieve, but handling both in a custom `Error` objects is one way to keep things neat.

First, let’s create a new error class called `RequiredInputError` :

```
class RequiredInputError extends Error {  
  constructor(label, ...params) {  
    super(...params);if (Error.captureStackTrace) {  
      Error.captureStackTrace(this, RequiredInputError);  
    };this.name = 'UserInputError';  
    this.label = label;this.userMessage = `The field "${label}" is required.`;if (!this.message) this.message = this.userMessage;  
  };  
};
```

Our new class is similar to our `TypeError` class above, but we’ve added a new property called `userMessage` , which we can then display in the DOM.

The exact way you go about this will depend on the framework you’re using, so here’s just one example. Let’s say we had a variable called `userInput` and we were using React. We could create an error object, send the error’s `userMessage` to our end-user using state, and — only if we’re in a development environment — log the error stack to the console. Let’s create a function that does exactly that:

```
const isBlank = (userInput, fieldName) => {  
  if (!userInput) {  
    const error = new RequiredInputError(fieldName);  
    this.setState({ error: error.userMessage });  
    if (process.env.NODE_ENV !== 'production')   
      console.error(error.stack);  
    return true;  
  };  
  return false;  
};
```

Now, can simply call `isBlank` on a variable:

```
isBlank(userInput, "email");
```

If the input *is* blank, the user will see a message that the variable is required. In addition, any developers working on the project will see all the information they need to know about where the error is occurring and why!

This may seem like overkill for just one input, but if your website has a lot of forms, it could be useful to identify missing fields with a unique class of error.

## Adding a toJSON method

Finally, we’ll create a third class, to demonstrate one last use-case: what if we wanted to serialise the various parts of our string as a regular object? This could be useful if, for example, we want to send errors between the client and our server.

This is fairly simple to achieve — we just need to expose the various properties in a new method:

```
class CustomError extends Error {  
  constructor(...params) {  
    super(...params);  
      
    if (Error.captureStackTrace) {  
      Error.captureStackTrace(this, CustomError);  
    };    this.name = 'ValidationError';    this.date = new Date();  
  }  toJSON() {  
    return {  
      name: this.name,  
      date: this.date,  
      message: this.message,  
      stack: this.stack  
    }  
  }  
}
```

There are a lot of similarities to the previous two examples. This time, we’ve added a custom `date` property, and in our `toJSON` method, we’re returning all the properties in their own object. This makes it easy to send and receive all the data available with each error. It could also be used to preserve the call trace if you want to rethrow an error.

## Conclusion

Handling errors is an inevitable reality of any programming, so I hope this article has given you some new ideas about how to handle errors in your next JavaScript project. We’ve clarified the distinction between `throw` , `return` and `console.error` and we’ve looked at various ways to extend the built-in `Error` object.

If you’d like to find out more about any of the topics discussed in the article, I would head over to MDN, which has a lot of useful examples. Here are some suggestions to get you started:

* [throw](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/throw)
* [try…catch](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch)
* [console.error()](https://developer.mozilla.org/en-US/docs/Web/API/Console/error)
* [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)
* [Promise.prototype.catch()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/catch)
* [Error](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)
* [Error.prototype](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error/prototype)

If you have any questions or feedback, feel free to leave a comment!