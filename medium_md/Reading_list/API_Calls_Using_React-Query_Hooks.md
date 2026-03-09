---
title: "API Calls Using React-Query Hooks"
url: https://medium.com/p/abbfff16b40e
---

# API Calls Using React-Query Hooks

[Original](https://medium.com/p/abbfff16b40e)

# API Calls Using React-Query Hooks

[![Chime Princewill](https://miro.medium.com/v2/resize:fill:64:64/2*3C5pZHfv_Fuu4SaXZe2SMQ.jpeg)](https://princewillchime43.medium.com/?source=post_page---byline--abbfff16b40e---------------------------------------)

[Chime Princewill](https://princewillchime43.medium.com/?source=post_page---byline--abbfff16b40e---------------------------------------)

7 min read

·

Oct 25, 2021

--

5

Listen

Share

More

Press enter or click to view image in full size

![]()

When building an application(mobile/web) you will most likely want to get some data from an API or locally with static JSON files. For a technology like javascript and its libraries, it has an inbuilt method like Fetch and a library like Axios which helps to make API calls.

Libraries like ReactJs with their life cycle methods make it more efficient to make an API call. In some scenarios, you may want to update the state only when there is an update in the data and not always onMount or onUpdate in the components.

**Prerequisite:**

* Node and Npm installed
* Know javascript
* Know ReactJs

In this article, I will show you how I manage my requests with a library called ***React-Query;*** It comes with a lot of hooks that help me to handle requests without thinking of the following edge cases:

* Reflecting updates to data
* Performance optimization
* Updating “out of date” data in the background
* Caching
* Managing memory and garbage collection of server state and more.

I am using visual studio code for this article. So if you are with me, let’s get started.

To start a react project use this [***link***](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Client-side_JavaScript_frameworks/React_getting_started#initializing_your_app)to create a project named reactquery.

Let’s install the react-query library and Axios in the following snippet:

```
yarn add react-queryyarn -D add axioscode .
```

The above code snippet is all we need to get started. Inside the react-query project that was created above, I installed the react-query package, installed Axios into the devDependencies, and open the directory in the vscode.

Inside the src folder, let’s create the

two directories and some files as follows in the terminal:

```
cd src mkdir component viewcd component mkdir query posts
```

Let’s integrate the react-query to have access to the client in all the components like so:

![]()

In the above snippet, I assigned an instance of QueryClient to the client variable and later pass it as a prop to the provider that is wrapping all of the components, the client is made available to all the components that are wrapped.

Inside the query directory, let’s create a file named posts.js and add the following into it:

![]()

This is an async function that awaits the data that is returned from the API call. The function is exported for use. Shortly, I will show you where I will be importing the **fetchPost** function.

Inside the posts directory let’s create a component named posts.jsx and add the following into it:

![]()

In the snippet above, I imported useQuery from the react-query library and **fetchPosts** from the posts.js file. The fetchPosts is a function that handles the API call in the background while the useQuery is a hook that helps to manage the request.

useQuery needs a query key and an async function for it to manage a request. The query key can be a string or an array, the second argument is where the function that makes the request is been passed. Once you have passed all the required arguments, it returns a series of variables to use. In my case, I destructured: **data**, **isFetching**, and **isLoading** from all that was returned.

***Data*** holds the response data if the request is successful, ***isFetching*** iscalledwhenthereis an update in the data, **isLoading** works similarly to **isfetching**, except that it is called when it’s trying to get the data. while **isfetching** is called when there is an update in the data.

In the following code snippet, let’s render the returned data:

![]()

In the above snippet, I am displaying some text when data is loading, another when fetching updated data and lastly render the data to the browser. This method of rendering data is likely What you may be seeing often in people’s codebase.

For me, I like handling the data as I want, like, setting data to the state, handling more things when the request returns some data or an error. So to that, I will show you how I manage the data that comes back and more in the following:

![]()

I created a state using useState-hook, useQuery gives us a third argument that holds options to manage the request properly. Common options are OnError and OnSuccess that I used in the snippet above.

OnError returns the error that is associated with the request, and onSuccess returns the data once the request is successful. When data is returned, the data is set to the state; instead of mapping the data directly like earlier, I am now getting the data from the state.

Note: Inside the OnSuccess | onError, you can decide to handle more functions/variables.

**How to pass a query/params to a useQuery:**To pass a query to the useQuery function I will add the query/params as shown below:

![]()

Inside the Post component, I adjusted the query key and pass in an object that holds the limit of posts that will be returned. Let’s go to the posts file in the query directory and adjust it with the following:

![]()

In the above snippet, I destructured the query key from the props, remember, the query was wrapped in an array that holds the key and the data limit, the limit is inside an object, so I destructured the limit from the object in other to use it in the request.

When making an API call with useQuery, once the query fails it tries to refetch the query up till three-time before it throws an error but it can be limited using the following:

![]()

The ***retry*** specifies the number of times the request should be called, so after the initial call, if there is any error, it tries to make the request one more time. On the other hand, once there is an error, it refetches immediately. So to avoid that, I added the ***retryDelay*** to wait for three seconds before retrying the request.

useQuery tries to fetch the data on every focus on the window, so to stop that behavior I set the ***refetchOnWindowFocus*** to false.

In some cases, you may want to condition the query — something happens before the query is made. you will have to add the enabled option and set it as follows:

![]()

The condition that is passed to the enabled is a state variable, when set to false the query returns, else the query will make a call to the API.

At times, you may wish to add multiple dependencies, to do that, you will have to condition the query as shown below:

![]()

The above snippet is used whenever you want to set multiple conditions to a query, it is like an observer that observes when there is a change to any of the dependencies — just like the way dependencies are set in the useEffect dependency array.

There are some cases, where you would want to **refetch** a query when something happens; to do that, you will destructure the **refetch** method from useQuery as shown below:

![]()

The **refetch** is a method that refetches a query once it's been called in any function or event triggers.

Now that we have all implemented these, let us see what we have built in the following [***Demo***](https://res.cloudinary.com/hobbyluv07/video/upload/v1634837753/Screencast_from_21-10-2021_18_33_37_cf9fpb.webm)***.*** The source code is available [***here***](https://github.com/chibuike07/react-query-tutorial)**.**

Finally, we have gotten to the end of this article, and I hope you will start using react-query going forward to manage your API calls.

If this article was helpful to you don’t forget to hit the clap icon, share the article and follow me on my [***Medium***](https://princewillchime43.medium.com/), and [***Linkedin***](https://www.linkedin.com/in/chime-princewill-3a2b1b192/) to see more of my articles.

Kindly drop any suggestions. If you have a topic based on the JavaScript/React.js ecosystem, feel free to reach out and I’d be glad to write on it. Thanks.

[![]()](https://faun.to/bP1m5)

Join FAUN: [**Website**](https://faun.to/i9Pt9)💻**|**[**Podcast**](https://faun.dev/podcast)🎙️**|**[**Twitter**](https://twitter.com/joinfaun)🐦**|**[**Facebook**](https://www.facebook.com/faun.dev/)👥**|**[**Instagram**](https://instagram.com/fauncommunity/)📷|[**Facebook Group**](https://www.facebook.com/groups/364904580892967/)🗣️**|**[**Linkedin Group**](https://www.linkedin.com/company/faundev)💬**|** [**Slack**](https://faun.dev/chat) 📱**|**[**Cloud Native** **News**](https://thechief.io)📰**|**[**More**](https://linktr.ee/faun.dev/)**.**

**If this post was helpful, please click the clap 👏 button below a few times to show your support for the author 👇**