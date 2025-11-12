"""
Sequential Workflow Pattern - Blog Post Creation Pipeline
Based on the Kaggle 5-Day Agents Course - Day 1b

This demonstrates how to create a reliable "assembly line" where agents
run in a guaranteed, specific order. Perfect for tasks that build on each other.

Use Sequential when:
- Order matters
- You need a linear pipeline
- Each step builds on the previous one
"""

import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types


def load_api_key():
    """Load the Google API key from environment variables."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "❌ GOOGLE_API_KEY not found. Please create a .env file with your API key.\n"
            "Get your API key from: https://aistudio.google.com/app/apikey"
        )

    os.environ["GOOGLE_API_KEY"] = api_key
    return api_key


def create_retry_config():
    """Create retry configuration for handling transient errors."""
    return types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504]
    )


def create_blog_pipeline(retry_config):
    """
    Create a sequential pipeline for blog post creation.

    Pipeline: Outline → Writer → Editor
    """

    # 1. Outline Agent - Creates the blog post structure
    outline_agent = Agent(
        name="OutlineAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Create a blog outline for the given topic with:
        1. A catchy headline
        2. An introduction hook
        3. 3-5 main sections with 2-3 bullet points for each
        4. A concluding thought""",
        output_key="blog_outline",
    )

    # 2. Writer Agent - Writes the full blog post
    writer_agent = Agent(
        name="WriterAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Following this outline strictly: {blog_outline}
        Write a brief, 200 to 300-word blog post with an engaging and informative tone.""",
        output_key="blog_draft",
    )

    # 3. Editor Agent - Polishes the draft
    editor_agent = Agent(
        name="EditorAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Edit this draft: {blog_draft}
        Your task is to polish the text by fixing any grammatical errors,
        improving the flow and sentence structure, and enhancing overall clarity.""",
        output_key="final_blog",
    )

    # Create the Sequential Pipeline
    pipeline = SequentialAgent(
        name="BlogPipeline",
        sub_agents=[outline_agent, writer_agent, editor_agent],
    )

    return pipeline


async def main():
    """Main function to demonstrate sequential workflow."""
    print("\n" + "="*80)
    print("🚥 SEQUENTIAL WORKFLOW PATTERN - Blog Post Creation")
    print("="*80 + "\n")

    # Setup
    load_api_key()
    retry_config = create_retry_config()

    # Create the pipeline
    print("📋 Creating blog post pipeline...")
    pipeline = create_blog_pipeline(retry_config)
    print("✅ Pipeline created: Outline → Writer → Editor\n")

    # Create runner
    runner = InMemoryRunner(agent=pipeline)

    # Example topics to try
    topics = [
        "Write a blog post about the benefits of multi-agent systems for software developers",
        "Write a blog post about the future of AI in healthcare",
        "Write a blog post about best practices for remote team collaboration",
    ]

    # Run with the first topic
    topic = topics[0]
    print(f"📝 Topic: {topic}\n")
    print("-"*80)

    response = await runner.run_debug(topic)

    print("-"*80)
    print("\n✅ Sequential pipeline completed!")
    print("\nℹ️  Notice how each agent ran in order:")
    print("   1️⃣  OutlineAgent created the structure")
    print("   2️⃣  WriterAgent wrote the content")
    print("   3️⃣  EditorAgent polished the final version")

    print("\n" + "="*80)
    print("💡 Key Takeaway:")
    print("   Sequential workflows guarantee predictable, step-by-step execution.")
    print("   Perfect for tasks that must happen in a specific order!")
    print("="*80 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
