# Event Ticketing Service

COMP 642 Course Project

## Overview

This project is a simple online event and ticketing service.

Users will be able to:

- Create accounts
- Browse events
- View event details
- Purchase tickets
- View previous orders
- Review events
- View trending events

Administrators will be able to:

- Create and manage events
- Manage ticket types
- Monitor ticket inventory
- Review ticket sales
- Analyze event activity

## Technology Stack

| Technology | Purpose |
|---|---|
| MySQL 8.4 | Users, venues, events, ticket types, orders, payments, and ticket inventory |
| MongoDB | Flexible event content such as descriptions, schedules, speakers, performers, tags, and reviews |
| Redis | Event cache and trending-event ranking |
| FastAPI | REST API that connects MySQL, MongoDB, and Redis |
| Docker Compose | Starts the full application environment |

## Requirements

Install the following before starting:

- Git
- Docker Desktop
- Visual Studio Code, recommended

Do not install MySQL, MongoDB, or Redis manually. Docker Compose starts them for this project.

## Install Docker Desktop

### Windows 10/11

1. Install Docker Desktop from [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. During installation, select the WSL 2 backend if prompted.
3. Restart Windows if prompted.
4. Open Docker Desktop.
5. Wait until Docker Desktop shows that the engine is running.
6. Open PowerShell as Administrator and run:

```powershell
wsl --install
wsl --update
```

7. Restart Windows if prompted.
8. In Docker Desktop, open:

```text
Settings → General
```

9. Enable:

```text
Use the WSL 2 based engine
```

10. In Docker Desktop, open:

```text
Settings → Resources → WSL Integration
```

11. Enable integration for your Ubuntu distribution.

Verify installation from WSL Ubuntu:

```bash
docker --version
docker compose version
docker run --rm hello-world
```

### macOS

1. Install Docker Desktop from [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Download the correct version:
   - Apple Silicon for M-series Macs
   - Intel for Intel-based Macs
3. Open the downloaded `.dmg` file.
4. Drag Docker into the Applications folder.
5. Open Docker Desktop from Applications.
6. Wait until Docker Desktop is running.

Verify installation in Terminal:

```bash
docker --version
docker compose version
docker run --rm hello-world
```

## Clone the Repository

Use SSH if your GitHub SSH key is configured:

```bash
git clone git@github.com:YOUR-GITHUB-USERNAME/event-ticketing-service.git
cd event-ticketing-service
```

## Environment Configuration

Create a local environment file:

```bash
cp .env.example .env
```

Edit `.env` and set local MySQL passwords:

```bash
nano .env
```

Do not commit `.env`. It contains local passwords.

## Start the Application

From the project root:

```bash
docker compose up --build
```

To run containers in the background:

```bash
docker compose up --build -d
```

The first run may take several minutes because Docker downloads images and installs Python dependencies.

## Verify the Application

Check running containers:

```bash
docker compose ps
```

Expected services:

```text
ticketing-api
ticketing-mysql
ticketing-mongodb
ticketing-redis
```

Check API health:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "api": "healthy",
  "mysql": "healthy",
  "mongodb": "healthy",
  "redis": "healthy"
}
```

Open API documentation in a browser:

```text
http://localhost:8000/docs
```

## Common Docker Commands

| Command | Purpose |
|---|---|
| `docker compose up --build` | Build FastAPI image and start all services |
| `docker compose up -d` | Start all services in the background |
| `docker compose down` | Stop services but keep database data |
| `docker compose down -v` | Stop services and delete all database data |
| `docker compose ps` | Show container status |
| `docker compose logs -f` | View logs from all services |
| `docker compose logs -f api` | View FastAPI logs |
| `docker compose logs -f mysql` | View MySQL logs |
| `docker compose build api` | Rebuild FastAPI image |
| `docker compose build --no-cache api` | Rebuild FastAPI image without cache |
| `docker compose restart api` | Restart only FastAPI |
| `docker compose config` | Validate the Compose configuration |

## Access Databases

Database ports are not exposed to the host machine. Use Docker Compose commands to access them.

### MySQL

```bash
docker compose exec mysql mysql \
  -u ticketing_user \
  -p \
  event_ticketing
```

Enter the value of `MYSQL_PASSWORD` from `.env`.

Example MySQL commands:

```sql
SHOW TABLES;
SELECT VERSION();
exit;
```

### MongoDB

```bash
docker compose exec mongodb mongosh
```

Example MongoDB commands:

```javascript
use event_ticketing
show collections
exit
```

### Redis

```bash
docker compose exec redis redis-cli
```

Example Redis commands:

```redis
PING
exit
```

## Project Structure

```text
event-ticketing-service/
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── .env.example
├── .gitignore
├── .dockerignore
├── README.md
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── routers/
│   │   ├── events.py
│   │   ├── users.py
│   │   ├── orders.py
│   │   ├── content.py
│   │   └── trending.py
│   └── services/
│
├── sql/
│   ├── create_schema.sql
│   └── seed_data.sql
│
├── mongo/
│   └── init-mongo.js
│
├── redis/
├── scripts/
├── tests/
├── docs/
└── diagram/
```

## Git Workflow

Check changes:

```bash
git status
```

Add files:

```bash
git add .
```

Create a commit:

```bash
git commit -m "feat(scope): describe change"
```

Push the feature branch:

```bash
git push -u origin feature/your-feature-name
```

Open a pull request:

```text
feature branch → develop
```

After review and merge into `develop`, update local code:

```bash
git checkout develop
git pull origin develop
```


## Important Notes

- MySQL is the authoritative source for users, events, ticket types, inventory, orders, and payments.
- MongoDB is the authoritative source for event content, schedules, speakers, performers, tags, and reviews.
- Redis stores temporary cached event responses and trending scores.
- Redis is not the authoritative source for inventory, orders, ticket prices, payments, or users.
- After changing `Dockerfile` or `requirements.txt`, rebuild FastAPI:

```bash
docker compose up --build -d
```

- After changing MySQL or MongoDB initialization scripts during early development, reset the database volumes:

```bash
docker compose down -v
docker compose up --build -d
```

Warning: `docker compose down -v` deletes all local MySQL, MongoDB, and Redis data.