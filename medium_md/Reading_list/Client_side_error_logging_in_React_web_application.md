---
title: "Client side error logging in React web application"
url: https://medium.com/p/b70d4b072400
---

# Client side error logging in React web application

[Original](https://medium.com/p/b70d4b072400)

# Client-side error logging in React web application

[![Sadhna Rana](https://miro.medium.com/v2/resize:fill:64:64/2*A-ZJFWj7fegNTwz-qX6jgQ.jpeg)](/@ranasadhna90?source=post_page---byline--b70d4b072400---------------------------------------)

[Sadhna Rana](/@ranasadhna90?source=post_page---byline--b70d4b072400---------------------------------------)

4 min read

·

Jan 15, 2020

--

2

Listen

Share

More

Error logging makes developer’s life bit easy ;)

Press enter or click to view image in full size

![]()

If we are not logging errors in our web application then what will happen if users faced some errors while using any website feature? These errors will be kept in their own browsers. Isn’t it hard to identify the issue and it also cost the huge development time in order to identify these errors?

Error logging helps to identify the key reasons for the errors faced by the users in a website. It helps to keep track of the errors occurring on the website without relying on the user's intervention. Therefore, Error logging should be an imperative part of web development.

In this article, I am going to describe how we can logs the errors in our React web application by using Rollbar which is an error tracking tool.

**Step 1: Install the rollbar package**

```
npm install --save rollbar
```

**Step 2: Create a custom rollbar component to logs errors in Rollbar items.**

```
// RollbarErrorTracking.js import Rollbar from 'rollbar';export const RollbarErrorTracking = (() => {  
const RollbarObj = new Rollbar({  
accessToken: process.env.REACT_APP_ROLLBAR_ACCESS_TOKEN,  
captureUncaught: true,  
captureUnhandledRejections: true, },);const logErroInfo = (info) => {  
RollbarObj.info(info);  
};const logErrorInRollbar = (error) => {  
throw new Error(error);  
};return { logErroInfo, logErrorInRollbar };  
})();export default RollbarErrorTracking;
```

Here, I created an instance ***RollbarObj*** by using rollbar object. Now, add the required configuration of the rollbar.

```
const RollbarObj = new Rollbar({  
accessToken: process.env.REACT_APP_ROLLBAR_ACCESS_TOKEN,  
captureUncaught: true,  
captureUnhandledRejections: true, },);
```

**For instance:** Rollbar ***accessToken*** and it should be set based on the current environment whether it is for staging or production website. We can read it through the env variable. ***captureUncaught*** and ***captureUnhandledRejections*** will also help to log uncaught exceptions.

```
const logErrorInRollbar = (error) => {  
throw new Error(error);  
};
```

*throw new Error(error)* helps to log the error in Rollbar.

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

```
const logErroInfo = (info) => {  
RollbarObj.info(info);  
};
```

*RollbarObj.info()* is used to add information about the logged error in Rollbar.

We can also add some more custom logs messages in Rollbar. Check this link  
<https://docs.rollbar.com/docs/custom-log-messages#section-javascript>

**Step 3: Add these rollbar tracking methods in your API integration source code**

If you want to log the uncaught exceptions occurs in an API then you can add these methods to log error in Rollbar.

```
// import RollbarErrorTracking.js fileaxios.post(API_URL, data: postData)  
.then({ result} => {  
  // handle API response  
}).catch({error} => {   RollbarErrorTracking.logErrorInRollbar(error.response.data.message);})
```

In this way, you can add the log of any API exception in the rollbar items.

**Step 4: We can also add logs for any JS error that occurs in a React component by using error boundary.**

If you want to logs the JS errors of React components we can also track it by using Rollbar. We just need to create an ErrorBoundary component   
and we can log the error in Rollbar inside the *componentDidCatch* method.

```
// CustomErrorTracking.jsimport React from 'react';  
import RollbarErrorTracking from 'utils/Rollbar';export default function Catch(  
  component,  
  errorHandler  
) {  
  return class extends React.Component {  
    constructor(props) {  
      super(props);  
      this.state = {  
        error: undefined,  
      };  
    }static getDerivedStateFromError(error) {  
      return { error };  
    }componentDidCatch(error, info) {  
      if (errorHandler) {  
        RollbarErrorTracking.logErroInfo(info);  
        RollbarErrorTracking.logErrorInRollbar(error);  
        errorHandler(error, info);  
      }  
    }render() {  
      const { error } = this.state;  
      return component(this.props, error);  
    }  
  };  
}
```

This is the custom error tracking component to catch any js error in a React component.

```
// ErrorBoundary.js  
import React from 'react';  
import Catch from './CustomErrorTracking';export const ErrorBoundary = Catch((props, error) => {  
  const node = (error)  
    ? (  
      <div className="error-screen">  
        <h2>Something went wrong</h2>  
        <h4>{error.message}</h4>  
      </div>  
    )  
    : (<>{props.children}</>);  
  return node;  
});ErrorBoundary.propsTypes = {  
  children: React.ReactNode  
};export default ErrorBoundary;
```

This is the functional error boundary component in which we are checking if there is any js error then it will show the error message inside the web view instead of crashing the whole webpage.

Below is an example of how we can use ErrorBoundary in a React component.

```
<ErrorBoundary>  
  <MyComponent   
    items={listing}  
    userId={currentUser}  
  />  
</ErrorBoundary>
```

In this way, we can track any js errors of a React component by enclosing it inside the *ErrorBoundary* .

In the above example, if the child component *Mycomponent* is receiving any invalid value from the props like *items* or *userId* it will through Js error and we can log these errors in the Rollbar as showing in the above code of *CustomErrorTracking* component.

```
componentDidCatch(error, info) {  
      if (errorHandler) {  
        RollbarErrorTracking.logErrorInfo(info);  
        RollbarErrorTracking.logErrorInRollbar(error);  
        errorHandler(error, info);  
      }  
}
```

*RollbarErrorTracking.logErrorInfo(info)* and *RollbarErrorTracking.logErrorInRollbar(error)* will through js errors in Rollbar items.

I hope this will help you to integrate Rollbar and to capture js errors on the client-side and it is definitely going to reduce the development time to identify the issues and get worried about how and when the errors occur to a user. Definitely, gonna make the developer’s life a bit easy ;) Isn’t it ?.

Thanks for reading this article. Please share your response and some informative feedback.