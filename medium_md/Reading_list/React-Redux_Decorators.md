---
title: "React-Redux Decorators"
url: https://medium.com/p/8b38f3b9ef2f
---

# React-Redux Decorators

[Original](https://medium.com/p/8b38f3b9ef2f)

# React-Redux Decorators

[![Alex Bazhenov](https://miro.medium.com/v2/resize:fill:64:64/1*R-XgmgAWms00xhyW7SfZ1A.jpeg)](/@Abazhenov?source=post_page---byline--8b38f3b9ef2f---------------------------------------)

[Alex Bazhenov](/@Abazhenov?source=post_page---byline--8b38f3b9ef2f---------------------------------------)

1 min read

·

Jan 7, 2018

--

4

Listen

Share

More

Did you know that you can use the `connect` method in `react-redux` as a decorator? Using a decorator allows us to go from code like this:

To code like this:

This approach gives us the advantage of immediately seeing that we are exporting a connected component when we look at the component definition, and lets us export the component on the line where we declare it. We can take this idea one step further if we define our own `mapStateToProps` and `mapDispatchToProps` decorators.

Using these decorators over the non-decorator method affords us an additional advantage. We do not have to pass in `() => ({})` as the first argument to `connect` when we only want to use `mapDispatchToProps`, and we do not have to pass in

We can also chain our decorators, so our initial example would become:

Easier to read, no redundant empty functions, and less lines of code. Getting this to work in current javascript environments is quite simple. simply install `babel-plugin-transform-decorators` and include it in your `.babelrc` file. As always i’ve [published an npm package](https://github.com/Abazhenov/react-redux-decorate) if you don’t feel like implementing these decorators yourself.

Happy Decorating!