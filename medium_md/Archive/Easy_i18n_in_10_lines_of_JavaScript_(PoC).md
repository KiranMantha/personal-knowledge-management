---
title: "Easy i18n in 10 lines of JavaScript (PoC)"
url: https://medium.com/p/eb9e5444d71e
---

# Easy i18n in 10 lines of JavaScript (PoC)

[Original](https://medium.com/p/eb9e5444d71e)

# Easy i18n in 10 lines of JavaScript (PoC)

[![Andrea Giammarchi](https://miro.medium.com/v2/resize:fill:64:64/1*54OyE6rg-MdELwb9mW56Xw.png)](/?source=post_page---byline--eb9e5444d71e---------------------------------------)

[Andrea Giammarchi](/?source=post_page---byline--eb9e5444d71e---------------------------------------)

3 min read

·

Oct 22, 2017

--

2

Listen

Share

More

**Update**: from PoC to WiP as set of little libraries and [utilities](https://github.com/WebReflection/i18n-utils)

If [hyperHTML](https://viperhtml.js.org/hyper.html) blew your mind with its revolutionary [Template Literals](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals) usage, you might be delighted to discover this little *TL* based trick too.

I don’t want to surprise you with a function that does pretty much nothing when used in conjunction with *TL*, but I want to show you the basics to create an environment already capable of internationalization.

How? Try typing the following in console: `` i18n`Hello ${'World'}` `` and see the string `"Hello World"` appear.

Got it? Good! We’ve just discovered all the basics we need to add *i18n* on top.

### The promised 10 lines

I know the code is compact, and we miss some extra detail, but once we have a way to configure that `i18n.db` object, you’ll see that actually that’s really what we need to write beautiful semantic code that will translate for us transparently.

### Configuring the database

In order to have translations in place we need:

* a database with at least one language stored in it
* a database that can be saved once but used in many places
* a database that could be loaded incrementally instead of all at once
* a database easy to define through translations

and this is the easiest way I could think of:

Above function does not need to be served together with the `i18n` one, it can be used only offline or as CLI functionality to setup translations.

Following an example on how you would setup an “*Hello World*” in various languages:

If you now check the `i18n.db` object, you’ll see everything is in place, and everything can be also stored as `JSON.stringify(i18n.db)` .

### Using those ten lines of code

We are now capable of writing our set language everywhere and obtain different outputs accordingly to the chosen locale.

That means that we can write an entire application in English, and offer multiple version of the language simply changing the `i18n.locale` info.

### What’s new or different?

Here a quick list of features compared to usual solutions:

* template literals and a default language to write
* no objects properties to remember
* no random function invocations with ordered arguments or object properties
* what you write is what you get in every other language
* you can also swap interpolations as long as these have the same value when defined

### Hypothetical FAQs

* *is it compatible with* `en-GB` *and* `en-US`*?* Yes, as long as you have those entries in the DB and you’ve set them via `` i18n.set("en-GB")`...`.for(…) `` and you have default `i18n.locale = "en-GB"`
* *how can the database be incremental?* You serve only one default language, and you load any other on demand. The `i18n.db` is a public property you can enrich as you need. Once the new language is in, you can `Object.assign(i18n.db, itIT)` and the `{"it-IT":{}}` locale will be copied over the initial database
* *do I need a global function?* As you wish. As long as you need the same function across all modules, and one of them is in charge of loading/enriching the right db for all of them, you can use modules too
* *will it work if I transpile template literals?* Yes
* *how is performance impacted?* It depends. The database surely need a mandatory GZip compression or repeated chunks will be heavy to load. However, producing the correct output, once the database is loaded, should be as fast, if not faster, than any other runtime i18n solution.

### Outstanding issues

Now that we’ve seen the concept, there are various things that need to be considered or created to make this pattern production ready:

* a proper source code parser that runs against the known DB and asks for every template literal entry that has no equivalent in other languages
* a smart literals analyzer that would inform another identical string is used somewhere with slightly different new lines (whenever we care about it)

Last point is about having two possible multi lines template literals defined at different indentation levels. There are various way to fix this manually, but ideally a tool able to catch them and fix them for us to keep the db as small as possible and the translation reliable in every occurrence would be ace.

I hope you liked this proof of concept and I hope I’ll see interest around it.

If you already have a similar solution, please share it ’cause I’d love to use it!