---
title: "A minimal guide to JavaScript (ECMAScript) Decorators and Property Descriptor of the Object"
url: https://medium.com/p/55b70338215e
---

# A minimal guide to JavaScript (ECMAScript) Decorators and Property Descriptor of the Object

[Original](https://medium.com/p/55b70338215e)

Member-only story

## JavaScript

# A minimal guide to JavaScript (ECMAScript) Decorators and Property Descriptor of the `Object`

## A short introduction of ECMAScript “decorators” proposal with basic examples and a little bit about the ECMAScript ecosystem.

[![Uday Hiwarale](https://miro.medium.com/v2/resize:fill:64:64/1*B4PQwnTacbDmtJgKYY7CzA.jpeg)](/@thatisuday?source=post_page---byline--55b70338215e---------------------------------------)

[Uday Hiwarale](/@thatisuday?source=post_page---byline--55b70338215e---------------------------------------)

13 min read

·

Jun 9, 2018

--

12

Listen

Share

More

> *⚠️* This article has been **revised** recently due to the change in the ECMAScript decorators proposal. You can read the **earlier** version of this article [**from here**](/jspoint/a-minimal-guide-to-javascript-ecmascript-decorators-and-property-descriptor-of-the-object-e19ce3f3ae).

Press enter or click to view image in full size

![]()

Why **ECMAScript Decorators** instead of **JavaScript Decorators** in the title? Because [**ECMAScript**](https://en.wikipedia.org/wiki/ECMAScript) is a standard for writing scripting languages like **JavaScript**. It doesn’t enforce JavaScript to support all the specs but a JavaScript engine (*implemented inside a browser*) may or may not support a feature introduced in ECMAScript or support with little different behavior.

Consider ECMAScript as a **language** that you speak such as ***English***. Then JavaScript would be a **dialect** like ***British English***. A dialect is a language in itself but it is based on principals of the language it was derived from. So, ECMAScript is a cookbook for cooking/writing JavaScript and it’s up to the chef/developer to follow all ingredients/rules or not.

Generally, JavaScript adopters (*such as web browsers or server-side platforms such as Node.js*) implement all the specifications written in the language (*else the whole point of having a standard crumbles*) and usually ship it with a beta-preview version to make sure if the implementation is stable.

**TC39** or Technical Committee 39 at **ECMA International** is responsible for maintaining the ECMAScript standard. Members of this team belong to ECMA International, browser vendors, and companies interested in the web industry in general such a Google, Mozilla, etc.

As ECMAScript is an open standard, anybody can suggest new ideas or features that would be a great addition to the language. Therefore, a proposal for a new feature goes through **4 main** stages and TC39 gets involved in this process until that feature is approved and included to the standard.

```
+-------+-----------+----------------------------------------+  
| stage | name      | mission                                |  
+-------+-----------+----------------------------------------+  
| 0     | strawman  | Present a new feature (proposal)       |  
|       |           | to TC39 committee. Generally presented |  
|       |           | by TC39 member or TC39 contributor.    |  
+-------+-----------+----------------------------------------+  
| 1     | proposal  | Define use cases for the proposal,     |  
|       |           | dependencies, challenges, demos,       |  
|       |           | polyfills etc. A champion              |  
|       |           | (TC39 member) will be                  |  
|       |           | responsible for this proposal.         |  
+-------+-----------+----------------------------------------+  
| 2     | draft     | This is the initial version of         |  
|       |           | the feature that will be               |  
|       |           | eventually added. Hence description    |  
|       |           | and syntax of feature should           |  
|       |           | be presented. A transpiler such as     |  
|       |           | Babel should support and               |  
|       |           | demonstrate implementation.            |  
+-------+-----------+----------------------------------------+  
| 3     | candidate | Proposal is almost ready and some      |  
|       |           | changes can be made in response to     |  
|       |           | critical issues raised by adopters     |  
|       |           |  and TC39 committee.                   |  
+-------+-----------+----------------------------------------+  
| 4     | finished  | The proposal is ready to be            |  
|       |           | included in the standard.              |  
+-------+-----------+----------------------------------------+
```

Right now (as of *June 2018*), **Decorators** are in [**stage 2**](https://github.com/tc39/proposal-decorators) and we have Babel plugin to transpile decorators `babel-plugin-transform-decorators-legacy`. In stage 2, as the syntax of the feature is subjected to change, it’s not recommended to use it in production as of now. In any case, decorators are beautiful and very useful to achieve things quicker.

From here on, we are working on a JavaScript feature that is still considered experimental by JavaScript engines, so your Node.js version might not support it. Therefore, we need **Babel** or **TypeScript** transpiler to convert decorator syntax into vanilla JavaScript syntax. Use the [**js-plugin-starter**](https://github.com/thatisuday/js-plugin-starter) plugin to set up a very basic project. I have configured this boilerplate to work well with what we are going to cover in this article.

To understand decorators, we need to first understand what is a **property descriptor** of a JavaScript object property. A **property descriptor** is a set of rules on an object property, like whether a property is **writable** or **enumerable**. Please follow the below lesson to read more about.

[## A quick introduction to the “Property Descriptor” of the JavaScript objects

### A JavaScript object, in a nutshell, is a data structure to hold key-value pairs. But unlike a simple map or dictionary…

medium.com](/jspoint/a-quick-introduction-to-the-property-descriptor-of-the-javascript-objects-5093c37d079?source=post_page-----55b70338215e---------------------------------------)

### ✱ Class Method Decorator

Now that we understood how we can define and configure new or existing properties of an object, let’s move our attention to decorators and why we discussed property descriptors at all.

A **decorator** is a JavaScript function (*recommended pure function*) that is used to modify class properties/methods or class itself. When you add `@decoratorFunction` syntax on the top of a **class property**, **method** or **class** itself, `decoratorFunction` **gets called** with few arguments **which we can use to modify class or class properties**.

As decorators are still in **Stage 2** of the ECMAScript proposal process, we can’t run any JavaScript code that contains decorators inside a browser or Node as this feature most probably isn’t implemented inside the JavaScript engine. For this purpose, we need to use a **transpiler** such as [**Babel**](https://babeljs.io/) or TypeScript that can compile JavaScript code containing decorators into something else that a JavaScript engine can understand.

We are going to use **Babel** for simplicity. You can follow [**this document**](https://babeljs.io/docs/en/babel-cli) to install Babel and CLI inside your project.

```
$ npm install --save-dev @babel/core @babel/cli$ npx babel --version  
7.10.4 (@babel/core 7.10.4)
```

With these commands, we have installed **Babel v7**. The `@babel/core` package contains the core implementation of Babel and `@babel/cli` package contains the command-line APIs to interface with it. You can follow [**this document**](https://babeljs.io/docs/en/babel-cli) to understand the command-line interface of `babel`.

```
$ npm install --save-dev @babel/preset-env  
$ npm install --save-dev @babel/plugin-proposal-decorators
```

The `@babel/preset-env` package is **preset** that contains standard babel **plugins**. A babel plugin performs the transformation of code that contain new JavaScript features such as ES6 [**arrow function expressions**](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions) into `function` declarations that can work across all browser.

A preset **configures and conducts** the compilation process using settings listed inside a configuration file such as `.babelrc` file. The `@babel/preset-env` contains plugins to transform standard JavaScript code containing features from **ES6** or above into ES5 or below.

When a proposal is in an early stage such as decorators in this example, it is may not be included in a **preset**. Therefore we need to install a **plugin** separately. Therefore we have installed the `@babel/plugin-proposal-decorators` plugin separately to compile decorators.

Now we need to tell the Babel CLI to use `@babel/preset-env` preset and `@babel/plugin-proposal-decorators` plugin. Let’s create a `babel.config.json` in the project directory. You can read more this file [**from here**](https://babeljs.io/docs/en/configuration).

```
{  
    "presets": [  
        "@babel/preset-env"  
    ],  
    "plugins": [  
        [  
            "@babel/plugin-proposal-decorators",  
            {  
                "decoratorsBeforeExport": true  
            }  
        ]  
    ]  
}
```

Press enter or click to view image in full size

![]()

In the above example, we have compiled a sample JavaScript file `babel-test.js` that contains ES6 features such as **arrow functions** and **template string literals**. As you can see, our babel setup is working fine. Now it’s time to move on to implementing decorators.

Let’s create a simple `readonly` decorator. But before that, let’s create simple `User` class with `getFullName` method which returns the full name of the user by combining `firstName` and `lastName`.

![]()

Above code prints `John Doe` to the console. But there is a huge problem, anybody can modify `getFullName` method.

![]()

To avoid public access to override any of our methods, we need to modify property descriptor of `getFullName` method which lives on `User.prototype` object. A class method is just a **property** with **function** value so the things are pretty similar to an object property.

![]()

Now, if any hacker tries to override `getFullName` method, the override operation will be simply ignored. In **strict mode**, this operation will result in an error as we saw in earlier example.

But if we have many methods on the `User` class, doing this manually won’t be so great. This is where decorator comes in. We can achieve the same thing by putting `@readonly` annotation on top of `getFullName` method as below.

![]()

Have a look at `readonly` fuction. A decorator is nothing but a function that is called when the JavaScript runtime encounters the decorator. The `target` argument value of this function is an object representation of the entity onto which the decorator was added, which is `getFullName` method in this case.

The `target` object is called **element** according to [**ECMAScript proposal**](https://tc39.es/proposal-decorators/) but we are going to call it to **target** for the heck of it. This `target` object contains the description of the element we are modifying. It could be a class method (*prototype property*), class field (*instance field*), or a class itself.

This `target` object looks like the following.

```
{  
  kind: 'method' | 'accessor' | 'field' | 'class',  
  key: '<property-name>',  
  descriptor: <property-descriptor>,  
  placement: 'prototype' | 'static' | 'own',  
  initializer: <function>,  
  ...  
}
```

The `kind` property indicates whether the element is a class **method**, class **field**, or something else while the `key` is the **name** of the element. You can read more about these properties from the [**decorators proposal**](https://tc39.es/proposal-decorators/) document. What we are interested in is the `descriptor` property. This is the actual property descriptor of the element.

Since we are decorating the `getFullName` method, the `descriptor` points to the property descriptor of `getFullName` method. A method of a class lives on its prototype and a prototype is an object. Therefore a method of the class is the property of its prototype and its value is a function.

From within a decorator function, we have to return the `target` object back at any cost. But before we do that, we can change the `descriptor` of the target. This `descriptor` will replace the existing property descriptor of that property. In the above example, we have made the `getFullName` property (*method*) readonly by setting `descriptor.writable` to `false`.

But when we tried to run this program with `node`, Node.js simply can’t recognize the `@readonly` syntax. That’s why we have set up Babel. Let’s compile this program using babel and then run it using Node.

![]()

Now when we compile the code with Babel and run the output file with Node, we get the expected error from runtime that the `getFillName` property is not something that you can write because it is read-only.

![]()

In the above example, we have logged the target object decorator is decorating. As we can see, the `kind` is `method` and `key` is the `getFullName` method name. The placement is `prototpe` since it lives on the prototype of the class and descriptor contains a function `value` among others.

There is another version of decorator annotation that goes like `@decorator( ...args )`. Here the `args` are the custom arguments passed to the decoration. Since this is a decorator **call**, the decorator function must **return a function** that decorates the target. This is also called the **decorator factory** since this function call returns an actual decorator.

![]()

When a class method is `static`, the method lives on the class itself instead on its `prototype`. Let’s add a static method to the `User` class.

![]()

In the above example, the `User` class has the `getVersion` method but since its property descriptor sets the `writable` to `true` by default, any intruder can override it. Let’s create the same old `@readonly` decorator.

![]()

Since the `target` object points to the method itself, nothing has changed between the instance method and static method. The only change in the `target` object is the `placement` which is not `static` since its a static method.

### ✱ Class Instance Property Decorator

So far, we have seen changing property descriptor of a method with `@decorator` or `@decorator(..args)` syntax, but what about **public/private properties** (*class instance fields*)?

```
// user.javaclass User {  
  String firstName = "John"; // class property  
  String lastName = "Doe"; // class propertyUser(String firstName, String lastName){  
    this.firstName = lastName;  
    this.firstName = lastName;  
  }  
}
```

Unlike Java (*or TypeScript*), JavaScript classes **do not have** support for class fields AKA **class properties** as shown in the above **Java** example. But there is a new [**proposal**](https://github.com/tc39/proposal-class-fields) to enable class properties with `public` and `private` access modifiers, which is now in [**stage 3**](https://github.com/tc39/proposals) and we have the `@babel/plugin-proposal-class-properties` plugin to compile it.

```
{  
    "presets": [  
        "@babel/preset-env"  
    ],  
    "plugins": [  
        [  
            "@babel/plugin-proposal-decorators",  
            {  
                "decoratorsBeforeExport": true  
            }  
        ],  
        [  
            "@babel/plugin-proposal-class-properties",  
            {  
                "loose": true  
            }  
        ]  
    ]  
}
```

After installing `@babel/plugin-proposal-class-properties` plugin with `npm install` command, our `babel.config.json` file should look like this.

Let’s define a simple `User` class but this time, we don’t need to set default values for `firstName` and `lastName` instance properties from within the constructor. We can do that on the class level itself.

![]()

![]()

Now, if you check `prototype` of `User` class, you won’t be able to see `firstName` and `lastName` properties. But also the `getFullName` method became the property of the instance since it was defined as a class property.

**Class instance fields** are a very helpful and important part of Object-Oriented Programming (**OOP**). You can completely remove the `constructor` function from the class and you would still have these properties on the instance with the default values.

However, there is a caveat. Unlike a class method that lives on the class prototype or a static method that lives on the class itself, a class property lives on the instance. That means if we want to decorate a class property, we need to do that while the instance is being created.

That being said, let’s modify our earlier example and create a simple `@upperCase` decorator that will change the case of the class instance properties default value.

![]()

While decorating a class property, things might look a little weird. This time, we have the `intializer` property on the `target` object which is a function that is called when an instance is being created of the `User` class. This function returns the initial value of the property.

We can override this function by assigning a new function to write a custom initializer of the property. We can call this function and retrieve the original initial value. We also have the `descriptor` object of the property on the target as usual so we can mess with that too.

This proposal also brings the **static properties** support for the class. In the below example, we have made all class properties static.

![]()

Since static properties live on the class, there won’t be any difference between a static method defined using normal static method form and the static class property form (*above*), therefore, `this` inside this method points to the `User` class. However, the `target` object has the `descriptor.value` in the former approach and `initializer` in later approach.

### ✱ Class Decorator

Now we are familiar with what decorators can do. They can change the properties and behavior of class methods and class fields (*static and instance*), giving us the flexibility to dynamically change the class behavior.

Decorators can also decorate classes. For example, if you want to dynamically add a method inside a class, you can do that using a decorator.

![]()

In the above example, we have added `getVersion` static method on the `User` class as well as the `getFullName` prototype method after the class was defined. We can achieve the same thing using a decorator. But first, let’s check the `target` value for a class element.

![]()

The `target` object while decorating a class looks a little different. Now the `target` object has the `kind` of class and the `elements` properties which are nothing but the potential targets (elements) of the class. At the moment, it has an element for the `getVersion` static method.

What we wanna do is to push a new target in the `elements` array. Let’s add an `element` that describes a prototype method.

![]()

In the above example, we have created the `add` decorator that takes a function and adds to the prototype of the class. We have achieved this by manually adding an element that describes the prototype method to the `elements` array of the class.

Decorators are amazing. You can **chain multiple decorators** together by placing them on top of each other. The order of execution will be the same as the order of their appearance.

Decorators are a fancy way to achieve things faster. But you may need to wait for some time before you could start implementing them until they are added to ECMAScript specifications.

Press enter or click to view image in full size

![]()

![]()