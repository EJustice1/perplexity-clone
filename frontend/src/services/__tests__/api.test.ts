import { apiService, SearchRequest, SearchResponse, WebSearchResult } from '../api'

// Mock fetch globally
global.fetch = jest.fn()

describe('ApiService', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('search', () => {
    it('should successfully make a search request', async () => {
      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({ 
          sources: [
            {
              title: 'Test Result 1',
              url: 'https://example1.com',
              snippet: 'Test snippet 1',
              source: 'web_search'
            }
          ]
        }),
      }
      ;(global.fetch as jest.Mock).mockResolvedValue(mockResponse)

      const request: SearchRequest = { query: 'test query' }
      const result = await apiService.search(request)

      expect(result).toEqual({ 
        sources: [
          {
            title: 'Test Result 1',
            url: 'https://example1.com',
            snippet: 'Test snippet 1',
            source: 'web_search'
          }
        ]
      })
      expect(global.fetch).toHaveBeenCalledWith('/api/v1/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
      })
    })

    it('should handle HTTP errors', async () => {
      const mockResponse = {
        ok: false,
        status: 400,
      }
      ;(global.fetch as jest.Mock).mockResolvedValue(mockResponse)

      const request: SearchRequest = { query: 'test query' }

      await expect(apiService.search(request)).rejects.toThrow('Failed to search: HTTP error! status: 400')
    })

    it('should handle network errors', async () => {
      const networkError = new Error('Network error')
      ;(global.fetch as jest.Mock).mockRejectedValue(networkError)

      const request: SearchRequest = { query: 'test query' }

      await expect(apiService.search(request)).rejects.toThrow('Failed to search: Network error')
    })

    it('should handle unknown errors', async () => {
      ;(global.fetch as jest.Mock).mockRejectedValue('Unknown error')

      const request: SearchRequest = { query: 'test query' }

      await expect(apiService.search(request)).rejects.toThrow('Failed to search. Please try again.')
    })

    it('should use the correct API endpoint', async () => {
      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({ 
          sources: [
            {
              title: 'Test Result',
              url: 'https://example.com',
              snippet: 'Test snippet',
              source: 'web_search'
            }
          ]
        }),
      }
      ;(global.fetch as jest.Mock).mockResolvedValue(mockResponse)

      const request: SearchRequest = { query: 'test' }
      await apiService.search(request)

      expect(global.fetch).toHaveBeenCalledWith('/api/v1/search', expect.any(Object))
    })
  })

  describe('SearchRequest interface', () => {
    it('should have the correct structure', () => {
      const request: SearchRequest = { query: 'test query' }
      expect(request).toHaveProperty('query')
      expect(typeof request.query).toBe('string')
    })
  })

  describe('WebSearchResult interface', () => {
    it('should have the correct structure', () => {
      const result: WebSearchResult = { 
        title: 'Test Title',
        url: 'https://example.com',
        snippet: 'Test snippet',
        source: 'web_search'
      }
      expect(result).toHaveProperty('title')
      expect(result).toHaveProperty('url')
      expect(result).toHaveProperty('snippet')
      expect(result).toHaveProperty('source')
      expect(typeof result.title).toBe('string')
      expect(typeof result.url).toBe('string')
      expect(typeof result.snippet).toBe('string')
      expect(typeof result.source).toBe('string')
    })
  })

  describe('SearchResponse interface', () => {
    it('should have the correct structure', () => {
      const response: SearchResponse = { 
        sources: [
          {
            title: 'Test Title',
            url: 'https://example.com',
            snippet: 'Test snippet',
            source: 'web_search'
          }
        ]
      }
      expect(response).toHaveProperty('sources')
      expect(Array.isArray(response.sources)).toBe(true)
      expect(response.sources).toHaveLength(1)
      expect(response.sources[0]).toHaveProperty('title')
      expect(response.sources[0]).toHaveProperty('url')
      expect(response.sources[0]).toHaveProperty('snippet')
      expect(response.sources[0]).toHaveProperty('source')
    })
  })
})
