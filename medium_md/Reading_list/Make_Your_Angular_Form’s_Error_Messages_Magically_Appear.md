---
title: "Make Your Angular Form’s Error Messages Magically Appear"
url: https://medium.com/p/1e32350b7fa5
---

# Make Your Angular Form’s Error Messages Magically Appear

[Original](https://medium.com/p/1e32350b7fa5)

# Make Your Angular Form’s Error Messages Magically Appear

[![Netanel Basal](https://miro.medium.com/v2/resize:fill:64:64/1*abTZV6gAiJNINYPHQUeOBg.png)](/@netbasal?source=post_page---byline--1e32350b7fa5---------------------------------------)

[Netanel Basal](/@netbasal?source=post_page---byline--1e32350b7fa5---------------------------------------)

5 min read

·

Jan 22, 2019

--

33

Listen

Share

More

Press enter or click to view image in full size

![]()

[## ngneat/error-tailor

### Making sure your tailor-made error solution is seamless! The Error Tailor offers seamless handling of form errors…

github.com](https://github.com/ngneat/error-tailor?source=post_page-----1e32350b7fa5---------------------------------------)

In this article, we’re going to learn how to develop a generic method that displays validation errors in Angular’s form. I will walk you through the process and ideas behind the decisions I made along the way.

As always, to get a taste of what I’m talking about, let’s first take a look at a nice visualization of the final result:

Press enter or click to view image in full size

![]()

Let’s get started.

First, we need to create a directive. We want to prevent consumers from adding specific selectors to apply our directive, so we take advantage of existing selectors and target them.

Next, we must obtain a reference to the current control instance in our directive. Luckily, Angular has simplified the process and [provides](https://github.com/angular/angular/blob/master/packages/forms/src/directives/reactive_directives/form_control_name.ts#L25) the injectable — `NgControl`.

Great, we have the control instance. Now, our goal is to display an error only when the user begins to interact with the field. To do so, we can use the control’s `valueChanges` observable.

Before we continue, we need to provide an error map. The `key` will be the error name and the `value` the text that will be displayed to the user. We don’t want to repeat this in each control, as the texts will likely be the same for each control. So instead, we’ll provide this via DI.

Note that we’re also bypassing the `error` object for more advanced errors. Now that we have the errors, let’s continue with the directive implementation.

We’re checking to see if the `control` contains errors. If it does, we grab the first error and find the error text we need to display.

Before we continue and learn how to display the error text, we’re still missing one crucial thing. Currently, we’re showing errors only if the user interacts with the fields. But what will happen if the user clicks on the submit button without any interaction? We need to support this as well by showing errors upon submit. Let’s see how can we do that.

Again, we’ll leverage directives and CSS selectors to expose a stream via a submitting action.

The directive is straight-forward. It targets any form in our application and exposes the `submit$` observable. In real life you’ll probably choose a more specific selector, like `form[appForm]`. We’re also using the `shareReplay()` operator, as we always want to create one event listener and not one per control.

Let’s use it in our directive.

First, we ask for Angular’s DI to provide us with a reference to the directive. We mark this directive as `Optional()`, because we also want to support **standalone controls** that don’t exist within a form tag. In such a case, we’re using the `EMPTY` observable that doesn’t do anything and immediately completes.

Ok, now that we’ve obtained the error text, how should we show it to our users? Your initial instinct will probably be to use the native JS API, create a new element, append the text, etc. But, I don’t recommend this, as the code won’t scale.

A better option would be to use Angular, and I will explain why in a minute. Let’s create a component we’ll use in order to show the text.

We’ve created a simple component that takes a text and displays it with proper error styles. The component also applies a display `none` rule if the error text is `null`. Now, let’s render the component in our directive.

This first time we’re inside the error handler, we create the component dynamically and set the current text error. If you’re not familiar with creating dynamic components in Angular, I recommend reading one of my [previous](https://netbasal.com/dynamically-creating-components-with-angular-a7346f4a982d) articles: Dynamically Creating Components with Angular.

As I mentioned before, the benefits of using Angular are that (1) we don’t need to clean the DOM by ourselves, but more importantly, (2) we have Angular’s power. Imagine you need to add a tooltip to the error message (`[appTooltip]` directive) or you want to give consumers the ability to override the default component template and provide a custom template (`*ngTemplateOutlet`). **The possibilities are endless.**

Ok, we’re almost there. But our code is still not flexible enough, as we’re limiting the error component to always render as a *sibling* to our host element, and there will be cases where we don’t want this behavior.

We need to be able to provide a different parent element that will act as our container. Again, directives to the rescue.

Yes, That’s about all. The only thing that we need now is a reference to the host `ViewContainerRef`. Let’s use it in our directive.

If someone declares the `controlErrorContainer`, we use his container; otherwise we’ll use the current host container.

**Note:** I will use it with caution as it may lead to undesired results. I’ll let you think about why.

Let’s finish by adding the input’s error style. To achieve this, we’ll simply add a `submitted` class to our form and use only CSS.

And our CSS will be:

That way we cover both the dirty and the submit behavior.

## Bonus

Currently, our directive supports only `formControl`, but we can easily add support for both `formGroup` and `formArray` by optionally injecting the `ControlContainer` [provider](https://github.com/angular/angular/blob/master/packages/forms/src/directives/reactive_directives/form_group_directive.ts#L20) that provides a reference to the current form group/array instance and using it as the control instance (if it exists).

Also, in the final demo, you can see support for custom local errors via `input`.

## Summary

We learned how to utilize the power of directives in Angular to create a clean form validation errors implementation. We also discussed why you should use Angular’s API so your code can easily scale.

## 🔥 **Last but Not Least, Have you Heard of Akita?**

Akita is a state management pattern that we’ve developed here in Datorama. It’s been successfully used in a big data production environment, and we’re continually adding features to it.

Akita encourages simplicity. It saves you the hassle of creating boilerplate code and offers powerful tools with a moderate learning curve, suitable for both experienced and inexperienced developers alike.

I highly recommend checking it out.

[## 🚀 Introducing Akita: A New State Management Pattern for Angular Applications

### Every developer knows state management is difficult. Continuously keeping track of what has been updated, why, and…

netbasal.com](https://netbasal.com/introducing-akita-a-new-state-management-pattern-for-angular-applications-f2f0fab5a8?source=post_page-----1e32350b7fa5---------------------------------------)

*Follow me on* [*Medium*](/@NetanelBasal/) *or* [*Twitter*](https://twitter.com/NetanelBasal) *to read more about Angular, Akita and JS!*