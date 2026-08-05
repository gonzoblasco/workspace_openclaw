# Chapter 12: Continuous Deployment with CircleCI and AWS

## Core Concepts

1. **Docker:** Containerization platform for consistent environments
2. **Multi-stage builds:** Separate build environment from production image
3. **Dockerfile:** Instructions to build a Docker image
4. **Amazon ECR:** Docker registry for storing images
5. **Amazon ECS:** Container orchestration service
6. **AWS ALB:** Application Load Balancer for traffic distribution
7. **Amazon RDS:** Managed relational database service
8. **CircleCI:** CI/CD platform with automated pipelines
9. **CI/CD Pipeline:** Test → Build → Deploy automation

## CI/CD Pipeline Flow

```
Git Push → CircleCI → Test → Build Docker Image → Push to ECR → Deploy to ECS
```

## Key Changes from Book

| Book (2020) | Modern (Aug 2026) | Reason |
|---|---|---|
| Node 14 | Node 22 LTS | Current LTS |
| Sequelize CLI | Drizzle Kit | ORM change |
| webpack build | Vite build | Bundler change |
| `circleci/node:14` | `cimg/node:22.0` | Current image |
| `circleci/mysql:8.0.4` | `cimg/mysql:8.0` | Current image |

## Files Created

- `Dockerfile` — Multi-stage Docker build
- `.dockerignore` — Excludes unnecessary files
- `.circleci/config.yml` — CircleCI pipeline configuration

## Running Locally with Docker

```bash
# Build the image
docker build -t graphbook .

# Run the container
docker run -p 8000:8000 -d \
  -e JWT_SECRET="***" \
  -e NODE_ENV=development \
  graphbook
```

## AWS Services Used

| Service | Purpose |
|---|---|
| Amazon ECR | Docker image registry |
| Amazon ECS | Container orchestration |
| AWS ALB | Load balancing |
| Amazon RDS | Managed MySQL/PostgreSQL |
| CloudWatch | Logging and monitoring |

## CircleCI Pipeline

1. **Test:** Install deps → wait for MySQL → run migrations → run tests
2. **Build:** Build Docker image → push to ECR
3. **Deploy:** Update ECS task definition → update service
