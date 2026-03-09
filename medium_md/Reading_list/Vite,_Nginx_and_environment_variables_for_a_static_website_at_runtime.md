---
title: "Vite, Nginx and environment variables for a static website at runtime"
url: https://medium.com/p/f3d0b2995fc7
---

# Vite, Nginx and environment variables for a static website at runtime

[Original](https://medium.com/p/f3d0b2995fc7)

Press enter or click to view image in full size

![]()

# Vite, Nginx and environment variables for a static website at runtime

[![Dmitrii Pashkevich](https://miro.medium.com/v2/resize:fill:64:64/1*jG9p4QsAq9_lz3WLbsc9OA.jpeg)](/@dipiash?source=post_page---byline--f3d0b2995fc7---------------------------------------)

[Dmitrii Pashkevich](/@dipiash?source=post_page---byline--f3d0b2995fc7---------------------------------------)

6 min read

·

May 17, 2024

--

Listen

Share

More

Hello everyone! My name is Dmitry Pashkevich, and I’m a Frontend developer at Quadcode. Today I’ll share a method for passing environment variables to a statically built website using the [Vite](https://vitejs.dev/) build tool in conjunction with the Nginx web server.

A common task in frontend development is passing environment variables to the application depending on the environment in which the application is running. It seems like a simple task, and everything is described in the [documentation](https://vitejs.dev/guide/env-and-mode) — just place a *.env* file next to it and run the build… on each environment.

It seems like the solution has been found. But this leads to a situation where each environment has a different build process and a different result of this build.

Practice shows that problems arise with the functionality of the build steps. For example, when making changes, settings, scripts, etc. are forgotten to be updated for one of the environments. As a result, we encounter issues with the application itself, as the artifacts also differ.

Thus, it seems logical to obtain a single build artifact for all available environments and be able to pass environment variable values. Therefore, it is easier to troubleshoot one issue with variable values than to investigate build steps as well.

Now, let’s see how to do this using the Vite and Nginx tools as an example.

## Repository Preparation

First, let’s create a project from the template provided by the Vite builder for React + Typescript.

```
npm create vite@latest vite-nginx-dynamic-env-variables-example --   
--template react-ts && cd vite-nginx-dynamic-env-variables-example && npm   
instal
```

## Project Configuration Preparation

After successfully executing the commands, let’s open the resulting project in our favorite IDE and start creating the target solution.

Let’s adjust the file src/vite-env.d.ts. We will add a description of the type of available environment variables to enable [IDE hinting](https://vitejs.dev/guide/env-and-mode.html#intellisense-for-typescript).

```
/// <reference types="vite/client" />  
  
interface ImportMetaEnv {  
    readonly VITE_VERSION: string  
}  
  
interface ImportMeta {  
    readonly env: ImportMetaEnv  
}
```

Now the IDE will provide hints about the available environment variables.

Next, let’s create a file with environment variable templates: *src/shared/projectEnvVariables.ts* and add the following content to it.

```
type ProjectEnvVariablesType = Pick<ImportMetaEnv, 'VITE_VERSION'>  
  
  
// Environment Variable Template to Be Replaced at Runtime  
const projectEnvVariables: ProjectEnvVariablesType = {  
   VITE_VERSION: '${VITE_VERSION}',  
}  
  
  
// Returning the variable value from runtime or obtained as a result of the build   
export const getProjectEnvVariables = (): {  
   envVariables: ProjectEnvVariablesType  
} => {  
   return {  
       envVariables: {  
           VITE_VERSION: !projectEnvVariables.VITE_VERSION.includes('VITE_') ? projectEnvVariables.VITE_VERSION : import.meta.env.VITE_VERSION,  
       }  
   }  
}
```

Next, it is necessary to make a change to the build configuration in *vite.config.ts* so that the file created above has a predictable name after the build stage. To do this, add a section with the configuration for rollup to the config.

```
import { defineConfig } from 'vite'  
import react from '@vitejs/plugin-react'  
  
// https://vitejs.dev/config/  
export default defineConfig({  
   plugins: [react()],  
   build: {  
       rollupOptions: {  
           output: {  
               format: 'es',  
               globals: {  
                   react: 'React',  
                   'react-dom': 'ReactDOM',  
               },  
               manualChunks(id) {  
                   if (/projectEnvVariables.ts/.test(id)) {  
                       return 'projectEnvVariables'  
                   }  
               },  
           },  
       }  
   }  
}
```

In the [manualChunks](https://rollupjs.org/configuration-options/#output-manualchunks) section, we create a custom chunk and save part of its name so that after the build, we can find this file for substituting environment variables.

Let’s make changes to the *src/App.tsx* file to see the values of environment variables.

```
import { getProjectEnvVariables } from "./shared/projectEnvVariables.ts";  
  
const { envVariables } = getProjectEnvVariables()  
  
function App() {  
 return (  
     <>  
         <h1>VITE_VERSION</h1>  
         <div>{envVariables.VITE_VERSION}</div>  
  
         <hr />  
  
         <h2>import.meta.env.VITE_VERSION</h2>  
         <div>{import.meta.env.VITE_VERSION}</div>  
     </>  
 )  
}  
  
export default App
```

Next, let’s run the build to make sure that we obtain the necessary chunk for substituting variables after the build stage.

```
npm run build
```

After the build is complete, navigate to the *dist/assets* directory. You will see that a chunk named *projectEnvVariables\**, which we specified in the configuration above, exists.

![]()

Next, let’s conduct a series of experiments.

For ease of understanding that the desired build result is obtained, each build will be performed with a specified environment variable. This will visually verify the condition for returning the value of the environment variable in the *getProjectEnvVariables* function.

For the first experiment, create a *.env* file in the project root with the following contents.

```
VITE_VERSION=dev
```

Let’s start the project build and the mode to view the build results.

```
npm run build && npm run preview
```

Upon navigating to <http://localhost:4173/>, you will see two identical values of the variable read from the config and directly from the environment variable.

Press enter or click to view image in full size

![]()

For the second experiment, let’s replace the variable in the *dist/assets/projectEnvVariables-wa84hTgi.js* file, which was generated after building the application. Replace the line with the value ${VITE\_VERSION} with *dev\_from\_env* in this file. After refreshing the page in the browser, you will get the updated version of the variable on the screen, read from the config *getProjectEnvVariables*.

Press enter or click to view image in full size

![]()

Everything works as expected! It’s time to automate variable substitution.

## Preparing Docker + Nginx Configuration

We’ll demonstrate the automation of variable substitution using a Docker container containing the Nginx web server, which executes i[nitialization scripts](https://www.nginx.com/resources/wiki/start/topics/examples/initscripts/) before startup, and substitutes environment variables using [envsubst](https://www.gnu.org/software/gettext/manual/html_node/envsubst-Invocation.html).

Let’s create a .docker directory in the project root with the configuration contents for the Nginx web server that will serve the application. A complete example of the Nginx configuration can be found in the [repository](https://github.com/dipiash/vite-nginx-dynamic-env-variables-example), and below is the bash code of the *.docker/app/nginx/init-scripts/100-init-project-env-variables.sh* file, which replaces the environment variables.

```
#!/usr/bin/env sh  
  
set -ex  
  
  
# Find the file where environment variables need to be replaced.  
projectEnvVariables=$(ls -t /usr/share/nginx/html/assets/projectEnvVariables*.js | head -n1)  
  
# Replace environment variables  
envsubst < "$projectEnvVariables" > ./projectEnvVariables_temp  
cp ./projectEnvVariables_temp "$projectEnvVariables"  
rm ./projectEnvVariables_temp
```

Next, in the project root, create a Dockerfile with the following content, which describes the application build and runs the Nginx web server to serve the static files.

```
FROM node:20-alpine as builder  
  
WORKDIR /app  
  
COPY package.json package-lock.json ./  
  
RUN npm ci  
  
COPY . .  
  
ARG NODE_ENV=production  
ENV NODE_ENV=${NODE_ENV}  
  
RUN npm run build  
  
FROM nginx:alpine  
  
ARG VITE_VERSION=dev  
ENV VITE_VERSION=${VITE_VERSION}  
  
ARG PORT=80  
ENV NGINX_PORT=${PORT}  
ENV NGINX_HOST=localhost  
  
EXPOSE ${PORT}  
  
COPY .docker/app/nginx/nginx.conf /etc/nginx/nginx.conf  
COPY .docker/app/nginx/conf.d/ /etc/nginx/conf.d/  
COPY .docker/app/entrypoint.sh /entrypoint.sh  
COPY .docker/app/nginx/init-scripts/ /docker-entrypoint.d/  
  
WORKDIR /usr/share/nginx/html  
  
COPY --from=builder /app/dist ./
```

Next, let’s build the container.

```
docker build -t   
vite-nginx-dynamic-env-variables-example .
```

Next, let’s run the created container with a new value for the environment variable available in the application.

```
docker run -p 81:80 -e VITE_VERSION=FROM_NGINX   
vite-nginx-dynamic-env-variables-example
```

Upon navigating to <http://127.0.0.1:81> , we see that the environment variable is initialized with the current value, while the directly read environment variable remains with the old value.

Press enter or click to view image in full size

![]()

## Conclusion

This way, environment variables can be substituted into a statically built application at runtime, allowing for a unified build across all environments.

The code can be found in [the repository](https://github.com/dipiash/vite-nginx-dynamic-env-variables-example).