---
title: "No More Confusion About TypeScript’s Type and Interface"
url: https://medium.com/p/63c39418ae35
---

# No More Confusion About TypeScript’s Type and Interface

[Original](https://medium.com/p/63c39418ae35)

Member-only story

# No More Confusion About TypeScript’s Type and Interface

## Explained with animations. Master the similarities and differences between Type and Interface, and understand their usage scenarios

[![Bytefer](https://miro.medium.com/v2/resize:fill:64:64/1*krjVh9VFhDEcMUif4Ewt-A.png)](https://medium.com/@bytefer?source=post_page---byline--63c39418ae35---------------------------------------)

[Bytefer](https://medium.com/@bytefer?source=post_page---byline--63c39418ae35---------------------------------------)

5 min read

·

Aug 16, 2022

--

3

Listen

Share

More

Press enter or click to view image in full size

![]()

Welcome to the **Mastering TypeScript** series. This series will introduce the core knowledge and techniques of TypeScript **in the form of animations**. Let’s learn together! Previous articles are as follows:

* [**What Are K, T, and V in TypeScript Generics?**](https://medium.com/frontend-canteen/what-are-k-t-and-v-in-typescript-generics-9fabe1d0f0f3)
* [**Using TypeScript Mapped Types Like a Pro**](/using-typescript-mapped-types-like-a-pro-be10aef5511a)
* [**Using TypeScript Conditional Types Like a Pro**](/use-typescript-conditional-types-like-a-pro-7baea0ad05c5)
* [**Using TypeScript Intersection Types Like a Pro**](/using-typescript-intersection-types-like-a-pro-a55da6a6a5f7)
* [**Using TypeScript infer Like a Pro**](https://levelup.gitconnected.com/using-typescript-infer-like-a-pro-f30ab8ab41c7)
* [**Using TypeScript Template Literal Types Like a Pro**](https://medium.com/javascript-in-plain-english/how-to-use-typescript-template-literal-types-like-a-pro-2e02a7db0bac)
* [**TypeScript Visualized: 15 Most Used Utility Types**](/15-utility-types-that-every-typescript-developer-should-know-6cf121d4047c)
* [**10 Things You Need To Know About TypeScript Classes**](https://levelup.gitconnected.com/10-things-you-need-to-know-about-typescript-classes-f58c57869266)
* [**The Purpose of ‘declare’ Keyword in TypeScript**](/purpose-of-declare-keyword-in-typescript-8431d9db2b10)
* [**How To Define Objects Type With Unknown Structures in TypeScript**](/how-to-define-objects-type-with-unknown-structures-in-typescript-c35e7b8462b0)

If you have written TypeScript on your resume, then the interviewer may ask you **what the difference is between type and interface.** Do you know how to answer this question? If you don’t know, you might understand after reading this article.

Type aliases can be used to give a type a new name, and are helpful when naming non-object types such as primitives or unions:

```
type MyNumber = number;  
type StringOrNumber = string | number;  
type Text = string | string[];  
type Point = [number, number];  
type Callback = (data: string) => void;
```

In TypeScript 1.6, type aliases began to support generic types. Utility types such as Partial, Required, Pick, Record, and Exclude which are commonly used in our work, are defined in terms of type alias.

Press enter or click to view image in full size

![]()

When defining object types, `interface`is usually used. App object in Vue 3 is defined using interface:

Press enter or click to view image in full size

![]()

As you can see from the above code, when defining an interface, we can declare both properties and methods on the object type. After understanding the role of type and interface, let’s introduce the similarities between them.

## Similarities

> Both type aliases and interface can be used to describe object or function types.

**type alias**

```
type Point = {  
  x: number;  
  y: number;  
};  
​  
type SetPoint = (x: number, y: number) => void;
```

In the above code, we use the type keyword to alias the object literal type and the function type respectively, so that these types can be used in other places.

**interface**

```
interface Point {  
  x: number;  
  y: number;  
}  
​  
interface SetPoint {  
  (x: number, y: number): void;  
}
```

> Both type aliases and interface can be extended

Type aliases are extended by `&`, while interfaces are extended by `extends`.

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

So can an interface extend the type defined by the type alias through extends? The answer is yes. Additionally, type aliases can also extend defined interface types via the **&** operator:

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Now that we know the similarities between type aliases and interfaces, let’s talk about the differences between them.

## Differences

1. Type aliases can define aliases for primitive types, union types, or tuple types, while interfaces cannot:

```
type MyNumber = number; // primitive type  
type StringOrNumber = string | number; // union type  
type Point = [number, number]; // tuple type
```

2. Interfaces with the same name are automatically merged(Declaration Merging), while type aliases are not:

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Using the feature of declaration merging, we can provide users with better security when developing third-party libraries. For example, the [webext-bridge](https://github.com/zikaari/webext-bridge) library uses interface to define the **ProtocolMap** interface, so that users can freely extend the **ProtocolMap** interface. After that, when using the onMessage function provided inside the library to monitor custom messages, we can infer the message body types corresponding to different messages.

**extends ProtocolMap interface**

```
import { ProtocolWithReturn } from 'webext-bridge'  
​  
declare module 'webext-bridge' {  
  export interface ProtocolMap {  
    foo: { title: string }  
    bar: ProtocolWithReturn<CustomDataType, CustomReturnType>  
  }  
}
```

**listen for custom messages**

```
import { onMessage } from 'webext-bridge'  
​  
onMessage('foo', ({ data }) => {  
  // type of `data` will be `{ title: string }`  
  console.log(data.title)  
}
```

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

If you’re interested, take a look at the type definition for onMessage in [webext-bridge](https://github.com/zikaari/webext-bridge). If you encounter problems, you can communicate with me. Finally, let’s summarize some usage scenarios for type aliases and interfaces.

**When to use** `type`

1. When defining aliases for primitive types, use `type`
2. When defining a tuple type, use `type`
3. When defining a function type, use `type`
4. When defining union types, use `type`
5. When defining the mapped types, use `type`

**When to use** `interface`

1. When you need to take advantage of the declaration merging feature, use `interface`
2. When defining an object type and no need to use type, use `interface`

After reading this article, I believe you already understand the difference between type alias and interface.

If you like to learn TypeScript in the form of animation, you can follow me on [Medium](https://medium.com/@bytefer) or [Twitter](https://twitter.com/Tbytefer) to read more about TS and JS!

## Resources

![Bytefer](https://miro.medium.com/v2/resize:fill:40:40/1*krjVh9VFhDEcMUif4Ewt-A.png)

[Bytefer](https://medium.com/@bytefer?source=post_page-----63c39418ae35---------------------------------------)

## Mastering TypeScript Series

[View list](https://medium.com/@bytefer/list/mastering-typescript-series-688ee7c12807?source=post_page-----63c39418ae35---------------------------------------)

63 stories

![](https://miro.medium.com/v2/da:true/resize:fill:388:388/0*XKfnkTao4t8Pi_-G)

![](https://miro.medium.com/v2/resize:fill:388:388/1*TA9YgJD1ueBDyHF9TsevoQ.jpeg)

![](https://miro.medium.com/v2/da:true/resize:fill:388:388/0*XKfnkTao4t8Pi_-G)

[## Interfaces vs Types in TypeScript

### For typescrpt version: 4.3.4 My personal convention, which I describe below, is this: When to use type: Use type when…

stackoverflow.com](https://stackoverflow.com/questions/37233735/interfaces-vs-types-in-typescript?source=post_page-----63c39418ae35---------------------------------------)

[## Documentation - Everyday Types

### In this chapter, we'll cover some of the most common types of values you'll find in JavaScript code, and explain the…

www.typescriptlang.org](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html?source=post_page-----63c39418ae35---------------------------------------#differences-between-type-aliases-and-interfaces)

*More content at* [***PlainEnglish.io***](https://plainenglish.io/)*. Sign up for our* [***free weekly newsletter***](http://newsletter.plainenglish.io/)*. Follow us on* [***Twitter***](https://twitter.com/inPlainEngHQ), [***LinkedIn***](https://www.linkedin.com/company/inplainenglish/)*,* [***YouTube***](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw)*, and* [***Discord***](https://discord.gg/GtDtUAvyhW)*.*