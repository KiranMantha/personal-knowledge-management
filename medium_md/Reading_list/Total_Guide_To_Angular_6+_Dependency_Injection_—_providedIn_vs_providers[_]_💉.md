---
title: "Total Guide To Angular 6+ Dependency Injection — providedIn vs providers:[ ] 💉"
url: https://medium.com/p/85b7a347b59f
---

# Total Guide To Angular 6+ Dependency Injection — providedIn vs providers:[ ] 💉

[Original](https://medium.com/p/85b7a347b59f)

Member-only story

# Total Guide To Angular 6+ Dependency Injection — providedIn vs providers:[ ] 💉

[![Tomas Trajan](https://miro.medium.com/v2/resize:fill:64:64/1*MfvHFyvZjqHRJDWlpv8n8Q.jpeg)](/?source=post_page---byline--85b7a347b59f---------------------------------------)

[Tomas Trajan](/?source=post_page---byline--85b7a347b59f---------------------------------------)

13 min read

·

Nov 6, 2018

--

27

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D85b7a347b59f&operation=register&redirect=https%3A%2F%2Ftomastrajan.medium.com%2Ftotal-guide-to-angular-6-dependency-injection-providedin-vs-providers-85b7a347b59f&source=---header_actions--85b7a347b59f---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

> 🤫 Psst! Do you think that NgRx or Redux are overkill for your needs? Looking for something simpler? Check out [@angular-extensions/model](https://www.npmjs.com/package/@angular-extensions/model) library!

Press enter or click to view image in full size

![]()

I know, I know… Angular 7 is out already but this topic is as relevant as ever! Angular 6 brought us new better `providedIn` syntax for registration of services into Angular dependency injection mechanism.

> As it turned out, this topic can evoke quite emotional responses and there is a lot of confusion across GitHub comments, Slack and Stack Overflow so let’s make this clear once and for all!

## 📖 What we’re going to learn

1. Dependency Injection (DI) recapitulation (optional😉)
2. The Old Way™ of doing DI in Angular — `providers: []`
3. The New Way™ of doing DI in Angular — `providedIn: 'root' | SomeModule`
4. Possible scenarios when using `providedIn`
5. Recommendation on how to use new syntax in your projects
6. Summary

## 💉 Dependency Injection