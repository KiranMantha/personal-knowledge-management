---
title: "Native Git Hooks: Bye Bye, Husky!"
url: https://medium.com/p/e50e04030c8a
---

# Native Git Hooks: Bye Bye, Husky!

[Original](https://medium.com/p/e50e04030c8a)

Member-only story

# Native Git Hooks: Bye Bye, Husky!

[![Rufat Khaslarov](https://miro.medium.com/v2/resize:fill:64:64/1*bJumFqkskTiCUkfgQz4TjA.jpeg)](https://rufat-khaslarov.medium.com/?source=post_page---byline--e50e04030c8a---------------------------------------)

[Rufat Khaslarov](https://rufat-khaslarov.medium.com/?source=post_page---byline--e50e04030c8a---------------------------------------)

3 min read

·

May 8, 2024

--

16

Listen

Share

More

Press enter or click to view image in full size

![]()

Husky, a widely-used NPM package, has become the go-to choice for developers looking to integrate Git hooks into their projects. Boasting an impressive 10 million weekly downloads, showing widespread adoption in the developer community. Husky makes it easy to manage Git hooks in projects, making setup and maintenance effortless. But what if I told you there’s a simpler, more native alternative?

Let’s explore Git’s hooks and why they might just be the solution you never knew you needed.

### Diving into the code.

When diving into the husky's code, we'll encounter fascinating lines that are worth exploring.

Press enter or click to view image in full size

![]()

Especially, this one:

```
let { status: s, stderr: e } = c.spawnSync('git', ['config', 'core.hooksPath', `${d}/_`])
```

You may have noticed that it performs a git command to configure and update "core.hooksPath". It's quite unusual, isn't it?

By googling it, you will encounter the link to official git documentation <https://git-scm.com/docs/githooks>. Here you will find the following information:

> Hooks are programs you can place in a hooks directory to trigger actions at certain points in git’s execution. Hooks that don’t have the executable bit set are ignored.
>
> By default the hooks directory is `$GIT_DIR/hooks`, but that can be changed via the `core.hooksPath` configuration variable.

### Guess what?

It seems that Husky is using git native hooks internally. Why can’t we do that on our own and remove it completely?

Let’s first create a folder for git hooks, let’s imagine *.hooks* in our repository. Please add the *pre-commit* file and grant it execution permission with *chmod +x.*

```
#!/bin/sh  
echo "pre-commit hook run"
```

Now, let's open the *package.json* file and add the following NPM script:

```
...  
"start": "node index.js",  
"prepare": "git config core.hooksPath .hooks",  
...
```

You may need to run *npm install* to run “prepare” script.

And that’s it.

[## Every Software Engineer Must Know This: Separation of Concerns

### Understand the importance of SoC, balance Coupling and Cohesion!

javascript.plainenglish.io](/every-software-engineer-must-know-this-separation-of-concerns-7652fa9f63a5?source=post_page-----e50e04030c8a---------------------------------------)

Using native Git hooks in your repository ensures a consistent and easily accessible setup for all contributors, without the need for extra packages.

Instead of using Husky, consider using Git's native hooks now ♥️

[## Running “npm install everything”: From Joke To Apology

### NPM package manager received criticism a few months ago, which sparked discussions about how dependencies should be…

javascript.plainenglish.io](/running-npm-install-everything-from-joke-to-apology-4436d77dbf8a?source=post_page-----e50e04030c8a---------------------------------------)

[## Enforcing Git Branch Naming Convention with Git Hooks and Simple Bash Script

### Any team will eventually create internal standards or development guidelines for consistent daily operations. It might…

javascript.plainenglish.io](/enforcing-git-branch-naming-convention-with-husky-and-simple-bash-script-73e7aa83b98f?source=post_page-----e50e04030c8a---------------------------------------)

## In Plain English 🚀

*Thank you for being a part of the* [***In Plain English***](https://plainenglish.io) *community! Before you go:*

* Be sure to **clap** and **follow** the writer ️👏**️️**
* Follow us: [**X**](https://twitter.com/inPlainEngHQ) **|** [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) **|** [**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw) **|** [**Discord**](https://discord.gg/in-plain-english-709094664682340443) **|** [**Newsletter**](https://newsletter.plainenglish.io/)
* Visit our other platforms: [**Stackademic**](https://stackademic.com/) **|** [**CoFeed**](https://cofeed.app/) **|** [**Venture**](https://venturemagazine.net/) **|** [**Cubed**](https://blog.cubed.run)
* More content at [**PlainEnglish.io**](https://plainenglish.io)