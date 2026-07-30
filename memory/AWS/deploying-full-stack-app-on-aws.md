---
title: Deploying full stack app on AWS
topic: AWS
tags:
  - aws
  - ec2
  - deployment
source_type: hands-on
confidence: confirmed
created: '2026-07-29'
---
Original article: https://www.sammeechward.com/deploying-full-stack-js-to-aws-ec2

Youtube: https://www.youtube.com/watch?v=nQdyiK7-VlQ

# Deploying Full Stack Apps to AWS EC2 with SQL Databases
Deploying Full Stack Apps to AWS EC2 with SQL Databases
-------------------------------------------------------

Setup EC2 Instance
------------------

```console
sudo apt update
sudo apt upgrade

```


Install Node.js
---------------

```console
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

```


rsync
-----

```console
rsync -avz --exclude 'node_modules' --exclude '.git' --exclude '.env' \
-e "ssh -i ~/.ssh/your-key.pem" \
. ubuntu@ip-address:~/app

```

Database
--------

```console
sudo apt install mysql-server

sudo systemctl start mysql
sudo systemctl enable mysql

sudo mysql -u root

```


```sql
CREATE DATABASE my_app;
CREATE USER 'my_app_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'MyNewPass1!';
GRANT ALL PRIVILEGES ON my_app.* TO 'my_app_user'@'localhost';

```


systemd
-------

### Step 1: Create the Environment File

Create a new file for your environment variables and open the file in Vim:

```console
sudo vim /etc/app.env
```


In Vim, add your variables in the format `VARIABLE=value`. For example:

```
DB_PASSWORD=your_secure_password

```


Note

to save and exit vim, press `esc` then `:wq` then `enter`

Restrict the file permissions for security.

```console
sudo chmod 600 /etc/app.env
sudo chown ubuntu:ubuntu /etc/app.env

```


### Step 2: Create the systemd Service File

Navigate to the systemd directory and create a new service file, `myapp.service`.

```console
sudo vim /etc/systemd/system/myapp.service

```


Define the service settings. Add the following content in Vim, modifying as needed for your application:

```vim
[Unit]
Description=Node.js App
After=network.target multi-user.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/app
ExecStart=/usr/bin/npm start
Restart=always
Environment=NODE_ENV=production
EnvironmentFile=/etc/app.env
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=myapp

[Install]
WantedBy=multi-user.target

```


Reload systemd and start your service.

```console
sudo systemctl daemon-reload
sudo systemctl enable myapp.service
sudo systemctl start myapp.service

```


Verify that the service is running properly.

```console
sudo systemctl status myapp.service

```


### View Logs

```console
sudo journalctl -u myapp.service

```


tail logs:

```console
sudo journalctl -fu myapp.service

```

Caddy
-----

### Step 1: Install Caddy

[https://caddyserver.com/docs/install](https://caddyserver.com/docs/install)

```console
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy

```

```console
sudo vim /etc/caddy/Caddyfile

```


```conf
:80 {
    reverse_proxy localhost:3000
}

```


```console
sudo systemctl restart caddy

```


### Step 2: Configure Caddy to Use HTTPS

Add a domain name for your server.

Update the Caddyfile to use your domain name and enable HTTPS.

```console
sudo vim /etc/caddy/Caddyfile

```


```conf
mydomain.com {
    reverse_proxy localhost:3000
}

```


```console
sudo systemctl restart caddy

```
