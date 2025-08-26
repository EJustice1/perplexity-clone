#!/usr/bin/env python3
"""
Demo script for the Intelligent LLM Synthesis System.

This script demonstrates how the new three-stage intelligent prompting system
works compared to the legacy two-stage system.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.llm_synthesis import LLMSynthesisService
from services.intelligent_llm_synthesis import IntelligentLLMSynthesisService
from api.v1.models import ExtractedContent


def create_mock_content():
    """Create mock extracted content for demonstration."""
    return [
        ExtractedContent(
            content="""
            Paris is the capital and most populous city of France. 
            It is located in the north-central part of the country, 
            on the Seine River. Paris has been the capital of France 
            since 987 CE and is known for its art, fashion, gastronomy, 
            and culture. The city is home to many famous landmarks 
            including the Eiffel Tower, Louvre Museum, and Notre-Dame Cathedral.
            """,
            url="https://example.com/paris-info",
            success=True,
            extraction_method="demo"
        ),
        ExtractedContent(
            content="""
            France is a country in Western Europe. It has a population 
            of about 67 million people and covers an area of 551,695 
            square kilometers. France is a unitary semi-presidential 
            republic with its capital in Paris. The country is known 
            for its rich history, culture, and influence in art, 
            science, and philosophy.
            """,
            url="https://example.com/france-info",
            success=True,
            extraction_method="demo"
        )
    ]


async def demo_legacy_system():
    """Demonstrate the legacy two-stage synthesis system."""
    print("🔄 Demo: Legacy Two-Stage Synthesis System")
    print("=" * 50)
    
    service = LLMSynthesisService()
    
    # Test with a simple factual question
    query = "What is the capital of France?"
    content = create_mock_content()
    
    print(f"Question: {query}")
    print("Using: Legacy Two-Stage System")
    print("- Stage 1: Initial Synthesis")
    print("- Stage 2: Formatting Refinement")
    print()
    
    try:
        response = await service.synthesize_answer(query, content)
        if response.success:
            print("✅ Response generated successfully!")
            print(f"Content length: {len(response.content)} characters")
            print("Preview:")
            print(response.content[:200] + "..." if len(response.content) > 200 else response.content)
        else:
            print(f"❌ Error: {response.error_message}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print("\n" + "=" * 50 + "\n")


async def demo_intelligent_system():
    """Demonstrate the intelligent three-stage synthesis system."""
    print("🧠 Demo: Intelligent Three-Stage Synthesis System")
    print("=" * 50)
    
    # Create service with intelligent system
    service = LLMSynthesisService()
    
    # Test with different types of questions
    questions = [
        ("What is the capital of France?", "FACTUAL"),
        ("How does France compare to other European countries?", "COMPARATIVE"),
        ("Tell me everything about Paris", "COMPREHENSIVE")
    ]
    
    content = create_mock_content()
    
    for query, expected_type in questions:
        print(f"Question: {query}")
        print(f"Expected Type: {expected_type}")
        print("Using: Intelligent Three-Stage System")
        print("- Stage 1: Question Analysis")
        print("- Stage 2: Intelligent Synthesis")
        print("- Stage 3: Adaptive Refinement")
        print()
        
        try:
            response = await service.synthesize_answer(query, content)
            if response.success:
                print("✅ Response generated successfully!")
                print(f"Content length: {len(response.content)} characters")
                print("Preview:")
                print(response.content[:200] + "..." if len(response.content) > 200 else response.content)
            else:
                print(f"❌ Error: {response.error_message}")
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print("-" * 30)
    
    print("=" * 50 + "\n")


def print_configuration_info():
    """Print information about system configuration."""
    print("⚙️  System Configuration")
    print("=" * 50)
    
    # Check environment variables
    google_api_key = bool(os.getenv("GOOGLE_AI_API_KEY"))
    
    print(f"GOOGLE_AI_API_KEY configured: {google_api_key}")
    print()
    
    if not google_api_key:
        print("⚠️  Warning: GOOGLE_AI_API_KEY not configured")
        print("   The demo will show the system structure but won't generate real responses")
        print("   Set GOOGLE_AI_API_KEY to test with real LLM calls")
        print()
    
    print("=" * 50 + "\n")


async def demo_question_analysis():
    """Demonstrate the integrated question analysis and search enhancement capabilities."""
    print("🔍 Demo: Integrated Question Analysis & Search Enhancement")
    print("=" * 50)
    
    # Create the intelligent service directly
    service = IntelligentLLMSynthesisService()
    
    # Test questions that should trigger different analysis results
    test_questions = [
        "What is the capital of France?",
        "How do vaccines work?",
        "Compare iPhone vs Android",
        "Tell me everything about climate change"
    ]
    
    content = create_mock_content()
    
    for query in test_questions:
        print(f"Analyzing: {query}")
        print("-" * 30)
        
        try:
            # This would normally require a real LLM provider
            # For demo purposes, we'll show the expected analysis
            if "capital" in query.lower():
                print("Expected Analysis:")
                print("- Question Type: FACTUAL")
                print("- Detail Level: LOW")
                print("- Recommended Format: CONCISE_TEXT")
                print("- Reasoning: Simple fact question requiring only a direct answer")
                print("- Search Enhancement: 'capital of France official facts government'")
                print("- Source Priorities: Government websites, official databases, encyclopedias")
            elif "how" in query.lower():
                print("Expected Analysis:")
                print("- Question Type: EXPLANATORY")
                print("- Detail Level: MEDIUM")
                print("- Recommended Format: DETAILED_EXPLANATION")
                print("- Reasoning: Process explanation needs clear steps and concepts")
                print("- Search Enhancement: 'how vaccines work explanation guide process'")
                print("- Source Priorities: Educational resources, scientific explanations, health guides")
            elif "compare" in query.lower():
                print("Expected Analysis:")
                print("- Question Type: COMPARATIVE")
                print("- Detail Level: HIGH")
                print("- Recommended Format: TABLES")
                print("- Reasoning: Direct comparison benefits from structured table format")
                print("- Search Enhancement: 'iPhone vs Android comparison features table'")
                print("- Source Priorities: Comparison articles, tech review sites, feature comparisons")
            elif "everything" in query.lower():
                print("Expected Analysis:")
                print("- Question Type: COMPREHENSIVE")
                print("- Detail Level: HIGH")
                print("- Recommended Format: DETAILED_EXPLANATION")
                print("- Reasoning: Broad question seeking comprehensive coverage")
                print("- Search Enhancement: 'climate change complete guide overview'")
                print("- Source Priorities: Comprehensive guides, overview articles, multiple sources")
            
            print()
            
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
    
    print("=" * 50 + "\n")


async def main():
    """Main demo function."""
    print("🚀 Intelligent LLM Synthesis System Demo")
    print("=" * 60)
    print()
    
    # Show configuration
    print_configuration_info()
    
    # Demo the different systems
    await demo_legacy_system()
    await demo_intelligent_system()
    await demo_question_analysis()
    
    print("🎯 Demo Complete!")
    print("\nThe intelligent system now provides:")
    print("- Question type analysis for optimal response format")
    print("- Search enhancement for better web results")
    print("- Source prioritization based on question type")
    print("- Adaptive formatting based on user needs")
    print("\nKey Benefits:")
    print("✅ Single analysis serves both search and response optimization")
    print("✅ Better search results through enhanced queries")
    print("✅ Appropriate response detail and format for each question type")
    print("✅ Eliminates redundancy between question analysis and search refinement")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
