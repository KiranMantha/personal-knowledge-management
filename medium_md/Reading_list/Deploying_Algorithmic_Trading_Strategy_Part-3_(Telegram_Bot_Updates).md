---
title: "Deploying Algorithmic Trading Strategy Part-3 (Telegram Bot Updates)"
url: https://medium.com/p/b22cd101a258
---

# Deploying Algorithmic Trading Strategy Part-3 (Telegram Bot Updates)

[Original](https://medium.com/p/b22cd101a258)

# Deploying Algorithmic Trading Strategy Part-3 (Telegram Bot Updates)

[![Ganesh N](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)](/@ganeshnagarvani?source=post_page---byline--b22cd101a258---------------------------------------)

[Ganesh N](/@ganeshnagarvani?source=post_page---byline--b22cd101a258---------------------------------------)

5 min read

·

May 22, 2022

--

Listen

Share

More

Press enter or click to view image in full size

![]()

My last two articles, **Deploying AlgoTrading Strategy** [**Part-1**](/@ganeshnagarvani/deploying-algorithmic-trading-strategy-part-1-68cd729eb2fe) & [**Part-2**](/@ganeshnagarvani/deploying-algorithmic-trading-strategy-part-2-logging-files-aa950b0fbba5)covered how to deploy trading strategy in python using Kite’s API and how to log trading events in a log file in real time. In this blog, we will further improve our strategy by getting **telegram updates** on our devices about trading events…

### CONTENTS

> **1. Introduction & Use of Bots in AlgoTrading**
>
> **2. Create Telegram Bot and activate it**
>
> **3. Create Chat id**
>
> **4. Send message through bot**
>
> **5. Integration of bot with our strategy**
>
> **6. Conclusion**

## **1. Introduction & Use of Bots in AlgoTrading**

Creating log files and recording events is good for analyzing the data later. But getting real time updates about our trading strategy would be even better. So in this article, I’ll be talking about how to make a **Telegram Bot and integrate it with our code** so that we can get updates on Telegram messenger.

We can get updates about trading through out the day using a bot. Like when was the trade entered , exited and at what price, etc. Below is the example of how a bot can give updates about trade

Press enter or click to view image in full size

![]()

To get these types of updates, we need to create a bot and activate it, get its bot token, get the chat id and finally integrate it with our code.

## 2. Create Telegram Bot & activate it

To create a telegram bot follow the steps :

**1.** Login **telegram app** on your device or on [***Telegram Web***](https://web.telegram.org/k/) for pc.

**2.** After login, in the search bar, type **@BotFather.** Click on the result which has blue tick.

![]()

**3.** A chat window will open…you need to click on **start**

![]()

**4.** You’ll automatically get the reply about what you need to do as shown…

Press enter or click to view image in full size

![]()

**5.** Click on **/newbot** or type **/newbot** in chat and press enter.

Press enter or click to view image in full size

![]()

**6.** Now you need to type in the **name** of your bot.

Press enter or click to view image in full size

![]()

**7.** Now type in the **username** of your bot. it should be **unique** and must end with **‘bot’**.

Press enter or click to view image in full size

![]()

**8.** After successfully creating a bot, you will get a confirmation message in which **access token** will be given. Save it somewhere as we need it in our code.

**9.** After completing this process, search the username in the search box and select your bot. Click **Start**. Now you bot is ready to send messages.

> **Note:** If you already have a bot and don’t know the access token, simply go to ***@BotFather > /start > /mybots > API Token***

## 3. Create Chat Id

Not that we created a bot, we need to specify to the bot where it should send messages. i.e. to whom it should send updates about trading events.

Let’s say you want the bot to give you updates. You need to know your chat id so that bot can send messages to you. Chat id is unique for each telegram user.

**1.** Go to the following link in your browser…remember to pass in your bot access token

[*https://api.telegram.org/bot****<bot***](https://api.telegram.org/bot{bot) ***access token>****/getUpdates*

If everything went ok, you will get something like this as result

![]()

**2.** Now send any message to your bot like *‘Hi’* and again refresh the link. You should get something like this…

Press enter or click to view image in full size

![]()

Now you can see your chat it. It’s 10 digit number. Save it as we need to use it in our code along with access token.

> **Note :** chat id is also available for groups. You can add your bot to the groups and get messages in group. But make sure your bot has permission to send message in group. You can also make it admin.

## 4. Send message through bot

Now that we know the access token and chat id, we can send messages through bot using python. There are many ways to do this using modules like telethon, telebot, etc. But we will send it using ***requests*** module. The `requests` module allows you to send HTTP requests using Python

Upon execution of above code, we will get a message

![]()

## **5.** Integration of telegram bot with our code

We can make a send\_message() function which upon call will automatically send message to the receiver about trading events.

We will add this function to our entry and exit conditions in code to get messages when it triggers the condition

Similarly we can add this function to our exit condition…

Let’s say entry and exit conditions triggered, we would get updates like this…

Press enter or click to view image in full size

![]()

So this is how we can overview the events of trading using bot in telegram.

## 6. Conclusion

* We saw the **use of bots** in AlgoTrading.
* We **created a bot** in telegram and activated it.
* We saw how to **get access token for a new bot** (or existing bot) & chat id.
* We saw how to **send messages through bot** using *requests* module.
* Finally we **integrated the bot with our code** to get timely updates of events.

> In case of any doubts and suggestions, reach out to me here…
>
> [***LinkedIn***](https://www.linkedin.com/in/ganesh-nagarvani/)[***GitHub***](https://github.com/ganigithub)[***HackerRank***](https://www.hackerrank.com/ganeshnagarvani)
>
> ***Happy Learning and Trading!!!***