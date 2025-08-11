# Perplexity Clone Frontend

Modern AI-powered search interface built with Next.js and TypeScript.

## Features

- **Next.js 14**: React framework with App Router
- **TypeScript**: Full type safety and better developer experience
- **Tailwind CSS**: Utility-first CSS framework
- **Responsive Design**: Mobile-first approach
- **Search Interface**: AI-powered search capabilities

## Quick Start

### Local Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

### Using Docker

```bash
# Build and run
docker build -t perplexity-frontend .
docker run -p 3000:3000 perplexity-frontend
```

## Project Structure

```
frontend/
├── src/
│   ├── app/           # Next.js App Router pages
│   ├── components/    # Reusable React components
│   ├── lib/          # Utility functions and libraries
│   └── types/        # TypeScript type definitions
├── public/            # Static assets
├── package.json       # Dependencies and scripts
└── Dockerfile         # Container configuration
```

## Components

### SearchBar
Main search input component with AI-powered suggestions.

### SearchResults
Displays search results with rich formatting and metadata.

## Configuration

Environment variables:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development
```

## Development

### Code Quality

```bash
# Lint code
npm run lint

# Type check
npm run type-check

# Format code
npm run format
```

### Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript compiler

## Styling

The project uses Tailwind CSS for styling:

- **Utility Classes**: Rapid UI development
- **Responsive Design**: Mobile-first approach
- **Custom Components**: Reusable styled components
- **Dark Mode**: Built-in theme support

## API Integration

The frontend communicates with the backend API:

- **Search Endpoints**: AI-powered search functionality
- **Health Checks**: Service status monitoring
- **Error Handling**: Graceful fallbacks and user feedback

## Deployment

### Vercel (Recommended)

```bash
# Deploy to Vercel
vercel --prod
```

### Docker

```bash
# Build production image
docker build -t perplexity-frontend .

# Run container
docker run -p 3000:3000 perplexity-frontend
```

### Environment Variables

Set production environment variables:

```bash
NEXT_PUBLIC_API_URL=https://your-api-domain.com
NODE_ENV=production
```

## Performance

- **Image Optimization**: Next.js built-in image optimization
- **Code Splitting**: Automatic route-based code splitting
- **Static Generation**: Pre-rendered pages for better SEO
- **Bundle Analysis**: Webpack bundle analyzer integration

## Contributing

1. Follow the established component patterns
2. Use TypeScript for all new code
3. Include proper prop types and interfaces
4. Test components across different screen sizes
5. Follow the existing styling conventions
