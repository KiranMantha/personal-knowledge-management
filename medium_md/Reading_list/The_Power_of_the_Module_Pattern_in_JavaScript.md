---
title: "The Power of the Module Pattern in JavaScript"
url: https://medium.com/p/3c73f7cd10e8
---

# The Power of the Module Pattern in JavaScript

[Original](https://medium.com/p/3c73f7cd10e8)

Member-only story

# The Power of the Module Pattern in JavaScript

## Embellish your app with the module pattern

[![jsmanifest](https://miro.medium.com/v2/resize:fill:64:64/2*hMSDnIbezH2uXPYk7tV2hA.jpeg)](/@jsmanifest?source=post_page---byline--3c73f7cd10e8---------------------------------------)

[jsmanifest](/@jsmanifest?source=post_page---byline--3c73f7cd10e8---------------------------------------)

6 min read

·

Nov 3, 2019

--

2

Listen

Share

More

Press enter or click to view image in full size

![]()

In JavaScript, a widely used and powerful pattern is the [Module Pattern](https://en.wikipedia.org/wiki/Module_pattern). It can be *incredibly* simple to implement, but the fact that it enables developers to encapsulate their code makes it one of the most versatile patterns to build robust code. When you look inside the source code of JavaScript libraries, you’re most likely looking at an implementation of this pattern — and they’re most likely a [singleton object](https://en.wikipedia.org/wiki/Singleton_pattern), meaning that only one instance exists throughout the lifetime of an app.

It may be difficult for newcomers in JavaScript to understand the module pattern as there are several variations that exist. However, it’s worth all the time and trouble because you’ll be using this pattern very often to make your app more robust.

## Modules

As you may have guessed, the module pattern lets you create modules. In the end, modules are basically just objects. But there are a couple of ways to create them.

The most basic way to create a module is to assign an object to a variable like so:

```
const myModule = {  
  drive() {  
    console.log('*drives*')  
  },  
}
```

A simple image representation:

Press enter or click to view image in full size

![]()

Things start to become more interesting when we utilize some of JavaScript’s unique features to create a module, which we’ll cover next.

## Immediately Invoked Function Expression

Arguably the most popular variation of the module pattern is the [IIFE](https://developer.mozilla.org/en-US/docs/Glossary/IIFE) (Immediately Invoked Function Expression). These are essentially functions that invoke immediately and return an object (or an interface, in other words), which then becomes the module.

Inside these functions is code that can be *private* in such ways that it would *only* be accessible *within* that function’s scope *unless* the returned object provides methods that can access them somehow. This returned object is public and available to the outside world.

Here’s an image representation of what this looks like, for those of you who are better at understanding things from a visual perspective:

Press enter or click to view image in full size

![]()

We’ll implement our own module using an IIFE. This allows us to assign the return value of an IIFE directly onto a variable so that we can use it just like a JavaScript module.

For example, let's pretend that we’re creating an RPG game, and the first thing we decide to do is create a *sorceress* class. In general roleplaying games, sorceresses are highly powerful beings that possess strong magical abilities like fire, wind, electricity, etc. They commonly possess telekinetic powers to pick up and move things around with just their minds. In just about every RPG game, sorceresses cast spells or magic, so we’ll keep this concept in context when we define the interface for the sorceress.

In this example, our sorceress class has four methods available to use from the outside world: `sorceress.fireBolt`, `sorceress.thunderBolt`, `sorceress.blizzard`, and `sorceress.castAll`.

Inside this module, we declared three *private* functions and four *public* functions. We can obviously tell that that the functions prefixed with underscores `_` are the private functions while the latter are public. We know this because the ones with the underscores aren't being returned — instead, some of them are just being used *by* the public methods. This concept of being able to reference local variables by [lexical scope](https://stackoverflow.com/questions/1047454/what-is-lexical-scope) is called *closure*. Because we didn’t return the variables prefixed by underscores, they’re not available outside of the module — but they *can be* if the returned methods chooses to make that happen.

Having the power to declare private and public variables this way is what makes the module pattern arguably the most powerful design pattern in JavaScript apps. The same pattern is essentially what’s being constantly used today when we `import` or `require` from node.js modules, as well as including `<script>` tags that point to a library like `jQuery`.

## Global Import

Uses of the module pattern in JavaScript isn’t limited to our previous code example. The module pattern in JavaScipt is powerful thanks to JavaScript’s flexibility. For example, JavaScript has a feature known as [implied globals](http://geniuscarrier.com/implied-globals/). If it’s used in an assignment, the global is created if it doesn’t already exist. So when we use or create global variables in anonymous closures, things can actually become easier to an extent.

Unfortunately, though, the resulting issue is that our code becomes harder to manage *over time* because it isn’t obvious to us which variables are global in a given file.

Luckily, anonymous functions provide an easy alternative. By passing in globals as parameters to our anonymous functions, they get imported into our code, which is both faster and clearer than implied globals.

Here’s a code example illustrating this concept:

```
const myModue = (function(_) {  
  // do stuff  
})(lodash)
```

As you can see, we now have access to lodash as part of the global variable. Here’s an image representing what this may look like now:

Press enter or click to view image in full size

![]()

## Why Modules in General?

In general, there are multiple benefits to using modules. Here are the most important:

### It helps you maintain your code better

By definition, a module is [self-contained](https://stackoverflow.com/questions/39133044/what-does-self-contained-mean) and shouldn’t rely on the outside world to survive. Updating a single module should be as easy as possible and shouldn’t break another part of the app when changed. A well-made module should be well-constructed and lessen the dependencies on parts of your code as much as possible so that they’re decoupled from other parts of your code.

If we take a look at our sorceress class in the previous code example, we can already assume that if we try to change one of the methods defined inside, debugging would end up becoming a stressful process if it proceeded to break other parts of the codebase. This is especially true if it creates a domino effect. Modules should be carefully designed in a way that any changes to them in the future don’t end up affecting other parts of the code.

### It helps us to avoid polluting the global namespace

In the JavaScript language, all variables located outside the scope of top-level functions are global. This means that other code can access them. This is problematic because it creates a situation called [*namespace pollution*](https://stackoverflow.com/questions/22903542/what-is-namespace-pollution), where any completely unrelated code shares variables in the global scope. This is something you want to avoid *at all times*.

### It helps us to reuse code

If you’ve been developing in JavaScript for a while, you’ve probably found yourself copying and pasting code to multiple projects. This is fine until you start realizing that you had written the code snippet using bad practices and decide to rewrite it using better practices. If you had copied and pasted the code to multiple projects, you’re faced with the boring, repetitive task of having to change every copy of the code. It would certainly be much easier to have a module that can be reused over and over so that you only need to update the module at one location. Then, consumers will automatically see the changes you made every time.

## Conclusion

And that concludes this post! I hope you found this to be valuable, and look out for more in the future!

Want to keep in touch? Subscribe to my [newsletter](https://app.getresponse.com/site2/javascript-newsletter?u=zpBtw&webforms_id=SM2hz).