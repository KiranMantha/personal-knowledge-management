---
title: "Build yourself a simple CRM from scratch in PHP and MySQL"
url: https://medium.com/p/58fef061b075
---

# Build yourself a simple CRM from scratch in PHP and MySQL

[Original](https://medium.com/p/58fef061b075)

# Build yourself a simple CRM from scratch in PHP and MySQL

[![Richard](https://miro.medium.com/v2/resize:fill:64:64/0*Ibcxqe4L6KkgMkf8.png)](/@chensformers?source=post_page---byline--58fef061b075---------------------------------------)

[Richard](/@chensformers?source=post_page---byline--58fef061b075---------------------------------------)

8 min read

·

Mar 1, 2017

--

2

Listen

Share

More

Press enter or click to view image in full size

![CRM]()

Customer Relationship Management (CRM) is a system that manages customer interactions and data throughout the customer life-cycle between the customer and the company across different channels. In this tutorial, we are going to build a custom CRM in PHP, which a sales team can use to track customers through the entire sales cycle.

We’ll be creating a simple CRM system for salespeople to:

* Access their tasks
* View their leads
* Create new tasks for each lead
* Create new opportunity
* Close a sale

Sales managers will be able to:

* Manage all customers
* Manage sales team
* View current sales activities

[Download Demo Files](https://github.com/phpcontrols/phpgrid-custom-crm)

## Building Blocks of a CRM

Here is a list of the essential components of the CRM:

* **Leads**: initial contacts
* **Accounts**: Information about the companies you do business with
* **Contact**: Information about the people you know and work with. Usually, one account has many contacts
* **Opportunities**: Qualified leads
* **Activities**: Tasks, meetings, phone calls, emails and any other activities that allow you to interact with customers
* **Sales**: Your sales team
* **Dashboard**: CRM dashboards are much more than just eye candy. They should deliver key information at a glance and provide links to drill down for more details.
* **Login**: Salespeople and managers have different roles in the system. Managers have access to reports and sales pipeline information.

![]()

## System Requirements

* PHP 5.3+,
* MySQL or MariaDB
* [phpGrid](http://phpgrid.com/)

## Create CRM Database

We will start by creating our custom CRM database. The main tables we will be using are:

* **contact** — contains basic customer data
* **notes** — holds information collection from Contact by sales people.
* **users** — information about sales people

![]()

The **Contact** table contains basic customer information including names, company addresses, project information, and so forth.

The **Notes** table stores all sales activity information such as meetings and phone calls.

The **Users** table holds login information about users of the system such as usernames and passwords. Users can also have roles, such as Sales or Manager.

All other tables are [lookup tables](https://www.quora.com/In-database-what-are-lookup-tables) to join to the three main relational database tables.

* **contact\_status** — contains contact status such as Lead and Opportunity. Each indicates a different stage in a typical sales cycle
* **task\_status** — the task status can be either Pending or Completed
* **user\_status** — a sale person can be Active or Inactive
* **todo\_type** — a type of task either Task or Meeting
* **todo\_desc** — description of a task such as Follow Up Email, Phone Call, and Conference etc.
* **roles** — a user can be either a Sales Rep or a Manager

### Complete Database Schema Diagram

A database schema is the structure that represents the logical view such as tables, views, or primary and foreign keys of the entire database. A database schema includes entities and the relationship among them.

It is a good practice to have one primary key for each table in a relational database. A primary key is a unique identifier for each record. It can be the social security number (SSN), vehicle identification number (VIN), or auto-increment number. This is a unique number that is generated when a new record is inserted into a table.

Below is the database diagram of our simple CRM. The key symbol in each table represents the table primary key. The magnifying glass indicates foreign key linking another table in the database. Sometimes we call it the “lookup” table.

Press enter or click to view image in full size

![]()

### install.sql

Once you have an understanding of the database table structure, find the “install.sql” script in the `db` folder and use a MySQL tool such as [MySQL Workbench](http://www.mysql.com/products/workbench/) or [Sequel Pro](https://www.sequelpro.com/) to run the SQL script. It should create a new relational database named `custom_crm` and its database tables.

## Setup phpGrid

Press enter or click to view image in full size

![]()

Our CRM contains many datagrids. The datagrid is a spreadsheet-like data table that displays rows and columns representing records and fields from the database table. The datagrid gives the end-user ability to read and write to database tables on a webpage. We can use a datagrid tool from [phpGrid](http://phpgrid.com/). We use a tool instead of building them from scratch because developing the datagrid is usually tedious and error-prone. The datagrid library will handle all internal database **CRUD (Create, Remove, Update, and Delete)** operations for us with better and faster results with little code. To install phpGrid, follow these steps:

1. Unzip the phpGrid download file.
2. Upload the phpGrid folder to the `phpGrid` folder.
3. Complete the installation by configuring the `conf.php` file.

Before we begin coding, we must specify the database information in `conf.php`, the phpGrid configuration file. Here is an example of database connection settings:

* **PHPGRID\_DB\_HOSTNAME** — web server IP or host name
* **PHPGRID\_DB\_USERNAME** — database user name
* **PHPGRID\_DB\_PASSWORD** — database password
* **PHPGRID\_DB\_NAME** — database name of our CRM
* **PHPGRID\_DB\_TYPE** — type of database
* **PHPGRID\_DB\_CHARSET** — always ‘utf8’ in MySQL

To learn more about configuring phpGrid, check out [phpGrid complete installation guide](http://phpgrid.com/documentation/installation/).

## Page Template

Press enter or click to view image in full size

![]()

Before we can start building our first page of the CRM, it is a good practice to make the reusable page items such as header and footer.

The page will comprise of a header, menu, body and footer. We will start by creating a reusable page template.

## head.php

This is a basic HTML5 template header. It includes a link to a custom stylesheet that will be created in a later step.

## menu.php

Press enter or click to view image in full size

![]()

Notice the usage of `$_GET['currentPage']`. Each page will set a value which will highlight the name of the current page on the top menu bar.

Include the following code in style.css for menu styling (minified). It will transform the above, unordered list into a menu.

## footer.php

Simple closing body and html tags.

## Complete Page Template

This is the complete page template. The main content will go after `Section Title`.

## CRM Main Pages

Press enter or click to view image in full size

![]()

Are you still with me? Good! We can now finally develop the first page in our CRM.

Our CRM for the sales team members has four pages:

* **Tasks**
* **Leads**
* **Opportunities**
* **Customers/Won**

Each page indicates a different stage in a typical sales cycle.

## Sale People Page Design Mockup

Here’s our CRM design mockup for the sales people.

Press enter or click to view image in full size

![]()

## Tasks Page

When a sales team member logged in, the first page he sees is a list of current tasks.

As you may recall, our Notes table holds all the sales activity information. We can create a datagrid and populate it from the Notes table using phpGrid.

The Tasks page main content is a datagrid. The following two lines will give us a list of tasks of the current sales person.

* The first line creates a phpGrid object by passing the SELECT SQL statement, its primary key — `ID`, and then the name of the database table - `notes`.
* The second and the final line calls [display()](http://phpgrid.com/documentation/display/) function to render the datagrid on the screen. Check out the [basic datagrid demo](http://phpgrid.com/example/example-1-a-basic-php-datagrid-2/) for more detail.

## Leads Page

The leads page contains list of current leads that the sales person is responsible for. Each Lead can have one or many Notes. We will use the [phpGrid master-detail](http://phpgrid.com/example/master-detail-grid/) feature for that.

We also need to use [set\_query\_filter](http://phpgrid.com/documentation/set_query_filterwhere/)() to display only the leads, `Status = 1`, and only for the current sales person.

### Contact status table

![]()

## Opportunities Page

A Lead becomes an Opportunity once it is qualified. The Opportunities page is similar to the Leads page. The only difference is the filtered status code in set\_query\_filter is `Status = 2`.

## Customers/Won Page

Customers/Won has the `Status = 3`. Similar to Leads and Opportunities, Customers/Won can also have Notes.

That’s all there is to it for sales people in our simple CRM.

## Manager Dashboard

Press enter or click to view image in full size

![]()

The sales manager will have access to all records in the sales pipeline as well as the ability to manage sales team and customer data.

We will have a single web page with tabbed menu similar to the [phpGrid tabbed grid demo](http://phpgrid.com/example/tabbed-datagrid/).

## Manager Dashboard Design Mockup

### My Sales Reps

Press enter or click to view image in full size

![]()

## Main content

Each tab represents a table in the CRM database. `$_GET['gn']` will store the table name. It dynamically generates the datagrid based on table name passed.

It’s very easy to integrate jQueryUI Tabs with phpGrid. Please refer to the phpGrid [Tabbed Grid demo](http://phpgrid.com/example/tabbed-datagrid/) for more information.

## My Sales Rep Page

Since a sales manager needs to quickly find out whom a sale person is working with, we added a detail grid `$sdg` populated from contact table and link with the master grid.

`sales_rep` is the connecting key in `contact` table to the `id` that is the foreign key in `users` table. Remember the `users` stores all of our sales people information.

## Screenshots

### CRM — Sales Screen

Press enter or click to view image in full size

![]()

### CRM — Manager Screen

Press enter or click to view image in full size

![]()

## Live Demo

[CRM Sales Rep Screen](http://phpdatagrid.com/apps/phpgrid-custom-crm/sales/tasks.php) | [CRM Managers screen](http://phpdatagrid.com/apps/phpgrid-custom-crm/managers/pipeline.php)

## Source Code

Available [here](https://phpgrid.com/example/build-first-simple-crm-scratch/)

## Thanks for reading. If you enjoyed this article, please hit that clap button 👏 to help others find it and [follow me on Twitter](https://twitter.com/midlifesaas).

[![]()](https://twitter.com/midlifesaas)