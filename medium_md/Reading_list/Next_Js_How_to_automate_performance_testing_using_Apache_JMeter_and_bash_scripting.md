---
title: "Next Js: How to automate performance testing using Apache JMeter and bash scripting"
url: https://medium.com/p/98d41d497172
---

# Next Js: How to automate performance testing using Apache JMeter and bash scripting

[Original](https://medium.com/p/98d41d497172)

# Next Js: How to automate performance testing using Apache JMeter and bash scripting

[![Debabrata Nayak](https://miro.medium.com/v2/resize:fill:64:64/1*lwoeV9514uXKRcKYYWJD2Q.jpeg)](/@debabrata100?source=post_page---byline--98d41d497172---------------------------------------)

[Debabrata Nayak](/@debabrata100?source=post_page---byline--98d41d497172---------------------------------------)

5 min read

·

Apr 8, 2023

--

Listen

Share

More

A quick tutorial to automate the JMeter load testing to get performance insights of you server render application using react and next js.

### Apache JMeter

Apache JMeter is an Apache project that can be used as a load testing tool for analysing and measuring the performance of a variety of services, with a focus on web applications.

> The codebase for this tutorial: [**https://github.com/debabrata100/nextjs-load-testing**](https://github.com/debabrata100/nextjs-load-testing)

Lets follow these steps to get along

* Setup a next js application with a todolist page
* Install and Start JMeter
* Run Load testing and analyse reports
* Automate terminal commands with bash script
* Increase Page load time and Analyse reports

> Prerequisite: You must have these packages installed onyou system: **node js**, **npm**, **Java**

This tutorial is focused on linux users. But windows users can benifit as well.

### Setup a next js application with a todolist page

Run the command to create a next js application. Let’s go with pages directory of next js when terminal prompt asks.

```
npx create-next-app@latest load-test-app  
npm run dev
```

At this point you application must be running on <http://localhost:3000/>

Now inside pages directory create a files called **todolist.jsx** and write the following code

```
export async function getServerSideProps(context) {  
  const todos = Array.from({ length: 5 }, (_, i) => i).map((id) => {  
    return {  
      id,  
      name: `Todo - ${id}`,  
    };  
  });  
  return {  
    props: {  
      todos,  
    },  
  };  
}  
  
export default function TodoList({ todos }) {  
  return (  
    <div className="todolist">  
      <h1>Todo List Page</h1>  
      <ul>  
        {todos.map(({ name, id }) => {  
          return <li key={id}>{name}</li>;  
        })}  
      </ul>  
    </div>  
  );  
}
```

In the above code we have created a react component called Todoist and rendering a list of todos. The todos are returned from **getServerSideProps** async function to make the todos array available from server side.

Now Visit <http://localhost:3000/todolist> and you must be seeing following screen.

Press enter or click to view image in full size

![]()

### Install and Start JMeter

for mac users

```
brew install jmeter  
open /usr/local/bin/jmeter
```

For other users, you can easily get it on internet :)

### Run Load testing and analyse reports

At this point our JMeter application should be up and running and you must be seeing following screen

Press enter or click to view image in full size

![]()

Right click on Test Plan and add a ThreadGroup user as following

Press enter or click to view image in full size

![]()

Next, Put number of threads: 5 and Loop Count: 10 as following

Press enter or click to view image in full size

![]()

Again Right Click on Thread Group and add a http request as following

Press enter or click to view image in full size

![]()

Next, fill the form as following:

Protocol: **http**, Server Name: **localhost**, port: **3000**, select **GET** for http request, path: **/todolist**

Press enter or click to view image in full size

![]()

Click on save and save the file inside a new directory **load-test** under root of you application. The file must have .jmx extention

Then create another directory called **results** under load-test.

It’s time to run load testing and generate report.

Now open your terminal and run the following command

```
jmeter -n -t <path to your app>/load-test/demo.jmx -l <path to your app>/load-test/results/demo_results.jtl -e -o <path to your app>/load-test/results/demo_results_temp
```

In order to fill ***path to your app***, cd to you app directory and run

```
pwd
```

Copy the entire path and replace <path to your app>. Here is an example

```
jmeter -n -t /Users/macuser/Documents/experiments/load-test-app/load-test/demo.jmx -l /Users/macuser/Documents/experiments/load-test-app/load-test/results/demo_results.jtl -e -o /Users/macuser/Documents/experiments/load-test-app/load-test/results/demo_results_temp
```

Press enter and run. When you run then the command you must be following results on your terminal

Press enter or click to view image in full size

![]()

On Completion, our artefacts are ready inside **/load-test/results** directory.

Inside **/results/demo\_results\_temp**, open **index.html** in your browser. you must be seeing following screen

Press enter or click to view image in full size

![]()

Lets get familiar with some of the matrices

**Samples**: Number of thread multplied to loop count. In our case a total of 25 request has been made to <http://localhost:3000/todolist> by 5 users each triggered 5 request

> You can modify the loop count and number of users analyse reports as per you requirement

**Average**: Response time or latency measured in milliseconds (587.00)

**Min**: Minimum Latency measured in milliseconds(71)

**Max**: Maximum Latency measured in milliseconds(2148)

**Received/Sent**: Network bandwidth at the time of testing

### Automate terminal commands with bash script

For Linux users:

Create a file called script.sh inside your load-test directory and make it executable using following commands.

```
touch script.sh  
chmod +x script.sh
```

Open script.sh file and write the same command we have run on the terminal. Put ***/bin/bash*** at the start as following

```
#! /bin/bash  
  
jmeter -n -t /Users/linx/Documents/experiments/load-test-app/load-test/demo.jmx -l /Users/linx/Documents/experiments/load-test-app/load-test/results/demo_results.jtl -e -o /Users/linx/Documents/experiments/load-test-app/load-test/results/demo_results_temp
```

Now open your terminal, cd to **load-test** dir and run the following command. Before running you must clear **results** directory in order to avoid folder not empty error.

```
./script.sh
```

### Increase Page load time and Analyse reports

Now let’s add some delay displaying the todolist. In order to do this we can take help of a simple Javascript async function, Javascript Promise and browser api SetTimeout. Lets modify out **todolist.jsx** file as following

```
const fetchTodos = async function () {  
  return new Promise((resolve) => {  
    setTimeout(() => {  
      const todos = Array.from({ length: 5 }, (_, i) => i).map((id) => {  
        return {  
          id,  
          name: `Todo - ${id}`,  
        };  
      });  
      resolve(todos);  
    }, 2000);  
  });  
};  
  
export async function getServerSideProps(context) {  
  const todos = await fetchTodos();  
  console.log({ todos });  
  return {  
    props: {  
      todos,  
    },  
  };  
}  
  
export default function TodoList({ todos }) {  
  return (  
    <div className="todolist">  
      <h1>Todo List Page</h1>  
      <ul>  
        {todos.map(({ name, id }) => {  
          return <li key={id}>{name}</li>;  
        })}  
      </ul>  
    </div>  
  );  
}
```

We have added 2 seconds delay to fetch the todos.

Now clear your results directory again and run the script.sh file. After running you might be seeing terminal results as follows

Press enter or click to view image in full size

![]()

On My machine I get the following results

Press enter or click to view image in full size

![]()

You must notice now, the average time has increased to 2045.36ms.

To get follow along check the commits of <https://github.com/debabrata100/nextjs-load-testing>

Thank you for reading. I hope it would help you to save some debugging time. Happy Coding. :)