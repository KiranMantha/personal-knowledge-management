---
title: "Recursion in Angular Components"
url: https://medium.com/p/1cd636269b12
---

# Recursion in Angular Components

[Original](https://medium.com/p/1cd636269b12)

# Recursion in Angular Components

[![Netanel Basal](https://miro.medium.com/v2/resize:fill:64:64/1*abTZV6gAiJNINYPHQUeOBg.png)](/@netbasal?source=post_page---byline--1cd636269b12---------------------------------------)

[Netanel Basal](/@netbasal?source=post_page---byline--1cd636269b12---------------------------------------)

2 min read

·

Feb 1, 2017

--

12

Listen

Share

More

Press enter or click to view image in full size

![]()

There are times that you need to render a template recursively. For instance, when you have a page with comments, you need to be able to render nested comments and reuse the same component.

In this short article, we are going to create a component that will take as `Input` comments and will know how to display them recursively.

## The Structure:

This is the JSON structure that we expect to get from our server. For this demonstration, we will make it static. ( you can change this structure to how you prefer it )

## Build the Comments Component

As you can see, we can call our component recursively. We don’t want to render the component when there are no comments, so we need to add the `ngIf` directive. ( not required if you don’t have any styles attached to the host )

## Create the App Component

## The Result

![]()

## 🔥 **Last but Not Least, Have you Heard of Akita?**

Akita is a state management pattern that we’ve developed here in Datorama. It’s been successfully used in a big data production environment, and we’re continually adding features to it.

Akita encourages simplicity. It saves you the hassle of creating boilerplate code and offers powerful tools with a moderate learning curve, suitable for both experienced and inexperienced developers alike.

I highly recommend checking it out.

[## 🚀 Introducing Akita: A New State Management Pattern for Angular Applications

### Every developer knows state management is difficult. Continuously keeping track of what has been updated, why, and…

netbasal.com](https://netbasal.com/introducing-akita-a-new-state-management-pattern-for-angular-applications-f2f0fab5a8?source=post_page-----1cd636269b12---------------------------------------)

*Follow me on* [*Medium*](/@NetanelBasal/) *or* [*Twitter*](https://twitter.com/NetanelBasal) *to read more about Angular!*