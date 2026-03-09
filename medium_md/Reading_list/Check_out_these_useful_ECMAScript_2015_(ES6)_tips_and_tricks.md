---
title: "Check out these useful ECMAScript 2015 (ES6) tips and tricks"
url: https://medium.com/p/6db105590377
---

# Check out these useful ECMAScript 2015 (ES6) tips and tricks

[Original](https://medium.com/p/6db105590377)

Member-only story

# Check out these useful ECMAScript 2015 (ES6) tips and tricks

[![rajaraodv](https://miro.medium.com/v2/resize:fill:64:64/1*HIuWP_7gy9QvnssCalFT4g.png)](/?source=post_page---byline--6db105590377---------------------------------------)

[rajaraodv](/?source=post_page---byline--6db105590377---------------------------------------)

8 min read

·

Mar 16, 2018

--

29

Listen

Share

More

Press enter or click to view image in full size

![]()

EcmaScript 2015 (aka ES6) has been around for couple of years now, and various new features can be used in clever ways. I wanted to list and discuss some of them, since I think you’ll find them useful.

If you know of other tips, please let me know in the comment and I’ll be happy to add them.

## 1. Enforcing required parameters

ES6 provides [default parameter values](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Default_parameters) that allow you to set some default value to be used if the function is called without that parameter.

In the following example, we are setting the `required()` function as the default value for both `a` and `b` parameters. This means that if either `a` or `b` is not passed, the `required()` function is called and you’ll get an error.

Press enter or click to view image in full size

![]()

```
const required = () => {throw new Error('Missing parameter')};//The below function will trow an error if either "a" or "b" is missing.  
const add = (a = required(), b = required()) => a + b;add(1, 2) //3  
add(1) // Error: Missing parameter.
```

## 2. The mighty “reduce”

Array’s r[educe](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce) method is extremely versatile. It is typically used to convert an array of items into a single value. **But you can do a lot more with it.**

> **🔥Tip: Most of these tricks rely on the initial value being an Array or an Object instead of a simple value like a string or a variable.**

**2.1 Using reduce to do both map and filter \*simultaneously\***

Suppose you have a situation where you have a list of items, and you want to update each item (that is, [map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map)) and then filter only a few items (that is, [filter](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter)). But this means that you would need to run through the list twice!

In the below example, we want to double the value of items in the array and then pick only those that are greater than 50. Notice how we can use the powerful reduce method to both double (map) and then filter? That’s pretty efficient.

Press enter or click to view image in full size

![]()

```
const numbers = [10, 20, 30, 40];const doubledOver50 = numbers.reduce((finalList, num) => {  
    
  num = num * 2; //double each number (i.e. map)  
    
  //filter number > 50  
  if (num > 50) {  
    finalList.push(num);  
  }  
  return finalList;  
}, []);doubledOver50; // [60, 80]
```

### 2.2 Using “reduce” instead of “map” or “filter”

If you look at the above example (from 2.1) carefully, you’ll know that reduce can be used to filter or map over items! **🔥**

### **2.3 Using reduce to balance** parentheses

Here’s another example of how versatile the reduce function is. Given a string with parentheses, we want to know if they are balanced, that is that there’s an equal number of “(“ and “)”, and if “(“ is before “)”.

We can easily do that in reduce as shown below. We simply hold a variable `counter` with starting value 0. We count up if we hit `(` and count down if we hit `)` . If they are balanced, then we should end up with `0`.

Press enter or click to view image in full size

![]()

```
//Returns 0 if balanced.  
const isParensBalanced = (str) => {  
  return str.split('').reduce((counter, char) => {  
    if(counter < 0) { //matched ")" before "("  
      return counter;  
    } else if(char === '(') {  
      return ++counter;  
    } else if(char === ')') {  
      return --counter;  
    }  else { //matched some other char  
      return counter;  
    }  
      
  }, 0); //<-- starting value of the counter  
}isParensBalanced('(())') // 0 <-- balanced  
isParensBalanced('(asdfds)') //0 <-- balancedisParensBalanced('(()') // 1 <-- not balanced  
isParensBalanced(')(') // -1 <-- not balanced
```

### 2.4 Counting Duplicate Array Items (Converting Array → Object)

There are times when you want to count duplicate array items or convert an array into an object. You can use reduce for that.

In the below example, we want to count how many cars of each type exist and put this figure into an object.

Press enter or click to view image in full size

![]()

```
var cars = ['BMW','Benz', 'Benz', 'Tesla', 'BMW', 'Toyota'];var carsObj = cars.reduce(function (obj, name) {   
   obj[name] = obj[name] ? ++obj[name] : 1;  
  return obj;  
}, {});carsObj; // => { BMW: 2, Benz: 2, Tesla: 1, Toyota: 1 }
```

There are plenty more things you can do using reduce, and I encourage you to read the examples listed on MDN [here](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/Reduce).

## **3. Object destructuring**

### 3.1 Removing unwanted properties

There are times when you want to remove unwanted properties — maybe because they contain sensitive info or are just too big. Instead of iterating over the whole object to removing them, we can simply extract such props to variables and keep the useful ones in the **\*rest\*** parameter.

In the below example, we want to remove `_internal` and `tooBig` properties. We can assign them to`_internal` and `tooBig` variables and store the remaining in a **\*rest\* parameter** `cleanObject` that we can use for later.

Press enter or click to view image in full size

![]()

```
let {_internal, tooBig, ...cleanObject} = {el1: '1', _internal:"secret", tooBig:{}, el2: '2', el3: '3'};console.log(cleanObject); // {el1: '1', el2: '2', el3: '3'}
```

### **3.2 Destructure nested objects in function params**

In the below example, the `engine` property is a nested-object of the `car` object. If we are interested in, say, the `vin` property of `engine`, we can easily destructure it as shown below.

Press enter or click to view image in full size

![]()

```
var car = {  
  model: 'bmw 2018',  
  engine: {  
    v6: true,  
    turbo: true,  
    vin: 12345  
  }  
}const modelAndVIN = ({model, engine: {vin}}) => {  
  console.log(`model: ${model} vin: ${vin}`);  
}modelAndVIN(car); // => model: bmw 2018  vin: 12345
```

### 3.3 Merge objects

ES6 comes with a spread operator (denoted by three dots). It is typically used to deconstruct array values, but you can use it on Objects as well.

In the following example, we use the spread operator to spread within a new object. Property keys in the 2nd object will override property keys in the 1st object.

In the below example, property keys `b and c` from `object2`override those from `object1`

Press enter or click to view image in full size

![]()

```
let object1 = { a:1, b:2,c:3 }  
let object2 = { b:30, c:40, d:50}  
let merged = {…object1, …object2} //spread and re-add into merged  
console.log(merged) // {a:1, b:30, c:40, d:50}
```

## 4. Sets

### 4.1 De-duping Arrays Using Sets

In ES6 you can easily de-dupe items using Sets, as Sets only allows unique values to be stored.

Press enter or click to view image in full size

![]()

```
let arr = [1, 1, 2, 2, 3, 3];  
let deduped = [...new Set(arr)] // [1, 2, 3]
```

### 4.2 Using Array methods

Converting Sets to an Array is as simple as using a spread operator (`…` ). You can use all the Array methods easily on Sets as well!

Let’s say we have a set as shown below and we want to `filter` it to only contain items greater than 3.

Press enter or click to view image in full size

![]()

```
let mySet = new Set([1,2, 3, 4, 5]);var filtered = [...mySet].filter((x) => x > 3) // [4, 5]
```

## 5. Array destructuring

Many times your function may return multiple values in an array. We can easily grab them by using Array destructuring.

### 5.1 Swap values

Press enter or click to view image in full size

![]()

```
let param1 = 1;  
let param2 = 2;//swap and assign param1 & param2 each others values  
[param1, param2] = [param2, param1];console.log(param1) // 2  
console.log(param2) // 1
```

### 5.2 Receive and assign multiple values from a function

In the below example, we are fetching a post at `/post` and related comments at `/comments` . Since we are using `async / await` , the function returns the result in an array. Using array destructuring, we can simply assign the result directly into corresponding variables.

Press enter or click to view image in full size

![]()

```
async function getFullPost(){  
  return await Promise.all([  
    fetch('/post'),  
    fetch('/comments')  
  ]);  
}const [post, comments] = getFullPost();
```

### If this was useful, please click the clap 👏 button down below a few times to show your support! ⬇⬇⬇ 🙏🏼

## My Other Posts

[*https://medium.com/@rajaraodv/latest*](https://medium.com/@rajaraodv/latest)

### ECMAScript 2015+

1. [*Examples of everything \*NEW\* in ECMAScript 2016, 2017, and 2018*](https://medium.freecodecamp.org/here-are-examples-of-everything-new-in-ecmascript-2016-2017-and-2018-d52fa3b5a70e)
2. [*Check out these useful ECMAScript 2015 (ES6) tips and tricks*](https://medium.freecodecamp.org/check-out-these-useful-ecmascript-2015-es6-tips-and-tricks-6db105590377)
3. [*5 JavaScript “Bad” Parts That Are Fixed In ES6*](https://medium.com/@rajaraodv/5-javascript-bad-parts-that-are-fixed-in-es6-c7c45d44fd81#.7e2s6cghy)
4. [*Is “Class” In ES6 The New “Bad” Part?*](https://medium.com/@rajaraodv/is-class-in-es6-the-new-bad-part-6c4e6fe1ee65#.4hqgpj2uv)

### Terminal Improvements

1. [*How to Jazz Up Your Terminal — A Step By Step Guide With Pictures*](https://medium.freecodecamp.org/jazz-up-your-bash-terminal-a-step-by-step-guide-with-pictures-80267554cb22)
2. [*Jazz Up Your “ZSH” Terminal In Seven Steps — A Visual Guide*](https://medium.freecodecamp.org/jazz-up-your-zsh-terminal-in-seven-steps-a-visual-guide-e81a8fd59a38)

### WWW

1. [*A Fascinating And Messy History Of The Web And JavaScript*](https://medium.freecodecamp.org/a-fascinating-and-messy-history-of-the-web-and-javascript-video-8978dc7bda75)

### Virtual DOM

1. [*Inner Workings Of The Virtual DOM*](https://medium.com/@rajaraodv/the-inner-workings-of-virtual-dom-666ee7ad47cf)

### React Performance

1. [*Two Quick Ways To Reduce React App’s Size In Production*](https://medium.com/@rajaraodv/two-quick-ways-to-reduce-react-apps-size-in-production-82226605771a#.6lepbl7ae)
2. [*Using Preact Instead Of React*](https://medium.com/@rajaraodv/using-preact-instead-of-react-70f40f53107c#.7fzp0lyo3)

### Functional Programming

1. [*JavaScript Is Turing Complete — Explained*](https://medium.com/@rajaraodv/javascript-is-turing-complete-explained-41a34287d263#.6t0b2w66p)
2. [*Functional Programming In JS — With Practical Examples (Part 1)*](https://medium.com/@rajaraodv/functional-programming-in-js-with-practical-examples-part-1-87c2b0dbc276#.fbgrmoa7g)
3. [*Functional Programming In JS — With Practical Examples (Part 2)*](https://medium.freecodecamp.org/functional-programming-in-js-with-practical-examples-part-2-429d2e8ccc9e)
4. [*Why Redux Need Reducers To Be “Pure Functions”*](https://medium.com/@rajaraodv/why-redux-needs-reducers-to-be-pure-functions-d438c58ae468#.bntrywxrf)

### WebPack

1. [*Webpack — The Confusing Parts*](https://medium.com/@rajaraodv/webpack-the-confusing-parts-58712f8fcad9#.6ot6deo2b)
2. [*Webpack & Hot Module Replacement [HMR]*](https://medium.com/@rajaraodv/webpack-hot-module-replacement-hmr-e756a726a07#.y667mx4lg) *(under-the-hood)*
3. [*Webpack’s HMR And React-Hot-Loader — The Missing Manual*](https://medium.com/@rajaraodv/webpacks-hmr-react-hot-loader-the-missing-manual-232336dc0d96#.fbb1e7ehl)

### Draft.js

1. [*Why Draft.js And Why You Should Contribute*](https://medium.com/@rajaraodv/why-draft-js-and-why-you-should-contribute-460c4a69e6c8#.jp1tsvsqc)
2. [*How Draft.js Represents Rich Text Data*](https://medium.com/@rajaraodv/how-draft-js-represents-rich-text-data-eeabb5f25cf2#.hh0ue85lo)

### React And Redux :

1. [*Step by Step Guide To Building React Redux Apps*](https://medium.com/@rajaraodv/step-by-step-guide-to-building-react-redux-apps-using-mocks-48ca0f47f9a#.s7zsgq3u1)
2. [*A Guide For Building A React Redux CRUD App*](https://medium.com/@rajaraodv/a-guide-for-building-a-react-redux-crud-app-7fe0b8943d0f#.g99gruhdz) *(3-page app)*
3. [*Using Middlewares In React Redux Apps*](https://medium.com/@rajaraodv/using-middlewares-in-react-redux-apps-f7c9652610c6#.oentrjqpj)
4. [*Adding A Robust Form Validation To React Redux Apps*](https://medium.com/@rajaraodv/adding-a-robust-form-validation-to-react-redux-apps-616ca240c124#.jq013tkr1)
5. [*Securing React Redux Apps With JWT Tokens*](https://medium.com/@rajaraodv/securing-react-redux-apps-with-jwt-tokens-fcfe81356ea0#.xci6o9s6w)
6. [*Handling Transactional Emails In React Redux Apps*](https://medium.com/@rajaraodv/handling-transactional-emails-in-react-redux-apps-8b1134748f76#.a24nenmnt)
7. [*The Anatomy Of A React Redux App*](https://medium.com/@rajaraodv/the-anatomy-of-a-react-redux-app-759282368c5a#.7wwjs8eqo)
8. [*Why Redux Need Reducers To Be “Pure Functions”*](https://medium.com/@rajaraodv/why-redux-needs-reducers-to-be-pure-functions-d438c58ae468#.bntrywxrf)
9. [*Two Quick Ways To Reduce React App’s Size In Production*](https://medium.com/@rajaraodv/two-quick-ways-to-reduce-react-apps-size-in-production-82226605771a#.6lepbl7ae)