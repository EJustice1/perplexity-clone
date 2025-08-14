FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the application for production
# NEXT_PUBLIC_API_URL must be provided as build argument for the target environment
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Validate that the backend URL is provided
RUN if [ -z "$NEXT_PUBLIC_API_URL" ]; then \
      echo "ERROR: NEXT_PUBLIC_API_URL build argument is required"; \
      exit 1; \
    fi

# Create .env.local file for Next.js build
RUN echo "NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL" > .env.local
RUN echo "Building for backend URL: $NEXT_PUBLIC_API_URL"

RUN npm run build

# Production stage
FROM node:20-alpine AS runner

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install only production dependencies
RUN npm install --omit=dev

# Copy built application from builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.js ./

# Expose port
EXPOSE 3000

# Start the production server
CMD ["npm", "start"]
