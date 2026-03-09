---
title: "Why and How to Lazy Load Components in Angular"
url: https://medium.com/p/b4aff3797c6d
---

# Why and How to Lazy Load Components in Angular

[Original](https://medium.com/p/b4aff3797c6d)

# Why and How to Lazy Load Components in Angular

## Create a reusable Angular accordion component and lazy load its content

[![Bharath Ravi](https://miro.medium.com/v2/resize:fill:64:64/1*0sgrFDygiIe9wlWfn2dDbg.jpeg)](/@bharath-ravi?source=post_page---byline--b4aff3797c6d---------------------------------------)

[Bharath Ravi](/@bharath-ravi?source=post_page---byline--b4aff3797c6d---------------------------------------)

5 min read

·

Sep 17, 2020

--

1

Listen

Share

More

Press enter or click to view image in full size

![]()

> *“Before software can be reusable it first has to be usable.”*
>
> *— Ralph Johnson*

*Lazy loading,* by definition, is the technique of loading something on demand.

Lazy loading can be applied to different levels of your application-development process, from modules to components. Module-level lazy loading is quite famous in the Angular world, but component-level lazy loading is something less spoken about. In this article, we’ll create an accordion component and lazy load the content.

## Why Lazyload Components at All?

Press enter or click to view image in full size

![]()

So you’ve published your production-ready Angular application!

You made sure to use best practices while writing the code, reusing components, lazyloading modules, and whatnot. After weeks of live usage, users have started complaining about application performance — specifically, about the initial loading time of some pages. For this reason, you started losing users, and the statistics keep coming down.

You did a round of analysis and found you have a component that’s making multiple API calls that aren’t necessary (or less important) for the initial user experience. It can be a modal, an accordion, or even a slider. This particular API call is slowing down your application and making user experience sluggish.

The better approach here (taking the accordion as the example) clearly would be to load content inside the accordion only when the user opens the particular accordion.

This above is a perfect use case to implement lazy loading.

Let’s get to it.

## The Initial Version

For the sake of practicality, let’s assume an application scenario where we have a list of blog posts that we want to show under an accordion.

Before we refactor and implement lazy loading, the below typical application setup is what we have.

We have two components:

1. Post component loading data of the blog post)
2. Accordion component

We’re using these two components to render the blog post to users in our `app-component`.

We’re using the `app-accordion` component and passing the `app-post` component to it for content projection.

And for the accordion implementation:

Inside our `post` component, we’re making an HTTP call to `jsonplaceholder`, getting a fake blog post, and displaying it on the template.

This will result in something like the following:

![]()

As you can clearly see, the data is now loading on the page’s initial load, which isn’t ideal in some cases, such as the one we discussed above.

## Implementing Lazy Loading

Here’s our plan to get the content loaded lazily.

We’ll be using `@ContentChild` from @angular/core to grab the accordion body using the directive syntax on a `<ng-template>` (we’re replacing the content-projection technique in the earlier version). We use `<ng-template>` and not a `<div>` because of the special nature of it, which we can make use of.

From the [docs](https://angular.io/guide/structural-directives#the-ng-template):

> “The `<ng-template>` is an Angular element for rendering HTML. It is never displayed directly. In fact, before rendering the view, Angular *replaces* the `<ng-template>` and its contents with a comment.   
> If there is no structural directive and you merely wrap some elements in a `<ng-template>`, those elements disappear.”

To start with, let’s create a new directive for the accordion body.

```
ng generate directive accordion
```

Let’s rename the selector to `[accordion-body]`. The purpose of this directive is to only act as a selector for our `<ng-template>`, which holds our accordion body. The only change we’re making to this directive is renaming it.

Let’s now add the `[accordion-body]` directive into our `app-component`.

If you now navigate to our application, you’ll see the `app-post` component not displayed at all — thus, our API isn’t triggered either.

Great!

The only part remaining now is to refactor the `app-accordion` component.

We’re extending our already existing accordion component. We’ve used `@ContentChild` to access the first child of `app-accordion` having `AccordionDirective` (i.e., `[accordion-body]`) in it. Note that we used `read: TemplateRef`, as we’re accessing a template reference. You can read about more options in the [documentation](https://angular.io/api/core/ViewChild).

Now we can simply use this in our `app-accordion` component template.

It’s as easy as that!

Note the use of `*ngTemplateOutlet`[,](https://angular.io/api/common/NgTemplateOutlet) which is used to insert an embedded view from a prepared `TemplateRef(accordionBodyRef)`.

That’s all of it! You now have a lazy-loaded an accordion component and have a faster-loading application.

![]()

## Extending the Solution to Support Eager Loading

The present implementation of our accordion only supports lazy loading. There’s no way you can eagerly load (on initial load of application content) with the present implementation. But at times, you might have cases where you need the accordion to support eagerly loading content. In that case, you might have to create another component to achieve this.

Let’s make our existing accordion component truly reusable by adding both lazy- and eager-loading capabilities.

This can be done easily by adding another `*ngIf` condition inside our accordion template.

We’re checking if the `accordionBodyRef` template exists or not. If it does, we’re showing the component, and the content would load lazily. If not, we’re simply picking the `accordionBody` using content projection.

Now on `app-component`:

There you go! You can now use the same `app-accordion` component to render contents lazily or eagerly as required.

You can find the completed project [here on GitHub](https://github.com/BharathRavi27/lazy-loaded-accordion).

Happy hacking!