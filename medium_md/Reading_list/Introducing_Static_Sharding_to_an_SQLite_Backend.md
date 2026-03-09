---
title: "Introducing Static Sharding to an SQLite Backend"
url: https://medium.com/p/f97ff6565221
---

# Introducing Static Sharding to an SQLite Backend

[Original](https://medium.com/p/f97ff6565221)

# Introducing Static Sharding to an SQLite Backend

[![Zlatin Stanimirov](https://miro.medium.com/v2/resize:fill:64:64/1*CufswoNKlBmzZNaalCxdSA.jpeg)](/@stanimirovv?source=post_page---byline--f97ff6565221---------------------------------------)

[Zlatin Stanimirov](/@stanimirovv?source=post_page---byline--f97ff6565221---------------------------------------)

5 min read

·

Jan 14, 2024

--

Listen

Share

More

I am recently reading up a bit on sharding and wanted to make an experiment — to introduce static sharding to an backend project I have that uses SQLite.

Sharding to a serverless database ? Controversial, I know.

SQLite is an amazing library and storage engine. It is single file, zero dependencies, offers amazing functionality and it is basically the most used database in the world. Due to embedded devices, but facts are facts!

Yes, it is a library not a server, therefore it is usually used in embeded systems / local databases. It isn’t the go-to thing for web development, however I am using it for a lot of my side projects. Some of the side projects are live for years and have hundreds of thousands of records, like the price tracker I previously wrote about.

One of said side projects is starting to get big so I thought to myself: How can I scale up? The obvious choice is to migrate to a database that allows more scaling, like postgres or mysql. I decided to try scale up the SQLite instance.

### Sharding SQLite is not usually a good idea

Sharding SQLite is usually a bad idea — SQLite is usually intended for single node usage. You may benefit from sharding SQLite if the different nodes are on different storage units (think HDDs/SSDs) therefore you may be able to paralelize the I/O. For most apps that you will use SQLite this is not a valid usecase, however, I was very interested to see how things will look.

In my specific use case, the dataset I am hosting in SQLite started growing with **30 megabytes per week**. This means that the dataset (if unchanged) will grow to **1.5 Gigabytes every year**! SQLite can handle it without a problem, but **the server I am renting will not.** And this is the exact moment when the idea was created — If I need to scale up the instance, what is the most effective way to do it ?

You can make a very valid comment that I should move away from SQLite, BUT I don’t want to do that. Let’s put the constraint that it has to be SQLite, so how can we refactor the app ?

### As is and To Be

Currently, the app is a single node that has a single SQLite instance.

The goal is to create a single node with multiple SQLite shards so that, if needed, the app can be scaled to several nodes, each node having one or more shards.

Let’s put the requirements, we need a library that:

* Supports sharding on SQLite that uses consistent hashing by some ID for each table.
* Allows you to setup a node that has different ammount of shards and can adapt to them and **doesn’t requre resharding when starting a new instance.** That last part is an artificial requirement — in reality since I own the APP I can allow as much downtime as needed. That being said I think the problem is much more interesting to solve if we don’t allow resharding.

### How do we implement this ?

The first problem we need to solve is, in a single node with multiple SQLite instances, how can we create consistent hasing ? In our use case the key by which we will search and store is a unique string. We can represent the string as a number and modulo divide it by the number of shards. This will give us consistent hashing. Modulo hashing isn’t a good idea for dynamic sharding as adding a new shard would require rebalancing, but in our case we will have a static number of shards so this is not an issue.

Now that we have solved the first problem, how can we solve it when we have multiple nodes ?

We would need to introduce some sort of routing. Let’s look at some possibilities.

We may introduce a load balancer with a thin layer of business logic to decide to which nodes it should route the requests This would be an extra layer and it would increase to complexity of the system. The load balancer configuration would also need to be updated when extra nodes are added.

Press enter or click to view image in full size

![]()

An alternative approach is to send a request to all of the instances simultaniously from the client. This means that the client must know about all possible endpoints, but it doesn’t have to know the implementation details of the sharding. As long as the node list is up to date, and we are fine with the extra HTTP traffic this is a good choice.

Press enter or click to view image in full size

![]()

The **final option** is to send the request to an arbitrary node and then the node can re route the request if it is not the correct one. This means that there will be 1 or at most 2 requests, which is likely to be less than the client fan out strategy described earlier. The tradeoff is in complexity and performance.

Press enter or click to view image in full size

![]()

The good thing about the first two strategies is the determinism of the requests.

The main difference between them is who holds the responsibility of the routing and how it is done (routing or the greedy fan out). The first option (seperate load balancer / router) adds more pieces to the board which is sub optimal but has nice seperation of concerns. Since there are more moving pieces there are more possible places an error may occur.

The second option is very greedy, but can be the most performant one as long as the network or nodes are not close to their limits — there is no routing so the requests don’t bounce which means that it is by design faster.

Let’s get back to the final option — the request routing is nondeterministic as you may or may not hit the correct node. I also don’t like the nodes knowing about each other’s existance. It adds an extra layer of complexity and meshes (which the communication type would be) are much trickier to debug in the long run.

The option I chose to implement was the second one — the client will fan out with requests to all the nodes. The traffic for the app allows for it.

### Ah yes, overengineering- my old nemesis

I did a prototype on my local machine with 2 nodes and changes to the client — it worked like a charm. In fact I did this part first and started doubting the sharding itself. For my purposes the client might know all the nodes and send a request to only one node.

The excercise in system design was a fun one, but not something I really need. In fact I started speculating that I can change the data model and drastically reduce the size of the dataset thus reducing the need for sharding. More on that next time.