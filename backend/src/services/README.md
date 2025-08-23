# Service Layer Documentation

## Prompts System

The `prompts.py` file contains system prompts used by the LLM synthesis service to guide AI responses.

### Current Prompts

#### `SEARCH_SYNTHESIS_PROMPT`
This is the main system prompt used for search synthesis. It focuses on:

- **Direct answers**: Answer the user's question directly and completely
- **100% accuracy**: Only use information from provided sources
- **Consumer-friendly language**: Clear, simple explanations without jargon
- **Beautiful markdown formatting**: Well-organized, easy-to-read responses
- **Comprehensive detail**: Include all relevant information without losing details
- **Proper citations**: Use `[1]`, `[2]`, `[3]` format for all information

### Customizing Prompts

To modify the prompts:

1. **Edit the prompt text** in `prompts.py`
2. **Update the import** in the service that uses it
3. **Test the changes** with a search query

### Adding New Prompts

To add new prompts for different use cases:

```python
# In prompts.py
SPECIALIZED_PROMPT = """Your specialized prompt here..."""

# In the service file
from .prompts import SPECIALIZED_PROMPT
```

### Prompt Best Practices

1. **Be specific** about what you want the AI to do
2. **Include examples** of the desired output format
3. **Set clear boundaries** about what information to use
4. **Specify citation formats** explicitly
5. **Test thoroughly** with various query types

### Example Usage

```python
from .prompts import SEARCH_SYNTHESIS_PROMPT

llm_request = LLMRequest(
    prompt=user_query,
    system_message=SEARCH_SYNTHESIS_PROMPT
)
```

### Current Implementation

The search synthesis service now uses the enhanced prompt to generate:
- ✅ **Direct, helpful answers** that address user questions completely
- ✅ **Consumer-friendly language** that's easy to understand
- ✅ **Beautiful markdown formatting** with headers, bullet points, and clear organization
- ✅ **Comprehensive detail** without losing important information
- ✅ **Proper source citations** with `[1]`, `[2]`, `[3]` format
- ✅ **100% accurate responses** based only on provided sources
