---
title: "Full Stack Application Deployment with Docker, AWS EC2, and GitHub Actions"
url: https://medium.com/p/dbc51b09e2c5
---

# Full Stack Application Deployment with Docker, AWS EC2, and GitHub Actions

[Original](https://medium.com/p/dbc51b09e2c5)

# Full Stack Application Deployment with Docker, AWS EC2, and GitHub Actions — PART 1: Dockerizing

[![Uğurcan Erdoğan](https://miro.medium.com/v2/resize:fill:64:64/1*6ZomfQytpILzqmN5g_c69w.png)](/@ugurcanerdogan?source=post_page---byline--dbc51b09e2c5---------------------------------------)

[Uğurcan Erdoğan](/@ugurcanerdogan?source=post_page---byline--dbc51b09e2c5---------------------------------------)

11 min read

·

May 4, 2023

--

1

Listen

Share

More

Press enter or click to view image in full size

![]()

## **Introduction:**

Software development is now more complex than ever in the modern world. Full-stack development is now a well-liked strategy for creating cross-platform applications. But with this increased complexity also comes the need for more effective application deployment and management.

In this article, we’ll look at how to deploy a full-stack application on AWS EC2 using docker, and how to set up continuous integration and deployment (CI/CD) using GitHub Actions.

Three steps will make up this process: **Dockerizing, AWS EC2 deployment, and CI/CD using GitHub Actions**. *BookPortal* is the name of the full-stack application that we’ll be working with; it was created using the **Spring Boot** and **ReactJS** technologies, as well as **Nginx**, **Docker**, **AWS EC2**, and **GitHub Actions**.

* The main topic of **part 1** is dockerizing this full-stack application. We’ll go over how to make a Dockerfile for the back-end, front-end, and proxy-nginx layers, as well as how to use docker-compose to connect them all.
* **Part 2** will cover the AWS EC2 deployment procedure. We’ll go over setting up an EC2 instance on AWS, installing and configuring Nginx, and deploying our dockerized full-stack application to the server.
* The main focus of **part 3** will be the setup of GitHub Actions for CI/CD. We will go over how to set up build and deployment jobs, create workflow files for each application tier, and automate the deployment of our application to the server after each commit to our repository.

This article should have given you a solid understanding of how to dockerize a full-stack application, deploy it on AWS EC2, and use GitHub Actions to automate the CI/CD process. So let’s get going!

### About the context and structure of the application:

*BookPortal is a full-stack application that serves as a platform for book enthusiasts. Users can search for friends in the system, add their favorite books to reading lists, and indicate which books they are currently reading. Additionally, users can follow their preferred authors.*

*The system also has an advanced admin panel with functions for managing books, authors, and users. The admin can keep the system organized and current with the aid of these features.*

*Overall, BookPortal is a complete solution for book lovers that offers an easy way to manage their social connections and reading habits.*

First of all, the BookPortal project is in a GitHub repository, which includes the following folders and files:

![]()

The ***book-portal-be*** folder contains the back-end source code, while the ***book-portal-fe*** folder includes the front-end source code. The ***nginx*** folder contains the Nginx configuration files, and the docker-compose.yml file is used to configure and run the Docker containers. (Your project may have a similar structure.)

The tables in the database of our application are as in the figure below. The system entities can also be seen in this way.

Press enter or click to view image in full size

![]()

When the application is deployed, the incoming requests will proceed in a flow as in the diagram below.

![]()

* The request from the client will be met in Nginx and forwarded to the front-end port.
* The requests to be made by the front-end will be directed to the back-end port by Nginx again.

**The brief tech stack information of the application is as follows:**

* JavaScript
* ReactJS
* Semantic UI
* Java 18
* Spring Boot
* Hibernate — JPA
* Swagger

We’ll go over how to set up continuous integration and deployment using GitHub Actions, as well as how to deploy our dockerized application on AWS EC2 later. The Dockerfile and docker-compose.yml files that are necessary for the dockerization process will now be covered in detail. 🐳

![]()

### Dockerizing back-end (Spring Boot) ⚙️

![]()

Firstly, we will observe the back-end Dockerfile file and quickly examine how to dockerize the Spring Boot part.

```
FROM maven:3.8-openjdk-18 AS build  
COPY src /usr/src/app/src  
COPY pom.xml /usr/src/app  
RUN mvn -f /usr/src/app/pom.xml clean package  
  
FROM openjdk:18-alpine  
COPY --from=build /usr/src/app/target/BookPortal-0.0.1-SNAPSHOT.jar /usr/app/BookPortal-0.0.1-SNAPSHOT.jar  
EXPOSE 8080  
ENTRYPOINT ["java","-jar","/usr/app/BookPortal-0.0.1-SNAPSHOT.jar"]
```

We will review the Dockerfiles in detail line by line when necessary, but we can directly examine the comprehensible parts in blocks.

* Firstly, the Dockerfile prepares the **maven-java18** image which is required to build the Spring Boot project.
* Then, it moves our back-end files and “pom.xml” files to the container for building.
* Finally, the building process is performed to make the back-end jar file ready for use.
* In the second block, the Dockerfile prepares the necessary Java JDK image to run this jar file, and Java 18 is used in this project.
* After that, the previously created jar file is copied to this Java container, and it is specified that the application will listen on port 8080.
* Lastly, the Dockerfile runs the back-end application by issuing the necessary command.

> *Some names may vary depending on your application’s configurations. For example port number, jar file name etc.*

In Dockerfile files of both BE and FE, we employ multi-stage build logic where we first build the project and then run it in the appropriate environment. This approach eliminates the need for build artifacts (maven and node in our project) in final images, resulting in smaller and more efficient images. You can click on [this link](https://docs.docker.com/build/building/multi-stage/#use-multi-stage-builds) to learn more about this concept.

### Dockerizing front-end (React JS) 👨‍💻

![]()

Now we will examine how to build our front-end React JS project and [how we can serve it with the help of Nginx](/@aedemirsen/hello-everyone-in-this-article-i-will-talk-about-a-web-server-technology-that-we-can-serve-our-9c54be595ddc).

```
# build front-end  
FROM node:alpine as build  
WORKDIR /app  
ENV PATH /app/node_modules/.bin:$PATH  
COPY package.json /app/package.json  
RUN npm install --silent  
COPY . /app  
RUN npm run build  
  
# move builds to nginx and run the front-end  
FROM nginx:alpine  
COPY --from=build /app/build /usr/share/nginx/html  
RUN rm /etc/nginx/conf.d/default.conf  
COPY ./nginx/nginx.conf /etc/nginx/conf.d  
EXPOSE 3000  
CMD ["nginx", "-g", "daemon off;"]
```

* To start, we use the node image to build our React JS project and set the working directory to “/app” in the image with `WORKDIR`keyword. This means that all subsequent operations and file copying will be performed in the app directory in the **node** container.
* Next, we add “/app/node\_modules/.bin” directory to the PATH variable using the `$ENV PATH` command. By doing so, the executable files of the packages installed in the application are added to the PATH, making them executable directly from the command line. The `$PATH` structure preserves the existing PATH variable and only adds the “/app/node\_modules/.bin” directory. [Here is another reference for these steps.](https://wkrzywiec.medium.com/how-to-put-your-java-application-into-docker-container-5e0a02acdd6b)
* In the following step, we copy the “package.json” file containing front-end dependencies to the container and download these dependencies to the “/app” folder. Afterward, all front-end files are copied to this folder and the project is built with its dependencies.
* Moving on to the second part, we run the files after the build process with the help of the Nginx image.
* The files built in the previous stage are copied to the appropriate directory in the Nginx container.
* Then, the default configurations of Nginx are removed and our own configurations (in the nginx folder of book-portal-fe folder) are included in their place.
* Finally, [the front-end is run](https://stackoverflow.com/a/28099946/12497995) by allowing the Nginx container to listen to port 3000. Now the front-end project can be accessed via localhost:3000. But it’s not ready to interact yet.

Here, it’s crucial to quickly look inside the “nginx.conf” configuration file located in the nginx folder. Because after the back-end and front-end dockerization processes, our third container, which we will examine, will also use Nginx, but we will benefit from the reverse proxy logic of this container. As a result, the configurations of the third container, the reverse proxy Nginx, and the front-end server Nginx should not be confused.

```
server {  
  
  listen 3000;  
  
  location / {  
    root   /usr/share/nginx/html;  
    try_files $uri $uri/ /index.html;  
  }  
}
```

The “nginx.conf” file above defines the settings for the front-end server to be served on port 3000. The `location /`block specifies the location of the web pages with the `ROOT`keyword. This is how we ensure that all incoming requests are directed to the relevant folder of FE project. *(Note that we have copied our files into the “/usr/share/nginx/html” directory in the front-end Dockerfile before.)*

The `try_files`keyword is used to determine the order of files to be checked in case of a missing file. The requested file will be sent immediately if it is present. Otherwise, a file ending in $uri/ will be searched first, and if found, it will be sent. The “index.html” file will be sent if it cannot be found as a [fallback](https://stackoverflow.com/a/17800131/12497995). *Although most of the time this configuration step may not be required, it is still beneficial to add them to prevent erroneous redirects.*

> *A point to note: The port in the FE “nginx.conf” file must be the same as the port we specified in the Dockerfile.* [*Otherwise, we will get ERR\_EMPTY\_RESPONSE error*](/bb-tutorials-and-thoughts/how-to-serve-react-application-with-nginx-and-docker-9c51ac2c50ba)*.*

Well, that was quite the explanation! But hey, at least now we’re all back-end/front-end Docker experts, right? 😎

### Dockerizing reverse proxy (Nginx)🔀

![]()

Finally, let’s dockerize our Nginx container, which will provide us with the [reverse proxy logic](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/) required for the proper routing of requests from the client and our BE container.

```
FROM nginx:alpine  
RUN rm /etc/nginx/conf.d/default.conf  
COPY ./nginx.conf /etc/nginx/conf.d
```

As with the FE part, dockerizing Nginx projects are pretty simple. After using the appropriate image, it is enough to replace our own configuration file with the configuration in the image. However, it is time to examine the configuration file in which we will build the reverse proxy logic.

```
upstream book-portal-fe {  
    server book-portal-fe:3000;  
}  
  
upstream book-portal-be {  
    server book-portal-be:8080;  
}  
  
  
server {  
  
  listen 80;  
  
    location / {  
        proxy_pass http://book-portal-fe;  
    }  
  
  location /api/v1/ {  
      proxy_pass http://book-portal-be;  
      proxy_http_version 1.1;  
      proxy_set_header Upgrade $http_upgrade;  
      proxy_set_header Connection 'upgrade';  
      proxy_set_header Host $host;  
      proxy_cache_bypass $http_upgrade;  
   }  
  
  error_page   500 502 503 504  /50x.html;  
  
  location = /50x.html {  
    root   /usr/share/nginx/html;  
  }  
  
}
```

The `upstream`directive specifies a set of servers that the `proxy_pass` directive later in the file can use as references. There are two upstreams defined in this situation: `book-portal-fe` and `book-portal-be`. `book-portal-fe` and `book-portal-be` both refer to servers that are listening on port 3000 and 8080, respectively.

You specify a virtual server’s configuration in the `server`block. The server in this instance listens on port 80.

The `location` directive defines a context in which the following directives apply. In this case, the first location directive matches any requests that don't match the `/api/v1/` context. The `proxy_pass` directive forwards these requests to the `book-portal-fe` upstream.

The second location directive matches any requests that start with `/api/v1/`. The `proxy_pass` directive forwards these requests to the `book-portal-be` upstream. The `proxy_http_version`, `proxy_set_header`, and `proxy_cache_bypass` directives are used to set headers and pass the appropriate information along with the request.

The `error_page` directive specifies a custom error page for any of the listed HTTP error codes. In this case, the error page is `/50x.html`.

Finally, the last location directive specifies where to find the custom error page. In this case, the file is located in `/usr/share/nginx/html`.

*The configurations mentioned in the last 2 steps may not be preferred again, but it is okay to use them.*

With this explanation, we are now the Nginx configuration master. 😜

**For successful reverse proxy redirects**, the RequestMapping parameters of the controllers on the Spring Boot project must be like this:

```
@RestController  
@RequestMapping("/api/v1/authors")  
@PreAuthorize("hasRole('ROLE_ADMIN')")  
public class AuthorController {  
#--
```

Also, requests on the React JS project must be sent in this way:

```
import axios from "axios";  
  
export default class AuthorService {  
  
  getAuthorByEmail = (authorName) => {  
    return axios.get(`/api/v1/authors/by-author-name?authorName=${authorName}`);  
  };  
#--
```

### Containerizing projects with docker-compose: Summoning Dockerfiles 🧟

So far we have created a Dockerfile for each project and now we are ready to launch the application with docker-compose.

```
version: "3"  
services:  
  book-portal-be:  
    build: ./book-portal-be  
    container_name: "book-portal-be"  
  
  book-portal-fe:  
    build: ./book-portal-fe  
    container_name: "book-portal-fe"  
    depends_on:  
      - book-portal-be  
  proxy:  
    build: ./nginx  
    container_name: "book-portal-proxy"  
    restart: always  
    ports:  
      - "80:80"
```

We have defined 3 different services.

* First of all, we create the container responsible for the running of the BE part with the Dockerfile in the relevant file directory for our back-end project.
* Then, we create and run the FE container with the relevant Dockerfile for the front-end project. This service [depends on](https://docs.docker.com/compose/compose-file/05-services/#depends_on) the book-portal-be service. Thus, if there is a problem in running the back-end container, this service will be affected.
* Finally, the proxy service is built using the Dockerfile located in the ./nginx directory. It is named “book-portal-nginx” and is responsible for running the Nginx server as a reverse proxy. This service is set to [restart always](https://serverfault.com/a/884823) and maps port 80 of the host to port 80 of the container.

The services are defined in the order they need to be started: book-portal-be, book-portal-fe, and proxy. The proxy service depends on the other two services to be started first, and **Docker Compose will automatically start them in the correct order**.

Now, let’s start **cmd** in the parent folder where all the projects of our application are located and run the application with that magical command!

![]()

*Open sesame…* oops, not that one:

> docker-compose up

![]()

After downloading the necessary images (which took a while) from the DockerHub registry with the `FROM`commands in the Dockerfile files:

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Here is our docker-compose **stack** (containers series), let’s go to the proxy port and do our first contact with our application.

Press enter or click to view image in full size

![]()

Ta daa, here is the application. Let’s try to log in and end this article, for now, to move on to part 2.

Press enter or click to view image in full size

![]()

## Conclusion

In this part, we completed the dockerizing of our full-stack application and we were able to launch the application locally with Docker.

In the next part of our article, we will send the images that we have created and used in our local as containers, to the DockerHub registry. Next, we will create an instance with the EC2 service on Amazon Web Services, make the necessary installations on this machine, and try to run our images after fetching them from DockerHub. See you in the next part!

> It’s like our app is slowly moving away from our local environment, right? :)

Press enter or click to view image in full size

![]()