Certainly! Here’s a comprehensive **LangChain Refactor Plan Document** that closely matches the style, clarity, and organization of your original plan. This document introduces adaptive query decomposition (1–5 sub-searches per user query) and walks through each stage in a structured, actionable manner.

***

### **Implementation Plan: LangChain Refactor with Adaptive Decomposed Search**

**Objective:**  
To transform the core AI search pipeline with robust, modular LangChain components and dynamic query decomposition. Each stage incrementally upgrades capability—from adaptive multi-part query handling, to high-quality retrieval, extraction, and LLM-powered answer synthesis. The final system delivers a comprehensive answer and source display, with strictly managed secret keys.

***

### **Stage 1: LangChain Integration & Dependency Setup**

**Goal:**  
Prepare the codebase to leverage LangChain for search orchestration, LLM calls, and web content handling.

**Step-by-Step Details:**

1. **Install Required Packages:**  
   - Add to your requirements or use pip:
     ```
     pip install langchain langchain-community python-dotenv beautifulsoup4 requests
     pip install langchain-google-genai
     ```
2. **Prepare for Environment-Based Keys:**  
   - Set `SERP_API_KEY` and `GEMINI_API_KEY` in `.env` (already present).
   - Ensure deployment pipeline passes these securely in production.

**Desired Result:**  
Project dependencies are installed and ready for LangChain-driven search, LLM, and HTML extraction.

***

### **Stage 2: Adaptive Query Decomposition**

**Goal:**  
Intelligently split the user's query into 1–5 sub-queries, maximizing retrieval breadth for complex questions and efficiency for simple ones.

**Step-by-Step Details:**

1. **Decomposition Prompt Template:**  
   - Create a Gemini-driven prompt that asks the model to output a variable number of focused, distinct search queries based on the complexity of the user's question.
   - If the question is trivial, instruct the model to repeat the original as a single query.
2. **Implement Query Decomposition Logic:**  
   - Use LangChain with Gemini (`gemini-pro` model) to run the prompt and output the sub-query list.
   - Parse results as a sequence of line-separated queries, capped at 5.

**Desired Result:**  
Every incoming search request is dynamically broken into 1–5 targeted sub-searches, enabling maximum coverage.

***

### **Stage 3: Multi-Subquery Web Search**

**Goal:**  
Run live web searches for each decomposed sub-query and aggregate the results for downstream processing.

**Step-by-Step Details:**

1. **LangChain Search Wrapper:**  
   - Initialize SerpAPIWrapper with `SERP_API_KEY`.
   - For each sub-query, run a search and collect the top N URLs (e.g., 2).
2. **Deduplicate and Aggregate URLs:**  
   - Combine all URLs from each sub-search, deduplicate, and retain for extraction.

**Desired Result:**  
A diverse and authoritative set of web sources is collected for answer synthesis.

***

### **Stage 4: Content Extraction and Collation**

**Goal:**  
Extract, clean, and aggregate text from all selected URLs to build a high-fidelity knowledge context.

**Step-by-Step Details:**

1. **Content Loader Integration:**  
   - Use LangChain’s `WebBaseLoader` to fetch and extract main article text from each URL.
   - Strip boilerplate, ads, and navigation for clean aggregation.
2. **Aggregate Context:**  
   - Concatenate all extracted texts into a single block (or structured object) for LLM input.

**Desired Result:**  
Relevant content from all sources is collated and made ready for answer synthesis.

***

### **Stage 5: LLM-Driven Answer Synthesis**

**Goal:**  
Leverage Gemini via LangChain to generate a direct answer based strictly on extracted content—using an explicit RAG prompt.

**Step-by-Step Details:**

1. **Prompt Template for Contextual Answering:**  
   - Specify a prompt instructing Gemini to base its answer ONLY on the provided extracted context.
2. **LLMChain Integration:**  
   - Set up LangChain’s LLMChain for orchestrated LLM answer generation.
   - Pass the user’s original question and the combined context.
3. **Handle Output:**  
   - Receive the synthesized answer from Gemini.
   - Package the answer and associated source URLs for API response.

**Desired Result:**  
A synthesized answer is generated, fully grounded in retrieved, extracted text, reducing hallucination and improving trustworthiness.

***

### **Stage 6: Backend Endpoint and API Update**

**Goal:**  
Route all search queries and answers through the new LangChain-based system.

**Step-by-Step Details:**

1. **Endpoint Refactor:**  
   - Update `/api/v1/search` to accept a user’s query, run the full decomposed pipeline, and return the result.
2. **Structured API Response:**  
   - Ensure the response includes both the synthesized answer and all source URLs.

**Desired Result:**  
The frontend now displays answers and citations from the new LangChain-driven backend.

***

### **Stage 7: Testing, Validation, and Deployment**

**Goal:**  
Ensure reliability, efficiency, and security before production rollout.

**Step-by-Step Details:**

1. **Integration Tests:**  
   - Test for both simple and complex queries: validate decomposition, retrieval, extraction, synthesis, and output formatting.
2. **Edge/Failure Handling:**  
   - Ensure robustness when no sources are found, when LLM outputs fewer/more queries than expected, and for malformed URLs.
3. **Security & Logging:**  
   - Confirm environment keys are loaded only in trusted contexts.
   - Enable logging and tracing features as needed.
4. **Production Deployment:**  
   - Roll out with full monitoring.

**Desired Result:**  
The search pipeline is resilient, scalable, and production-ready.

***

### **Summary Chart**

| Stage                     | Key Components                | Output/Transition                                      |
|---------------------------|-------------------------------|--------------------------------------------------------|
| LangChain Integration     | Install, API keys             | Ready for modularity and secret management             |
| Adaptive Decomposition    | Gemini, PromptTemplate        | 1–5 sub-search queries per user input                  |
| Multi-Subquery Search     | SerpAPIWrapper                | Diverse deduplicated set of URLs                       |
| Content Extraction        | WebBaseLoader                 | Clean aggregated knowledge context                     |
| Answer Synthesis          | LLMChain, Gemini              | RAG-grounded answer                                    |
| API Endpoint              | Flask/FastAPI, JSON           | Synthesized answer and sources for frontend            |
| Testing/Deployment        | Test, validate, monitor       | Secure, reliable, maintainable release                 |

***

**Desired Result:**  
The entire application is refactored to use LangChain in all core AI logic, with automatic adjustment to query complexity, robust data retrieval, and trustworthy RAG-based answer synthesis. The user experience is modernized and modular, supporting rapid iterative improvements.