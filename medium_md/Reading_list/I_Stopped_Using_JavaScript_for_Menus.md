---
title: "I Stopped Using JavaScript for Menus"
url: https://medium.com/p/f94335faf876
---

# I Stopped Using JavaScript for Menus

[Original](https://medium.com/p/f94335faf876)

Member-only story

# I Stopped Using JavaScript for Menus

## HTML and CSS now handles what JS used to

[![Tushar Kanjariya](https://miro.medium.com/v2/resize:fill:64:64/2*lSBGQKdOUsG8qNMLANgd1w.jpeg)](/@TusharKanjariya?source=post_page---byline--f94335faf876---------------------------------------)

[Tushar Kanjariya](/@TusharKanjariya?source=post_page---byline--f94335faf876---------------------------------------)

4 min read

·

Jan 2, 2026

--

3

Listen

Share

More

For years, I wrote the same 100 lines of JavaScript every time I needed a dropdown.

> [Read Free](/@TusharKanjariya/i-stopped-using-javascript-for-menus-f94335faf876?sk=2457c5b79e0e8016e7818c1b6e8519ab) for non-members.

Calculate position. Track scroll. Handle resize. Fix mobile bugs. Add escape key logic. Patch the weird stuff that only breaks in production.

Not because I liked it.

Because I thought I had no choice.

Then one day, while playing with modern CSS, I realized something uncomfortable:

**The browser was already doing the hard part.**

Press enter or click to view image in full size

![I Stopped Using JavaScript for Menus | Tushar Kanjariya]()

### The real problem with menus

Menus are simple UI elements.

They just need to:

* Open near the trigger
* Stay attached while scrolling
* Never overflow the screen
* Close correctly

Yet we’ve been solving this with JavaScript math for years.

Mostly because **CSS couldn’t express intent**.

Now it can.

### Native popover changed everything

HTML now has a native `popover` attribute.

And it instantly removes a surprising amount of JavaScript.

```
<button popovertarget="menu">Profile</button>  
  
<div id="menu" popover>  
  <a href="#">Settings</a>  
  <a href="#">Logout</a>  
</div>
```

No click handler.

No state management.

No JS.

The browser handles opening, closing, focus, and escape behavior.

All I control is **how it looks when open.**

```
#menu:popover-open {  
  display: grid;  
}
```

One important lesson I learned early:

> **Never set** `display` **on the base selector**, or the popover will never close.

### Why it opens in the center (and how to fix it)

By default, the browser treats popovers like dialogs.

This confused me until I saw what the browser does:

```
position: fixed;  
inset: 0;  
margin: auto;
```

Makes sense for modals. Terrible for menus.

So we reset it.

### Attach(Anchoring) the menu to the button (this is the magic)

Instead of calculating positions in JavaScript, CSS now lets us say:

> “This menu belongs to that button.”

**Step 1: Name the anchor**

```
.user-button {  
  anchor-name: --user;  
}
```

**Step 2: Attach the menu**

```
#menu {  
  position: absolute;  
  position-anchor: --user;  
  inset: auto;  
  top: anchor(bottom);  
  margin-top: 6px;  
}
```

The menu opens below the button.

Scrolls with the page.

Stays attached without any extra code.

This replaced most of my dropdown logic in many projects.

### Where I actually use this in real projects

This isn’t theoretical.

I use this pattern everywhere now.

### 1. Navbar “More” menus on small screens

Earlier, I handled this with JS:

* Detect screen size
* Flip menu direction
* Recalculate on resize

Now I don’t.

```
#more-menu {  
  top: anchor(bottom);  
  left: anchor(left);  
}  
  
@position-try --flip {  
  top: anchor(bottom);  
  right: anchor(right);  
}  
  
#more-menu {  
  position-try-fallbacks: --flip;  
}
```

The browser flips the menu **only when needed**.

No media queries.

No resize listeners.

### 2. Three-dot action menus inside cards

Every dashboard has these.

The problem is scroll containers.

JS dropdowns usually break here.

With popovers + anchors:

```
.card-actions {  
  anchor-name: --actions;  
}  
  
.actions-menu {  
  position-anchor: --actions;  
  top: anchor(bottom);  
}
```

Because the menu is `position: absolute`, it scrolls naturally with the card.

No hacks.

No sync logic.

### 3. Avatar menus in sticky headers

Sticky headers + dropdowns used to be painful.

Scroll once → menu floats

Scroll again → menu desyncs

With CSS anchors, this problem disappears.

The browser understands layout context better than we do.

This felt like cheating the first time I saw it work.

### 4. Filter dropdowns near screen edges

Filters often sit close to edges.

Instead of writing logic like:

> “If near right edge, open left…”

I let CSS decide.

```
@position-try --left {  
  right: anchor(left);  
}
```

If it fits → fine.

If not → fallback kicks in.

No manual math.

### Handling overflow without JavaScript

This is where `@position-try` shines.

It lets CSS say:

> “Try this position. If it overflows, try another.”

```
@position-try --right {  
  inset: auto;  
  top: anchor(bottom);  
  right: anchor(right);  
}  
  
#menu {  
  position-try-fallbacks: --right;  
}
```

The browser only applies the fallback **when overflow would happen**.

No jumping.

No guessing.

### Adding animation (cleanly)

Animating menus used to require hacks.

Now it’s simple.

```
#menu {  
  opacity: 0;  
  transition: opacity 0.3s ease, display 0.3s ease;  
  transition-behavior: allow-discrete;  
}  
  
#menu:popover-open {  
  opacity: 1;  
}
```

Unsupported browsers just ignore it.

That’s progressive enhancement done right.

### Browser support (the honest part)

* Chrome, Edge, Safari → works
* Firefox → not yet

There’s a small polyfill:

```
<script type="module" src="https://unpkg.com/css-anchor-polyfill@latest"></script>
```

I use it in production. Works fine.

Best part: supported browsers ignore it completely.

### When I still use JavaScript (important)

This is not an anti-JavaScript post.

I still use JS when:

* The menu content is dynamic
* Position depends on pointer coordinates
* I need complex keyboard logic
* The UI must support very old browsers
* The menu is part of a larger state machine

CSS handles **layout and positioning** beautifully now.

JS is still great for **behavior and data**.

The win is knowing **where each belongs**.

### Why I actually stopped using JS here

This wasn’t about trends.

It was about maintenance.

With native popovers and anchors, I get:

* Less code
* Fewer bugs
* Better accessibility
* Cleaner intent
* Easier refactors

Menus finally became boring.

And boring UI is stable UI.

### Conclusion

If you’re still writing JavaScript just to:

* Open menus
* Position dropdowns
* Handle overflow
* Fix scroll issues

Take another look at modern CSS.

I didn’t stop using JavaScript because I wanted to.

I stopped because **I didn’t need it anymore**.

And that’s the best kind of refactor.

Thanks for reading 🙏

Connect with me 👇

[## Tushar Kanjariya | Linktree

### Full Stack Developer who occasionally writes

linktr.ee](https://linktr.ee/TusharKanjariya?source=post_page-----f94335faf876---------------------------------------)