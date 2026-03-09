---
title: "Deploy your static web app to a blockchain and make it a Web3.0 app in 5 minutes"
url: https://medium.com/p/79ca35c0044b
---

# Deploy your static web app to a blockchain and make it a Web3.0 app in 5 minutes

[Original](https://medium.com/p/79ca35c0044b)

# Deploy your static web app to a blockchain and make it a Web3.0 app in 5 minutes

[![Liron Navon](https://miro.medium.com/v2/resize:fill:64:64/1*Tch8vmZYcqutwbobqEI0Pw.jpeg)](https://codesight.medium.com/?source=post_page---byline--79ca35c0044b---------------------------------------)

[Liron Navon](https://codesight.medium.com/?source=post_page---byline--79ca35c0044b---------------------------------------)

4 min read

·

Oct 23, 2021

--

3

Listen

Share

More

One of the most interesting projects right now in the world of blockchain and web 3.0 is [Dfinity](https://dfinity.org/) which distributes the Internet Computer Protocol tokens (ICP). [Coin market cap described it nicely](https://coinmarketcap.com/currencies/internet-computer/).

> The Internet Computer is the world’s first blockchain that runs at web speed with unbounded capacity. It also represents the third major blockchain innovation, alongside Bitcoin and Ethereum — a blockchain computer that scales smart contract computation and data, runs them at web speed, processes and stores data efficiently, and provides powerful software frameworks to developers.

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

So how does a static app runs on a blockchain? The protocol is connecting multiple physical data centers around the world into the blockchain and runs units of processing on them called “canisters” which you can think of as containers (kind of) that run web assembly (WASM) bytecode.

Press enter or click to view image in full size

![]()

The canisters can run our website, and serve it through the internet computer, with automatic end-to-end encryption.

Press enter or click to view image in full size

![]()

All of this is very nice, but the official language to code for ICP is [Motoko](https://sdk.dfinity.org/docs/language-guide/motoko.html) and the other official language is [Rust](https://sdk.dfinity.org/docs/rust-guide/rust-intro.html) although you technically can use any language that can compile into web assembly.

So how can we deploy a simple HTML5 app? a project named [Fleek](https://fleek.co/) that is built on the ICP is meant to solve that for us, it is basically a version of [Netlfy](https://www.netlify.com/) that is aimed at running only on Web3.0, it also provides more features than just static site hosting, but we are only going to focus on the hosting part here.

Press enter or click to view image in full size

![]()

The first step is to have a project with some static web app, fleek can integrate into GitHub and build the project automatically for you, for example, you might have a React or Vue app, or simply a few HTML files that need to be served.

### Deploying to fleek

It’s very straightforward, simply go to [https://fleek.co](https://fleek.co/), and sign in.  
After signing in you will be redirected to <https://app.fleek.co/> where you can click `add new site`there you can link your GitHub and choose the repository to deploy.

The location step will ask you to choose where to host the project, we are gonna go for ICP, [you can learn more about IPFS here](https://ipfs.io/), but it’s outside the scope of this post.

Press enter or click to view image in full size

![]()

The last step is the deployment and build settings, choose the branch to deploy, the framework is optional, the runtime can be `node:lts` (long-term support) unless you look for something specific, if you have a build command you can add it and the directory for your static files, for a [React CRA project](https://reactjs.org/docs/create-a-new-react-app.html) it would be `dist`.

Press enter or click to view image in full size

![]()

After the deployment, you will meet this page where you get a link to the deployed website.

Press enter or click to view image in full size

![]()

I don’t like my website being called dry-tooth, that’s just a random name given by fleek, we can assign a custom domain, but I don’t have any domain for this site right now, so let’s give it a nicer name through the settings.

Press enter or click to view image in full size

![]()

### Conclusion

We can now easily deploy static apps to the internet computer, fleek has other features that you can explore like IPFS file storage and integrations with ICP.

Please clap and follow as I will publish content every couple of weeks, I truly appreciate every follower, clapper, and commenter 🙂.