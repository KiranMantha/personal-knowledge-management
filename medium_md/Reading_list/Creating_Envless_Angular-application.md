---
title: "Creating Envless Angular-application"
url: https://medium.com/p/0ce3c2ecaddd
---

# Creating Envless Angular-application

[Original](https://medium.com/p/0ce3c2ecaddd)

Press enter or click to view image in full size

![]()

Member-only story

# Creating Envless Angular-application

## Ways to move from hard-coded code for each environment to a universal build that can be used anywhere

[![Maksim Dolgikh](https://miro.medium.com/v2/resize:fill:64:64/1*9933gAkwEAVfvxqGXBA7vQ.jpeg)](https://medium.com/@maks-dolgikh?source=post_page---byline--0ce3c2ecaddd---------------------------------------)

[Maksim Dolgikh](https://medium.com/@maks-dolgikh?source=post_page---byline--0ce3c2ecaddd---------------------------------------)

9 min read

·

Aug 9, 2024

--

4

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D0ce3c2ecaddd&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fcreating-envless-angular-application-0ce3c2ecaddd&source=---header_actions--0ce3c2ecaddd---------------------post_audio_button------------------)

Share

## Introduction

As you all know, Angular has its own tools for building an application for different environments

[## Angular

### The web development framework for building modern apps.

angular.dev](https://angular.dev/tools/cli/environments?source=post_page-----0ce3c2ecaddd---------------------------------------#angular-cli-configurations)

This is accomplished by creating and using the `environment.<env>.ts` file for the appropriate environment in the build. These allow you to switch between settings for:

* Development (`environment.ts`)
* Testing (`environment.test.ts`)
* Production (`environment.prod.ts`)

### The main tasks of environment.ts files are:

* **API settings.** Each file can contain different URLs for API servers depending on the environment.
* **Optimization.** The production file disables debugging features and enables optimization to improve performance.
* **Environment variables.** Easily manage environment variables such as API keys…