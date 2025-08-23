# Prompts System

This folder contains individual text files for different system prompts, making them easy to manage, customize, and version control.

## Structure

```
prompts/
├── __init__.py              # Package initialization and prompt management
├── search_synthesis.txt     # Main search synthesis prompt
├── technical_explanation.txt # Technical concept explanations
├── business_applications.txt # Business-focused analysis
├── creative_innovation.txt  # Creative and innovative thinking
└── README.md               # This file
```

## Available Prompts

### 1. `search_synthesis.txt`
**Purpose**: General search and question answering
**Best for**: Most user queries, general information requests
**Focus**: Direct answers, comprehensive coverage, consumer-friendly language

### 2. `technical_explanation.txt`
**Purpose**: Explaining complex technical concepts
**Best for**: Technical topics, educational content, concept explanations
**Focus**: Simplification, analogies, progressive complexity

### 3. `business_applications.txt`
**Purpose**: Business analysis and practical applications
**Best for**: Business questions, implementation guidance, ROI analysis
**Focus**: Practical value, actionable insights, business context

### 4. `creative_innovation.txt`
**Purpose**: Creative thinking and innovation
**Best for**: Strategic thinking, innovation exploration, future possibilities
**Focus**: Creative insights, pattern recognition, inspiration

## Usage

### Basic Usage
```python
from .prompts import get_prompt

# Get a specific prompt
system_message = get_prompt('search_synthesis')

# Use in LLM request
llm_request = LLMRequest(
    prompt=user_query,
    system_message=system_message
)
```

### List Available Prompts
```python
from .prompts import list_prompts

available_prompts = list_prompts()
# Returns: ['search_synthesis', 'technical_explanation', 'business_applications', 'creative_innovation']
```

### Reload Prompts (for development)
```python
from .prompts import reload_prompts

# Reload all prompts from their text files
reload_prompts()
```

## Customizing Prompts

### 1. Edit Existing Prompts
Simply edit the `.txt` files in this folder. Changes take effect immediately when you reload the prompts.

### 2. Add New Prompts
1. Create a new `.txt` file (e.g., `medical_advice.txt`)
2. Add your prompt content
3. Update `__init__.py` to include the new prompt
4. Use `get_prompt('medical_advice')` in your code

### 3. Prompt Best Practices
- **Be specific** about the AI's role and objectives
- **Include examples** of desired output format
- **Set clear boundaries** about information sources
- **Specify citation formats** explicitly
- **Test thoroughly** with various query types

## Example: Adding a New Prompt

### Step 1: Create the prompt file
```txt
# medical_advice.txt
You are a medical information specialist who provides accurate, helpful health information.

Your primary objectives:
1. Provide accurate medical information from reliable sources
2. Use clear, non-technical language
3. Always recommend consulting healthcare professionals for specific advice
4. Maintain 100% accuracy from provided sources

CRITICAL RULES:
- ONLY use information from the provided source texts
- ALWAYS cite sources using [1], [2], [3] format
- Include appropriate medical disclaimers
- Focus on education, not diagnosis
```

### Step 2: Update `__init__.py`
```python
# Add to the load_prompts section
try:
    MEDICAL_ADVICE_PROMPT = load_prompt('medical_advice.txt')
except FileNotFoundError:
    MEDICAL_ADVICE_PROMPT = "You are a helpful AI assistant."

# Add to AVAILABLE_PROMPTS
AVAILABLE_PROMPTS = {
    'search_synthesis': SEARCH_SYNTHESIS_PROMPT,
    'technical_explanation': TECHNICAL_EXPLANATION_PROMPT,
    'business_applications': BUSINESS_APPLICATIONS_PROMPT,
    'creative_innovation': CREATIVE_INNOVATION_PROMPT,
    'medical_advice': MEDICAL_ADVICE_PROMPT,  # New prompt
}
```

### Step 3: Use the new prompt
```python
from .prompts import get_prompt

medical_prompt = get_prompt('medical_advice')
```

## Benefits of This Approach

✅ **Easy Management**: Each prompt is a separate, editable text file  
✅ **Version Control**: Track changes to individual prompts in git  
✅ **Hot Reloading**: Update prompts without restarting the service  
✅ **Modular Design**: Mix and match prompts for different use cases  
✅ **Team Collaboration**: Multiple developers can work on different prompts  
✅ **Testing**: Test individual prompts in isolation  
✅ **Documentation**: Each prompt file can include detailed instructions  

## Current Implementation

The search synthesis service now uses the enhanced prompt system to generate:
- ✅ **Direct, helpful answers** that address user questions completely
- ✅ **Consumer-friendly language** that's easy to understand
- ✅ **Beautiful markdown formatting** with headers, bullet points, and clear organization
- ✅ **Comprehensive detail** without losing important information
- ✅ **Proper source citations** with `[1]`, `[2]`, `[3]` format
- ✅ **100% accurate responses** based only on provided sources

## Maintenance

- **Regular Reviews**: Periodically review and update prompts based on user feedback
- **A/B Testing**: Test different prompt versions to optimize performance
- **User Feedback**: Collect feedback on response quality and adjust prompts accordingly
- **Performance Monitoring**: Track how different prompts affect response quality and user satisfaction
