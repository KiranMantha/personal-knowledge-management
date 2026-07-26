---
title: "JavaScript Fundamentals: Mastering Objects"
url: https://medium.com/p/7936db8156e0
---

# JavaScript Fundamentals: Mastering Objects

[Original](https://medium.com/p/7936db8156e0)

Member-only story

# JavaScript Fundamentals: Mastering Objects

[![Timothy Robards](https://miro.medium.com/v2/resize:fill:64:64/1*zuWDE_3Lm2iHL26T1aesMg@2x.jpeg)](https://timothyrobards.medium.com/?source=post_page---byline--7936db8156e0---------------------------------------)

[Timothy Robards](https://timothyrobards.medium.com/?source=post_page---byline--7936db8156e0---------------------------------------)

5 min read

·

Apr 15, 2019

--

5

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D7936db8156e0&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fjavascript-fundamentals-mastering-objects-7936db8156e0&source=---header_actions--7936db8156e0---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

*Objects* in JavaScript are used to store collections of data in the format of “key: value” pairs. Contained within an object we can have any number of variables and/or functions which are then referred to as object properties and methods.

🤓 *Want to stay up to date with web dev?*  
🚀 *Want the latest news delivered right to your inbox?  
🎉 Join a growing community of designers & developers!*

**Subscribe to my newsletter here →** [**https://easeout.eo.page**](https://easeout.eo.page/)

## Creating an Object

Let’s work with an example! To initialize a variable **car** as an object**,** we use curly braces **{}**:

```
var car = {};
```

We now have an empty object which can be accessed via the Developer Tools console, by simply typing our variable name:

```
car// {} [object]
```

An empty object isn’t all that useful, so lets update it with some data:

```
var car = {  
  name: 'Tesla',  
  model: 'Model 3',  
  weight: 1700,  
  extras: ['heated seats', 'wood decor', 'tinted glass'],  
  details: function() {  
    alert('This ' + this.name + ' is a ' + this.model + ' it weighs ' + this.weight + 'kg and includes the following extras: ' + this.extras[0] + ', ' +…
```