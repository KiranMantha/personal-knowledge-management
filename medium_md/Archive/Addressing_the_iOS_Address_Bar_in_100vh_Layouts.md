---
title: "Addressing the iOS Address Bar in 100vh Layouts"
url: https://medium.com/p/46e78d54af0d
---

# Addressing the iOS Address Bar in 100vh Layouts

[Original](https://medium.com/p/46e78d54af0d)

# Addressing the iOS Address Bar in 100vh Layouts

## It’s not a bug, it’s a feature.

[![Susie Kim](https://miro.medium.com/v2/resize:fill:64:64/1*CaCVKWu3BCrGcwDaXJQjug.jpeg)](/@susiekim9?source=post_page---byline--46e78d54af0d---------------------------------------)

[Susie Kim](/@susiekim9?source=post_page---byline--46e78d54af0d---------------------------------------)

4 min read

·

Sep 6, 2018

--

22

Listen

Share

More

As I deployed my first PSD conversion with its beautiful 100vh and 100vw hero image, I was horrified to discover that the bottom of my layout was hidden when viewed from my iPhone 6s iOS 10 Safari. Why? I thought I did everything right! Did I accidentally add margin or padding somewhere? What was I overlooking?

Upon closer inspection, I quickly realized that although my hero image was in fact 100vh, it was partially covered by Safari’s address and tool bar, creating the dreaded “wiggle-scroll”. That’s fine, I thought. Nothing a quick search on Google and Stack Overflow can’t fix. However, I learned that the solution isn’t quite so straightforward.

After doing some research, I realized it was a fairly common complaint, referred to by some as the “iOS viewport scroll bug”. In February of 2015, [Nicolas Hoizey](https://nicolas-hoizey.com/2015/02/viewport-height-is-taller-than-the-visible-part-of-the-document-in-some-mobile-browsers.html) reported the bug on Webkit Bugzilla when he discovered the bottom of his 100vh mobile game was cut off by the browser buttons bar. Benjamin Poulain, an engineer at Apple replied to Hoizey . He stated — in true programmer fashion — that it wasn’t a bug, it’s a feature.

> This is completely intentional. It took quite a bit of work on our part to achieve this effect. :)  
>   
> The base problem is this: the visible area changes dynamically as you scroll. If we update the CSS viewport height accordingly, we need to update the layout during the scroll. Not only that looks like shit, but doing that at 60 FPS is practically impossible in most pages (60 FPS is the baseline framerate on iOS).  
>   
> It is hard to show you the "looks like shit" part, but imagine as you scroll, the contents moves and what you want on screen is continuously shifting.  
>   
> Dynamically updating the height was not working, we had a few choices: drop viewport units on iOS, match the document size like before iOS 8, use the small view size, use the large view size.  
>   
> From the data we had, using the larger view size was the best compromise. Most website using viewport units were looking great most of the time.

I for one, am not an engineer at Apple, so I believe him when he says there are good reasons behind why they designed this behaviour. Thus, the bug was marked “RESOLVED WONTFIX”, and I realized I would have to delve deeper if I ever wanted my beautiful, 100vh hero image.

### Solution 1: CSS Media Queries

This method, albeit not entirely elegant, is simple and easy to implement. Simply target all iOS devices with specific device-width and heights. Here is a code, courtesy of pburtchaell, where “.foo” would be a class on your full-height element.

```
@media all and (device-width: 768px) and (device-height: 1024px) and (orientation:portrait) {  
    .foo {                             
        height: 1024px;                           
    }                         
}     
                                              
/* iPad with landscape orientation. */                         
@media all and (device-width: 768px) and (device-height: 1024px) and (orientation:landscape) {                           
    .foo {                             
        height: 768px;                           
    }                         
}  
                                                 
/* iPhone 5   
You can also target devices with aspect ratio. */                       @media screen and (device-aspect-ratio: 40/71) {                                
    .foo {                             
        height: 500px;                           
    }                         
}
```

Looking at the code above, it appears a slight content overlap is inevitable. However, elements with positioning and sizing that depend on viewport units would remain constant. That’s a win! Adding something like a simple calc(100vh — heightOfBar) would compensate for the address bar. But with so many devices and browsers to support, this doesn’t seem like a sustainable solution.

### Solution 2: Targeting innerHeight with Javascript.

Inner measurements refer to the height/width of the viewport, taking into calculation vertical/horizontal scrolls bars. Now we’re talking! Here is a diagram of what this entails:

Press enter or click to view image in full size

![]()

Using this knowledge, you can use a simple script like this to set the height on page-load and keep it constant till resize, from Stack Overflow user [tobiq](https://stackoverflow.com/questions/43575363/css-100vh-is-too-tall-on-mobile-due-to-browser-ui):

```
window.onresize = function() {  
    document.body.height = window.innerHeight;  
}window.onresize(); // called to initially set the height.
```

### Solution 3: Div100vh React Component

Since we all love React, I wanted to find a solution catered to React Components. I found a npm package by [Mikhail Vasin](http://github.com/mvasin/react-div-100vh) that aims to fix this issue. Install like so:

```
npm install --save react-div-100vh
```

Then import the component and wrap your elements in it, like such:

```
import Div100vh from 'react-div-100vh';const MyFullscreenComponent = () => (  
    <Div100vh>  
       Your stuff goes here  
    </Div100vh>  
)
```

And there you go!

After testing these various solutions, I realize there isn’t a one-size-fits-all solution for this issue. So, please be diligent with your cross-browser, cross-device testing. And maybe avoid using vh/vw units for mobile altogether as buggy behaviour with these units is well-documented in mobile browsers.

Let me know if these solutions were helpful to you, and which ones worked best!

**February 26, 2021 - Update: You could also try** [webkit-fill-available](https://allthingssmitty.com/2020/05/11/css-fix-for-100vh-in-mobile-webkit/)!