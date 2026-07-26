---
title: "The Hidden Power of Custom States For Web Components"
url: https://medium.com/p/dcae5b048e20
---

# The Hidden Power of Custom States For Web Components

[Original](https://medium.com/p/dcae5b048e20)

Member-only story

# The Hidden Power of Custom States For Web Components

[![Danny Moerkerke](https://miro.medium.com/v2/resize:fill:64:64/1*LNE7VNHhYk__VDTzO8InnA.jpeg)](https://medium.com/@dannymoerkerke?source=post_page---byline--dcae5b048e20---------------------------------------)

[Danny Moerkerke](https://medium.com/@dannymoerkerke?source=post_page---byline--dcae5b048e20---------------------------------------)

7 min read

·

Nov 16, 2022

--

4

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Ddcae5b048e20&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fthe-hidden-power-of-custom-states-for-web-components-dcae5b048e20&source=---header_actions--dcae5b048e20---------------------post_audio_button------------------)

Share

A crucial step in the evolution of Custom Elements

Press enter or click to view image in full size

![]()

In my previous articles “[Web Components Can Now Be Native Form Elements](https://javascript.plainenglish.io/web-components-can-now-be-native-form-elements-107c7a93386)” and “[Native Form Validation Of Web Components](/native-form-validation-of-web-components-a599e85176c7)”, I wrote about the `ElementInternals` property that enables Custom Elements to be associated with a form.

This interface also enables developers to associate custom states with Custom Elements and style them based on these states.

The `states` property of `ElementInternals` returns a `CustomStateSet` that stores a list of possible states for a Custom Element to be in, and allows states to be added and removed from the set.

Each state in the set is represented by a string and currently there are two types of syntax for that:

* old syntax: `--mystate` (to be deprecated)
* new syntax: `mystate`

> Currently, Chrome supports the old syntax and Safari Tech Preview and Firefox Nightly support the new syntax. Chrome will implement the new syntax soon and keep the old syntax as well for a while for backwards compatibility.

These states can then be accessed from CSS with the custom state pseudo-class in the same way that built-in states can be accessed.