---
title: "Introducing NG-VDOM: A new way to write Angular application"
url: https://medium.com/p/60a3be805e59
---

# Introducing NG-VDOM: A new way to write Angular application

[Original](https://medium.com/p/60a3be805e59)

# Introducing NG-VDOM: A new way to write Angular application

[![Trotyl Yu](https://miro.medium.com/v2/resize:fill:64:64/1*W5P71V4HDn_dSdLTgtxxWA.jpeg)](/@trotyl?source=post_page---byline--60a3be805e59---------------------------------------)

[Trotyl Yu](/@trotyl?source=post_page---byline--60a3be805e59---------------------------------------)

7 min read

·

Jan 28, 2019

--

13

Listen

Share

More

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

> [***AngularInDepth***](https://medium.com/angular-in-depth) ***is moving away from Medium. More recent articles are hosted on the new platform*** [***inDepth.dev***](https://indepth.dev/angular/)***. Thanks for being part of indepth movement!***

Front end development has evolved dramatically in the last decade. With AngularJS released back in 2009, **declarative representation of UI** has become a standard approach for front-end web development. Angular makes declarative programming first class citizen by utilizing templates in components. Using static templates to define logic has a number of benefits and we’ll review them in this article.

However, there’s an alternative approach to describing UI representation through an expression-based view definition known as Virtual DOM. This approach uses JavaScript to define the view and is the approach implemented by React. In this article I want to describe it and introduce a library I wrote to use this approach in Angular.

## The benefits of a templating approach

[Component](https://angular.io/guide/glossary#component) is a fundamental concept in Angular, responsible for defining UI representation and logic. Every component in Angular has a template. Components are modeled after the [MVVM](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93viewmodel) architecture, which is explained [on Angular docs](https://angular.io/guide/template-syntax#template-syntax):

> You may be familiar with the component/template duality from your experience with model-view-controller (MVC) or model-view-viewmodel (MVVM). In Angular, the component plays the part of the controller/viewmodel, and the template represents the view.

A component and its template are connected by the public shape of Component, then they together could instantiate the View. A simple Angular component could look like this:

With its template to be:

Defining view through templates has a lot of advantages.

### Separation of Concern

One can fully focus on UI when writing templates, without worrying about data sources, their dependency graph and presentation logic. For example, [a template in Angular Material](https://github.com/angular/material2/blob/bc8fc75bf8af82378077d7c2277e31a1dcd6aac9/src/lib/datepicker/calendar-header.html#L1-L25) datepicker looks like this:

The template only defines the structure and contents, omitting the implementation details. The real origin of `periodButtonText` сan be component input, internal state or computed result, which makes no difference to the template.

By using a top-down development process, one can make the templates first, driving the shape of the component, ensure an effective design of the data layer.

### Simplicity

With an abstraction layer, the template could help simplify the control flow, with a simple attribute on the tag:

On the contrary, implementing control flow inside expressions is troublesome and inevitably requires extra conditional operators or callbacks. Even when using [JSX Control Statements](https://www.npmjs.com/package/babel-plugin-jsx-control-statements) to remain declarative, an extra nesting level would still break the VCS history.

Also, with the idea of Pipes (possibly known as Filters in other systems), one can elegantly handle complex data structures, such as [Observables](https://rxjs.dev/api/index/class/Observable):

Rather than repeating `subscribe` and `unsubscribe` in each consumption.

### Consistent `this`

As a consumer of a component’s state, a template can make direct calls to the instance, rather than asking a component to pass them out. Without passing the method reference, all of the following codes have the same result:

### Performance Optimization

With concrete knowledge of which parts of the template are dynamic, the template:

Will be compiled to:

So that only the bindings need to be handled in the update pass.

In an expression-based dynamic view description, all the parts need to be checked in each component during the change detection cycle, or require an extra setup during bootstrap to determine the dynamic parts. Both ways would introduce extra runtime costs.

However, there are some restrictions for the approach with a template when having a complex control flow:

In the example above, making a dynamic heading level via template will result in bloated code.

## A New Possibility

Given there are some conditions that can’t be handled elegantly with a templating approach. Can we make it possible to write an expression-based view definition in Angular when needed? The answer is Yes. And this is where our library comes in handy. When we’re using the library, we just need to extend from `Renderable` and implement the `render` method similar to React. Here’s an example:

This implementation will result into the `“Hello, Angular!”` string rendered in the browser. ([live example](https://codesandbox.io/s/wqomov90k))

> Both [Angular](https://github.com/angular/angular/pull/20556) and [Angular CLI](https://github.com/angular/angular-cli/pull/11407) already support .tsx file. Moreover, one can actually change “tsconfig.json” with a different “jsxFactory” option, rather than writing “import \* as React” in the component.

Besides [intrinsic elements](http://www.typescriptlang.org/docs/handbook/jsx.html#intrinsic-elements), both Class Component and Function Component can also be rendered (not fully compatible with React API yet). But most importantly, one can render another canonical Angular Component ([live example](https://codesandbox.io/s/qk0x5l9rvw)):

`HelloComponent` here is a plain Angular Component with nothing special, but currently we need to register it in `entryComponents`. In the current implementation of Angular a component is resolved through the [ComponentFactory](https://angular.io/api/core/ComponentFactory). If not found, it would be treated as a Function Component which would cause an error.

> The concept of `entryComponent` will be significantly improved after Ivy.

The mapping here can be illustrated as:

* Prop: foo -> \@Input(‘foo’)
* Prop: onBar -> \@Output(‘bar’)
* Prop: children -> Content Projection

Please be aware the template names of Input/Output will be used rather than property names, but they’re likely to be equivalent in most components.

> ***A fully-featured TODO MVC example that uses the library can be found on*** [***GitHub***](https://github.com/trotyl/ng-renderable-todomvc) ***with*** [***online preview available***](https://trotyl.github.io/ng-renderable-todomvc/)***.***

## From Template to ViewModel

To understand how Virtual DOMs can be handled in Angular, we should first understand what Virtual DOM is. Briefly, Virtual DOM is just a superfluous name for ViewModel that holds values for dynamic parts of a template. Given a fully static template, its ViewModel is empty:

When we define all the properties of an element as dynamic and extract them to bindings, the ViewModel becomes the container of properties and their values:

Then the binding data-source can be made “the container of properties” itself, rather than individual traits:

Finally, once the tag name is also a dynamic binding, the template no longer has any static parts and actually becomes redundant:

**When the ViewModel carries all the information of the View, it becomes a definition of the View.** No matter what it’s being called, it’s still a ViewModel and can be treated like any other ViewModel. **The most important part is determining what is changed in a change detection pass. This is** [**change detection in Angular**](https://blog.angularindepth.com/a-gentle-introduction-into-change-detection-in-angular-33f9ffff6f10) **or** [**reconciliation in React**](/react-in-depth/inside-fiber-in-depth-overview-of-the-new-reconciliation-algorithm-in-react-e1c04700ef6e)**.**

## How It All Works

When looking at the implementation of complex data-structure handling directives such as `NgForOf`, `NgClass` and `NgStyle`, it’s easy to observe that to detect changes we need to diff consecutive Input values and apply changes if detected.

While most frameworks contain some diffing implementation, Angular has been exposing them to developers for us to reuse. There’re two kinds of differs in Angular:

* [IterableDiffer](https://angular.io/api/core/IterableDiffer): compare a sequence of items;
* [KeyValueDiffer](https://angular.io/api/core/KeyValueDiffer): compare a dictionary;

While an Angular directive normally only uses one differ (`NgClass` uses either one depends on its Input, but not both), the structure of a Virtual DOM is much more complicated and nested, so both differs need to be used: `KeyValueDiffer` for props and `IterableDiffer` for children. The detailed implementation will not be illustrated here, but conceptually they are just recursive diffing.

With the knowledge of what is being changed, we need to apply the changes to the View. In Angular there’s an abstract helper for view operations, known as [Renderer](https://angular.io/api/core/Renderer2), with the following shape:

As long as we use `Renderer` methods for UI manipulations, any implementation will remain platform-agnostic and can be used in any platform without special handling.

For rendering Angular components, we need to make use of [Angular Dynamic Components](https://angular.io/guide/dynamic-component-loader) functionality, the most important parts `ComponentFactory` and `ComponentFactoryResolver`.

`ComponentFactory` provides the required metadata of Input/Output, making the properties mapping work:

In fact, commonly used packages like [ngUpgrade](https://angular.io/guide/upgrade) and [Angular Elements](https://angular.io/guide/elements) are both built on the top of the Dynamic Components functionality.

With the ability of Virtual DOM rendering, we still need to let Angular know when to do that. Then comes the life-cycle hook — [DoCheck](https://angular.io/api/core/DoCheck).

As a specially named hook (all others start with “*on*” or “*after*”), *DoCheck* is designed to handle extra jobs when the change detection runs, which is exactly what we want. So the basic structure of *Renderable* would be:

Now, we can use a `render` method on an Angular component to render another Angular component, nothing magical.

## The Future Plan

While it’s possible to organize Angular components via the `render` method, there's still plenty of features to do.

### HTML Attributes support

The React API for intrinsic elements is a [mixture of DOM properties, HTML attributes and renamed DOM properties](https://github.com/facebook/react/issues/13525#issuecomment-417818906). (ignoring event system for now)

While renamed DOM properties are controversial, HTML attributes are definitely needed:

The `data-` or `aria-` attributes have no corresponding properties, without attributes support, they can only be added by `ref` callbacks (also not supported yet), which isn’t a declarative approach.

### React/React DOM API Compatibility

The concepts and features for Class Component and Function Component are mainly determined by React, while compatibility via alias is a long way to go, lifecycle-hooks and utility functions would still be important for development.

### Reverse Bridge

Use existing Class Components or Function Components in the Angular template without making a Virtual DOM object. Likely, this only makes sense after compatibility support is complete.

### Global Bootstrap

It could be useful to render a Virtual DOM structure without writing any Angular code. This was actually implemented in earlier versions but was removed in a recent refactoring due to the complexity in the build process.

The basic concept here is: due to no user-defined Angular type, the whole AOT process can be lifted to the build process of the library, and then publishing the AOT-compiled code. The user will no longer need to bring the compiler to the runtime.

## Summary

Templates are great, there’s no need to write expression-based View definition unless having extreme complexity.

Virtual DOM is technically just a ViewModel and can be handled the same way, there’s no real implementation diversity regardless if it’s being called View or ViewModel.

The library repo can be found at [on GitHub](https://github.com/trotyl/ng-vdom), while it’s technically not the first release, it’s now no longer a POC and I encourage you to experiment with it (but not recommended for production yet). Feel free to file Bug Report or Feature Request.