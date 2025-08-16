import { renderHook, act, waitFor } from '@testing-library/react'
import { useSearch } from '../useSearch'
import { apiService } from '../../services/api'

// Mock the API service
jest.mock('../../services/api', () => ({
  apiService: {
    search: jest.fn(),
  },
}))

const mockApiService = apiService as jest.Mocked<typeof apiService>

describe('useSearch', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('should initialize with default state', () => {
    const { result } = renderHook(() => useSearch())

    expect(result.current.isLoading).toBe(false)
    expect(result.current.result).toBe('')
    expect(result.current.error).toBe('')
    expect(result.current.hasSearched).toBe(false)
  })

  it('should successfully execute a search', async () => {
    const mockResponse = { result: 'You searched for: test query' }
    mockApiService.search.mockResolvedValue(mockResponse)

    const { result } = renderHook(() => useSearch())

    await act(async () => {
      await result.current.search('test query')
    })

    expect(result.current.isLoading).toBe(false)
    expect(result.current.result).toBe('You searched for: test query')
    expect(result.current.error).toBe('')
    expect(result.current.hasSearched).toBe(true)
    expect(mockApiService.search).toHaveBeenCalledWith({ query: 'test query' })
  })

  it('should handle empty query gracefully', async () => {
    const { result } = renderHook(() => useSearch())

    await act(async () => {
      await result.current.search('')
    })

    expect(result.current.isLoading).toBe(false)
    expect(result.current.result).toBe('')
    expect(result.current.error).toBe('')
    expect(result.current.hasSearched).toBe(false)
    expect(mockApiService.search).not.toHaveBeenCalled()
  })

  it('should handle whitespace-only query gracefully', async () => {
    const { result } = renderHook(() => useSearch())

    await act(async () => {
      await result.current.search('   ')
    })

    expect(result.current.isLoading).toBe(false)
    expect(result.current.result).toBe('')
    expect(result.current.error).toBe('')
    expect(result.current.hasSearched).toBe(false)
    expect(mockApiService.search).not.toHaveBeenCalled()
  })

  it('should handle API errors gracefully', async () => {
    const apiError = new Error('API Error')
    mockApiService.search.mockRejectedValue(apiError)

    const { result } = renderHook(() => useSearch())

    await act(async () => {
      await result.current.search('test query')
    })

    expect(result.current.isLoading).toBe(false)
    expect(result.current.result).toBe('')
    expect(result.current.error).toBe('API Error')
    expect(result.current.hasSearched).toBe(true)
  })

  it('should handle unknown errors gracefully', async () => {
    // Mock API service to throw an unknown error
    mockApiService.search.mockRejectedValue('Unknown error' as never)

    const { result } = renderHook(() => useSearch())

    await act(async () => {
      await result.current.search('test query')
    })

    expect(result.current.isLoading).toBe(false)
    expect(result.current.result).toBe('')
    expect(result.current.error).toBe('Failed to process search. Please try again.')
    expect(result.current.hasSearched).toBe(true)
  })

  it('should set loading state during search', async () => {
    let resolvePromise: (value: { result: string }) => void
    const promise = new Promise<{ result: string }>((resolve) => {
      resolvePromise = resolve
    })
    mockApiService.search.mockReturnValue(promise)

    const { result } = renderHook(() => useSearch())

    act(() => {
      result.current.search('test query')
    })

    expect(result.current.isLoading).toBe(true)
    expect(result.current.hasSearched).toBe(true)

    // Resolve the promise
    resolvePromise!({ result: 'test result' })

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })
  })

  it('should clear results when clearResults is called', async () => {
    const mockResponse = { result: 'You searched for: test query' }
    mockApiService.search.mockResolvedValue(mockResponse)

    const { result } = renderHook(() => useSearch())

    // First, perform a search
    await act(async () => {
      await result.current.search('test query')
    })

    expect(result.current.result).toBe('You searched for: test query')
    expect(result.current.hasSearched).toBe(true)

    // Then clear results
    act(() => {
      result.current.clearResults()
    })

    expect(result.current.result).toBe('')
    expect(result.current.error).toBe('')
    expect(result.current.hasSearched).toBe(false)
  })

  it('should clear error when starting a new search', async () => {
    // First, cause an error
    mockApiService.search.mockRejectedValue(new Error('First error'))

    const { result } = renderHook(() => useSearch())

    await act(async () => {
      await result.current.search('first query')
    })

    expect(result.current.error).toBe('First error')

    // Then, perform a successful search
    mockApiService.search.mockResolvedValue({ result: 'You searched for: second query' })

    await act(async () => {
      await result.current.search('second query')
    })

    expect(result.current.error).toBe('')
    expect(result.current.result).toBe('You searched for: second query')
  })

  it('should handle multiple rapid searches', async () => {
    const mockResponse = { result: 'You searched for: rapid query' }
    mockApiService.search.mockResolvedValue(mockResponse)

    const { result } = renderHook(() => useSearch())

    // Perform multiple rapid searches
    await act(async () => {
      await Promise.all([
        result.current.search('query 1'),
        result.current.search('query 2'),
        result.current.search('query 3'),
      ])
    })

    // Should have processed the last search
    expect(result.current.result).toBe('You searched for: rapid query')
    expect(mockApiService.search).toHaveBeenCalledTimes(3)
  })
})
