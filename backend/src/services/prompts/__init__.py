"""
Prompts package for LLM services.

This package contains the intelligent prompt system:
1. Question analysis for determining response format and detail level
2. Intelligent synthesis for adaptive content generation
3. Adaptive refinement for format-appropriate presentation
"""

from pathlib import Path

# Get the directory containing this file
PROMPTS_DIR = Path(__file__).parent


def load_prompt(filename: str) -> str:
    """
    Load a prompt from a text file.

    Args:
        filename: Name of the prompt file (e.g., 'question_analysis.txt')

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
    QUESTION_ANALYSIS_PROMPT = load_prompt("question_analysis.txt")
except FileNotFoundError:
    QUESTION_ANALYSIS_PROMPT = (
        "You are an intelligent question analyzer."
    )

try:
    INTELLIGENT_SYNTHESIS_PROMPT = load_prompt("intelligent_synthesis.txt")
except FileNotFoundError:
    INTELLIGENT_SYNTHESIS_PROMPT = (
        "You are an intelligent information synthesizer."
    )

try:
    ADAPTIVE_REFINEMENT_PROMPT = load_prompt("adaptive_refinement.txt")
except FileNotFoundError:
    ADAPTIVE_REFINEMENT_PROMPT = (
        "You are an adaptive content refiner."
    )

try:
    QUERY_ENHANCEMENT_PROMPT = load_prompt("query_enhancement.txt")
except FileNotFoundError:
    QUERY_ENHANCEMENT_PROMPT = (
        "Improve this search query for better web search results."
    )

# List of all available prompts
AVAILABLE_PROMPTS = {
    "question_analysis": QUESTION_ANALYSIS_PROMPT,
    "intelligent_synthesis": INTELLIGENT_SYNTHESIS_PROMPT,
    "adaptive_refinement": ADAPTIVE_REFINEMENT_PROMPT,
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
    global QUESTION_ANALYSIS_PROMPT, INTELLIGENT_SYNTHESIS_PROMPT
    global ADAPTIVE_REFINEMENT_PROMPT, QUERY_ENHANCEMENT_PROMPT

    try:
        QUESTION_ANALYSIS_PROMPT = load_prompt("question_analysis.txt")
        INTELLIGENT_SYNTHESIS_PROMPT = load_prompt("intelligent_synthesis.txt")
        ADAPTIVE_REFINEMENT_PROMPT = load_prompt("adaptive_refinement.txt")
        QUERY_ENHANCEMENT_PROMPT = load_prompt("query_enhancement.txt")

        # Update the available prompts dictionary
        AVAILABLE_PROMPTS.update(
            {
                "question_analysis": QUESTION_ANALYSIS_PROMPT,
                "intelligent_synthesis": INTELLIGENT_SYNTHESIS_PROMPT,
                "adaptive_refinement": ADAPTIVE_REFINEMENT_PROMPT,
                "query_enhancement": QUERY_ENHANCEMENT_PROMPT,
            }
        )
    except FileNotFoundError as e:
        print(f"Warning: Could not reload some prompts: {e}")
