---
title: "ES6 Destructuring: The Complete Guide"
url: https://medium.com/p/7f842d08b98f
---

# ES6 Destructuring: The Complete Guide

[Original](https://medium.com/p/7f842d08b98f)

# ES6 Destructuring: The Complete Guide

[![Glad Chinda](https://miro.medium.com/v2/resize:fill:64:64/1*K5myVh5FXG5SWb-VzPcgJA.png)](https://medium.com/@gladchinda?source=post_page---byline--7f842d08b98f---------------------------------------)

[Glad Chinda](https://medium.com/@gladchinda?source=post_page---byline--7f842d08b98f---------------------------------------)

9 min read

·

Apr 18, 2018

--

16

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D7f842d08b98f&operation=register&redirect=https%3A%2F%2Fcodeburst.io%2Fes6-destructuring-the-complete-guide-7f842d08b98f&source=---header_actions--7f842d08b98f---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

JavaScript is currently one of the most used programming languages in the world, being used across different platforms ranging from web browsers, mobile devices, VR, web servers, etc. Although the language has not changed a lot through the years when compared to other programming languages, there are some recent changes that are worth taking note of, because of the expressive power they add to the language — some of which are: *template literals*, *destructuring*, *spread operator*, *arrow functions*, *classes*, etc.

In this tutorial, our major focus will be on learning how to **harness the power of destructuring** to simplify our JavaScript programs. Before we dive into the ***what*** and ***how*** of destructuring I think the ***why*** should be considered. If you already use TypeScript or a modern JavaScript framework like React, Vue, Preact, Angular, etc, you may already be familiar with destructuring. However, there is a possibility that by going through this tutorial, you may learn a few new stuffs about destructuring you may not have known.

For this tutorial, it is assumed you already have some prior experience writing JavaScript code. There is a chance that some of the code snippets may not work on your browser depending on the version of the browser, since all the ES6 and ES7 features are not yet fully supported in all browsers. You may opt to test the code snippets on [**Codepen**](https://codepen.io/) or your favorite online JavaScript live editor. Another alternative would be using the [**Babel transpiler**](https://babeljs.io/) to get it to work on your browser.

## Why Destructuring?

To explain the why of destructuring, we will consider a scenario which most of us might be familiar with or might have come across at one time or the other when coding in JavaScript. Imagine we have the data of a student including scores in three subjects(*Maths*, *Elementary Science*, *English*) represented in an object and we need to display some information based on this data. We could end up with something that looks like this:

With the above code snippet, we would achieve the desired result. However, there are a few caveats to writing code this way. One of which is — you can easily make a *typo* and instead of writing `scores.english` for example, you write `score.english` which will result in an error. Again, if the `scores` object we are accessing is deeply nested in another object, the object access chain becomes longer which could mean more typing. These may not seem to be much an issue, but with destructuring we can do the same in a more expressive and compact syntax.

## What is Destructuring?

**Destructuring simply implies breaking down a complex structure into simpler parts.** In JavaScript, this complex structure is usually an object or an array. With the destructuring syntax, you can extract smaller fragments from arrays and objects. Destructuring syntax can be used for ***variable declaration*** or ***variable assignment***. You can also handle nested structures by using nested destructuring syntax.

Using destructuring, the function from our previous snippet will look like this:

There is a chance that the code in the last snippet didn’t go down well with you. If that’s the case, then follow up with the tutorial till you get to the end — I assure you it will all make sense. Let’s continue to learn how we can harness the power of destructuring.

## Object Destructuring

What we saw in that last snippet is a form of ***object destructuring*** being used as an assignment to a function. Let’s explore what we can do with object destructuring starting from the ground up. Basically, **you use an object literal on the left-hand-side of an assignment expression** for object destructuring. Here is a basic snippet:

Here we used object destructuring syntax to assign values to three variables: `firstname`, `lastname` and `country` using the values from their corresponding keys on the `student` object. This is the most basic form of object destructuring.

**The same syntax can be used in variable assignment** as follows:

The above snippet shows how to use object destructuring to assign new values to local variables. Notice that we had to **use a pair of enclosing parentheses (**`()`**) in the assignment expression**. If omitted, the destructuring object literal will be taken to be a block statement, which will lead to an error because a block cannot appear at the left-hand-side of an assignment expression.

### Default Values

Trying to assign a variable corresponding to a key that does not exist on the destructured object will cause the value `undefined` to be assigned instead. You can pass ***default values*** that will be assigned to such variables instead of `undefined`. Here is a simple example.

Here we assigned a default value of `25` to the `age` variable. Since the `age` key does not exist on the `person` object, `25` is assigned to the `age` variable instead of `undefined`.

### Using Different Variable Names

So far, we have been assigning to variables that have the same name as the corresponding object key. You can assign to a different variable name using this syntax: `[object_key]:[variable_name]`. You can also pass default values using the syntax: `[object_key]:[variable_name] = [default_value]`. Here is a simple example.

Here we created three local variables namely: `fullname`, `place` and `years` that map to the `name`, `country` and `age` keys respectively of the `person` object. Notice that we specified a default value of `25` for the `years` variable in case the `age` key is missing on the `person` object.

### Nested Object Destructuring

Referring back to our initial destructuring example, we recall that the `scores` object is nested in the `student` object. Let’s say we want to assign the *Maths* and *Science* scores to local variables. The following code snippet shows how we can use nested object destructuring to do this.

Here, we defined three local variables: `name`, `maths` and `science`. Also, we specified a default value of `50` for `science` in case it does not exist in the nested `scores` object. Notice that, `scores` is not defined as a variable. Instead, we use nested destructuring to extract the `maths` and `science` values from the nested`scores` object.

**When using nested object destructuring, be careful to avoid using an empty nested object literal.** Though it is valid syntax, it actually does no assignment. For example, the following destructuring does absolutely no assignment.

## Array Destructuring

By now you are already feeling like a destructuring ninja, having gone through the rigours of understanding object destructuring. The good news is that array destructuring is very much similar and straight forward so let’s dive in right away.

In array destructuring, **you use an array literal on the left-hand-side of an assignment expression**. Each variable name on the array literal maps to the corresponding item at the same index on the destructured array. Here is a quick example.

In this example, we have assigned the items in the `rgb` array to three local variables: `red`, `green` and `blue` using array destructuring. Notice that each variable is mapped to the corresponding item at the same index on the `rgb` array.

### Default Values

If the number of items in the array is more than the number of local variables passed to the destructuring array literal, then the excess items are not mapped. But if the number of local variables passed to the destructuring array literal exceed the number of items in the array, then each excess local variable will be assigned a value of `undefined` except you specify a ***default value***.

Just as with object destructuring, you can set default values for local variables using array destructuring. In the following example, we would set default values for some variables in case a corresponding item is not found.

You can also do an **array destructuring assignment**. Unlike with object destructuring, **you don’t need to enclose the assignment expression in parentheses**. Here is an example.

### Skipping Items

It is possible to skip some items you don’t want to assign to local variables and only assign the ones you are interested in. Here is an example of how we can assign only the blue value to a local variable.

We used *comma separation*(`,`) to omit the first two items of the `rgb` array, since we only needed the third item.

### Swapping Variables

One very nice application of array destructuring is in ***swapping local variables***. Imagine you are building a photo manipulation app and you want to be able to swap the `height` and `width` dimensions of a photo when the orientation of the photo is switched between `landscape` and `portrait`. The old-fashioned way of doing this will look like the following.

The above code snippet performs the task, although we had to use an additional variable to copy the value of one of the swapped variables. With array destructuring, we can perform the swap with a single assignment statement. The following snippet shows how array destructuring can be used to achieve this.

### Nested Array Destructuring

Just as with objects, you can also do nested destructuring with arrays. The corresponding item must be an array in order to use a nested destructuring array literal to assign items in it to local variables. Here is a quick example to illustrate this.

In the code above, we assigned `hex` variable and used nested array destructuring to assign to the `red`, `green` and `blue` variables.

### Rest Items

Sometimes you may want to assign some items to variables, while ensuring that the remaining items are ***captured***(assigned to another local variable). The new **rest parameter** syntax(`...param`) added in ES6 can be used with destructuring to achieve this. Here is a quick example.

Here you can see that after we assigned the first and third items of the `rainbow` array to `red` and `yellow` respectively, we used the *rest parameters* syntax(`...param`) to capture and assign the remaining values to the `otherColors` variable. This is referred to as the ***rest items*** variable. **Note however that the rest parameter, if used, must always appear as the last item** in the destructuring array literal otherwise an error will be thrown.

There are some **nice applications of rest items** that are worth considering. One of which is cloning arrays.

### Cloning Arrays

In JavaScript, **arrays are reference types and hence they are assigned by reference instead of being copied**. So in the following snippet, both the `rainbow` and the `rainbowClone` variables point to the same array reference in memory and hence any change made to `rainbow` is also applied to `rainbowClone` and vice-versa.

The following code snippet shows how we can clone an array in the **old-fashioned(ES5)** way — `Array.prototype.slice` and `Array.prototype.concat` to the rescue.

Here is how you can use **array destructuring** and the **rest parameter syntax** to create an array clone.

## Mixed Destructuring

There are cases when you are working with a pretty complex object/array structure and you need to assign some values from it to local variables. A good example would be an object with several deeply nested objects and arrays. In cases like this, you can use a combination of object destructuring and array destructuring to target certain parts of the complex structure as required. The following code shows a simple example.

## Destructured Function Parameters

Destructuring can also be applied on function parameters to extract values and assign them to local variables. Note however that the **destructured parameter cannot be omitted (it is required)** otherwise it throws an error. A good use case is the `displaySummary()` function from our initial example that expects a `student` object as parameter. We can destructure the `student` object and assign the extracted values to local variables of the function. Here is the example again:

Here we extracted the values we need from the `student` object parameter and assigned them to local variables: `name`, `maths`, `english` and `science`. Notice that although we have specified default values for some of the variables, if you call the function with no arguments you will get an error because **destructured parameters are always required**. You can assign a fallback object literal as default value for the `student` object and the nested `scores` object in case they are not supplied to avoid the error as shown in the following snippet.

## Conclusion

In this tutorial, we have explored the ES6 destructuring syntax and various ways we can utilize it in our code. If you are already pretty familiar with JavaScript destructuring, you may have learnt a few new stuffs as well. Although we used the rest parameter syntax at several points, it is worth noting that there is still more you can achieve with rest parameters. You can check [**Spread Syntax**](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) and [**Rest Parameters**](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/rest_parameters) for more details.

[![]()](http://bit.ly/codeburst)

> ✉️ *Subscribe to* CodeBurst’s *once-weekly* [***Email Blast***](http://bit.ly/codeburst-email)***,*** 🐦 *Follow* CodeBurst *on* [***Twitter***](http://bit.ly/codeburst-twitter)*, view* 🗺️ [***The 2018 Web Developer Roadmap***](http://bit.ly/2018-web-dev-roadmap)*, and* 🕸️ [***Learn Full Stack Web Development***](http://bit.ly/learn-web-dev-codeburst)*.*