---
title: "Dynamic Conditional Types in TypeScript"
url: https://medium.com/p/ebaa00b04a09
---

# Dynamic Conditional Types in TypeScript

[Original](https://medium.com/p/ebaa00b04a09)

# Dynamic Conditional Types in TypeScript

## Explained with Examples

[![Mayur Koshti](https://miro.medium.com/v2/resize:fill:64:64/1*9e3EfvMp0pXPx7mnzk0AKg.jpeg)](https://medium.com/@mayurkoshti12?source=post_page---byline--ebaa00b04a09---------------------------------------)

[Mayur Koshti](https://medium.com/@mayurkoshti12?source=post_page---byline--ebaa00b04a09---------------------------------------)

5 min read

·

Feb 5, 2025

--

Listen

Share

More

Press enter or click to view image in full size

![Dynamic Conditional Types in TypeScript Explained with Examples]()

> TypeScript is a powerful tool for building robust and scalable JavaScript applications, and one of its most impressive features is its ability to handle conditional types dynamically.

Conditional types allow you to add logic to your types, enabling TypeScript to select the right type based on specific conditions. This feature brings TypeScript closer to a fully functional programming language, giving developers the tools to express complex type logic with clarity.

In this article, we’ll explore dynamic conditional types in TypeScript in depth. We’ll walk through what they are, why they’re useful, and how to use them with practical examples.

> **🌈 Not a Member?** [**click here to read full article**](https://medium.com/@mayurkoshti12/ebaa00b04a09?sk=4aa3d16e5735ecab1af9b5927ce6adcd)

## 🥀 What Are Conditional Types in TypeScript?

Conditional types in TypeScript are a way to define types based on a condition. They follow the form:

```
T extends U ? X : Y
```

This means:

* If `T` extends `U` (i.e., `T` is assignable to `U`), the type resolves to `X`.
* Otherwise, it resolves to `Y`.

It’s similar to a ternary operator in JavaScript but is used at the type level.

## 🍄 Why Use Conditional Types?

Conditional types offer several benefits:

> **Flexibility**

* They allow you to express dynamic logic in type definitions.

> **Type Inference**

* They enable the creation of types that adapt to the input type.

> **Code Safety**

* By defining logic in types, you can catch potential errors during compilation rather than at runtime.

## 🍁 Syntax of Conditional Types

Here’s a simple example to illustrate the syntax:

```
type IsString<T> = T extends string ? true : false;  
  
type Test1 = IsString<string>; // true  
type Test2 = IsString<number>; // false
```

In this example:

* `IsString<string>` resolves to `true` because `string` extends `string`.
* `IsString<number>` resolves to `false` because `number` does not extend `string`.

## 🍂 Building Dynamic Conditional Types

### 1. Extracting Properties Based on Conditions

Conditional types can be used to extract properties from a type:

```
type ExtractStringProperties<T> = {  
  [K in keyof T]: T[K] extends string ? K : never;  
}[keyof T];  
  
interface Person {  
  name: string;  
  age: number;  
  email: string;  
}  
  
type StringProperties = ExtractStringProperties<Person>; // "name" | "email"
```

**Explanation**:

* `T[K] extends string ? K : never` checks if the property type is a string.
* If it is, it keeps the key (`K`); otherwise, it returns `never`.
* `[keyof T]` collects all keys that are not `never`.

### 2. Inferring Types with `infer`

The `infer` keyword is used within conditional types to infer a type from another type.

Example: Extracting the return type of a function:

```
type ReturnTypeOf<T> = T extends (...args: any[]) => infer R ? R : never;  
  
type ExampleFunction = () => string;  
  
type Result = ReturnTypeOf<ExampleFunction>; // string
```

**Explanation**:

* `T extends (...args: any[]) => infer R` checks if `T` is a function.
* `infer R` captures the return type of the function.
* If `T` is not a function, the type resolves to `never`.

### 3. Narrowing Down Union Types

Conditional types can be used to narrow down union types.

```
type ExcludeType<T, U> = T extends U ? never : T;  
  
type Result = ExcludeType<string | number | boolean, boolean>; // string | number
```

**Explanation**:

* `T extends U ? never : T` excludes types from `T` that extend `U`.
* In this case, `boolean` is excluded from the union type.

### 4. Handling Complex Scenarios

Let’s define a conditional type that maps specific types to their plural forms:

```
type Pluralize<T> = T extends 'cat'  
  ? 'cats'  
  : T extends 'dog'  
  ? 'dogs'  
  : T extends 'mouse'  
  ? 'mice'  
  : T;  
  
type CatPlural = Pluralize<'cat'>; // "cats"  
type DogPlural = Pluralize<'dog'>; // "dogs"  
type DefaultCase = Pluralize<'fish'>; // "fish"
```

**Explanation**:

* The type checks each condition in order.
* If none of the conditions match, it falls back to `T` (default case).

## 💐 Combining Conditional Types with Utility Types

TypeScript provides built-in utility types that work well with conditional types.

### Example: Combining `Partial` and Conditional Types

```
type ConditionalPartial<T, K extends keyof T> = {  
  [P in keyof T]: P extends K ? Partial<T[P]> : T[P];  
};  
  
interface User {  
  id: number;  
  name: string;  
  address: {  
    city: string;  
    zip: number;  
  };  
}  
  
type PartialAddressUser = ConditionalPartial<User, 'address'>;  
  
const user: PartialAddressUser = {  
  id: 1,  
  name: 'John',  
  address: {  
    city: 'New York',  
  },  
};
```

**Explanation**:

* `P extends K ? Partial<T[P]> : T[P]` makes properties in `K` optional while keeping the rest intact.

## 🌏 Real-World Use Cases

1. **API Response Handling**  
    When working with APIs, conditional types can help map responses dynamically.

```
type ApiResponse<T> = T extends { error: string } ? 'ErrorResponse' : 'SuccessResponse';  
  
type Success = ApiResponse<{ data: string }>; // "SuccessResponse"  
type Error = ApiResponse<{ error: string }>; // "ErrorResponse"
```

1. **Custom Validation**  
    Define types for validating forms dynamically based on input.

```
type ValidateInput<T> = T extends string  
  ? { valid: boolean; value: string }  
  : { valid: boolean; value: number };  
  
type StringValidation = ValidateInput<string>; // { valid: boolean; value: string }  
type NumberValidation = ValidateInput<number>; // { valid: boolean; value: number }
```

## 💦 Final Thoughts

Dynamic conditional types in TypeScript empower developers to write flexible and type-safe code. By incorporating conditions into your type logic, you can define robust types that adapt to various scenarios, ensuring fewer runtime errors and better developer experience.

From extracting properties to handling complex unions and inferring types, conditional types are a cornerstone of advanced TypeScript programming. By understanding their syntax and applying them effectively, you can unlock the full potential of TypeScript in your projects.

With practice, these types will become a natural part of your TypeScript toolkit, allowing you to express even the most complex type relationships with ease.

> ***Thank you for reading. Before you go 🙋‍♂️:  
>    
>  Please clap for the write 👏  
>    
>  🏌️‍♂️ Follow me:*** [***https://medium.com/@mayurkoshti12***](https://medium.com/@mayurkoshti12) ***🤹 Follow Publication:*** [***https://medium.com/the-code-compass***](https://medium.com/the-code-compass)

## 🌈 More Topics

![Mayur Koshti](https://miro.medium.com/v2/resize:fill:40:40/1*9e3EfvMp0pXPx7mnzk0AKg.jpeg)

[Mayur Koshti](https://medium.com/@mayurkoshti12?source=post_page-----ebaa00b04a09---------------------------------------)

## JavaScript

[View list](https://medium.com/@mayurkoshti12/list/javascript-5f40a40d1ac3?source=post_page-----ebaa00b04a09---------------------------------------)

62 stories

![Oops! Don’t Let These JavaScript Errors Haunt Your Debug Logs 👻 Every JavaScript Developer Needs to Know — Mayur Koshti](https://miro.medium.com/v2/resize:fill:388:388/1*O0Azu18ZZigs6kijrU02ug.png)

![Top 10 JavaScript Hints: From Beginner to Pro in Seconds 🚀 The Magic of Code Suggestions](https://miro.medium.com/v2/resize:fill:388:388/1*1wCbdCT-w0E9X8QNs-XF1g.png)

![Stop Writing Functions the Old Way In Javascript! The Arrow Function Revolution is Here 🚀](https://miro.medium.com/v2/resize:fill:388:388/1*DBxY9IvsMI-1w-kcd9Bv4w.jpeg)

![Mayur Koshti](https://miro.medium.com/v2/resize:fill:40:40/1*9e3EfvMp0pXPx7mnzk0AKg.jpeg)

[Mayur Koshti](https://medium.com/@mayurkoshti12?source=post_page-----ebaa00b04a09---------------------------------------)

## node.js

[View list](https://medium.com/@mayurkoshti12/list/nodejs-f51e108e6864?source=post_page-----ebaa00b04a09---------------------------------------)

15 stories

![5 Node.js Tricks You MUST Know in 2025! The Only Node.js Tricks You’ll Ever Need](https://miro.medium.com/v2/resize:fill:388:388/1*yPUkMTvXl7oHZc-Vzmtyvg.png)

![The Node.js Buffer Mistake That’s Crashing Your App Avoid These Common Buffer Mistakes](https://miro.medium.com/v2/resize:fill:388:388/1*SnNn7pIV-Lm_U_7VUPA3gw.png)

![Best Top 5 Libraries in Node JS](https://miro.medium.com/v2/resize:fill:388:388/1*LKgFaPp9Rw2W7yN3o2mQjg.jpeg)

![Mayur Koshti](https://miro.medium.com/v2/resize:fill:40:40/1*9e3EfvMp0pXPx7mnzk0AKg.jpeg)

[Mayur Koshti](https://medium.com/@mayurkoshti12?source=post_page-----ebaa00b04a09---------------------------------------)

## React

[View list](https://medium.com/@mayurkoshti12/list/react-ca0b887fc035?source=post_page-----ebaa00b04a09---------------------------------------)

15 stories

![Stop Doing Fetch Wrong in React! Use Axios Instead — Mayur Koshti](https://miro.medium.com/v2/resize:fill:388:388/1*AC9Sjg2861jKtZGpGJlkgA.png)

![](https://miro.medium.com/v2/resize:fill:388:388/1*m77kviec8-fa7yTA1cLJcw.png)

![Laravel and React are two powerful tools in the web development ecosystem. Laravel, a PHP-based framework, is known for its elegance and simplicity in backend development, while React, a JavaScript library developed by Facebook, is widely used for creating dynamic and interactive user interfaces.](https://miro.medium.com/v2/resize:fill:388:388/1*qCe9L1M9BtJW7pSNsYbYYg.jpeg)

![Mayur Koshti](https://miro.medium.com/v2/resize:fill:40:40/1*9e3EfvMp0pXPx7mnzk0AKg.jpeg)

[Mayur Koshti](https://medium.com/@mayurkoshti12?source=post_page-----ebaa00b04a09---------------------------------------)

## Angular

[View list](https://medium.com/@mayurkoshti12/list/angular-85a989fbcdc7?source=post_page-----ebaa00b04a09---------------------------------------)

8 stories

![](https://miro.medium.com/v2/resize:fill:388:388/1*m77kviec8-fa7yTA1cLJcw.png)

![Choosing the right technology stack is a critical decision for any project, and when it comes to front-end frameworks, Angular and React are two of the most popular options. Both are powerful tools for building modern web applications, but they have key differences that make each suitable for different kinds of projects. So, which should you use in your project: Angular or React?](https://miro.medium.com/v2/resize:fill:388:388/1*RgzHxM4M6LaNWsk1NWzlyw.jpeg)

![In modern web development, creating interactive and dynamic forms is essential for a seamless user experience. Angular, one of the leading front-end frameworks, offers powerful form-handling capabilities with its Reactive Forms module. Coupling Reactive Forms with RxJS, Angular’s underlying reactive library, brings a new level of flexibility and power to form control.](https://miro.medium.com/v2/resize:fill:388:388/1*KTonFNXKW8ROS8i9BUf2Vg.jpeg)

## Thank you for being a part of the community

*Before you go:*

* Be sure to **clap** and **follow** the writer ️👏**️️**
* Follow us: [**X**](https://x.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0)
* [**Check out CoFeed, the smart way to stay up-to-date with the latest in tech**](https://cofeed.app/) **🧪**
* [**Start your own free AI-powered blog on Differ**](https://differ.blog/) 🚀
* [**Join our content creators community on Discord**](https://discord.gg/in-plain-english-709094664682340443) 🧑🏻‍💻
* For more content, visit [**plainenglish.io**](https://plainenglish.io/) + [**stackademic.com**](https://stackademic.com/)