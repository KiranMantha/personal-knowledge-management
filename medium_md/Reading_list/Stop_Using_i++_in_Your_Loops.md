---
title: "Stop Using i++ in Your Loops"
url: https://medium.com/p/1f906520d548
---

# Stop Using i++ in Your Loops

[Original](https://medium.com/p/1f906520d548)

Member-only story

# Stop Using i++ in Your Loops

## Why ++i is often better than i++ (pre-increment vs. post-increment)

[![Devin Soni](https://miro.medium.com/v2/resize:fill:64:64/2*1Z-JeVOl6yKM5IwAUOu35Q.png)](/@devins?source=post_page---byline--1f906520d548---------------------------------------)

[Devin Soni](/@devins?source=post_page---byline--1f906520d548---------------------------------------)

2 min read

·

Nov 6, 2019

--

59

Listen

Share

More

Press enter or click to view image in full size

![]()

## Introduction

If you’ve written a for-loop before, then you have almost definitely used `i++` before to increment your loop variable.

However, have you ever thought about *why* you choose to do it like that?

Clearly, the end result of `i++` is that `i` is one higher than it was before — which is what we want. But, there are many ways to accomplish this, such as `++i`, `i++`, and even `i = i + 1`.

In this article, I will cover two methods of adding 1, `++i`, and `i++`, and explain why `++i` may be better than `i++` in most situations.

## Post-Increment (i++)

The `i++` method, or post-increment, is the most common way.

In psuedocode, the post-increment operator looks roughly as follows for a variable `i`:

```
int j = i;  
i = i + 1;  
return j;
```

Since the post-increment operator has to return the original value of `i`, and not the incremented value `i + 1`, it has to store the old version of `i`.

This means that it typically needlessly uses additional memory to store that value, since, in most cases, we do not actually use the old version of `i`, and it is simply discarded.

## Pre-Increment (++i)

The `++i` method, or pre-increment, is much less common and is typically used by older programmers in languages such as C and C++.

In psuedocode, the pre-increment operator looks roughly like this for a variable `i`:

```
i = i + 1;  
return i;
```

Notably, here, we do not have to save the old value of `i` — we can simply add to it and return. This aligns much better with the typical use-case in a for-loop, since we rarely need the old value of `i` in that context.

## Caveats

After seeing the difference between post-increment and pre-increment, one might notice that, since the cached value of `i` is never used in post-increment, the compiler will just optimize that line away, making the two operators equivalent.

This is most likely true for primitive types, such as an integer.

However, for more complex types, such as user-defined types or iterators with the `+` operation overloaded, the compiler may not be able to safely optimize the caching operation.

So, it seems that in most cases, the pre-increment operator is better than, or equal to, the post-increment operator, as long as you do not need the previous value of whatever you are incrementing.