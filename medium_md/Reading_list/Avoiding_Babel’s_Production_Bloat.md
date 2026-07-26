---
title: "Avoiding Babel’s Production Bloat"
url: https://medium.com/p/d53eea2e1cbf
---

# Avoiding Babel’s Production Bloat

[Original](https://medium.com/p/d53eea2e1cbf)

# Avoiding Babel’s Production Bloat

[![Andrea Giammarchi](https://miro.medium.com/v2/resize:fill:64:64/1*54OyE6rg-MdELwb9mW56Xw.png)](/?source=post_page---byline--d53eea2e1cbf---------------------------------------)

[Andrea Giammarchi](/?source=post_page---byline--d53eea2e1cbf---------------------------------------)

8 min read

·

Jan 26, 2019

--

7

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dd53eea2e1cbf&operation=register&redirect=https%3A%2F%2Fwebreflection.medium.com%2Favoiding-babels-production-bloat-d53eea2e1cbf&source=---header_actions--d53eea2e1cbf---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

I once wrote `typeof any`, a **6** chars operator followed by a **3** chars reference, to realize that [**translated into 424 uncompressed bytes**](https://babeljs.io/repl#?babili=false&browsers=&build=&builtIns=false&spec=false&loose=false&code_lz=C4TwDgpg9gZgBAQwHYgNxA&debug=false&forceAllTransforms=false&shippedProposals=false&circleciRepo=&evaluate=false&fileSize=false&timeTravel=false&sourceType=module&lineWrap=true&presets=es2015&prettier=false&targets=&version=7.2.2&envVersion=):

```
"use strict";function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }typeof any === "undefined" ? "undefined" : _typeof(any);
```

By no mean this post goal is to discourage you from using the mighty [**Babel 7**](https://babeljs.io) though, which is by far **the best transpiler out there**. One would be crazy today to trust anything else, including TypeScript, which I start calling *TypeSeppuku*, and not for its `.d.ts` files, just for its resulting code.

This post is about the sometime inevitable bloat transpilers bring in, explaining the why, the what, and the how to avoid such bloat, when possible.

### The Three Kinds Of Bloat

To simplify the topic, let’s try to understand what kind of bloat we have:

* the **real *syntax sugar*** bloat, which has the smallest footprint in terms of bloated code, providing simple, safe, and fast fallbacks for older engines
* the ***recycled fix*** bloat, which has the `typeof` kind of bloat, the first time it’s needed, but it’ll be recycled for every other used`typeof`
* the **inline *syntax polyfill*** bloat, which is the worst of all kind, ’cause it cannot be optimized in any way and it will bloat your code each time

Every part of JS can be more or less transpiled with one of these kinds, either as single case, or mixed up cases, where ***recycled polyfills*** are **also an option**.

Shall we start with the scariest kind, so that we can have some sort of mild happy ending after all? 😅

## The Syntax Polyfill Hell

You can [check it live directly](https://babeljs.io/repl#?babili=false&browsers=&build=&builtIns=false&spec=false&loose=false&code_lz=GYewTgBAFAxiB2BnALhAbgQwDYFcCmEIwEWAligJQDcQA&debug=false&forceAllTransforms=false&shippedProposals=false&circleciRepo=&evaluate=false&fileSize=false&timeTravel=false&sourceType=module&lineWrap=true&presets=es2015&prettier=false&targets=&version=7.2.2&envVersion=), or simply trust me on this, the ***for/of*** operator is a curse for any project that needs to transpile it:

```
for (const value of list);
```

Accordingly with Closure Compiler Service, [the result](https://closure-compiler.appspot.com/home#code%3D%252F%252F%2520%253D%253DClosureCompiler%253D%253D%250A%252F%252F%2520%2540output_file_name%2520default.js%250A%252F%252F%2520%2540compilation_level%2520SIMPLE_OPTIMIZATIONS%250A%252F%252F%2520%253D%253D%252FClosureCompiler%253D%253D%250A%250A%250A%250A%2522use%2520strict%2522%253B%250A%250Avar%2520_iteratorNormalCompletion%2520%253D%2520true%253B%250Avar%2520_didIteratorError%2520%253D%2520false%253B%250Avar%2520_iteratorError%2520%253D%2520undefined%253B%250A%250Atry%2520%257B%250A%2520%2520for%2520(var%2520_iterator%2520%253D%2520list%255BSymbol.iterator%255D()%252C%2520_step%253B%2520!(_iteratorNormalCompletion%2520%253D%2520(_step%2520%253D%2520_iterator.next()).done)%253B%2520_iteratorNormalCompletion%2520%253D%2520true)%2520%257B%250A%2520%2520%2520%2520var%2520value%2520%253D%2520_step.value%253B%250A%2520%2520%2520%2520%253B%250A%2520%2520%257D%250A%257D%2520catch%2520(err)%2520%257B%250A%2520%2520_didIteratorError%2520%253D%2520true%253B%250A%2520%2520_iteratorError%2520%253D%2520err%253B%250A%257D%2520finally%2520%257B%250A%2520%2520try%2520%257B%250A%2520%2520%2520%2520if%2520(!_iteratorNormalCompletion%2520%2526%2526%2520_iterator.return%2520!%253D%2520null)%2520%257B%250A%2520%2520%2520%2520%2520%2520_iterator.return()%253B%250A%2520%2520%2520%2520%257D%250A%2520%2520%257D%2520finally%2520%257B%250A%2520%2520%2520%2520if%2520(_didIteratorError)%2520%257B%250A%2520%2520%2520%2520%2520%2520throw%2520_iteratorError%253B%250A%2520%2520%2520%2520%257D%250A%2520%2520%257D%250A%257D) is **2.18KB of code** for doing basically “*nothing*”.

And the worst part of it, is that the more you copy and paste that loop, the more the bloat grows.

You cannot even blame Babel for this, because `for/of` is one of those parts of recent specifications that simplifies gazillion tasks so that Babel, if unaware of the kind of `list` is dealing with, has to try all the options: is it an *Array*? is it *Iterable*? is it a *generator*?

Not only this could be true even for engines that support natively `for/of`, but if I were you, whenever you need to loop over an array, arguments object, static list, or something with an index and a finite `length`, I strongly suggest you to don’t use `for/of` in the wild.

### About the …rest

Another funny, inevitable, bloated transformation is `...rest` parameters:

```
function rest(...args) {  
  return args;  
}
```

Becoming minumum twice their size every time these are used. But not only above function is basically the equivalent of just:

```
function rest() { return arguments; }
```

The performance penalty you pay looping every time over `arguments` can be relevant, when you invoke functions gazillion times per second, and each function is transpiled as such:

```
function rest() {  
  for (var  
    _len = arguments.length,  
    args = new Array(_len),  
    _key = 0;  
    _key < _len; _key++  
  ) {  
    args[_key] = arguments[_key];  
  }  
  return args;  
}
```

Now, maybe we don’t all know that `arguments` is a special object that might leak into memory, which is the reason transpilers might do this array transformation dance, but any linter rule that forces avoiding arguments, in favor of `...rest`, is actually a dumb rule if the code will get transpiled.

### Generating\* Bloat

Generators are another inline polyfill fix, mixed up with some recycling, but basically the following:

```
function* blow() {}
```

becomes [some unusable code](https://babeljs.io/repl#?babili=false&browsers=&build=&builtIns=false&spec=false&loose=false&code_lz=GYVwdgxgLglg9mABAKgEYBs4HcAUBKRAbwF8g&debug=false&forceAllTransforms=false&shippedProposals=false&circleciRepo=&evaluate=false&fileSize=false&timeTravel=false&sourceType=module&lineWrap=true&presets=es2015&prettier=false&targets=&version=7.2.2&envVersion=) that will make sense only if applied properly.

Add a `yield` and a `for/of`, and [be surprised by other 2.18 extra KBs](https://babeljs.io/repl#?babili=false&browsers=&build=&builtIns=false&spec=false&loose=false&code_lz=GYVwdgxgLglg9mABAKgEYBs4HcAUBKRAbwChFEBPGAU3QBNEBtAXQG5iBfY44OAJ0RwQEAZyiIAbgEN0IKojjBEGbPjxsgA&debug=false&forceAllTransforms=false&shippedProposals=false&circleciRepo=&evaluate=false&fileSize=false&timeTravel=false&sourceType=module&lineWrap=true&presets=es2015&prettier=false&targets=&version=7.2.2&envVersion=)!

### Destructuring Arrays

Another lovely, and inevitable, code bloat is generated by array destructuring:

```
const [a, b] = unknown;
```

[That alone might scare you](https://babeljs.io/repl#?babili=false&browsers=&build=&builtIns=false&spec=false&loose=false&code_lz=MYewdgzgLgBA2gQwDQwEYF0YF4YFcwDWYIA7mANxA&debug=false&forceAllTransforms=false&shippedProposals=false&circleciRepo=&evaluate=false&fileSize=false&timeTravel=false&sourceType=module&lineWrap=true&presets=es2015&prettier=false&targets=&version=7.2.2&envVersion=), but at least here there’s some recycled part of the transpiler that most likely will be reused elsewhere.

Indeed, adding something like `function ab([a, b]){}` after, won’t blow up the final code size any further, it will just reuse the same helpers.

However, there is a better destructuring than array, as example using an object as single parameter:

```
function ab({a = 1, b = 2}) { return [a, b]; }
```

or abusing the `arguments` object:

```
function ab() {  
  const {0: a = 1, 1: b = 2} = arguments;  
  return [a, b];  
}
```

where both approaches will produce way smaller outcome than:

```
function ab(a = 1, b = 2) { return [a, b]; }
```

which is [another little monster](https://babeljs.io/repl#?babili=false&browsers=&build=&builtIns=false&spec=false&loose=false&code_lz=GYVwdgxgLglg9mABAQwEYApmILyIIwA0iqOiATAJSIDeiATgKZQh1IDayRqAugNyIBfAFBA&debug=false&forceAllTransforms=false&shippedProposals=false&circleciRepo=&evaluate=false&fileSize=false&timeTravel=false&sourceType=module&lineWrap=true&presets=es2015&prettier=false&targets=&version=7.2.2&envVersion=) in terms of bloated size.

## An Absurd Class

Press enter or click to view image in full size

![]()

I cannot be the only one that consciously prefer the good old function way to declare small classes, right?

```
function Small() {}  
// or  
class Small {}  
// ?
```

Well, I let you judge the difference, where using `class` [results into 298 uncompressed bytes](https://babeljs.io/repl#?babili=false&browsers=&build=&builtIns=false&spec=false&loose=false&code_lz=MYGwhgzhAEDKC2YQmgbwL5A&debug=false&forceAllTransforms=false&shippedProposals=false&circleciRepo=&evaluate=false&fileSize=false&timeTravel=false&sourceType=module&lineWrap=true&presets=es2015%2Creact%2Cstage-2&prettier=false&targets=&version=7.2.2&envVersion=) through the closure compiler, something actually irrelevant if we consider 1.49K needed to represent a single `extends`.

```
// 1.49K (almost 10x than ...)  
class B extends class A {} {}// 156 bytes uncompressed  
function extend(a, b) {  
  const sPO = Object.setPrototypeOf;  
  if (typeof a === 'function')  
    sPO(a.prototype, b.prototype);  
  return sPO(a, b);  
}function A() {}  
const B = extend(function B() {}, A);
```

Add recent private fields in the mix, and reach 1.75KB with ease:

```
class Top {  
  #pvt1 = 123;  
}class Sub extends Top {  
  #pvt2 = 123;  
}
```

where `Sub` will initialize each instance like …

```
var Sub = function (_Top) {  
  // extend  
  _inherits(Sub, _Top);  
  // the class  
  function Sub() {  
    var _getPrototypeOf2;  
    var _this;  
    // with instance check  
    _classCallCheck(this, Sub);  
    // possible arguments (avoiding leaks)  
    for (var _len = arguments.length,  
             args = new Array(_len) ... ) {  
      args[_key] = arguments[_key];  
    }  
    // possible different return from the super  
    _this = _possibleConstructorReturn(this, ...);  
    // private field  
    _pvt.set(  
      _assertThisInitialized(  
        _assertThisInitialized(_this)), {  
          writable: true,  
          value: 123  
        }  
      );  
    // the current context  
    return _this;  
  }  
  // the current class  
  return Sub;  
}(Top);  
// and its `pvt` private field  
var _pvt = new WeakMap();
```

Now imagine if it was you writing such logic per each class, instead of simply defining a `function` within a module and its private `WeakMap` for some private reference, as in the following case:

```
const _ = new WeakMap;function GoodOldES3() {'use strict';  
  _.set(this, {any: 'value'});  
}GoodOldES3.prototype.getAny = function getAny() {  
  return _.get(this).any;  
};
```

* the runtime check for `this` is implied by the `use strict` guard
* the code is **already compatible with IE11** ’cause IE11 supports WeakMap
* there is absolutely no extra cost in initializing a `GoodOldES3` instance
* no code outside that module can reach private fields
* zero production bloat 🎉

### … the instanceof curse anyway …

Incapable of knowing upfront if an instance comes from a class that used some modern alchemy to trick the engine, `instanceof` would be another keyword to avoid when possible, ’cause it’ll bring in:

```
function _instanceof(left, right) {  
  if (  
    right != null &&  
    typeof Symbol !== "undefined" &&  
    right[Symbol.hasInstance]  
  ) {  
    return right[Symbol.hasInstance](left);  
  } else {  
    return left instanceof right;  
  }  
}
```

which is yet another recycled bloat, but one that could slow down one of the fastest checks of the JS world, second only to `typeof`.

## OK Then … What Is Safe ?

I’ve sneaked in already most common recycled bloat in previous examples, but it’s time to see what doesn’t really affect the final production code size.

### Arrows and Methods are just fine

```
const o = {  
  // shortcut  
  method() {},  
  // arrows without this / arguments  
  contextless: () => {}  
};// even with this / arguments  
const arrow = () => [this, arguments];
```

### and so are template literals

These are rightly translated to follow latest ECMAScript standard, and even if bigger than their native counterpart, and [somehow slower to interact with](https://docs.google.com/document/d/1X6zO5F_Zojizn2dmo_ftaOWsY8NltPHUhudBbUzMxnc/preview), these are just fine ’cause these play well with minifiers and compressors.

```
tag`blown`;  
tag`blown`;  
function same() {  
  tag`blown`;  
}
```

Be aware that **these are not safe in TypeScript** if you target IE11, or old environments, and these are **different in Babel 6 too**.

… but I said already that Babel 7 is the only transpiler you should use, right?

### destructuring objects? all good!

```
const {a, b} = object;
```

which [translates in a super sweet way](https://babeljs.io/repl#?babili=false&browsers=&build=&builtIns=false&spec=false&loose=false&code_lz=MYewdgzgLgBA3gQwDQwEYF8YF4YlQKwFNgoBuAKCA&debug=false&forceAllTransforms=false&shippedProposals=false&circleciRepo=&evaluate=true&fileSize=false&timeTravel=false&sourceType=module&lineWrap=true&presets=es2015%2Creact%2Cstage-2&prettier=false&targets=&version=7.2.2&envVersion=).

### Not arrays though !

Beside bringing a lot of boilerplate for something this short:

```
const [a, b] = array;  
const a = [...b];
```

specially the spreading one makes no sense when it comes to methods:

```
// 520 bytes uncompressed  
arr.push(...values);// VS 38 bytes uncompressed  
arr.push.apply(arr, values);
```

I don’t think we always need to be that lazy, right?

## How To Avoid The Bloat

Press enter or click to view image in full size

![]()

There are various ways to accomplish this, and the most obvious one is: do not target ES5 or IE11 unless it’s strictly necessary.

The “*how to do that?*” part has been already extensively covered in my previous “[*A Bloatless Web*](https://itnext.io/a-bloatless-web-d4f811c7991b)” post, where all it takes is just to adjust your targets or produce multiple bundles and distribute only what’s necessary.

It’s. Deadly. Simple.

However, there are other ways to avoid some bloat ending up in your production code, and here just few of the various solutions.

### Exclude Specific Helpers

If you are using `typeof`, as example, and your are not needing, or using it, to ever deal with `Symbol`, another hard to polyfill and trust variable in the modern specifications, you can exclude that right away.

```
["@babel/preset-env", {  
  "exclude": ["transform-typeof-symbol"]  
}]
```

The `transform-instanceof` is probably not needed in Babel 7, but please double check there’s no undesired transformation, usually already the case if the class is already known.

### Brute Force Exclusion

If you deal with third parts modules that might have already been transpiled, you can also use something like [drop-babel-typeof](https://github.com/WebReflection/drop-babel-typeof) utility.

Just install it as dev-dependency, and run it as production hook.

## … and what about classes ?

Well, there have been alternatives to modern classes declaration for decades now, but the tricky part is when you need to extend builtins.

In that case, if you are targeting ES5, or IE11, your code will be broken, end of the story; you can already start targeting ES6/2015 ’cause until now you never had IE11 users or you’d be drawn by filed bugs and issues.

However, if you are shipping to third parts, and you are worried about class bloat, I can still suggest my good old [Classtrophobic](https://github.com/WebReflection/classtrophobic#classtrophobic--) work around, and its [ES5 compatible](https://github.com/WebReflection/classtrophobic-es5#classtrophobic-es5--) counter part.

If you are curious to know more about Classtrophobic, [here my previous post](https://medium.com/@WebReflection/a-case-for-js-classes-without-classes-9e60b3b5992).

### Finally: Use Common Sense!

New syntax is cool, but if it gets transpiled, users, browsers, and ultimately you, won’t ever benefit from any new feature, slowing down instead, and for no reason, also increasing production code size.

Whenever you can choose a specific pattern, and you are still targeting legacy browsers, choose wisely if it makes sense to use modern syntax penalizing all modern browsers, and slowing down the already, legacy, slow one.

Last, but not least, **keep an eye on your transpiled code before it gets minified**, and try to figure out if there’s some unnecessary bloat brought in by feaatures you are not even using in your production code.

You now know how to work around, exclude, or deal with it 👋