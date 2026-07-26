---
title: "How I converted my React app to VanillaJS (and whether or not it was a terrible idea)"
url: https://medium.com/p/4b14b1b2faff
---

# How I converted my React app to VanillaJS (and whether or not it was a terrible idea)

[Original](https://medium.com/p/4b14b1b2faff)

# How I converted my React app to VanillaJS (and whether or not it was a terrible idea)

[![David Gilbertson](https://miro.medium.com/v2/resize:fill:64:64/2*wMzreVypTZ6R-T9S2HvONQ.jpeg)](/?source=post_page---byline--4b14b1b2faff---------------------------------------)

[David Gilbertson](/?source=post_page---byline--4b14b1b2faff---------------------------------------)

15 min read

·

Jan 1, 2017

--

62

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D4b14b1b2faff&operation=register&redirect=https%3A%2F%2Fdavid-gilbertson.medium.com%2Fhow-i-converted-my-react-app-to-vanillajs-and-whether-or-not-it-was-a-terrible-idea-4b14b1b2faff&source=---header_actions--4b14b1b2faff---------------------post_audio_button------------------)

Share

This is a long and winding tale (with lots of code) of my attempts replicate JSX syntax, component structure, server-side rendering, and React’s update magic with VanillaJS.

I wrote a post last week, “[10 things I learned making the fastest site in the world](https://hackernoon.com/10-things-i-learned-making-the-fastest-site-in-the-world-18a0e1cdf4a7#.eqysd36e6)”. All was going well, I had the usual wonderfully constructive comments on medium and snarky ones on reddit. But then I came across this friendly but rage-inducing comment:

![]()

I was not happy (Jan). I had let my readers down. I had let myself down. And most of all, I had let the foxes down.

I decided that I wouldn’t rest until I was faster than [motherfuckingwebsite.com](http://motherfuckingwebsite.com/).

Then I had a little rest.

Then I got to work on the last piece of my web app I thought I could make faster — replacing React with VanillaJS.

You’ll [find the site here](https://knowitall-9a92e.firebaseapp.com/) (it’s a work in progress) and [the source is on github](https://github.com/davidgilbertson/know-it-all), feedback is the aim of the game so don’t be shy.

## What is React?

You know what React is, why are you even asking?

But now that you have, I will point out that I’m using “React” as an umbrella term in this post, to refer to concepts shared by React and Preact and friends, and sometimes to concepts from flux/redux.

## What is VanillaJS?

VanillaJS is a framework written many years ago by a dude called Brendan that is rarely used anymore. It has quite a few interesting features that I thought would be useful in my project, so I dusted off the spider webs — or whatever you call the webs of spiders in your weird country — and reacquainted myself with the framework of frameworks.

This must be confusing for those of you new to web development. Allow me to speak plainly for a moment: [serious voice] When I say VanillaJS I am simply referring to [JavaScript](https://hackernoon.com/tagged/javascript) and the DOM APIs. I am gently poking fun at the fact that most of us wouldn’t even consider writing code without first picking at least one framework or library, hence talking about JavaScript as though it was a framework. [end serious voice]

## How does one go about replacing React with VanillaJS?

I am so, *so* glad you asked. I decided to try something unusual with this endeavor and write the blog post first. It worked out really well, because as I’m writing a post I’m imagining detractors in the comments picking apart every decision I make (you guys are *mean*).

It’s like [rubber ducking](https://en.wikipedia.org/wiki/Rubber_duck_debugging) on steroids, and it helped me get the design decisions stable in my head before starting to write any code.

One of the things that crystallized for me is that there are three distinct parts to React that make it great:

1. JSX syntax
2. Components/composability
3. One-directional data flow (UI > action > state > magic > UI)

As I picked these apart I came to realise something. The performance overhead that React brings comes from two places:

1. The sheer effort of parsing 60 KB of JavaScript.
2. The magic that happens after you update the state, before the DOM updates.

The first of these — the time taken to parse the framework— I can solve by not using the framework (like how I avoid arguments with people by never talking to people).

The second one — the time taken to update the UI — is much more difficult; there’s something for you to look forward to in about 9 minutes.

So of the three things that make React great, only the third one introduces a performance penalty.

The result is, I want to *replicate* JSX, I want to *replicate* components, and I want to come up with some new way to update the UI when state changes.

[movie trailer voice]

And he’s only got 48 hours to do it.

[end movie trailer voice]

## #1 Replicating JSX

I like JSX.

I like that it visually represents the output HTML, but doesn’t shy away from the fact that I’m using JavaScript. It taught me that ‘separation of concerns’ doesn’t mean ‘separation of languages into different files’.

My key objective in replicating JSX is to be able to define my components in a way that is visually similar to the resulting HTML — just like JSX does — but in VanillaJS.

First up, I don’t want to be writing `document.createElement()` over and over. So I’ll write a shorthand function for that:

This uses VanillaJS’s “virtual DOM” technology to create an element without actually writing it to the document.

My laziness doesn’t stop there, though. I don’t want to have to type `makeElement('h1')` all the time either, so I’ll write another shorthand function.

Let’s test this out…

![]()

That’s amazing.

I probably want some text in my h1 though, let me extend my functions…

![]()

I astound myself.

You know what though, I probably want to give that element a class. Maybe even set some other attributes one of these days. Hey I know! I’ll pass in an object with some properties and values. Then I’ll iterate over it, applying all the properties.

Since I’m now passing a few different arguments, I’ll update my `h1` function to just pass all of its args along to `makeElement`.

![]()

I’m speechless.

…

Still speechless.

…

OK this is great but it’s of no use to me if I can’t *nest* my elements. That was, like, nine words in a row with three or less letters!

Before I go any further I will take a piece of HTML from my site and work toward being able to create that.

Looked at it? Good.

So, to generate this nested HTML, I will need to extend my `makeElement` function to handle other elements being passed in. It will simply append those to the element it returns. For example, I need a `div` that I pass a `header` to. And I will pass an `h1` and an `a` to that `header`. Have you ever noticed how HTML tags are like functions?

No? Really? Whatever.

At this point I ran into a bit of complexity because for this to be useful, the arguments could be all sorts of things in all sorts of wacky orders. I’ll need to do some fancy footwork to work out what each argument is.

[David from the future here, this was the only difficult part, so stick in there, champ.]

I know the first argument to `makeElement` will always be a tag name, such as “h1”. But the second argument could be:

* An object defining the props for the element
* A string defining some text to display
* A single element
* An array of elements

Anything *after* the second argument will be an element or an array of elements, I’ll use the rest syntax again (the most relaxing of all the syntaxes) to gather these up into a variable called `otherChildren`. Most of the complexity here is to allow flexibility in what can be passed to `makeElement`.

Boom, there’s my frontend framework, 0.96 KB.

I should put it on npm and call it `elementr` and gradually add features until it’s 30 KB at which point I will realise that maintaining a package on npm is a thankless task that I regret deeply. My only recourse will be to escape to a dessert island and gorge myself on crème brulee until the end of my days.

One of the other great things about React is the helpful errors. They save so much time, so I’ve built in some checks (`if (propName in el)` and `if (styleName in el.style)`) so I get a nice warning when I inevitably try to set `herf` and `backfroundColor`.

I think half the skill in [programming](https://hackernoon.com/tagged/programming) is predicting the stupid things you’ll do in the future and protecting against them now.

I now have a function that I can throw pretty much anything at and it will return a little DOM tree for me.

Let’s vigorously kick the tires:

I find that quite readable. In fact it looks remarkably similar to my desired output HTML. Don’t have the time to scroll back up?

If I try and look at all that JavaScript as functions, I’ll go (more) insane trying to work out what returns what. But I started to look at the `h1`, `div`, etc. as HTML tags with different shaped brackets, and after a bit of adjusting, and a lot of squinting, my brain began to do a real-time transformation and I now just see the resulting HTML.

Thanks, brain.

Bonus: since the props you pass to an element are just objects, and JavaScript is wonderful and functions are objects, you can go right ahead and pass in a property called `onclick` with a function as the value and the VanillaJS event system will bind a click event to that element for you.

Isn’t that just bonkers? I love that I didn’t even think about events till I got halfway through, then felt stupid for not taking them into account, then felt like the god of programming when I realised that they would Just Work.

So *that’s* what love feels like. It’s nice!

## #2 Replicating React components

Now, here’s the cool part. The above stuff is all just functions, right? And by nesting them, we have functions that return functions that return functions that eventually return elements.

And what’s a component in React? It’s just a function that returns an element (more or less). So I can arbitrarily group some functions into a function, give it a capital letter and call it a component. I can even pass it props just like I was using React.

The below outputs the same HTML as above, but is grouped into “Components”.

This *feels* like React doesn’t it?

And all for about 6 hours of writing code (yes it took me 6 hours to write 73 lines of code. Somehow I feel proud and ashamed of that at the same time. I don’t know why I’m telling you all this.)

We’re not done yet. This was the easy part. How the pyjamas are we going to update these components when the data changes?

### Server rendering

Server rendering? Hey, this isn’t what the previous sentence implied we’d be talking about next, you scallywag!

Yes yes, but server-rendering is important and, as luck would have it, blindingly easy.

I thought about this backwards. Why *wouldn’t* the above functions work in NodeJS? Easy, because `window` and `document` don’t exist in Node.

What if I initialise `jsdom` just before trying to use my App component? Then I could just take the `outerHTML` of the result.

Surely that wouldn’t *just work*, would it?

Well whaddaya know, this works just fine!

Thanks, jsdom people.

With my HTML being rendered on the server, I will need to ‘rehydrate’ this on the client, in three easy steps:

1. Get a reference to the DOM the server rendered.
2. Render App again (not appending to body yet) using the data in `window.APP_DATA`.
3. Replace the server-rendered DOM with the client-rendered DOM (which will be visually identical but have events bound).

Again, good errors are worth the effort, so I’ll compare the server-rendered DOM and client-rendered DOM just before I switch them out. If they don’t match I write the full HTML strings for both to the console so I can copy/paste into [an online diff tool](https://www.diffchecker.com/) and see what’s different. Nothing beats a little excess.

## # Rethinking one-way data flow

*Now*, how the pyjamas are we going to update these components?

Having your data flow in one direction means you’re never reaching into the DOM to fiddle with the way the UI looks. Instead you fiddle with the underlying data and trust that the UI will update to match that data.

This is what makes React pretty great to work with.

From the React docs:

> In our experience, thinking about how the UI should look at any given moment rather than how to change it over time eliminates a whole class of bugs.

From One Direction’s smash hit *Drag me Down*:

> I’ve got fire for a heart  
> I’m not scared of the dark  
> You’ve never seen it look so easy  
> I got a river for a soul  
> And baby you’re a boat  
> Baby you’re my only reason

“Baby you’re a boat”. Swoon.

I definitely don’t want to go back to the world of locating elements with selectors and adding/removing bits and bobs in response to user interactions.

I did a full-body twitch just thinking about it.

Please join me now for imagination time. Imagine a user clicks a button on a TODO list that should reveal a list of items. In the React world, *your* code defines how the UI should look based on a given state, *your* code will update the state when something happens, and *React’s* code will magically update the UI when the state changes.

*Magically* you say?

Press enter or click to view image in full size

![]()

![]()

The above was generated by clicking “All” on a TODO list with 10 items. Then turning my monitor sideways to get the screenshot.

That’s ~60 milliseconds on a fast phone to show 10 things. Expect closer to 200ms on a mid-range phone.

*Edit: turns out that TodoMVC is not the performance showcase I expected it to be, and is using a a dev build of React. I will update the “60” and “200” shortly. Other charts on the page do use the proper production build.*

It all boils down to this: you feed in some new state at the top-level component(s), it trickles down into each child component, and each child component works out if it needs to update or not. Then, when React has worked out *which* components need to update, it works out the fastest way to do so (either wholesale replacement of DOM, or updating attributes individually).

Here’s that with a lot fewer words and arrows that *aren’t quite* quarter circles.

Press enter or click to view image in full size

![]()

I’m not going to write my own updating logic, that’s probably [quite a lot of work](https://github.com/facebook/react/commits/master/src/renderers/shared/fiber), so what’s the alternative?

I know that I want the state to be the source of truth for my app, and by extension I want any user interaction to result only in an updating of the state (not directly adding a class to elementX or something similarly awful). And I know that when my components update, they should do so based on the current state and nothing else.

How do I get from updating the state to the components re-rendering when they need to?

Press enter or click to view image in full size

![]()

After thinking about this for a while and buying a new mouse (unrelated) I came to realise that what React is doing is, in a way, a “just-in-time” calculation of what to update.

So what if I could know what I wanted to update “ahead-of-time”? That would bypass the whole DOM-diffing algorithm, and remove the amount of time spent doing that.

What I’ve come up with (deep breath — be gentle) is that the *store* works out which components will need to be updated.

It doesn’t know *how* to update the components, it only knows to instruct them to update themselves.

So, for example, on my web page I click on a row in a table to select it. Three things need to happen:

1. The data in the store must be updated to set `selected: true` for the clicked row and `selected: false` for the previously selected row
2. The component that *was* selected must be re-rendered
3. The component that *is now* selected must be re-rendered

In the store, it looks like this:

Whenever `updateItem()` is called, the data in the store is updated, *and* the component associated with that item is re-rendered.

Before we get into the reasons why this is a terrible idea, let’s look at the results:

Press enter or click to view image in full size

![]()

120ms (React) is a bit laggy, and the more DOM I have on the page, the longer this gets. Preact is doin’ great.

The VanillaJS version won’t change regardless of how much DOM is on the page— it still knows exactly which two nodes need to be updated.

That was just selecting a row, what about clicking the little arrow to expand a row (which will render a bunch of new child DOM nodes)?

Press enter or click to view image in full size

![]()

All of these charts, by the way, are the median of five runs. So it isn’t an anomaly that Preact was slower, it was consistently so.

Pretty chart, but let’s dive into what’s actually taking place when I expand a row.

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

You can see the style/layout/paint tasks (purple and green) are about the same in React or VanillaJS. But the JavaScript (orange) takes a third the time in the VanillaJS version. This is because it isn’t trying to work out what to update by comparing two versions of the DOM. It just knows that someone clicked the ‘expand’ button on a row, which means change `expanded` to `true` and re-render the associated component. Those 61.04ms are 99% DOM creation.

Isn’t it interesting that purple, orange, and silver are all colours, and also 3 of the top 4 words that don’t rhyme with anything?

So, how does a component actually ‘update itself’?

It’s funny you ask because I was *just about to explain that*. Here’s a component, `TableRow`, that has three things worth noting:

* `render()`, which does the initial render. It returns an element, and the component returns that element.
* `store.listen`, registers this component with the store by ID.
* `update()`, which is called, via the callback passed to `store.listen`, from the store when it wants this component to update.

Note that the `update()` function does a check to see if an update was really required. This is just a preemptive catch to help iron out logic errors when developing.

That’s it. This works.

It’s not *great*, it doesn’t feel as nice as the React way. There’s mutability hidden in there waiting to cause trouble. Also, I have quite a simple relationship between data and DOM (each ‘item’ in my array maps neatly to one `<div>`) that would not work so nicely in a more complex app. So I would be a bit nervous about using this pattern for a big project. On the other hand, you know what they say, anxiety is the spice of life.

## Bonus: replicating redux devtools

OK I can’t even get *close* to the amazingness that is the Redux dev tools. But I would like some simple logging, and it doesn’t get much simpler than this (all changes flow through the `updateItem` method).

So I can type `APP_DEBUG = true` in the console (even in production — [you may try it](https://knowitall-9a92e.firebaseapp.com/)) to ‘turn on’ logging and I’ll get something like this with each update:

![]()

Good enough, says I.

## The End

This little exercise started as a React replacement project, but quickly turned into a React appreciation project. I’m quite sure that if I hadn’t been peeking over the shoulder of React, my efforts would have been a white hot mess.

[start wrap-up soliloquy voice]

Frameworks will often be doing a bit of extra work that you could avoid if you wrote the code yourself, this is true. But on the whole, I think this is a fair tradeoff for the improved productivity that comes with using a well-written framework that encourages some great practices.

For a small project though, or one where performance is absolutely critical, I’m glad that I now have a few tricks up my sleeve, and that the prospect of creating a complete app in VanillaJS doesn’t seem quite so daunting any more.

[end wrap-up soliloquy voice]

## Prologue.

Prologue is the one after the end, right?

OK motherfuckingwebsite, it’s you and me. Chrome DevTools, after school behind the girls toilets, nothing below the waist or witty taunts that go over my head.

To make it a fair fight we’ll go first visit, no cache, no service workers, and networks throttled to “Good 3G”, K?

First one to the little red line wins.

Press enter or click to view image in full size

![]()

Is that the best you got? 600ms? I ate lunch before your website showed first paint. I wrote an Elizabethan novel before your website showed any signs of life. Yo mamma could knit a sweater before your site’s ready for reading.

My turn.

(You thought this was a fight metaphor? No no, it’s a dance-off with lots of weird smack talk.)

Press enter or click to view image in full size

![]()

[does the splits, panting]

OK that probably sounded awfully cocky, let me knock myself down a few pegs before people start throwing flowers and their delicates:

* Try this on a slower CPU and I lose
* Compare the ‘speed index’ on webpagetest.org and I lose
* Chrome has unfairly put the red marker *after* the motherfucking google analytics snippet which is set to async (thought it wouldn’t have made a difference).
* Put both sites on the same hosting and I’d lose (Firebase FTW!)

Now I’m going to have a little lie down.

[![]()](http://bit.ly/HackernoonFB)[![]()](https://goo.gl/k7XYbx)[![]()](https://goo.gl/4ofytp)