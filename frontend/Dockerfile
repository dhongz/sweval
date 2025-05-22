FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Expose the port Next.js runs on
EXPOSE 3000

# Start the application in development mode with HTTPS
CMD ["npm", "run", "dev", "--", "--port", "3000", "--hostname", "0.0.0.0"]