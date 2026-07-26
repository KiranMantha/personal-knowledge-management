---
title: "Step by step: Building and publishing an NPM Typescript package."
url: https://medium.com/p/44fe7164964c
---

# Step by step: Building and publishing an NPM Typescript package.

[Original](https://medium.com/p/44fe7164964c)

Member-only story

# Step by step: Building and publishing an NPM Typescript package.

[![C-J Kihl](https://miro.medium.com/v2/resize:fill:64:64/1*lwDBV2EY5NGrBYNjDgqO-g.jpeg)](https://medium.com/@carljohan.kihl?source=post_page---byline--44fe7164964c---------------------------------------)

[C-J Kihl](https://medium.com/@carljohan.kihl?source=post_page---byline--44fe7164964c---------------------------------------)

11 min read

·

May 30, 2018

--

41

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D44fe7164964c&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fstep-by-step-building-and-publishing-an-npm-typescript-package-44fe7164964c&source=---header_actions--44fe7164964c---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

## Introduction

In this guide, we will build a reusable module in Typescript and publish it as a **Node.js** package. I’ve seen it being done in many different ways so I want to show you how you can use the best practices and tools out there to create your own package, step by step using **Typescript**, **Tslint**, **Prettier,** and **Jest.**

This is what we are going to build:  
<https://www.npmjs.com/package/my-awesome-greeter>  
<https://github.com/cjkihl/my-awesome-greeter>

## What is NPM?

Npm is the package manager for Javascript and the world's biggest library of reusable software code. It’s also a great build-tool itself as I will show later on.

## Why Typescript?

As a superset to Javascript, Typescript provides optional typing and deep IntelliSense. When it comes to package development, this is my personal opinion:

> **I believe that all packages should be built in Typescript**