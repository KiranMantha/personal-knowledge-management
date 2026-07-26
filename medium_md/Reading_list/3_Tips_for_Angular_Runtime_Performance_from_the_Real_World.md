---
title: "3 Tips for Angular Runtime Performance from the Real World"
url: https://medium.com/p/d467fbc8f66e
---

# 3 Tips for Angular Runtime Performance from the Real World

[Original](https://medium.com/p/d467fbc8f66e)

# 3 Tips for Angular Runtime Performance from the Real World

[![Paul Spears](https://miro.medium.com/v2/resize:fill:64:64/0*BY0U-PzLU7jVHl4G.)](https://medium.com/@dpsthree?source=post_page---byline--d467fbc8f66e---------------------------------------)

[Paul Spears](https://medium.com/@dpsthree?source=post_page---byline--d467fbc8f66e---------------------------------------)

4 min read

·

Oct 2, 2017

--

12

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dd467fbc8f66e&operation=register&redirect=https%3A%2F%2Fblog.angular.dev%2F3-tips-for-angular-runtime-performance-from-the-real-world-d467fbc8f66e&source=---header_actions--d467fbc8f66e---------------------post_audio_button------------------)

Share

Co-authored by Andrew Wiens

At Oasis Digital, we train and work with large companies that build software with Angular. In this time, we’ve learned a lot about about building performance sensitive applications. From these experiences we’ve distilled out our top 3 performance tips for building great user experiences.

Press enter or click to view image in full size

![]()

## What is Runtime Performance?

To discuss any type of application performance, it’s important to define what we mean.

Being responsible for creating highly responsive interfaces requires that we care about performance. This means responding to user input and rendering in less than 17 milliseconds. Achieving this creates a smooth and seamless experience, in turn, increasing user confidence in your application.

We often write applications with little concern for the internal Angular operations. But, some situations need fine-tuning and a deeper understanding of what Angular does under the hood. Care is most often needed as data size or feature complexity grows. Data tables are a classic example. Often, a table that works well with small quantities of data begins lagging as the data size increases.

Knowing how your application’s events behave and how they interact with Angular is key to improving performance. As such, runtime performance in Angular ties to its change detection process, which includes three steps:

1. Run event handlers
2. Update data bindings
3. Propagate DOM updates and repaint

Let’s look at a few simple ways that we can improve each of these aspects.

## Tip 1: Make Events Fast

Event handlers can exist in many locations within an Angular application. The most obvious examples are DOM and component event bindings. Designing these events to take as little time as possible ensures that change detection does not take more than 17 ms. If this target is not met the frame rate drops below 60 frames per second. This happens because Angular must wait for the callback to finish before change detection can continue and the update rendered.

## Get Paul Spears’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

Let’s examine a simple example of where an event binding may take longer to execute than anticipated. The following code contains a component (AppComponent) that responds to a click event. It does so by passing a value from the template into a service (ListService). The service in turn utilizes that value to filter a list. Finally, control returns to the click handler before completing. It isn’t until control returns from the service that change detection can continue. As the size of the list grows, the event’s performance will degrade.

As demonstrated above, it is easy to forget that event handlers will often run code defined outside of the component definition. Identifying these lengthy processes allows them to be improved. This usually takes the form of choosing a more efficient algorithm. Alternatively, executing this process asynchronously allows change detection to complete while filtering finishes.

## Tip 2: Minimize Change Detections

By default, components in an Angular application undergo change detection with nearly every user interaction. But, Angular allows you take control of this process. You can indicate to Angular if a component subtree is up to date and exclude it from change detection.

The first way to exclude a component subtree from change detection is by setting the `changeDetection` property to `ChangeDetectionStrategy.OnPush` in the @Component decorator. This tells Angular that the component only needs to be checked if an input has changed, and that all of the inputs can be considered immutable.

At the price of a bit more complexity it is possible to increase the amount of control. For example, by injecting the ChangeDetectorRef service, you can inform Angular that a component should be detached from change detection. You can then manually take control of calling `reattach` or `detectChanges()` yourself, giving you full control of when and where a component subtree is checked.

## Tip 3: Minimize DOM Manipulations

By default, when iterating over a list of objects, Angular will use object identity to determine if items are added, removed, or rearranged. This works well for most situations. However, with the introduction of immutable practices, changes to the list’s content generates new objects. In turn, ngFor will generate a new collection of DOM elements to be rendered. If the list is long or complex enough, this will increase the time it takes the browser to render updates. To mitigate this issue, it is possible to use trackBy to indicate how a change to an entry is determined.

## The Full Runtime Performance Guide

Knowing where to begin when facing performance issues can be an intimidating task. Hopefully these practical examples show where performance issues can hide and help you get started. Although these tips are a great starting point, there are many more opportunities to increase performance. You can read more about these tips in our full [Angular Runtime Performance Guide](https://blog.oasisdigital.com/2017/angular-runtime-performance-guide/).