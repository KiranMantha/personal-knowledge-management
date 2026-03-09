---
title: "Execution context, Scope chain and JavaScript internals"
url: https://medium.com/p/319dd72e8e2c
---

# Execution context, Scope chain and JavaScript internals

[Original](https://medium.com/p/319dd72e8e2c)

# Execution context, Scope chain and JavaScript internals

[![Rupesh Mishra](https://miro.medium.com/v2/resize:fill:64:64/1*vkWAize3YPtA-vPkoQ06cA.jpeg)](/@happymishra66?source=post_page---byline--319dd72e8e2c---------------------------------------)

[Rupesh Mishra](/@happymishra66?source=post_page---byline--319dd72e8e2c---------------------------------------)

10 min read

·

May 18, 2017

--

26

Listen

Share

More

Press enter or click to view image in full size

![]()

In this post, we will discuss what is execution context and scope chain in JavaScript. We will also check the internal working of JavaScript step by step. Understanding these concepts will not only help in understanding the JavaScript internals but also other concepts like hoisting and closure.

**Execution context** (**EC**)is defined as the environment in which the JavaScript code is executed. By environment, I mean the value of `this`, *variables*, *objects*, and *functions* JavaScript code has access to at a particular time.

Execution context in JavaScript is of three types as:

1. **Global execution context** (**GEC**): This is the default execution context in which JS code start its execution when the file first loads in the browser. All of the global code i.e. code which is not inside any function or object is executed inside the global execution context. GEC cannot be more than one because only one global environment is possible for JS code execution as the JS engine is single threaded.
2. **Functional execution context** (**FEC**): Functional execution context is defined as the context created by the JS engine whenever it finds any function call. Each function has its own execution context. It can be more than one. Functional execution context has access to all the code of the global execution context though vice versa is not applicable. While executing the global execution context code, if JS engine finds a function call, it creates a new functional execution context for that function. In the browser context, if the code is executing in `strict` mode value of `this`is `undefined`else it is `window`object in the function execution context.
3. **Eval**: Execution context inside `eval` function.

**Execution context stack (ECS):** Execution context stack is a stack data structure, i.e. last in first out data structure, to store all the execution stacks created during the life cycle of the script. Global execution context is present by default in execution context stack and it is at the bottom of the stack. While executing the global execution context code, if JS engines find a function call, it creates a functional execution context for that function and pushes it on top of the execution context stack. JS engine executes the function whose execution context is at the top of the execution context stack. Once all the code of the function is executed, JS engines pop out that function’s execution context and start’s executing the function which is below it.

Let’s understand this with the help of an example:

Press enter or click to view image in full size

![]()

As soon as the above code loads into the browser, JS engine pushes the global execution context in the execution context stack. When `functionA` is called from global execution context, JS engine pushes `functionA` execution context in the execution context stack and starts executing `functionA`.

When `functionB` is called from `functionA` execution context, JS engine pushes `functionB` execution context in the execution context stack. Once all the code of `functionB` gets executed, JS engine pops out `functionB` execution context. After this, as `functionA` execution context is on top of the execution context stack, JS engine starts executing the remaining code of `functionA`.

Once all the code from `functionA` gets executed, JS engine pops out `functionA` execution context from execution context stack and starts executing remaining code from the global execution context.

When all the code is executed JS engine pops out the global execution context and execution of JavaScript ends.

So far we have discussed how the JavaScript engine handles the execution context. Now, we will see how it creates the execution context.

JavaScript engine creates the execution context in the following two stages:

1. Creation phase
2. Execution phase

**Creation phase** is the phase in which the JS engine has called a function but its execution has not started. In the creation phase, JS engine is in the compilation phase and it just scans over the function code to compile the code, it doesn’t execute any code.

In the creation phase, JS engine performs the following task:

1. **Creates the Activation object or the Variable object**: Activation object is a special object in JS which contain all the variables, function arguments and inner functions declaration information. As activation object is a special object it does not have the`dunder proto` property.
2. **Creates the scope chain:** Once the activation object gets created, the JS engine initializes the scope chain which is a list of all the variables objects inside which the current function exists. This also includes the variable object of the global execution context. Scope chain also contains the current function variable object.
3. **Determines the value of this:**After the scope chain, the JavaScript engine initializes the value of `this`*.*

Let’s understand how JavaScript engine creates the activation object with an example

Just after `funA` is called and before code execution of `funA` starts, JS engine creates an `executonContextObj` for `funA` which can be represented as shown below:

Activation object or variable object contains the argument object which has details about the arguments of the function.

It will have a property name for each of the variables and functions which are declared inside the current function. Activation object or the variable object in our case will be as shown below:

1. **ArgumentObject**: JS engines will create the argument object as shown in the above code. It will also have the `length` property indicating the total number of arguments in the function. It will just have the property name, not its value
2. Now, for each variable in the function, JS engine will create a property on the *activation object or variable object* and will initialize it with `undefined`. As arguments are also variables inside the function, they are also present as a property of the argument object.
3. If the variable already exists as a property of the argument object JS engine will not do anything and will move to the next line.
4. When JS engine encounters a function definition inside the current function, it will create a new property by the name of the function. Function definitions in the creation phase are stored in heap memory, they are not stored in the execution context stack. Function name property points to its definition in the heap memory.

Hence in our case, first, `d`will get the value of `undefined`as it is a variable but when JS engine encounters a function with the same name it overrides its value to point it to the definition of function `d`stored in the heap.

After this JS engines will create the scope chain and will determine the value of `this`.

**Execution phase:**

In the execution phase, JS engines will again scan through the function to update the variable object with the values of the variables and will execute the code.

After the execution stage, the variable object will look like this:

**Complete example:**

Consider the code below.

When the above code loads in the browser, JS engine will enter the compilation phase to create the execution objects. In the compilation phase, JS engine will handle only the declarations, it won’t bother about the values. This is the creation phase of the execution context.

**Line 1**: In this line, variable`a`is assigned a value of `1`, so JS engine does not think of it as a variable declaration or function declaration and it moves to *line 3*. It does not do anything with this line in the compilation phase as it is not any declaration.

**Line 3**: As the above code is in the global scope and it’s a variable declaration, JS engines will create a property with the name of this variable in the global execution context object and will initialize it with an `undefined`value.

**Line 5**: JS engine finds a function declaration, so it will store the function definition in heap memory and creates a property which will point to the location where function definition is stored. JS engine doesn’t know what is inside of *cFunc* it just points to its location.

**Line 18**: This code is not any declaration hence, JS engine will not do anything.

**Global Execution Context object after the creation phase stage:**

As further there is no code, JS engine will now enter the **execution phase** and will scan the function again. Here, it will update the variable value and will execute the code.

**Line 1**: JS engines find that there is no property with the name `a`in the variable object, hence it adds this property in the global execution context and initializes its value to `1`.

**Line 3**: JS engines checks that there is a property with the name`b`in the variable object and hence update its value to `2`.

**Line 5**: As it is a function declaration, it doesn’t do anything and moves to line 18.

**Global execution context object after the execution phase:**

**Line 18**: Here, `cFunc` is called, so JS engine again enters the compilation phase to create the execution context object of `cFunc`by scanning it.

As `cFunc`has `e`as an argument, JS engine will add `e`in the argument object of `cFunc`execution context object and create a property by the name of `e`and will initialize it to `2`.

**Line 6**: JS engine will check if `c`is a property in the activation object of `cFunc`. As there is no property by that name, it will add `c`as property and will initialize its value to `undefined`.

**Line 7**: Same as line 6

**Line 9**: As this line is not a declaration, JS engine will move to the next line

**Line 11**: JS engine finds a function declaration, so it will store the function definition in the heap memory and create a property `dFunc`which will point to the location where function definition is stored. JS engine doesn’t know what is inside `dFunc`.

`cFunc` **execution context object after the compilation phase:**

**Line 15**: As this statement is not a declaration, JS engine will not do anything.

As further there are no lines in this function JS engine will enter the execution phase and will execute *cFunc*by scanning it again.

**Line 6 and 7**: `c`and `d`gets the value of 10 and 15 respectively

**Line 9**: As `a`is not a property on `cFunc`execution context object and it’s not a declaration, JS engine will move to the global execution context with the help of scope chain and checks if a property with the name `a`exists in the global execution context object. If the property does not exist, it will create a new one and will initialize it. Here, as property with the name `a`already exists on the global execution context object, it will update its value to `3` from `1`. JS engine moves to global execution context in this case only i.e. when it finds a variable in the execution phase which is not a property on the current execution context object

**Line 11**: JS engines will create a `dFunc`property and will point to its heap location

**Execution context object of** `cFunc` **after the execution phase:**

**Line 15**: As this is a function call, JS engines will again enter the compilation phase to create `dFunc`execution context object.

`dFunc`execution context object has access to all the variables and functions defined on *cFunc*and in the global scope using the scope chain.

Similarly, `cFunc`has access to all the variables and objects in the global scope but it does not have any access to the `dFunc` variables and objects.

Global execution context does not have access to `cFunc`or `dFunc`variables or objects.

With the above concepts, I guess it will be easy to understand how **hoisting** works in JavaScript.

**Scope Chain**

The scope chain is a list of all the variable objects of functions inside which the current function exists. Scope chain also consists of the current function execution object.

Consider the below code:

Here, when function `cFunc`is called from the global execution context, the scope chain of `cFunc`will look like this

```
Scope chain of cFunc = [ cFunc variable object,   
                         Global Execution Context variable object]
```

When `dFunc`is called from `cFunc`, as `dFunc`is inside `cFunc`, `dFunc’s`scope chain consists of `dFunc` variable object, `cFunc`variable object and **global execution context** variable object.

```
Scope chain of dFunc = [dFunc variable object,   
                        cFunc variable object,  
                        Global execution context variable object]
```

When we try to access `f`inside `dFunc`, JS engine checks if `f` is available inside `dFunc’s`variable object. If it finds `f’s`value it `console.log` `f’s`value.

When we try to access variable `c` inside `dFunc`, JS engine checks if `c`is available inside `dFunc’s` variable object. If the variable is not available, then it will move to `cFunc` variable object.

As variable `c` is not available inside `dFunc’s`variable object, JS engines moves to `cFunc’s`variable object. As `c`is available on `cFunc`variable object, it will `console.log` `c’s`value.

When we try to log `a’s`value inside `dFunc`, JS engines will check if `a`is available inside `dFunc’s` variable object. If `a`is not available inside *dFunc’s*variable object, it will move to the next item in scope chain i.e. `cFunc’s` variable object. JS engines will check if `cFunc’s` variable object as variable `a`. Here, variable `a` is not available on `cFunc’s`variable object hence, it will check the next items in `dFunc’s` scope chain i.e. **global execution context** variable object. Here `a` is available on `dFunc’s`variable object and it will console `a’ s`value.

Similarly, in the case of *cFunc*, JS engine will find variable `a’s`value from global execution object.

`cFunc` does not know that variable `f` exists. Hence if we try to access `f`from `cFunc`it will give an error. But, `dFunc`function has access `c` and `d`variable using the scope chain

Closures can be explained using the scope chain context in JavaScript.

**If you like my articles and find them useful**, feel free to buy me a coffee. Thanks!

[![]()](https://www.buymeacoffee.com/rupeshmishra)

**To get updates for my new stories, follow me on** [**medium**](/@happymishra66) **and** [**twitter**](https://twitter.com/happyrupesh123)

**Other articles:**

1. [JavaScript Internals: JavaScript engine, Run-time environment & setTimeout Web API](https://blog.bitsrc.io/javascript-internals-javascript-engine-run-time-environment-settimeout-web-api-eeed263b1617)
2. [Understanding Web Share APIs](https://blog.bitsrc.io/understanding-web-share-apis-d987ea3648ad)
3. [Beginner’s guide to ReactJS](/free-code-camp/a-beginners-guide-to-getting-started-with-react-c7f34354279e)
4. [The Journey of JavaScript: from Downloading Scripts to Execution](/@amasand23/the-journey-of-javascript-from-downloading-scripts-to-execution-part-i-967cc1112b4f)
5. [Why Progressive Web Apps are great and how to build one](/free-code-camp/benefits-of-progressive-web-applications-pwas-and-how-to-build-one-a763e6424717)
6. [Let’s get this ‘this’ once and for all](https://hackernoon.com/lets-get-this-this-once-and-for-all-f59d76438d34)
7. [Service Workers](https://hackernoon.com/service-workers-62a7b14aa63a)
8. [Service Workers implementation](https://hackernoon.com/building-pokemon-app-to-evaluate-the-power-of-berries-service-worker-176d7c4e70e3)
9. [Virtual DOM in ReactJS](/@happymishra66/virtual-dom-in-reactjs-43a3fdb1d130)
10. [Prototypes in JavaScript](/@happymishra66/prototypes-in-javascript-5bba2990e04b)
11. [‘this’ in JavaScript](/@happymishra66/this-in-javascript-8e8d4cd3930)
12. [Object.create in JavaScript](/@happymishra66/object-create-in-javascript-fa8674df6ed2)
13. [Inheritance in JavaScript](/@happymishra66/inheritance-in-javascript-21d2b82ffa6f)
14. [Create objects in JavaScript](/@happymishra66/create-objects-in-javascript-10924cfa9fc7)
15. [Objects in JavaScript](/@happymishra66/objects-in-javascript-2980a15e9e71)
16. [Zip in Python](/@happymishra66/zip-in-python-48cb4f70d013)
17. [decorators in Python](/@happymishra66/decorators-in-python-8fd0dce93c08)
18. [Concatenating two lists in Python](/@happymishra66/concatenating-two-lists-in-python-3cf9051da17f)
19. [lambda, map and filter in Python](/@happymishra66/lambda-map-and-filter-in-python-4935f248593)
20. [List comprehensions in Python](/@happymishra66/list-comprehension-in-python-8895a785550b)