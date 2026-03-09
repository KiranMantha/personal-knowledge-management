---
title: "Material design styled inputs with CSS."
url: https://medium.com/p/626e7f01681a
---

# Material design styled inputs with CSS.

[Original](https://medium.com/p/626e7f01681a)

# Material design styled inputs with CSS.

[![Will Bowman](https://miro.medium.com/v2/resize:fill:64:64/1*dJsDwIN_GL5AshXZkWRFew.jpeg)](/@asked_io?source=post_page---byline--626e7f01681a---------------------------------------)

[Will Bowman](/@asked_io?source=post_page---byline--626e7f01681a---------------------------------------)

2 min read

·

Sep 4, 2016

--

3

Listen

Share

More

Press enter or click to view image in full size

![]()

**TL;DR** [View the example.](http://codepen.io/anon/pen/yayOXk)

Last year, when I was using jQuery and Bootstrap, I wrote a [snippet](http://bootsnipp.com/user/snippets/V0dqb) (and [article](https://asked.io/fancy-bootstrap-forms-using-placeholders---labels)) that copied Digital Oceans style of form placeholders.

![]()

This worked well, and I still use it, but the animations are awful and well — it uses jQuery.

While looking at the Angular Material Design version I figured a simple input and label would be enough to get the job done, and as you can see, it was.

![]()

**There is a CSS hack:** The ***required*** option is used to indicate if the field has a value, there are other ways to do this — with javascript — if your fields are not all required.

## The Code

[View the example.](http://codepen.io/anon/pen/yayOXk)

Looking for the CSS? Goto the [code pin](http://codepen.io/anon/pen/yayOXk) and..

![]()

## Conclusion

I kept it simple, mostly because my design won’t be yours. I’ll probably add in some Angular 2 code to get rid of the required hack, but maybe not (I have basic forms)

I did minimal testing (Android, Chrome, Firefox, Safari) and it seems to work well, there isn’t much to it.