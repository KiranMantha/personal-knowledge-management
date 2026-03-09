---
title: "AEM: Configure NGINX as a Load Balancer for two AEM Dispatchers on RHEL9"
url: https://medium.com/p/7c3ab97ff841
---

# AEM: Configure NGINX as a Load Balancer for two AEM Dispatchers on RHEL9

[Original](https://medium.com/p/7c3ab97ff841)

Member-only story

# AEM: Configure NGINX as a Load Balancer for two AEM Dispatchers on RHEL9

[![Shankar Angadi](https://miro.medium.com/v2/resize:fill:64:64/0*-1pQrVD3TD58V6lb.jpg)](/@angadi.saa?source=post_page---byline--7c3ab97ff841---------------------------------------)

[Shankar Angadi](/@angadi.saa?source=post_page---byline--7c3ab97ff841---------------------------------------)

4 min read

·

Sep 2, 2024

--

5

Listen

Share

More

In this guide, we’ll configure **NGINX** to act as a load balancer for two Adobe Experience Manager (AEM) dispatchers running on `localhost:8081` and `localhost:8082`. The **NGINX** server will listen on port `8080` and distribute incoming requests between the two dispatchers, ensuring load balancing and fault tolerance.

Non members can access from [**here**](/@angadi.saa/aem-configure-nginx-as-a-load-balancer-for-two-aem-dispatchers-on-rhel9-7c3ab97ff841?sk=5b0ca887c5dbb71185f4c2d63eef4229)

### Prerequisites

* **Dispatcher 1**: Running on `localhost:8081`
* **Dispatcher 2**: Running on `localhost:8082`
* **NGINX**: Configured on `localhost:8080`
* **Operating System**: RHEL9 (Red Hat Enterprise Linux 9)

### Step 1: Install and Configure NGINX on RHEL9

1. **Update System Packages**: Ensure your system packages are up-to-date before installing NGINX.

```
sudo yum update -y
```

**2. Install NGINX**: Install NGINX from the default RHEL repositories.

```
sudo yum install nginx -y
```

**3. Start and Enable NGINX**: After installation, start the NGINX service and enable it to start automatically on system boot.

```
sudo systemctl start nginx  
sudo systemctl enable nginx
```

**4. Check NGINX Status**: Verify that NGINX is running and active.

```
sudo systemctl status nginx
```

**Step 2: Configure Firewall Rules**

If your system has a firewall enabled, you need to allow HTTP and HTTPS traffic through the firewall.

1. **Allow HTTP and HTTPS Services**: Open the necessary ports (80 for HTTP and 443 for HTTPS) to allow incoming traffic.

```
sudo firewall-cmd --permanent --add-service=http  
sudo firewall-cmd --permanent --add-service=https
```

**2. Reload Firewall**: Apply the new firewall rules.

```
sudo firewall-cmd --reload
```

### Step 3: Configure NGINX as a Load Balancer

1. **Edit NGINX Configuration**: Open the NGINX configuration file for editing. /etc/nginx/nginx.conf .

Update as below

```
# For more information on configuration, see:  
#   * Official English Documentation: http://nginx.org/en/docs/  
#   * Official Russian Documentation: http://nginx.org/ru/docs/  
  
user nginx;  
worker_processes auto;  
error_log /var/log/nginx/error.log;  
pid /run/nginx.pid;  
  
# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.  
include /usr/share/nginx/modules/*.conf;  
  
events {  
    worker_connections 1024;  
}  
  
http {     
       upstream loadbalancemysite {  
       server localhost:8081;  
       server localhost:8082;         
       }  
       server {  
       listen 80;  
       server_name localhost;  
       location / {  
       proxy_pass http://loadbalancemysite;  
       }         
    }  
}
```

In this configuration:

* The `upstream` directive defines a pool of servers (`localhost:8081` and `localhost:8082`) to which NGINX will forward client requests.
* The `proxy_pass` directive tells NGINX to forward requests to the defined upstream servers.

2. **Test NGINX Configuration**: After saving the configuration, test the NGINX configuration for syntax errors.

```
sudo nginx -t
```

**3. Reload NGINX**: Apply the new configuration by reloading NGINX.

```
sudo systemctl reload nginx
```

### Step 4: Manage NGINX Service

You can manage the NGINX service using the following commands:

```
sudo systemctl stop nginx  
sudo systemctl restart nginx  
sudo systemctl status nginx
```

### Step 5: Verify the Load Balancer

1. **Access the Load Balancer**: Open a web browser and navigate to `http://localhost/`. NGINX should distribute requests between the two dispatchers.
2. **Monitor Load Balancing**: You can monitor the load balancing behavior by repeatedly refreshing the page and observing logs on both dispatchers to ensure that requests are being distributed as expected.

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

### Load Balancing Algorithms

When configuring NGINX as a load balancer, it’s important to understand the different algorithms that can be used to distribute traffic across the upstream servers. These algorithms determine how incoming requests are distributed to your AEM dispatchers.

1. **Round Robin**:

* **Default Algorithm**: NGINX uses Round Robin as the default load balancing algorithm.
* **How It Works**: Requests are distributed sequentially across all available servers in the upstream pool. For example, the first request goes to `localhost:8081`, the second to `localhost:8082`, the third back to `localhost:8081`, and so on.
* **When to Use**: This is a simple and effective algorithm when all servers have roughly equal capacity and the workload is evenly distributed.

**2. Least Connections**:

* **How It Works**: This algorithm directs traffic to the server with the fewest active connections at the time the request is made. It is useful when the servers have varying capacities or when some requests are expected to take longer to process than others.
* **When to Use**: Use this algorithm in environments where you have varying server loads or where some servers may be more powerful than others.

Example configuration:

```
upstream aem_dispatchers {  
    least_conn;  
    server localhost:8081;  
    server localhost:8082;  
}
```

**3. IP Hash**:

* **How It Works**: The IP Hash algorithm ensures that requests from the same client IP address are always directed to the same server. It creates a more sticky session behavior, which can be beneficial for certain types of applications that require session persistence.
* **When to Use**: Use this algorithm when session persistence is important, such as in applications where user state is stored on the server.

Example configuration:

```
upstream aem_dispatchers {  
    ip_hash;  
    server localhost:8081;  
    server localhost:8082;  
}
```

**4. Weighted Load Balancing**:

* **How It Works**: With weighted load balancing, you can assign different weights to each server in the upstream pool. Servers with higher weights receive a larger share of the traffic. This is useful when you have servers with different capacities.
* **When to Use**: Use weighted load balancing when your servers have different performance characteristics, and you want to route more traffic to the more powerful servers.

Example configuration:

```
upstream aem_dispatchers {  
    server localhost:8081 weight=3;  
    server localhost:8082 weight=1;  
}
```