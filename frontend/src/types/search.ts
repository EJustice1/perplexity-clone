export interface SearchResult {
  id: string
  title: string
  snippet: string
  url: string
  source: string
  timestamp: string
  relevance: number
}

export interface SearchQuery {
  query: string
  filters?: {
    dateRange?: string
    source?: string[]
    language?: string
  }
  page?: number
  limit?: number
}

export interface SearchResponse {
  results: SearchResult[]
  total: number
  page: number
  hasMore: boolean
  query: string
  processingTime: number
}

export interface SearchSuggestion {
  text: string
  type: 'query' | 'autocomplete' | 'trending'
  relevance: number
}
