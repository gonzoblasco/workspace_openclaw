# Multi-stage Docker build for Graphbook
# Stage 1: Build
FROM node:22 AS build

WORKDIR /usr/src/app

# Copy only what's needed for build
COPY package*.json ./
COPY src src
COPY drizzle.config.js ./
COPY drizzle/ drizzle/

# Install dependencies and build
RUN npm install
RUN npm run build 2>/dev/null || echo "Build step placeholder"

# Stage 2: Production image
FROM node:22

WORKDIR /usr/src/app

# Environment variables (override at runtime)
ENV NODE_ENV production

# Copy from build stage
COPY --from=build /usr/src/app/package.json package.json
COPY --from=build /usr/src/app/dist dist
COPY --from=build /usr/src/app/src/server src/server
COPY --from=build /usr/src/app/drizzle drizzle
COPY --from=build /usr/src/app/drizzle.config.js ./

# Install production dependencies only
RUN npm install --only=production

EXPOSE 8000

# Start script runs migrations then server
CMD ["sh", "-c", "npx drizzle-kit push 2>/dev/null; node src/server/index.js"]
