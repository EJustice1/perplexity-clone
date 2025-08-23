# Stages 3-4: Design & Architecture Documentation

**Document ID:** STAGES-3-4-DESIGN-V1  
**Status:** DESIGN  
**Last Updated:** Current Date  

## Overview

This document outlines the design choices, architecture, and file structure for implementing Stages 3 (Content Extraction) and 4 (LLM Integration) in the search engine system. The design follows clean architecture principles, uses interfaces for external API integrations, and implements a factory pattern for service creation.

## Design Philosophy

### Core Principles
- **Separation of Concerns**: Clear boundaries between different layers of the system
- **Dependency Inversion**: Business logic depends on abstractions, not concrete implementations
- **Single Responsibility**: Each component has one clear purpose
- **Open for Extension**: Easy to add new providers without changing existing code
- **Testability**: Business logic can be tested independently of external dependencies

### Architectural Approach
- **Clean Architecture**: Layered design with clear dependencies
- **Interface-Based Design**: Abstract contracts for external service integrations
- **Factory Pattern**: Centralized creation of service implementations
- **Repository Pattern**: Data access abstraction for external APIs

## System Architecture

### High-Level Overview
The system is organized into four distinct layers, each with specific responsibilities and clear boundaries. Data flows from the top layer (API) down through the domain layer, then to the infrastructure layer, and finally to external services.

### Layer Responsibilities

#### 1. API Layer
- **Purpose**: Handle HTTP requests and responses
- **Responsibility**: Route requests to appropriate services, validate input, format output
- **Dependencies**: Depends only on the domain services layer
- **Isolation**: Completely isolated from external API implementations

#### 2. Domain Layer
- **Purpose**: Contain business logic and define contracts
- **Responsibility**: Orchestrate the search pipeline, define interfaces for external services
- **Dependencies**: No dependencies on external systems or infrastructure
- **Isolation**: Pure business logic that can run without external dependencies

#### 3. Infrastructure Layer
- **Purpose**: Implement external service integrations
- **Responsibility**: Provide concrete implementations of domain interfaces
- **Dependencies**: Depends on domain interfaces and external API clients
- **Isolation**: Each implementation is isolated from others

#### 4. External Services Layer
- **Purpose**: Provide raw access to external APIs
- **Responsibility**: Handle HTTP communication, authentication, and basic error handling
- **Dependencies**: Only on external service APIs
- **Isolation**: Minimal business logic, focused on communication

## File Structure & Organization

### Root Directory: `backend/src/`

The source code is organized into logical modules that reflect the architectural layers and business domains.

### API Layer: `api/v1/`

#### Purpose
The API layer serves as the entry point for all external requests. It handles HTTP-specific concerns and delegates business logic to the domain layer.

#### Files and Responsibilities

**`endpoints.py`**
- **Purpose**: Define HTTP endpoints and handle request routing
- **Responsibilities**: 
  - Accept HTTP requests
  - Validate request data
  - Call appropriate domain services
  - Handle HTTP-specific errors
  - Format responses
- **Design Choice**: Single file for all search-related endpoints to keep routing simple

**`models.py`**
- **Purpose**: Define data structures for API requests and responses
- **Responsibilities**:
  - Define input validation schemas
  - Define output serialization formats
  - Ensure data consistency between frontend and backend
- **Design Choice**: Pydantic models for automatic validation and serialization

### Core Module: `core/`

#### Purpose
The core module contains application-wide configuration, utilities, and shared components that are used across multiple layers.

#### Files and Responsibilities

**`config.py`**
- **Purpose**: Centralized configuration management
- **Responsibilities**:
  - Load environment variables
  - Provide typed configuration access
  - Define default values
  - Validate configuration on startup
- **Design Choice**: Pydantic settings for type-safe configuration with validation

**`exceptions.py`**
- **Purpose**: Define custom exception types for the application
- **Responsibilities**:
  - Provide meaningful error types
  - Enable proper error handling and logging
  - Support error categorization
- **Design Choice**: Hierarchical exception structure for better error handling

### Domain Layer: `domain/`

#### Purpose
The domain layer contains the core business logic, entities, and contracts. This is the heart of the application and should be completely independent of external concerns.

#### Entities Subdirectory: `domain/entities/`

**`search_query.py`**
- **Purpose**: Represent a user's search request
- **Responsibilities**:
  - Validate search parameters
  - Provide search constraints
  - Ensure data integrity
- **Design Choice**: Immutable data structure with validation

