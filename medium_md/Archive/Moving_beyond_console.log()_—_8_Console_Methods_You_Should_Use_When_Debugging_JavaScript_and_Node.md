---
title: "Moving beyond console.log() — 8 Console Methods You Should Use When Debugging JavaScript and Node"
url: https://medium.com/p/25f6ac840ada
---

# Moving beyond console.log() — 8 Console Methods You Should Use When Debugging JavaScript and Node

[Original](https://medium.com/p/25f6ac840ada)

Member-only story

# Moving beyond console.log() — 8 Console Methods You Should Use When Debugging JavaScript and Node

## Moving beyond console.log and learn the console functions you have never used for debugging!

[![Marco Antonio Ghiani](https://miro.medium.com/v2/resize:fill:64:64/1*2lpPxdlbU8N8uDolDFGXaw.jpeg)](https://medium.com/@tonyghiani?source=post_page---byline--25f6ac840ada---------------------------------------)

[Marco Antonio Ghiani](https://medium.com/@tonyghiani?source=post_page---byline--25f6ac840ada---------------------------------------)

7 min read

·

Sep 17, 2019

--

10

Listen

Share

More

Press enter or click to view image in full size

![]()

## The Console API

**Every** JavaScript developer has used `console.log(‘text’)`. The `console` module is one of the most common utilities in JavaScript, and the API implemented in Node:

> provides a simple debugging console that is similar to the JavaScript console mechanism provided by web browsers.

This is the definition written in the [Node.js documentation](https://nodejs.org/dist/latest-v12.x/docs/api/console.html) page for the Console module 😅. However, beginners are prone to consult online tutorials instead of reading the documentation while starting with new technologies, missing the chance to learn how to properly use this new tool to 100% of its potential.

When talking about the Console API, newbies usually use only some functions like 👌`console.log()`*, ⚠️* `console.warn()`*,* or ❌ `console.error()`to debug their application, while often there are many other methods which can perfectly implement our requirements and improve debugging efficiency.

This article is made to expose some of the most interesting `console` methods with related examples that I use while teaching at [***Codeworks***](https://codeworks.me/?utm_source=medium&utm_medium=organic&utm_campaign=marco_ghiani_hackernoon_learning_nodejs_5_tips)***.*** So let’s see a list of the 8 best functions from the Console module!

**All the following methods are available in the global instance** `console`***,* so it is not necessary to require the console module.**

### 1) [console.assert](https://nodejs.org/dist/latest-v12.x/docs/api/console.html#console_console_assert_value_message) ✅

The `console.assert` function is used to test if the passed argument is a truthy or falsey value. In the case that the passed value is falsey, the function logs the extra arguments passed after the first one, otherwise, the code execution proceeds without any log.

Press enter or click to view image in full size

![]()

The assert method is particularly useful whenever you want to check the existence of values while keeping the console clean (avoid logging long list of properties, etc.).

### 2) [console.count](https://nodejs.org/dist/latest-v12.x/docs/api/console.html#console_console_count_label) and [console.countReset](https://nodejs.org/dist/latest-v12.x/docs/api/console.html#console_console_countreset_label) 💯

These two methods are used to set and clear a counter of how many times a particular string gets logged in the console:

Press enter or click to view image in full size

![]()

### 3) [console.group](https://nodejs.org/dist/latest-v12.x/docs/api/console.html#console_console_group_label) and [console.groupEnd](https://nodejs.org/dist/latest-v12.x/docs/api/console.html#console_console_groupend) 🎳

`.group` and `.groupEnd` create and end a group of logs in your console. You can pass a label as the first argument of `.group()` to describe what it is concerned about:

Press enter or click to view image in full size

![]()

### 4) [console.table](https://nodejs.org/dist/latest-v12.x/docs/api/console.html#console_console_table_tabulardata_properties) 📋

This particular method is incredibly useful to describe an object or array content in a human-friendly table:

Press enter or click to view image in full size

![]()

`console.table` makes it easier for the inspection and logging of nested and complex arrays/objects.

### 5) [console.time](https://nodejs.org/dist/latest-v12.x/docs/api/console.html#console_console_time_label) and [console.timeEnd](https://nodejs.org/dist/latest-v12.x/docs/api/console.html#console_console_timeend_label) ⏱

In the case that you want to check the performance of your code in execution time, and to solve it you create a start timestamp with the `Date` API and use it to compute the difference after your code execution? Something like this:

Press enter or click to view image in full size

![]()

Well, using the `time` and `timeEnd` functions, it is not necessary to do this trick. You can create your timing report simply by doing:

Press enter or click to view image in full size

![]()

## Summary

With only 3 minutes of your time, you now have a larger scope of some of the wonderful tools available in the Console API. Integrate them with your debugging habits and your development speed will increase exponentially!

See you with the next chapter of **Learning Node.js! 🚀🎉**

> Comments, shares, and discussion about the topic are always accepted and I’ll be glad to answer any of your questions!

Thanks for reading the article!

> **Exciting news! I’m moving all of my content into one home — my personal website** [**https://marcoghiani.com/**](https://marcoghiani.com/)**.**
>
> **Everything will be easier to find, better organized, and packed with fresh updates.**
>
> **To stay in the loop and never miss a beat, be sure to subscribe to my newsletter! You’ll be the first to know about new posts, exclusive content, and more! You can find some of these posts there!**

[## The Fullscreen API is a game-changer for your website!

### Discover how the Fullscreen API can enhance user experience on your blog by offering immersive, full-screen viewing for…

marcoghiani.com](https://marcoghiani.com/blog/fullscreen-api-game-changer-website?source=post_page-----25f6ac840ada---------------------------------------)

[## How the useEventListener Hook Will Shrink Your React Components

### The useEventListener React custom hook helps attach event listeners to a React component keeping the code readable and…

marcoghiani.com](https://marcoghiani.com/blog/how-the-useeventlistener-hook-will-shrink-your-react-components?source=post_page-----25f6ac840ada---------------------------------------)

[## Lazy Load React Components With Strong Type Inference

### Create a simple utility function to encapsulate lazy loading of React components in your codebase, without compromising…

marcoghiani.com](https://marcoghiani.com/blog/lazy-load-react-components-with-strong-type-inference?source=post_page-----25f6ac840ada---------------------------------------)

[## Master the Art of Refactoring: 10 Techniques for Building Maintainable Code

### Discover 10 powerful refactoring techniques to level up your front-end coding skills.

marcoghiani.com](https://marcoghiani.com/blog/10-refactoring-techniques-maintainable-structured-code?source=post_page-----25f6ac840ada---------------------------------------)

[## Unlocking the Power of Type Encoding / Decoding with io-ts

### Revolutionize your development workflow and eliminate bugs with the io-ts library.

marcoghiani.com](https://marcoghiani.com/blog/runtime-type-encoding-decoding-io-ts?source=post_page-----25f6ac840ada---------------------------------------)

[## Introducing React v18 with real-world examples

### A simplified overview of the latest features introduced with React v18. Automatic Batching, new hooks, improved…

marcoghiani.com](https://marcoghiani.com/blog/introducing-react-v18-examples?source=post_page-----25f6ac840ada---------------------------------------)

[## React Custom Hooks #3: Simplify Your Code with useToggle and useBoolean

### Learn how to simplify your React code with the useToggle and useBoolean custom hooks. Discover how these hooks can help…

marcoghiani.com](https://marcoghiani.com/blog/react-custom-hooks-usetoggle-useboolean?source=post_page-----25f6ac840ada---------------------------------------)

[## React Custom Hooks #2: Optimize Your Font Size with useFontSize

### Improve your React app's user experience with the useFontSize custom hook. Discover how to optimize your font sizes and…

marcoghiani.com](https://marcoghiani.com/blog/react-custom-hooks-usefontsize?source=post_page-----25f6ac840ada---------------------------------------)

[## React Custom Hooks #1: Manage Your Data with useLocalStorage

### Manage your data efficiently with the useLocalStorage custom hook. Learn how to simplify data storage and retrieval in…

marcoghiani.com](https://marcoghiani.com/blog/react-custom-hooks-uselocalstorage?source=post_page-----25f6ac840ada---------------------------------------)

[## How to Use React useReducer Effectively

### Learn how to use the useReducer hook in React to manage your app's state more effectively. Discover best practices and…

marcoghiani.com](https://marcoghiani.com/blog/how-to-use-react-reducer-effectively?source=post_page-----25f6ac840ada---------------------------------------)

[## 6 Essential NPM Commands for Highly Productive Developers

### Discover 6 essential NPM commands to improve your productivity as a developer. Learn how to optimize your development…

marcoghiani.com](https://marcoghiani.com/blog/6-npm-commands-used-by-highly-productive-developers?source=post_page-----25f6ac840ada---------------------------------------)

[## How a Simple Daily Routine Built A Writing Habit.

### Learn how a simple daily routine can help you build a writing habit. Discover practical tips and strategies for…

marcoghiani.com](https://marcoghiani.com/blog/the-daily-routine-to-achieve-more?source=post_page-----25f6ac840ada---------------------------------------)

[## Write a JavaScript Fetch Wrapper in Less Than 1kb

### Learn how to write a lightweight JavaScript fetch wrapper in less than 1kb. Discover how this powerful tool can…

marcoghiani.com](https://marcoghiani.com/blog/write-a-javascript-fetch-wrapper-in-less-than-1kb?source=post_page-----25f6ac840ada---------------------------------------)

[## Do I Really Know Programming? 5 Signs You're on the Right Track

### Wondering if you know programming? Discover 5 signs that you're on the right track to becoming a skilled developer…

marcoghiani.com](https://marcoghiani.com/blog/do-i-really-know-programming?source=post_page-----25f6ac840ada---------------------------------------)

[## Remote Work Transforms You Into Your Best Version.

### Discover how remote work can help you become your best self. Learn practical tips and strategies for staying productive…

marcoghiani.com](https://marcoghiani.com/blog/remote-work-transforms-you-into-your-best-version?source=post_page-----25f6ac840ada---------------------------------------)

[## 4 Must-Read Books for Everyone in Tech and Why

### Find out which books you should be reading as a tech professional. Discover why these books are essential for building…

marcoghiani.com](https://marcoghiani.com/blog/4-books-everyone-in-tech-should-read-and-why?source=post_page-----25f6ac840ada---------------------------------------)

[## 5 Git Shortcuts to Improve Your Coding Speed and Efficiency

### Simplify your Git workflow and speed up your coding with these 5 essential Git shortcuts. Learn how to work smarter…

marcoghiani.com](https://marcoghiani.com/blog/learning-git-shortcuts?source=post_page-----25f6ac840ada---------------------------------------)

[## 42 Mac Keyboard Shortcuts: Boost Your Productivity 5x Faster

### Spend less time clicking and more time doing with these 42 Mac keyboard shortcuts. Increase your productivity and…

marcoghiani.com](https://marcoghiani.com/blog/fast-as-never-before-42-mac-keyboard-shortcuts-to-work-5x-faster?source=post_page-----25f6ac840ada---------------------------------------)

[## 10 Programming Code Smells That Affect Your Codebase

### Improve the quality of your codebase by eliminating these 10 common programming code smells. Ensure maintainability…

marcoghiani.com](https://marcoghiani.com/blog/10-programming-code-smells-that-affect-your-codebase?source=post_page-----25f6ac840ada---------------------------------------)

[## UseDeepEffect Hook in React: A Comprehensive Guide for Improved Performance

### Learn how to use the useDeepEffect hook in React to optimize your app's performance. Get step-by-step instructions for…

marcoghiani.com](https://marcoghiani.com/blog/how-to-use-the-react-hook-usedeepeffect?source=post_page-----25f6ac840ada---------------------------------------)

[## 5 Tips to Speed Up Your MacBook Productivity

### A collection of hints to improve MacBook performance.

marcoghiani.com](https://marcoghiani.com/blog/5-tips-to-speed-up-your-macbook-productivity?source=post_page-----25f6ac840ada---------------------------------------)

[## How to Become a Better Software Engineer: Proven Tips and Strategies

### Transform your skills and become a better software engineer with these proven tips and strategies. From coding to…

marcoghiani.com](https://marcoghiani.com/blog/how-to-become-a-better-software-engineer?source=post_page-----25f6ac840ada---------------------------------------)

[## 3 JavaScript Refactoring Techniques for Clean Code and Best Practices

### Improve the quality of your JavaScript code with these 3 essential refactoring techniques. Follow these best practices…

marcoghiani.com](https://marcoghiani.com/blog/3-javascript-refactoring-techniques-for-clean-code?source=post_page-----25f6ac840ada---------------------------------------)

[## Boost Your React App with 4 Custom Hooks

### Discover 4 powerful custom hooks to enhance your React app. These hooks will help you improve performance…

marcoghiani.com](https://marcoghiani.com/blog/4-custom-hooks-to-boost-your-react-app?source=post_page-----25f6ac840ada---------------------------------------)

[## How to Use Component Composition in React

### Get started with component composition in React with this beginner's guide. Learn the basics of this essential…

marcoghiani.com](https://marcoghiani.com/blog/how-to-use-component-composition-in-react?source=post_page-----25f6ac840ada---------------------------------------)

[## Refactoring a React Component: Best Practices for Better Code

### Follow these 5 best practices for refactoring a React component and improve the quality of your codebase. Learn how to…

marcoghiani.com](https://marcoghiani.com/blog/refactoring-a-react-component?source=post_page-----25f6ac840ada---------------------------------------)

[## Moving beyond console.log() - 8 Console Methods You Should Use When Debugging JavaScript and Node

### Improve your JavaScript and Node debugging with these 8 powerful console methods beyond console.log(). Learn how to use…

marcoghiani.com](https://marcoghiani.com/blog/moving-beyond-console-log-8-console-methods-you-should-use-when-debugging-javascript-and-node?source=post_page-----25f6ac840ada---------------------------------------)

[## How to Setup Your Redux Store for a High-Performing React Application

### Learn how to set up your Redux store for a high-performing React application with this step-by-step guide. Discover the…

marcoghiani.com](https://marcoghiani.com/blog/redux-store-setup-for-your-react-application?source=post_page-----25f6ac840ada---------------------------------------)

[## How I Became a Fast Learner Changing My Habits.

### 9 effective habits to learn faster and increase your productivity.

marcoghiani.com](https://marcoghiani.com/blog/how-i-became-a-fast-learner-changing-my-habits?source=post_page-----25f6ac840ada---------------------------------------)

[## Building a High-Performance Web Application with Advanced Koa.js Boilerplate

### Maximize your web application's performance with this advanced Koa.js boilerplate. Learn how to create a…

marcoghiani.com](https://marcoghiani.com/blog/advanced-koa-js-boilerplate?source=post_page-----25f6ac840ada---------------------------------------)

[## How to Use the useViewport Custom Hook in React

### Enhance your React development process with the useViewport custom hook. Our guide offers a step-by-step tutorial on…

marcoghiani.com](https://marcoghiani.com/snippets/use-viewport-custom-hook?source=post_page-----25f6ac840ada---------------------------------------)

[## How to Filter Object Properties in JavaScript

### A simple JavaScript polyfill of the filter array method applied to object properties

marcoghiani.com](https://marcoghiani.com/snippets/filter-method-for-object-properties?source=post_page-----25f6ac840ada---------------------------------------)

[## How to Implement Array Flat and FlatMap Methods in JavaScript

### Learn how to use the Array flat and flatMap methods in JavaScript and speed up your development process. Our guide…

marcoghiani.com](https://marcoghiani.com/snippets/array-flat-and-flatmap?source=post_page-----25f6ac840ada---------------------------------------)

[## From Error-First Callback Functions to Promises in JavaScript

### Make the transition from error-first callback functions to promises in JavaScript with our guide. Learn how to use…

marcoghiani.com](https://marcoghiani.com/snippets/error-first-callback-functions-to-promises?source=post_page-----25f6ac840ada---------------------------------------)

[## Object and Array Deep Clone: How to Implement in JavaScript

### A straightforward implementation for a deep clone method in JavaScript

marcoghiani.com](https://marcoghiani.com/snippets/object-array-deep-clone?source=post_page-----25f6ac840ada---------------------------------------)