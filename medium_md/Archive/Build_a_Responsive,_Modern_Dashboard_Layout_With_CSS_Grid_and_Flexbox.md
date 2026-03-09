---
title: "Build a Responsive, Modern Dashboard Layout With CSS Grid and Flexbox"
url: https://medium.com/p/bd343776a97e
---

# Build a Responsive, Modern Dashboard Layout With CSS Grid and Flexbox

[Original](https://medium.com/p/bd343776a97e)

Member-only story

# Build a Responsive, Modern Dashboard Layout With CSS Grid and Flexbox

## Create a beautiful, responsive dashboard page without *any* framework and including a sliding side nav

[![Matt Holland](https://miro.medium.com/v2/resize:fill:64:64/1*AwRA246dlg8iMIz_PC3J8w.png)](/@matthollandtips?source=post_page---byline--bd343776a97e---------------------------------------)

[Matt Holland](/@matthollandtips?source=post_page---byline--bd343776a97e---------------------------------------)

8 min read

·

Nov 14, 2018

--

17

Listen

Share

More

Press enter or click to view image in full size

![]()

Have you every been mystified by those gorgeous online dashboard demos that have you wondering, “Will I ever be able to build that…?” Well, I am here to tell you that you *can build it!*

## How Do We Go About This?

We will first introduce some CSS Grid basics. We’ll then use those to build our base dashboard layout. After that, we’ll explore the setup and structure of our inner content blocks, including some flexbox. Finally, we’ll talk briefly about responsible mobile-responsiveness, while integrating mobile-friendly sliding functionality into our side nav. What will you walk away with? A boom-goes-the-dynamite dashboard that will make people like you a lot.

Note: We will be building a [simplified version](https://codepen.io/trooperandz/pen/YRpKjo) of the dashboard above, which uses the same concepts as the [full version](https://codepen.io/trooperandz/pen/EOgJvg). The full version would make this piece silly long…

### First things first: our basic grid layout

I’m going to break down CSS Grid for you, short and sweet. We need a main grid container, and then we need a `div` (or semantic element) for each element within the grid container:

Pretty simple structure, right? Our layout will help produce this immediately-beautiful canvas below. Don’t worry, we will be adding more content.

Press enter or click to view image in full size

![]()

### Next, let’s lay down the law…I mean CSS

Your main container must be defined as `display: grid;` for any grid functionality to actually work. We also give it a height of 100% to tell it that we want our dashboard to fill the entire page. And, for each child container, we will assign a name so that we can tell the grid what to do with it. Then we will use the names to create the page structure in a spreadsheet-like declaration using `grid-template-areas`:

Our final, responsive dashboard will look like [this](https://codepen.io/trooperandz/pen/YRpKjo):

Press enter or click to view image in full size

![]()

### Grid-template-areas explained

We basically assigned each of our child containers a name, and then threw them into a spreadsheet-like format via `grid-template-areas`. Dead simple.

We have two columns total from left to right. The first column is 250px wide (the side nav), and the second one is 1fr, or fraction. That means that it will take up the remaining container space after the first column has been drawn.

Next, we declare three total rows. Rows flow from top to bottom. So, starting at the top, we have a `<header>` element that is 50px tall. Then we declare the `<main>` content area, which is given a height of 1fr. This means that it will vertically stretch to fill the remaining window space after explicitly-declared heights have been drawn. Finally, we declare our `<footer>`, also at a height of 50px.

### Adding the header and footer

Both the `<header>` and the`<footer>` will be flex containers, with [flex spacing and alignment](/mtholla/twerking-it-with-flexbox-55489dccafa1):

We use `justify-content: space-between;` to spread out the first and last elements so that they stretch to both ends of their container. This is so easy compared to old-school `float` instructions. And, thanks to `align-items: center;`, we have our items perfectly aligned without having to rely on padding, etc., for centering.

A brief note on our weird-looking CSS class syntax: we are using [BEM](http://getbem.com/introduction/)-style (block-element-modifier) CSS, which I recommend for scalability and readability. It is recommended to avoid raw html tag selectors.

### Adding the side nav element

For the side nav content, we use traditional `<ul>` and `<li>` elements. I recommend this over `<div>` or any other elements for good html semantics and human readability. We will be adding mobile-friendly sliding functionality into our side nav a little bit further down:

### Adding the first `<main>` section element

This one is straightforward and simple. Another flex container:

### Now things get interesting… the responsive grid introduction cards

Press enter or click to view image in full size

![]()

This is one of my favorite sections of our dashboard, because we get to utilize a super effective, elegant grid solution. Watch the dashboard animation provided previously again. Notice how these gray cards behave as the screen changes? Our cards amazingly keep a consistent gutter width between them, they have consistent wrapping, and when we can’t fill up an entire row, our wrapped card matches exactly the height and width of the card above it, while remaining lined up with it. This is *very* challenging and tedious to accomplish without the method that I’m about to show you:

Neat how we used a grid container for these, which is inside of our main page grid container, right? We did this because it’s the most straightforward, elegant solution to use for the needed responsiveness of the card items. Our instruction `repeat(auto-fit, minmax(265px, 1fr)` takes care of a couple of major hurdles:

1. If cards go below 265px in width, they will wrap to another row.
2. If cards go above 265px in width, they will stretch to take up the available remaining container width.
3. When cards wrap to a new row (`auto-fit`), they will line up from left to right with the cards above them, matching their widths! *And* you also get built-in responsiveness without any media queries!

Using the column `repeat` method is also a *fantastic* way to build beautiful, responsive image galleries, even with images of differing sizes. You even have access to dynamic packing algorithms with the `grid-auto-flow: dense;` instruction. This will prevent any empty row spaces due to different image heights. They must scale with each other in relative `fr` units for this method to work, however, which is why we won’t use it for our cards shown below.

### Adding the main content containers

Press enter or click to view image in full size

![]()

This section also has an interesting twist. These cards will contain your dashboard’s main content items, and they will vary in height from each other due to their dynamic content. On most typical interfaces, you would want like-minded cards on the same row to have the same uniform height and width. And you would accomplish that by assigning each card a `flex: 1;` value so that they would grow to match the tallest card.

However, in our case, we don’t want to force these cards to match each other’s height because their content subject matter will vary. To get them flowing naturally in two columns, we will use a special CSS property for this, `column-count`:

Using `column-count` will ensure that our content inside of the `main-cards` section gets split into two columns. We also apply a gap between the cards with `column-gap`. This is very similar to our overview cards, where we used `grid-gap`.

The reason we didn’t use `display: grid;` for this section is that our heights for each card are dynamic. We want them to flow naturally into two columns, while observing their varying heights. This method also prevents us from having to use a traditional float grid, which would have us calculating percentage widths, gutters, and special margin rules for first and last child elements.

We also used `column-break-inside: avoid;` to make sure that each card does not get its content split.`column-count` will actually break up the content of each element to make both rows the same height, which we do not want.

### A brief note on responsible mobile-responsiveness

Watch the responsive video at the top of the piece again. See how the `main-cards` section turns into one column as you approach tablet-sized screens? And see how the side nav disappears on mobile-sized screens? For this responsiveness, we should really write our CSS in a mobile-first format.

That means that our initial CSS should be mobile-friendly. Then, as our screen size increases, we observe larger screen styles using graduating `min-width` media queries. This is better practice than overriding desktop styles with `max-width` media queries, as that approach can lead to some headaches:

### Making our side nav slidable on mobile devices

Our job is not really complete until we also make the side nav useable on mobile devices. We need to:

1. Add our menu icon and close icon.
2. Add some responsive transitions for the sliding action.
3. Write some JavaScript to make our clicks activate the side nav.

We’ll use the [Font Awesome](https://fontawesome.com/icons?d=gallery) library for our icons, and bring in [jQuery](https://jquery.com/) for some easy DOM manipulation (See the [codepen](https://codepen.io/trooperandz/pen/YRpKjo) for reference).

Next, let’s update our CSS to include the new icons and to give our side nav some sliding transitions. Once again, we will use *graduating* media queries:

Finally, we need to write some JavaScript to get our clicks working. The sliding functionality is accomplished by toggling the `.active` class name, which updates the `transform: translateX();` instruction. Don’t forget to add the jQuery [CDN link](https://developers.google.com/speed/libraries/) before your ending `</body>` tag:

You should now have a fully responsive side nav. Scale down your window until it is mobile-sized. It should hide, and the menu icon should appear. Click it, and the side nav should slide into view. Click the close icon, and the side nav should close again. Pretty slick, eh? And you thought you couldn’t do it…

## In Summary…

What did you just learn?

1. How to build a dashboard layout using CSS Grid & Flexbox.
2. Special rules for dynamic content blocks using `repeat`, `auto-fit`, `min-max`, `column-count` , `grid-gap`, and `column-gap`.
3. The *right* way to write mobile-first, responsive CSS using graduating `min-width` media queries.
4. How to build a sliding, mobile-responsive side nav.

Please check out the full dashboard [codepen](https://codepen.io/trooperandz/pen/EOgJvg), which includes a clickable, sliding side nav with accordion list items, a nice dropdown user menu, and some slick `transition` hover action.

I hope you gained some new knowledge from this piece and that dashboard layouts will never mystify you ever again. Please comment if you have any questions!