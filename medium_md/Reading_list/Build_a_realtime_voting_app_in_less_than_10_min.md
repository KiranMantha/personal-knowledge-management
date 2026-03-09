---
title: "Build a realtime voting app in less than 10 min"
url: https://medium.com/p/336ec364b5da
---

# Build a realtime voting app in less than 10 min

[Original](https://medium.com/p/336ec364b5da)

# Build a realtime voting app in less than 10 min

[![Srushtika Neelakantam](https://miro.medium.com/v2/resize:fill:64:64/1*_mV9ia0k7MiWxILUAzg69Q.jpeg)](/@n.srushtika?source=post_page---byline--336ec364b5da---------------------------------------)

[Srushtika Neelakantam](/@n.srushtika?source=post_page---byline--336ec364b5da---------------------------------------)

6 min read

·

Mar 5, 2018

--

2

Listen

Share

More

Realtime technology and data are making applications more useful and practical. The whole realtime world is so fascinating and every bit of its exploration only makes one more awestruck!

This tutorial is a follow to a [talk](https://youtu.be/PJZ06MLXGwA) I did in March 2018 at the [ngVikings Conference](http://ngvikings.org) held in Helsinki, Finland! The [presentation](https://speakerdeck.com/srushtika/understanding-the-realtime-ecosystem-2) can be viewed on my [profile](https://speakerdeck.com/srushtika) on speaker deck.

## What will we build?

![]()

We will build a simple voting app that allows the conference attendees to vote for their feedback about the conference in realtime as shown above!

The attendees will use another application that consists of three simple buttons, one for each type of vote. Once, a user has voted, all the buttons are disabled so they do not vote repeatedly. However, this application is not foolproof as it doesn’t require user login and hence, a single user can cast multiple votes by repeatedly refreshing the page. Hence, this is just for a realtime demo :)

Press enter or click to view image in full size

![]()

## Demo

If you just wish to try out the final outcome, fire up a browser and open up the angular app hosted, [here](https://188l9p4jj.codesandbox.io/). Now from a mobile or another browser window/tab, open up the vote casting app hosted, [here](http://tiny.cc/realtime-voting).

The complete source code is hosted on my [GitHub repo](https://github.com/Srushtika/realtime-voting).

## What will we use?

We’ll use a few JavaScript frameworks and Libraries that would make our work easy and more presentable.

### 1. Ably for realtime functionality

![]()

[Ably](https://ably.com/) is an excellent realtime messaging platform that makes it easy to add realtime functionality to our applications. It comes with both realtime and REST libraries to be used in accordance with the use case. For our app, we’ll use [Ably’s realtime library](https://ably.com/documentation/realtime) which lets us connect to the platform over WebSockets. For this, you’ll first need to create a new account (you can get one for free) [here](https://ably.com/) and obtain an APP URL from the dashboard.

### 2. Chart.js for building beautiful charts

Press enter or click to view image in full size

![]()

[Chart.js](http://www.chartjs.org/) is a library that lets us easily include beautiful graphs that represent either static or dynamically changing data. We’ll use Chart.js to show the votes cast by our users.

### 3. Angular 4 CLI as a frontend framework

Press enter or click to view image in full size

![]()

We build the voting app using Angular 4. Why? Because Angular is a really good JavaScript framework for building frontend web apps. Moving forward, Angular has the potential to beautifully present the data obtained in realtime using a platform such as [Ably](https://ably.com/). If you don’t already have this installed on your system, follow [these](https://cli.angular.io/) simple steps from the [website](https://cli.angular.io/).

## Getting started

We’ll have a detailed look at the angular app that shows the graph with vote numbers in realtime. However, we’ll only skim through the client app with three buttons that let users cast these votes since it’s super simple!

Note: This tutorial is a high-level overview of how the app is built, if you wish to copy the code, please visit the [GitHub repo](https://github.com/Srushtika/realtime-voting).

### Creating a new Angular4 application via CLI on macOS terminal

Before we get started, make sure that the Node Package Manager([npm](https://www.npmjs.com/get-npm))and [Angular CLI](https://cli.angular.io/) are installed on your computer.

Start by creating a new Angular app. I’ve named it *ng-vote-ably*, feel free to modify this.

Next, move into the new project folder and serve this app locally on your browser to ensure that there were no problems in the initial setup.

If everything so far works, we shall start with creating a new component that will hold our chart. I’ve named the component *vote-chart*, feel free to modify this.

Press enter or click to view image in full size

![]()

Now within the index.html file inside the src folder, add two scripts each for Ably and Chart.js, as shown below:

Press enter or click to view image in full size

![]()

Next, navigate to src->app->app.component.ts and modify it to contain the follows:

Press enter or click to view image in full size

![]()

Note that a new tag ‘app-vote-chart’ is also added which will hold the content from the new component that we created earlier.

The ‘title’ variable is declared in src->app->app.component.ts. Modify it’s contents to ‘Vikings’ so that when interpolated in the HTML file, it would make some sense.

### vote-chart component

Let us now write some real code!

In the HTML file for the component, add a new div that will contain the canvas for our graph as shown below:

Press enter or click to view image in full size

![]()

Now in the component’s TS file, we’ll connect to Ably’s realtime library using:

> this.ably = new Ably.Realtime(‘<YOUR-APP-URL>’);

Attach to the channel on which votes will be published by the users as follows:

> this.receiveChannel = this.ably.channels.get(‘vote-channel’);

Next, subscribe to updates on this channel so that a callback function is triggered whenever any data (new votes) is published on this channel as follows:

> this.receiveChannel.subscribe(“update”, function(message: any) {}

But before doing this, make sure to import chart.js and declare the Ably variable. Our goal is to update the graph every time a user publishes any votes on the channel called ‘vote-channel’, this is shown below. Your *vote-chart.component.ts* file should contain the following:

Press enter or click to view image in full size

![]()

As seen above, we create a new chart and set the labels and the actual data which comes from the vote publishers. Further, each type of vote has a different background colour. For every vote published, we increment a simple counter and update the chart to reflect this new data.

### Publishing votes

The complete code for the app containing the buttons which can be used to cast the votes can be found [here](https://glitch.com/edit/#!/clear-pirate). It’s a simple JavaScript application that publishes votes on the channel ‘vote-channel’ when a button is clicked, as show here:

Press enter or click to view image in full size

![]()

## That’s it!

Your realtime voting app is now ready. If you have any difficulties in implementing this app or if you have questions about anything, feel free to reach out to me by commenting on this post or via [Twitter](http://twitter.com/Srushtika).

If you wish to stay updated about what’s happening in the realtime tech world, subscribe to Ably’s Newsletter!

Claps and share if you found this tutorial helpful :)