"""
LLM-Based Coordinator Pattern - Research & Summarization
Based on the Kaggle 5-Day Agents Course - Day 1b

This demonstrates how to use an LLM as a "manager" to dynamically orchestrate
a team of specialized agents. The coordinator decides when and how to use each agent.

Use LLM Coordinator when:
- Dynamic orchestration is needed
- Workflow order may vary based on context
- You need flexible, adaptive execution
"""

import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, google_search
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


def create_coordinated_system(retry_config):
    """
    Create an LLM-coordinated system with specialized sub-agents.

    Structure: Coordinator Agent manages: Research Agent + Summarizer Agent
    """

    # 1. Research Agent - Searches for information
    research_agent = Agent(
        name="ResearchAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""You are a specialized research agent. Your only job is to use the
        google_search tool to find 2-3 pieces of relevant information on the given topic
        and present the findings with citations.""",
        tools=[google_search],
        output_key="research_findings",
    )

    # 2. Summarizer Agent - Creates concise summaries
    summarizer_agent = Agent(
        name="SummarizerAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Read the provided research findings: {research_findings}
        Create a concise summary as a bulleted list with 3-5 key points.""",
        output_key="final_summary",
    )

    # 3. Root Coordinator - Orchestrates the workflow
    root_agent = Agent(
        name="ResearchCoordinator",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""You are a research coordinator. Your goal is to answer the user's query by orchestrating a workflow.

        1. First, you MUST call the `ResearchAgent` tool to find relevant information on the topic provided by the user.
        2. Next, after receiving the research findings, you MUST call the `SummarizerAgent` tool to create a concise summary.
        3. Finally, present the final summary clearly to the user as your response.""",
        tools=[
            AgentTool(research_agent),
            AgentTool(summarizer_agent),
        ],
    )

    return root_agent


async def main():
    """Main function to demonstrate LLM-coordinated workflow."""
    print("\n" + "="*80)
    print("🤖 LLM COORDINATOR PATTERN - Research & Summarization")
    print("="*80 + "\n")

    # Setup
    load_api_key()
    retry_config = create_retry_config()

    # Create the system
    print("📋 Creating LLM-coordinated system...")
    coordinator = create_coordinated_system(retry_config)
    print("✅ System created: Coordinator manages [Research Agent, Summarizer Agent]\n")

    # Create runner
    runner = InMemoryRunner(agent=coordinator)

    # Example queries
    queries = [
        "What are the latest advancements in quantum computing and what do they mean for AI?",
        "What is the current state of renewable energy adoption globally?",
        "How are autonomous vehicles progressing in 2025?",
    ]

    # Run with the first query
    query = queries[0]
    print(f"❓ Query: {query}\n")
    print("-"*80)

    response = await runner.run_debug(query)

    print("-"*80)
    print("\n✅ LLM-coordinated workflow completed!")
    print("\nℹ️  Notice how the workflow executed:")
    print("   1️⃣  Coordinator LLM decided to call ResearchAgent first")
    print("   2️⃣  Then it called SummarizerAgent with the research results")
    print("   3️⃣  Finally, it presented the final summary to the user")
    print("   🧠 The LLM dynamically orchestrated the entire workflow!")

    print("\n" + "="*80)
    print("💡 Key Takeaway:")
    print("   LLM coordinators provide flexible, dynamic orchestration.")
    print("   Great for workflows that need adaptive decision-making!")
    print("="*80 + "\n")

    print("\n⚠️  Note: LLM-based orchestration is flexible but can be unpredictable.")
    print("   For guaranteed execution order, use Sequential/Parallel/Loop agents.\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
