---
title: "How to Setup a JavaScript Monorepo Like a Professional"
url: https://medium.com/p/cf71d13501c5
---

# How to Setup a JavaScript Monorepo Like a Professional

[Original](https://medium.com/p/cf71d13501c5)

Member-only story

# How to Setup a JavaScript Monorepo Like a Professional

## It’s not as hard as you might think

[![Daniel Cender](https://miro.medium.com/v2/resize:fill:64:64/1*UHZi47DcCbIQBH4LOLB_Vw.jpeg)](https://danielcender.medium.com/?source=post_page---byline--cf71d13501c5---------------------------------------)

[Daniel Cender](https://danielcender.medium.com/?source=post_page---byline--cf71d13501c5---------------------------------------)

7 min read

·

Dec 1, 2019

--

4

Listen

Share

More

Press enter or click to view image in full size

![]()

I have traditionally hated ESLint, Babel, Prettier, and the like. Don’t get me wrong, they are fantastic tools; it’s simply a nightmare to navigate setting up a new project with a conglomeration of these tools.

Last weekend I dug into the muck of how to bootstrap a decent JavaScript Monorepo, complete with code linting enforcement, testing support, and a decent build process.

If you’re like me at all, you’ve used Create React App for most of your prior React projects. It handles a lot for you, and it’s really quite good. But, what if you want to create a larger library using multiple distinct packages? What if you want tighter control over repository rules and scripts? Or just wanted to get the experience of setting up your own React environment from scratch? The answer to my query was [Lerna](https://lerna.js.org/), a convenient JS monorepo management tool.

I’d checked it out before, but I remember discounting the tool since it seemed all was well in my multi-repo project at the time. Now, at the tail end of this year-long project, I am wishing we’d applied some tighter control over code management and utilized Lerna.

So, here are some basics on how to set up a repository using Lerna, which will set you up for success down the road as your development process evolves.

## Create a Fresh Repository

Navigate to your profile in GitHub, or BitBucket (or what-have-you), and create a new repository. Then clone it with trusty old `git clone <url>` . Or, create a new folder with `yarn init` and `cd` into that. Don’t forget to add your `.gitignore` file. Here’s the simple one I’m using for this example project:

***For reference,*** I’ve uploaded the completed boilerplate set up as a [public GitHub repository](https://github.com/DanielCender/test-lerna-setup) on my profile, so we can see the final result of this guide.

### Now, some opinion

I personally prefer to use Yarn for my package management. Truthfully, the benefits of Yarn over NPM are minimal for most development projects, so it really doesn’t matter whether you manage your dependencies through one or the other. It’s just another case of [Red](https://www.npmjs.com/) vs. [Blue](https://yarnpkg.com/lang/en/). To my knowledge, the only edge Yarn holds over NPM currently is its use of global caching to install common dependencies even while you’re offline.

## Getting Lerna Running

Follow along with the [instructions here](https://lerna.js.org/#getting-started) in the case my instructions are out of date.

**TL;DR -** Run `npm install --global lerna` or `yarn add global lerna`, then `cd <proj folder>` && `lerna init`.

This should do the same as `npm init` or `yarn init` by creating a package.json file with the basic fields. Add the `--independent` or `--i` flag to the init command to set up versioning separately for your individual packages, which you’ll want if you *don’t* plan on deploying updates to all your packages at the same time.

Be sure that your lerna.json config file matches the NPM client of your choice. Mine looks like this:

You will then need to create at least one package to make this a productive space. So either run `lerna create <package name>` or `cd` into `packages` and `mkdir <folder>` your way to glory.

If using `mkdir`, be sure to run `yarn init` in that new package to get it set up properly.

## Setting Up ESLint

ESLint has been a thorn in my side for ages. It’s arguably the most finicky of all peripheral tools for a JS developer to grapple with, save for Babel. Babel is a beast.

### Setup

Per the docs, run `yarn add eslint --dev` , then `npx eslint --init` . If you’re using Yarn, be sure to select N for when the guide asks if you want to add packages using NPM. You should then have an `.eslintrc` file wherever you ran those commands. I personally like to install these tools in each sub-package that requires a particular setup. There are some strange complexities that occur when trying to require libraries or dependencies from the root directory. Most JS runtime/bundling tools look in the immediate directory for the respective `node_modules` package. [This piece of documentation](https://verdaccio.org/blog/2019/09/07/managing-multiples-projects-with-lerna-and-yarn-workspaces#managing-dependencies-and-devdependencies) by Verdaccio explains this good practice more succinctly than I do.

There are many linting standards that can be configured with ESLint. Airbnb’s style config is perhaps the most popular standard, but there’s also a [Google config](https://www.npmjs.com/search?q=eslint-config+google) that has a good following. If you don’t want to mess with that at all, a recommended config comes with ESLint and is already set by default in your `.eslintrc` file.

Here’s the base [Airbnb config](https://www.npmjs.com/package/eslint-config-airbnb-base), which includes all rules minus the ones relating to React.

If you are working with React, [this config](https://www.npmjs.com/package/eslint-config-airbnb) will include the rules you’ll need.

Per the README for both of those setups, there are a few ways to install all the dependencies necessary, but if nothing else you can just run `npm info "eslint-config-airbnb-base@latest" peerDependencies` to list the peer dependencies and versions, then run `yarn add --dev <dependency>@<version>` for each listed peer dependency (same for `eslint-config-airbnb`). **Remember** to install the config package too though, or you’ll get an error when running `eslint` .

Press enter or click to view image in full size

![]()

But our work’s not done there. We need to be sure to extend our ESLint `.eslintrc` (or other JS/JSON config) with `"extends”: [“airbnb"]` , which will tell ESLint to use the config in our modules.

Test out our new ESLint setup by making a sample index.html file in your first package/ directory.

Then create a simple `index.js` file for ESLint to run on.

This index.js file should throw a couple errors when we run ESLint on our package.

Add `“lint”: “eslint — debug index.js”` to `“scripts”: {}` in your packages’s `package.json` file, so it looks like this:

This will signify a successful ESLint setup if we run `yarn lint` or `npm run lint` and we get syntax errors from ESLint in our console.

If you set up ESLint and those Airbnb config plugins at the root of the Lerna repo, then you may get errors when running that `yarn lint` script in the packages 📦. For the swiftest setup, it’s best to treat each package as a separate repository and define all dependencies explicitly, dev or ordinary.

## Setting up Parcel

Okay, with ESLint all set up, we should be set to start configuring our package for bundling. For this, we’ll use Parcel, a zero-configuration web app bundler. I have found Parcel to be worlds easier to get running than Webpack. Defer to [this part](https://parceljs.org/getting_started.html#adding-parcel-to-your-project) of their Getting Started page for adding Parcel to your package.

I will run: `yarn add parcel-bundler --dev` and add the necessary scripts to our simple package.json file. Our file should now look like this, minus dependency version differences.

At this point you should be able to run: `yarn dev` to spin up a development bundle that will be served at `http://localhost:1234` by default. Notice how parcel is pointing to the entry point of index.html, since that file imports our only JS file in the package so far. The `lint` script will still run explicitly on that JS file, however.

At this point, you could move on and use this setup to manage a simple Vanilla JS project with hand-crafted HTML. Almost safe to say most projects will want to include a framework like React, however.

## Adding React

Just run `yarn add react react-dom` in your package. Edit your HTML file and add a `<div id="app"></div>` inside the `<body></body>` tags where you can attach your React application.

Replace `index.js` with a basic React application boilerplate.

This should work out of the box if we just run `yarn dev` again. Refer to [this article](https://blog.jakoblind.no/react-parcel/) if you’d like to see this setup in the context of a standalone repo.

## Babel Setup

Parcel makes it unbelievably easy to use Babel for our React app. All we need to do is install our Babel presets and add a `.babelrc` file to our package.

Run: `yarn add --dev @babel/preset-react @babel/preset-env`

Add a `.babelrc` file:

Parcel will detect this configuration and default to using Babel for transpiling our JSX and ES6 code to ES5 syntax. We we run `yarn dev` yet again we’ll notice Parcel-bundler using Babel to bundle our starter application.

This is by no means a comprehensive guide on how to setup/manage/deploy use monorepos, but simply a starting point of how to get set up for a simple web-based application. If this article proves helpful for any, I release another outlining how to integrate testing libraries for React and non-React setups.

There’s so much that goes into every unique application’s setup and maintenance that no one guide could fit them all. My personal and professional time of working with Lerna has been pleasant and eye-opening to how larger teams manage projects subject to rapid development changes and tightly-integrated sub-module systems.

I started to look into the monorepo setup after building a project using React and the Serverless framework, with both pieces existing in separate repos. Many bugs, needless complexity, and change management hardships could have been eliminated if we had used a monorepo setup in development.

To close, here’s some very recognizable projects that use Lerna in similar setups:

* [Babel](https://github.com/babel/babel)
* [Create React App](https://github.com/facebook/create-react-app)
* [React-Router](https://github.com/ReactTraining/react-router)
* [Pug](https://github.com/pugjs/pug)
* [Jest](https://github.com/facebook/jest)
* [Storybook](https://github.com/storybookjs/storybook)
* [Gatsby](https://github.com/gatsbyjs/gatsby)
* [Gutenberg](https://github.com/WordPress/gutenberg)
* [AWS Amplify JS](https://github.com/aws-amplify/amplify-js)

> My name is Daniel Cender, and I am an avid technologist in constant development of my craft. Currently a huge fan of all tools Web, GraphQL, and Mobile.
>
> If you found this article helpful, please share it and spread the knowledge! If you experienced any bugs or issues with my guide, please drop a response and I will promptly look into it.