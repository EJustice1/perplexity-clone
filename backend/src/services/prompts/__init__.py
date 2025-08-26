"""
Prompts package for LLM services.

This package contains the two-stage prompt system:
1. Initial synthesis for pure information accuracy
2. Formatting refinement for professional presentation
"""

from pathlib import Path

# Get the directory containing this file
PROMPTS_DIR = Path(__file__).parent


def load_prompt(filename: str) -> str:
    """
    Load a prompt from a text file.

    Args:
        filename: Name of the prompt file (e.g., 'initial_synthesis.txt')

    Returns:
        The prompt content as a string

    Raises:
        FileNotFoundError: If the prompt file doesn't exist
    """
    prompt_path = PROMPTS_DIR / filename

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {prompt_path}"
        )

    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()


# Load all available prompts
try:
    INITIAL_SYNTHESIS_PROMPT = load_prompt("initial_synthesis.txt")
except FileNotFoundError:
    INITIAL_SYNTHESIS_PROMPT = (
        "You are an information synthesis specialist."
    )

try:
    FORMATTING_REFINEMENT_PROMPT = load_prompt(
        "formatting_refinement.txt"
    )
except FileNotFoundError:
    FORMATTING_REFINEMENT_PROMPT = (
        "You are a professional content formatter."
    )

try:
    QUERY_ENHANCEMENT_PROMPT = load_prompt("query_enhancement.txt")
except FileNotFoundError:
    QUERY_ENHANCEMENT_PROMPT = (
        "Improve this search query for better web search results."
    )

# List of all available prompts
AVAILABLE_PROMPTS = {
    "initial_synthesis": INITIAL_SYNTHESIS_PROMPT,
    "formatting_refinement": FORMATTING_REFINEMENT_PROMPT,
    "query_enhancement": QUERY_ENHANCEMENT_PROMPT,
}


def get_prompt(prompt_name: str) -> str:
    """
    Get a prompt by name.

    Args:
        prompt_name: Name of the prompt to retrieve

    Returns:
        Prompt content as string
    """
    return AVAILABLE_PROMPTS.get(prompt_name, "")


def list_prompts() -> list:
    """
    Get a list of all available prompt names.

    Returns:
        List of available prompt names
    """
    return list(AVAILABLE_PROMPTS.keys())


def reload_prompts() -> None:
    """Reload all prompts from their text files."""
    global INITIAL_SYNTHESIS_PROMPT, FORMATTING_REFINEMENT_PROMPT
    global QUERY_ENHANCEMENT_PROMPT

    try:
        INITIAL_SYNTHESIS_PROMPT = load_prompt(
            "initial_synthesis.txt"
        )
        FORMATTING_REFINEMENT_PROMPT = load_prompt(
            "formatting_refinement.txt"
        )
        QUERY_ENHANCEMENT_PROMPT = load_prompt(
            "query_enhancement.txt"
        )

        # Update the available prompts dictionary
        AVAILABLE_PROMPTS.update(
            {
                "initial_synthesis": INITIAL_SYNTHESIS_PROMPT,
                "formatting_refinement": FORMATTING_REFINEMENT_PROMPT,
                "query_enhancement": QUERY_ENHANCEMENT_PROMPT,
            }
        )
    except FileNotFoundError as e:
        print(f"Warning: Could not reload some prompts: {e}")
