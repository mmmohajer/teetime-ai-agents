# Application Deployment Guide

This document provides a comprehensive, step-by-step guide for deploying and hardening your server for the application. Follow each section carefully to ensure a secure and reliable deployment.

---

# Table of Contents

- [1. Initial Server Hardening](#1-initial-server-hardening)
  - [1.1. Login and User Setup](#11-login-and-user-setup)
  - [1.2. Disable Root Login via SSH](#12-disable-root-login-via-ssh)
- [2. SSH Key Authentication](#2-ssh-key-authentication)
  - [2.1. Generate SSH Keys (Local Machine)](#21-generate-ssh-keys-local-machine)
  - [2.2. Copy Public Key to Server](#22-copy-public-key-to-server)
  - [2.3. Configure Server for Key Authentication](#23-configure-server-for-key-authentication)
  - [2.4. Test SSH Key Login](#24-test-ssh-key-login)
- [3. SSH Config Alias (Local Machine)](#3-ssh-config-alias-local-machine)
- [4. System Updates & Firewall](#4-system-updates--firewall)
  - [4.1. Update & Upgrade](#41-update--upgrade)
  - [4.2. Configure UFW Firewall](#42-configure-ufw-firewall)
- [5. Install & Configure fail2ban](#5-install--configure-fail2ban)
- [6. Install Docker & Docker Compose](#6-install-docker--docker-compose)
- [7. Git Configuration & SSH for GitHub](#7-git-configuration--ssh-for-github)
- [8. Clone the Repository](#8-clone-the-repository)
- [9. Application Setup](#9-application-setup)
  - [9.1. Create Required Folders](#91-create-required-folders)
  - [9.2. Update Configuration Files](#92-update-configuration-files)
  - [9.3. Set Executable Permissions](#93-set-executable-permissions)
  - [9.4. Setup HTTP Basic Auth for Flower (Optional)](#94-setup-http-basic-auth-for-flower-optional)
  - [9.5. SSL Certificate Setup](#95-ssl-certificate-setup)
  - [9.6. Clean Up Docker (Optional)](#96-clean-up-docker-optional)
  - [9.7. Test SSL Setup](#97-test-ssl-setup)
  - [9.8. Production Deployment](#98-production-deployment)
- [10. Docker Swarm & GlusterFS Deployment](#10-docker-swarm--glusterfs-deployment)
  - [10.1. Swarm Architecture Overview](#101-swarm-architecture-overview)
  - [10.2 📘 GlusterFS Deployment Guide](#102-📘-glusterfs-deployment-guide)
    - [10.2.1. 🎯 Objective](#1021-🎯-objective)
    - [10.2.2. Install GlusterFS](#1022-install-glusterfs)
    - [10.2.3. Prepare Brick Directories](#1023-prepare-brick-directories)
    - [10.2.4. Form the Trusted Pool](#1024-form-the-trusted-pool)
    - [10.2.5. Create a Replicated Volume](#1025-create-a-replicated-volume)
    - [10.2.6. Temporary Mount (Safe Migration)](#1026-temporary-mount-safe-migration)
    - [10.2.7. Copy Existing Data Into GlusterFS](#1027-copy-existing-data-into-glusterfs)
    - [10.2.8. Switch the Real Mount](#1028-switch-the-real-mount)
    - [10.2.9. Persistent Mounts via /etc/fstab](#1029-persistent-mounts-via-etc-fstab)
    - [10.2.10. Test Replication](#10210-test-replication)
    - [10.2.11. Monitoring & Healing](#10211-monitoring--healing)
    - [10.2.12 Adding a New Node (Scaling)](#10212-adding-a-new-node-scaling)
      - [10.2.12.1 Install GlusterFS on the New Node](#102121-install-glusterfs-on-the-new-node)
      - [10.2.12.2. Prepare Brick Directory](#102122-prepare-brick-directory)
      - [10.2.12.3. Add Node to the Cluster](#102123-add-node-to-the-cluster)
      - [10.2.12.4. Expand the Volume](#102124-expand-the-volume)
      - [10.2.12.5. Trigger a Heal](#102125-trigger-a-heal)
      - [10.2.12.6 Mount on the New Node](#102126-mount-on-the-new-node)
    - [10.2.13. GlusterFS Watchdog Service](#10213-glusterfs-watchdog-service)
    - [✅ Final Outcome](#✅-final-outcome)
  - [10.3. Swarm Cluster Setup](#103-swarm-cluster-setup)
    - [10.3.1. Initialize the Swarm Manager](#1031-initialize-the-swarm-manager)
    - [10.3.2. Configure Load Balancer (DigitalOcean Example)](#1032-configure-load-balancer-digitalocean-example)
    - [10.3.3. Join Worker Nodes](#1033-join-worker-nodes)
    - [10.3.4. Add Additional Manager Nodes (Optional)](#1034-add-additional-manager-nodes-optional)
    - [10.3.5. Verify Cluster Status](#1035-verify-cluster-status)
    - [✅ Outcome](#✅-outcome)
  - [10.4. Useful Docker Swarm Commands](#104-useful-docker-swarm-commands)
- [11. Continuous Integration & Continuous Deployment (CI/CD)](#11-continuous-integration--continuous-deployment-cicd)
  - [Deploying with automation.sh](#deploying-with-automationsh)
  - [Automated Maintenance (SSL Renewal, Sitemap, and Backups)](#automated-maintenance-ssl-renewal-sitemap-and-backups)

## 1. Initial Server Hardening

### 1.1. Login and User Setup

1. **Login to the server as root:**
   ```sh
   ssh root@IP_ADDRESS
   ```
2. **Change the root user password:**
   ```sh
   passwd
   ```
3. **Add a new user:**
   ```sh
   adduser USER_NAME
   ```
4. **Grant sudo privileges to the new user:**
   - Open the sudoers file:
     ```sh
     visudo
     ```
   - Add the following line under root privileges:
     ```
     USER_NAME ALL=(ALL:ALL) ALL
     ```

### 1.2. Disable Root Login via SSH

1. Navigate to the SSH config directory:
   ```sh
   cd /etc/ssh/
   cp sshd_config sshd_config.bak
   nano sshd_config
   ```
2. Change the following line:
   ```
   PermitRootLogin no
   ```
3. Save and exit (`Ctrl+X`), then restart SSH:
   ```sh
   systemctl restart ssh
   ```
4. **Login as the new user:**
   ```sh
   ssh USER_NAME@IP_ADDRESS
   ```
5. **Switch to root (if needed):**
   ```sh
   sudo -s
   ```

---

## 2. SSH Key Authentication

Switch to public/private key authentication for enhanced security.

### 2.1. Generate SSH Keys (Local Machine)

```sh
mkdir -p ~/.ssh
cd ~/.ssh
ssh-keygen -t rsa -b 4096 -C "Comment for the file"
```

### 2.2. Copy Public Key to Server

```sh
scp ~/.ssh/PUB_SSH_KEY_NAME.pub USER_NAME@IP_ADDRESS:/home/USER_NAME
```

### 2.3. Configure Server for Key Authentication

```sh
ssh USER_NAME@IP_ADDRESS
mv PUB_SSH_KEY_NAME.pub authorized_keys
mkdir -p ~/.ssh
mv authorized_keys ~/.ssh/
chmod 600 ~/.ssh/authorized_keys
sudo chattr +i ~/.ssh/authorized_keys
chmod 700 ~/.ssh
cd /etc/ssh
sudo nano sshd_config
# Ensure the following lines are set:
PubkeyAuthentication yes
AuthorizedKeysFile %h/.ssh/authorized_keys .ssh/authorized_keys2
PasswordAuthentication no
sudo systemctl restart ssh
```

### 2.4. Test SSH Key Login

```sh
ssh -i ~/.ssh/PRIVATE_SSH_KEY_NAME USER_NAME@IP_ADDRESS
```

---

## 3. SSH Config Alias (Local Machine)

Create an alias for easier login:

Edit `~/.ssh/config` and add:

```sh
Host myserver
    Hostname IP_ADDRESS
    User USER_NAME
    IdentityFile /path/to/private_key
    ServerAliveInterval 60
    ServerAliveCountMax 120
```

Now you can login with:

```sh
ssh myserver
```

---

## 4. System Updates & Firewall

### 4.1. Update & Upgrade

```sh
sudo apt update
sudo apt upgrade
sudo apt autoremove
```

### 4.2. Configure UFW Firewall

```sh
sudo apt install ufw
sudo ufw status verbose
```

Then copy from your system to server using:

```sh
scp ./utils/shellScripting/funcs/setup_ufw.sh TexVoMaster1:/home/USER_NAME
```

Then in the server, run:

```sh
sudo chmod +x setup_ufw.sh
sudo ./setup_ufw.sh
sudo ufw enable
sudo reboot
```

---

## 5. Install & Configure fail2ban

```sh
sudo apt update
sudo apt install fail2ban
cd /etc/fail2ban
sudo cp jail.conf jail.local
sudo nano jail.local
# Set the following:
bantime = 604800s
findtime = 10800s
maxretry = 2
sudo systemctl restart fail2ban
```

**View fail2ban logs:**

```sh
cd /var/log
sudo cat fail2ban.log
```

**Unban your IP if needed:**

```sh
fail2ban-client set sshd unbanip IP_ADDRESS
```

---

## 6. Install Docker & Docker Compose

**Docker:** [Official Guide](https://docs.docker.com/engine/install/ubuntu/)

**Docker Compose:**

```sh
sudo apt update
sudo apt install docker-compose-plugin
docker compose version
```

**Add your user to the docker group:**

```sh
sudo groupadd docker
sudo usermod -aG docker USER_NAME
newgrp docker
docker run hello-world
```

---

## 7. Git Configuration & SSH for GitHub

**Set git config:**

```sh
sudo git config --global user.email "OWNER_OF_GITHUB_REPO_EMAIL"
git config --global user.email "OWNER_OF_GITHUB_REPO_EMAIL"
```

**Generate SSH keys for GitHub:**

```sh
ssh-keygen -t rsa -b 4096 -C "Comment for the file"
# Do not set a passphrase
# Copy the private key to your server's ~/.ssh folder
# Add the public key to your GitHub account
```

**Add to `~/.ssh/config` on the server:**

```sh
Host github.com
User GIT_USER_NAME
Hostname github.com
IdentityFile ~/.ssh/github_rsa
```

**Test the connection:**

```sh
ssh -T git@github.com
```

---

## 8. Clone the Repository

```sh
sudo chown -R USER_NAME:USERNAME /var/www/app
cd /var/www/app
git clone SSH_REPO_URL .
```

---

## 9. Application Setup

### 9.1. Create Required Folders

```sh
mkdir -p ./api/vol/static ./api/vol/media ./db_backups ./volume_data volume_data/django_static/static volume_data/django_static/media
```

### 9.2. Update Configuration Files

Update the following files from their sample files:

Find the google processor ID from here:
https://console.cloud.google.com/ai/document-ai/locations/us/processors/

- `.env`
- `secrets/api/.env`
- `secrets/db/.env`
- `secrets/pgbouncer/.env`
- `secrets/secret_files/cloudflare.ini`
- `secrets/secret_files/cred.json`
- `client/next.config.js`
- `redis/redis.conf`
- `janus/janus.jcfg`
- `nginx/configs/default.conf`
- `init-letsencrypt.sh`
- `utils/assistances/backup_db_swarm.sh`
- `utils/shellScripting/funcs/secret_vars.sh`

Update the following file in your local system:

- `utils/shellScripting/funcs/secret_vars.sh`

### 9.3. Set Executable Permissions

```sh
sudo chmod +x ./init-letsencrypt.sh
sudo chmod +x /var/www/app/utils/assistances/backup_db_swarm.sh
```

### 9.4. Setup HTTP Basic Auth for Flower (Optional)

```sh
sudo apt-get install apache2-utils
cd nginx
htpasswd -c .htpasswd CELERY_FLOWER_USER
# Use the CELERY_FLOWER_PASSWORD defined in your env variables
```

### 9.5. SSL Certificate Setup

1. Create the following folders:
   ```sh
   mkdir -p ./nginx/certbot/conf/
   mkdir -p ./nginx/certbot/www/
   ```
2. Add A records to your domain's DNS pointing to the server IP (including www as a CNAME).
3. Run the script:
   ```sh
   sudo ./init-letsencrypt.sh
   ```

### 9.6. Clean Up Docker (Optional)

```sh
docker container rm -f $(docker container ls -a -q)
docker image rm -f $(docker image ls -q)
docker volume rm $(docker volume ls -q)
```

### 9.7. Test SSL Setup

1. Update the domain in the server_name block of `default-temp-with-ssl.conf`.
2. Set permissions:
   ```sh
   sudo chown -R USERNAME:USERNAME /var/www/app
   sudo chown -R USERNAME:docker /var/www/app/nginx/certbot
   ```
3. Start the app with SSL:
   ```sh
   sudo docker compose -f docker-compose-temp-with-ssl.yml up --build -d
   ```

### 9.8. Production Deployment

**With Compose:**

```sh
sudo docker compose -f docker-compose-prod.yml up --build -d
```

---

## 10. Docker Swarm & GlusterFS Deployment

### 10.1. Swarm Architecture Overview

- **Basic:** 1 Manager Node, 2 Worker Nodes
- **High Availability:** 3+ Manager Nodes (for quorum), 3+ Worker Nodes
- **(Recommended)**: Use a load balancer in front of your managers for production.

---

### 10.2 📘 GlusterFS Deployment Guide

Replicated Setup for `/var/www/app` with Data Migration, Persistence & Scaling\_

---

#### 10.2.1. 🎯 Objective

- Share `/var/www/app` across multiple nodes using GlusterFS.
- Ensure **real-time replication** of files, ownership, permissions, and executability.
- Safely migrate existing data without hiding or losing it.
- Configure persistent mounts across reboots.
- Support scaling by adding new nodes in the future.

---

#### 10.2.2. Install GlusterFS

On **all nodes**:

```bash
sudo apt update
sudo apt install glusterfs-server -y
sudo systemctl enable glusterd --now
```

Verify:

```bash
sudo systemctl status glusterd
```

Create the app directory on the node if not exists:

```bash
sudo mkdir -p /var/www/app/
sudo chown -R USER_NAME:USER_NAME /var/www/app
```

---

#### 10.2.3. Prepare Brick Directories

On **each node**:

```bash
sudo mkdir -p /gluster/brick1
sudo chown -R $USER:$USER /gluster/brick1
```

⚠️ Bricks must be **dedicated and empty**. Do not reuse a directory with existing data.

---

#### 10.2.4. Form the Trusted Pool

On the **first (master) node**:

```bash
sudo gluster peer probe NODE2_IP
sudo gluster peer probe NODE3_IP
```

Check:

```bash
sudo gluster peer status
```

---

#### 10.2.5. Create a Replicated Volume

On the **master node**:

```bash
sudo gluster volume create app-volume replica 2 NODE1_IP:/gluster/brick1 NODE2_IP:/gluster/brick1 force
```

- Use `replica 3` for three nodes.
- Each node contributes one brick.

Start the volume:

```bash
sudo gluster volume start app-volume
sudo gluster volume info
```

---

#### 10.2.6. Temporary Mount (Safe Migration)

On the node holding the **original `/var/www/app` data**:

```bash
sudo mkdir -p /mnt/gluster_app
sudo mount -t glusterfs NODE1_IP:/app-volume /mnt/gluster_app
```

---

#### 10.2.7. Copy Existing Data Into GlusterFS

On the same node:

```bash
sudo rsync -aAXHv /var/www/app/ /mnt/gluster_app/
```

This preserves:

- Permissions
- Ownership
- Symlinks
- Executability

Now your data is inside GlusterFS and will replicate across all nodes.

---

#### 10.2.8. Switch the Real Mount

1. Unmount the temporary mount:

   ```bash
   sudo umount /mnt/gluster_app
   ```

2. Mount GlusterFS at the application directory:
   ```bash
   sudo mount -t glusterfs NODE1_IP:/app-volume /var/www/app
   ```

At this point, **real-time replication is active**.

---

#### 10.2.9. Persistent Mounts via `/etc/fstab`

On **all nodes**, edit `/etc/fstab`:

```bash
sudo nano /etc/fstab
```

Add the following line:

```
NODE1_IP,NODE2_IP:/app-volume /var/www/app glusterfs defaults,_netdev 0 0
```

- Multiple IPs ensure high availability.
- `_netdev` guarantees mount waits for network readiness.

Apply immediately:

```bash
sudo mount -a
```

Verify:

```bash
mount | grep gluster
```

---

#### 10.2.10. Test Replication

On Node1:

```bash
touch /var/www/app/test_from_node1
```

On Node2:

```bash
ls -l /var/www/app/ | grep test_from_node1
```

✅ The file should appear instantly.

---

## 10.2.11. Monitoring & Healing

- Volume status:
  ```bash
  sudo gluster volume status
  ```
- Heal check:
  ```bash
  sudo gluster volume heal app-volume info
  ```
- Force full heal if required:
  ```bash
  sudo gluster volume heal app-volume full
  ```

---

#### 10.2.12 Adding a New Node (Scaling)

##### 10.2.12.1 Install GlusterFS on the New Node

```bash
sudo apt update
sudo apt install glusterfs-server -y
sudo systemctl enable glusterd --now
```

###### 10.2.12.2. Prepare Brick Directory

```bash
sudo mkdir -p /gluster/brick1
sudo chown -R $USER:$USER /gluster/brick1
```

⚠️ Must be **empty**.

##### 10.2.12.3. Add Node to the Cluster

From an existing node:

```bash
sudo gluster peer probe NODE3_IP
sudo gluster peer status
```

##### 10.2.12.4. Expand the Volume

Since the volume is currently `replica 2`, expand to `replica 3`:

```bash
sudo gluster volume add-brick app-volume replica 3 NODE3_IP:/gluster/brick1 force
```

Confirm:

```bash
sudo gluster volume info
```

It should show **Number of Bricks: 1 x 3 = 3**.

##### 10.2.12.5. Trigger a Heal

```bash
sudo gluster volume heal app-volume full
sudo gluster volume heal app-volume info
```

Wait until all entries are healed (`Number of entries: 0`).

##### 10.2.12.6 Mount on the New Node

On Node3:

```bash
sudo mkdir -p /var/www/app
```

Edit `/etc/fstab`:

```
NODE1_IP,NODE2_IP,NODE3_IP:/app-volume /var/www/app glusterfs defaults,_netdev 0 0
```

Apply:

```bash
sudo mount -a
```

---

#### 10.2.13. GlusterFS Watchdog Service

```sh
sudo nano /etc/systemd/system/glusterfs-watchdog.service
```

```ini
[Unit]
Description=GlusterFS Watchdog
After=network.target

[Service]
ExecStart=/var/www/app/glusterfs_watchdog.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

(Optional) Create a log file for the watchdog script:

```sh
sudo touch /var/log/glusterfs_watchdog.log
sudo chmod 666 /var/log/glusterfs_watchdog.log
```

Reload and enable the automated services:

```sh
sudo systemctl daemon-reload
sudo systemctl enable glusterfs-watchdog
sudo systemctl start glusterfs-watchdog
```

---

#### ✅ Final Outcome

- `/var/www/app` is now a **replicated GlusterFS volume**.
- Existing data safely migrated without being hidden.
- Any change on one node instantly appears on all others.
- Permissions and executability are preserved.
- Mounts survive reboots automatically via `/etc/fstab`.
- Cluster can be expanded by adding new nodes when needed.

---

### 10.3. Swarm Cluster Setup

Docker Swarm is used to orchestrate and scale the services in this project.  
This section covers initializing the Swarm, onboarding worker and manager nodes, and configuring load balancing.

---

#### 10.3.1. Initialize the Swarm Manager

1. On the designated manager node, initialize the Swarm cluster:

   ```sh
   docker swarm init --advertise-addr <MANAGER_IP>
   ```

2. Create **four private repositories** on Docker Hub for the following services:

   - Client
   - API
   - NGINX
   - Janus

3. Update repository references:

   - Edit `utils/shellScripting/constants/constants.sh`.
   - Replace the placeholders with your Docker Hub repository names and server aliases.

4. Authenticate the manager node with Docker Hub:

   ```sh
   docker login -u <DOCKER_HUB_USERNAME>
   ```

5. Remove the default Docker Compose network (if present):

   ```sh
   docker network rm app_default
   ```

6. From your local machine, run the automation script to deploy the stack:

   ```sh
   ./automation.sh
   ```

---

#### 10.3.2. Configure Load Balancer (DigitalOcean Example)

To ensure scalability and high availability, configure a regional load balancer with the following settings:

- **Forwarding Rules**

  - HTTP: port 80 → port 80
  - HTTPS: port 443 → port 443

- **Health Checks**

  - Protocol: HTTP
  - Path: `/health`
  - Port: 80

- **SSL Settings**
  - Enable SSL certificate.
  - Redirect all HTTP traffic to HTTPS.

---

#### 10.3.3. Join Worker Nodes

1. On each worker node, join the cluster:

   ```sh
   docker swarm join --token <WORKER_TOKEN> <MANAGER_IP>:2377
   ```

2. To retrieve the worker join token, run on the manager node:

   ```sh
   docker swarm join-token worker
   ```

---

#### 10.3.4. Add Additional Manager Nodes (Optional)

1. On the primary manager node, retrieve the manager join token:

   ```sh
   docker swarm join-token manager
   ```

2. On the new manager node, join the cluster as a manager:

   ```sh
   docker swarm join --token <MANAGER_TOKEN> <MANAGER_IP>:2377
   ```

---

#### 10.3.5. Verify Cluster Status

On any manager node, list all nodes and confirm their roles and statuses:

```sh
docker node ls
```

- Managers are marked with `Leader` or `Reachable`.
- Workers show `Active`.

---

#### ✅ Outcome

- A Docker Swarm cluster is initialized with one or more managers.
- Worker nodes are joined successfully.
- Services can be deployed and scaled across the cluster.
- The load balancer ensures traffic distribution, health checks, and SSL termination.

---

### 10.4. Useful Docker Swarm Commands

- **List nodes:**
  ```sh
  docker node ls
  ```
- **Inspect node:**
  ```sh
  docker node inspect <NODE_ID>
  ```
- **Remove node:**
  ```sh
  docker node rm <NODE_ID>
  ```
- **Leave swarm:**
  ```sh
  docker swarm leave [--force]
  ```
- **List services:**
  ```sh
  docker service ls
  ```
- **List tasks of a service:**
  ```sh
  docker service ps <service_name>
  ```
- **Logs:**
  ```sh
  docker service logs <service_name>
  docker logs <container_id>
  ```
- **Scale a service:**
  ```sh
  docker service scale <service_name>=<replicas>
  ```
- **Update node availability:**
  ```sh
  docker node update --availability drain|active <NODE_ID>
  ```

---

## 11. Continuous Integration & Continuous Deployment (CI/CD)

CI/CD (Continuous Integration and Continuous Deployment) is a set of practices that automate the process of integrating code changes, testing, and deploying applications. This ensures that new features, bug fixes, and updates can be delivered to users quickly, reliably, and with minimal manual intervention. In this project, you can use the provided automation script to streamline your deployment process.

### Deploying with automation.sh

1. Update variables in `utils/shellScripting/constants`:
   ```sh
   PROD_SERVER_ALIAS=PROD_SERVER_ALIAS
   NGINX_REPO="NGINX_REPO_ON_DOCKER_HUB"
   CLIENT_REPO="CLIENT_REPO_ON_DOCKER_HUB"
   API_REPO="API_REPO_ON_DOCKER_HUB"
   ```
2. Run `automation.sh` in the root folder and follow the prompts to deploy your application.

---

#### Automated Maintenance (SSL Renewal, Sitemap, and Backups)

To ensure SSL certificates are auto-renewed, sitemaps are generated, and database backups are performed regularly, add the following to `sudo crontab -e`:

```cron
0 1 * * * /var/www/app/utils/assistances/generate_sitemap.sh
0 2 * * * /var/www/app/utils/assistances/backup_db_swarm.sh
0 3 * * * /var/www/app/utils/assistances/update_nginx.sh
0 4 * * * docker system prune -a --volumes
```

These scheduled tasks will keep your SSL certificates up to date, generate sitemaps for SEO, and back up your database automatically.

---

Your application should now be securely deployed and production-ready!
