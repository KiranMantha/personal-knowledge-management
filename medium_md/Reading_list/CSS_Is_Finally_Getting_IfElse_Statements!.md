---
title: "CSS Is Finally Getting If/Else Statements!"
url: https://medium.com/p/3fabcec72a1f
---

# CSS Is Finally Getting If/Else Statements!

[Original](https://medium.com/p/3fabcec72a1f)

Member-only story

# CSS Is Finally Getting If/Else Statements!

[![Kenton de Jong](https://miro.medium.com/v2/resize:fill:64:64/1*03zVqD8dodsM7h8nFuFW9A.jpeg)](/?source=post_page---byline--3fabcec72a1f---------------------------------------)

[Kenton de Jong](/?source=post_page---byline--3fabcec72a1f---------------------------------------)

3 min read

·

Oct 9, 2021

--

17

Listen

Share

More

Press enter or click to view image in full size

![]()

When I started coding CSS in 2011 (*wow*) I could never have suspected how much the language would change. I still remember using PIE.htc to make `border-radius` work across all browsers, and my coworker making a PHP script that generated a PNG to round corners.

How far we have come!

![]()

However, the past few years have rolled out an explosive amount of new CSS features. Some of these could be perceived as “if statements” too, like the `@supports` style:

```
@supports (border-radius: 50%) {  
   //don't use PIE.htc! {}  
}
```

(Do you think my CSS comment is a typeo? It’s not. CSS does have single-line comments. [They’re just a little weird.](https://medium.com/geekculture/does-css-support-single-line-comments-1d7acbdd22d8))

There is also the classic media query too, which has been around for over a decade:

```
@media (max-width: 1000px) {  
  //maybe a mobile sized device? {}  
}
```

There’s also the new `clamp()` which is a little different, but looks like this:

```
width: clamp(1000px, 50%, 10vw);
```

But acts like this:

```
width: clamp(1000px >= (50% >= 10vw));
```

![]()

But those are arguable just “if statements”. If we wanted an “if/else statement” we would need to do something like this:

```
@media (max-width: 1000px) and (prefers-color-scheme: dark) {  
   //maybe a mobile device in dark mode {}  
}@media (max-width: 1000px) and (prefers-color-scheme: light) {  
   //maybe a mobile device in light mode {}  
}
```

Which is annoying.

But thankfully we can be annoyed no more with the newly proposed `@when` statement. It works something like this:

```
@when media(max-width: 1000px) {  
   //maybe a mobile device {}  
}
```

Which is cool, I guess. But what about an else?

```
@when media(max-width: 1000px) {  
   //maybe a mobile device {}  
} @else {  
   ///maybe a desktop{}  
}
```

And an else if!?

```
@when media(max-width: 1000px) {  
   //maybe a mobile device {}  
} @else media(max-width: 700px) { {  
   ///totally a mobile device{}  
} @else {  
   //a desktop or tablet{}  
}
```

![]()

We could probably even do something like this too:

```
@when media(max-width: 700px) {  
   @when (prefers-color-scheme: dark) {  
      //dark mode on mobile device  
   } @else {  
      //light mode on mobile device   
   }  
}
```

I say “probably” [because the spec is still in consideration](https://tabatkins.github.io/specs/css-when-else/), but hey, [if Chris Coyier is celebrating it already](https://css-tricks.com/proposal-for-css-when/), we can too!

But I know what you’re thinking. Why the `@s` ? Other languages don’t need them. The going theory is that due to SASS using `@if` , they are worried about breaking sites. The whole concept of web development is not to break websites. This is nice, but I don’t think a web standard should cater to third-party software, [especially since SASS also uses](https://sass-lang.com/documentation/at-rules/control/if) `@else`[already.](https://sass-lang.com/documentation/at-rules/control/if)

![]()

What does the browser support look like at the time of writing (Oct 8, 2021)? Zilch. So little that it isn’t even on [Can I Use?](https://caniuse.com/?search=%40when). But with new CSS styles rolling out all the time, I’m sure we’ll see it soon enough.

What are your thoughts on the proposed if/if-else statements? Let me know in the comments.