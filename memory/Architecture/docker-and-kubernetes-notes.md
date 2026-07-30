---
type: Learning
title: docker and kubernetes notes
topic: Architecture
tags:
  - docker
  - kubernetes
status: stable
generated:
  by: 'human:kiran'
  at: '2026-07-30T07:06:37.067Z'
verified:
  - by: agent-kiran/seed-script
    at: '2026-07-30T07:06:37.067Z'
---
Docker
-----
- To create docker image from `Dockerfile`, run `docker build . -t <your-image-name>`
- to run the created docker image, run `docker run -d --publish <localhost-port>:<container-port> <your-image-name>`
- To view the created image in the images list, run `docker image list`. this should list the created image
- Once completed, to verify the contents of the image, run `docker run -ti <your-image-name> bash`
- To verify the contents of the container, run `docker exec -it <your-container-name> bash`
- To delete a docker image, run `docker image rm <space-seperated-image-names> -f`
- To create images from a `yml` file, run `docker compose build`. This will by default pick `docker-compose.yml` and `Dockerfile` files. To build image through a different config file then run `docker compose -f <custom-config-yml> build`.
- To run containers through `docker-compose.yaml` file, run `docker compose up`. For a different yaml file, run `docker compose -f <your-config-yaml-file> up`

Kubernetes
-----
- To give an alias name for your kubectl: `alias k="microk8s kubectl"` and use it as `k get pods/svc` (in windows powershell, run `Set-Alias k` then enter `microk8s kubectl` as value)
- To create objects (service/deployment) from (multiple)config file: `kubectl create -f config1.yaml -f config2.yaml`
- To delete objects defined in (multiple)config file: `kubectl delete -f config1.yaml -f config2.yaml`
- To update objects by overriding (multiple)live configuration: `kubectl replace -f config1.yaml -f config2.yaml`
- To delete pod/deploy/svc by name: `kubectl delete deploy/pod/svc <name>`
- To check logs for a given pod: `kubectl logs <pod-name>`
- To list out all pods, services, deployments: `kubectl get pods,deploy,svc`
- To list out all pods, services, deployments for a given metadata label with key _app_:

  - run `kubectl get pods,deploy,svc -l app=<your-app-name>` or
  - run `kubectl get pods,deploy,svc -l 'app in (<your-app-name>)'`
  - more info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/

- To scale any deployment by name: `kubectl scale deployment/<deployment-name> --replicas=5`
- To check if a deployment is working successfully or not:

  - run `kubectl get pods`
  - run `kubectl exec -it <pod-name> sh`
  - run `nc -zv localhost:<container-port-number-of-the-pod>` => this should be success confirming that the pod is running as expected.

- To start/pause/stop microk8s, run `microk8s start/pause/stop`.
- To start minikube with proper resources: `minikube start --cpus 4 --memory 4096`. This will start minikube with 4cpus and 4gb of ram.
- To manage multiple namespaces, install `kubectx` that provides a `kubens` tool to manage namespaces.
  - To list namespaces, run `kubens`. 
  - To change namespace run `kubens <your-namespace>`.
  - To view all the components in the given namespace: `kubectl get all -n <your-namespace>`
- This will avoid headache of passing `-n` property to all kubectl commands for the selected namespace.
