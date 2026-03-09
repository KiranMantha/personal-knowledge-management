---
title: "The Proxy API Is So Powerful That Every Web Developer Should Master It!"
url: https://medium.com/p/9bdc71a4032c
---

# The Proxy API Is So Powerful That Every Web Developer Should Master It!

[Original](https://medium.com/p/9bdc71a4032c)

Member-only story

# The Proxy API Is So Powerful That Every Web Developer Should Master It!

## The 8 Major Usage Scenarios of the Proxy API That 80% of Web Developers Should Not Be Aware Of!

[![Bytefer](https://miro.medium.com/v2/resize:fill:64:64/1*krjVh9VFhDEcMUif4Ewt-A.png)](https://medium.com/@bytefer?source=post_page---byline--9bdc71a4032c---------------------------------------)

[Bytefer](https://medium.com/@bytefer?source=post_page---byline--9bdc71a4032c---------------------------------------)

7 min read

·

Oct 19, 2022

--

1

Listen

Share

More

Press enter or click to view image in full size

![]()

The [Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy) API is very powerful and very useful. **In this article, I will introduce its 8 usage scenarios**.

In daily work, I believe that many developers have used Web debugging proxy tools, such as Fiddler or Charles. By using the web debugging proxy tool, we can intercept HTTP/HTTPS protocol requests and manually modify request parameters and response results. Not only that, when debugging online problems, using the Web debugging proxy tool, **you can also map online compressed and obfuscated JavaScript files to local uncompressed and obfuscated JavaScript files**.

After a brief introduction to the basic functions of the Web Debugging Proxy Tool, let’s take a look at the HTTP request process using the Web Debugging Proxy Tool:

Press enter or click to view image in full size

![]()

As can be seen from the above figure, after using the Web proxy tool, the HTTP requests we initiate will be forwarded and processed through the Web Proxy. The addition of the Web Proxy proxy layer allows us to better control the flow of HTTP requests. For single-page applications, after getting data from the server, we will read the corresponding data and display it on the page:

Press enter or click to view image in full size

![]()

The above process is similar to the browser fetching data directly from the server:

Press enter or click to view image in full size

![]()

In order to be able to flexibly control the flow of HTTP requests, we have added a Web Proxy layer. So can we control the reading process of the data object? The answer is yes, we can use Web API like `Object.defineProperty` or `Proxy` API. After the introduction of Web API, the data access process is shown in the following figure:

Press enter or click to view image in full size

![]()

Next, I will focus on the `Proxy` API, which is the “hero” behind the Vue3 implementation of data reactive.

## 1. Introduction to Proxy Object

The `Proxy` object is used to create a proxy for an object, enabling interception and customization of basic operations (such as property lookup, assignment, enumeration, function invocation, etc.).

The constructor syntax for `Proxy` is:

```
const p = new Proxy(target, handler)
```

* `target`: the target object to wrap with Proxy (can be any type of object, including native arrays, functions, or even another proxy).
* `handler`: an object that defines which operations will be intercepted and how to redefine intercepted operations.

After introducing the Proxy constructor, let’s take a simple example:

```
const man = {  
  name: "Bytefer",  
};const proxy = new Proxy(man, {  
  get(target, property, receiver) {  
    console.log(`Accessing the ${property} property`);  
    return target[property];  
  },  
});console.log(proxy.name);  
console.log(proxy.age);
```

In the above example, we used the `Proxy` constructor to create a proxy object for the `man` object. **When creating the proxy object, we define a get trap to capture the property read operation.** The function of the trap is to intercept the user’s related operations on the target object. Before these operations are propagated to the target object, the corresponding trap function will be called first, thereby intercepting and modifying the corresponding behavior.

After the above code is successfully executed, the following result will be output:

```
Accessing the name property  
Bytefer  
Accessing the age property  
undefined
```

Based on the above output results, we can find that the get trap can intercept not only the read operation of known properties, but also the read operation of unknown properties. When creating a `Proxy` object, in addition to defining the get trap, we can also define other traps, such as `has`, `set`, `delete`, `apply` or `ownKeys`, etc.

The handler object supports 13 kinds of traps, here I only list the following 5 commonly used traps:

* `handler.get`: is a trap for getting a property value.
* `handler.set`: is a trap for setting a property value.
* `handler.has`: is a trap for the `in` operator.
* `handler.deleteProperty`: is a trap for the delete operator.
* `handler.ownKeys`: is a trap for `Reflect.ownKeys()`.

Note that all traps are optional. If no trap is defined, the default behavior of the source object is preserved. After reading the introduction of the traps above, do you think the `Proxy` API is very powerful?

## 2. Proxy API usage scenarios

### 2.1 Enhanced Array

In the above code, in addition to using the Proxy API, we also use the [Reflect](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Reflect) API. Once we have the `enhancedArray` function, we can use it like this:

```
const arr = enhancedArray([10, 6, 8, 5, 2]);console.log(arr[-1]); // 2  
console.log(arr[[2, 4]]); // [ 8, 2 ]  
console.log(arr[[2, -2, 1]]); // [ 8, 5, 6 ]  
console.log(arr["2:4"]); // [ 8, 5 ]  
console.log(arr["-2:3"]); // [ 5, 2, 10, 6, 8 ]
```

It can be seen from the above output results that the enhanced array object can support functions such as **negative index and fragment index**. In addition to enhancing arrays, we can also enhance plain objects using the `Proxy` API.

### 2.2 Enhanced Object

Once we have the `enhancedObject` function, we can use it like this:

```
const data = enhancedObject({  
  user: {  
    name: "Bytefer",  
    settings: {  
      theme: "light",  
    },  
  },  
});console.log(data.user.settings.theme); // light  
console.log(data.theme); // light  
console.log(data.address); // null
```

As can be seen from the above output results, we can easily access the deep properties inside the ordinary object by using the object processed by the `enhancedObject` function.

### 2.3 Freeze Object

After defining the freeze function, let’s test its functionality:

```
console.log(freezedMan.name); // Bytefer  
freezedMan.name = "Lolo";   
delete freezedMan.man;   
freezedMan.age = 30;  
console.log(freezedMan); // { name: 'Bytefer' }
```

### 2.4 Trace Method Call

With the `traceMethodCall` function, we can use it to trace the method call of the specified object:

```
const man = {  
  name: "Bytefer",  
  say(msg) {  
    return `${this.name} says: ${msg}`;  
  },  
};const tracedObj = traceMethodCall(man);  
tracedObj.say("Hello Proxy API");   
// Call say method -> "Bytefer says: Hello Proxy API"
```

In fact, in addition to being able to track method calls, we can also track access to properties in object.

### 2.5 Trace Property Access

With the `tracePropertyAccess` function, we can use it to trace the property access of the specified object:

```
const man = {  
  name: "Bytefer",  
};const tracedMan = tracePropertyAccess(man, ["name"]);console.log(tracedMan.name); // GET name; Bytefer  
console.log(tracedMan.age); // undefined  
tracedMan.name = "Lolo"; // SET name=Lolo
```

In the above example, we have defined a `tracePropertyAccess` function that receives two parameters: obj and propKeys, which represent the target to be traced and the list of properties to be traced, respectively. After calling the `tracePropertyAccess` function, a proxy object will be returned, and when we access the traced property, the console will output the corresponding access log.

### 2.6 Hide Property

With the `hideProperty` function, we can use it to hide properties starting with `_`(underscore):

```
const man = {  
  name: "Bytefer",  
  _pwd: "ProxyAPI",  
};const safeMan = hideProperty(man);console.log(safeMan._pwd); // undefined  
console.log("_pwd" in safeMan); // false  
console.log(Object.keys(safeMan)); // [ 'name' ]
```

### 2.7 Sandbox

For JavaScript, the sandbox is not a sandbox in the traditional sense, it is just a security mechanism to run some untrusted code in the sandbox, so that it cannot access code outside the sandbox.

With the `sandbox` function, let’s verify its capabilities:

```
const man = {  
  name: "Bytefer",  
  log() {  
    console.log("Hello Proxy API");  
  },  
};let code = "log();console.log(name)";  
sandbox(code)(man);
```

When running the above code in the browser, the console will throw the following error message:

Press enter or click to view image in full size

![]()

### 2.8 Builder

The builder pattern decomposes a complex object into relatively simple parts, then creates them separately according to different needs, and finally builds the complex object.

Using the `Proxy` API, we can implement a `Builder` function, so that the object wrapped by it supports the builder pattern to construct the object.

With the `Builder` function, let’s look at two ways it can be used. The first way is to handle ordinary object:

```
const defaultUserInfo = {  
  id: 1,  
  userName: "Bytefer",  
  email: "bytefer@gmail.com",  
};const bytefer = Builder(defaultUserInfo).id(2).build();  
console.log(bytefer);
```

The second way is to handle the class:

```
class User {  
  constructor() {}  
}const lolo = Builder(User, defaultUserInfo);  
console.log(lolo.id(3).userName("Lolo").build());
```

If you know other usage scenarios of Proxy API, you can leave me a message. If you want to learn TypeScript, then don’t miss the **Mastering TypeScript** series.

[## With 30+ Articles, You Will Not Be Confused When Learning TypeScript

### Through Vivid Animations, You Can Easily Understand the Difficult Points and Core Knowledge of TypeScript! Continuously…

medium.com](https://medium.com/frontend-canteen/with-these-articles-you-will-not-be-confused-when-learning-typescript-d96a5c99e229?source=post_page-----9bdc71a4032c---------------------------------------)

Follow me on [Medium](https://medium.com/@bytefer) or [Twitter](https://twitter.com/Tbytefer) to read more about TS and JS!

## Resources

[## Proxy - JavaScript | MDN

### The Proxy object allows you to create an object that can be used in place of the original object, but which may…

developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy?source=post_page-----9bdc71a4032c---------------------------------------)

*More content at* [***PlainEnglish.io***](https://plainenglish.io/)*. Sign up for our* [***free weekly newsletter***](http://newsletter.plainenglish.io/)*. Follow us on* [***Twitter***](https://twitter.com/inPlainEngHQ), [***LinkedIn***](https://www.linkedin.com/company/inplainenglish/)***,*** [***YouTube***](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw)***, and***[***Discord***](https://discord.gg/GtDtUAvyhW)***.*** *Interested in Growth Hacking? Check out* [***Circuit***](https://circuit.ooo/)***.***