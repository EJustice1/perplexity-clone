"""
Prompts package for LLM services.

This package contains various system prompts for different use cases,
allowing easy customization and management of AI behavior.
"""

import os
from pathlib import Path

# Get the directory containing this file
PROMPTS_DIR = Path(__file__).parent

def load_prompt(filename: str) -> str:
    """
    Load a prompt from a text file.
    
    Args:
        filename: Name of the prompt file (e.g., 'search_synthesis.txt')
        
    Returns:
        The prompt content as a string
        
    Raises:
        FileNotFoundError: If the prompt file doesn't exist
    """
    prompt_path = PROMPTS_DIR / filename
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

# Load all available prompts
try:
    SEARCH_SYNTHESIS_PROMPT = load_prompt('search_synthesis.txt')
except FileNotFoundError:
    SEARCH_SYNTHESIS_PROMPT = "You are a helpful AI assistant."

try:
    TECHNICAL_EXPLANATION_PROMPT = load_prompt('technical_explanation.txt')
except FileNotFoundError:
    TECHNICAL_EXPLANATION_PROMPT = "You are a helpful AI assistant."

try:
    BUSINESS_APPLICATIONS_PROMPT = load_prompt('business_applications.txt')
except FileNotFoundError:
    BUSINESS_APPLICATIONS_PROMPT = "You are a helpful AI assistant."

try:
    CREATIVE_INNOVATION_PROMPT = load_prompt('creative_innovation.txt')
except FileNotFoundError:
    CREATIVE_INNOVATION_PROMPT = "You are a helpful AI assistant."

# List of all available prompts
AVAILABLE_PROMPTS = {
    'search_synthesis': SEARCH_SYNTHESIS_PROMPT,
    'technical_explanation': TECHNICAL_EXPLANATION_PROMPT,
    'business_applications': BUSINESS_APPLICATIONS_PROMPT,
    'creative_innovation': CREATIVE_INNOVATION_PROMPT,
}

def get_prompt(prompt_name: str) -> str:
    """
    Get a specific prompt by name.
    
    Args:
        prompt_name: Name of the prompt (e.g., 'search_synthesis')
        
    Returns:
        The prompt content as a string
        
    Raises:
        KeyError: If the prompt name doesn't exist
    """
    if prompt_name not in AVAILABLE_PROMPTS:
        raise KeyError(f"Prompt '{prompt_name}' not found. Available prompts: {list(AVAILABLE_PROMPTS.keys())}")
    
    return AVAILABLE_PROMPTS[prompt_name]

def list_prompts() -> list:
    """
    Get a list of all available prompt names.
    
    Returns:
        List of prompt names
    """
    return list(AVAILABLE_PROMPTS.keys())

def reload_prompts():
    """Reload all prompts from their text files."""
    global SEARCH_SYNTHESIS_PROMPT, TECHNICAL_EXPLANATION_PROMPT, BUSINESS_APPLICATIONS_PROMPT, CREATIVE_INNOVATION_PROMPT
    
    try:
        SEARCH_SYNTHESIS_PROMPT = load_prompt('search_synthesis.txt')
        TECHNICAL_EXPLANATION_PROMPT = load_prompt('technical_explanation.txt')
        BUSINESS_APPLICATIONS_PROMPT = load_prompt('business_applications.txt')
        CREATIVE_INNOVATION_PROMPT = load_prompt('creative_innovation.txt')
        
        # Update the available prompts dictionary
        AVAILABLE_PROMPTS.update({
            'search_synthesis': SEARCH_SYNTHESIS_PROMPT,
            'technical_explanation': TECHNICAL_EXPLANATION_PROMPT,
            'business_applications': BUSINESS_APPLICATIONS_PROMPT,
            'creative_innovation': CREATIVE_INNOVATION_PROMPT,
        })
    except FileNotFoundError as e:
        print(f"Warning: Could not reload some prompts: {e}")
