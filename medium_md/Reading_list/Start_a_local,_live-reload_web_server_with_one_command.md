---
title: "Start a local, live-reload web server with one command"
url: https://medium.com/p/72f99bc6e855
---

# Start a local, live-reload web server with one command

[Original](https://medium.com/p/72f99bc6e855)

Member-only story

# Start a local, live-reload web server with one command

## Honestly, this is all you need to start developing and test across multiple browsers and devices!

[![Scott Vinkle](https://miro.medium.com/v2/resize:fill:64:64/2*xc4MU4FHwc_iigu3_wy47w.jpeg)](/@svinkle?source=post_page---byline--72f99bc6e855---------------------------------------)

[Scott Vinkle](/@svinkle?source=post_page---byline--72f99bc6e855---------------------------------------)

5 min read

·

Nov 7, 2017

--

16

Listen

Share

More

Press enter or click to view image in full size

![]()

As developers, we often require a local web server to test something we’re working on and often don’t have time to set up a complex system for a quick test. We need something ready-to-go and easy to use to check our latest code changes, now!

> Here’s a quick tip on starting a local web server with one command!

The server we’ll use features live-reload, which means when you make a change to your code, your browser will refresh automatically!

Oh, you also need to test on mobile, tablet, and/or your gaming console? No problem! Connect each of your devices to your local server and watch as they all refresh, hyper-link *and* scroll together in **real-time**! 😱

Let’s go! 🚀

## First, let’s install some stuff

### Node.js and npm

Like most things these days, make sure you have Node.js and `npm` installed. You can do this by downloading the official installer for your platform from [NodeJS.org](https://nodejs.org/en/download/).

After Node.js is installed, open your Terminal application to verify `npm` is installed and ready to go by running the following command:

```
npm -v
```

This should return the current version number.

Press enter or click to view image in full size

![]()

### Browsersync

Next let’s use `npm` to install our server application, [Browsersync](https://browsersync.io/)! This is the app that does all the heavy lifting like serving your files, reloading all the connected browsers on file save, and more!

Type and run the following command:

```
npm install -g browser-sync
```

This will install `browser-sync` “globally” so that you can use it to serve and test your work in any directory on your computer.

Now that we have everything installed, let’s set up the command to start the server in your Terminal!

## Creating the command

One of the coolest things about using the Terminal and working with the command line interface is that you can create your own custom commands which then runs a bunch of other commands for you!

We’re going to do just this in order to run our server with one simple command: `serve`.

### Open the shell config

A custom command is called an “alias” which are created in your Terminal shell configuration file.

By default, the **macOS** Terminal runs the [Bash](https://www.gnu.org/software/bash/) shell. From your home directory (`~/`) open either the `.bash_profile` file or, if that doesn’t exist, the `.bashrc` file. In case that one also doesn’t exist, just create it and we’ll make the changes there.

My text editor of choice is [Atom](https://atom.io/), so if you have this installed, run the following in your Terminal to edit you shell configuration file:

```
atom ~/.bashrc
```

Scroll to the end of this file as we’ll be including our additions at the very end.

### Get your local IP address

The first line to add will be used to get the current local IP address of your computer. This will come in handy if and when you’re testing something elsewhere other than your home network.

Add this to your file:

```
export LOCAL_IP=`ipconfig getifaddr en0`
```

This line creates a new variable called `$LOCAL_IP` and stores your local network IP address. Why do we need this information? You’ll soon find out!

### Setup the serve command alias

The other line we need to add is the actual command alias which will start the Browsersync server.

Add this line to your shell configuration file:

```
alias serve="browser-sync start -s -f . --no-notify --host $LOCAL_IP --port 9000"
```

Let’s breakdown what’s in this line.

* The first part, `alias`, tells our shell environment that we want to create a new, custom command.
* Whatever comes after `alias` is the command that we type. In this case, our command will be, “`serve`.” The string that’s set to this command is what *actually* gets run in the background.
* The `browser-sync start` command is what starts up the Browsersync server.
* The `-s` option runs the *local* server.
* The `-f` option tell Browsersync which files to watch. In this case we use the dot `.` character to denote the current Terminal directory.
* Normally when connecting to a Browsersync server there’s a little message to signify a connection. We use the `--no-verify` option to remove this feature.
* The `--host` option sets the IP address of the host computer. This is where we use the `$LOCAL_IP` variable we created earlier.
* Finally, the `--port` option denotes which port our server should run on.

**Note:** Checkout all the other [Browsersync command line options](https://browsersync.io/docs/command-line) available to customize your server!

Press enter or click to view image in full size

![]()

Now, let’s save the file and try out the new `serve` command!

## Run the command

In your Terminal, change directories to somewhere with project files that you’re working on. For example, I’m checking out a change I’ve made on [The A11Y Project](http://a11yproject.com/) site, and I want to test it locally.

Since my copy of the site is in `~/Sites/a11yproject.com/_site`, I’d issue the following command to change to this directory:

```
cd ~/Sites/a11yproject.com/_site
```

In this directory there’s an `index.html` file with content and style sheets linked from a subdirectory, along with all the other files to make up the site.

I’m going to run the serve command from here:

```
serve
```

Your Terminal should output information like the following, as well as open your default browser and load the `index.html` page automatically:

Press enter or click to view image in full size

![]()

As displayed in the Terminal output, the “Local:” IP value is that of your own computer, `http://localhost:9000`. However, the “External:” IP is what’s interesting here. This is yet another benefit and use of the `$LOCAL_IP` variable in the shell configuration file.

> The `$LOCAL_IP` variable adds a quick note of your current, local network IP address when starting up your server.

Use this value when you want to test on a mobile, tablet, or other computing device with a browser!

Checkout the `serve` command in action! 👇

![]()

I hope this tip has been helpful in getting a local, live-reload server up and running quickly!

Are there any other Browsersync configurations you’d recommend? Are you using a different method for launching a local server for quick tests? Let me know in the comments! 🙌

Happy hacking! 💻😄💖