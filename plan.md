Of course. Now that the foundational infrastructure and UI skeleton are complete, we can begin the exciting process of incrementally implementing the core AI search feature.

This plan is designed to be executed in small, manageable stages. Each stage builds upon the last, resulting in a testable and functional improvement at every step. This minimizes risk and allows for continuous validation of the process.

***

### **Implementation Plan: Incremental AI Search Feature**

**Objective:** To methodically replace the placeholder "!!!" functionality with a complete, multi-step AI-powered search pipeline. The process will be broken down into discrete stages, each adding a new layer of capability, culminating in a user experience similar to modern answer engines.

---

### **Stage 1: Backend Refactoring & API Preparation**

**Goal:** To clean up the placeholder logic and prepare the backend API to handle the more complex, multi-step search workflow. This stage ensures a clean foundation for the new feature.

**Step-by-Step Details:**

1.  **Remove Placeholder Logic:** On the backend, delete the "!!!" string manipulation logic from the primary endpoint.
2.  **Rename API Endpoint:** Rename the endpoint from `/api/v1/process-text` to a more descriptive name, such as `/api/v1/search`. This clarifies its new purpose.
3.  **Update Frontend API Call:** Modify the frontend code to call the new `/api/v1/search` endpoint.
4.  **Establish a "Passthrough" State:** For now, have the new endpoint simply accept the user's query and return it in the JSON response (e.g., `{"result": "You searched for: [user's query]"}`).
5.  **Deploy and Verify:** Commit these changes and allow the CI/CD pipeline to deploy them. Verify that the web application still works as expected, now showing the new passthrough response.

**Desired Result:** The placeholder functionality is cleanly removed, and the technical contracts between the frontend and backend are updated. The entire system is stable and ready for the first real step of the AI pipeline.

---

### **Stage 2: Live Web Search Integration**

**Goal:** To empower the backend to search the live web for information relevant to the user's query and display the raw results (links) on the frontend.

**Step-by-Step Details:**

1.  **Select & Procure API Key:** Choose a third-party web search provider (e.g., Google Custom Search API, Serper, Brave Search API) and obtain an API key.
2.  **Secure Secret Management:**
    *   **Local:** Add the API key to a local `.env` file (which is git-ignored) to be loaded as an environment variable in your `docker-compose.yml`.
    *   **Production:** Add the API key as a new secret in Google Secret Manager and grant the Cloud Run service account permission to access it. Update the Terraform configuration to inject this secret into the backend service.
3.  **Create a Backend Search Service:** In the backend codebase, create a new, dedicated module (e.g., `services/web_search.py`). This module will contain a function that takes a query string, calls the search provider's API, and returns a clean list of relevant URLs.
4.  **Integrate into the API Endpoint:** Update the `/api/v1/search` endpoint. It will now call the new web search service with the user's query.
5.  **Modify API Response:** Change the endpoint's response to return a list of the URLs found (e.g., `{"sources": ["http://url1.com", "http://url2.com", ...]}`).
6.  **Update Frontend for Display:** Modify the frontend's Result Display component to iterate through the `sources` array from the API response and render them as a clickable list of links.

**Desired Result:** The application can now perform live web searches. A user can enter a query, and the UI will display a list of relevant web links, proving the first step of the data retrieval pipeline is functional.

---

### **Stage 3: Content Extraction and Processing**

**Goal:** To add the capability to fetch and clean the textual content from the URLs discovered in the previous stage.

**Step-by-Step Details:**

1.  **Choose an HTML Parsing Library:** Add a robust Python library for fetching and parsing web content to your backend's requirements. `BeautifulSoup` combined with `requests` is a standard choice, or a more advanced library like `trafilatura` can excel at extracting main article text.
2.  **Create a Content Extraction Service:** Create a new backend module (e.g., `services/content_extractor.py`). This module will contain a function that takes a single URL, fetches its HTML content, and extracts the primary, clean text, stripping out ads, navigation, and other boilerplate.
3.  **Integrate into the Search Flow:** In the `/api/v1/search` endpoint, after retrieving the list of URLs, loop through the top 3-5 results and use the new content extraction service on each one.
4.  **Combine Content:** Aggregate the clean text from all sources into a single, large string or a structured object.
5.  **Update API for Verification:** Temporarily modify the API response to include a snippet of the extracted content (e.g., the first 500 characters) to verify the process is working. The frontend can display this raw text.

**Desired Result:** The backend can now not only find relevant sources but also read their content. The application is one step away from being able to synthesize an answer.

---

### **Stage 4: LLM Integration for Answer Synthesis**

**Goal:** To integrate a Large Language Model (LLM) to read the extracted content and synthesize a single, comprehensive answer to the user's original query. This is the core "AI" implementation.

**Step-by-Step Details:**

1.  **Select & Procure LLM API Key:** Choose an LLM provider (e.g., Google's Gemini API, OpenAI's API) and obtain an API key. Secure it using the same local `.env` and production Google Secret Manager method as in Stage 2.
2.  **Create an LLM Service:** Create a new backend module (e.g., `services/llm_synthesis.py`). This module will contain a function that orchestrates the call to the LLM.
3.  **Develop a Prompt Template:** This is a critical step. The function will take the original user query and the combined extracted content and format them into a specific prompt. The prompt should instruct the LLM clearly: *"Based ONLY on the provided text below, answer the user's question: [User's Question]. Do not use any outside knowledge."* This technique, known as Retrieval-Augmented Generation (RAG), significantly reduces hallucination.
4.  **Orchestrate the Full Pipeline:** Update the `/api/v1/search` endpoint to perform the complete sequence:
    1.  Get query from user.
    2.  Call Web Search Service to get URLs.
    3.  Call Content Extractor Service to get text from URLs.
    4.  Call LLM Synthesis Service to generate the final answer.
5.  **Finalize API Response:** Update the API response to its final form, containing the synthesized answer and the list of sources used: `{"answer": "This is the synthesized answer...", "sources": [...]}`.
6.  **Update Frontend Display:** Modify the Result Display component to prominently show the `answer` text. The list of source links should be displayed below the answer for reference.

**Desired Result:** The application's primary feature is now complete. A user can ask a question, and the system will perform research, read sources, and generate a unique, synthesized answer, displaying it in the UI.