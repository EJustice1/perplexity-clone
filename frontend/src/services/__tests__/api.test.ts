import { apiService, SearchRequest, SearchResponse } from '../api'

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
        json: jest.fn().mockResolvedValue({ result: 'You searched for: test query' }),
      }
      ;(global.fetch as jest.Mock).mockResolvedValue(mockResponse)

      const request: SearchRequest = { query: 'test query' }
      const result = await apiService.search(request)

      expect(result).toEqual({ result: 'You searched for: test query' })
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
        json: jest.fn().mockResolvedValue({ result: 'test' }),
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

  describe('SearchResponse interface', () => {
    it('should have the correct structure', () => {
      const response: SearchResponse = { result: 'test result' }
      expect(response).toHaveProperty('result')
      expect(typeof response.result).toBe('string')
    })
  })
})
