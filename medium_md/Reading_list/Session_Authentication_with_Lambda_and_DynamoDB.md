---
title: "Session Authentication with Lambda and DynamoDB"
url: https://medium.com/p/60355bff8a97
---

# Session Authentication with Lambda and DynamoDB

[Original](https://medium.com/p/60355bff8a97)

# Session Authentication with Lambda and DynamoDB

[![Shreyas Sreenivas](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)](/@shreyas44?source=post_page---byline--60355bff8a97---------------------------------------)

[Shreyas Sreenivas](/@shreyas44?source=post_page---byline--60355bff8a97---------------------------------------)

14 min read

·

Feb 10, 2021

--

Listen

Share

More

Press enter or click to view image in full size

![]()

In this tutorial, we create Session Authentication using AWS Lambda and DynamoDB. We go over what Session Authentication is, why we use Lambda for it, and build it from scratch. We also go over testing, packaging, and deploying the Lambda functions using the Serverless Application Model (SAM) framework.

## What is Session Authentication?

You might have already guessed it, session authentication is a type of authentication which is one of the most widely used kind and one of the easiest to implement.

### How Does It Work?

When a user enters their credentials and submits a request to login, the backend first checks if the credentials are valid and if they are, a random string is generated. This randomly generated string is our session token.

This string is then stored in the database along with some other data that is required such as the User ID. Let’s call this string a *token* because that’s what it is, a token to get access to a set of services. This token is then stored on the client-side as a Cookie which is sent on every subsequent request to the backend of the application.

The following things happen when a user sends a request to the API:

1. The request is sent to the server which contains the cookies
2. Backend parses the cookies and gets the session token
3. The session token is validated and if valid get the session data by sending a request to the database which stores the session token

This is the simplest version of session authentication we can implement.

*Note, the database can be of any kind. However, since the session info is read very often, it’s useful to store it in databases that are built to have extremely fast read speeds.*

![flowchart of the flow of requests in session authentication]()

### But Why Use Lambda for This?

You may be wondering why we need to use Lambda for session authentication when the logic to implement it is not so complex and requires minimal effort. The answer to this, like a lot of other questions today, is microservices.

For a monolithic application, using Lambda would be counter-productive as you often have a single codebase where all your logic exists. There could even be dips in performance because you’ll be sending a request to the Lambda Function every time a user sends a request.

![flowchart of multiple microservices accessing data from a database]()

But, in a modern-day application, there are often tens and hundreds or even thousands of microservices, and reimplementing the logic required to authenticate a user in each service can get quite cumbersome to write and maintain.

The most common rule followed by developers is probably DRY (**D**o not **R**epeat **Y**ourself) and that is exactly what we’re trying to achieve. With Lambda, our flowchart would like something like how it does below, where all the logic is in one place and maintenance becomes much easier. This also creates an extra layer of abstraction which could be very useful.

![Flowchart of microservices accessing data from DynamoDB via Lambda]()

***Important:*** *this doesn’t mean you should always strive towards DRY code.* [*Here’s a great talk on WET code (the opposite of DRY code)*](https://www.deconstructconf.com/2019/dan-abramov-the-wet-codebase)*.*

## What About JWTs?

If you don’t know, [JWT](https://jwt.io) stands for JSON Web Tokens. It’s another kind of authentication that has gained immense popularity and adoption in recent years.

The main advantage is that the JWT is cryptographically signed and the session data is stored in the token itself, which means the backend doesn’t have to send a request to the database every time a user sends a request, potentially leading to better performance in a lot of cases.

However, it’s not all bells and whistles with JWTs.

### Disadvantages of JWTs

1. Harder to implement something secure. Here’s an [article](https://www.pingidentity.com/en/company/blog/posts/2019/jwt-security-nobody-talks-about.html) describing the harder bits and pieces required to implement with JWTs without which it isn’t secure.
2. Limitations in the data that can be stored. Sensitive data regarding the user cannot be stored in JWTs as this data would then become public.
3. Features that require you to know which devices the user is logged in on are not possible. For example, if you want to show the user all the devices they’re logged in on and log out on one device from another.

## Prerequisites

1. An [AWS account](https://aws.amazon.com). Don’t worry, you will not be billed for anything as we’ll be using DynamoDB and Lambda which can be used for free with [certain limits](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free+Tier+Types=tier%23always-free).
2. [Node and NPM](https://nodejs.org/en/download/)
3. [Docker](https://docs.docker.com/get-docker/) — To run our Lambda Functions locally
4. Your editor of choice

If you’re comfortable with using the AWS CLI for the below steps you can do so. However, we’ll be working directly with the AWS Dashboard as it’s simpler to get started with.

Make sure you’re logged in to an AWS account that has the required permissions to use DynamoDB, Lambda, CloudFormation, and S3. If you’re using a personal account or a root user account, you don’t have to worry about the permissions and can move forward.

## Create a DynamoDB Table

First, log in to your AWS Console and head over to [DynamoDB](http://console.aws.amazon.com/dynamodb). Then, click on *Create Table.*

Press enter or click to view image in full size

![Screenshot of DynamoDB homepage]()

DynamoDB is a schemaless NoSQL database. It’s a hybrid of a document database and a key-value store. We’re using DynamoDB because it’s serverless which means we have almost nothing to manage, it’s extremely fast and reliable, and since it’s schemaless we can store unstructured data.

If you’ve never used a NoSQL database like DynamoDB or MongoDB before and are coming from using a traditional relational database like PostgreSQL, I’d suggest reading [this section from the AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SQLtoNoSQL.html) to learn more about how they compare and how they work.

[## From SQL to NoSQL

### If you are an application developer, you might have some experience using a relational database management system…

docs.aws.amazon.co](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SQLtoNoSQL.html?source=post_page-----60355bff8a97---------------------------------------)

When we click on *Create Table*, we’re taken to the below page.

Press enter or click to view image in full size

![Screenshot of the new table page of DynamoDB]()

Let’s analyze the different components that go into a DynamoDB table.

1. Table Name — Quite literally, the name of the table
2. Primary Key — Just like how in a relational database we have a Primary Key to identify a certain record, we have the Primary Key in DynamoDB.

If you look closely, you’ll also notice something called a Partition Key and a checkbox for a Sort key.

> The primary key is made up of a partition key (hash key) and an optional sort key. The partition key is used to partition data across hosts for scalability and availability. Choose an attribute which has a wide range of values and is likely to have evenly distributed access patterns. For example CustomerId is good while GameId is bad if most of your traffic relates to a few popular games.
>
> The sort key allows for searching within a partition. For example, an Orders table with primary attribute CustomerId and sort attribute OrderTimestamp would allow for queries for all orders by a specific customer in a given date range.

At this point if you’re confused about the terminology used, don’t worry, you’re not alone. The naming of the partition and sort keys are linked to the inner workings of DynamoDB and how it uses the two to distribute and store data and you don’t have to know much about what they are. However, for the curious ones out there, you can check out [this section](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.Partitions.html) of the AWS docs which explains the two in much more detail.

Let’s move forward by naming our table `UserSessions` and primary key `sessionId` which is of type `string`.

We’ll be sticking with the default settings as that will help us get started quickly and we don’t need to modify anything to get up and running with our application.

Finally, click *Create.*

## Working With DynamoDB

The API to work with DynamoDB is fairly simple. You can execute commands using the [REST API](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Using.API.html), the [AWS CLI](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Tools.CLI.html), or by using the [DynamoDB SDK](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.NodeJs.html). We’ll only be covering the basics of working with DynamoDB in this tutorial and won’t be going in-depth, but as always feel free to explore the [documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) if you want to learn more about working with DynamoDB.

In DynamoDB, an *item* is a collection of attributes where each attribute is a key-value pair and the value can be a scalar, a set, or a document type (documents are similar to JSON objects). To put it in simple words, an *item* is a record with multiple properties that are stored as key-value pairs. Each table has multiple items, and each item has multiple attributes.

To work with the data in DynamoDB we make use of operations. Operations are commands we can use to modify data in our DynamoDB table. There are four main operations for Create, Write, Update and Delete (CRUD) functionality, namely, `PutItem`, `GetItem`, `UpdateItem`, and `DeleteItem`.

### Writing Data

To write data to a DynamoDB table we make use of the `PutItem` operation.

```
{   
  "sessionId": { "S": "abcd-abcd-abcd" },  
  "userId": { "S": "dcba-dcba-dcba" },  
  "timestamp": { "N": 1612969254 },  
  "isActive": { "BOOL": true }  
}
```

If we perform the `PutItem` operation with the above input on the table we created, a new itemgets created in our table with the `sessionId` set to `abcd-abcd-abcd`, `userId` set to `dcba-dbca-dcba` and `timestamp` set to `1612969254`. Remember, we set `sessionId` as our primary key and of type string, so the value of this field has to be unique and of type string, else an error will be thrown.

**But what are** `S`, `N` and `BOOL`?  
That’s the data type of the value we’re providing. `S` stands for string, `N` for number, and `BOOL` for boolean. You can find the full list of all the available data types along with their constraints in the [official documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.NamingRulesDataTypes.html#HowItWorks.DataTypes).

### Updating Data

Similar to the `PutItem` operation, we use the `UpdateItem` operation to update data in our table. However, the `UpdateItem` operation works a little differently. We have to provide the primary key of the item whose data we want to modify and provide an **update expression**. An update expression specifies which attribute’s value to modify.

Suppose we want to modify the `isActive` attribute of the item we just created in the previous section, our update expression would be `SET active = :activeStatus` , where `:activeStatus` is a placeholder for the attribute value which we pass using the update expression attributes argument.

The update expression attributes argument will look similar to the input we provide to the `PutItem` operation like below.

```
{   
  ":activeStatus": { "BOOL": true }  
}
```

We specify the placeholder key and the value of that placeholder along with the value of the type.

### Reading Data

To read data we provide the primary key of the item we want to retrieve to the `GetItem` operation.

So far, the operations we’ve talked about and how we use them may seem a little vague as we haven’t run them yet. Hopefully, it becomes more clear when we write some code in the next section where we work with Lambda and DynamoDB.

## Creating the Lambda Functions

Unlike how we worked with DynamoDB directly from the AWS Dashboard, we’ll be working solely from our text editor and terminal when working with Lambda. We’ll even be bundling and deploying the Lambda functions directly from our terminal which we’ll look at in the next section.

### Functions We’ll Be Creating

1. Create session
2. Validate and get session info
3. Deactivate session

### Project Setup

1. Create three separate folders named `create-session`, `get-session-info`, and `deactivate-session`, one for each function.
2. In each folder run `npm init -y` to initialize NPM
3. All the Lambda functions will need to interact with DynamoDB which we’ll be doing using the AWS JavaScript SDK. We’ll also be needing the `@aws-sdk/util-dynamodb` package which contains utility functions that make working with the SDK easier. To install the SDK and utility library, run `npm i @aws-sdk/client-dynamodb @aws-sdk/util-dynamodb` in each of the folders.

### Create Session Function

For the create-session function, we’ll be using an additional package called `crypto-js` which contains functions that use different algorithms to generated hashes. To install it, run `npm i crypot-js`.

We first create a `generateId` function that randomly generates a Session ID using the `SHA256` hash function with the input being a concatenated string of the User ID, current timestamp, and a randomly generated number.

Then, we initialize an instance of the DynamoDB client.

And finally, we create the Lambda function handler whose input will be the user info such as the User ID and the output will be the session info which includes the Session ID, the expiry date, the active status, and the time it was created.

In the previous section, we discussed how we have to provide the data type of the value of the arguments. But notice how we’re not doing that here. Instead, we create a regular JavaScript object and pass that to the `marshall` function from the `@aws-sdk/util-dynamodb` package.

The `marshall` function takes a regular JavaScript object as input, interprets the data type of each argument, and returns an object with the format expected by DynamoDB where the datatype of the value of an attribute is provided.

For example, if we provide the input `{ sessionId: "abcd-abcd-abcd" }` to the `marshall` function, we get the output as `{ sessionId: { S: "abcd-abcd-abcd" } }`.

We call the `.putItem()` method on the instance of `DynamoDB` with the table name and the attributes of the item as input to perform the `PutItem` command.

### Validate Session and Get Session Data

Similar to the create-session function, we first initialize an instance of `DynamoDB`. The input to the Lambda function in this case will be an object with a single `sessionId` property and the output will be the session information.

We perform the `GetItem` operation by running the `.getItem()` method with the table name and key of the item we want to access as input, which in this case is the Session ID.

The structure of the response of the `GetItem` operation is similar to the input we provide to the `PutItem` operation, i.e. the datatypes of the attribute values are provided. However, we don’t want to deal with that as that makes accessing the data cumbersome. To remove the datatypes from the object we use the `unmarshall` utility whose function is the exact opposite of the `marshall` function. For example, if we provide the string `{ sessionId: { S: "abcd-abcd-abcd" } }` as input, the output would be `{ sessionId: "abcd-abcd-abcd" }`.

Before returning the session info we check if the session is expired, and if it is, we perform an `UpdateItem` operation by running the `.updateItem()` method and set the `isActive` attribute to false and return the session info object. If it is not expired, we update the expiry date of the session to 14 days from the current time and return the session info object with the updated expiry date.

### Deactivate Session

You might ask why we’re deactivating a session and not deleting it. Imagine after a session is created the user logs out, but before that, the user stores the session token that was created elsewhere.

Then, let’s consider we delete the token instead of deactivating it when the user logs out. Sometime in the future, however slim the possibility there might be, imagine a token is created that matches the exact token we had previously created and deleted for the previous user.

The previous user still has access to that token and if they try to access the application using that session token, they will get complete access to the second user's account.

To prevent the above scenario, we make sure the token will be unique till the end of time (literally). The simplest way to do this would be to have an active state and store whether that token is active or not. This way there’s a built-in constraint in the database preventing us from creating a duplicate session token including the ones which are deactivated.

Similar to the validate and get session data function, the input to this function will also be an object with the Session ID as a property. We then run the `UpdateItem` operation and set the `isActive` attribute to false and return the updated session info.

We also set the `ReturnValues` attribute of the `UpdateItem` command to `ALL_NEW`, which is telling DynamoDB to return all the attributes after updating the item.

## Testing locally and deploying with SAM

The [Serverless Application Model (SAM)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) is a framework that helps us build, test, package, and deploy serverless applications. In our case, we’ll be using it to test and deploy the Lambda functions we just created.

### How SAM works

To test Lambda functions locally, SAM creates an execution environment using Docker and executes the function based on the SAM template. To package and deploy the functions, SAM uses S3 and AWS CloudFormation under the hood.

### SAM Template

The SAM template is a YAML file that gives it the information it requires such as the functions runtime and where the code for our functions is situated.

At the top of the template, we provide the description of the application and some basic information that is required by CloudFormation which we won’t have to worry about.

Under the Resources section, we have the three functions we just created which are all of type `AWS::Serverless::Function`, i.e. a Lambda function.

We then provide the following properties to each function under `Properties`:

1. `CodeUri` — The relative path of the directory which contains the code
2. `Handler`— The Lambda handler function, which in our case is `index.lambdaHandler`, i.e. the `lambdaHandler` function which we exported in `index.js`.
3. `Runtime`— The execution environment of the Lambda Function which will be `nodejs12.x`.

### Setup AWS Credentials

To authenticate with AWS, we’ll need our a*ccess key ID* and the s*ecret access key.* You can get them by clicking on *My Security Credentials* under your username in the AWS Dashboard. In the *Your Security Credentials* page, under the Access Keys section click *Create New Access Key.* Make sure to note down or download the s*ecret access key* as it won’t be visible again.

Press enter or click to view image in full size![]()

Press enter or click to view image in full size![]()

You can set up your AWS Credentials [using the AWS CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-set-up-credentials.html), a credentials file, or environment variable. To set your credentials using environment variables, run the below commands in your terminal.

```
$ export AWS_ACCESS_KEY_ID=your_access_key_id  
$ export AWS_SECRET_ACCESS_KEY=your_secret_access_key
```

### Invoking the Functions

To start a dev server which will be the endpoint for calling our Lambda functions run `sam local start-lambda`. By default, this command will start a server at `localhost:3001`.

Let’s say you have a `/login` endpoint. Once you verify the credentials the user entered are correct, you would invoke the `CreateUserSessionFunction` with the user info as input and then store the `sessionId` from the output in the user's cookies. This way, every time a user sends a request to your backend, you can get the `sessionId` from the cookies and call `GetSessionInfoFunction` with that `sessionId` as input and get the session info.

To invoke the function using the AWS JavaScript SDK for node, you can use the code below. It invokes the `GetSessionInfoFunction` as mentioned in the SAM template file.

### Deploying the Functions

Finally, to package the function run `sam build` and to deploy it to AWS, run `sam deploy`. It’s really that easy!

To invoke the functions in deployment, remove the endpoint from the above example and you should be good to go!

## Conclusion

There are numerous ways we can go about session authentication and as mentioned before, using the approach we just used with Lambda and DynamoDB is not for every use case, especially not for monolithic applications.

The great thing about our approach, and of serverless in general is that it’s production-ready from day one. And with much less effort, our approach is just as secure as some of the more secure methods of using JWTs.

### What Next

* You can try using an in-memory database like Redis for the best performance.
* Use a `.env` file or a credentials file to store your AWS credentials so that you don’t have to set the environment variables every time.

The final code for the tutorial can be found on GitHub at[*shreyas44/session-auth-tutorial*](https://github.com/shreyas44/session-auth-tutorial)