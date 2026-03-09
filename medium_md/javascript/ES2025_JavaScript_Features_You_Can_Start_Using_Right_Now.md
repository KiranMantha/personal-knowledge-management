---
title: "ES2025 JavaScript Features You Can Start Using Right Now"
url: https://medium.com/p/fed3784298b4
---

# ES2025 JavaScript Features You Can Start Using Right Now

[Original](https://medium.com/p/fed3784298b4)

Member-only story

# ES2025 JavaScript Features You Can Start Using Right Now

[![Kevin - MERN Stack Developer](https://miro.medium.com/v2/resize:fill:64:64/1*aUGBohBB1VAnsoGAdjEZoQ.png)](/@mernstackdevbykevin?source=post_page---byline--fed3784298b4---------------------------------------)

[Kevin - MERN Stack Developer](/@mernstackdevbykevin?source=post_page---byline--fed3784298b4---------------------------------------)

3 min read

·

Oct 4, 2025

--

Listen

Share

More

The TC39 proposals that graduated to Stage 4 are already shipping in browsers **— here’s what changes how you write JavaScript today.**

Press enter or click to view image in full size

![Code editor with ES2025 JavaScript badge and colorful syntax highlighting on dark futuristic background]()

JavaScript would not wait for January 1 to become better. Notice: React updates while you were building React apps and optimizing Next. ES2025 features slipped in the chrome and Firefox and Node finally land js bundles. js — and they are about to redefine how do you implement some of the most common patterns in your codebase.

These aren’t theoretical proposals. They’re here to ship, tested, and replace the workarounds you’ve been copy-pasting for years.

## Array Grouping: Finally Built-In

How many times did you find yourself reaching for Lodash `groupBy`? Not anymore:

```
const products = [  
  { name: 'Laptop', category: 'electronics', price: 999 },  
  { name: 'Desk', category: 'furniture', price: 299 },  
  { name: 'Phone', category: 'electronics', price: 699 },  
  { name: 'Chair', category: 'furniture', price: 199 }  
];  
  
// The old way  
const grouped = products.reduce((acc, item) => {  
  (acc[item.category] = acc[item.category] || []).push(item);  
  return acc;  
}, {});  
  
// ES2025 way  
const grouped = Object.groupBy(products, item => item.category);  
// Result: { electronics: [...], furniture: [...] }
```

**Supported browsers**: Chrome 117+, Firefox 119+, Safari 17+, Node js 21+

This works with `Map.groupBy()` as well when keys are not strings. Zero dependencies, no polyfills in modern environments

## Promise. withResolvers: Cleaner Async Control

Making promises with externally defined resolve/reject functions once required this clunky pattern:

```
// The old way  
let resolve, reject;  
const promise = new Promise((res, rej) => {  
  resolve = res;  
  reject = rej;  
});  
  
// ES2025 way  
const { promise, resolve, reject } = Promise.withResolvers();  
  
// Perfect for event-driven flows  
function waitForWebSocket(ws) {  
  const { promise, resolve, reject } = Promise.withResolvers();  
    
  ws.addEventListener('open', resolve);  
  ws.addEventListener('error', reject);  
    
  return promise;  
}
```

This pattern is present all over in any TypeScript codebases that you would encounter if they are working with some event emitter, message queues or any kind of async coordination which is not following the traditional Promise constructor pattern.

**Implemented in** Chrome 119+, Firefox 121+, Safari 17.4+, Node. js 22+

## RegEx with Duplicate Named Capture Groups

Keep Reading Regular expressions got a little bit easier to maintain Capture group names got a little more powerful in that you can now reuse them across alternations:

```
// Extract dates in multiple formats  
const dateRegex = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})|(?<month>\d{2})\/(?<day>\d{2})\/(?<year>\d{4})/;  
  
const match1 = '2025-03-15'.match(dateRegex);  
const match2 = '03/15/2025'.match(dateRegex);  
  
console.log(match1.groups); // { year: '2025', month: '03', day: '15' }  
console.log(match2.groups); // { year: '2025', month: '03', day: '15' }
```

You’d have to use different group names for each format, which is overkill given ES2025 has not been released.

**Cross-browser test**: Chrome 125+, Firefox 130+, Safari 18+

## What Does This Imply About Your Stack

If you are using **next.js or React. js** to build, these features integrate seamlessly:

* Use `Object.groupBy()` in Redux selectors instead of importing Lodash
* Replace custom promise utilities in TypeScript with `Promise.withResolvers`
* Simplify form validation regex patterns with duplicate named groups

With 67% of developers targeting evergreen browsers as per the State of JavaScript 2024 survey, these features are ready for the production use.

## Start Using Them Now

To type this properly add this to your TypeScript config:

```
{  
  "compilerOptions": {  
    "lib": ["ES2025", "DOM"]  
  }  
}
```

These are already handled by Babel for older browser support via `@babel/preset-env` and a proper `browserslist` config.

The development of JavaScript is not a big bang, it is a gradual, quiet, and practical evolution that has layered itself for decades. ES2025 won’t change your architecture but will clean up your code, make it more readable and reduce reliance on utility functions that should’ve been native long ago.

The features are here. Your browsers support them. Enough of writing JavaScript as if it is 2020.