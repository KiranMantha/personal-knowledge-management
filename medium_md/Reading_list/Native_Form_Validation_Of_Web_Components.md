---
title: "Native Form Validation Of Web Components"
url: https://medium.com/p/a599e85176c7
---

# Native Form Validation Of Web Components

[Original](https://medium.com/p/a599e85176c7)

Member-only story

# Native Form Validation Of Web Components

[![Danny Moerkerke](https://miro.medium.com/v2/resize:fill:64:64/1*LNE7VNHhYk__VDTzO8InnA.jpeg)](https://medium.com/@dannymoerkerke?source=post_page---byline--a599e85176c7---------------------------------------)

[Danny Moerkerke](https://medium.com/@dannymoerkerke?source=post_page---byline--a599e85176c7---------------------------------------)

14 min read

·

Sep 14, 2022

--

3

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Da599e85176c7&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fnative-form-validation-of-web-components-a599e85176c7&source=---header_actions--a599e85176c7---------------------post_audio_button------------------)

Share

A thorough guide to easy, native form validation

Press enter or click to view image in full size

![]()

In my previous article “[Web Components Can Now Be Native Form Elements](https://javascript.plainenglish.io/web-components-can-now-be-native-form-elements-107c7a93386)” I explained how the `ElementInternals` object can be used to make Web Components participate in forms just like any other native form element.

In this article I will explain how you can easily validate these custom form controls using nothing but the native platform

## Native form validation

A crucial part of working with forms on the web is validation: checking if the input the user provided is what we expect it to be and showing feedback to the user when it’s not.

When you provide a custom form control it should therefore participate in this form validation like any native form control.

While there are many libraries available for this, the native platform already provides all the tools you need to validate forms.

## Constraints

To validate a form you first need to define when a form control is valid or invalid. In other words, you will need to set *constraints* for the controls.

For example, you can define if a field is required or if its data should be of a certain type or have a maximum length.