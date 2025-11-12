"""
Loop Workflow Pattern - Iterative Story Refinement
Based on the Kaggle 5-Day Agents Course - Day 1b

This demonstrates how to create iterative refinement cycles where agents
review and improve their own work repeatedly until quality standards are met.

Use Loop when:
- Iterative improvement is needed
- Quality refinement matters
- You need repeated cycles of review and revision
"""

import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import FunctionTool
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


def exit_loop():
    """
    Function to signal loop termination.
    Called by the RefinerAgent when the story is approved.
    """
    return {
        "status": "approved",
        "message": "Story approved. Exiting refinement loop."
    }


def create_story_refinement_system(retry_config):
    """
    Create a loop-based story refinement system.

    Structure: Initial Writer → [Critic → Refiner Loop] with max 2 iterations
    """

    # 1. Initial Writer - Creates the first draft
    initial_writer_agent = Agent(
        name="InitialWriterAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Based on the user's prompt, write the first draft of a short story (around 100-150 words).
        Output only the story text, with no introduction or explanation.""",
        output_key="current_story",
    )

    # 2. Critic - Reviews and provides feedback
    critic_agent = Agent(
        name="CriticAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""You are a constructive story critic. Review the story provided below.
        Story: {current_story}

        Evaluate the story's plot, characters, and pacing.
        - If the story is well-written and complete, you MUST respond with the exact phrase: "APPROVED"
        - Otherwise, provide 2-3 specific, actionable suggestions for improvement.""",
        output_key="critique",
    )

    # 3. Refiner - Improves the story or exits the loop
    refiner_agent = Agent(
        name="RefinerAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""You are a story refiner. You have a story draft and critique.

        Story Draft: {current_story}
        Critique: {critique}

        Your task is to analyze the critique.
        - IF the critique is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
        - OTHERWISE, rewrite the story draft to fully incorporate the feedback from the critique.""",
        output_key="current_story",
        tools=[FunctionTool(exit_loop)],
    )

    # Create the refinement loop (Critic → Refiner)
    story_refinement_loop = LoopAgent(
        name="StoryRefinementLoop",
        sub_agents=[critic_agent, refiner_agent],
        max_iterations=2,  # Prevents infinite loops
    )

    # Wrap in Sequential: Initial Write → Refinement Loop
    story_pipeline = SequentialAgent(
        name="StoryPipeline",
        sub_agents=[initial_writer_agent, story_refinement_loop],
    )

    return story_pipeline


async def main():
    """Main function to demonstrate loop workflow."""
    print("\n" + "="*80)
    print("➰ LOOP WORKFLOW PATTERN - Iterative Story Refinement")
    print("="*80 + "\n")

    # Setup
    load_api_key()
    retry_config = create_retry_config()

    # Create the system
    print("📋 Creating story refinement system...")
    story_system = create_story_refinement_system(retry_config)
    print("✅ System created: Initial Writer → [Critic ↔ Refiner Loop]\n")

    # Create runner
    runner = InMemoryRunner(agent=story_system)

    # Story prompts to try
    prompts = [
        "Write a short story about a lighthouse keeper who discovers a mysterious, glowing map",
        "Write a short story about an AI that learns to dream",
        "Write a short story about the last tree on Earth",
    ]

    # Run with the first prompt
    prompt = prompts[0]
    print(f"📖 Prompt: {prompt}\n")
    print("-"*80)

    response = await runner.run_debug(prompt)

    print("-"*80)
    print("\n✅ Loop workflow completed!")
    print("\nℹ️  Notice how the workflow executed:")
    print("   1️⃣  InitialWriterAgent created the first draft")
    print("   2️⃣  CriticAgent reviewed and provided feedback")
    print("   3️⃣  RefinerAgent improved the story based on feedback")
    print("   🔄 Loop repeated until approval or max iterations reached")

    print("\n" + "="*80)
    print("💡 Key Takeaway:")
    print("   Loop workflows enable iterative refinement for quality improvement.")
    print("   Perfect for tasks that benefit from review and revision cycles!")
    print("="*80 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
