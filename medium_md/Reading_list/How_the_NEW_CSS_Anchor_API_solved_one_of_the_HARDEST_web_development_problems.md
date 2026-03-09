---
title: "How the NEW CSS Anchor API solved one of the HARDEST web development problems"
url: https://medium.com/p/69ce290ac95e
---

# How the NEW CSS Anchor API solved one of the HARDEST web development problems

[Original](https://medium.com/p/69ce290ac95e)

Member-only story

# How the NEW CSS Anchor API solved one of the HARDEST web development problems

[![Arnold Gunter](https://miro.medium.com/v2/resize:fill:64:64/1*TAhisa8nN_coYYb4QZuehw.jpeg)](/@arnoldgunter?source=post_page---byline--69ce290ac95e---------------------------------------)

[Arnold Gunter](/@arnoldgunter?source=post_page---byline--69ce290ac95e---------------------------------------)

5 min read

·

Jan 28, 2025

--

26

Listen

Share

More

[Read it here for free](/@arnoldgunter/69ce290ac95e?sk=a89d74a08f0c37797c4840fdbc722090)

Press enter or click to view image in full size

![]()

It was a boring afternoon, and I was watching some YouTube videos when I stumbled across an [advertisement from Google](https://www.youtube.com/watch?v=LjkraMIWPEY).

The idea immediately got me hyped.

> Build interactive, engaging web interfaces with CSS anchor positioning and popover elements. Create tooltips, hover cards, or overlays anchored to an element with only a few lines of CSS and HTML — no JavaScript or complex layouts required.

How amazing is that?!

Okay let’s see how it works…

**Level up your CSS skills —** [**check out my new ebook on mastering Subgrid!**](https://arnoldgunter.gumroad.com/l/rlrnp)

## What is the CSS Anchor API?

The CSS Anchor API introduces a way to position and align elements dynamically in relation to a specific anchor element — without relying on JavaScript or convoluted layout hacks.

Think of tooltips, popovers, and hover cards that need to follow an anchor element.

In the past, achieving this required JavaScript gymnastics or complex CSS. Now, the Anchor API streamlines this process to just a few lines of CSS and HTML.

## Before: The Old Way (Painful but Necessary)

Imagine you need a tooltip to appear below a button when hovered. Back in the day, here’s how you’d typically do it:

```
<button id="myButton">Hover me</button>  
<div id="tooltip">I’m a tooltip!</div>
```

```
#tooltip {  
  display: none;  
  position: absolute;  
  background: #333;  
  color: #fff;  
  padding: 5px;  
  border-radius: 5px;  
}
```

```
const button = document.getElementById('myButton');  
const tooltip = document.getElementById('tooltip');  
  
button.addEventListener('mouseover', () => {  
  const rect = button.getBoundingClientRect();  
  tooltip.style.display = 'block';  
  tooltip.style.top = `${rect.bottom + window.scrollY}px`;  
  tooltip.style.left = `${rect.left + window.scrollX}px`;  
});  
button.addEventListener('mouseout', () => {  
  tooltip.style.display = 'none';  
});
```

Yikes! That’s a lot of work just to align a tooltip.

You have to calculate element positions, handle scrolling, and add event listeners. Now enter the CSS Anchor API.

## After: The New Way (Goodbye JavaScript!)

Here’s how you’d do the same thing with the Anchor API:

```
<button popover-anchor="tooltip">Hover me</button>  
<div popover id="tooltip">I’m a tooltip!</div>
```

```
[popover-anchor] {  
  position: relative;  
}  
  
[popover] {  
  position: anchor;  
  anchor-name: tooltip;  
  anchor-offset: 0 8px; /* 8px below the anchor */  
  background: #333;  
  color: #fff;  
  padding: 5px;  
  border-radius: 5px;  
}  
  
button:hover + [popover] {  
  display: block; /* Show when button is hovered */  
}
```

**That’s it.** No JavaScript. No manual calculations. Just clean, declarative HTML and CSS.

![]()

## How It Works

* `position: anchor;`: This positions the element relative to the specified anchor.
* `anchor-name: tooltip;`: Matches the anchor name in your button element to identify where the tooltip is anchored.
* `anchor-offset: 0 8px;`: Defines the offset (horizontal and vertical) between the anchor and the positioned element.

The tooltip is automatically positioned, and it stays in sync even if the anchor element moves or scrolls. Magic, right?

## Supported Properties in the CSS Anchor API

Here are the properties supported by the CSS Anchor API and what they do:

1. `anchor-name`: Specifies the name of the anchor element that another element should be positioned relative to.
2. `position-anchor`: Defines the specific anchor point (e.g., top, bottom, left, right) on the anchor element to which the positioned element should align.
3. `position-area`: Determines the area around the anchor element where the positioned element is allowed to be placed.
4. `position-try-fallbacks`: Provides a list of fallback anchor positions if the preferred position is unavailable (e.g., due to space constraints).
5. `position-try-order`: Defines the order in which fallback positions are attempted when the preferred position cannot be used.
6. `position-try` **(shorthand)**: A shorthand property combining the preferred position and fallbacks into one concise declaration.
7. `position-visibility`: Specifies the visibility rules for the positioned element (e.g., whether it should remain visible if it cannot fit in the specified area).

These properties work together to make positioning both precise and flexible, ensuring that your layouts adapt to various screen sizes and edge cases seamlessly.

## Main Advantages of the CSS Anchor API

1. **Simplicity**: No more event listeners or manual position calculations. Everything is handled with a couple of CSS properties.
2. **Performance**: By offloading layout updates to the browser, you reduce the overhead of JavaScript calculations. This leads to smoother interactions and better performance.
3. **Better Maintainability**: Your codebase stays clean and declarative. Future developers (or future you) will thank you.
4. **Browser Native**: This is handled directly by the browser, which means less room for bugs or inconsistencies compared to JavaScript solutions.

## Bonus Example: Popovers with Interactive Content

The Anchor API also works beautifully for more complex use cases, like interactive popovers.

```
<button popover-anchor="popoverMenu">Click me</button>  
<div popover id="popoverMenu">  
  <ul>  
    <li><a href="#">Option 1</a></li>  
    <li><a href="#">Option 2</a></li>  
    <li><a href="#">Option 3</a></li>  
  </ul>  
</div>
```

```
[popover-anchor] {  
  position: relative;  
}  
  
[popover] {  
  position: anchor;  
  anchor-name: popoverMenu;  
  anchor-offset: 0 12px;  
  background: #fff;  
  border: 1px solid #ccc;  
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);  
  border-radius: 5px;  
  padding: 10px;  
}  
  
button:hover + [popover] {  
  display: block; /* Show when button is hovered */  
}
```

With no extra JavaScript, you now have a fully functional, anchored popover that’s beautifully (okay I admit there are rooms for improvement) styled and easy to maintain.

![]()

## Browser Support

CSS Anchor Positioning is gaining support in major browsers like Chrome, Edge, and Opera, while Firefox unfortunately and Safari (as usual), lag behind. Developers targeting Apple devices may need workarounds until Safari catches up — whenever that may be!

Press enter or click to view image in full size

![]()

## Why the Anchor API is a Game-Changer

In web development, simplicity often equals happiness. The CSS Anchor API eliminates the headaches of dynamic positioning, makes your codebase leaner, and ensures your interfaces work as expected across devices.

No more fiddling with `getBoundingClientRect` or worrying about edge cases when an anchor element moves or scrolls.

So the next time you’re building a tooltip, hover card, or popover, give the Anchor API a shot. Your future self will thank you, and your users will enjoy seamless, polished interactions.

**Happy coding!**

**Level up your CSS skills —** [**check out my new ebook on mastering Subgrid!**](https://arnoldgunter.gumroad.com/l/rlrnp)