---
title: "Envoy Vs Nginx and How to install Envoy and Nginx."
url: https://medium.com/p/e142be786618
---

# Envoy Vs Nginx and How to install Envoy and Nginx.

[Original](https://medium.com/p/e142be786618)

# Envoy Vs Nginx and How to install Envoy and Nginx.

[![NotJustRestart](https://miro.medium.com/v2/resize:fill:64:64/1*aBQLnCPAm7_ev5JkphQrcQ@2x.jpeg)](/?source=post_page---byline--e142be786618---------------------------------------)

[NotJustRestart](/?source=post_page---byline--e142be786618---------------------------------------)

3 min read

·

Jan 31, 2023

--

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3De142be786618&operation=register&redirect=https%3A%2F%2Fnotjustrestart.medium.com%2Fenvoy-vs-nginx-and-how-to-install-envoy-and-nginx-e142be786618&source=---header_actions--e142be786618---------------------post_audio_button------------------)

Share

## Top 10 Highlighted points about Envoy proxy

1. Envoy is an open-source, high-performance, service proxy and communication bus.
2. Designed for microservices architecture to provide traffic management, observability, and security.
3. Supports various protocols such as HTTP, gRPC, TCP, and more.
4. Dynamic service discovery and configuration management.
5. Can be used as a sidecar proxy, ingress proxy, or service mesh.
6. Supports advanced traffic routing rules and resiliency features such as circuit breaking and fault injection.
7. Integrates with service meshes such as Istio and Consul Connect.
8. Provides detailed observability through metrics, tracing, and logging.
9. Can be extended through filters for custom processing logic.
10. Adopted by major companies and widely used in production environments.

## Difference between Envoy and Nginx

1. Purpose: Envoy is a service proxy designed for microservices architecture while Nginx is a web server and reverse proxy.
2. Protocols: Envoy supports a wide range of protocols while Nginx primarily supports HTTP and HTTPS.
3. Load balancing: Envoy has more advanced load balancing options compared to Nginx.
4. Configuration: Envoy has a dynamic configuration model while Nginx uses a file-based configuration.
5. Observability: Envoy provides more comprehensive observability features such as distributed tracing and metrics.
6. Service Mesh: Envoy is often used as a core component in service mesh architectures, Nginx doesn’t have this capability.
7. Scalability: Envoy is designed to be horizontally scalable, Nginx can handle high loads but does not have native scaling features.
8. Extensibility: Envoy can be extended through filters for custom processing logic, Nginx doesn’t have this feature.
9. Performance: Both Envoy and Nginx have high performance, but Envoy’s performance may be impacted by its added features.
10. Use cases: Envoy is suitable for microservices architecture and service mesh while Nginx is suitable for web server and reverse proxy use cases.

## Installing envoy Proxy

1. Binary distribution: You can download the pre-compiled binary for your operating system from the Envoy website.
2. Docker: Envoy provides official Docker images, which can be pulled from the Docker Hub.
3. Package manager: Envoy is available in some package managers such as Homebrew (macOS) and apt (Debian/Ubuntu).

**sudo apt-get update  
sudo apt-get install envoy**

Once installed, you can start Envoy by running the `envoy` command in your terminal. Before using Envoy, you will need to configure it by creating a configuration file. The configuration file specifies how Envoy should behave and how it should route traffic.

> **How to start Envoy**

**envoy -c envoy.yaml**

**envoy — help**

> **Basic Envoy.yaml file**

In this example, Envoy is configured to listen on `0.0.0.0` on port `80` and act as an HTTP reverse proxy. Requests are routed to a single service cluster named `service_cluster` running on `127.0.0.1` on port `8000`. This is a very basic example and can be customized based on your requirements.

**admin:  
 access\_log\_path: /tmp/admin\_access.log  
 address:  
 socket\_address:  
 address: 0.0.0.0  
 port\_value: 9901  
static\_resources:  
 listeners:  
 — name: listener\_0  
 address:  
 socket\_address:  
 address: 0.0.0.0  
 port\_value: 80  
 filter\_chains:  
 — filters:  
 — name: envoy.http\_connection\_manager  
 config:  
 stat\_prefix: ingress\_http  
 codec\_type: AUTO  
 route\_config:  
 virtual\_hosts:  
 — name: local\_service  
 domains: [“\*”]  
 routes:  
 — match:  
 prefix: “/”  
 route:  
 cluster: service\_cluster  
 http\_filters:  
 — name: envoy.router  
 clusters:  
 — name: service\_cluster  
 connect\_timeout: 0.25s  
 type: STRICT\_DNS  
 lb\_policy: ROUND\_ROBIN  
 load\_assignment:  
 cluster\_name: service\_cluster  
 endpoints:  
 — lb\_endpoints:  
 — endpoint:  
 address:  
 socket\_address:  
 address: 127.0.0.1  
 port\_value: 8000**

## Installing Nginx Proxy

**sudo apt-get update**

**sudo apt-get install nginx**

> **How to start Nginx**

**sudo service nginx start**

**sudo service nginx status**

> **Example nginx.conf**

In this example, Nginx is configured to listen on port `80` and serve files from the `/usr/share/nginx/html` directory. Requests to `example.com` will be served by Nginx. This is a very basic example and can be customized based on your requirements.

**user nginx;  
worker\_processes 1;**

**error\_log /var/log/nginx/error.log;  
pid /var/run/nginx.pid;**

**events {  
 worker\_connections 1024;  
}**

**http {  
 include mime.types;  
 default\_type application/octet-stream;**

**log\_format main ‘$remote\_addr — $remote\_user [$time\_local] “$request” ‘  
 ‘$status $body\_bytes\_sent “$http\_referer” ‘  
 ‘“$http\_user\_agent” “$http\_x\_forwarded\_for”’;**

**access\_log /var/log/nginx/access.log main;**

**sendfile on;  
 keepalive\_timeout 65;**

**server {  
 listen 80;  
 server\_name example.com;**

**location / {  
 root /usr/share/nginx/html;  
 index index.html index.htm;  
 }**

**error\_page 500 502 503 504 /50x.html;  
 location = /50x.html {  
 root /usr/share/nginx/html;  
 }  
 }  
}**