**`content_source.py`**
- **Purpose**: Represent a web source found during search
- **Responsibilities**:
  - Store source metadata
  - Provide access to source information
  - Support content extraction
- **Design Choice**: Rich object with metadata for better content processing

**`processed_content.py`**
- **Purpose**: Represent extracted and cleaned content from a source
- **Responsibilities**:
  - Store processed text content
  - Track extraction method used
  - Maintain source attribution
- **Design Choice**: Separate from raw content to support multiple extraction strategies

**`synthesized_answer.py`**
- **Purpose**: Represent the final AI-generated answer
- **Responsibilities**:
  - Store the synthesized response
  - Track sources used
  - Provide confidence metrics
- **Design Choice**: Rich response object for better user experience

#### Repositories Subdirectory: `domain/repositories/`

**`web_search_repository.py`**
- **Purpose**: Define contract for web search operations
- **Responsibilities**:
  - Abstract web search functionality
  - Define search result format
  - Support different search providers
- **Design Choice**: Interface-based design for provider flexibility

**`content_repository.py`**
- **Purpose**: Define contract for content extraction operations
- **Responsibilities**:
  - Abstract content extraction logic
  - Support multiple extraction strategies
  - Handle batch processing
- **Design Choice**: Batch processing interface for performance

**`llm_repository.py`**
- **Purpose**: Define contract for LLM operations
- **Responsibilities**:
  - Abstract LLM interactions
  - Support different LLM providers
  - Handle prompt engineering
- **Design Choice**: Provider-agnostic interface for model flexibility

#### Services Subdirectory: `domain/services/`

**`search_service.py`**
- **Purpose**: Orchestrate the complete search pipeline
- **Responsibilities**:
  - Coordinate between different repositories
  - Manage the search workflow
  - Handle errors and fallbacks
  - Provide unified search interface
- **Design Choice**: Single service class to maintain pipeline simplicity

### Infrastructure Layer: `infrastructure/`

#### Purpose
The infrastructure layer provides concrete implementations of domain interfaces and handles external service communication.

#### External Subdirectory: `infrastructure/external/`

**`serper_client.py`**
- **Purpose**: Low-level client for Serper web search API
- **Responsibilities**:
  - Handle HTTP communication with Serper
  - Manage authentication
  - Parse API responses
  - Handle basic error cases
- **Design Choice**: Minimal client focused only on API communication

**`http_client.py`**
- **Purpose**: Generic HTTP client for content fetching
- **Responsibilities**:
  - Fetch web content from URLs
  - Handle timeouts and retries
  - Manage connection pooling
  - Provide consistent error handling
- **Design Choice**: Generic client for reusability across different content sources

**`gemini_client.py`**
- **Purpose**: Low-level client for Google Gemini API
- **Responsibilities**:
  - Handle communication with Gemini
  - Manage API authentication
  - Handle response parsing
  - Provide error handling
- **Design Choice**: Minimal client to keep LLM logic in repository layer

#### Repositories Subdirectory: `infrastructure/repositories/`

**`serper_search_repository.py`**
- **Purpose**: Implement web search using Serper API
- **Responsibilities**:
  - Implement WebSearchRepository interface
  - Transform Serper responses to domain entities
  - Handle Serper-specific errors
  - Provide fallback behavior
- **Design Choice**: Single responsibility implementation focused on Serper integration

**`trafilatura_content_repository.py`**
- **Purpose**: Implement content extraction using Trafilatura
- **Responsibilities**:
  - Implement ContentRepository interface
  - Use Trafilatura for content extraction
  - Handle extraction failures gracefully
  - Support batch processing
- **Design Choice**: Trafilatura as primary strategy for its superior article extraction

**`gemini_llm_repository.py`**
- **Purpose**: Implement LLM operations using Google Gemini
- **Responsibilities**:
  - Implement LLMRepository interface
  - Handle prompt engineering
  - Manage context window limitations
  - Transform Gemini responses to domain entities
- **Design Choice**: Gemini as primary LLM for cost-effectiveness and quality

#### Factories Subdirectory: `infrastructure/factories/`

**`api_factory.py`**
- **Purpose**: Create and configure repository implementations
- **Responsibilities**:
  - Instantiate appropriate repository classes
  - Configure dependencies
  - Support provider selection
  - Enable easy testing through dependency injection
- **Design Choice**: Factory pattern for centralized object creation and configuration

### Application Entry: `main.py`

