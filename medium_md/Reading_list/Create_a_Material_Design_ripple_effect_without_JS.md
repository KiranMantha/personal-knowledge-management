---
title: "Create a Material Design ripple effect without JS"
url: https://medium.com/p/9d3cbee25b3e
---

# Create a Material Design ripple effect without JS

[Original](https://medium.com/p/9d3cbee25b3e)

# Create a Material Design ripple effect without JS

## Goodbye JavaScript 👋

[![Vaibhav Khulbe](https://miro.medium.com/v2/resize:fill:64:64/2*uCsd8FI_d-XTL4wzD515wg.jpeg)](https://medium.com/@vaibhavkhulbe?source=post_page---byline--9d3cbee25b3e---------------------------------------)

[Vaibhav Khulbe](https://medium.com/@vaibhavkhulbe?source=post_page---byline--9d3cbee25b3e---------------------------------------)

4 min read

·

Jun 15, 2018

--

7

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D9d3cbee25b3e&operation=register&redirect=https%3A%2F%2Fcodeburst.io%2Fcreate-a-material-design-ripple-effect-without-js-9d3cbee25b3e&source=---header_actions--9d3cbee25b3e---------------------post_audio_button------------------)

Share

Okay, so this one will be real quick to implement. I know most of you already know how to create a great ripple effect on `buttons`, `menus` and other `div` elements using JavaScript (JS). Well, initially I was one of those who was scared of JS as a language to bring out interactivity on the front-end. I used to think *“Why do we even need such a language which had lots of declarations, loops, functions and what not while making just the front-end of a website?”* . Yeah, I was so wrong and wrong about this. Why not just eliminate the need of JS for a moment and focus more on our beautiful CSS?

## What will I make? 🤔

This:

![]()

Not this:

Yeah, that button doesn’t look really cool. It’s okay, **you’re not using a single line of JS in this project** and you need to compromise that. This is the only point, ***no JS only CSS***, and uh, of course HTML…

## What is a Material Design❔

Honestly, this design theme is brought to you by Google years back at their Google I/O 2014 event. Now you’re using this theme on your Android smartphones, some websites and yes, all other ‘Googly’ things from sometime. It’s like some flat elements on top of a website or app, but it’s not limited to that.

### What exactly ‘Material’ means?

Well, if we were to believe [Envato](https://envato.com/blog/introduction-material-design/),

> Google’s Material design considers material to be a homogeneous digital “fabric” created with pixels. Users can tap, swipe, or pinch this material fabric and it will move according to user interaction.

You can learn more about the same in 

[Daniel Hollick](https://medium.com/u/c142f50c335?source=post_page---user_mention--9d3cbee25b3e---------------------------------------)

’s [blog post](https://medium.com/@danhollick/material-design-is-design-science-6c99c1d76498) or refer to [Google Design publication](https://medium.com/google-design).

## What will I need? 🛠️

* H̸a̸m̸m̸e̸r̸ ̸a̸n̸d̸ ̸w̸r̸e̸n̸c̸h̸
* Your already wonderful HTML and CSS skills.
* A text editor (I’ll be using [Atom](https://atom.io/) just because for [my last tutorial on Flutter](/quick-start-flutter-on-windows-9391fc0ce023) I used VS Code…)

## Shall we…ripple?

Let’s do what we had done before. Create a folder, add two files namely `index.html` and `style.css`. Start with HTML. I hope you’re already familiar with Atom’s shortcuts. I think this one is really handy:

Press enter or click to view image in full size

![]()

Now we have the most basic structure of a HTML file you can think of. A `head`, a `title`, a `meta` and the `body` tag. First, we gonna link our CSS file in this. That means, using `<link rel=”stylesheet” href=”style.css”>` inside our `<head>`. Give it a suitable `<title>` like *Material Ripple Effect.*

We’ll now add a `class`, say *container* in the `<body>` . Just like this:

Press enter or click to view image in full size

![]()

Inside this `container` class, we’ll add a `button` element. Don’t forget to add a class like `class=”btn ripple”` . Both the `btn` and `ripple` will be used individually in our styling.

At last, this will be our final HTML code:

Let’s hover to styling. All the materialistic magic will happen here. I’ll only write what all you need to make the button materialistic on click. So, your `style.css` file should have the following:

1. [**Container**](https://www.w3schools.com/w3css/w3css_containers.asp): `display` property set to `flex` to make it of same length regardless of the content.
2. **Ripple**: `transform` property set to `translate3d` to define a 3D translation.
3. **Ripple-after**: this is where the ripple effect ends. We can show something like a text but it doesn’t make sense here. Therefore the `content` has been set to `""`.

* `background-image`'s value has been set to the `radial-gradient` function which takes in a `circle` as its `shape`, `#fff` or white as the `start-color` and `last-color` as `transparent 10.01%`.
* `transition` is used along with `transform` with its corresponding timing and `opacity`.

If that felt too overwhelming for you in first go, try to implement the same again and use the documentation links to dive deeper in those elements. Obviously, there is some more code other than this. Take a look at our final `style.css` file:

That’s it! No JS! Run the `.html` in your favorite web browser and see for yourself. You’ll have a `container` and a `button` with Material ripple effect!

## Where to next? 🤔

You can experiment more with the `.container`, `.ripple`, `.ripple:after` and `.ripple:active:after` in your style sheet. Or if you want to be more like a ninja 🐱‍👤, *you can tell me how to start the ripple from different places on the button*. Like, if I click on lower left side of the button, the ripple should originate from there.

The source code for this project is hosted on GitHub (and not GitLab 😉):

[## Kvaibhav01/Ripple-without-JS

### Ripple-without-JS - Create Material Design ripple effect in your HTML without using a single line of JavaScript code.

github.com](https://github.com/Kvaibhav01/Ripple-without-JS?source=post_page-----9d3cbee25b3e---------------------------------------)

### You can now see LIVE DEMO [here](https://kvaibhav01.github.io/Ripple-without-JS/), thanks to GitHub Pages.

### Liked this story? Feel free to clap and motivate me to write more and better. Did I missed something? Any suggestions? The comment box below serves the exact purpose!

[![]()](http://bit.ly/codeburst)

> ✉️ *Subscribe to* CodeBurst’s *once-weekly* [***Email Blast***](http://bit.ly/codeburst-email)***,*** 🐦 *Follow* CodeBurst *on* [***Twitter***](http://bit.ly/codeburst-twitter)*, view* 🗺️ [***The 2018 Web Developer Roadmap***](http://bit.ly/2018-web-dev-roadmap)*, and* 🕸️ [***Learn Full Stack Web Development***](http://bit.ly/learn-web-dev-codeburst)*.*