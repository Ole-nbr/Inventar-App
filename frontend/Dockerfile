# Development image: the source code is mounted by docker-compose.yml for hot reload.
FROM node:24-slim

WORKDIR /app

# Dependencies first, so this layer is only rebuilt when the lockfile changes.
COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 5173

# --host: listen on all interfaces, otherwise the port mapping cannot reach Vite.
CMD ["npm", "run", "dev", "--", "--host"]
