---
title: "Factory Functions vs Constructor Functions in JavaScript: Which One Should You Use?"
url: https://medium.com/p/fbeba4a5ecd6
---

# Factory Functions vs Constructor Functions in JavaScript: Which One Should You Use?

[Original](https://medium.com/p/fbeba4a5ecd6)

Member-only story

# **Factory Functions vs Constructor Functions in JavaScript: Which One Should You Use?**

## A practical guide to understanding the differences between factory functions and constructor functions, their pros and cons, and real-world use cases in JavaScript.

[![CodeByUmar](https://miro.medium.com/v2/resize:fill:64:64/1*vjFe2I18KAEfLTTJKyDC0Q.jpeg)](/@codebyumar?source=post_page---byline--fbeba4a5ecd6---------------------------------------)

[CodeByUmar](/@codebyumar?source=post_page---byline--fbeba4a5ecd6---------------------------------------)

3 min read

·

Feb 8, 2026

--

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dfbeba4a5ecd6&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fskillstuff%2Ffactory-functions-vs-constructor-functions-in-javascript-which-one-should-you-use-fbeba4a5ecd6&source=---header_actions--fbeba4a5ecd6---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

## “Why do I see two ways of creating objects in JavaScript?”

If you’ve ever written:

```
function createPerson(name) {  
  return { name };  
}  
  
const alice = createPerson("Alice");  
console.log(alice.name); // Alice
```

…and then seen someone use a constructor function like this:

```
function Person(name) {  
  this.name = name;  
}  
const bob = new Person("Bob");  
console.log(bob.name); // Bob
```

…it’s natural to ask: **what’s the difference?**

Both patterns create objects, but they have different behaviors, pros, and pitfalls.

In this article, we’ll cover:

* What factory functions and constructor functions are
* Syntax differences
* Prototype behavior
* Pros and cons
* When to use each in real-world JavaScript