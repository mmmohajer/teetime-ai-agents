# Automation System Documentation

## Overview

This automation system is designed to accelerate development workflows for projects using React (frontend) and Django (backend). By running the `./automation.sh` script, developers can quickly scaffold new components, pages, and Django app structures, as well as manage deployments and database operations. The system leverages modular shell scripts to automate repetitive tasks, enforce consistency, and reduce manual errors.

---

## 1. Code Generation & Project Scaffolding

### How It Works

Upon executing `./automation.sh`, a menu-driven interface is presented. Each menu option corresponds to a specific automation task, such as creating a new React component or Django app. The system prompts for necessary input (e.g., names), generates the required files and folders, and inserts boilerplate code where appropriate.

### Benefits

- **Speed:** Instantly scaffold new files and folders with correct structure.
- **Consistency:** Enforces project conventions and reduces manual mistakes.
- **Productivity:** Frees developers from repetitive setup, allowing focus on business logic.

### Menu Options

| Option | Description                                                                                  |
| ------ | -------------------------------------------------------------------------------------------- |
| 1      | **Create a new React component**<br>Scaffolds a new component in `client/src/components/`.   |
| 2      | **Create a new React page**<br>Creates a new page in `client/src/pages/`.                    |
| 3      | **Create a new Django app**<br>Generates a Django app structure under `api/`.                |
| 4      | **Create a new Django model file**<br>Adds a model file to an existing Django app.           |
| 5      | **Create a new Django admin file**<br>Adds an admin file to an existing Django app.          |
| 6      | **Create a Django serializer file**<br>Adds a serializer file to an existing Django app.     |
| 7      | **Create a Django view file**<br>Adds a view file to an existing Django app.                 |
| 8      | **Deploy in local server**<br>Builds and deploys the stack locally using Docker Swarm.       |
| 9      | **Deploy to prod server With Swarm**<br>Builds, pushes, and deploys to production via Swarm. |
| 10     | **Deploy to prod server With Compose**<br>Deploys to production using Docker Compose.        |
| 11     | **Make a backup from the local DB**<br>Creates a backup of the local PostgreSQL database.    |
| 12     | **Restore local DB from a file**<br>Restores the local database from a backup file.          |
| 0      | **Show MenuBar**<br>Redisplays the menu.                                                     |
| Q      | **Exit**<br>Quits the automation script.                                                     |

---

## 2. CI/CD Pipeline Integration

### Versioning & Deployment

The automation system includes robust support for version management and deployment, streamlining the CI/CD process.

#### Versioning

- **File:** `utils/shellScripting/constants/versioning.sh`
- **Variables:**
  - `NGINX_VERSION`
  - `CLIENT_VERSION`
  - `API_VERSION`
- **How it works:**  
  During deployment, the script prompts for the type of version bump (patch, minor, major, or none) for each component. It then updates the versioning file accordingly, ensuring that Docker images are tagged and pushed with the correct versions.

#### Environment Variables

- **File:** `utils/shellScripting/constants/constants.sh`
- **Variables to update:**
  - `NGINX_REPO` (Docker Hub repo for NGINX image)
  - `CLIENT_REPO` (Docker Hub repo for client image)
  - `API_REPO` (Docker Hub repo for API image)
  - `PROD_SERVER_ALIAS` (SSH alias for production server)

**Ensure these variables are set to your actual Docker Hub repositories and server alias before running production deployments.**

#### Deployment Options

- **Local Deployment:**  
  Builds and deploys all services locally using Docker Swarm.

- **Production Deployment (Swarm):**

  - Commits and pushes code to the master branch.
  - Connects to the production server via SSH.
  - Pulls the latest code, builds images, pushes to Docker Hub, and deploys using Swarm.

- **Production Deployment (Compose):**
  - Similar to Swarm, but uses Docker Compose for deployment.

---

## 3. Best Practices

- **Always update the constants and versioning files before deploying to production.**
- **Use the menu options for file generation to maintain project structure and consistency.**
- **Review generated files and add them to version control as needed.**
- **For database operations, ensure you have the correct credentials and backup/restore files.**

---

## 4. Getting Started

1. **Configure constants:**  
   Edit `utils/shellScripting/constants/constants.sh` and `utils/shellScripting/constants/versioning.sh` with your project-specific values.

2. **Run the automation script:**

   ```bash
   ./automation.sh
   ```

3. **Follow the menu prompts to generate code or manage deployments.**

---

## 5. Troubleshooting

- If you encounter permission issues, ensure `automation.sh` and related scripts are executable:
  ```bash
  chmod +x automation.sh utils/shellScripting/funcs/*.sh
  ```
- For deployment errors, verify Docker, SSH, and environment variable configurations.

---

This automation system is designed to make your development and deployment process faster, more reliable, and less error-prone. For any customizations, extend the shell scripts in `utils/shellScripting/funcs/` as needed.
