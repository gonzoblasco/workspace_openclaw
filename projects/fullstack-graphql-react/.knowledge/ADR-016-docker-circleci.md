# ADR-016: Docker Multi-Stage Build for Production

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Full-Stack Web Development with GraphQL and React (2nd Ed.), Chapter 12
**Scope:** Global

## Context

The book uses Docker for containerization with CircleCI for CI/CD and AWS ECS for deployment. The Docker setup uses multi-stage builds to keep the production image small.

## Decision

Use Docker multi-stage builds with Node 22 base image. Use CircleCI for CI/CD pipeline with automated testing, Docker image building, and ECS deployment.

## Key Changes from Book

| Book (2020) | Modern (Aug 2026) | Reason |
|---|---|---|
| Node 14 base image | Node 22 LTS | Current LTS |
| Sequelize CLI for migrations | Drizzle Kit (`drizzle-kit push`) | ORM change |
| `npm run build` (webpack) | Vite build | Bundler change |
| `sequelize db:migrate` | `npx drizzle-kit push` | ORM change |
| CircleCI `circleci/node:14` | `cimg/node:22.0` | Current CircleCI image |
| `circleci/mysql:8.0.4` | `cimg/mysql:8.0` | Current CircleCI image |

## CI/CD Pipeline

```
1. Push to GitHub
2. CircleCI triggers pipeline
3. Test job: install deps → wait for MySQL → run migrations → run tests
4. Build job: build Docker image → push to Amazon ECR
5. Deploy job: update ECS task definition → update service
6. New version live on AWS ALB
```

## Files Created

- `Dockerfile` — Multi-stage build (build → production)
- `.dockerignore` — Excludes node_modules, .env, dist
- `.circleci/config.yml` — CircleCI pipeline with test, build, deploy jobs

## References

- https://docs.docker.com/develop/develop-images/multistage-build/
- https://circleci.com/docs/
- https://aws.amazon.com/ecs/
