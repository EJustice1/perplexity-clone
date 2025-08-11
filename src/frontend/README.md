# Perplexity Clone - Next.js Frontend

A modern, responsive frontend for the Perplexity Clone application built with Next.js 14, TypeScript, and Tailwind CSS.

## 🚀 Features

- **Modern UI/UX** - Clean, professional design with smooth animations
- **TypeScript** - Full type safety and better developer experience
- **Responsive Design** - Works perfectly on all devices
- **Search Interface** - AI-powered search with suggestions and results
- **Real-time Updates** - Live search results and loading states
- **API Integration** - Seamless integration with FastAPI backend
- **Performance Optimized** - Built with Next.js 14 App Router

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **UI Components**: Headless UI
- **State Management**: React Hooks

## 📁 Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── components/             # Reusable UI components
│   ├── SearchBar.tsx      # Search input component
│   └── SearchResults.tsx  # Search results display
├── lib/                    # Utilities and API clients
│   └── api.ts             # API integration
├── types/                  # TypeScript type definitions
│   └── search.ts          # Search-related types
└── package.json            # Dependencies and scripts
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- FastAPI backend running (optional for development)

### Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd src/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env.local
   ```
   
   Edit `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🔧 Development

### Available Scripts

- **`npm run dev`** - Start development server
- **`npm run build`** - Build for production
- **`npm run start`** - Start production server
- **`npm run lint`** - Run ESLint
- **`npm run type-check`** - Run TypeScript compiler

### Development Workflow

1. **Component Development** - Create new components in `src/components/`
2. **Type Definitions** - Add new types in `src/types/`
3. **API Integration** - Extend API client in `src/lib/api.ts`
4. **Styling** - Use Tailwind CSS classes for consistent design

### Code Style

- **TypeScript** - Use strict typing for all components
- **Tailwind CSS** - Utility-first CSS approach
- **Component Structure** - Functional components with hooks
- **Error Handling** - Proper error boundaries and user feedback

## 🌐 API Integration

### Backend Connection

The frontend is designed to work with your FastAPI backend:

- **Base URL**: Configurable via `NEXT_PUBLIC_API_URL`
- **Endpoints**: Health, metrics, search, suggestions
- **Error Handling**: Graceful fallbacks and user notifications
- **Authentication**: Ready for future JWT integration

### API Endpoints

- **`/health`** - Backend health check
- **`/metrics`** - Prometheus metrics
- **`/search`** - Search functionality
- **`/suggestions`** - Search suggestions
- **`/trending`** - Trending searches

## 🎨 UI Components

### SearchBar Component

- **Smart Input** - Auto-complete and suggestions
- **Loading States** - Visual feedback during search
- **Accessibility** - Keyboard navigation and screen reader support
- **Responsive** - Adapts to different screen sizes

### SearchResults Component

- **Rich Results** - Title, snippet, source, timestamp
- **Relevance Scoring** - Visual indicators for result quality
- **External Links** - Safe opening of source URLs
- **Pagination** - Load more results functionality

## 📱 Responsive Design

- **Mobile First** - Optimized for mobile devices
- **Breakpoints** - Tailwind CSS responsive utilities
- **Touch Friendly** - Proper touch targets and gestures
- **Progressive Enhancement** - Works on all devices

## 🔒 Security Features

- **CSP Ready** - Content Security Policy support
- **XSS Protection** - Safe rendering of user content
- **External Links** - `rel="noopener noreferrer"` for security
- **Input Validation** - Client-side validation and sanitization

## 🚀 Deployment

### Production Build

1. **Build the application:**
   ```bash
   npm run build
   ```

2. **Start production server:**
   ```bash
   npm run start
   ```

### Environment Variables

- **Development**: `.env.local`
- **Production**: Set in your hosting platform
- **Required**: `NEXT_PUBLIC_API_URL`

### Hosting Options

- **Vercel** - Zero-config deployment
- **Netlify** - Easy static hosting
- **Docker** - Containerized deployment
- **Self-hosted** - Any Node.js server

## 🔮 Future Enhancements

- **Authentication** - User accounts and search history
- **Advanced Search** - Filters, date ranges, source selection
- **Dark Mode** - Theme switching capability
- **Offline Support** - Service worker for offline functionality
- **Real-time Updates** - WebSocket integration for live results
- **Analytics** - User behavior tracking and insights

## 🤝 Contributing

1. **Follow the established patterns** in existing components
2. **Use TypeScript** for all new code
3. **Add proper error handling** and user feedback
4. **Test on multiple devices** and screen sizes
5. **Update documentation** for new features

## 📚 Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [React Documentation](https://react.dev/)

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Check if backend is running
   - Verify `NEXT_PUBLIC_API_URL` in environment
   - Check browser console for CORS errors

2. **Build Errors**
   - Clear `.next` folder and rebuild
   - Check TypeScript errors with `npm run type-check`
   - Verify all dependencies are installed

3. **Styling Issues**
   - Ensure Tailwind CSS is properly configured
   - Check for CSS conflicts in `globals.css`
   - Verify responsive breakpoints

### Getting Help

- Check the browser console for error messages
- Review the FastAPI backend logs
- Check network tab for API request/response details

---

**Built with ❤️ using Next.js, TypeScript, and Tailwind CSS**
