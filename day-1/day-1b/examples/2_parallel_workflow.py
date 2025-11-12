"""
Parallel Workflow Pattern - Multi-Topic Research
Based on the Kaggle 5-Day Agents Course - Day 1b

This demonstrates how to run independent tasks concurrently for dramatic speed improvements.
Tasks run simultaneously, then results are combined.

Use Parallel when:
- Tasks are independent
- Speed matters
- You can execute concurrently
"""

import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
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


def create_research_system(retry_config):
    """
    Create a parallel research system with multiple specialized researchers.

    Structure: [Tech, Health, Finance Researchers run in parallel] → Aggregator
    """

    # 1. Tech Researcher - Focuses on AI/ML trends
    tech_researcher = Agent(
        name="TechResearcher",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Research the latest AI/ML trends. Include 3 key developments,
        the main companies involved, and the potential impact. Keep the report very concise (100 words).""",
        tools=[google_search],
        output_key="tech_research",
    )

    # 2. Health Researcher - Focuses on medical breakthroughs
    health_researcher = Agent(
        name="HealthResearcher",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Research recent medical breakthroughs. Include 3 significant advances,
        their practical applications, and estimated timelines. Keep the report concise (100 words).""",
        tools=[google_search],
        output_key="health_research",
    )

    # 3. Finance Researcher - Focuses on fintech trends
    finance_researcher = Agent(
        name="FinanceResearcher",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Research current fintech trends. Include 3 key trends,
        their market implications, and the future outlook. Keep the report concise (100 words).""",
        tools=[google_search],
        output_key="finance_research",
    )

    # 4. Aggregator - Combines all research findings
    aggregator_agent = Agent(
        name="AggregatorAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Combine these three research findings into a single executive summary:

        **Technology Trends:**
        {tech_research}

        **Health Breakthroughs:**
        {health_research}

        **Finance Innovations:**
        {finance_research}

        Your summary should highlight common themes, surprising connections,
        and the most important key takeaways from all three reports.
        The final summary should be around 200 words.""",
        output_key="executive_summary",
    )

    # Create the parallel research team
    parallel_research_team = ParallelAgent(
        name="ParallelResearchTeam",
        sub_agents=[tech_researcher, health_researcher, finance_researcher],
    )

    # Wrap in Sequential to run parallel research first, then aggregator
    research_system = SequentialAgent(
        name="ResearchSystem",
        sub_agents=[parallel_research_team, aggregator_agent],
    )

    return research_system


async def main():
    """Main function to demonstrate parallel workflow."""
    print("\n" + "="*80)
    print("🛣️  PARALLEL WORKFLOW PATTERN - Multi-Topic Research")
    print("="*80 + "\n")

    # Setup
    load_api_key()
    retry_config = create_retry_config()

    # Create the system
    print("📋 Creating parallel research system...")
    research_system = create_research_system(retry_config)
    print("✅ System created: [Tech, Health, Finance] run in parallel → Aggregator\n")

    # Create runner
    runner = InMemoryRunner(agent=research_system)

    # Run the daily briefing
    print("📰 Running daily executive briefing...\n")
    print("-"*80)

    response = await runner.run_debug(
        "Run the daily executive briefing on Tech, Health, and Finance"
    )

    print("-"*80)
    print("\n✅ Parallel workflow completed!")
    print("\nℹ️  Notice how the workflow executed:")
    print("   1️⃣  Tech, Health, and Finance researchers ran SIMULTANEOUSLY")
    print("   2️⃣  Aggregator combined all results once parallel tasks completed")
    print("   ⚡ Result: 3x faster than running sequentially!")

    print("\n" + "="*80)
    print("💡 Key Takeaway:")
    print("   Parallel workflows run independent tasks concurrently for massive speed gains.")
    print("   Perfect for tasks that don't depend on each other!")
    print("="*80 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
