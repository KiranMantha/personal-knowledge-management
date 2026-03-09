---
title: "Product-Oriented JavaScript Interview Questions"
url: https://medium.com/p/ec5fbca3aa5d
---

# Product-Oriented JavaScript Interview Questions

[Original](https://medium.com/p/ec5fbca3aa5d)

# Product-Oriented JavaScript Interview Questions

## Interview questions asked in interviews at companies like Google, Amazon, and Uber

[![Kunal Tandon](https://miro.medium.com/v2/resize:fill:64:64/1*bQcQd07juIPQOuH8Z4-Xlw.jpeg)](https://medium.com/@kunaltandon.kt?source=post_page---byline--ec5fbca3aa5d---------------------------------------)

[Kunal Tandon](https://medium.com/@kunaltandon.kt?source=post_page---byline--ec5fbca3aa5d---------------------------------------)

4 min read

·

Aug 4, 2019

--

1

Listen

Share

More

Press enter or click to view image in full size

![]()

Note: Try to solve these questions without seeing the answers.

There is some white space after every question so that you do not directly see the answers and get a chance to solve these questions yourself.

## Question 1

Consider the following code snippet and try to identify what its output will be.

Press enter or click to view image in full size

![]()

Have you guessed it?

.

.

.

Let’s see…

### Answer

The following code will write the value `10` times.

Press enter or click to view image in full size

![]()

The value 10 is printed ten times as the variable `i` gets hoisted to the top of the code snippet and the final value of `i` is 10 after the code gets executed.

## Question 1 — Part 2

At this point, the interviewer generally asks: “What if I want values from `0-9` in the console?"

Try to guess this before scrolling to the solution…

### Printing values from 0–9 in the console

There are different ways to achieve this.

### By using IIFE

*IIFE* is Immediately Invoked Function Expressions. By using IIFE’s we can also scope the value of the variable `i` to print the current index, instead of printing the final value as `10`.

Below is the solution to print values `0-9` using IIFE's.

Press enter or click to view image in full size

![]()

Here, we wrapped the code of the first loop inside an IIFE that will print the following output in the console:

Press enter or click to view image in full size

![]()

### Using ES6 syntax

There is another way to fix this issue using ES6 syntax. To print the values from `0-9` in the console, simply replace the `var` keyword inside the first loop with the `let` keyword.

This way, the variable `i` does not get hoisted to the top of the code and its scope gets limited to the loop's block scope.

Press enter or click to view image in full size

![]()

Output:

Press enter or click to view image in full size

![]()

## Question 2

Let’s look at the following JavaScript code snippet:

Press enter or click to view image in full size

![]()

Can you identify what could probably go wrong here?

Take some time and try to identify if something could go wrong here.

.

.

.

### Answer

We are playing with references here. After the code gets executed, we will have an array of five elements so that each element is referencing the same object.

The final value of `arr` would look like:

Press enter or click to view image in full size

![]()

## Conclusion

The questions seem to be pretty difficult at first, but if you have a broader look at them, you will identify that they are nothing, just the core basic concepts of JavaScript that are combined together to create a problem.

The first question is a combination of:

* Lexical scoping.
* `var` /`let`/`const` in JavaScript.
* IIFE.

The second question is a combination of:

* Copying object references instead of object values.
* Arrays in JavaScript.

If you encounter any difficult problems in a real interview, just calm down and start thinking about the basic concepts that create the problem and surely, you will come to the right conclusion with ease.

## Loved the article? SUPPORT MY WRITING…

Press enter or click to view image in full size

![]()

**Patreon —** <https://www.patreon.com/kunaltandon>  
**Paypal —** <https://www.paypal.com/paypalme2/kunaltandon94>