---
title: "Dockerizing Turborepo Remix Application"
url: https://medium.com/p/fca679002c23
---

# Dockerizing Turborepo Remix Application

[Original](https://medium.com/p/fca679002c23)

Press enter or click to view image in full size

![]()

# Dockerizing Turborepo Remix Application

[![Joud W. Awad](https://miro.medium.com/v2/resize:fill:64:64/1*90R_KzJMLZmqoFWEeCHlCA.png)](/?source=post_page---byline--fca679002c23---------------------------------------)

[Joud W. Awad](/?source=post_page---byline--fca679002c23---------------------------------------)

9 min read

·

Oct 17, 2024

--

Listen

Share

More

Recently, I had the opportunity to work with a technology that I find particularly impressive: Turborepo. Turborepo is an incremental bundler and build system optimized for JavaScript and TypeScript, written in Rust.

During this project, we were tasked with dockerizing one of our applications within the repository, specifically a Remix application. In this article, I will guide you through the process I used to achieve this, demonstrating how we leveraged the power of Turborepo in conjunction with Docker to build a final image with minimal size.

> For the complete code and further details, check out my [GitHub repo](https://github.com/JoudAwad97/turborepo-remix-dockerized-app).

## Prerequisites

* Ensure that you have the Turborepo CLI installed. If it is not already installed, please refer to the [Turborepo documentation](https://turborepo.org/docs/getting-started) for detailed installation instructions.

## Understanding The Turborepo Structure

Before we delve into building our Docker image, it is essential to understand the structure of a typical Turborepo project. A standard project would have the following high-level structure:

```
turborepo-remix-app/  
│  
├── package.json  
├── package-lock.json  
├── turbo.json  
├── apps/  
│   ├── docs/  
│   │   └── package.json  
│   │       ... other related code files  
│   └── web/ (Remix App)  
│       └── package.json  
│           ... other related code files  
└── packages/  
    └── ui/  
        └── package.json  
            ... other related code files
```

There are two main directories to focus on: apps and packages.

* **apps**: This directory contains our repository applications. Each folder within it represents a separate application, each with its own package.json and related files. In our case, the `/web` directory contains our "Remix" application.
* **packages**: This directory holds all the shared components or utilities used across our projects within the Turborepo.

Understanding this structure is crucial as it helps us efficiently manage and build our applications using Turborepo.

## Understanding Turborepo Commands

Before we begin writing our Dockerfile, it is important to familiarize ourselves with a few key commands provided by Turborepo. We will focus primarily on the `prune` command. According to the Turborepo documentation, this command:

Generates a partial monorepo for a target package. The output will be placed into a directory named out containing the following:

> - The full source code of all internal packages needed to build the target “app”.
>
> - A pruned lockfile containing the subset of the original lockfile needed to build the target “app”.
>
> - A copy of the root package.json.so if we run the command `turbo prune web --docker` with the previous structured project we mentioned we get an output that looks something like this in a folder called `out`

For example, running the command `turbo prune web --docker` on the previously mentioned project structure will produce an output similar to the following in a folder named out:

```
turborepo-remix-app/  
├── out/  
│   ├── package-lock.json  
│   ├── full/  
│   │   ├── apps/  
│   │   │   └── web/  
│   │   │       └── package.json  
│   │   │       ... other related code files  
│   │   ├── package.json (from repo root)  
│   │   ├── packages/  
│   │   │   └── ui/  
│   │   │       └── package.json  
│   │   │       ... other related code files  
│   ├── json/  
│   │   ├── apps/  
│   │   │   └── web/  
│   │   │       └── package.json  
│   │   ├── package.json (from repo root)  
│   │   ├── packages/  
│   │   │   └── ui/  
│   │   │       └── package.json
```

From the above structure, we can observe the following:

* A folder named `json` containing the pruned workspace's package.json files.
* A folder named `full` containing the pruned workspace's full source code for the internal packages needed to build the target.
* A pruned lockfile containing the subset of the original lockfile needed to build the target.

Understanding these outputs is crucial for efficiently managing and building our applications using Turborepo.

## 🐳 Let us Dockerize It 🐳

Now that we have a solid understanding of how Turborepo works, it is time to start writing our Dockerfile to dockerize our Remix application. Note that this approach can be applied to any JavaScript framework, not just Remix.

In Turborepo, we add the Dockerfile at the application level. For our case, we will add the Dockerfile at the following path: `apps/web/dockerfile`.

Another important aspect to consider is the use of multi-stage build steps. This approach allows us to make our code more efficient and significantly reduce the final image size.

### Stage One: “**Base Stage**”

```
FROM node:20-alpine3.19 as base
```

* **Platform Specification**: The Dockerfile starts by specifying the node version `node:20-alpine3.19` that is used by the image as the base. This ensures compatibility and a lightweight environment.
* **Label**: This stage is labeled as `base` for easy reference in subsequent stages.

### Stage Two: “Prune”

```
# Generate a partial monorepo for a target package. The output will be placed into a directory named "out"  
FROM base AS prune  
RUN apk update  
RUN apk add --no-cache libc6-compat  
  
WORKDIR /app  
RUN npm install turbo --global  
COPY . .  
RUN turbo prune web --docker
```

* **Base Inheritance**: The `prune` stage inherits from the `base` stage.
* **Package Updates and Installation**: It updates the Alpine package index and installs `libc6-compat` to ensure compatibility with certain binaries.
* **Working Directory**: Sets the working directory to `/app`.
* **Turbo Installation**: Installs Turbo globally using npm.
* **Copying Files**: Copies the entire project directory into the container.
* **Turbo Prune**: Executes `turbo prune web --docker` to generate a partial monorepo for the `web` package, placing the output into a directory named (discussed previously in the “Understanding Turborepo Commands” Section)

### Stage Three: “Dev Installer”

```
# This Step only installs Production & Dev dependencies  
FROM base AS installer  
RUN apk update  
RUN apk add --no-cache libc6-compat  
WORKDIR /app  
# the /out/json contain the package.json file that is used to install packages related to the "web"   
COPY --from=prune /app/out/json/ .  
  
RUN npm install
```

* **Base Inheritance**: The `installer` stage inherits from the `base` stage.
* **Package Updates**: Updates the Alpine package index.
* **Package Installation**: Installs `libc6-compat` without caching to keep the image size small.
* **Working Directory**: Sets the working directory to `/app`.
* **Copying Files**: Copies the package.json file from the `prune` stage's output directory to the current working directory. This file contains the dependencies required for the `web` package.
* **Dependency Installation**: Runs `npm install` to install both production and development dependencies specified in the package.json file.

### Stage Four: “Production Installer”

```
# This Step only installs Production dependencies only  
FROM base AS installer-production  
RUN apk update  
RUN apk add --no-cache libc6-compat  
WORKDIR /app  
# the /out/json contain the package.json file that is used to install packages related to the "web"   
COPY --from=prune /app/out/json/ .  
  
RUN npm install --only=production
```

* **Base Inheritance**: The `installer-production` stage inherits from the `base` stage.
* **Package Updates**: Updates the Alpine package index.
* **Package Installation**: Installs `libc6-compat` without caching to keep the image size small.
* **Working Directory**: Sets the working directory to `/app`.
* **Copying Files**: Copies the package.json file from the `prune` stage's output directory to the current working directory. This file contains the dependencies required for the `web` package.
* **Dependency Installation**: Runs `npm install --production` to install only production dependencies specified in the package.json file.

***A question may arise about why we have two installers (Development and Production).***

The answer is that we want to separate these two steps to optimize our build process. The Development installer is used during the build stage, while the Production installer is used for the final image. More information on this will be provided in the subsequent stages.

### Stage Five: “Builder”

```
# Uses the dev & production dependencies to make a production build  
FROM base AS builder  
WORKDIR /app  
COPY --from=installer /app/node_modules /app/node_modules  
  
# the /out/full contain the code files that is used to run the package "web"   
COPY --from=prune /app/out/full/ .  
  
# We assume that you have a "build" command in your root package.json file  
# The --filter is used to tell which of the "apps" to run this command against  
RUN npx turbo build --filter=web
```

* **Base Inheritance**: The `builder` stage inherits from the `base` stage.
* **Working Directory**: Sets the working directory to `/app`.
* **Copying Files**: Copies the development packages pruned files from the `prune` stage's output directory to the current working directory.
* **Build Command**: Executes the `npx turbo build`command to build the production version of the `web` package.

### Stage Six: “Runner”

```
# runner will use the builder output, and use only the node_modules for production to reduce the size of the final image  
FROM base AS runner  
WORKDIR /app  
  
# Don't run production as root  
RUN addgroup --system --gid 1001 web-group  
RUN adduser --system --uid 1001 web-user  
USER web-user  
  
# Copy Production dependencies, build and public dirctories  
COPY --from=installer-production --chown=web-user:web-group /app/node_modules /app/node_modules  
COPY --from=prune   --chown=web-user:web-group /app/out/json/ .  
COPY --from=builder --chown=web-user:web-group /app/apps/web/build /app/apps/web/build  
COPY --from=builder --chown=web-user:web-group /app/apps/web/public /app/apps/web/public  
  
WORKDIR /app/apps/web  
  
CMD ["npm", "run", "start"]
```

1. **Base Image**: The runner stage starts from the `base` image, which is a minimal image containing only the necessary runtime dependencies.
2. **Working Directory**: The working directory is set to `/app`, where the application code and dependencies will reside.
3. **Non-Root User Setup**:

* A system group `web-group` with GID 1001 is created.
* A system user `web-user` with UID 1001 is created and added to `web-group`.
* The `USER` directive switches to `web-user` to avoid running the application as the root user, enhancing security.

4. **Copying Dependencies and Build Artifacts**:

* Production dependencies are copied from the `installer-production` stage to `/app/node_modules`.
* JSON output files are copied from the `prune` stage to the current directory.
* Build and public directories are copied from the `builder` stage to their respective locations in the `/app/apps/web` directory.
* All copied files and directories are assigned ownership to `web-user:web-group` to ensure proper permissions.

5. **Final Working Directory**: The working directory is changed to `/app/apps/web`, where the main application resides.

6. **Command to Start the Application**: The `CMD` directive specifies the command to start the application using `npm run start`.

### Putting it all together

Now that we have discussed each step in detail, it is time to view the full source code.

```
FROM node:20-alpine3.19 as base  
  
# Generate a partial monorepo for a target package. The output will be placed into a directory named "out"  
FROM base AS prune  
RUN apk update  
RUN apk add --no-cache libc6-compat  
  
WORKDIR /app  
RUN npm install turbo --global  
COPY . .  
RUN turbo prune web --docker  
  
# Responsible for creating an authentication between our dockerfile and the private gituhb repositories  
FROM base AS authentication  
WORKDIR /app  
# This Step only installs Production & Dev dependencies  
FROM base AS installer  
RUN apk update  
RUN apk add --no-cache libc6-compat  
WORKDIR /app  
# the /out/json contain the package.json file that is used to install packages related to the "web"   
COPY --from=prune /app/out/json/ .  
  
RUN npm install  
  
# This Step only installs Production dependencies only  
FROM base AS installer-production  
RUN apk update  
RUN apk add --no-cache libc6-compat  
WORKDIR /app  
# the /out/json contain the package.json file that is used to install packages related to the "web"   
COPY --from=prune /app/out/json/ .  
  
RUN npm install --only=production  
  
# Uses the dev & production dependencies to make a production build  
FROM base AS builder  
WORKDIR /app  
COPY --from=installer /app/node_modules /app/node_modules  
  
# the /out/full contain the code files that is used to run the package "web"   
COPY --from=prune /app/out/full/ .  
  
RUN npx turbo build --filter=web  
  
# runner will use the builder output, and use only the node_modules for production to reduce the size of the final image  
FROM base AS runner  
WORKDIR /app  
  
# Don't run production as root  
RUN addgroup --system --gid 1001 web-group  
RUN adduser --system --uid 1001 web-user  
USER web-user  
  
# Copy Production dependencies, build and public dirctories  
COPY --from=installer-production --chown=web-user:web-group /app/node_modules /app/node_modules  
COPY --from=prune   --chown=web-user:web-group /app/out/json/ .  
COPY --from=builder --chown=web-user:web-group /app/apps/web/build /app/apps/web/build  
COPY --from=builder --chown=web-user:web-group /app/apps/web/public /app/apps/web/public  
  
WORKDIR /app/apps/web  
  
CMD ["npm", "run", "start"]
```

To build this Docker image, run the following command from the root of the Turborepo:

`docker build -t <image-tag> -f ./apps/web/dockerfile .`

## Conclusion

Dockerizing any application can be a challenging task. It is crucial to understand the main aspects of your development workflow and how things work. Once you reach that understanding, you can start building a Dockerfile that adheres to the rules of your repository.

In this blog post, we walked you through the process of dockerizing an application in Turborepo. While we specifically covered a Remix application, the tools and techniques discussed here can be applied to any other framework with minimal adjustments.

## References

* <https://turbo.build/>

## Follow Me For More Content

If you made it this far and you want to receive more content similar to this make sure to follow me on [Medium](https://medium.com/@joudwawad) and on [Linkedin](https://www.linkedin.com/in/joud-awad/)