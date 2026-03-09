---
title: "How I Am Using a Lifetime 100% Free Server"
url: https://medium.com/p/bd241e3a347a
---

# How I Am Using a Lifetime 100% Free Server

[Original](https://medium.com/p/bd241e3a347a)

Member-only story

# How I Am Using a Lifetime 100% Free Server

## Get a server with 24 GB RAM + 4 CPU + 200 GB Storage + Always Free

[![Harendra](https://miro.medium.com/v2/resize:fill:64:64/1*uTEzlRvlNBr3ralJoTQkmg.jpeg)](/@harendra21?source=post_page---byline--bd241e3a347a---------------------------------------)

[Harendra](/@harendra21?source=post_page---byline--bd241e3a347a---------------------------------------)

5 min read

·

Oct 26, 2024

--

180

Listen

Share

More

[***Read here for free***](/@harendra21/how-i-am-using-a-lifetime-100-free-server-bd241e3a347a?sk=8528079e21d46c9655eba001993ed11e)

As developers, we need to run and host the backends on cloud services. Many BaaS (backend as a service) are available, but they have limitations in functionality, features, or duration of free use. If you are tired of searching for a free and reliable server, I think you are at the right place.

What if I say I have been using the Linux-based server for free for more than 4–5 years? Yes, you heard it right. I am using this Linux server with Ubuntu 20 installed, 24 GB RAM, 4 CPUs, and 200 GB storage for a lifetime free.

I have used **AWS** and **Google Cloud Platform** for one year, and after that, their free services expired. AWS is providing one free server with 1 GB RAM and 30 GB Storage for one year; meanwhile, Google Cloud Platform provides a $300 credit for one year, which is enough to create an 8 GB server or more. But the problem is that they both provide it only for one year.

Press enter or click to view image in full size

![How I Am Using a Lifetime 100% Free Server]()

Approximately four years ago, I was looking for some free cloud services; hence, my AWS and GCP trial expired. During the search, I found that Oracle Cloud provides lifetime free servers without any restrictions. So, I signed up for Oracle Cloud and started using it, and since today, which is approximately four to five years ago, I have been using it for free.

Press enter or click to view image in full size

![]()

## Here, I came up with the full guide to getting started with Oracle Cloud

The first thing we need to do is create the Oracle Cloud account; for that, you require your working email and credit card. It will take a few minutes, and they will charge you $1 or $2 for payment and credit card verification. Don’t worry; this amount is refundable and will be credited back after a couple of days.

* Navigate to [**https://signup.oraclecloud.com/**](https://signup.oraclecloud.com/)
* **Fill out the signup form correctly.**
* **Verify your email**
* **Provide the valid details along with payment details (You will not be charged) and finish the signup process.**

Press enter or click to view image in full size

![]()

## Create free instance

Once you complete the signup process, you have to log into your Oracle Cloud account using the recently created identity. Once you successfully log in, you will see the Oracle Dashboard, You have to choose compute > instances.

Press enter or click to view image in full size

![]()

Then, click on the Create instance button.

Press enter or click to view image in full size

![]()

On the next screen, you have to choose the always free tagged resources only. For example, if you want to use Ubuntu, then you have to edit the image and shape and select the Ubuntu image tagged always free —

Press enter or click to view image in full size

![]()

In the next step, download the public and private keys that are required to connect with your server via SSH.

Then attach the boot volume up to 200GB and click on the create button.

It will take some time, and you will be ready to use your always-free instance.

> Note: For AMD-based architecture, you will get 1 GB RAM with 1 CPU, and for ARM-based architecture, you will get 24 GB RAM with 4 CPUS

Press enter or click to view image in full size

![]()

## SSH into your Server

To manage a newly created instance, you need to log in to it using SSH (Secure Shel); this will provide you the command line access to your server. You can log in to your server via the keys that you have downloaded (server.key) in previous steps while creating the new instance. You may be required to change the permission of the key file one, you can use the following commands—

```
chmod 600 path/to/server.key // to change the permission  
ssh -i path/to/server.key ubuntu@your-public-ip
```

It will take a few seconds. After that, you will be able to log in to your server, and it will show a screen like the one below —

Press enter or click to view image in full size

![]()

Also Read —

[## The Best Open-Source Alternatives to Your Favorite Productivity Tools

### Open-source alternatives to Google Drive, Notion, Figma, Zoom, and Photoshop

medium.com](/with-code-example/the-best-open-source-alternatives-to-your-favorite-productivity-tools-2713985809bc?source=post_page-----bd241e3a347a---------------------------------------)

To help you create and set up the free Oracle server, I have found a well-explained video on YouTube. This will show you a step-to-step guide to set up your server, I hope this will help you a lot.

Based on the response on this story I can conclude that you have 50–50 chances of working this trick. Many developers are taking advantage of this service and may of them are not able to complete it. So you can give it a try.

Thank you for taking the time to read this article! If you found it helpful, a clap 👏 would be greatly appreciated — it **motivates** me to continue writing more. If you want to learn more about open-source and full-stack development, follow meon [***Twitter*** (X)](https://x.com/harendraverma2) and [***Medium***](/@harendra21).