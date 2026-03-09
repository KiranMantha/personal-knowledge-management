---
title: "PWA: Create a “New Update Available” Notification using Service Workers"
url: https://medium.com/p/18be9168d717
---

# PWA: Create a “New Update Available” Notification using Service Workers

[Original](https://medium.com/p/18be9168d717)

# PWA: Create a “New Update Available” Notification using Service Workers

[![Simon Wicki](https://miro.medium.com/v2/resize:fill:64:64/1*YmuwlXlJ3fBPF_gSkP_18g.jpeg)](/@zwacky?source=post_page---byline--18be9168d717---------------------------------------)

[Simon Wicki](/@zwacky?source=post_page---byline--18be9168d717---------------------------------------)

3 min read

·

Jun 12, 2017

--

13

Listen

Share

More

service workers, offline-first, cache busting

Press enter or click to view image in full size

![]()

PWAs are getting more and more coverage and support. They improve the web experience and can load your app instantly with their great ability for HTTP caching (among other things, but this post only covers caching).

The thing with Offline-First is, that you cache all the resources that are needed for launching up the webapp — even your index.html!

> **Note:** No sweat! Browser implementations prevent you from deploying a version that will be cached for all eternity. For instance Chrome treats `max-age` of [1 day or 1 week or 1 year as 24 hours](https://stackoverflow.com/a/38854905/825444).

## #1 Structure

For example reasons, the 3 needed files are linked to the source of an actual PWA ([gamemusicplayer.io](https://gamemusicplayer.io)) for a clearer understanding.

* [**index.html**](https://github.com/zwacky/game-music-player/blob/master/src/index.html#L46-L69) — registers the service-worker.js and is wrapped inside the `isUpdateAvailable` Promise
* [**service-worker.js**](https://github.com/zwacky/game-music-player/blob/master/src/service-worker.js#L29-L35) — defines what files will be cached
* [**somewhere inside your webapp**](https://github.com/zwacky/game-music-player/blob/82ed69f48873aab840853f907edf63aaa4b158e2/src/pages/home/home.ts#L48-L58) — listens to `isUpdateAvailable` Promise and acts accordingly

## #2 Why can’t it just load the latest version?

When the browser loads your PWA, it doesn’t know if there is a new version available. It promptly loads the cached assets. There are different [cache strategies](https://serviceworke.rs/caching-strategies.html), depending on your use case.

* `networkOnly` – only fetch from network
* `cacheOnly` – only fetch from cache
* `fastest` – fetch from both, and respond with whichever comes first
* `networkFirst` – fetch from network, if that fails, fetch from cache
* `cacheFirst` – fetch from cache, but also fetch from network and update cache

In 99% of the cases you can decide on 2 user experiences:

1. Load the page instantly from the cache
2. Check first if network is available, otherwise load from cache as a fallback

Both options are offline-first. The 2nd option, if network is available, will therefore always deliver the most updated version, but with a delay.

If you want to give your users that ⚡️-fast page load experience and notify them when a newer version of their cached version is available, you’d need to hook into the `onupdatefound` function in your Service Worker.

## #3 How to check if your cached files have changed

We can hook into `onupdatefound` function on the registered Service Worker. Even though you can cache tons of files, the Service Worker only checks the hash of your registered **service-worker.js**. If that file has only 1 little change in it, it will be treated as a new version.

### #3.1 Register service-worker.js

The following code should be inside `<script>` tags in your **index.html**. It will add a `isUpdateAvailable` function to the global scope, so it can later be used as a Promise.

### #3.2 Check if update is available

In this example i’m using [Ionic 3](http://ionicframework.com/) to easily display a toast that will tell the user that there has been an update — in case of an update.

## #4 Caveats

Problems can arise when you use a hosting service, that automatically adds `max-age` headers to your resources — especially your **service-worker.js**.

For instance if you host your PWA over [Firebase Hosting](https://firebase.google.com/docs/hosting/), you’ll find this configuration useful.

*(Bonus: the public folder is set to* `./platforms/browser/www/` *because* [*Ionic 3*](https://ionicframework.com/) *makes it very easy for PWAs from start to finish!)*

## #5 Summary

Service Workers aren’t as scary as they seem at first. With the appropriate safety mechanisms in place (never cache more than 24 hours) you can create a great experience for your users without having to change your domain name.

Simon Wicki is a Freelance Developer in Berlin. Worked on Web and Mobile apps at JustWatch. Fluent in Vue, Angular, React and Ionic. Passionate about Frontend, tech, web perf & non-fiction books.

**👉** [**Join me on Twitter to follow my latest updates.**](https://twitter.com/zwacky)