'use client'

import { SearchResult } from '@/types/search'
import { ExternalLink, Clock, Globe, Star, Loader2 } from 'lucide-react'

interface SearchResultsProps {
  results: SearchResult[]
  query: string
  isSearching: boolean
}

export default function SearchResults({ results, query, isSearching }: SearchResultsProps) {
  if (isSearching) {
    return (
      <div className="text-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600 mx-auto mb-4" />
        <p className="text-gray-600">Searching for &ldquo;{query}&rdquo;...</p>
        <p className="text-sm text-gray-500 mt-2">This may take a few seconds</p>
      </div>
    )
  }

  if (results.length === 0) {
    return (
      <div className="text-center py-12">
        <Globe className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">No results found</h3>
        <p className="text-gray-600 mb-4">
          We couldn&apos;t find any results for &ldquo;{query}&rdquo;
        </p>
        <p className="text-sm text-gray-500">
          Try different keywords or check your spelling
        </p>
      </div>
    )
  }

  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60))
    
    if (diffInHours < 1) return 'Just now'
    if (diffInHours < 24) return `${diffInHours} hours ago`
    if (diffInHours < 48) return 'Yesterday'
    return date.toLocaleDateString()
  }

  const getRelevanceColor = (relevance: number) => {
    if (relevance >= 0.9) return 'text-green-600'
    if (relevance >= 0.7) return 'text-blue-600'
    if (relevance >= 0.5) return 'text-yellow-600'
    return 'text-gray-500'
  }

  return (
    <div className="space-y-6">
      {/* Results Header */}
      <div className="border-b border-gray-200 pb-4">
        <h2 className="text-2xl font-semibold text-gray-900 mb-2">
          Search Results for &ldquo;{query}&rdquo;
        </h2>
        <p className="text-gray-600">
          Found {results.length} result{results.length !== 1 ? 's' : ''}
        </p>
      </div>

      {/* Results List */}
      <div className="space-y-6">
        {results.map((result) => (
          <div
            key={result.id}
            className="bg-white p-6 rounded-xl border border-gray-200 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 mb-2 hover:text-blue-600 transition-colors">
                  <a
                    href={result.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center group"
                  >
                    {result.title}
                    <ExternalLink className="w-4 h-4 ml-2 text-gray-400 group-hover:text-blue-600 transition-colors" />
                  </a>
                </h3>
                
                <p className="text-gray-700 mb-3 leading-relaxed">
                  {result.snippet}
                </p>
                
                <div className="flex items-center space-x-4 text-sm text-gray-500">
                  <div className="flex items-center">
                    <Globe className="w-4 h-4 mr-1" />
                    <span>{result.source}</span>
                  </div>
                  
                  <div className="flex items-center">
                    <Clock className="w-4 h-4 mr-1" />
                    <span>{formatDate(result.timestamp)}</span>
                  </div>
                  
                  <div className="flex items-center">
                    <Star className={`w-4 h-4 mr-1 ${getRelevanceColor(result.relevance)}`} />
                    <span className={getRelevanceColor(result.relevance)}>
                      {Math.round(result.relevance * 100)}% relevant
                    </span>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="flex items-center justify-between pt-3 border-t border-gray-100">
              <a
                href={result.url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
              >
                Visit Source
                <ExternalLink className="w-4 h-4 ml-2" />
              </a>
              
              <div className="text-xs text-gray-400">
                ID: {result.id}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Load More Button */}
      {results.length > 0 && (
        <div className="text-center pt-6">
          <button className="px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
            Load More Results
          </button>
        </div>
      )}
    </div>
  )
}
