import '@testing-library/jest-dom'

// Mock Next.js router
jest.mock('next/navigation', () => ({
  useRouter() {
    return {
      push: jest.fn(),
      replace: jest.fn(),
      prefetch: jest.fn(),
      back: jest.fn(),
      forward: jest.fn(),
      refresh: jest.fn(),
    }
  },
  useSearchParams() {
    return new URLSearchParams()
  },
  usePathname() {
    return '/'
  },
}))

// Mock Next.js image component
jest.mock('next/image', () => ({
  __esModule: true,
  default: (props) => {
    // eslint-disable-next-line @next/next/no-img-element
    return <img {...props} />
  },
}))

// Mock Next.js server components
jest.mock('next/server', () => ({
  NextRequest: class MockNextRequest {
    constructor(input, init = {}) {
      this.url = input
      this.method = init.method || 'GET'
      this.body = init.body || null
      this.headers = {
        get: jest.fn().mockReturnValue(init.headers?.['Content-Type'] || 'application/json'),
      }
      this.json = jest.fn().mockResolvedValue(JSON.parse(init.body || '{}'))
    }
  },
  NextResponse: {
    json: jest.fn().mockImplementation((data, options = {}) => ({
      status: options.status || 200,
      json: jest.fn().mockResolvedValue(data),
      headers: {
        get: jest.fn().mockReturnValue(null),
      },
    })),
  },
}))

// Global test setup
global.ResizeObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}))

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(), // deprecated
    removeListener: jest.fn(), // deprecated
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
})
