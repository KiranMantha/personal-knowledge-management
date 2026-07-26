---
title: "A Dart REPL PoC"
url: https://medium.com/p/f327e3769b6f
---

# A Dart REPL PoC

[Original](https://medium.com/p/f327e3769b6f)

# A Dart REPL PoC

## Hacking with Dart

[![Andreas Kirsch](https://miro.medium.com/v2/resize:fill:64:64/1*mmND4OQvbUKv3OavQtrkOQ.jpeg)](/@BlackHC?source=post_page---byline--f327e3769b6f---------------------------------------)

[Andreas Kirsch](/@BlackHC?source=post_page---byline--f327e3769b6f---------------------------------------)

6 min read

·

Jan 17, 2017

--

6

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Df327e3769b6f&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fdartlang%2Fdart-repl-poc-f327e3769b6f&source=---header_actions--f327e3769b6f---------------------post_audio_button------------------)

Share

![]()

[Python](https://www.python.org/)’s interactive mode is great. [Dart](http://dartlang.org/) does not have an interactive mode at the moment, but it is really good for prototyping ideas quickly, so let’s see if we can hack something together!

*Disclaimer: I do work for Google, but this post is about a personal project. I’m not on the Dart team or related. This is just my humble opinion and my story. Come along.*

The interactive mode in languages like Python or Ruby has helped make them very approachable for beginners. But these are not the only ones that use the concept of a [REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop). A REPL is a read-eval-print loop. Shells like BASH or zsh also employ REPLs when you interact with them in a terminal. It is also what you get when you work with notebooks in [Jupyter](http://jupyter.org/) (IPython Notebooks), [Matlab](https://www.mathworks.com/products/matlab.html), [Mathematica](https://www.wolfram.com/mathematica/) or [Maple](https://www.maplesoft.com/products/maple/). This way of interactive computing is very popular with researchers.

This is what Python’s interactive mode looks like:

[![]()](https://asciinema.org/a/99317)

Dart does not support evaluating statements in a global scope like Python, so there is no obvious way to do it correctly. In Dart, statements have to be inside functions and the main function is the entry point of a program. Just like in C++ or C#. Personally, I prefer this as it makes it easier to figure out what is happening when a program runs. But… I’d still really want an interactive mode. It would allow me to play around with ideas and try things out even faster. So let’s see if we can create a REPL as a proof of concept!

## How can we create a REPL in dart?

Dart is really good for prototyping. So let’s do just that and not get bogged down by language design questions :)

Now there is no `eval` function like in JavaScript or Python, and I don’t want to write a full blown interpreter myself to implement one. It wouldn’t be very fast and I don’t have a lot of time either. However, when you debug [Dart code in Intellij](https://www.dartlang.org/tools/jetbrains-plugin), you can evaluate expressions while you step through your code. Evaluating expressions is very much what we’d like to do, isn’t it? Can we use this feature?

Dart’s debugging capabilities are exposed through its [VM service](https://github.com/dart-lang/sdk/blob/master/runtime/vm/service/service.md). It is an JSON-RPC service provided by the [Dart VM](https://www.dartlang.org/dart-vm) that you can connect to to debug your application. 

[Natalie Weizenbaum](https://medium.com/u/a81c627aeff9?source=post_page---user_mention--f327e3769b6f---------------------------------------)

 has published an article about the `vm_service_client` package that provides a very nice API to interact with the VM service: <http://news.dartlang.org/2016/05/unboxing-packages-vmserviceclient.html>

Now what we can do is: our REPL can connect to its own VM service to evaluate expressions that it reads from the terminal! That sounds crazy…

![]()

… but it works! I have written a [quick spike](https://github.com/BlackHC/dart_repl/blob/ca3518074c94f48ce5be872b15b58556133a474c/bin/repl.dart) and indeed it works. Dart supports [asynchronous programming](https://www.dartlang.org/tutorials/language/futures), which comes in really handy as it keeps the program from blocking itself when talking to its own VM service.

> Spikes are a concept from test-driven development: they are quick and dirty experiments one writes to figure out some technical questions.

With the question of feasibility settled, it is easy to write a proper proof of concept. To evaluate expressions that go beyond `1 + 1`, we need to support variables. Now variables cannot easily be created because a variable declaration is not an expression in Dart. In Python, you can just declare a variable on the fly by assigning to it. In Dart, we can simulate dynamic fields by overloading `noSuchMethod` to create elements in a dictionary on the fly. I call this class `Scope` and when we [evaluate expressions within an instance](https://www.dartdocs.org/documentation/vm_service_client/0.2.3/vm_service_client/VMInstanceRef/evaluate.html) of it, the fields can be accessed like globals.

![]()

The code is actually more straight-forward:

With this, we can already do stuff like `a = 3`and `b = a*3`:

[![]()](https://asciinema.org/a/99312)

One limitation, we quickly run into is, that we can only access symbols that have been imported in the file that declares the `Scope` class. `import ‘…’;` cannot be evaluated using the VM service. So no `dart:io` if we don’t import it explicitly, and no custom libraries :(

Oh wait! Dart can spawn new isolates (independent workers) using a URI with [Isolate.spawnUri](https://api.dartlang.org/stable/1.21.1/dart-isolate/Isolate/spawnUri.html). Users could specify additional imports on the command-line, and the REPL could generate source code to include these imports and then spawn a new isolate using the generated code that has the imports available for the user.

![]()

And it works \o/

[![]()](https://asciinema.org/a/99313)

## Supporting more Dart

Now another issue is that we only can evaluate expressions. Control statements like `if/else` blocks or `while` loops are not expressions. For statements, we could wrap them in a closure and execute the closure, which is a function call expression. Thus, `if (a == 1) print('a is 1!!');` would become

```
() { if (a == 1) print('a is 1!!'); }();
```

We just need to figure out if the input is an expression or a statement. This is difficult because we’d have to write a Dart parser for this. But Dart is written in Dart, and the `analyzer` package provides a parser that can parse any Dart code for free!

And thus, that is also solved.

[![]()](https://asciinema.org/a/99314)

## More imports

The last bit that keeps us from importing just any library is that by default a new Isolate only sees the packages that are mentioned in its `pubspec.yaml`. We want to support importing any library though. `Isolate.spawnUri` has a `packageConfig` parameter that allows us to specify a map from package name to package path. We can just use another command-line parameter to target another package and use its package config in our Isolate. Woohoo!

We quickly run into the problem that our Isolate needs to access the `analyzer` package (and others) that might not be loaded by whatever package you want to toy around with in your REPL session. Package `package_resolver` to the rescue! With it, we can easily manipulate package configurations.

With all this, we have a full workflow implemented:

[![]()](https://asciinema.org/a/99316)

## What’s next?

This was a long post… The whole proof of concept clocks in at **451 lines of code**, so almost as long as this post.

![]()

The code can be found on [https://github.com/BlackHC/dart\_repl](https://github.com/BlackHC/dart_repl/tree/master/lib). You can give it a go easily if you have Dart installed:

```
pub global activate dart_repl  
pub global run dart_repl
```

I really enjoyed creating this proof of concept in my spare time. All the pieces just fell into place within a couple of hours. IDE support for Dart in Intellij is excellent, and there are a ton of documentation and articles around now. Check out 

[Natalie Weizenbaum](https://medium.com/u/a81c627aeff9?source=post_page---user_mention--f327e3769b6f---------------------------------------)

’s Unboxing Packages series for example: <http://news.dartlang.org/2016/04/unboxing-packages-async-part-3.html> et al. Low-level hacking in Dart is fun, and there are great libraries to get creative with. `code_builder` is looking very promising and `built_collection` is providing immutable collections. 

[David Morgan](https://medium.com/u/7c51fc1918ba?source=post_page---user_mention--f327e3769b6f---------------------------------------)

 has also been publishing articles on [immutable collections](/dartlang/darts-built-collection-for-immutable-collections-db662f705eff#.kj3ubd2xj) in Dart.

For `dart_repl`, it would be nice to import additional libraries at runtime without restarts. The Dart team has recently added support for hot reloading to the VM. This mainly provides a better experience in [Flutter](https://flutter.io/) for mobile app developers. Maybe, this could be used for adhoc imports and for defining functions and classes in the REPL, too.

In general, Dart could be great for research and for researchers, and I would absolutely love to see Jupyter support for Dart. One would only have to implement its kernel interface to make such a Dart REPL compatible with it… :) That should be easy, right?

![]()