**Purpose**: Application startup and configuration
**Responsibilities**:
- Initialize FastAPI application
- Configure middleware
- Set up dependency injection
- Start the application server
**Design Choice**: Single entry point for clean application startup

## Design Choices Explained

### Why Interfaces?
- **Testability**: Business logic can be tested with mock implementations
- **Flexibility**: Easy to swap providers without changing business logic
- **Maintainability**: Clear contracts make the system easier to understand
- **Extensibility**: New providers can be added by implementing existing interfaces

### Why Factory Pattern?
- **Centralization**: All object creation logic in one place
- **Configuration**: Easy to change implementations through configuration
- **Testing**: Simple to inject mock implementations for testing
- **Dependency Management**: Clear dependency graph and initialization order

### Why Clean Architecture?
- **Independence**: Business logic doesn't depend on external systems
- **Testability**: Each layer can be tested independently
- **Maintainability**: Clear boundaries make the system easier to modify
- **Scalability**: Easy to add new features without affecting existing code

### Why Single Provider Per Service?
- **Simplicity**: Easier to implement and debug initially
- **Focus**: Can optimize for the chosen provider
- **Learning**: Team can learn the architecture before adding complexity
- **Foundation**: Provides a solid base for adding more providers later

## Data Flow

### Search Request Flow
1. **HTTP Request**: User sends search request to `/api/v1/search`
2. **API Layer**: Endpoint validates request and calls SearchService
3. **Domain Layer**: SearchService orchestrates the search pipeline
4. **Infrastructure Layer**: Repository implementations call external APIs
5. **External APIs**: Serper, HTTP clients, and Gemini execute operations
6. **Response Flow**: Data flows back up through the layers to the user

### Pipeline Execution
1. **Web Search**: SearchService calls WebSearchRepository to find relevant sources
2. **Content Extraction**: SearchService calls ContentRepository to extract content from sources
3. **LLM Synthesis**: SearchService calls LLMRepository to generate the final answer
4. **Result Assembly**: SearchService combines all results into a unified response

## Error Handling Strategy

### Error Categories
- **Validation Errors**: Invalid input data (handled at API layer)
- **Business Logic Errors**: Domain-specific errors (handled at service layer)
- **External API Errors**: Network or API failures (handled at repository layer)
- **System Errors**: Unexpected failures (handled at all layers)

### Error Handling Approach
- **Graceful Degradation**: System continues to function with reduced capability
- **Meaningful Messages**: Users receive helpful error information
- **Logging**: All errors are logged with context for debugging
- **Fallbacks**: Alternative strategies when primary methods fail

## Configuration Strategy

### Environment Variables
- **API Keys**: External service authentication
- **Service Selection**: Which providers to use
- **Performance Tuning**: Timeouts, limits, and thresholds
- **Feature Flags**: Enable/disable specific functionality

### Configuration Management
- **Type Safety**: All configuration values are typed and validated
- **Defaults**: Sensible defaults for all configuration options
- **Validation**: Configuration is validated on application startup
- **Documentation**: All configuration options are clearly documented

## Testing Strategy

### Testing Layers
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows
- **Performance Tests**: Test system performance under load

### Mocking Strategy
- **Repository Interfaces**: Mock all external service interactions
- **HTTP Clients**: Mock network communication
- **Configuration**: Use test configuration for consistent test environment
- **Dependencies**: Inject mock dependencies through factory pattern

## Future Extensibility

### Adding New Providers
- **Implement Interface**: Create new class implementing existing interface
- **Register in Factory**: Add new implementation to factory
- **Update Configuration**: Add configuration options for new provider
- **No Other Changes**: Business logic remains unchanged

### Adding New Services
- **Define Interface**: Create new repository interface
- **Implement Service**: Create concrete implementation
- **Update Factory**: Add creation method to factory
- **Integrate**: Wire into existing service layer

### Performance Optimizations
- **Caching**: Add caching layer for frequently accessed data
- **Async Processing**: Implement concurrent processing where possible
- **Connection Pooling**: Optimize external API connections
- **Load Balancing**: Distribute load across multiple providers

## Conclusion

This design provides a solid foundation for implementing Stages 3 and 4 while maintaining clean architecture principles. The interface-based approach ensures the system is testable, maintainable, and extensible. The factory pattern simplifies object creation and configuration, while the layered architecture keeps concerns properly separated.

The single provider per service approach keeps the initial implementation simple while providing a clear path for adding more providers in the future. The clean separation between layers makes the system easy to understand, test, and modify as requirements evolve.
