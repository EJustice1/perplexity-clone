'use client'

import { useState } from 'react'
import { Search, Sparkles, MessageSquare, Zap } from 'lucide-react'
import SearchBar from '@/components/SearchBar'
import SearchResults from '@/components/SearchResults'
import { SearchResult } from '@/types/search'

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('')
  const [isSearching, setIsSearching] = useState(false)
  const [searchResults, setSearchResults] = useState<SearchResult[]>([])
  const [hasSearched, setHasSearched] = useState(false)

  const handleSearch = async (query: string) => {
    if (!query.trim()) return
    
    setIsSearching(true)
    setSearchQuery(query)
    setHasSearched(true)
    
    try {
      // TODO: Replace with actual API call to your FastAPI backend
      // const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`)
      // const results = await response.json()
      
      // Mock results for now
      const mockResults: SearchResult[] = [
        {
          id: '1',
          title: 'Understanding AI and Machine Learning',
          snippet: 'Artificial Intelligence (AI) and Machine Learning (ML) are transforming how we interact with technology...',
          url: 'https://example.com/ai-ml-guide',
          source: 'AI Research Institute',
          timestamp: new Date().toISOString(),
          relevance: 0.95
        },
        {
          id: '2',
          title: 'The Future of Search Technology',
          snippet: 'Search engines are evolving beyond simple keyword matching to understand context and intent...',
          url: 'https://example.com/search-future',
          source: 'Tech Insights',
          timestamp: new Date().toISOString(),
          relevance: 0.87
        }
      ]
      
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      setSearchResults(mockResults)
    } catch (error) {
      console.error('Search failed:', error)
      setSearchResults([])
    } finally {
      setIsSearching(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <Sparkles className="w-8 h-8 text-blue-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-900">Perplexity Clone</h1>
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Your AI-powered search assistant that understands context and provides intelligent answers
          </p>
        </header>

        {/* Search Section */}
        <div className="max-w-4xl mx-auto mb-12">
          <SearchBar 
            onSearch={handleSearch}
            isSearching={isSearching}
            placeholder="Ask anything... Search the web, get AI-powered insights"
          />
          
          {/* Search Features */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-6 bg-white rounded-xl shadow-sm border border-gray-200">
              <MessageSquare className="w-8 h-8 text-blue-600 mx-auto mb-3" />
              <h3 className="font-semibold text-gray-900 mb-2">Conversational AI</h3>
              <p className="text-sm text-gray-600">Ask follow-up questions and get contextual responses</p>
            </div>
            
            <div className="text-center p-6 bg-white rounded-xl shadow-sm border border-gray-200">
              <Zap className="w-8 h-8 text-green-600 mx-auto mb-3" />
              <h3 className="font-semibold text-gray-900 mb-2">Real-time Search</h3>
              <p className="text-sm text-gray-600">Get the latest information from across the web</p>
            </div>
            
            <div className="text-center p-6 bg-white rounded-xl shadow-sm border border-gray-200">
              <Search className="w-8 h-8 text-purple-600 mx-auto mb-3" />
              <h3 className="font-semibold text-gray-900 mb-2">Smart Results</h3>
              <p className="text-sm text-gray-600">AI-curated answers with source citations</p>
            </div>
          </div>
        </div>

        {/* Search Results */}
        {hasSearched && (
          <div className="max-w-4xl mx-auto">
            <SearchResults 
              results={searchResults}
              query={searchQuery}
              isSearching={isSearching}
            />
          </div>
        )}

        {/* Footer */}
        <footer className="text-center mt-16 text-gray-500">
          <p>Powered by Next.js, TypeScript, and Tailwind CSS</p>
        </footer>
      </div>
    </main>
  )
}
