---
title: "Deploy React Application using Tekton Pipelines"
url: https://medium.com/p/b639be5104dc
---

# Deploy React Application using Tekton Pipelines

[Original](https://medium.com/p/b639be5104dc)

# Deploy React Application using Tekton Pipelines

[![Vinamra Jain](https://miro.medium.com/v2/resize:fill:64:64/0*EpYIMtnwbom_WcUq.jpg)](/?source=post_page---byline--b639be5104dc---------------------------------------)

[Vinamra Jain](/?source=post_page---byline--b639be5104dc---------------------------------------)

5 min read

·

Apr 5, 2021

--

2

Listen

Share

More

Press enter or click to view image in full size

![]()

## What is Tekton?

[Tekton](https://tekton.dev/) is a powerful and flexible open-source framework for creating CI/CD systems, allowing developers to build, test, and deploy across cloud providers and on-premise systems. It provides the primitive blocks necessary to build your own CI/CD workflows. It is one of the incubating projects from [CD Foundation](https://cd.foundation/). In this post we’ll be building a CI/CD Pipeline from scratch for your React application.

In this blog I will be deploying Tekton Hub UI and the source code is present [here](https://github.com/tektoncd/hub/tree/main/ui).

### Step 1: Install Kubernetes

Since Tekton is totally based on Kubernetes so we’ll start by first creating Kubernetes cluster on your system. We can install kubernetes using [minikube](https://minikube.sigs.k8s.io/docs/start/) or [kind](https://kind.sigs.k8s.io/docs/user/quick-start/). You should also install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) so that you can interact with the kubernetes cluster.

We can now start our cluster using the following command:

```
$ minikube start --cpus=4 --memory=12g
```

I have kept the cpu count as 4 and memory as 12GB. You can change it as per your convenience or simply execute the command ***minikube start*** which will use default values.

Also enable the ingress controller by following the guide from [here](https://kubernetes.io/docs/tasks/access-application-cluster/ingress-minikube/).

### Step 2: Install Tekton Pipelines

Now that we have cluster up and running, let’s install Tekton Pipelines (the core project). To install we need to execute the following kubectl command:

```
$ kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
```

If you are using an OpenShift cluster and want to install the latest Pipelines then please follow the following process:

```
$ oc new-project tekton-pipelines  
$ oc adm policy add-scc-to-user anyuid -z tekton-pipelines-controller  
$ oc adm policy add-scc-to-user anyuid -z tekton-pipelines-webhook  
$ oc apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.notags.yaml
```

Verify that the Pipelines Controller and Webhook pods are in running state by executing the command below

```
$ kubectl get pods -n tekton-pipelines     
NAME                                           READY   STATUS    RESTARTS   AGE  
tekton-pipelines-controller-749d876cf8-n547t   1/1     Running   0          50s  
tekton-pipelines-webhook-7f9f848664-m6bkc      1/1     Running   0          50s
```

### Step 3: Install tkn CLI

You can use *kubectl* or *oc* CLI as well to interact with Tekton but I’ll be showing the use of *tkn* CLI to install resuable Tasks from [tektoncd/catalog](https://github.com/tektoncd/catalog) which contains a collection of resuable Tekton resources which we can reuse directly from there instead of writing our own.

You can install *tkn* CLI from [here](https://github.com/tektoncd/cli#installing-tkn) depending on the OS and Arch which you are using. After the successful installation you can check the version by

```
$ tkn version  
Client version: 0.17.0  
Pipeline version: v0.22.0
```

### Step 4: Install Tasks from Catalog

Tasks which we are going to use in our Pipeline are:-

* git-clone to clone the source code

```
$ tkn hub install task git-clone --version 0.2
```

* npm to run tests

```
$ tkn hub install task npm --version 0.1
```

* codecov for code coverage

```
$ tkn hub install task codecov --version 0.1
```

* buildah to build and push the image to container registry

```
$ tkn hub install task buildah --version 0.2
```

* kubernetes-actions to check whether there is an existing deployment or not.

```
$ tkn hub install task kubernetes-actions --version 0.2
```

you can now list the installed *Tasks*

```
$ tkn task list  
NAME                 DESCRIPTION              AGE  
buildah              Buildah task builds...   4 minutes ago  
codecov              This task publishes...   4 minutes ago  
git-clone            These Tasks are Git...   4 minutes ago  
kubernetes-actions   This task is the ge...   4 minutes ago  
npm                  This task can be us...   4 minutes ago
```

### Step 5: Create and Install the UI Pipeline

A `Pipeline` is a collection of `Tasks` that you define and arrange in a specific order of execution as part of your continuous integration flow.

The ui-pipeline will clone the source code, install required *npm* dependencies and store them in the external [PVC](https://kubernetes.io/docs/concepts/storage/persistent-volumes/). After this a few tests are run and if all the tests are green then code coverage will be uploaded to [codecov](https://about.codecov.io/). Also after successful completion of tests, the pipeline will start to build and push the container image to image registry. When the image is pushed to desired registry then the CI will check whether hub deployment exists or not. If it doesn’t exists then it create the required secrets and the deployment else it will patch the recently created image to the existing deployment. Below is the visualisation and code of above explained Pipeline :-

Press enter or click to view image in full size

![]()

```
$ kubectl apply --filename ui-pipeline.yaml
```

### Step 6: Create the Secrets and ServiceAccount

Create the necessary secrets which will upload the coverage report to codecov and push the image to desired registry.

Edit the above file with your credentials and apply the file

```
$ kubectl apply --filename secrets-and-sa.yaml
```

Also create the appropriate Role and RoleBinding so that we can deploy on the current cluster

```
$ kubectl create role hub-pipeline \     
--resource=deployment,services,pvc,job \      
--verb=create,get,list,delete,patch   
$ kubectl create rolebinding hub-pipeline \      
--serviceaccount=default:quay-login \      
--role=hub-pipeline
```

### Step 7: Create the PipelineRun

A `PipelineRun` allows you to instantiate and execute a `Pipeline` on-cluster. A `PipelineRun` executes the `Tasks` in the `Pipeline` in the order they are specified until all `Tasks` have executed successfully or a failure occurs.

Edit the above file by providing your image name, tag, namespace and kubernetes variant (if using openshift) and apply it

```
$ kubectl create --filename pipelinerun.yaml
```

The Pipeline will start running and in order to check the logs you can run

```
$ tkn pipeline logs -f  
[fetch-repository : clone] + CHECKOUT_DIR=/workspace/output/  
[fetch-repository : clone] + '[[' true '==' true ]]  
[fetch-repository : clone] + cleandir  
[fetch-repository : clone] + '[[' -d /workspace/output/ ]]  
[fetch-repository : clone] + rm -rf /workspace/output//CONTRIBUTING.md /workspace/output//LICENSE /workspace/output//OWNERS /workspace/output//README.md /workspace/output//api /workspace/output//code-of-conduct.md /workspace/output//config /workspace/output//config.yaml /workspace/output//docs /workspace/output//go.mod /workspace/output//go.sum /workspace/output//test /workspace/output//tools.go /workspace/output//ui /workspace/output//vendor  
[fetch-repository : clone] + rm -rf /workspace/output//.git /workspace/output//.github /workspace/output//.gitignore /workspace/output//.yamllint  
[fetch-repository : clone] + rm -rf '/workspace/output//..?*'  
[fetch-repository : clone] + test -z   
[fetch-repository : clone] + test -z   
[fetch-repository : clone] + test -z   
[fetch-repository : clone] + /ko-app/git-init -url https://github.com/tektoncd/hub -revision test-ci -refspec  -path /workspace/output/ '-sslVerify=true' '-submodules=true' -depth 1  
[fetch-repository : clone] {"level":"info","ts":1617594931.117907,"caller":"git/git.go:165","msg":"Successfully cloned https://github.com/tektoncd/hub @ 61c5eba4fbc924ed1d1ec44f5add0fbf5711961f (grafted, HEAD, origin/test-ci) in path /workspace/output/"}  
[fetch-repository : clone] {"level":"info","ts":1617594931.1321423,"caller":"git/git.go:203","msg":"Successfully initialized and updated submodules in path /workspace/output/"}  
[fetch-repository : clone] + cd /workspace/output/  
[fetch-repository : clone] + git rev-parse HEAD  
[fetch-repository : clone] + RESULT_SHA=61c5eba4fbc924ed1d1ec44f5add0fbf5711961f  
[fetch-repository : clone] + EXIT_CODE=0  
[fetch-repository : clone] + '[' 0 '!=' 0 ]  
[fetch-repository : clone] + echo -n 61c5eba4fbc924ed1d1ec44f5add0fbf5711961f  
[fetch-repository : clone] + echo -n https://github.com/tektoncd/hub
```

When the Pipeline finishes it’s execution successfully, you can check the deployment by running

```
$ kubectl get deployments -n tekton-hub
```

After the deployment is up and running you can visit the page by entering the url which you might have provided in the Ingress or OpenShift Route.

If you found this article insightful or of the slightest help, please give it a few claps. Feel free to reach out in case of any queries. Happy learning!