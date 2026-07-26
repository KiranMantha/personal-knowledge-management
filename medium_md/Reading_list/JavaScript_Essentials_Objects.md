---
title: "JavaScript Essentials: Objects"
url: https://medium.com/p/56373a1a6bfb
---

# JavaScript Essentials: Objects

[Original](https://medium.com/p/56373a1a6bfb)

# JavaScript Essentials: Objects

[![CodeDraken](https://miro.medium.com/v2/resize:fill:64:64/2*utMzH99Qblt1d3UvyOIrrA.png)](https://codedraken.medium.com/?source=post_page---byline--56373a1a6bfb---------------------------------------)

[CodeDraken](https://codedraken.medium.com/?source=post_page---byline--56373a1a6bfb---------------------------------------)

9 min read

·

Oct 9, 2018

--

10

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D56373a1a6bfb&operation=register&redirect=https%3A%2F%2Fcodeburst.io%2Fjavascript-essentials-objects-56373a1a6bfb&source=---header_actions--56373a1a6bfb---------------------post_audio_button------------------)

Share

Essentials is a series that covers the most used and important methods for X topic along with some other fundamentals. In this post we cover Objects.

## Table of Contents

— [**JavaScript Essentials: Objects**](https://medium.com/p/56373a1a6bfb#ced4)  
 — — [Prerequisites](https://medium.com/p/56373a1a6bfb#07bc)  
 — [**Objects the Basics**](https://medium.com/p/56373a1a6bfb#01e0) — — [Basic Object Creation](https://medium.com/p/56373a1a6bfb#5da4)  
 — — [Object Definitions](https://medium.com/p/56373a1a6bfb#5afd)  
 — — [What is This?](https://medium.com/p/56373a1a6bfb#d662)  
 — — [What does ‘this’ point to?](https://medium.com/p/56373a1a6bfb#649a)  
 — — [Prototypes](https://medium.com/p/56373a1a6bfb#2636)  
 — — [Class Syntax](https://medium.com/p/56373a1a6bfb#9499)  
 — [**Important Guidelines and Fundamentals**](https://medium.com/p/56373a1a6bfb#dc26)  
 — [**Common Methods**](https://medium.com/p/56373a1a6bfb#f8bc)  
 — — [Getters and Setters](https://medium.com/p/56373a1a6bfb#2a46)  
 — — [Key-Pair Array into Object ( experimental )](https://medium.com/p/56373a1a6bfb#b8da)  
 — — [Make an Object Immutable](https://medium.com/p/56373a1a6bfb#fb82)  
 — — [Shallow Copy an Object](https://medium.com/p/56373a1a6bfb#3164)  
 — — [Deep Copy an Object](https://medium.com/p/56373a1a6bfb#e460)  
 — — [Convert Object to JSON](https://medium.com/p/56373a1a6bfb#5b61)  
 — — [Loop an Object](https://medium.com/p/56373a1a6bfb#d3ec)  
 — — [Check if a Key Exists in an Object](https://medium.com/p/56373a1a6bfb#9337)  
 — — [Dynamic Keys](https://medium.com/p/56373a1a6bfb#4b1a)  
 — — [Binding ‘this’ on Classes](https://medium.com/p/56373a1a6bfb#c3b0)  
 — [**References and Links to Learn More**](https://medium.com/p/56373a1a6bfb#5899)

### Prerequisites

It’s *recommended* that you know about types. Other JS topics would be helpful too but are not required.

[## JavaScript Essentials

### JavaScript Essentials started out as just a quick showcase of common methods and techniques to do certain things but it…

medium.com](https://medium.com/@codedraken/javascript-essentials-cc600606bab0?source=post_page-----56373a1a6bfb---------------------------------------)

**Note**: This is a long post covering both the fundamentals of objects and common methods. You can [skip to the methods by clicking here](#f8bc).

You can access all the code shown here for copying/experimenting using [this gist](https://gist.github.com/CodeDraken/870a732174f54601d63b92f2fc1818d1).

## Objects the Basics

> An object is a collection of related data and/or functionality (which usually consists of several variables and functions — which are called properties and methods when they are inside objects.)  
>  — [MDN](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/Basics)

Objects are just like objects in real life. They have properties, sometimes can do things and often extend another object.

For example, let’s imagine a dog.

![]()

How would you describe a dog? What properties does it have? What can it do? Dogs evolved from wolves — so we could say they **extend** the properties of a wolf. What can a wolf do? What properties does a wolf have?

![]()

In this example, I’ve modeled a very simple wolf and dog. A wolf has a fur color, size, age, etc and it can run, eat and sleep. A dog is a type of wolf with some extra properties and actions.

A **dog has everything a wolf does** and gets a special name i.e “poodle”. It can do more actions like cuddle and pee on fire hydrants. You could go even deeper and extend what a dog does for a specific type of dog. i.e rescue dog extends dog and has an additional action “rescue”.

### Basic Object Creation

There are quite a few ways to create objects. The simplest way is using an object literal — which is literally writing out the contents of an object. ( don’t worry we’ll cover more advanced Object creation later! )

Press enter or click to view image in full size

![]()

**Note**: The greet function syntax above is an ES6 feature. You could alternatively define a key like normal and give it a value of a function — either a reference to a function or inline a function. i.e `greet: function() {}` or `greet: greetFunc` etc.

### Object Definitions

**Property/Key** — these are basically variables located in an object. They have a name which you use to access it and a value. i.e `name: 'Jeff'`

**Method** — methods are **functions that live on an object** and often make use of the object’s properties.

### What is This?

I’m literally referring to `this` in JavaScript. This is perhaps the part of JS that confuses people the most.

**This** — a **variable created by JavaScript** when an execution context is created ( i.e running a function ) that **points to an object**. What object it points to depends on how the function is called.

**Execution Context** — when a function is called an execution context is created. This context holds function variables, `this` and a reference to the outer environment.

![]()

### What does ‘this’ point to?

We understand `this` is a value given to us by JavaScript when a function is called. What determines the object `this` points to? That depends on how the function is called.

**Rules in order of precedence:**

1. **Using an Arrow Function? (lexical)** — `this` comes from the outer lexical scope / containing function. If there is no containing function then it’s global, otherwise perform these checks again on the outer function.

![]()

**2. Using the New Operator? (constructor functions)** — if the function is called with the `new` keyword then `this` is **set to the newly created object**.

Press enter or click to view image in full size

![]()

**3. Did you set this yourself? (explicit) —** If you used `.call` `.apply` `.bind` or an argument to set `this` in a supported function then `this` is whatever value you set it to using explicit binding unless you used `null` or `undefined` which in that case it would point to the global object.

Press enter or click to view image in full size

![]()

**4. Was the function called as a method? (implicit)**— `this` is the preceding object. For `obj.method` `obj` is the value for `this` using implicit binding. Be aware that functions nested inside the method may not have the same `this` variable.

Press enter or click to view image in full size

![]()

**Note:** The function doesn’t have to be inside the object. It can be a reference to a function i.e `greet: greetFunc` What matters is the **function call is preceded by an object reference**.

**5. None of the above? (default) —** by default `this` will **refer to the global object**. If strict mode is enabled it will be `undefined`.

Press enter or click to view image in full size

![]()

If you’re interested in learning more about `this` then here are some reference links and my tutorial on it.

[## The Simple Guide to “This” in JavaScript

### The last guide you will ever need for understanding this in JavaScript. We will explore what this is, and how to…

codeburst.io](/the-simple-guide-to-this-in-javascript-24a6638b1105?source=post_page-----56373a1a6bfb---------------------------------------)

[## Arrow functions

### An arrow function expression has a shorter syntax than a function expression and does not have its own this, arguments…

developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions?source=post_page-----56373a1a6bfb---------------------------------------)

[## this

### A function's this keyword behaves a little differently in JavaScript compared to other languages. It also has some…

developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this?source=post_page-----56373a1a6bfb---------------------------------------)

### Prototypes

Prototypes is a way to add methods to your objects while only having one method exist in memory.

**Inheritance** — when an object shares the methods and properties of another object.

**Classical Inheritance** — this is what you find in languages like C#, Java, etc

**Prototypal Inheritance** — when a property can’t be found on an object it searches a chain like structure called the prototype. If it’s not found on the next prototype object it will look at the prototype of that prototype.

For example, when you have an Array and you use a method like `.sort` that method does not exist on the array itself — it exists on the prototype.

![]()

Here’s a simple example in code.

Press enter or click to view image in full size

![]()

Here’s a comparison of a traditional constructor vs prototypes.

Press enter or click to view image in full size

![]()

[## Object prototypes

### This article has covered JavaScript object prototypes, including how prototype object chains allow objects to inherit…

developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/Object_prototypes?source=post_page-----56373a1a6bfb---------------------------------------)

### Class Syntax

Classes are popular in other Object Oriented programming languages and JavaScript decided to copy that. Classes in JS are not the same, they don’t introduce a new object model — they’re just **syntactic sugar for prototypes**.

Let’s define some parts of a Class.

* **Class Definition** — how we define a class, can be a top level class or extend another class.
* **Constructor** — method for initializing values on the class instance
* **Super** — used to pass arguments to the parent class and use methods from the parent
* **Static Methods** — methods that only work on the class constructor, not on instances
* **Instance Methods** — methods with `this` set to the specific instance of a class

Here’s what it looks like in code, using the dog example from earlier with some changes.

Press enter or click to view image in full size

![]()

## Important Guidelines and Fundamentals

Important guidelines to keep in mind.

* Everything that’s not a primitive is an Object. [( learn about types )](/javascript-essentials-types-data-structures-3ac039f9877b)
* There are many ways to create objects
* Objects are ways to describe objects or data with properties and methods
* `this` is determined at runtime
* Classes are just syntactic sugar

## Common Methods

Below are code blocks, some with a scenario/task described in a comment up top then some code below and others just showcasing methods.

For the most part, you’ll define your own methods on objects, but there are a few static methods on Object that are useful. I’ll cover those and techniques for doing certain things such as looping over an object.

### Getters and Setters

We can use getters and setters to control access to our Object.

Press enter or click to view image in full size

![]()

### Key-Pair Array into Object ( experimental )

Currently a stage-3 proposal.

Press enter or click to view image in full size

![]()

### Make an Object Immutable

We can use `Object.freeze()` to make an Object immutable.

Qualities of a frozen object:

* New properties cannot be added
* Existing properties cannot be removed
* Values of properties cannot be changed
* The prototype cannot be changed

Press enter or click to view image in full size

![]()

### Shallow Copy an Object

Shallow copying an Object means we’re copying values, but the references are the same. i.e objects point to the same object.

Press enter or click to view image in full size

![]()

### Deep Copy an Object

Deep copying is making an entire copy of an Object with no shared references.

Press enter or click to view image in full size

![]()

### Convert Object to JSON

Press enter or click to view image in full size

![]()

### Loop an Object

Press enter or click to view image in full size

![]()

### Check if a Key Exists in an Object

Press enter or click to view image in full size

![]()

### Dynamic Keys

…

### Binding ‘this’ on Classes

…

*More to be added*

## References and Links to Learn More

[## Object-oriented JavaScript for beginners

### This article has provided a simplified view of object-oriented theory - this isn't the whole story, but it gives you an…

developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/Object-oriented_JS?source=post_page-----56373a1a6bfb---------------------------------------)

[## JavaScript object basics

### Congratulations, you've reached the end of our first JS objects article - you should now have a good idea of how to…

developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/Basics?source=post_page-----56373a1a6bfb---------------------------------------)

[## Object

### The Object constructor creates an object wrapper.

developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object?source=post_page-----56373a1a6bfb---------------------------------------)

[## this

### A function's this keyword behaves a little differently in JavaScript compared to other languages. It also has some…

developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this?source=post_page-----56373a1a6bfb---------------------------------------)

[## ES6 In Depth: Classes - Mozilla Hacks - the Web developer blog

### ES6 In Depth is a series on new features being added to the JavaScript programming language in the 6th Edition of the…

hacks.mozilla.org](https://hacks.mozilla.org/2015/07/es6-in-depth-classes/?source=post_page-----56373a1a6bfb---------------------------------------)

[## The Simple Guide to “This” in JavaScript

### The last guide you will ever need for understanding this in JavaScript. We will explore what this is, and how to…

codeburst.io](/the-simple-guide-to-this-in-javascript-24a6638b1105?source=post_page-----56373a1a6bfb---------------------------------------)

Read more JavaScript Essentials:

[## JavaScript Essentials

### JavaScript Essentials started out as just a quick showcase of common methods and techniques to do certain things but it…

medium.com](https://medium.com/@codedraken/javascript-essentials-cc600606bab0?source=post_page-----56373a1a6bfb---------------------------------------)

Thanks for reading! Leave any feedback or questions in the comments below.