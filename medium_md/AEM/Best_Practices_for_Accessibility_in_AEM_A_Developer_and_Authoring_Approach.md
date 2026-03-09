---
title: "Best Practices for Accessibility in AEM: A Developer and Authoring Approach"
url: https://medium.com/p/eb8d3d2e7597
---

# Best Practices for Accessibility in AEM: A Developer and Authoring Approach

[Original](https://medium.com/p/eb8d3d2e7597)

# **Best Practices for Accessibility in AEM: A Developer and Authoring Approach**

[![Mircea Gabriel Dumitrescu](https://miro.medium.com/v2/resize:fill:64:64/1*TW-JpYR1nk7ciXTnm9yAmA.png)](/@mirceagab?source=post_page---byline--eb8d3d2e7597---------------------------------------)

[Mircea Gabriel Dumitrescu](/@mirceagab?source=post_page---byline--eb8d3d2e7597---------------------------------------)

4 min read

·

Feb 12, 2025

--

1

Listen

Share

More

Press enter or click to view image in full size

![Best Practices for Accessibility in AEM: A Developer and Authoring Approach]()

## Introduction

Accessibility isn’t just a nice-to-have anymore — it’s essential. Making sure your digital experiences work for everyone, including people with disabilities, isn’t just about **checking a box**; it’s about building better, more inclusive websites. When it comes to **Adobe Experience Manager (AEM)**, both **developers** and **content authors** play a big role in keeping things accessible. Let’s dive into how both sides can make sure they’re not leaving anyone behind.

## 1. Developer Best Practices: Building Accessible AEM Components

## 1.1 Use Semantic HTML

Semantic HTML is the backbone of accessibility. It’s what makes sure assistive technologies, like screen readers, can **properly interpret and navigate** your page. If you’re just throwing everything into `<div>`s and `<span>`s, you’re setting yourself up for problems.

### Why does this matter?

* **Screen readers love it**: Proper headings, landmarks, and lists help screen readers announce content correctly.
* **Keyboard users benefit**: Logical structure makes it easier to navigate with just a keyboard.
* **SEO boost**: Search engines prefer well-structured content, so it’s a win-win.

### Example

❌ Bad: Using `<div>` for everything like it's the 2000s.

```
<div class="header">Site Title</div>  
<div class="nav">Navigation</div>  
<div class="main">Main Content</div>  
<div class="footer">Footer Information</div>
```

✅ Good: Using proper elements so everything makes sense.

```
<header>Site Title</header>  
<nav>Navigation</nav>  
<main>Main Content</main>  
<footer>Footer Information</footer>
```

## 1.2 Implement ARIA Where Necessary

ARIA (Accessible Rich Internet Applications) can help where semantic HTML falls short, but don’t **overuse it**. If a native HTML element does the job, use that instead.

### Why does this matter?

* **Enhances interactivity**: Helps screen readers understand complex components.
* **Provides extra context**: Roles like `role="navigation"` and `aria-live` make dynamic elements easier to interpret.
* **Prevents accessibility issues**: But **misusing ARIA** can actually break accessibility — so use it wisely.

### Example

❌ Bad: Using ARIA when a native element would do just fine.

```
<div role="button">Click me</div>
```

✅ Good: Just use a button!

```
<button>Click me</button>
```

## 1.3 Keyboard Navigation & Focus Management

If users can’t tab through your site properly, you have a problem. Everything interactive needs to be **keyboard accessible**.

### Why does this matter?

* **Keyboard-only users depend on it**.
* **Focus states need to be clear**, so users know where they are.
* **Trap focus in modals** so users don’t get lost.

### Example

❌ Bad: No focus styles, no way to navigate properly.

```
button:focus {  
  outline: none;  
}
```

✅ Good: Make focus clear but stylish.

```
button:focus-visible {  
  outline: 2px solid #005fcc;  
}
```

## 1.4 Forms & Labels

Forms are one of the most common accessibility failures. Every input should have a **proper label**.

### Why does this matter?

* **Screen readers need labels** to describe inputs.
* **Placeholder text isn’t enough** — it disappears when users start typing.
* **Error messages should be clear and announced properly**.

### Example

❌ Bad: Using placeholders instead of labels.

```
<input type="text" placeholder="Enter your name">
```

✅ Good: Properly associating labels.

```
<label for="name">Name</label>  
<input type="text" id="name">
```

## 1.5 Ensure Color Contrast & Avoid Solely Color-Based Indicators

Low contrast text is hard to read. **Never rely on color alone** to convey meaning.

### Why does this matter?

* **Visually impaired users** may not distinguish certain colors.
* **Colorblind users** might miss critical info.
* **High contrast improves readability for everyone.**

### Example

❌ Bad: Relying on color to show errors.

```
<p style="color: red">Error: Invalid input</p>
```

✅ Good: Adding text AND icons.

```
<p style="color: red">❌ Error: Invalid input</p>
```

## 2. Authoring Best Practices: Ensuring Accessible Content in AEM

## 2.1 Use Proper Heading Structure

In some components you might have accessibility fields for the author to fill in, for each tenant or language. The quality of the text is their responsibility and that can make or break the score.

As a developer, you can add validations in the author dialogue to make sure they cannot leave the fields blank.

### Example

❌ Bad: Naming a sort button state.

```
<button aria-label="Sort">
```

✅ Good: Descriptive button name.

```
<button aria-label="Sort by date, ascending">
```

### Why does this matter?

* **Screen readers use headings to navigate**.
* **Proper structure keeps content organized.**

## 2.2 Add Descriptive Alternative Text for Images

If you’re uploading images into AEM, **don’t skip the alt text!**

### Why does this matter?

* **Screen readers rely on it** to describe images.
* **Empty alt text is ignored** by assistive tech (which is good for purely decorative images).

### Example

❌ Bad: Skipping alt text.

```
<img src="dog.jpg">
```

✅ Good: Descriptive alt text.

```
<img src="dog.jpg" alt="A golden retriever playing in the park">
```

## 2.3 Use Proper Heading Structure

Headings should be in order. **No jumping from** `<h1>` **to** `<h4>` **just because you like how it looks.**

### Why does this matter?

* **Screen readers use headings to navigate**.
* **Proper structure keeps content organized.**

### Example

❌ Bad: Skipping heading levels.

```
<h1>Main Title</h1>  
<h4>Subheading</h4>
```

✅ Good: Keeping things in order.

```
<h1>Main Title</h1>  
<h2>Subheading</h2>
```

## 3. Collaboration Between Developers and Authors

## 3.1 Implement Validation Rules in AEM

Developers should add **validation** to make sure authors don’t accidentally create inaccessible content.

### - Example: Enforcing Alt Text in an Image Component

You can add a required field in your **cq:dialog** for image components using Granite UI validation.

### - Example: Enforcing Validation with AEM Workflows

You can also use **AEM Workflows** to automatically check for accessibility issues **before publishing**.

## 3.2 Provide Accessibility Documentation for Authors

A simple **checklist** can go a long way. Make sure your authors know what to do.

## 3.3 Establish a Review Process

Set up **regular accessibility audits** to catch issues before they go live.

## Conclusion

Accessibility isn’t just a **developer problem** or an **author problem** — it’s a **team effort**. Devs need to build accessible components, and authors need to create accessible content. If everyone follows these best practices, we’ll all end up with better, more inclusive websites.

Would you like a deeper dive into AEM’s built-in accessibility tools? Let me know! 🚀