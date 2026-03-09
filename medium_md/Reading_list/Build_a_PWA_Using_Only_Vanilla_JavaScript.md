---
title: "Build a PWA Using Only Vanilla JavaScript"
url: https://medium.com/p/bdf1eee6f37a
---

# Build a PWA Using Only Vanilla JavaScript

[Original](https://medium.com/p/bdf1eee6f37a)

# Build a PWA Using Only Vanilla JavaScript

[![Sayan Mondal](https://miro.medium.com/v2/resize:fill:64:64/0*GXBNZh80MX-Ptc15.jpg)](https://sayanmondal342.medium.com/?source=post_page---byline--bdf1eee6f37a---------------------------------------)

[Sayan Mondal](https://sayanmondal342.medium.com/?source=post_page---byline--bdf1eee6f37a---------------------------------------)

14 min read

·

Sep 30, 2019

--

3

Listen

Share

More

Press enter or click to view image in full size

![]()

## Progressive Web App (PWA)

*“A Progressive Web App (PWA) is a web app that uses modern web capabilities to deliver a native app-like experience to users. These apps meet certain requirements (see below), are deployed to servers, accessible through URLs, and indexed by search engines.”*

A Progressive Web App (PWA) works like any other normal app but with a lot of added features and a lot less hassle. They are fast, reliable, and can work perfectly in an offline environment.

Press enter or click to view image in full size

![]()

## Why should we use it?

Progressive Web Apps (PWAs) creates a very rich experience for the users because they are:

* **Responsive**

A PWA can be built to fit into a desktop browser, mobile phone, or TV screen— any product that supports internet connection and has browser support.

* **Reliable**

It uses a technology called a **Service Worker** which enables the users to load PWAs instantly in their environment. A PWA can give offline support for the application, and the user won’t face network related issues.

* **No App Store/Play Store**

Users don’t need to visit an app store to download these Progressive Web Apps. They can be installed instantly and directly from the browser. Requires no waiting time as they are very quick and give a native application like simulation.

* **Engaging for developers as well as users**

Developers can also add/play around with tons of features in the manifest files. One of the most well-known features is re-engaging users with push notifications enabled by the PWA.

* **Easy to share**

Progressive Web Apps are very easy to share with your friends or colleagues. All that a user needs to share is the website/app URL. Users don’t need to share an installable apk or go through the process of verification followed by downloading tons of files. All that a user requires is a simple click.

*To learn more about Progressive Web Apps visit this* [*link by Google Developers*](https://developers.google.com/web/progressive-web-apps/)

Press enter or click to view image in full size

![]()

## Creating a Basic PWA

In this tutorial, we are going to build a PWA using only vanilla JavaScript but to do that we’ll need to make a normal Web App first.

Before proceeding any further, let’s have a look at what our final UI would look like and the functionality we are trying to achieve.

## Final Project UI

Press enter or click to view image in full size

![]()

The UI will display colored boxes in the middle, and clicking on the boxes will play short music clips.

Similarly, each box produces different musical clips. The concept of this website is to mix different music and create your own while playing around with it.

## GitHub Repository

All the files related to this project is present here: [***https://github.com/S-ayanide/MixCentro***](https://github.com/S-ayanide/MixCentro)

During this tutorial, you’ll need to download certain assets which are available in the GitHub repo. If you want to create, change, or modify something, I’d suggest you do that once you’ve completed this tutorial.

## Web App HTML

The HTML for this project will be very simple. We’ll be needing divisions for individual colorful pads as displayed and the audio for each one.

Let’s take a look at this code snippet:

All we are doing here is naming our title and header as MixCentro as that is the name we’ve chosen for this website (feel free to choose your own).

You’ll be needing sounds for this project to work, go ahead and download that from the [GitHub repository](https://github.com/S-ayanide/MixCentro) mentioned above which contains all the sound files.

We’ve created a main division “**pads**” and that contains “**pad-top**” and “**pad-bottom**” which does nothing but create the pads we see in the UI, divided into two parts, each containing 3 pads.

The top pad is termed as “**pad-top**” with three pads consisting of different audio. Similarly, the bottom pad division is termed as “pad-bottom” and consists of three pads as well.

Although **style.css** and **index.js** have been imported, we aren’t using them as of now.

## Web App CSS

Now we can build a stylesheet at the root of the directory. I’ve called it `style.css`.

By default, we get a margin and padding at the sides of our screen, in our case we don’t want that to happen. So let’s manually remove any padding and margins which have been added by default.

Since we’ve added headers in our HTML file and it also has no background, we need to make our website look attractive and subtle. To do that let’s upgrade the font’s styling and make it look better by adding a background which would go well with the theme.

In the GitHub repository mentioned above you can find an image already there for you in the path `images/bg/background.jpg` This is the same image as the one used in the UI preview.

## Importing Google Fonts

To move ahead further we’ll need to choose a nice and subtle font for our website. To choose from a wide variety of fonts we’d be using [Google Fonts](https://fonts.google.com/).

This might take a while since everyone’s choices and tastes are different. Choose one font and click on the ‘+’ button at the top right of the selected font.

Press enter or click to view image in full size

![]()

Once you click on that you’ll find a black bar appear on your screen which says “**1 Family Selected**”, upon clicking on that bar it expands and lets you see something similar to this.

The details might be a little different as it depends on the font you’ve selected but the rest remains the same. We’ll be using the standard way of importing the font here, so let’s go ahead and copy the whole `<link href … >` provided in the grey box.

To use the font in effect open your `index.html` file and paste this link anywhere between the `<head>` tags.

## More Styling

After importing our font, it’s time to reflect that on the main browser as well

In my case, I’ve used the font-family “Lexend Exa” and also added the background image mentioned earlier. To maintain a continuous, evenly spaced layout we’re using a flexbox with the contents justified with a space between property.

We also keep a class called “pads” which has a width of 60% so that it takes only a little more than half of the screen which makes it not too expanded and also keep it tight and gentle looking.

The divisions inside the “pad-top” and “pad-bottom” classes have been targeted so that they grow to their potential width and height and also keep the flex property equal to 1 so that they are projected out in front.

We finally assign different hex colors for all of our pads.

## Adding Media Queries

Lastly, we add media queries to control the responsive nature of our application.

In this simple code, we only control the size of our fonts which we’re shrinking if the screen size drops below 480 pixels and also add some margin at the bottom to make it look better.

![]()

Press enter or click to view image in full size

![]()

## Add Vanilla JavaScript Functionality

At this point, we have our wonderful UI set up, but the pads don’t produce any sounds upon clicking them. Why is that?

Our division at this point already has the audio present inside of it but to play that particular sound upon user click, we call a `play()` function. That’s where JavaScript comes in.

Our basic JavaScript code would be very simple and would just consist of 11 lines only.

In‌ ‌the‌ ‌beginning, we are gathering sounds and pads by storing the whole query which is targets the HTML classes `.sounds` and `.pads` respectively and stores them into variables.

But we want to perform this operation whenever the window loads first, therefore we wrap everything inside a `window.addEventListener(‘load’)`.

Next we add a `forEach` which loops through all the pad divisions. It has two parameters: one is pad which initializes itself to each individual pad every time it loops, and the other is an index which is required to play the sound of that particular pad.

We utilize the sound from the above sound variable to play the file associated with the individual pads with the help of the `play()` function.

We use something like a `currentTime = 0`. the reason we do that is we are re-initializing the time back to zero every time a pad plays so that we can play one pad for multiple times upon multiple clicks on the same pad itself.

***Congratulations, You’ve just built a Web App with vanilla JavaScript. You can play around with it or even deploy it online for others to use. But wait! we still have to convert this Web App into a Progressive one. Let’s dive in.***

Press enter or click to view image in full size

![]()

## What is a Web App Manifest?

A Web App Manifest is a simple JSON file which contains the details of your Progressive Web App and tells the browser how it should behave when it is installed in a user’s device.

A manifest can contain information like the application name (full and short name), the app icon, the URL it points to which will open once the app launches, control theme colors, etc.

## Build a Manifest File

Creating a Progressive Web App a manifest file is essential since it controls the behavior of the browser upon installing it in the user’s device.

![]()

To create your own Web App Manifest, you can create a new file and name it as `manifest.json` and add further details in the JSON format. However, there is a better way of doing it by using the tools which are already provided to us online.

## Generate a Manifest Online

In this era, the internet already provides us with lots of time-saving options which come in handy once again when we create a `manifest.json` file.

Instead of typing the whole key-value pairs in a JSON format, simply navigate to this website: <https://app-manifest.firebaseapp.com/>

This is a Web App Manifest Generator and it only requires you to fill certain input fields and it will automatically generate a manifest for you.

Things to consider while filling the input fields:

* Give your application a full and a short name.
* A theme color and background color is important as it can modify the browser version of the normal Web App and provide more life to it.
* Change the Display Mode to `‘standalone’`.
* Remove the “Application Scope” for now.
* Make the value for the Start URL as a `‘.’` since we want to create the PWA at the root directory itself.
* On the right-hand side, you’ll see a button called ‘ICON’. Choose an image to use as your app icon then simply drag and drop/upload it here.

***Note: Make sure your icon size doesn’t exceed 512x512 resolution since the icons undergo scaling for them to fit into different devices.***

Once all of that is done, click on ‘**GENERATE .ZIP**’ and extract all the contents of the zip file into your project folder.

At this point, you’ve just added your manifest file in your project but aren’t using it. To actually reflect the manifest file in your project, add a link to it in the `index.html` file in-between the `<head>` tags.

```
<head>  
   <link rel=”manifest” href=”manifest.json”>  
</head>
```

***Viola***! You’ve got your readymade manifest file in your project now.

Press enter or click to view image in full size

![]()

Now we will add new dependencies using Yarn.

## What is Yarn?

Yarn is a new package manager that replaces the existing workflow for the NPM client or other package managers while remaining compatible with the NPM registry. A package manager servers the purpose of installing some packages which serve a particular purpose.

## Advantages of using yarn

Of course, there are other package managers, but for this project, we will use Yarn for a few reasons:

* Package downloading occurs only once i.e. no requirement for a second-time download.
* It is more secure.
* Uses lock format which locks dependencies ensuring that both the system works on the same packages/dependencies.

## Installing Yarn in your system

Installing yarn in your system is very simple. All you need to do is visit <https://yarnpkg.com/lang/en/> and click on “**Install Yarn”**,and the download will start automatically.

Press enter or click to view image in full size

![]()

Just follow the normal setup procedures and the Yarn installation will start in your system, and the path will also modify itself in your environment variables automatically.

Another alternative to this method is by using **npm** and this is easy as well. If you are already using **npm** then simply open a terminal and type:

![]()

To check if yarn installation was successful in your system or not, open a terminal and type:

![]()

If you get a response like **1.16.0** or anything similar, that means Yarn has been successfully installed and you are good to go.

## Initializing a yarn project

To create a new yarn project the first step is to navigate into your project folder in your terminal and type this command:

Press enter or click to view image in full size

![]()

Once you type the `yarn init` in your terminal, you’ll receive a lot of questions. When you answer these questions, the response will store itself in a `package.json` file which keeps all the information.

At first, a name will be asked to you. In there type the name of the project which you want to keep. As for other fields, you can keep them empty or type your own specification if you choose.

A very important question which should not be skipped is the **entry point**. It decides where the entry point of our project should be. Initialize it to **index.js** which we created earlier.

Once you finish this step you’ll find lots of new folders and files populated in your project. If that’s the case, pat your back because you’ve successfully initialized your first yarn project.

***Note: yarn init should be done after navigating to the project folder so that index.js is accessible as an entry point***

## Installing a Package Called Serve

Since a Progressive Web App (PWA) requires a live server to run, we need at least a localhost to test our application. So, we need to install a package called `serve`.

`serve` works best when we want to test a static site using a server. We can check how it runs in localhost and then push it into a deployment later.

To install `serve` in your project we simply type the following in the terminal (after navigating into your project folder):

![]()

This will add the dependency into your project and you can view it inside the `package.json` file.

To run your static page in a local server, we need to start the server first using this dependency. To start the server type, `yarn serve`in your terminal.

Press enter or click to view image in full size

![]()

You will see something similar in your case providing you the details about your localhost and network address. You can open any one of them to view your static website running on a local server.

Press enter or click to view image in full size

![]()

## What is a ServiceWorker?

*“A* [*service worker*](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API) *is a type of* [*web worker*](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API)*. It’s essentially a JavaScript file that runs separately from the main browser thread, intercepting network requests, caching or retrieving resources from the cache, and delivering push messages.”*

Basically, a service worker runs separately from the main thread and are completely independent of the application they are currently associating with.

A Service Worker can control network requests, can handle caching, and also provide offline resource support through the cache.

A Service Worker has three steps involved in its lifecycle:

* Registration
* Installation
* Activation

## Registering the ServiceWorker First

To **install** our Service Worker we need to **register** it first into our main JavaScript file which in our case is **index.js**. Before proceeding any further let’s create a Service Worker file and call it `serviceWorker.js`.

The first step in the lifecycle of a Service Worker is Registration:

First checks for browser support thus we need to add it inside our `window.addEventListener()`. The service worker then registers itself with `navigator.serviceWorker.register`, which returns a promise that resolves when the service worker has been successfully registered.

The **scope** of a Service Worker is very important as it determines which files the service worker controls. In other words, from which path the service worker will intercept requests.

Thus we always prefer a Service Worker in the **root** directory so that it can control requests from all files at this domain.

## Creating Our serviceWorker.js Using Vanilla JS

Now that we already have our s`erviceWorker.js` file created and registered in our browser, we can confirm it by opening our inspect element tab and in the **Developer Tools** navigating to the **Application** menu.

Press enter or click to view image in full size

![]()

You’ll find that your Service Worker registration is successful and has also written in the message log of your console.

To make all of your assets available in our local cache we need to dynamically mention the path of all the static assets.

As a Service Worker is completely event-driven, we need to add events like install and fetch for it to perform them in the browser side.

## Install

An Install event calls itself every time the browser detects a new Service Worker. What we are targeting is to call the Cache API to retrieve all our static assets and save them for later.

In‌ ‌this‌ ‌case, we are calling our cache by the name `‘static-cache’`. You can use any name you want, but for the ease of simplicity, “static-cache” is preferred.

Since the Service Worker is a low-level API, we always need to tell it what to do. If at this point you moved back to the **Application** menu in your browser and simulate an offline environment, you’d still find nothing is happening.

Let’s solve this problem with the help of the **fetch** API.

## Fetch

In a Service Worker, we can decide how we want to respond to a given event. For that, we use a method called `respondWith()`.

In our case, we want to check whether there is something present in the cache first, and if not, we will fetch it from the network.

To create our cache-first approach, we create a function which matches the request with the files present in the cache itself. Thus the request acts as a key.

Now, this returns either undefined if there is nothing in the cache or the cache response itself.

To create a network-first approach, we want to create a dynamic cache where all the network assets if‌ ‌required, will be fetched. In the case that it’s unable to, it will fall back to the static cache.

This would fetch any request online if required by our browser and will be added using a `put()` method into our dynamic cache

With that now, when we visit our **Application** Menu we’d find two Cache Storage one **Static** and the other **Dynamic** which we just created.

Press enter or click to view image in full size

![]()

Now if we go back to our Service Workers and simulate an offline environment by clicking on the “Offline” checkbox, we would face no internet issues and the application will run smoothly because of all the cache storages.

![]()

**A Huge Congratulations for making it here, you now have your very own Progressive Web App which you can use/install on all the platforms.**

To install your PWA, simply deploy your project on an online server (free hosting would work as well). Once your website loads completely, you’ll find a small `+` sign at the right side of your address bar.

![]()

**Click on it to see your wonderful PWA install and work in your local system.**

[## Learn JavaScript - Best JavaScript Tutorials (2019) | gitconnected

### JavaScript is one of the most popular programming languages in the world - it can be found everywhere. JavaScript is a…

gitconnected.com](https://gitconnected.com/learn/javascript?source=post_page-----bdf1eee6f37a---------------------------------------)