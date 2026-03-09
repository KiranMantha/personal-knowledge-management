---
title: "Google API authentication with OAuth 2 —on the example of gmail"
url: https://medium.com/p/a103c897fd98
---

# Google API authentication with OAuth 2 —on the example of gmail

[Original](https://medium.com/p/a103c897fd98)

# Google API authentication with OAuth 2 —on the example of gmail

[![Paweł Świderski](https://miro.medium.com/v2/resize:fill:64:64/1*s1h8mPuOdLYxc9mc328T7A.png)](/?source=post_page---byline--a103c897fd98---------------------------------------)

[Paweł Świderski](/?source=post_page---byline--a103c897fd98---------------------------------------)

5 min read

·

Mar 18, 2018

--

35

Listen

Share

More

Press enter or click to view image in full size

![]()

The article presents how to authenticate and authorize an access to Gmail API from the application.

Google gives us an access to lots of welfare with the Google API. The API enable to use Google services from our own applications. For example our apps can exchange data with google drive, use Gmail, calendar, Blogger, ask for analytical data from YouTube. Besides that there are lots of google cloud services that are available to use. Each API has its own big free quota which allows to reliably rely on Google services. Full list of APIs is available [here](https://developers.google.com/apis-explorer/#p/).

Let’s start to use Google API. Log into your google account and go through the steps.

## Create project

First you need to create a project in Google Developers Console.

Go to:

```
https://console.developers.google.com/
```

Then you see the action bar on the top of the page:

Press enter or click to view image in full size

![]()

Click on the list of projects:

Press enter or click to view image in full size

![]()

and select “**+**” to add a new one.

Press enter or click to view image in full size

![]()

Give your project a name. Let’s name it “**GmailApiTest**”.

Press enter or click to view image in full size

![]()

**Create** project and go to **Credentials > OAuth consent screen**. Put the name of the product in the field “**Product name shown to users**”. It is possible to use the same name — “GmailApiTest”. It will be displayed on the list of apps that have granted permissions to use google account.

Press enter or click to view image in full size

![]()

## Generate credentials

**Credentials > credentials** page allows to generate a key .

Press enter or click to view image in full size

![]()

Choose **OAuth client ID**

Press enter or click to view image in full size

![]()

Choose application type. I prefer to select “**Other**”. Put the name for the client.

Press enter or click to view image in full size

![]()

If you choose different option, for example, *Web application* you have to insert one of the *Authorized redirect URIs*. For the purpose of this tutorial I suggest to put there

```
http://localhost
```

Press enter or click to view image in full size

![]()

Save your OAuth client. Thanks to that you receive **clientID** and **clientSecret**.

Press enter or click to view image in full size

![]()

## Get authorization tokens

There are 2 steps to get authorization tokens for your project. First is a request for an authorization **code** and then there is the code confirmation. After the process you will have an **access\_token** and **refresh\_token**. You need both of them if your app is offline app, in other case access\_token is enough. Refresh\_token is useful to renew access\_token after it expires.

Full documentation of this process is available in the [google developers website](https://developers.google.com/identity/protocols/OpenIDConnect#setredirecturi) but you fortunately don’t need it with my tutorial.

### Get code for permissions request

Use your browser to request permissions for your app. You need to call

```
https://accounts.google.com/o/oauth2/v2/auth
```

with GET parameters.

* **client\_id**
* **response\_type**, put here **code**, it is the simplest way to authenticate by requesting the **code**
* **scope** — each API has its own scope. E.g. Gmail API has scope to send messages, compose messages etc. Choose [one of the scopes you need for Gmail](https://developers.google.com/gmail/api/auth/scopes). We’ll choose

```
https://www.googleapis.com/auth/gmail.send
```

* **redirect\_uri** — put here:

```
http://localhost
```

* **access\_type** — use it with value *offline*,only if you need **refresh\_token.**

Our request URI looks like that:

```
https://accounts.google.com/o/oauth2/v2/auth?client_id=187637922392-nm8r2q89o9gub1ftmuos32coutiumkt1.apps.googleusercontent.com&response_type=code&scope=https://www.googleapis.com/auth/gmail.send&redirect_uri=http://localhost&access_type=offline
```

After the call, browser shows question about granting permissions to the app:

![]()

Turn off any service that is running on your computer that is available on port 80 with URL [*http://localhost*.](http://localhost.) Click **“Allow”** and then we will be redirected into *localhost*.

Redirected URI looks as follows:

```
http://localhost/?code=4/AACbpkMFarNdMwz1qVPV0mWcnfjSt0zMcNcUogSMgr2lcZU2G7qjf7B-f1lmTkhRpfgXFBwxzd9ad3vRD1Oymgk#
```

We can extract **code** from this. It is:

```
4/AACbpkMFarNdMwz1qVPV0mWcnfjSt0zMcNcUogSMgr2lcZU2G7qjf7B-f1lmTkhRpfgXFBwxzd9ad3vRD1Oymgk#
```

### Confirm permissions request

We need to POST **code** with some other parameters on:

```
https://www.googleapis.com/oauth2/v4/token
```

Parameters that we need:

* **code**
* **client\_id**
* **client\_secret**
* **grant\_type** — use *authorization\_code*
* **redirect\_uri** — use[*http://localhost*](http://localhost)

Let’s use rest client of your choice e.g. SoapUI.

Headers:

```
Content-Type: application/x-www-form-urlencoded
```

Body:

```
code=4/AACbpkMFarNdMwz1qVPV0mWcnfjSt0zMcNcUogSMgr2lcZU2G7qjf7B-f1lmTkhRpfgXFBwxzd9ad3vRD1Oymgk#&client_id=187637922392-nm8r2q89o9gub1ftmuos32coutiumkt1.apps.googleusercontent.com&client_secret=aspzni4WpLp3pv_Ixszax_pQ&grant_type=authorization_code&redirect_uri=http://localhost
```

The answer gives us **access\_token** and **refresh\_token**:

```
{  
 "access_token": "ya29.GluCBcWz5DTsbBTAGvNV2m0eJXSn4rBpXq7wNKw8Ryqp52JAckB9iBvvTnrUIzTSiDv1oQE6NTrDytoYYEhCngBPwyyhhfJJXYBj574rZ5MwnIXZhUbcWrkF8PtD",  
 "token_type": "Bearer",  
 "expires_in": 3600,  
 "refresh_token": "1/qK6SZ1UoFciRvVdY6B7u0oZRXiIOvMdhaaB1myjEoV8"  
}
```

As you can see in the picture, application “GmailApiTest” has access to sending emails through Gmail.

Press enter or click to view image in full size

![]()

## Enable API

In the end enable API you need. It is not enough to have a permission to some service. API need to be enabled.

Do it by clicking “**Enable**” for specific API. In case of Gmail, go to <https://console.developers.google.com/apis/library/gmail.googleapis.com/?project=gmailapitest-198410>

Press enter or click to view image in full size

![]()

## Summary

I hope you’ve learned how to authenticate to Google APIs and you will be able to use the power of Google Services.

After this tutorial you can [sending emails by Gmail API from your Java app](https://medium.com/@pablo127/sending-emails-from-java-app-with-gmail-api-eac23ca0eb5).

If you have any questions or comments. Please let me know. Constructive feedback is appreciated.