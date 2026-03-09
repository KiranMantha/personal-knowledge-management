---
title: "End to End Deployment Automation to AWS Using GitHub Actions"
url: https://medium.com/p/b61d28fb3c61
---

# End to End Deployment Automation to AWS Using GitHub Actions

[Original](https://medium.com/p/b61d28fb3c61)

# End to End Deployment Automation to AWS Using GitHub Actions

[![Muna Bhattarai](https://miro.medium.com/v2/resize:fill:64:64/1*by4isKAsu784MEcnQbqyJQ.jpeg)](https://medium.com/@munashree?source=post_page---byline--b61d28fb3c61---------------------------------------)

[Muna Bhattarai](https://medium.com/@munashree?source=post_page---byline--b61d28fb3c61---------------------------------------)

16 min read

·

Dec 18, 2025

--

Listen

Share

More

Press enter or click to view image in full size

![]()

## Introduction

Not too long ago, deploying an application to production was a manual nightmare. Engineers would spend entire weekends copying files to servers, restarting services, and hoping nothing would break. When something went wrong (and it often did), they had to do everything again from scratch.

Fast forward to today, and things are very different.

Modern deployment doesn’t require late nights or manual file transfers. You write code, push it to GitHub, and your application updates itself in production.

No clicking through server dashboards.   
No SSH sessions at midnight.

This matters more than you might think.

Imagine you’re working on a student project with your team. Someone finds a bug right before a demo.

**Without automation, fixing it means:**

* Building the application on your laptop
* Uploading files somewhere
* Hoping you didn’t miss anything
* Testing everything manually
* Repeating if something breaks

**With automation, it’s different:**

* Fix the bug
* Push to GitHub
* Wait 5 minutes
* Done

Press enter or click to view image in full size

![]()

In this blog, I’ll show you exactly how to set this up. We’ll build a **real application** and deploy it to **AWS**.

By the end, you’ll understand how companies deploy software multiple times a day without breaking things.

### **Get the Code**

The complete application code for this project is available on GitHub:

*👉* [/End-to-End-Deployment-Automation-to-AWS-using-GitHub-Actions](https://github.com/GitHer-Muna/End-to-End-Deployment-Automation-to-AWS-using-GitHub-Actions)

You can clone this repository and follow along with this blog.

### What You will Need

Before we start, make sure you have:

* A GitHub account
* An AWS account (free tier is fine)
* Basic familiarity with Git commands
* Node.js installed on your laptop (for local testing)
* Docker installed (optional, but helpful)

Don’t worry if you’re not an expert in any of these. I’ll explain everything as we go.

## What We Are Building

We’re going to build and deploy a **Campus Event Management System**.

It’s a web application where students can:

* Browse upcoming campus events
* Filter by category (hackathons, workshops, tech talks, etc.)
* See registration status and availability
* Find your Registered event and unregister if needed

**I chose this example for a few reasons:**

1. First, it’s realistic. Every university needs something like this. You’re not building a “hello world” example that teaches nothing useful.
2. Second, it has both a frontend and a backend. This is important because real applications always have multiple parts that need to work together. You’ll learn how to handle both.
3. Third, it’s simple enough to understand quickly, but complex enough to show you real deployment challenges.
4. The application itself is built with React on the frontend and Node.js with Express on the backend. If you don’t know these technologies deeply, that’s fine.

> The focus here is on deployment, not application development.

Press enter or click to view image in full size

![]()

*The final application, students can browse and filter campus events*

## High-Level Architecture

Before we dive into the details, let me show you the complete architecture. Understanding this picture will help everything else make sense.

```
┌─────────────────────────────────────────────────────────────────┐  
│                          YOUR LAPTOP                            │  
│                                                                 │  
│  ┌──────────────┐                                              │  
│  │  Git Push    │  git push origin main                        │  
│  └──────┬───────┘                                              │  
└─────────┼──────────────────────────────────────────────────────┘  
          │  
          ▼  
┌─────────────────────────────────────────────────────────────────┐  
│                           GITHUB                                │  
│                                                                 │  
│  ┌──────────────┐         ┌─────────────────┐                 │  
│  │ Code Repo    │────────>│ GitHub Actions  │                 │  
│  └──────────────┘         └────────┬────────┘                 │  
└────────────────────────────────────┼──────────────────────────┘  
                                      │  
                                      │ Build & Push  
                                      ▼  
┌─────────────────────────────────────────────────────────────────┐  
│                        AMAZON ECR                               │  
│                   (Container Registry)                          │  
│                                                                 │  
│  ┌────────────────┐           ┌────────────────┐              │  
│  │ Backend Image  │           │ Frontend Image │              │  
│  │  (Node.js)     │           │   (React)      │              │  
│  └────────────────┘           └────────────────┘              │  
└─────────────────────────────────────────────────────────────────┘  
                                      │  
                                      │ Pull Images  
                                      ▼  
┌─────────────────────────────────────────────────────────────────┐  
│                      AMAZON ECS (FARGATE)                       │  
│                                                                 │  
│  ┌─────────────────────────────────────────────────────┐      │  
│  │            Application Load Balancer                │      │  
│  └──────────────────┬─────────────────┬────────────────┘      │  
│                     │                 │                        │  
│          ┌──────────▼──────┐    ┌────▼─────────────┐         │  
│          │  Backend Tasks  │    │  Frontend Tasks  │         │  
│          │   (Containers)  │    │   (Containers)   │         │  
│          └─────────────────┘    └──────────────────┘         │  
│                                                                 │  
└─────────────────────────────────────────────────────────────────┘  
                                      │  
                                      │ Users Access  
                                      ▼  
                            🌐 Production URL
```

### Let me break down what each component does:

1. **Your Laptop :** This is where you write code. When you’re happy with your changes, you run `git push`.
2. **GitHub** **:** GitHub stores your code. When you push, GitHub Actions automatically triggers.
3. **GitHub Actions** **:** This is the automation engine. It reads your workflow file and executes the build process. It builds Docker containers for both frontend and backend.
4. **Amazon ECR (Elastic Container Registry)** **:** Think of this as a secure storage for your Docker containers. GitHub Actions pushes the built containers here.
5. **Amazon ECS (Elastic Container Service) :** This is where your application runs. ECS pulls containers from ECR and executes them using Fargate.
6. **Fargate:** Itis the serverless compute engine. You don’t manage any servers; AWS does it all.
7. **Application Load Balancer:** This sits in front of your application and distributes incoming traffic across your containers.

Press enter or click to view image in full size

![]()

## **The Complete Flow**

When you push code to GitHub:

1. GitHub receives your code
2. GitHub Actions triggers and builds Docker containers
3. Containers are pushed to Amazon ECR
4. GitHub Actions tells ECS to deploy the new containers
5. ECS pulls the new containers from ECR
6. ECS performs a rolling deployment (gradually replacing old containers with new ones)
7. The load balancer routes traffic to the new containers
8. Your application is now live with the latest code

*Each step happens automatically.*

*You only touch* ***step 1****.* Have some patience 🙂

## Application Overview

Let me break down what our application actually does.

### The Frontend

The frontend is what students see. It’s a clean, simple website built with React. When you open it, you see a list of events. Each event shows:

* The event name
* When (Time) and where (Location) it’s happening
* How many people have registered
* A button to register/unregister after registration

You can filter events by category. If you only want to see hackathons, you click a filter and the list updates.

The frontend talks to the backend through API calls. When the page loads, it asks the backend ***“give me all events”*** and displays what it receives.

Press enter or click to view image in full size

![]()

### The Backend

The backend is a **Node.js server running + Express API**. It’s much simpler than you might think.

**It has one main job:** Send event data when asked. Right now, the events are stored in the code itself (we’re not using a database to keep things simple). In a real system, you’d connect to a database here.

**The backend exposes a few endpoints:**

* `/api/events` - Returns all events
* `/api/events/:id` - Returns one specific event
* `/health` - Confirms the server is running (Health check)

Press enter or click to view image in full size

![]()

That’s it. The backend is just a thin API layer that serves data.

Both the frontend and backend run as **separate containers**. They’re independent but work together to make the application function.

## Dockerizing the Application

Let me explain why we use Docker and what it actually does.

Imagine you built an application on your laptop. It works perfectly. But when your teammate tries to run it, they get errors. Maybe they have a different version of Node.js. Maybe they’re missing a library. Maybe their operating system handles things differently.

Docker solves this by packaging everything your application needs into a container.

Press enter or click to view image in full size

![]()

**The container includes:**

* Your code
* The right version of Node.js
* All libraries and dependencies
* The correct configuration

When someone runs your container, it works exactly the same everywhere. On your laptop, on your teammate’s laptop, on AWS, it doesn’t matter.

**The result:** **same behavior everywhere**.

## **What a Dockerfile Does**

A Dockerfile is like a recipe. It tells Docker how to build your container.

### For our backend, the Dockerfile uses a multi-stage build:

**Stage 1: Builder**

1. Start with Node.js 18 Alpine (a lightweight Linux distribution)
2. Copy package.json files
3. Install production dependencies using `npm ci`
4. Copy the source code

**Stage 2: Production**

1. Start with a fresh Node.js 18 Alpine image
2. Copy the installed dependencies and source code from the builder stage
3. Create a non-root user for security
4. Expose port 3000
5. Set up a health check endpoint
6. Define the command to start the server

```
# Build stage  
FROM node:18-alpine AS builder  
  
WORKDIR /app  
  
# Copy package files  
COPY package*.json ./  
  
# Install dependencies  
RUN npm ci --only=production  
  
# Copy source code  
COPY src ./src  
  
# Production stage  
FROM node:18-alpine  
  
WORKDIR /app  
  
# Copy dependencies and source from builder  
COPY --from=builder /app/node_modules ./node_modules  
COPY --from=builder /app/package*.json ./  
COPY --from=builder /app/src ./src  
  
# Create non-root user  
RUN addgroup -g 1001 -S nodejs && \  
    adduser -S nodejs -u 1001  
  
USER nodejs  
  
# Expose port  
EXPOSE 3000  
  
# Health check  
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \  
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"  
  
# Start application  
CMD ["node", "src/index.js"]
```

### For the frontend:

It’s more complex because we need to build the React app and serve it:

**Stage 1: Builder**

1. Start with Node.js 18 Alpine
2. Copy package.json files
3. Install all dependencies (including dev dependencies needed for building)
4. Copy the entire source code
5. Run `npm run build` to create optimized production files

**Stage 2: Production**

1. Start with Nginx Alpine (a lightweight web server)
2. Copy custom Nginx configuration
3. Copy the built files from the builder stage to Nginx’s web directory
4. Create a non-root user for security
5. Expose port 80
6. Set up a health check
7. Start Nginx to serve the static files

```
# Build stage  
FROM node:18-alpine AS builder  
  
WORKDIR /app  
  
# Copy package files  
COPY package*.json ./  
  
# Install all dependencies (including dev dependencies for build)  
RUN npm ci  
  
# Copy source code  
COPY . .  
  
# Build the application  
RUN npm run build  
  
# Production stage  
FROM nginx:alpine  
  
# Copy custom nginx config  
COPY nginx.conf /etc/nginx/conf.d/default.conf  
  
# Copy built assets from builder stage  
COPY --from=builder /app/dist /usr/share/nginx/html  
  
# Create non-root user  
RUN addgroup -g 1001 -S nginx_group && \  
    adduser -S nginx_user -u 1001 -G nginx_group  
  
# Expose port  
EXPOSE 80  
  
# Health check  
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \  
  CMD wget --quiet --tries=1 --spider http://localhost:80 || exit 1  
  
# Start nginx  
CMD ["nginx", "-g", "daemon off;"]
```

We use multi-stage builds for both containers. This approach has several benefits:

* **Smaller images:** We don’t include build tools in the final container
* **Security:** Only production files are included, reducing attack surface
* **Performance:** Smaller images download and start faster
* **Clean separation:** Build dependencies stay in the build stage

You don’t need to understand every detail of Docker right now.

**The key point is:** Docker turns your application into a portable package that runs the same everywhere.

Press enter or click to view image in full size

![]()

## Setting Up Amazon ECR

ECR stands for Elastic Container Registry. It’s where we store our Docker containers.

Think of it like GitHub, but for containers instead of code. *HAHA!*

**Here’s why we need it:**

When GitHub Actions builds your containers, they exist only on GitHub’s servers temporarily. We need to store them somewhere permanent. We also need ECS to be able to download them later.

**ECR is perfect for this because:**

* It’s secure (you control who can access your containers)
* It’s fast (especially when used with other AWS services)
* It integrates easily with ECS
* You can store multiple versions of your containers

**For our project, we create two repositories in ECR:**

* One for the backend container
* One for the frontend container

Press enter or click to view image in full size

![]()

Each time we push code, GitHub Actions builds new containers and uploads them to ECR. ECS then pulls the latest version from ECR and runs it.

## GitHub Actions CI/CD Pipeline

This is where the magic happens. Let me walk you through what GitHub Actions does.

Press enter or click to view image in full size

![]()

### **What Is GitHub Actions?**

GitHub Actions is a tool built into GitHub that runs code when certain things happen. In our case, it runs **when you push code** to the main branch.

You configure it with a YAML file. This file lives in your repository at `.github/workflows/deploy.yml`. It tells GitHub Actions exactly what to do.

Press enter or click to view image in full size

![]()

*The workflow file that defines our entire deployment process.*

## The Workflow Step by Step

When you push code, here’s what happens:

**Step 1: Trigger**

GitHub notices you pushed to the Push to `main` branch. It checks if there’s a workflow file. There is, so it starts running.

**Step 2: Authentication**

GitHub Actions needs permission to talk to AWS. It uses secrets you’ve stored in GitHub (AWS\_ACCESS\_KEY\_ID and AWS\_SECRET\_ACCESS\_KEY). These secrets are never visible in logs or code, they’re encrypted.

**Step 3: Build Backend Container**

GitHub Actions builds your backend into a Docker container. It reads the Dockerfile, follows the instructions, and creates a container image.

**Step 4: Build Frontend Container**

Same thing for the frontend. Build the React application and package it with Nginx.

**Step 5: Tag the Containers**

Each container gets two tags:

* The commit SHA (like `a1b2c3d`)
* The word `latest`

This lets you track exactly which version of code is in which container.

**Step 6: Push to ECR**

The containers are uploaded to ECR. Now they’re stored safely in AWS.

**Step 7: Update ECS Services**

GitHub Actions tells ECS *“****there are new containers, please deploy them.”*** ECS pulls the new containers from ECR and starts running them.

**Step 8: Wait for Stability**

GitHub Actions waits until ECS confirms everything is running properly. If something goes wrong, you’ll see it in the logs.

**Step 9: Done**

The workflow finishes. Your new code is now live.

Press enter or click to view image in full size

![]()

*GitHub Actions workflow running showing all steps in green.*

Press enter or click to view image in full size

![]()

*GitHub Actions workflow completed successfully. Yay!!*

## About Secrets and Security

You might wonder: ***How does*** ***GitHub Actions access AWS?***

We use something called secrets. In your GitHub repository settings, you add:

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`

These are like a username and password for AWS. GitHub encrypts them and only makes them available to your workflows. They never appear in logs or code.

Press enter or click to view image in full size

![]()

*This is important. Never put AWS credentials directly in your code. Always use secrets.*

### How Long Does This Take?

From the moment you push code to the moment it’s live: about 3 to 5 minutes.

Most of that time is spent building the Docker containers and uploading them to ECR. The actual deployment to ECS is pretty fast.

## Deploying to Amazon ECS with Fargate

Let me explain what happens on the AWS side.

### What Is ECS?

ECS stands for Elastic Container Service. It’s AWS’s service for running Docker containers.

You tell ECS ***“here are my containers, please run them.”*** ECS handles everything else:

* Starting the containers
* Restarting them if they crash
* Distributing traffic between multiple containers
* Updating to new versions without downtime

### What Is Fargate?

Here’s where it gets interesting.

Traditionally, to run containers, you need servers. You’d have to:

* Create EC2 instances (virtual servers)
* Install Docker on them
* Configure them to talk to ECS
* Update and patch them regularly
* Scale them up or down

Press enter or click to view image in full size

![]()

Fargate changes this. **With Fargate,** you don’t manage any servers. You just say ***“run my container”*** and AWS handles everything.

**Fargate = no servers to manage**

No servers to configure. No security updates to install. No capacity planning.

This is what ***“serverless containers”*** means. The containers exist, but you don’t manage the underlying servers.

## How ECS Pulls and Runs Containers

Here’s the process:

1. You define a ***“task definition”*** which is like a blueprint. It says, ***“this is what my application needs to run.”***
2. You create a ***“service”*** that uses that task definition. A service says, ***“keep 2 copies of this task running at all times.”***
3. ECS creates tasks (running containers) based on your task definition.

Press enter or click to view image in full size

![]()

4. When you deploy new code, ECS gradually replaces old tasks with new ones. This is called a rolling deployment.

5. If a container crashes, ECS automatically starts a new one.

Press enter or click to view image in full size

![]()

## The Load Balancer

In front of your ECS tasks, there’s usually a load balancer. This distributes incoming traffic across all running containers.

When users visit your application, they hit the load balancer first. The load balancer picks one of your containers and sends the request there.

**This does two things:**

* If one container is busy, traffic goes to another
* During deployments, traffic gradually shifts from old to new containers

You never notice the deployment happening because the load balancer keeps traffic flowing to healthy containers.

## Final Result

After everything is set up, here’s what your workflow looks like:

You’re working on the application. Maybe you fix a bug or add a new feature. You test it on your laptop. It works.

You commit your changes:

```
git add .  
git commit -m "Fixed event registration bug"  
git push origin main
```

That’s it. You’re done.

GitHub receives the push. Within seconds, you see a yellow dot next to your commit in GitHub. This means the workflow is running.

You can click on it to watch the progress. You’ll see logs showing:

* Building backend container
* Building frontend container
* Pushing to ECR
* Deploying to ECS

After a few minutes, the yellow dot turns green. Your changes are live.

You open the application URL. The bug you fixed is gone. Everything works.

Press enter or click to view image in full size

![]()

If you push code multiple times a day, each push triggers the same process. New containers are built, pushed to ECR, and deployed to ECS automatically.

This is what modern deployment looks like. You focus on writing code. The system handles everything else.

## Common Mistakes and Tips

Let me share some mistakes I see beginners make and how to avoid them.

### **Mistake 1:** Putting AWS Credentials in Code

Never, ever put your AWS access keys in your code or Dockerfile. Always use GitHub Secrets.

I’ve seen people accidentally push credentials to public GitHub repositories. Within minutes, someone finds them and runs up a huge AWS bill.

Use secrets. Always.

### Mistake 2: Not Testing Locally First

Before you push code and trigger a deployment, test it on your laptop first.

Run the backend locally. Make sure it works. Then push.

It’s faster to catch bugs on your laptop than in production.

### Mistake 3: Ignoring Logs

When something goes wrong, the logs tell you what happened. GitHub Actions shows logs for the build process. ECS shows logs for the running containers.

Don’t guess what’s wrong. Read the logs.

### Mistake 4: Not Understanding the Flow

Take time to understand what each part does:

* GitHub Actions builds
* ECR stores
* ECS runs

If you don’t understand where your application is at each stage, debugging becomes very hard.

### Mistake 5: Skipping the Health Checks

Your containers should have health check endpoints (like `/health`). ECS uses these to know if your container is working.

Without health checks, ECS might send traffic to broken containers.

Press enter or click to view image in full size

![]()

## Tips for Success

1. **Start small :** Get one container working before you add the second one.
2. **Use descriptive names :** When you create ECR repositories or ECS services, use clear names. Future you will thank current you.
3. **Keep your Docker images small.** Don’t include unnecessary files. Smaller images build faster and deploy faster.
4. **Monitor your costs :** AWS has a free tier, but it’s easy to go over if you’re not careful. Set up billing alerts.
5. **Document your setup :** Write down what you did. When something breaks six months later, you’ll need those notes.

## What You Learned

If you followed along and built this project, you now know:

1. **About Containers**

You understand why Docker exists and what containers do. You can write a Dockerfile and build an image. You understand multi-stage builds and why they matter.

**2. About CI/CD**

You know what continuous integration and continuous deployment mean. You’ve built a pipeline that automatically deploys your code. You understand the benefits of automation over manual deployment.

**3. About GitHub Actions**

You can write workflow files. You understand triggers, steps, and secrets. You know how to build Docker images and deploy to AWS automatically.

**4. About AWS Services**

You know what ECR, ECS, Fargate, VPC, Security Groups, and Application Load Balancer do. You understand how they work together. You can read CloudFormation templates that define these resources.

**5. About Deployment**

You understand the complete flow from code on your laptop to an application running in the cloud. You know what happens at each step. You understand rolling deployments and zero-downtime updates.

### Real-World Skills

These aren’t dummy examples. This is how real companies deploy software. The principles you learned here apply whether you’re deploying a student project or a production system handling millions of users.

Companies want people who understand this stuff. If you can explain how you set up a CI/CD pipeline to deploy containers to AWS, that’s a valuable skill.

## Conclusion

Deployment automation might seem complex when you first look at it. There are a lot of moving parts: Docker, GitHub Actions, ECR, ECS, Fargate, load balancers, CloudFormation, security groups.

But when you break it down, each piece is doing something simple:

* Docker packages your application
* GitHub Actions builds the packages
* ECR stores them
* ECS runs them

That’s it. Everything else is just details.

Once it works, you’ll never deploy manually again.

The first time you set this up, it will take time. You’ll make mistakes. Things won’t work. That’s normal. Even experienced engineers make mistakes when setting up new systems.

But once it’s working, you’ll wonder how you ever deployed applications manually. Pushing code and watching it automatically go live never gets old.

Start with this project. Get it working. Then think about what else you can build and deploy the same way.

The best way to learn is by doing. So clone the repository, follow the steps, and deploy something to AWS. Break things. Fix them. Learn from the process.

### **Ready to start?**

1. Clone the repository: [*/End-to-End-Deployment-Automation-to-AWS-using-GitHub-Actions*](https://github.com/GitHer-Muna/End-to-End-Deployment-Automation-to-AWS-using-GitHub-Actions)
2. Push this code to your own GitHub repository where you have administrative access to manage secrets.
3. Configure AWS Credentials in GitHub Secrets
4. Simply push any change to the main branch, or manually trigger the workflow with `git push origin main`
5. Deploy your first application to AWS
6. When you’re done experimenting or need to delete all AWS resources to avoid ongoing charges, you can do using GitHub Actions Workflow I have created in my repository with command `gh workfloe rn cleanup.yml`
7. Follow the README guide for complete setup

You’ve got this.🙂

*This blog post accompanies a live tech talk given at AWS Student Community Day Pokhara 2025 by Muna Bhattarai. The complete code is available on my GitHub at* [*https://github.com/*](https://github.com/GitHer-Muna/End-to-End-Deployment-Automation-to-AWS-using-GitHub-Actions)[GitHer-Muna/End-to-End-Deployment-Automation-to-AWS-using-GitHub-Actions](https://github.com/GitHer-Muna/End-to-End-Deployment-Automation-to-AWS-using-GitHub-Actions)*. Feel free to use it, modify it, and learn from it.*