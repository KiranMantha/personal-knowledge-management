---
title: "Sharing the UI router between AngularJS and Angular 6"
url: https://medium.com/p/84f6370ec557
---

# Sharing the UI router between AngularJS and Angular 6

[Original](https://medium.com/p/84f6370ec557)

Press enter or click to view image in full size

![]()

# Sharing the UI router between AngularJS and Angular 6

[![Roelof Jan Elsinga](https://miro.medium.com/v2/resize:fill:64:64/1*W_mTQctyX4GxKtC50ltCJQ.png)](https://medium.com/@roelofjanelsinga?source=post_page---byline--84f6370ec557---------------------------------------)

[Roelof Jan Elsinga](https://medium.com/@roelofjanelsinga?source=post_page---byline--84f6370ec557---------------------------------------)

4 min read

·

Jul 22, 2018

--

3

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D84f6370ec557&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fsharing-the-ui-router-between-angularjs-and-angular-6-84f6370ec557&source=---header_actions--84f6370ec557---------------------post_audio_button------------------)

Share

In some of my previous posts, [“AngularJS + Angular (v6) hybrid (finally!)”](https://medium.com/@roelofjanelsinga/angularjs-angular-v6-hybrid-finally-97ac37087de1) and [“Sharing state between AngularJS and Angular v6 with Redux”](/sharing-state-between-angularjs-and-angular-v6-with-redux-75e3abe7f4f3), I’ve documented the process of making a hybrid AngularJS/Angular application.

So far I’ve explained how to set up the Angular application to be able to display both AngularJS and Angular content (from now on I’ll use Angular to refer to Angular 6 and AngularJS to refer to version v1.x). As I’ve progressed a lot in converting the application, I’ve come to the point where I start to convert entire pages to Angular. For this to work you can downgrade the entire page to an AngularJS directive and component and inject it into the AngularJS UI Router, or you can use a wonderful package I’ve found. Let’s use that package!

## Angular UI hybrid router

In my AngularJS application, I’m using the UI Router instead of the “normal” Angular Router. The sole reason for this is that the UI Router gives me the option to work with named routes, instead of just URL’s. Let’s get started with the process. First, install the package using NPM or Yarn:

```
yarn add @uirouter/angular-hybrid
```

or

```
npm install @uirouter/angular-hybird --save
```

Now in your AppModule, import this module:

There you go, all done! Well… almost! You can refer to any Angular component in your AngularJS UI routing after you’ve followed the setup steps in the section below.

## Steps to take in your AngularJS application

Follow the steps described on [the packages’ GitHub page](https://github.com/ui-router/angular-hybrid#getting-started) to make a small adjustment to your AngularJS installation. This will make sure that AngularJS understands what you’re trying to do. You can get more information about the setup of this package [on their GitHub page](https://github.com/ui-router/angular-hybrid). There is very important information on there to avoid certain errors and making sure the AngularJS routes and Angular routes get merged, so have a look there as well. The changes for the Angular application they suggest on there I personally haven’t implemented, however, the steps I did take are documented under the section “Bootstrap the app”. Just have a look yourself if you need to implement the other steps too.

## Static routes

You may wish to start building some Angular routing alongside your AngularJS routing, this is very easy. Below I’ve created a module for all the static pages I’d like to be able to show in the application. Pay special attention to the UIRouterUpgradeModule here. It doesn’t use the forRoot(), but the forChild() this time, make sure you do the same. This provides extra routes to the already existing router you created in the AppModule.

So after this, you can simply import StaticPagesModule in your AppModule and you will be able to view the pages on the Angular routes you’ve just defined.

## Dynamic routes

We’ve just defined a few static routes, without any data to resolve, but normal apps don’t work this way most of the time. Your pages need data to be able to render a list, or a table, or anything else you may want to display. So how do we do this? Well, the UI Router provides a few ways, that are very badly documented. I only found some of these by digging through the source code, so let me help you. Pay attention to the resolve parameter in the state objects to see three different options that I have found. There may be more (or better) solutions, but I haven’t found them so far.

There are five scenarios here, the first one uses a provided string, which you can find in the providers’ section of the NgModule. The second uses the same syntax you may recognize from the AngularJS UI Router. The third option simply provides a class and the UI Router resolves this automatically. The fourth option is similar to the first option, but you can provide a value inline. The fifth option is a variation on the fourth option but shows that you can inject a resolver in a resolver. The resolver that has the injected resolver will not do anything until it’s dependency is….resolved.

I personally like the third method the best, because it keeps the routes clean. When a route doesn’t need dependency injection, your best bet is either option 1 or 2, this is up to you. As you can see, when you use option 1 and 3 you get these “magic” route and transition variables, the UI Router provides these for you. You can find the query parameters, the state you just came from, and the state you’re going to in there and can be used for things like conditional redirects for example.

There are a lot of options for you to resolve data, so find the one that works best for you and use this throughout your routing.

## Conclusion

The hybrid UI Router helps you to slowly migrate your whole application from AngularJS to Angular. If you wish, you can keep using the AngularJS UI Router and downgrade the Angular components to keep everything compatible with AngularJS, but sooner or later, you’re going to need to make the transition anyway. Start with the hybrid routes when you start to convert entire pages because otherwise, you’ll be doing twice the work in the long run. Angular UI Hybrid Router helps you to migrate from v1.x to the newer versions and keep the routing state objects almost identical, so not a lot of rewriting will be necessary.

If you have any tips or suggestions on how I can explain to better, please let me know, I’d love to help you and learn from you.