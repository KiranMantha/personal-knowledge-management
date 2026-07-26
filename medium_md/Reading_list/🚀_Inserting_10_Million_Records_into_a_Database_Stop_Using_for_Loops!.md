---
title: "🚀 Inserting 10 Million Records into a Database? Stop Using for Loops!"
url: https://medium.com/p/70079bc72ae4
---

# 🚀 Inserting 10 Million Records into a Database? Stop Using for Loops!

[Original](https://medium.com/p/70079bc72ae4)

Member-only story

# 🚀 Inserting 10 Million Records into a Database? Stop Using `for` Loops!

[![Umesh Kumar Yadav](https://miro.medium.com/v2/resize:fill:64:64/1*Tf54OEWBcwlddSz7jrZffg.jpeg)](/@umeshcapg?source=post_page---byline--70079bc72ae4---------------------------------------)

[Umesh Kumar Yadav](/@umeshcapg?source=post_page---byline--70079bc72ae4---------------------------------------)

5 min read

·

May 26, 2026

--

6

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D70079bc72ae4&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fjavarevisited%2Finserting-10-million-records-into-a-database-stop-using-for-loops-70079bc72ae4&source=---header_actions--70079bc72ae4---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

When working on backend systems, there’s one task almost every developer eventually encounters:

* Data migration
* Batch imports
* Initialization scripts
* Log archiving
* ETL pipelines

And then comes the classic nightmare:

> *“My boss asked me to insert 10 million rows into the database.  
>  I wrote a* `for` *loop yesterday… and it’s still running.”*

If you’re still inserting records one row at a time, this article may save you days of execution time — literally.

Today, we’ll benchmark **5 different insertion strategies** using MySQL and compare their real-world performance to find out which method truly deserves the crown.

## 🛠️ Test Environment

To keep the comparison fair, all tests were executed under the same environment.

## Database

* MySQL 8.0 (Docker deployment)

## ORM / Frameworks

* Spring Data JPA (Hibernate)
* Native JDBC

## Dataset

* 10 million records