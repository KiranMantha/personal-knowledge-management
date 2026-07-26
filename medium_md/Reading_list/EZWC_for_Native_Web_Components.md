---
title: "EZWC for Native Web Components"
url: https://medium.com/p/e574a6f39de
---

# EZWC for Native Web Components

[Original](https://medium.com/p/e574a6f39de)

# EZWC for Native Web Components

[![Will Steinmetz](https://miro.medium.com/v2/resize:fill:64:64/1*bpg4C-2BT3RtPo2vuLdT_A.jpeg)](https://medium.com/@willsteinmetz86?source=post_page---byline--e574a6f39de---------------------------------------)

[Will Steinmetz](https://medium.com/@willsteinmetz86?source=post_page---byline--e574a6f39de---------------------------------------)

4 min read

·

May 15, 2019

--

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3De574a6f39de&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fezwc-for-native-web-components-e574a6f39de&source=---header_actions--e574a6f39de---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

Both in my career and in personal projects, I’ve been making more and more use of native web components. At this point in mid-2019, browser support is pretty wide-spread making it a much easier to task with fewer polyfills required.

At the same time, I’ve been learning and using [Vue](https://vuejs.org/) over the last few months. I enjoy using it and it’s a great library for smaller/lighter projects. Having used Polymer years ago when it first came out, one of the things I noticed right away was that the [single-file component .vue file](https://vuejs.org/v2/guide/single-file-components.html) structure resembled the component style in early versions of Polymer. I like the structure and organization of the single-file component format because it forces me to keep components smaller and more concise by allowing me to see when I need to break things down faster.

While working on using native components more, I found myself wanting to organize the component code in an easier way for me to read. That want combined with my goal of getting better at writing Node-based applications gave me an idea: why not create the ability to do that myself?

## Introducing EZWC

[EZWC](https://github.com/pynklynn/ezwc) is short for easy web components. It’s comprised of a CLI and file structure resembling Vue single-file components with the file extension `.ezwc`. I wanted to make it as useful as I could early on so it also supports writing the script code with Typescript, Sass, a few templating engines, and separating the component pieces into their own files similar to Angular 2+ components.

Example of a very basic EZWC component:

To convert this to a native web component, run it through the CLI:

The output file (in this case `dist/hello-world.js`) is a JavaScript file containing a native web component (in ES2015+ format) that can be immediately imported into the rest of the code base, built by your tool chain, and used in a page!

You may notice that in the EZWC file, there is no attaching of the shadow root, defining the custom element with the browser, or setting up the rendering for the component. These are taken care of by the CLI. The CLI will look for the `lang` attributes on each container tag to do the appropriate actions and add an import for templating engines. The script tag also has a required `selector` attribute. The `selector` attribute and class name are used by the CLI to generate the `createElement.define()` code for the final output.

## Other Features

Some other features include:

* Generator command to generate a new EZWC component (including imports if the appropriate flags are used)
* Ability to create a component without a shadow root via the `no-shadow` attribute on the `<script>` tag
* Add a config file to the project to remove the need to pass in options on each run — including default options for commands such as generate
* Watch flag to automatically transpile components on change — including imported source files!

## Where This Project Is Going

I put this out there into the world to see if it is useful for other people. It’s entirely possible that it may not be and that is OK because this has been a great learning experience for me.

The next task I have planned is a `new` command to initialize a project making use of EZWC. The command will run a wizard that will ask questions for default options to create a config file and will create the directories for the project, source code, and compiled code. This will make it easier to create a project using EZWC and use the defaults from the config file when generating new components.

Some planned features that I would gladly welcome help on include:

* LESS support
* Stylus support
* Webpack loader — once this exists, I have plans for further enhancements to the `new` command such as including a router library
* Syntax highlighters and intellisense for editors/IDEs such as Visual Studio Code

I’m also trying to figure out as time goes on if there is any other syntactic sugar that could be added to the CLI such as:

* Generating an invalidator method for more efficient template rendering when an attribute changes
* Shorthand for creating getters/setters for attributes and whether or not to watch the attribute

It is still early days for this project so it may not be ready for production yet. If you happen use it and find a bug, please feel free to file a bug report on GitHub or open a pull request if you are open to fixing it.

Thanks for reading and let me know if you find EZWC useful in a project!