---
title: "NestJS vs Go: Performance comparison for JWT verify and MySQL query"
url: https://medium.com/p/510221e6dea8
---

# NestJS vs Go: Performance comparison for JWT verify and MySQL query

[Original](https://medium.com/p/510221e6dea8)

Press enter or click to view image in full size

![]()

# NestJS vs Go: Performance comparison for JWT verify and MySQL query

[![Mayank C](https://miro.medium.com/v2/resize:fill:64:64/0*a4jE1aEeFKMXLgkE.jpg)](/@choubey?source=post_page---byline--510221e6dea8---------------------------------------)

[Mayank C](/@choubey?source=post_page---byline--510221e6dea8---------------------------------------)

5 min read

·

Jun 20, 2023

--

15

Listen

Share

More

## Introduction

After publishing a record number of articles on comparing performance of various technologies like Node.js, Deno, Bun, Rust, Go, Spring, Python, etc. for a simple hello world case, I consistently got comments that the articles were good, but weren’t applicable directly for real-world use cases. I was asked to do the same for more ‘real-world’ cases. The articles also (and still) attracted a record number of views. However, the point was well taken. Hello world was the best starting point, but definitely not a ‘real-world’ case.

### Real-world use case

This article is a part of the series where I’m going to compare a number of technologies for a real-world case:

* Get JWT from the authorization header
* Verify JWT & get email from claims
* Perform a MySQL query with email
* Return the user record

This is a very common real-world case. For the ‘Hello world’ case, I’ve seen the technologies offering somewhere between 50K to 200K RPS. The RPS was high because all the app was doing was returning a simple string. Of course, we won’t expect a 200K RPS for the JWT + MySQL use case. How much we’ll get is yet to be seen.

This article compares NestJS & Go for this use-case. This is an interesting comparison because NestJS (which runs in Node.js) is interpreted, while Go compiles to machine code. Also, verifying JWT is a CPU intensive operation. The compiled language should be faster than interpreted one? Isn’t it? We’ll know very soon.

Due to the large number of articles that will get published, I’ll also be creating an article to index all the real-world cases. At the end of this article, you’ll find a link to that article. Let’s get started.

## Test setup

All tests are executed on MacBook Pro M1 with 16G of RAM.

The software versions are:

* Node v20.3.0
* Go v1.20.4

On Node side, I’m using NestJS framework for the webapp part. By default, the NestJS app runs over the Express framework. The other frameworks on Node side are nest-jwt for verifying & decoding JWTs (nest-jwt is a wrapper over jsonwebtoken), and mysql2 for performing MySQL queries.

On the Go side, I’m using Gin web framework. The other frameworks that I’m using are: golang-jwt for verifying and decoding JWTs, and go-sql-driver for performing MySQL queries.

The HTTP load tester is built over libcurl. There is a pre-created list of 100K JWTs. The tester picks random JWTs and sends it in the Authorization header of the HTTP request.

The MySQL database contains a table called users, which has 6 columns:

```
mysql> desc users;  
+--------+--------------+------+-----+---------+-------+  
| Field  | Type         | Null | Key | Default | Extra |  
+--------+--------------+------+-----+---------+-------+  
| email  | varchar(255) | NO   | PRI | NULL    |       |  
| first  | varchar(255) | YES  |     | NULL    |       |  
| last   | varchar(255) | YES  |     | NULL    |       |  
| city   | varchar(255) | YES  |     | NULL    |       |  
| county | varchar(255) | YES  |     | NULL    |       |  
| age    | int          | YES  |     | NULL    |       |  
+--------+--------------+------+-----+---------+-------+  
6 rows in set (0.00 sec)
```

The users table is prepopulated with 100K records:

```
mysql> select count(*) from users;  
+----------+  
| count(*) |  
+----------+  
|    99999 |  
+----------+  
1 row in set (0.01 sec)
```

For each email present in the JWT, there is a corresponding user record in the MySQL database.

### Code

***NestJS***

***Go***

## Results

Each test is executed for 1M requests in total. The concurrency levels are 10, 50, and 100 connections. A warm-up of 1K requests is given before taking measurements.

Here are the charts with the results:

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

## Conclusion

A scorecard is generated from the results using the following formula. For each measurement, get the winning margin. If the winning margin is:

* < 5%, no points are given
* between 5% and 20%, 1 point is given to the winner
* between 20% and 50%, 2 points are given to the winner
* > 50%, 3 points are given to the winner

![]()

![]()

A list of all real-world performance comparisons is [here](/deno-the-complete-reference/list-of-all-of-my-real-world-performance-comparisons-a8e9182ac50).