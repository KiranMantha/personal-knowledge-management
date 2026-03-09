---
title: "How to build a Chrome Extension to save web content to Cosmic JS"
url: https://medium.com/p/ca503ceabd84
---

# How to build a Chrome Extension to save web content to Cosmic JS

[Original](https://medium.com/p/ca503ceabd84)

# How to build a Chrome Extension to save web content to Cosmic JS

[![Tony Spiro](https://miro.medium.com/v2/resize:fill:64:64/0*slEndc0ZwyA05fNb.png)](/@tonyspiro?source=post_page---byline--ca503ceabd84---------------------------------------)

[Tony Spiro](/@tonyspiro?source=post_page---byline--ca503ceabd84---------------------------------------)

2 min read

·

Mar 21, 2018

--

Listen

Share

More

Press enter or click to view image in full size

![]()

In this tutorial, we’re going to build a Google Chrome extension to save web content to [Cosmic JS Buckets](https://cosmicjs.com). Think of it as your personal web clipper.

## TL;DR

[**Download the code from the GitHub repo**](https://github.com/cosmicjs/content-grabber)

## Pre-requisites

You just need to have Chrome installed for testing it out and nothing else.

## Installing the demo

1. Get the source code into your machine by either downloading or cloning the repo, which is located [**here**](https://github.com/cosmicjs/content-grabber)**.**
2. In Chrome, visit `chrome://extensions`
3. Enable Developer mode by ticking the checkbox in the upper-right corner.
4. Click on the “Load unpacked extension…” button.
5. Select the directory containing your **unpacked** extension.
6. Refresh loaded pages.

You’ll now see the extension icon to the right of the Omnibox. Click on it and login with your Cosmic JS credentials. You can now start saving content to your buckets.

## Understanding the Source Code

The defining file in a Chrome extension is the [manifest.json](https://github.com/cosmicjs/content-grabber/blob/master/manifest.json) file. Most of the fields in the Manifest are self explanatory. Let’s go through the major fields, and see what each file do.

* `manifest_version` is "2". it is very important not change it because it is a sign to chrome to how to compile the extension.
* `permissions` includes the permissions which extension needs  
  -`storage` permission allows you to store data at "Chrome local storage" which is important to save data across websites and different pages.  
   -`https://api.cosmicjs.com/v1` permission gives access to retrieve and send data from and to the API anywhere in the extension.
* `browser_action` contains "default\_icon" and "default\_popup" which related with top bar icon and HTML file
* `content_scripts`this is an important part which it contains scripts which injected into websites  
  - `matches: [*://*/*]` tells the browser tp inject the scripts to any protocol [http, https,...] and any domain.
* - `css` field contains CSS style sheets to be injected
* - `js` field contains JavaScript files to be injected
* -`all_frames` is true which tells to inject script to all frames like "iframe" tag . it is important to make the extension work everywhere
* `background` include background scripts which manage send data to Cosmic JS and checks authorization

The JavaScript files in the js folder is where the whole functionality is resided. `myscript.js`file contains all the functions of the extension. `contentscript.js` file uses jquery and `myscript.js` to manage the extension function is matched websites. `background.js` file periodically calls the authorization function and also sends data to the Cosmic bucket.

## Conclusion

The advantage of API-first content management systems is that there is no limit as to where you can integrate your app into. Your Cosmic JS Bucket can thus power your web app, native app, browser extensions or basically anything than can consume an API. If you have any questions, please reach out to us on [Twitter](https://twitter.com/cosmic_js) or join our [Slack](https://cosmicjs.com/community) community.

[This article originally appeared on Cosmic JS](https://cosmicjs.com/articles/how-to-build-a-chrome-extension-to-save-web-content-to-cosmic-js).