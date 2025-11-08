# docker-dev-template

This repository provides a **standardized template** for quickly spinning up lightweight, ready-to-use development containers.
The goal is to offer a plug-and-play setup that works **consistently across all projects**.

---

### 🧰 Requirements

Before getting started, make sure you have the following installed and running:

* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* An IDE (e.g., [Visual Studio Code](https://code.visualstudio.com/))
* The **Dev Containers** extension for VS Code (installable from the Marketplace)

---
### 🚀 Get Started

#### 1. Clone this repository as your project base

```bash
git clone https://github.com/santarsierilorenzo/docker-dev-template.git your-project-name
cd your-project-name
code .
```

You’ll now have a structure like this:

```
your-project-name/
├── .devcontainer/
│   ├── devcontainer.json
│   ├── devcontainer.json.extensions
│   ├── devcontainer.json.extensions_ssh_mount   
│   └── devcontainer.json.ssh_mount
└── requirements.txt
```

⚠️ **Important:** After cloning, run the initialization script to finalize setup:

```bash
bash ./init.sh
```

This script will:
* 🧹 **Clear the content** of the `README.md` file so you can start fresh with your own project description.  
* 🔒 **Remove the remote origin** to safely detach your local copy from the original template repository.

#### 2. Choose your preferred setup

* **`devcontainer.json`** → minimal setup with a base Python environment.  
* **`devcontainer.json.extensions`** → same as above, but with preinstalled VS Code extensions (recommended for IDE-ready environments).  
* **`devcontainer.json.ssh_mount`** → same as the base setup, but with SSH key mounting enabled for direct GitHub access inside the container.  
* **`devcontainer.json.extensions_ssh_mount`** → full setup with both VS Code extensions and SSH key mounting (recommended for development environments requiring GitHub access).  

⚠️ **Important:** if you choose the *extensions*, *ssh_mount* or *extensions_ssh_mount* configuration, you must rename the file by removing the suffix so it becomes:

```
devcontainer.json
```

VS Code only detects a single `devcontainer.json` file as the active configuration.

#### 3. Open the Command Palette in VS Code

```bash
Ctrl + Shift + P
```

and select:

```bash
Dev Containers: Rebuild Without Cache and Reopen in Container
```

This will:

* Build the Docker image based on the selected configuration.
* Mount your project directory into the container.
* Set up an isolated and reproducible Python environment.


#### 4. Automatic local setup (runs on first build)

You no longer need to manually run any setup scripts — everything happens automatically when the container is created.  
Under the hood, the `postCreateCommand` triggers the `setup.sh` script, which:
* Marks specific files (like `.devcontainer/`, `requirements.txt`) as “unchanged” locally, so they won’t appear in `git status`.

✅ This ensures your local environment is clean, isolated, and ready to use without affecting the original GitHub project.

#### 5. Start developing

Once the container is up and ready, you can begin working immediately in a reproducible, isolated environment.


---

### 🧠 What Happens Under the Hood

When you select *Reopen in Container*, VS Code:

* Reads the `.devcontainer/<config>.json` file you selected.
* Builds a Docker image using Python and the dependencies listed in `requirements.txt`.
* Creates a container and mounts your local folder into `/your-project-name`.
* Automatically sets environment variables:

  * `WORKDIR=/your-project-name`
  * `PYTHONPATH=/your-project-name`
  * `USER=myuser`

This gives you an isolated, reproducible, and consistent environment across systems.

---

### 🔐 Using SSH with the Dev Container (`devcontainer.json.ssh_mount`)

**Your SSH keys will never be copied or exposed in the image.**
They are mounted temporarily and only accessible at runtime for Git operations inside the container.

#### How it works

When you use the SSH-enabled configuration, VS Code mounts your local SSH folder (`~/.ssh`) into the container at:

```
/home/myuser/.ssh
```

This allows you to use GitHub SSH authentication (e.g., `git push`, `git pull`) from inside the container without manually configuring anything.

#### Requirements

Ensure your host system has a valid SSH configuration:

```
~/.ssh/
```

containing at least:

```
id_rsa / id_ed25519
id_rsa.pub / id_ed25519.pub
known_hosts
```

If you don’t have keys, generate them:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Then add your public key to your GitHub account:
👉 [https://github.com/settings/keys](https://github.com/settings/keys)

#### Security notes

* The `.ssh` folder is **mounted read-only**.
* The keys remain **on your host**, never inside the image.
* The container can only use them temporarily during its runtime.

To verify your setup inside the container:

```bash
ssh -T git@github.com
```

You should see:

```
Hi <username>! You've successfully authenticated, but GitHub does not provide shell access.
```

---

### 🧩 Template Structure

```
.devcontainer/
├── Dockerfile  # Defines the base image and user
├── devcontainer.json  # Minimal setup
├── devcontainer.json.extensions  # Setup with VS Code extensions
└── devcontainer.json.ssh_mount  # Setup with SSH key support
requirements.txt  # Optional Python dependencies
```

---

### 🧱 Technologies Included

* **Python 3.10**
* **Non-root user** (`myuser`)
* **Bash shell**
* Full **VS Code Dev Containers** integration

---

### 🧭 Customization

You can easily adjust the template to your needs:

* **Dockerfile** → Add system packages or CLI tools.
* **requirements.txt** → Add Python dependencies.
* **devcontainer.json** → Configure extensions, mounts, or environment variables.

---

### ⚙️ .gitignore and .dockerignore

These files are included to **protect your development environment from accidental pushes** and avoid polluting the repository or Docker image.

---

### 🧹 Cleanup

To remove containers and images created by this setup:

```bash
docker ps -a      # List containers
docker rm <id>    # Remove container
docker rmi <image> # Remove image
```

---

### ✅ Goal

A single, consistent Docker setup for all your Python projects.

>
