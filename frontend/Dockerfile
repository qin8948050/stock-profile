# Stage 1: Build the frontend application
FROM m.daocloud.io/docker.io/node:22-alpine AS builder

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json ./

RUN npm config set registry https://registry.npmmirror.com
# Install dependencies
RUN npm install

# Copy the rest of the application source code
COPY . .

# Build the application for production
RUN npm run build

# Stage 2: Production image
FROM m.daocloud.io/docker.io/node:22-alpine AS runner

WORKDIR /app

# Set environment variables
ENV NODE_ENV=production

# Create a non-root user for security
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Copy the standalone folder from the builder stage
COPY --from=builder /app/.next/standalone ./

# Copy the public and static folders
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/static ./.next/static

# Change ownership of the files to the non-root user
RUN chown -R nextjs:nodejs /app

# Switch to the non-root user
USER nextjs

# Expose the port the app will run on
EXPOSE 3000

# Command to start the server
CMD ["node", "server.js"]
