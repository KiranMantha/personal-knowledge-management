---
title: "Angular component testing with examples"
url: https://medium.com/p/7c52b2b7035e
---

# Angular component testing with examples

[Original](https://medium.com/p/7c52b2b7035e)

# Angular component testing with examples

[![Benjamin Cabanes](https://miro.medium.com/v2/resize:fill:64:64/1*swX67Ie8PSD7CPSHgWr5oA.jpeg)](/@bencabanes?source=post_page---byline--7c52b2b7035e---------------------------------------)

[Benjamin Cabanes](/@bencabanes?source=post_page---byline--7c52b2b7035e---------------------------------------)

3 min read

·

May 16, 2018

--

6

Listen

Share

More

![]()

In this article we will look at some tips and techniques for doing unit and integration tests of Angular Components.

> All examples and codes are available in the Stackblitz link for each case by folder. Make sure to check them out!

Before jumping right away into the test examples, let see the three mains ways we have to actually test an Angular component.

## Isolated vs Shallow vs Integrated

When we want to test an Angular Component, we have three different possible ways to do it: *isolated testing*, *shallow testing* or *integrated testing*.

Here is the annotate code for the ones that can’t wait, we will see the differences right after. You can play with it in the Stackblitz below, in the `integrated-isolated-shalow` folder.

### Isolated testing

When we use the isolated test on a component, we usually want to test its (*complex*) logic above all, we don’t want to focus on its template.

We can take the`CounterComponent`. This component has some logic we want to test, and a very simple template. Its template has some custom DOM elements which are in this case, other Angular components and directives.

Because we want to focus on the component’s logic, the template is irrelevant. We will do, in that case, an isolated test, focusing only on the component class.

> An isolated test only focuses on the component’s class.

### Shallow testing

When we use the shallow test on a component, we usually want to test its own template with the class logic. By doing so, we will mock all the other components that are part of the template.

We can see that the `CounterComponent` template has some buttons that we can click on. Furthermore, we can see that the template has still some custom DOM elements and directives. If we test it right away, Angular will throw an error to tell us that it doesn’t know some template syntaxes. These custom elements are not what we want to test right now. We only want to focus our test on the direct component’s template.

To be able to only focus on the component’s template and not its dependencies, we need to tell to not try to compile those custom elements. This is exactly what `schemas: [NO_ERRORS_SCHEMA]` do by telling to Angular to not throw any error when it doesn’t recognize a custom elements, in the TestBed configuration. You can have more information [here in the documentation](https://angular.io/api/core/NO_ERRORS_SCHEMA).

> You can use `CUSTOM_ELEMENTS_SCHEMA` too, but only if your template has custom elements like `<custom-element>`or `<div custom-attribute>...</div>`. If you have attribute binding/directive like elements in your template, you will need to use `NO_ERRORS_SCHEMA`. More information [here in the documentations](https://angular.io/api/core/CUSTOM_ELEMENTS_SCHEMA).

This test is one of the most common as it tests the component and its template.

> The shadow test focuses on the component’s class and its template, without its dependencies by mocking them.

### Integrated test

When we use an integrated test on a component, we want to test its class logic, its template and all its dependencies. Meaning, if its template includes custom elements (Angular components or directives), we will need to satisfy all those dependencies by injecting them in the TestBed configuration.

This test is the most heavy as it tests the component as a whole. Even if it looks like the shallow test, it tests more design and goes deeper. It could be more costly to main and harder to debug too, because you need to handle its dependencies.

> An integrated test will test the component and its dependencies as a whole.

## Component testing examples

Here is the Stackblitz with all the examples set, you can play, fork, and modify, do as you please.

You will see basic examples of:

* component content projection testing
* component dynamic style testing
* component input testing
* component output testing
* component stream testing
* component attribute directive testing
* component observable testing with marbles

## Resources

If you want to check and go deeper on isolated, shadow and integrated testing, check this out.

[## Three Ways to Test Angular Components

### Victor Savkin is a co-founder of nrwl.io, providing Angular consulting to enterprise teams. He was previously on the…

vsavkin.com](https://vsavkin.com/three-ways-to-test-angular-2-components-dcea8e90bd8d?source=post_page-----7c52b2b7035e---------------------------------------)

Be sure to check out the official Angular documentation on testing too.

[## Angular Docs

### Edit description

angular.io](https://angular.io/guide/testing?source=post_page-----7c52b2b7035e---------------------------------------)

There is a Github repository too, with more examples, check this one too.

[## juristr/angular-testing-recipes

### angular-testing-recipes - Simple testing patterns for Angular version 2+

github.com](https://github.com/juristr/angular-testing-recipes?source=post_page-----7c52b2b7035e---------------------------------------)