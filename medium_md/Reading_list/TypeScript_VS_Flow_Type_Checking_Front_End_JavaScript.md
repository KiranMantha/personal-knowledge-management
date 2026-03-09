---
title: "TypeScript VS Flow: Type Checking Front End JavaScript"
url: https://medium.com/p/abb2716b68e5
---

# TypeScript VS Flow: Type Checking Front End JavaScript

[Original](https://medium.com/p/abb2716b68e5)

# TypeScript VS Flow: Type Checking Front End JavaScript

## TypeScript VS Flow: Syntax, IDE support, framework support, and roadmaps.

[![Nathan Sebhastian](https://miro.medium.com/v2/resize:fill:64:64/1*lNCvmVYcU9IPwP0IQZ2dFw.png)](https://nsebhastian.medium.com/?source=post_page---byline--abb2716b68e5---------------------------------------)

[Nathan Sebhastian](https://nsebhastian.medium.com/?source=post_page---byline--abb2716b68e5---------------------------------------)

6 min read

·

Apr 29, 2020

--

3

Listen

Share

More

Press enter or click to view image in full size

![]()

JavaScript is a dynamically typed programming language. It means that the variables that you write in JavaScript can be reassigned with a value of different data type after it has been initialized.

```
let x = 8 // this variable is a number  
x = "Eight" // but I can assign a string into it as well
```

In a language that is statically typed like Java, you need to define the type of a variable, and that variable can’t be reassigned to a value of another type down the line. Java will throw an error when you try it:

```
int x = 8; // this is a Java variable  
x = "Eight"; // Nope. It will throw an error
```

At first, dynamic typing seems like a great feature for developers. After all, isn’t it nice to have a language that can accommodate data type change at runtime? Sadly, no. Being able to change values data type dynamically leads to unpredictable behavior and can cause bugs in your code.

As of this writing, an explicit data type is an important part of software requirements because web applications tend to consume a lot of APIs. To interact with these APIs effectively, you need to have explicitly defined rules. If an API expects a string, then the requested data being sent must be a string.

Moreover, it has become increasingly common for frontend teams to publish, document and organize their frontend components in cloud component hubs like [**Bit.dev**](https://bit.dev). This is done to make reusable components discoverable and available for all repositories, future and present.

[![]()](https://bit.dev)

For [reusable components](https://bit.dev) to be simple to use and maintain by others, you need static typing. Read more about it here:

[## 9 Tips for Building Awesome Reusable React Components

### Tips for building reusable and shareable React components.

blog.bitsrc.io](/9-tips-for-building-awesome-reusable-react-components-b91f4846a30a?source=post_page-----abb2716b68e5---------------------------------------)

To help make JavaScript more predictable, you need a static type checker that can help you define the data type for your variables. Currently, the most popular type checking libraries are Typescript, which is backed by Microsoft, and Flow, developed by Facebook.

As of this writing, TypeScript is clearly the more popular choice with over two million NPM packages that have registered dependency on it compared to Flow’s sixty-six thousand packages. Which one of these libraries should you use for your next project? Let’s find out.

## Installation and declaring variables

We’ll start by installing both libraries and then write a simple statically typed variable. First, we will install TypeScript:

```
npm install -g typescript
```

Then write an `index.ts` file and declare a variable. This variable will be of number type, but we’ll assign it to a string:

```
let price :number = "7"
```

Let’s run this file by using `tsc` command from the terminal:

```
tsc index.ts
```

The terminal will log the following error:

```
index.ts:1:5 - error TS2322: Type '"7"' is not assignable to type 'number'.
```

Alright, we’ve just finished getting started with TypeScript. Now let’s see how we do the same with Flow. First, install its dependencies into our project:

```
npm install --save-dev flow-bin
```

Then, we need to add Flow command into our `package.json` file. Here’s an example:

```
{  
  "name": "ts-vs-flow",  
  "version": "1.0.0",  
  "description": "",  
  "main": "index.js",  
  "scripts": {  
    "flow": "flow"  
  },  
  "devDependencies": {  
    "flow-bin": "^0.123.0"  
  }  
}
```

For the first time, we need to run `flow init` :

```
npm run flow init
```

With this, Flow is ready to check our JavaScript files for type errors. Let’s write a new `index.js` file and test it:

```
// @flow  
let price :number = "7"
```

The comment `// @flow` is used to tell Flow to check on the file. Any `.js` file without the comment will be ignored by the library. Finally, we can run the `flow` command:

```
npm run flow
```

Just like TypeScript, Flow will log an error into the terminal:

```
Cannot assign "7" to price because string [1] is incompatible with number [2].
```

I have to say that I prefer Typescript’s use `.ts` file extension over Flow’s `//@flow` in the comment. The use of the comment feels odd to me.

## Simple syntax comparison

After a few hours of research, I found that most type annotation syntax in both libraries are identical. For example, here is how both annotate function parameters:

```
function sum(x: number, y: number): number {  
  return(x+y)  
}sum(3, 5)
```

In the code above, both parameters were declared as number types, as well as the return value of the function. Here’s another example on annotating an object:

```
let myObject: {  
  foo: string,  
  bar: number,  
  baz: boolean  
}myObject = {  
  foo: "foo",  
  bar: 8,  
  baz: true  
}
```

Both TypeScript and Flow will compile your code into standard JavaScript code. But Flow also supports type commenting as the syntax, so that you don’t need to compile your JavaScript file for production:

```
function myMethod(value /*: string */) /*: number */ {  
  return value  
}myMethod("spoon")
```

You can try to run the code above with both `npm run flow` and `node index.js`. Flow will log an error while NodeJS will run without an error.

Alright, now we know that both libraries had an identical syntax. Let’s move on to compare IDE support.

## IDE support

Both TypeScript and Flow support popular IDEs for building JavaScript applications like VSCode, Atom, SublimeText, Vim, and WebStorm. I’m going to compare the support for VSCode since it’s currently the most popular editor for JavaScript.

VSCode provides first-class support for TypeScript, and it recognizes that you’re writing a TS code without any additional plugin (which is perfectly natural, since both are developed by Microsoft)

Press enter or click to view image in full size

![]()

In order to make VSCode recognize Flow syntax, you need to install [Flow Language Support](https://marketplace.visualstudio.com/items?itemName=flowtype.flow-for-vscode) for VSCode. You may also want to disable TypeScript support from VSCode so that it won’t give TypeScript error in your flow file.

Press enter or click to view image in full size

![]()

## Framework support

Popular frameworks like Angular, Vue, Electron and Nuxt fully support TypeScript for development. By contrast, you need to integrate Flow manually into many popular frameworks, except React which supports Flow by default.

![]()

So unless you’re using React, you need to setup Babel correctly to use Flow with other libraries.

## Library roadmap and release

TypeScript has a clear and [open roadmap](https://github.com/Microsoft/TypeScript/wiki/Roadmap) where its users can look and know what to expect in the future. It also follows the semantic versioning guide for its release. At the time of this writing, TypeScript is on version 3.9 RC.

On the other hand, Flow has no public roadmap and release its update incrementally. It currently is on version 0.123.0.

Maybe it’s just me, but I prefer not to use package below version 1 where I can.

## Conclusion

Lots of things about development and code comes down to preferences, but when it comes to type checker for JavaScript, it’s hard to pick Flow over TypeScript.

Although both are backed by a big tech company and have similar type checking syntax, TypeScript has great support from popular JavaScript frameworks and has a clear development roadmap so that you know what to expect in the future.

## Learn More

[## React TypeScript: Basics and Best Practices

### An updated handbook/cheat sheet for working with React.js with TypeScript.

blog.bitsrc.io](/react-typescript-cheetsheet-2b6fa2cecfe2?source=post_page-----abb2716b68e5---------------------------------------)

[## Gradually using TypeScript in Your React Project

### How to safely build and introduce React TypeScript components into your React JS project

blog.bitsrc.io](/react-js-to-typescript-how-to-migrate-gradually-d82026126d29?source=post_page-----abb2716b68e5---------------------------------------)

[## 9 Tips for Building Awesome Reusable React Components

### Tips for building reusable and shareable React components.

blog.bitsrc.io](/9-tips-for-building-awesome-reusable-react-components-b91f4846a30a?source=post_page-----abb2716b68e5---------------------------------------)