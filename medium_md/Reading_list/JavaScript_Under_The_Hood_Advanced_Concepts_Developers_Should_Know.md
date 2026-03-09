---
title: "JavaScript Under The Hood: Advanced Concepts Developers Should Know"
url: https://medium.com/p/a89ddbb11228
---

# JavaScript Under The Hood: Advanced Concepts Developers Should Know

[Original](https://medium.com/p/a89ddbb11228)

# JavaScript Under The Hood: Advanced Concepts Developers Should Know

## The art of programming is the skill of controlling complexity.

[![Noor Ahmed](https://miro.medium.com/v2/resize:fill:64:64/1*p53Smv8cq2h9bizJ335xZQ@2x.jpeg)](https://medium.com/@noor882?source=post_page---byline--a89ddbb11228---------------------------------------)

[Noor Ahmed](https://medium.com/@noor882?source=post_page---byline--a89ddbb11228---------------------------------------)

8 min read

·

May 12, 2022

--

12

Listen

Share

More

Have you ever wondered what happens inside the JavaScript engine when you execute your code?

![]()

It’s pretty interesting!

Currently, it’s 2022. JavaScript has taken over the internet. People are swarming to libraries and frameworks searching for helpful anything — Not understanding the **fundamentals** of JavaScript.

In addition, they claim that JavaScript sucks. What the hell?

> When I first decided to work using JavaScript, I had a lot of questions and couldn’t figure out why my code behaved the way it did. It was challenging to handle undefined errors or identify the scope of a variable.

In this blog, I’ll walk you through your code’s journey, illustrating the inner workings of advanced concepts like **scope chain, hoisting, asynchronous, and function execution** concerning **execution context** and the **call stack**.

All subtopics are related, so please don’t skip them — grab a cup of coffee, and enjoy reading!.

[![Build in AI speed — Compose enterprise-grade applications, features, and components]()](https://bit.cloud)

## The first thing that happens inside the engine

Press enter or click to view image in full size

![]()

Your code isn’t magic. Someone else wrote a program to translate it for the computer.

When you write a program, a **syntax parser** reads your code and then the **compiler** translates it into computer instructions(*a lower-level language).*

Take a look at this simple code:

![]()

Where you write your code and what surrounds it is crucial! The area of the code you are looking at physically is the **lexical environment.**

In the above example, I would say the variable “**greetings**” sits **lexically** inside the function **sayHello.**

It sounds funny, but not every programming language is like that. In JS, however, the **compiler** that converts your code cares about where you put things. And based on it, decide where your code will sit in the memory and interact.

So there are multiple **lexical environments**, but one that is being executed is handled by **the execution context** — *a context in which javascript code is running.*

## **The Global Execution Context**

When the compiler first looks at your code, it asks the JS engine to create a **global execution context** for you.

![]()

The following duties are carried out:

> *• Create a* ***Memory Heap*** *to keep all variables and functions at a global level*
>
> *• Create a* ***Global Object*** *and “***this***” keyword*

The location of “***this”*** depends on where your code is running. In the browser, for example, it points to **windows** objects. Nodejs, for example, will point to a different global object.

Press enter or click to view image in full size

![]()

Before proceeding with the code execution, it is vital to grasp the **hoisting.** And for that, we need to look at the **memory allocation.**

## Execution Context: Hoisting

We are frequently baffled when it comes to hoisting. One of the most fundamental JS concepts to grasp and among the interviewer’s top questions.

Take a look at the code above. We ran our code before the declaration and, sayHello() returned “**Hello!**” whereas myVar logged **undefined**?

Why is that?

We need to look at the **execution context creation phase**. When your **parser** runs through your code, it recognizes where you have created the variables and functions, and so it sets up the **memory space** for them — *Which explains why you can access functions and variables before they are* ***declared***.

However, keep in mind that only **declarations are hoisted** by JavaScript, **not initializations**! That is, initialization does not occur until the appropriate line of code is executed. Until then, when declared with “**var**,” the variable is set to “**undefined**” (*let and const are hoisted but are* ***not initialized*** *with a* ***default value***). Function declarations are hoisted in the same way, but **function expressions are not**.

*Now that your code has been* ***compiled*** *and* ***memory space*** *has been set up, it’s time to* ***execute it***.

## Execution context — function invocation and the Call Stack

***When your code is executed line by line…***

![]()

As your code is executed, the variable **favorite** is assigned to **“C#”**, and when it encounters **favLanguage()**, it says, “*Ahh, I need to invoke this function*.”

It creates a **new execution context** and puts it on top of the **call stack —** *like an actual stack in data structures that follows the* ***Last In First Out (LIFO) principle.*** It has its **creation and execution phases**, where **memory space** for any variables or function calls inside side **favLanguage()** is assigned.

It then runs each line inside **favLanguage()**. As it does so, a **favorite** is assigned to “**javascript**”, and **otherLanguage()** is invoked, which creates another execution context for it and places it at the top of the **call stack**.

![]()

Here’s how the above explanation looks in real-time!

![]()

```
Even though "favorite" is declared 3 times, they are unique and don't touch each other as they exist in their execution context within its variable environment.
```

***Quick note****:* When a function completes its execution, JS immediately freezes and **garbage-collects** the **memory** associated with it to **prevent memory leaks**, unless you’re using **closures**, in which case it will only release the memory once all of its **dependant functions** have been removed from the call stack.

## Execution Context: Scope Chain

***How does a function access variables outside of its execution context?***

In JavaScript, the scope goes from outer to inner. This means that variables declared in the outer scope can be accessed in all inner scope, not vice versa. This entire notion is called a **scope chain**…!

**What do you anticipate console.log (sport) to return in the code below?**

I hope you said “basketball”. As we already know when **otherSport()** ran, an execution context was generated, triggering **favoriteSport()**, which likewise produced another execution context. When **console.log (sport)** was run, it attempted to locate the variable declaration in the **favoriteSport** function.

Still, when it couldn’t, it examined the outside reference and went hunting for the variables someplace **down the call stack**. And the **external reference** point is **determined** by where your function is **lexically situated**.

![]()

For example, **favoriteSport() is lexically positioned not within function** **otherSport** but at the global level. As a result, its **external environment** is **global**, and it discovered “**sport**” in the **global execution context, hence logging “basketball”**

> Here is a bit of fun exercise for you guys. What do you think console.log will return and why? Explain the code execution or draw a scope chain like the above. Let me know in the comments.

![]()

## JS fascinatingly handles asynchronous tasks!

I hope this does not surprise you, but Javascript is ***NOT*** **asynchronous** but **synchronous, single-threaded language**(*one task at a time). Y*ou can, however, manipulate JavaScript to behave **asynchronously**. It’s not baked in, but it’s feasible!. Let’s have a peek.

As you can see in the preceding code, it logged “**hi,**” **hi again!**,” and “**I’m awake**” in that sequence; however, given what we know so far, it can’t be using a call stack as functions are handled synchronously. Then what?. This is where the **Javascript runtime** comes in.

![]()

The web browser comes with a **web API** that handles **HTTP requests**, managing **dom events**, or delaying execution like **setTimeout**. We call these web APIs **asynchronous.**

```
So, here's how it works: We have things like a set timeout in the call stack that aren't part of JavaScript. The call stack tells the web API, "Oh, I have something that isn't mine, and I don't know what to do with it." It passes it on to the Web API.  
   
In contrast to Web APIs, JavaScript synchronously performs tasks in the call stack. Tasks are placed in the callback queue when the web API completes its processing.The call stack will be informed that I have something for you through the Event Loop. A task from the callback queue is added to the call stack and logged as "Hi, I'm awake" when the call stack is empty.
```

Another live visualization, this time with the Javascript runtime!

Press enter or click to view image in full size

![]()

## Conclusion

JavaScript is a powerful tool you use every day, so I hope you gain a deeper understanding of its fundamental concepts as I have introduced them with sample code to help students comprehend the principles.

Don’t stop there, though. If you want to be in the top **10% of JavaScript developers**, you should study these topics and their inner workings:

```
Object-oriented & functional Programming, prototype inheritance, modules, error handling, and types in javascript.
```

**Cheers!**

Follow me on [Medium](https://medium.com/@noor882) and [LinkedIn](https://www.linkedin.com/in/noorahmed11/) to remain up to date on new articles I’ll be writing!

## Bit: Feel the power of component-driven dev

Say hey to [**Bit**](https://bit.cloud). It’s the #1 tool for component-driven app development.

With Bit, you can create any part of your app as a “component” that’s composable and reusable. You and your team can share a toolbox of components to build more apps faster and consistently together.

* Create and compose “**app building blocks**”: UI elements, full features, pages, applications, serverless, or micro-services. With any JS stack.
* Easily **share, and reuse** components as a team.
* Quickly **update** **components** across projects.
* Make hard things simple: [Monorepos](https://bit.cloud/blog/painless-monorepo-dependency-management-with-bit-l4f9fzyw), [design systems](/how-we-build-our-design-system-15713a1f1833) & [micro-frontends](/how-we-build-micro-front-ends-d3eeeac0acfc).

[**Try Bit open-source and free→**](https://bit.cloud)

[![]()](https://bit.cloud)

## Learn more

[## How We Build Micro Frontends

### Building micro-frontends to speed up and scale our web development process.

blog.bitsrc.io](/how-we-build-micro-front-ends-d3eeeac0acfc?source=post_page-----a89ddbb11228---------------------------------------)

[## How we Build a Component Design System

### Building a design system with components to standardize and scale our UI development process.

blog.bitsrc.io](/how-we-build-our-design-system-15713a1f1833?source=post_page-----a89ddbb11228---------------------------------------)

[## How to reuse React components across your projects

### Finally, you completed the task of creating a fantastic input field for the newsletter in your app. You are happy with…

bit.cloud](https://bit.cloud/blog/how-to-reuse-react-components-across-your-projects-l3bhezsg?source=post_page-----a89ddbb11228---------------------------------------)

[## Painless monorepo dependency management with Bit

### Simplify dependency management in a monorepo to avoid issues with phantom dependencies and versions. Learn about…

bit.cloud](https://bit.cloud/blog/painless-monorepo-dependency-management-with-bit-l4f9fzyw?source=post_page-----a89ddbb11228---------------------------------------)