---
title: "Building a Rich-Text Editor for Modern Publishers"
url: https://medium.com/p/cff7db6dc2e9
---

# Building a Rich-Text Editor for Modern Publishers

[Original](https://medium.com/p/cff7db6dc2e9)

# Building a Rich-Text Editor for Modern Publishers

[![Joost Jansky](https://miro.medium.com/v2/resize:fill:64:64/1*ohcptiMGAYgHfCOAqrusdA.png)](/@jamify?source=post_page---byline--cff7db6dc2e9---------------------------------------)

[Joost Jansky](/@jamify?source=post_page---byline--cff7db6dc2e9---------------------------------------)

8 min read

·

Apr 30, 2021

--

Listen

Share

More

An inside look into the making of a flexible Rich-Text editor that will be shipped as an integral part of Blogody — the new blogging platform I am building. It’s been a bumpy path to choose the editor technology best suited for modern publishers. Sneak preview into the final result…

Press enter or click to view image in full size

![]()

If you are like most people in this digital age, you use text editors every day and more likely every other minute. Just a quick message to your friend, an email to your colleague, or a document for your boss: most electronic text is written with an editor.

The ubiquity of editors may lead you to believe that you are dealing with fairly simple technology, but that’s far from reality. The illusion of a smooth, natural-feeling editor experience can only be created by an extremely advanced piece of technology that takes all possible user interactions into account while remaining extremely fast and amazingly responsive.

Press enter or click to view image in full size

![]()

This is even more true for web editors, which need to deal with different browser technologies, alleviate their quirks, compensate for slow network speeds and silently master all state and user interaction intricacies.

Modern writers and publishers demand an editor that produces clean, semantically meaningful documents, that let them focus on writing and article composition. The best editors of this trade are the ones that are not overly rigid but still use some constraints that don’t feel constraining for that specific use case. These editors artfully bridge the gap between unambiguous and rigid Markdown editors and full-fledged WYSIWYG editors.

## Rich-text editors for the web

Picking the right editor technology for the web is not easy. As the browser understands JavaScript natively, the editor should be written in that language or in a framework like React that uses JavaScript under the hood. While there are a number of open-source editor frameworks available, it still surprises me how much work you need to put into building a great a meaningful editor in 2021.

For [Blogody](https://www.https://www.blogody.com), I required primitive building blocks to be included by the framework *and* the ability to customize the editor to match exactly the main target group: modern content publishers and writers.

Press enter or click to view image in full size

![]()

I started by looking at the [König editor](https://github.com/TryGhost/Admin/tree/main/lib/koenig-editor) from Ghost because it is available open-source. It uses [Mobiledoc](https://github.com/bustle/mobiledoc-kit) in connection with [EmberJS](https://emberjs.com). There is also a React Mobiledoc variant that I intended to use, but the König editor turned out to be too tightly coupled to EmberJS and the Ghost’s NodeJS Admin interface. I figured, that carving it out would require more work than starting anew. Starting from scratch also gives me more freedom to choose a better technology stack from the get-go.

As [Blogody](https://www.blogody.com) is built with React, a more sensible choice would be to look for a native React editor framework. That’s how I got to know [Slate](https://github.com/ianstormtaylor/slate) which was recommended to me by one of the full-stack developers at [Republik](https://www.republik.ch/), a renown Swiss online newspaper. Slate looked very promising, with clear principles, a vibrant open-source community and outstanding React integration. Inspired by the success stories from the Republik team, I spent more than one month building a new editor based on Slate.

While I still think Slate has the best React interface, it turned out to be lacking in some unexpected ways: when you need to construct sensible boundaries for primitive elements, you don’t get much tooling. For example, if you want to ensure a picture element is always followed by a paragraph, you have do define that yourself in a so called [normalizer](https://docs.slatejs.org/concepts/11-normalizing) function. While this is possible, you’ll soon find out that you need to develop a content schema from scratch, not something easily done over a weekend. What turned out to be even more surprising for me: pasting long documents would freeze the UI for more than seven seconds on a fast desktop computer. That’s when I literally lost patience with Slate.

If you ever need to pick an editor framework for one of your own projects, the following advice would have saved me a lot of time:

> *Before you decide for a technology, make some simple end-user tests with demanding test data. For an editor, copy & paste large amounts of text, write text with high speeds, etc. and see if it the technology can still impress you when stressed.*

## Entering ProseMirror

With these findings, I found myself back on square zero. Is a slow editor the price for getting seamless React integration? Are there alternatives out there which I didn’t come across yet?

While looking further around, I stumbled upon an article about [ProseMirror](https://prosemirror.net), another highly acclaimed editor framework used in the digital news room of the [New Your Times](https://open.nytimes.com/building-a-text-editor-for-a-digital-first-newsroom-f1cb8367fc21). Open-sourced with a more traditional yet helpful forum community, thoroughly maintained by the creator and master mind. The project is supported by some well-known companies, so it captured my attention. First end-user tests showed stunning performance characteristics. The above mentioned example that took over seven seconds in Slate would complete in 150 milliseconds in ProseMirror — which immediately electrified me.

Press enter or click to view image in full size

![]()

There was just one problem with ProseMirror. How could I possibly integrate ProseMirror into the Blogody React app? All ProseMirror-React boilerplate implementations I found looked really complicated and I hardly understood what they were doing: Communicating state between React and ProseMirror neither seemed to be straight forward nor easy.

With some help from people of the the ProseMirror forum community I started with trying to make a simple React bridge. Firsts steps were really difficult and I was constantly thinking of dropping out from that experiment. How much time would I need to get even simple things working, like integrating a simple paragraph React component?

While I learned a lot about all the ProseMirror lego pieces and the well designed interfaces that you can hook into, I had almost abandoned ProseMirror when I was suddenly struck by a sparkling idea:

> *Let ProseMirror handle primitive elements like paragraphs, figures, etc. with its native JavaScript framework and use React only for interactive overlay elements, such as hover-bars or drop-down menus.*

With this clear conceptional distinction, I was able to make progress much faster and secure ProseMirror’s nice performance characteristics while being able to integrate the editor into the main React app.

Looking back after another month, I am convinced that this was finally the right choice. ProseMirror is extremely efficient in handling the basic editor elements, it is easily extended with a plugin approach and ensures document integrity with a flexible schema design system. Furthermore it allows me to amend it with complex React overlay components through my custom built React bridge.

Itching to see some demo results? Here we go.

## Hover toolbar

I have always been a fan of contextual toolbars that offer exactly the editing choices that make sense at this very moment. Just select some text and an inline formatting toolbar opens:

Press enter or click to view image in full size

![]()

A side menu lets you insert block level content, such as horizontal lines or images. A plus button will show up on every new line as you can see below:

Press enter or click to view image in full size

![]()

## Side menu

A side menu lets you insert block level content, such as horizontal lines or images. A plus button will show up on every new line as you can see below:

Press enter or click to view image in full size

![]()

## Keyboard Shortcuts

One of the early design goals for the Blogody editor has been to make the keyboard a first class input method. While every action can be invoked with your mouse, the keyboard is an equally good alternative.

* `Ctrl` + `b` toggles the selection **bold**.
* `Ctrl` + `i` toggles the selection *italic.*
* `Ctrl` + `` ` `` toggles the selection `inline code`.
* `Ctrl` `Shift` + `1...3` changes the text-block to heading at a level.
* `Ctrl` `Shift` + `8` wraps the selection in an ordered list.
* `Ctrl` `Shift` + `9` wraps the selection in a bullet list.

## Input Rules

You can also use Markdown inspired input rules. The side-menu can always be opened by pressing `/` and you can move the current selection with your arrow keys, confirm with `Enter` or leave with `Esc`.

The following screen-cast demonstrates how easy it is to structure your text without leaving the keyboard:

Press enter or click to view image in full size

![]()

* `#` followed by a space, to start the line as a heading.
* `##` followed by a space, to start the line a sub-heading.
* `###` followed by a space, to make the line a sub-sub-heading.
* `-` or `*` followed by a space, to create a bullet list.
* `1.` followed by a space, to create an ordered list.
* `>` followed by a space, to create a quote.
* ```` ``` ```` to create a code block.

## Unsplash Widget

More complex features are also possible with the ProseMirror React bridge. I have partnered with [Unsplash](https://unsplash.com) to be able to integrate a royalty-free image picker into the Blogody editor:

Press enter or click to view image in full size

![]()

## Summary

Blogody’s richt-text editor is ideally suited for the modern web and will help writers and publishers focus on producing stunning content for their audience. Powered by ProseMirror under the hood, the editor is extremely stable and fast. With the newly developed React bridge for Blogody, even complex widgets like the Unsplash image picker are easily integrated and you can expect more eye-catching features coming in future [Blogody releases](https://www.blogody.com/news).

> [*Do you want early access to Blogody, the brand new blogging platform that I am creating? Just sign-up on the new Blogody landing page and be among the first to get notified!*](https://www.blogody.com/landing)

*Originally published at* [*https://www.jamify.org*](https://www.jamify.org/2021/04/30/building-a-rich-text-editor-for-modern-publishers/) *on April 30, 2021.*