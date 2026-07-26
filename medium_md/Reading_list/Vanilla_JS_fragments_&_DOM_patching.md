---
title: "Vanilla JS fragments & DOM patching"
url: https://medium.com/p/b4f8d7ec8fbd
---

# Vanilla JS fragments & DOM patching

[Original](https://medium.com/p/b4f8d7ec8fbd)

# Vanilla JS fragments & DOM patching

[![Brooklyn Nicholson](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)](https://babybrooklyn.medium.com/?source=post_page---byline--b4f8d7ec8fbd---------------------------------------)

[Brooklyn Nicholson](https://babybrooklyn.medium.com/?source=post_page---byline--b4f8d7ec8fbd---------------------------------------)

1 min read

·

Jul 23, 2018

--

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Db4f8d7ec8fbd&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fvanilla-js-fragments-dom-patching-b4f8d7ec8fbd&source=---header_actions--b4f8d7ec8fbd---------------------post_audio_button------------------)

Share

I was curious about how to do react-like things myself without relying on `innerHTML` or, frankly, any dependencies. It ended up quite easy.

First, fragments via [document.createDocumentFragment()](https://developer.mozilla.org/en/docs/Web/API/Document/createDocumentFragment) are pretty magical. They exist in memory and you can construct them as usual, basically creating a micro virtual dom.

Their purpose is to let you build out a substantial amount of changes to a future DOM before actually rendering. This helps you control repaint count, for ex:

That’s 15k repaints reduced to 1.

With this, there should never be any use case for the expensive `innerHTML`. However, there are times when we *must* parse strings to HTML. We can still do this.

See [createContextualFragment](https://developer.mozilla.org/en-US/docs/Web/API/Range/createContextualFragment) — it will (try to) parse your string into HTML as long as it’s valid. Example:

For fun, I also threw in updating a text node via fragments rather than modifying innerText/textContent.