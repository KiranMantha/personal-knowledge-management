---
title: "Comparing bundlers: Webpack, Rollup & Parcel"
url: https://medium.com/p/f8f5dc609cfd
---

# Comparing bundlers: Webpack, Rollup & Parcel

[Original](https://medium.com/p/f8f5dc609cfd)

# Comparing bundlers: Webpack, Rollup & Parcel

[![Garima Bhatia](https://miro.medium.com/v2/resize:fill:64:64/0*GdI-3F-6ll-c68Si.)](/@garimabhatia806?source=post_page---byline--f8f5dc609cfd---------------------------------------)

[Garima Bhatia](/@garimabhatia806?source=post_page---byline--f8f5dc609cfd---------------------------------------)

6 min read

·

Jun 12, 2018

--

21

Listen

Share

More

Press enter or click to view image in full size![]()

Press enter or click to view image in full size![]()

Press enter or click to view image in full size![]()

> **Module Bundling In Javascript:**

Module Bundling, on a high level, is a process of integrating together a group of modules in a single file so that multiple modules can be sent to the browser in a single bundle.

When we write our code in a modular pattern:

* We keep our javascript in separate files and folders based on functionality.
* Add the script tag for each file that we are using in correct order of dependency.

For each script tag , browser will send the request to the server which will have bad effect on the performance of our application. In order to overcome this we usually create a single bundled file which will integrate all the other files and that bundled file is sent to browser.

Module bundling can also include a minification step i.e. all the unnecessary characters like space, comma, comments etc. are removed from the file and its minified version is created and whenever a request comes from the browser that minified version is sent back. Less data means less browser processing time.

![]()

![]()

Apart from creating a bundle and minifying the code, a module bundler also provides features for good developer experience such as hot reloading, code splitting etc.

There are a lot of module bundlers in market today like webpack, browserify, rollup, parcel etc. Here we will be focusing on comparision between webpack, rollup and parcel.

> **Webpack vs Rollup vs Parcel :**

All these bundlers came up with a different approach of solving a problem which existing tools couldn’t solve.

Webpack was designed to solve the problems of asset management (i.e. it can include any type of file, even non-javascript files) and code splitting. It’s very flexible and has a huge amount of plugins for every use-case you could imagine.

Rollup, on the other hand, came up with the idea of using a standardised format (i.e. ES2015 module format) to write your code and tries to get really small builds with the help of dead code elimination.

Parcel tries to give you “blazing fast” bundling as it uses multiple worker processes to ensure that the compilation process is executed in parallel on multiple cores without the need of any configuration.

I will be doing further comparisions between these three on the following points:

### **1. Configuration:**

Webpack and rollup both require a config file for applications. The config file contains the options related to entry, output, plugin, transformations etc. There is a slight difference between rollup and webpack config file.

* Rollup has node polyfills for import/export, whereas webpack doesn’t.
* Rollup has support for relative paths, whereas webpack does not, so we either use path.resolve or path.join.

Parcel, on the other hand doesn’t require any config file to be specified. It will do everything out of the box.

### 2. **Entry points:**

Webpack supports only javascript file as entry point in config file. In order to support other formats such as html we need to add third party plugins.

Rollup can take an html file as entry point but in order to make that happen we need to install a plugin (eg. rollup-plugin-html-entry).

Parcel can take *index.html* file as entry file and it figures out which javascript bundles to create and download by looking at the script tag in the index.html file.

### 3. **Transformations:**

Module bundlers require javascript files to create a bundle. They cannot process any other format directly. So, in order to process files other than javascript , we need to first convert that format into javascript then we will pass it to the bundler. This process of conversion is called transformation.

Webpack uses loaders of different formats for transformation. eg: style-loader, css-loader for css files. We need to configure the file type and corresponding loader to be used in it’s config file.

Rollup uses plugins for transformation. We need to specify the plugin in the rollup config file.

Parcel supports various transformations like css, scss , images etc without config file. Parcel automatically runs these transforms when it finds a configuration file (e.g. `.babelrc`, `.postcssrc`) in a module.

### 4. Tree Shaking:

Tree shaking, in javascript context, refers to dead code elimination.

In order to implement tree shaking in webpack we need to:

* Use ES2015 module syntax (i.e. `import` and `export`).
* Add a “sideEffects” entry to your project’s `package.json` file.
* Include a minifier that supports dead code removal (e.g. the `UglifyJSPlugin`).

Rollup statically analyzes the code you are importing, and will exclude anything that isn’t actually used. This allows you to build on top of existing tools and modules without adding extra dependencies or bloating the size of your project.

Parcel doesn’t support tree shaking yet.

### 5. Dev Server :

A development server is a type of server that is designed to facilitate the development and testing of programs, websites, software or applications for software programmers. It provides a run-time environment, as well as all hardware/software utilities that are essential to program debugging and development.

Webpack provides a plugin called `webpack-dev-server` which provides a simple development server with live reload functionality. We need to add this plugin in our project and add some configuration specifying the file to serve when we run this and a script to run webpack-dev-server in package.json.

To implement development server in rollup, we need to install `rollup-plugin-serve` which will just rebuild the script whenever we make any changes but in order to provide live reload functionality we need to install another plugin `rollup-plugin-livereload`. Both the plugins need to be configured.

Parcel has a development server built in, which will automatically rebuild your app as you change files.

### 6. Hot Module Replacement :

Hot Module Replacement (HMR) exchanges, adds, or removes modules while an application is running, without a full reload. This can significantly speed up development.

Hot Module Replacement is one of the most useful features offered by webpack. It allows all kinds of modules to be updated at runtime without the need for a full refresh. `webpack-dev-server` supports a `hot`mode in which it tries to update with HMR before trying to reload the whole page.

Rollup doesn’t do hot module replacement (HMR).

Parcel has built-in support for hot module replacement.

### 7. **Code Splitting :**

Loading application code can take a long time, especially on mobile. Code-splitting breaks your app into smaller chunks, so that the user only has to load enough JavaScript to get started, and the application can quietly fetch the rest whenever it becomes relevant.

Code Splitting is the most compelling feature of webpack. There are three general approaches to code splitting available in webpack:

* Entry Points: Manually split code using `entry` configuration.
* Prevent Duplication: Use the `CommonsChunkPlugin` to dedupe and split chunks.
* Dynamic Imports: Split code via inline function calls within modules.

Rollup has recently added experimental code splitting feature. Split chunks created by rollup are *themselves* just standard ES modules that use the browser’s built-in module loader without any additional overhead. We need to set `experimentalCodeSplitting` and `experimentalDynamicImport` flags to true in the config file.

Parcel supports zero configuration code splitting. Here code splitting is controlled by use of the dynamic `import()` function [syntax proposal](https://github.com/tc39/proposal-dynamic-import), which works like the normal `import` statement or `require` function, but returns a Promise. This means that the module is loaded asynchronously.

To demonstrate this, I have created a small project using each of the above bundlers. I have added the basic configuration in the project.

> Rollup-config:

> webpack-config:

> **Build** **Results:**

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Below are the github links.

> Links:

[webpack-react-boiler-plate](https://github.com/garima33/webpack-react-boiler-plate/)

[rollup-react-boiler-plate](https://github.com/garima33/react-rollup-boiler-plate)

[parcel-react-boiler-plate](https://github.com/garima33/parcel-react-boiler-plate)

Originally posted at [blog.imaginea.com](https://blog.imaginea.com/comparing-javascript-module-bundlers-webpack-rollup-or-parcel/)