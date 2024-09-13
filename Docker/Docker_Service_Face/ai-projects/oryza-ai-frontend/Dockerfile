FROM node:22.6 AS build

WORKDIR /app

# Copy package.json and package-lock.json to leverage Docker cache
COPY package*.json ./

# Install dependencies (including development dependencies)
RUN npm install --legacy-peer-deps

# Copy the rest of the application code
COPY . .

# Build the Next.js application (adjust command if necessary)
RUN npm run build

# Stage 2: Production stage
FROM node:22.6-alpine AS production

WORKDIR /app

# Copy only the production dependencies from the build stage
COPY --from=build /app/node_modules /app/node_modules

# Copy built application files from the build stage
COPY --from=build /app/.next /app/.next
COPY --from=build /app/public /app/public
COPY --from=build /app/next.config.js /app/next.config.js
COPY --from=build /app/package.json /app/package.json

# Install only the production dependencies
RUN npm install --production --legacy-peer-deps

# Expose the port Next.js runs on
EXPOSE 3000

# Start the application
CMD ["npm", "start"]