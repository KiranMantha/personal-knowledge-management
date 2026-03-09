---
title: "Building a Simple Carousel Component with Angular"
url: https://medium.com/p/3a94092b7080
---

# Building a Simple Carousel Component with Angular

[Original](https://medium.com/p/3a94092b7080)

# Building a Simple Carousel Component with Angular

[![Netanel Basal](https://miro.medium.com/v2/resize:fill:64:64/1*abTZV6gAiJNINYPHQUeOBg.png)](/@netbasal?source=post_page---byline--3a94092b7080---------------------------------------)

[Netanel Basal](/@netbasal?source=post_page---byline--3a94092b7080---------------------------------------)

3 min read

·

Sep 12, 2017

--

24

Listen

Share

More

Press enter or click to view image in full size

![]()

In this article, we will create a simple carousel component with Angular that includes animation with the help of the Animation Builder service. We will also discuss several approaches to querying the DOM.

The following will be our final result:

Press enter or click to view image in full size

![]()

Let’s start by creating the `carousel` component.

## The Component CSS

Here, we’ll use a well-known CSS technique. We need a wrapper element with `overflow: hidden` and a fixed width we will define later as equal to the width of a carousel item. We must also set the carousel element to `display: flex` so the items appear in the same row. Later, we will use the Animation Builder service to animate the transform property of the carousel element.

Press enter or click to view image in full size

![]()

Let’s continue to see how we can pull the items out of the template.

### Building the Carousel Item Directive

The Carousel Item directive is a [structural](https://netbasal.com/the-power-of-structural-directives-in-angular-bfe4d8c44fb1) directive. We can leverage Dependency Injection to get a reference to the template.

### Rendering The Items

Now, let’s see how we can use this data in the parent component.

We can query for the `CarouselItemDirective` instances in our template with the `ContentChildren` decorator. Then we loop through them, passing the `CarouselItemDirective.tpl` property that holds a reference to a template to the `ngTemplateOutlet` directive. ( which we can get from the `CarouselItemDirective` constructor via DI ).

### Setting The Wrapper Width

As I mentioned before, we need to set the `wrapper` element width to the same as the first item width by querying for the `.carousel-item` element. For this task, I will use a directive with selector `.carousel-item`.

Now we can obtain a reference to every element in the template matching the directive selector.

Pay attention to two things here: we used `ViewChildren` and not `ContentChildren`, and we asked for the native DOM element by setting the read property to `ElementRef`.

Now we can get the width of the first element and set the wrapper element to the same value.

**Note:** You can also use `ViewChild` to get the first element, but I wanted to illustrate this method in case you want to build a carousel with dynamic width.

### Adding The Control Buttons

Before we see the `next()` and `prev()` methods, let’s create a couple properties that will help us to build the carousel.

The `carousel` property is a reference to the native DOM element of the carousel. Note that in this case I’m using a local template variable to query the element from the template.

We also have two `Inputs`, one for the animation timing and one that relays whether we need to show the controls. (we will see why this is useful later)

The remaining properties simply keep track of the carousel position.

### Implementing The next() Method

We need to do some math to calculate the carousel position. Then, we can use the Animation Builder service to create and play the animation based on the timing and offset variables.

The purpose of Animation Builder service is to produce an animation sequence programmatically within an Angular component or directive.

Programmatic animations are first built and then a player is created when the build animation is attached to an element.

When an animation is built an instance of `AnimationFactory` will be returned. Using that an `AnimationPlayer` can be created which can then be used to start the animation.

### Implementing The prev() Method

Here, we can use the same process as the `next()` method: calculate the carousel position and building and starting the animation.

### Using Custom Controls

We can export our component to the consumer template with the `exportAs` property on the component metadata.

That’s all.

*Follow me on* [*Medium*](/@NetanelBasal/) *or* [*Twitter*](https://twitter.com/NetanelBasal) *to read more about Angular, Vue and JS!*