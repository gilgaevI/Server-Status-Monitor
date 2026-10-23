Server Status Monitor
A DevOps pet project for monitoring the availability of web resources. It covers the full development lifecycle, including CI/CD, containerization, database integration, caching, reverse proxy, and a monitoring stack.

Architecture
The project consists of the following microservices:

App: A Python Flask application that checks the status of target URLs.

Database: PostgreSQL is used to store the history of all checks.

Cache: Redis caches the latest status for 30 seconds to reduce database load.

Reverse Proxy: Nginx routes external traffic to the Flask application.

Monitoring: Prometheus collects metrics, and Grafana is used for visualization.

CI/CD: GitHub Actions automatically tests, builds, and pushes the Docker image to GHCR.

Tech Stack
Backend: Python 3.11, Flask, Gunicorn

Database: PostgreSQL 16

Cache: Redis 7

Infrastructure: Docker, Docker Compose

CI/CD: GitHub Actions, GitHub Container Registry (GHCR)

Monitoring: Prometheus, Grafana

How to Run Locally
Clone the repository:

bash
git clone https://github.com/gilgaevi/Server-Status-Monitor.git
cd Server-Status-Monitor
Start the whole stack:

bash
docker compose up -d
Access the services:

Status Board: http://localhost

Prometheus: http://localhost:9090

Grafana: http://localhost:3000 (admin/admin)

CI/CD Pipeline
On every push to the main branch, GitHub Actions performs the following steps:

Builds the Docker image.

Pushes it to GitHub Container Registry (ghcr.io).

Runs integration tests by spinning up the entire docker-compose stack and checking health endpoints.

Monitoring
The application exposes custom Prometheus metrics at /metrics. You can track the total number of checks and their statuses (UP/DOWN) in real-time using the pre-configured Grafana dashboard.

