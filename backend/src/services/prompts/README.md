# Intelligent Prompting System

This directory contains the intelligent prompt system for LLM services. The system implements a unified three-stage approach that combines question analysis, search optimization, and intelligent response generation.

## System Overview

### **Integrated Three-Stage System** ⭐ **NEW**
1. **Question Analysis & Search Optimization** - Determines response format, detail level, AND enhanced search queries
2. **Intelligent Synthesis** - Generates content based on question type and user needs
3. **Adaptive Refinement** - Applies appropriate formatting for the chosen response style

## Key Innovation: Unified Analysis

**The system now performs a single analysis that serves both purposes:**
- **Response Optimization**: Determines optimal format and detail level
- **Search Enhancement**: Provides enhanced search queries for better web results
- **Source Prioritization**: Identifies the best types of sources for each question

This eliminates redundancy and ensures consistency between search strategy and response format.

## Prompt Files

### Core System
- **`question_analysis.txt`** - **NEW**: Unified analysis for response format AND search optimization
- **`intelligent_synthesis.txt`** - Generates adaptive content based on comprehensive analysis
- **`adaptive_refinement.txt`** - Applies format-appropriate refinement with search context

### Utility Prompts
- **`query_enhancement.txt`** - **DEPRECATED**: Functionality now integrated into question analysis

## Question Types and Response Strategies

### 1. FACTUAL Questions (Low Detail)
- **Examples**: "What is the capital of France?", "Who invented the telephone?"
- **Goal**: Quick, direct answer
- **Format**: Single sentence or short paragraph
- **Search Enhancement**: Add "official", "facts", "definition" to search terms
- **Source Priority**: Government websites, official databases, encyclopedias

### 2. EXPLANATORY Questions (Medium Detail)
- **Examples**: "How does photosynthesis work?", "Why do leaves change color?"
- **Goal**: Clear understanding with key concepts
- **Format**: Concise explanation with bullet points for key concepts
- **Search Enhancement**: Add "how to", "explanation", "guide" to search terms
- **Source Priority**: Educational websites, expert blogs, tutorial sites

### 3. COMPARATIVE Questions (High Detail)
- **Examples**: "Compare iPhone vs Android", "What's the difference between X and Y?"
- **Goal**: Clear comparison and analysis
- **Format**: Structured comparison with tables when beneficial
- **Search Enhancement**: Add "vs", "comparison", "difference" to search terms
- **Source Priority**: Comparison articles, review sites, analysis pieces

### 4. COMPREHENSIVE Questions (High Detail)
- **Examples**: "Tell me everything about climate change", "Explain the history of..."
- **Goal**: Complete coverage of the topic
- **Format**: Organized sections with appropriate detail level
- **Search Enhancement**: Add "complete guide", "overview", "everything about" to search terms
- **Source Priority**: Comprehensive guides, overview articles, multiple sources

## Search Enhancement Examples

### Before (Basic Search)
- "capital of France" → Generic results
- "photosynthesis" → Mixed quality content
- "iPhone Android" → Unclear comparison focus

### After (Enhanced Search)
- "capital of France official facts government" → Authoritative sources
- "how photosynthesis works explanation guide process" → Educational content
- "iPhone vs Android comparison features table" → Structured comparisons

## Benefits of the Integrated System

### 1. **Eliminates Redundancy**
- Single analysis serves both search and response optimization
- No duplicate question analysis
- Consistent understanding across all stages

### 2. **Better Search Results**
- Enhanced queries based on question type
- Source prioritization for higher quality content
- Context-aware search strategies

### 3. **Improved User Experience**
- Responses match the quality of sources found
- Consistent detail level and format
- Better source attribution and credibility

### 4. **Efficiency Gains**
- Single LLM call for analysis instead of two
- Reduced latency and cost
- Simplified system architecture

## Technical Implementation

### Service Architecture
- **`IntelligentLLMSynthesisService`** - Three-stage service with integrated analysis
- **`LLMSynthesisService`** - Simplified wrapper using intelligent system
- **Factory Pattern** - Clean service creation

### Data Flow
1. **Question Analysis** → Response format + Search enhancement + Source priorities
2. **Web Search** → Uses enhanced query and source priorities
3. **Content Extraction** → Focuses on prioritized source types
4. **Intelligent Synthesis** → Uses analysis for optimal content generation
5. **Adaptive Refinement** → Applies format with search context

### Error Handling
- **Graceful degradation** - Falls back to basic functionality if analysis fails
- **Comprehensive logging** - Tracks analysis results and search enhancements
- **User feedback** - Clear error messages and fallback responses

## Migration from Legacy System

The system has been completely refactored to remove legacy functionality:

1. **Removed**: Two-stage synthesis system
2. **Removed**: Separate query enhancement
3. **Removed**: Configuration options for legacy system
4. **Simplified**: Single service with integrated functionality

## Future Enhancements

### Planned Features
- **Custom search strategies** - User-defined enhancement patterns
- **Multi-language support** - Search enhancement in different languages
- **A/B testing** - Compare different enhancement strategies
- **Performance metrics** - Measure search quality improvements

### Extensibility
- **Plugin system** - Add custom question analyzers
- **Search provider integration** - Direct integration with search APIs
- **Learning system** - Improve enhancements based on search results
