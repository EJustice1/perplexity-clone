'use client'

import { useState, useRef, useEffect } from 'react'
import { Search, X, Loader2 } from 'lucide-react'
import { SearchSuggestion } from '@/types/search'

interface SearchBarProps {
  onSearch: (query: string) => void
  isSearching: boolean
  placeholder?: string
}

export default function SearchBar({ onSearch, isSearching, placeholder }: SearchBarProps) {
  const [query, setQuery] = useState('')
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [suggestions, setSuggestions] = useState<SearchSuggestion[]>([])
  const searchRef = useRef<HTMLDivElement>(null)

  // Mock suggestions - replace with actual API call
  const mockSuggestions: SearchSuggestion[] = [
    { text: 'What is artificial intelligence?', type: 'trending', relevance: 0.9 },
    { text: 'Latest developments in machine learning', type: 'trending', relevance: 0.85 },
    { text: 'How does quantum computing work?', type: 'trending', relevance: 0.8 },
    { text: 'Climate change solutions 2024', type: 'trending', relevance: 0.75 },
  ]

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setShowSuggestions(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      onSearch(query.trim())
      setShowSuggestions(false)
    }
  }

  const handleSuggestionClick = (suggestion: string) => {
    setQuery(suggestion)
    onSearch(suggestion)
    setShowSuggestions(false)
  }

  const handleInputChange = (value: string) => {
    setQuery(value)
    if (value.trim()) {
      setSuggestions(mockSuggestions.filter(s => 
        s.text.toLowerCase().includes(value.toLowerCase())
      ))
      setShowSuggestions(true)
    } else {
      setShowSuggestions(false)
    }
  }

  const clearQuery = () => {
    setQuery('')
    setShowSuggestions(false)
  }

  return (
    <div className="relative" ref={searchRef}>
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          
          <input
            type="text"
            value={query}
            onChange={(e) => handleInputChange(e.target.value)}
            placeholder={placeholder || "Search..."}
            className="w-full pl-12 pr-12 py-4 text-lg border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm hover:shadow-md transition-shadow"
            disabled={isSearching}
          />
          
          {query && (
            <button
              type="button"
              onClick={clearQuery}
              className="absolute right-16 top-1/2 transform -translate-y-1/2 p-1 hover:bg-gray-100 rounded-full transition-colors"
            >
              <X className="w-4 h-4 text-gray-400" />
            </button>
          )}
          
          <button
            type="submit"
            disabled={!query.trim() || isSearching}
            className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-blue-600 text-white px-6 py-2 rounded-xl hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            {isSearching ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              'Search'
            )}
          </button>
        </div>
      </form>

      {/* Search Suggestions */}
      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-xl shadow-lg z-10 max-h-80 overflow-y-auto">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => handleSuggestionClick(suggestion.text)}
              className="w-full text-left px-4 py-3 hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-b-0"
            >
              <div className="flex items-center">
                <Search className="w-4 h-4 text-gray-400 mr-3" />
                <div>
                  <p className="text-gray-900">{suggestion.text}</p>
                  <p className="text-sm text-gray-500 capitalize">{suggestion.type}</p>
                </div>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
