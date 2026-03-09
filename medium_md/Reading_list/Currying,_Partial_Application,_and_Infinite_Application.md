---
title: "Currying, Partial Application, and Infinite Application"
url: https://medium.com/p/73d16bb3d7a9
---

# Currying, Partial Application, and Infinite Application

[Original](https://medium.com/p/73d16bb3d7a9)

# Currying, Partial Application, and Infinite Application

[![Alexander Nied](https://miro.medium.com/v2/resize:fill:64:64/1*HI2vkR69iC0l5SqkP56ChA.png)](/?source=post_page---byline--73d16bb3d7a9---------------------------------------)

[Alexander Nied](/?source=post_page---byline--73d16bb3d7a9---------------------------------------)

10 min read

·

Jan 11, 2019

--

3

Listen

Share

More

![]()

Although my primary programming language is a functional one (JavaScript), I still occasionally find myself getting my head spun around by functional design patterns. When functions are a first-class citizen, the bag of tricks available to a developer can get a bit mind bending at times.

One place I frequently used to get confused was the difference between “currying” and “partial application.” Given the number of blog posts explaining this, I can see I am not the only one.

We’ll attempt here to explore these concepts in JavaScript, and look at how we could create a utility function to simplify currying and partial application.

### Arity

To understand currying and partial application, it is helpful to understand a concept called “[arity](https://en.wikipedia.org/wiki/Arity).” This sounds like a hardcore CS term, but it is essentially just a fancy word for describing the number of arguments a function or operator accepts — functions accepting more arguments have a higher arity, and functions accepting less arguments have lower arity. For instance, take the below function as an example:

```
function add(a, b) {  
    return a + b;  
}
```

We could describe `add` as having an arity of two (although we would more likely use a conventional shorthand and call it a “[binary function](https://en.wikipedia.org/wiki/Arity#Examples).”)

### Currying

Press enter or click to view image in full size

![]()

So, simply put, currying is the process of taking a function with arity greater than one and expressing it as a sequence of functions of single arity. Put even more plainly (but less succinctly), it is the process of taking a function that accepts multiple arguments and expressing it as a function that takes a single argument and then returns a new function that takes a single argument, which itself returns a function that accepts a single argument, all the way down until you are out of arguments. So, to reuse our `add` example, we could take the original function:

```
function add(a, b) {  
    return a + b;  
}
```

And rewrite it like this:

```
function curriedAdd(a) {  
    return function (b) {  
        return a + b;  
    }  
}
```

We would call `add` as `add(3, 5)` to get `8` returned. We could call `curriedAdd` as `curriedAdd(3)(5)` and get the same result. In the original `add`, both args are passed in a single call to the function and are immediately evaluated and the result returned. In `curriedAdd` we pass the value for `a` first, and get a function back that accepts `b`, then evaluates the result against `a` (which is held in a closure).

The above example is a bit simplistic with only two arguments — let’s look at another example with four arguments. Take the below function `playChord`, leveraging an imaginary `Piano` object:

```
function playChord(root, third, fifth, seventh) {  
     Piano.play(root, third, fifth, seventh);  
}
```

We could use the same technique as we used above for `add` to curry this function:

```
function curriedPlayChord(root) {  
    return function (third) {  
        return function (fifth) {  
            return function (seventh) {  
                Piano.play(root, third, fifth, seventh);  
            }  
        }  
    }  
}
```

You may be thinking that this approach does not scale well. You are correct. Luckily, this isn’t the only way to curry a function; we’ll explore another option later in the article.

### Partial Application

Why would we want to curry a function? Well it turns out that there are various contexts in which doing so might be a helpful pattern. One such pattern is partial application.

Partial application is a pattern in which a function with arity greater than one is expressed as a sequence of functions of lower arity. If this sounds familiar, it is because it is very close to the definition of currying! The primary technical difference is that we don’t specify that we are restricted to unary functions (functions with arity of one) when we are using a partial application pattern.

So why/how would this be useful? Let’s contrive an example. Imagine we are building a web application that handles employee management for client companies. We have a function called `getEmployee` that requires a company code, department code, and employee code in order to get information about an employee:

```
function getEmployee(companyCode, deptCode, employeeCode) {  
    const employee = lookup({  
        company: companyCode,  
        department: deptCode,  
        employee: employeeCode  
    )};  
    return employee;  
}
```

*(For simplicity’s sake, we will be pretending that* `lookup` *is completely synchronous in our example* `getEmployee`*.)*

This is relatively straightforward. Now, pretend that we have been tasked with building out boutique sites for several departments within several companies. For example, we will be making a site for SodaCo’s Marketing Division, for FoodCo’s Food Safety Division, for Weyland Industries’ R&D Division, etc. For each of these we will be making several requests for employees in the code for this portion of the site. We *know* that each of those requests will be using the same `companyCode` and `deptCode`. We *could* keep making the request the same way, over and over, with the same two arguments repeated every time. However, this might be a good opportunity to *partially apply* the function to avoid the need of passing the same args over and over. Perhaps we create the following service:

```
import getEmployee from './getEmployee';export default function GetEmployeeFetcher(companyCode, deptCode) {  
    return function (employeeCode) {  
        return getEmployee(companyCode, deptCode, employeeCode);  
    }  
}
```

So, if we were building the site for Weyland Industries’ Manufacturing, we could get a reusable function for getting only the salient employees like this:

```
import GetEmployeeFetcher from './GetEmployeeFetcher';const getWeylandManufacturingEmployee = GetEmployeeFetcher('WEY', 'MANUFACTURING');getWeylandManufacturingEmployee('EMP123');
```

By partially applying the function and fixing the first two arguments, we are left with a reusable function into which we only need to pass the employee number. Note that we didn’t need to curry to do this — we were able to apply the first two arguments in one pass. However, when we curry a function, we get partial application for free, because we can pass one argument at a time.

### tl;dr Review

Before we go further, let’s recap the terms we’ve covered:

**Arity**: A word that describes the quantity of arguments going to a function. A function accepting one argument has arity of one, a function accepting two arguments has arity of two, etc.

**Currying:** The expression of a function as a sequence of unaries that each return the next unary in the sequence until the last one, at which point it executes the body of the original function.

**Partial Application:** A pattern in which a function accepts some subset of its arguments and returns a function that accepts the remaining arguments. One way to accomplish this is by currying.

## Infinite Application

Press enter or click to view image in full size

![]()

### …For Discrete Arguments

So we see that when we curry a function we have, because of the definition of currying, provided ourselves with the ability to partially apply a function to our heart’s content. This is awesome. However, the currying technique we explored in our functions leaves a lot to be desired. While this technique could be used to curry any function of binary arity or greater, we can see that it scales linearly, so that every additional argument means writing an additional nested returned function. What would be preferable would be a utility that can curry any function without the need for manual repetition. Even better if the function could take variable numbers of arguments.

How could we accomplish this? Well, let’s look at an example implementation below:

```
function curryifier(fn, ...initialArgs) {    const cachedArgs = [...initialArgs];    const curryifierWrappedFunction = function () {  
        if (arguments.length === 0) {  
            return fn.apply(null, cachedArgs);  
        }  
        cachedArgs.push(...arguments);  
        return curryifierWrappedFunction;  
    };    return curryifierWrappedFunction;  
}
```

There’s a few things going on in the above JavaScript utility. The first argument to `curryifier` is the function we wish to curry. Following that, we leverage the [rest parameter syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/rest_parameters) to allow us to represent an indefinite number of arguments to be partially applied. If any are passed, they are cached in the `cachedArgs` `const` that will hold all passed args until we apply them to the original function.

What is returned from this initial call is a new “currified” version of the original function. The new function leverages the special `arguments` object — if any arguments at all are passed, they are pushed into `cachedArgs` and the “currified” function returns itself — this enables call chaining. If the “currified” function is called with *no* arguments, the original function will be called using every argument stored in `cachedArgs` by leveraging `apply`.

So, consider the below function `speak` :

```
function speak(fname, lname, line) {  
    return `${fname}${lname ? ` ${lname}` : ''}: "${line}"`;  
}
```

Below are a few examples of the various ways that speak could be called:

```
// with single argument partial applications  
let wrappedSpeak = currifier(speak);  
wrappedSpeak('Peter');  
wrappedSpeak('Venkman');  
wrappedSpeak('What do you see?');  
wrappedSpeak(); // returns "Peter Venkman: "What do you see?""// with variable argument partial application  
wrappedSpeak = currifier(speak);  
wrappedSpeak('Ray', 'Stantz');  
wrappedSpeak('This place is great!');  
wrappedSpeak(); //returns "Ray Stanz: "This place is great!""// leveraging the chained function return   
const wrappedSpeak = currifier(speak);  
// returns "Egon Spengler: "Don't cross the streams.""  
wrappedSpeak('Egon')('Spengler')('Don\'t cross the streams.')();// presetting args on initial wrapping call  
const wrappedSpeak = currifier(speak, 'Winston', 'Zeddemore');  
wrappedSpeak('Tell him about the Twinkie.');  
wrappedSpeak(); // returns "Winston Zeddemore: "Tell him about the Twinkie."
```

This is a big improvement over the approach we were using for currying previously. It can accept functions of any arity and it can also apply arguments at a variable amount.

### …For A Config Object Argument

This standard implementation of partial application still has some shortcomings. The biggest one is that the order is fixed; we couldn’t partially apply the `line` or `lname` arguments to our `speak` function using this approach. We also don’t have any recourse for a scenario in which we want to change the value of an argument we’ve already partially applied.

These aren’t huge problems, but I was interested in trying to create some solution that could mitigate them. What if we had a function that accepted a configuration object as an argument in lieu of discrete args (a pattern made more popular since ES6+ with [destructuring](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment))? This would allow us to accept config objects with some subset of the total set of properties, and simply extend the new object into the cache using `Object.assign`. Consider the example implementation below:

```
function infiniteApplication(fn, ...initialArgs) {    const cachedArgs = Object.assign({}, ...initialArgs);    const infiniteApplicationWrappedFunction = function () {  
        if (arguments.length === 0) {  
            return fn.call(null, cachedArgs);  
        }  
        Object.assign(cachedArgs, ...arguments);  
        return infiniteApplicationWrappedFunction;  
    };    return infiniteApplicationWrappedFunction;  
}
```

At a glance, this looks very similar to our previous implementation for discrete args. The primary difference is that rather than pushing into an array, we are now `assign`[ing](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/assign) into an object. When it comes time to execute the original function, we use the function method `call` instead of `apply` to avoid having to wrap our object in an array.

With this new form of our currifying utility, we can now partially apply our arguments in any order, and even override previous values for partially applied arguments. Consider an implementation of `speak` leveraging a config object for arguments:

```
function speak({fname, lname, line}) {  
    return `${fname}${lname ? ` ${lname}` : ''}: "${line}"`;  
}
```

Using our new config object-based function signature and partial application utility we have more flexible ways in which to partially apply `speak`:

```
// out of order  
let wrappedSpeak = infiniteApplication(speak);  
wrappedSpeak({line: "I am The Keymaster!"});  
wrappedSpeak({fname: "Louis", lname: "Tully"});  
wrappedSpeak(); // returns "Louis Tully: "I am The Keymaster!""// overriding/revising previously assigned partially applied args  
const wrappedSpeak = infiniteApplication(speak, {  
    fname: 'Dana',  
    lname: 'Barrett'  
});  
wrappedSpeak({fname: 'The GateKeeper'});  
wrappedSpeak({lname: undefined});  
wrappedSpeak('I am The GateKeeper!');  
wrappedSpeak(); // returns "The GateKeeper: "I am The Gatekeeper!""
```

### Combined

Ideally, we would have a single utility that could handle both of the above cases, and also do a little light validation on inputs. Below is my attempt at this:

```
function infiniteApplication(fn, useConfigForArgs, ...initialArgs) {    if (typeof fn !== 'function') {  
        throw new Error('infiniteApplication expects to be called with a function as the first argument.');  
    }    if (typeof useConfigForArgs === 'undefined') {  
        useConfigForArgs = false;  
    }    if (typeof useConfigForArgs !== 'boolean') {  
        throw new Error('infiniteApplication expects that a second argument, if present, be a boolean.');  
    }    let cachedArgs;  
    if (useConfigForArgs) {  
        cachedArgs = Object.assign({}, ...initialArgs);  
    } else {  
        cachedArgs = [...initialArgs];  
    }    const infiniteApplicationWrappedFunction = function () {  
        if (arguments.length === 0) {  
            if (useConfigForArgs) {  
                return fn.call(null, cachedArgs);  
            } else {  
                return fn.apply(null, cachedArgs);  
            }  
        }        if (useConfigForArgs) {  
            for (const arg of arguments) {  
                if(typeof arg !== 'object' || arg === null) {  
                    throw new Error('infiniteApplication expects objects as subsequent args when using `useConfigForArgs` mode');  
                }  
            }  
            Object.assign(cachedArgs, ...arguments);  
        } else {  
            cachedArgs.push(...arguments);  
        }        return infiniteApplicationWrappedFunction;  
    };    return infiniteApplicationWrappedFunction;  
}
```

[The above is available on my GitHub as](https://github.com/anied/infiniteApplication) `infiniteApplication` (version 0.3.0 at the time of this article). It is a bit less naive as to the potential inputs it may receive, and will `throw` if it receives a bad argument. The biggest compromise is that it requires a flag to be passed to indicate whether the passed function will be using discrete args or a single configuration argument. This isn’t particularly elegant, but there is unfortunately no good way to detect the signature of a function. We could possibly leverage `function.length`, but we would have to make some specific assumptions about what those arguments were that could prove problematic. If we wanted to be cute about it, we could write `infiniteApplication` to use a config object instead of discrete arguments, and then pass it to itself to partially apply the `useConfigForArgs` flag; it didn’t seem worth the trade-off when I first wrote it, but perhaps that would be a worthwhile adjustment.

Please do note that none of this is new — several utilities exist to curry input functions. [Lodash](https://lodash.com) even has a `curry` method that will curry an input function and a `curryRight` method to do the same but reverse the order of arguments in the resulting curried function. And I wouldn’t be surprised to discover others had come upon the same conclusion around a variant of partial application using an object rather than discrete arguments. However, hopefully this article has been informative on the topics of arity, currying, and partial application, and provided you with some code to play with in exploring these concepts further. Please feel free to fork `infiniteApplication` and mess around with it. I’d be interested in any feedback as to what about the implementation works, doesn’t work, could be improved, etc. Thanks for reading, and happy coding!