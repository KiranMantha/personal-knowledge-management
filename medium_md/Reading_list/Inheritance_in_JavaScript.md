---
title: "Inheritance in JavaScript"
url: https://medium.com/p/21d2b82ffa6f
---

# Inheritance in JavaScript

[Original](https://medium.com/p/21d2b82ffa6f)

# Inheritance in JavaScript

[![Rupesh Mishra](https://miro.medium.com/v2/resize:fill:64:64/1*vkWAize3YPtA-vPkoQ06cA.jpeg)](/@happymishra66?source=post_page---byline--21d2b82ffa6f---------------------------------------)

[Rupesh Mishra](/@happymishra66?source=post_page---byline--21d2b82ffa6f---------------------------------------)

5 min read

·

May 4, 2017

--

10

Listen

Share

More

Detailed walk thorough of inheritance in JavaScript

Press enter or click to view image in full size

![]()

JavaScript does not have classes like other languages. It uses the concept of prototypes and prototype chaining for inheritance. In this post, we will discuss how we can achieve inheritance in JavaScript using Prototypes.

I recommend reading [this article](/@happymishra66/prototypes-in-javascript-5bba2990e04b) to have a thorough understanding of Prototypes in JavaScript.

**Prototype Chaining**

Prototype chaining means an object’s *dunder proto* or *proto* property will point to another object instead of pointing to the constructor function `prototype`. If the other object’s *dunder proto* or *proto* property points to another object it will result in the chain. This is called Prototype Chaining.

As shown in the below image, `SubType` object’s `prototype` property points to `SuperType` object. `SuperType` object’s `prototype` property points to the `SuperSuperType` object. This is called **prototype chaining**

Press enter or click to view image in full size

![]()

Let’s implement prototype chaining

Press enter or click to view image in full size

![]()

Above code defines two `constructor` functions, `SuperType` and `SubType`. By default, `SubType.prototype` has a `constructor`function which points to the `constructor` *function* itself and `proto` property which inherits the default object properties.

```
//Inherit the properties from SuperType  
SubType.prototype = new SuperType();
```

Above line rewrites the default prototype or the *dunder* proto property of the `SubType`constructor function and makes `SubType.prototype` to point to an object of `SuperType` constructor function.

This means that all the properties and methods that exist on an instance of `SuperType` will now exist on `SubType.prototype` *also.* This means that now, `SubType`function has access to all the `SuperType`properties and methods.

```
//Add new property to SubType prototype  
SubType.prototype.getSubAge = function(){  
	return this.age;  
}
```

After the default prototype of `SubType`constructor function has been overwritten, by using the above line of code we add a new method `getSubAge()` on top of what was inherited from `SuperType`, to the prototype object of `SubType`constructor function.

**Note**: New methods must be added to the `SubType`after the inheritance because inheritance overwrites the existing prototype of *SubType*

**Console output**

![]()

![]()

![]()

***Note***: `getSuperName()` method remains on the `SuperType.prototype` object, but name property ends up on `SubType.prototype`. That’s because `getSuperName()` is a prototype method, and the property is an instance property. `SubType.prototype` is now an instance of `SuperType`, so the property is stored there. Also note that `SubType.prototype.constructor`points to `SuperType`, because the constructor property on the `SubType.prototype` was overwritten.

### Problems with prototype chaining

As all the properties of the super type prototype are shared among the child objects, if one child modifies the property of the super type prototype, other children also get affected. This issue has been explained in great details [here](/@happymishra66/prototypes-in-javascript-5bba2990e04b)

To fix this issue, we use the constructor to inherit the instance properties and prototype chaining to inherit methods and share properties

Let’s try to understand the code, we have defined a `SuperType`constructor function with `firstName`, `lastName`*,* and `friends`as instance properties, then we have defined a `superName`property on the prototype of `SuperType`*.*

Now, let’s look at how we have defined the *SubType* constructor function

Here, we define a `SubType`constructor function. Inside the `SubType`constructor function, we call the `SuperType`constructor function with `call`. Call executes the `SuperType`constructor function in the context of the object being created using the `SubType`constructor function. After inheriting the instance properties of the `SuperType`, we add one `age`property to the `SubType`constructor function

```
//Inherit methods and shared properties  
SubType.prototype = new SuperType();
```

So far we have just inherited all the instance properties of the `SuperType`constructor function, but the shared properties and methods of the `SuperType`constructor function is still not inherited. We inherit them using the above lines of code.

Once the above lines of code are executed, we have inherited all the properties of the `SuperType`constructor function

When we execute the above line of code, all the three parameters (Virat, Kohli and 26) are passed to the `SubType`constructor function. `SubType`constructor function then calls `SuperType`constructor function using call `SuperType.call(this, firstname, lastName)` *this* here represent the `subTypeObj1`

`SuperType`constructor function is executed in the context of `subTypeObj1` and add properties `firstName, lastName, friends` to the `subTypeObj1` object After the return of `SuperType.call(this, firstname, lastName)`, `SubType`constructor function adds a `age` property to `subTypeObj1` object.

Thus as of now, there are properties with the `subTypeObj1` object (firstName, lastName, and age). Currently, `SubType`constructor function has the following methods and shared properties in its prototype property:

1. `getSuperName()`
2. `getSubAge`

`subTypeObj1` inherits all these properties from `SubType`constructor function.

Press enter or click to view image in full size

![]()

**If you like my articles and find them useful**, feel free to buy me a coffee. Thanks!

[![]()](https://www.buymeacoffee.com/rupeshmishra)

To get updates for my new stories, follow me on [medium](/@happymishra66) and [twitter](https://twitter.com/happyrupesh123)

**Other articles:**

1. [Understanding Web Share APIs](https://blog.bitsrc.io/understanding-web-share-apis-d987ea3648ad)
2. [Beginner’s guide to ReactJS](/free-code-camp/a-beginners-guide-to-getting-started-with-react-c7f34354279e)
3. [The Journey of JavaScript: from Downloading Scripts to Execution](/@amasand23/the-journey-of-javascript-from-downloading-scripts-to-execution-part-i-967cc1112b4f)
4. [Why Progressive Web Apps are great and how to build one](/free-code-camp/benefits-of-progressive-web-applications-pwas-and-how-to-build-one-a763e6424717)
5. [Let’s get this ‘this’ once and for all](https://hackernoon.com/lets-get-this-this-once-and-for-all-f59d76438d34)
6. [Service Workers](https://hackernoon.com/service-workers-62a7b14aa63a)
7. [Service Workers implementation](https://hackernoon.com/building-pokemon-app-to-evaluate-the-power-of-berries-service-worker-176d7c4e70e3)
8. [Execution Context in JavaScript](/@happymishra66/execution-context-in-javascript-319dd72e8e2c)
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