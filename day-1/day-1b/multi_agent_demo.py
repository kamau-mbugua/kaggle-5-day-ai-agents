"""
Multi-Agent Systems & Workflow Patterns - Interactive Demo
Based on the Kaggle 5-Day Agents Course - Day 1b

This interactive demo lets you explore all four workflow patterns:
1. LLM-Based Coordinator (Dynamic orchestration)
2. Sequential Workflow (Guaranteed order)
3. Parallel Workflow (Concurrent execution)
4. Loop Workflow (Iterative refinement)
"""

import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool, google_search
from google.genai import types


def load_api_key():
    """Load the Google API key from environment variables."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "❌ GOOGLE_API_KEY not found in environment variables.\n"
            "Please create a .env file with your API key.\n"
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


# ============================================================================
# Pattern 1: LLM-Based Coordinator
# ============================================================================

def create_llm_coordinator(retry_config):
    """Create an LLM-coordinated research system."""

    research_agent = Agent(
        name="ResearchAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a specialized research agent. Use the google_search tool
        to find 2-3 pieces of relevant information on the given topic and present findings with citations.""",
        tools=[google_search],
        output_key="research_findings",
    )

    summarizer_agent = Agent(
        name="SummarizerAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Read the provided research findings: {research_findings}
        Create a concise summary as a bulleted list with 3-5 key points.""",
        output_key="final_summary",
    )

    root_agent = Agent(
        name="ResearchCoordinator",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a research coordinator. Your goal is to answer the user's query by orchestrating a workflow.
        1. First, you MUST call the `ResearchAgent` tool to find relevant information.
        2. Next, call the `SummarizerAgent` tool to create a concise summary.
        3. Finally, present the final summary to the user.""",
        tools=[AgentTool(research_agent), AgentTool(summarizer_agent)],
    )

    return root_agent


# ============================================================================
# Pattern 2: Sequential Workflow
# ============================================================================

def create_sequential_pipeline(retry_config):
    """Create a sequential blog post creation pipeline."""

    outline_agent = Agent(
        name="OutlineAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Create a blog outline for the given topic with:
        1. A catchy headline, 2. An introduction hook,
        3. 3-5 main sections with 2-3 bullet points for each, 4. A concluding thought""",
        output_key="blog_outline",
    )

    writer_agent = Agent(
        name="WriterAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Following this outline strictly: {blog_outline}
        Write a brief, 200 to 300-word blog post with an engaging and informative tone.""",
        output_key="blog_draft",
    )

    editor_agent = Agent(
        name="EditorAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Edit this draft: {blog_draft}
        Polish the text by fixing grammatical errors, improving flow, and enhancing clarity.""",
        output_key="final_blog",
    )

    return SequentialAgent(
        name="BlogPipeline",
        sub_agents=[outline_agent, writer_agent, editor_agent],
    )


# ============================================================================
# Pattern 3: Parallel Workflow
# ============================================================================

def create_parallel_research(retry_config):
    """Create a parallel multi-topic research system."""

    tech_researcher = Agent(
        name="TechResearcher",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Research the latest AI/ML trends. Include 3 key developments,
        main companies involved, and potential impact. Keep concise (100 words).""",
        tools=[google_search],
        output_key="tech_research",
    )

    health_researcher = Agent(
        name="HealthResearcher",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Research recent medical breakthroughs. Include 3 significant advances,
        practical applications, and estimated timelines. Keep concise (100 words).""",
        tools=[google_search],
        output_key="health_research",
    )

    finance_researcher = Agent(
        name="FinanceResearcher",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Research current fintech trends. Include 3 key trends,
        market implications, and future outlook. Keep concise (100 words).""",
        tools=[google_search],
        output_key="finance_research",
    )

    aggregator_agent = Agent(
        name="AggregatorAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Combine these research findings into a single executive summary:
        **Technology:** {tech_research}
        **Health:** {health_research}
        **Finance:** {finance_research}
        Highlight common themes, connections, and key takeaways (200 words).""",
        output_key="executive_summary",
    )

    parallel_team = ParallelAgent(
        name="ParallelResearchTeam",
        sub_agents=[tech_researcher, health_researcher, finance_researcher],
    )

    return SequentialAgent(
        name="ResearchSystem",
        sub_agents=[parallel_team, aggregator_agent],
    )


# ============================================================================
# Pattern 4: Loop Workflow
# ============================================================================

def exit_loop():
    """Function to signal loop termination."""
    return {"status": "approved", "message": "Story approved. Exiting refinement loop."}


def create_loop_refinement(retry_config):
    """Create a loop-based story refinement system."""

    initial_writer = Agent(
        name="InitialWriterAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Based on the user's prompt, write the first draft of a short story (100-150 words).
        Output only the story text, no introduction or explanation.""",
        output_key="current_story",
    )

    critic_agent = Agent(
        name="CriticAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a constructive story critic. Review: {current_story}
        Evaluate plot, characters, and pacing.
        - If well-written and complete, respond with EXACTLY: "APPROVED"
        - Otherwise, provide 2-3 specific, actionable suggestions for improvement.""",
        output_key="critique",
    )

    refiner_agent = Agent(
        name="RefinerAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a story refiner.
        Story: {current_story}
        Critique: {critique}
        - IF critique is EXACTLY "APPROVED", call the `exit_loop` function and nothing else.
        - OTHERWISE, rewrite the story to incorporate the feedback.""",
        output_key="current_story",
        tools=[FunctionTool(exit_loop)],
    )

    refinement_loop = LoopAgent(
        name="StoryRefinementLoop",
        sub_agents=[critic_agent, refiner_agent],
        max_iterations=2,
    )

    return SequentialAgent(
        name="StoryPipeline",
        sub_agents=[initial_writer, refinement_loop],
    )


# ============================================================================
# Main Interactive Menu
# ============================================================================

def print_menu():
    """Display the main menu."""
    print("\n" + "="*80)
    print("🤖 MULTI-AGENT SYSTEMS & WORKFLOW PATTERNS")
    print("="*80)
    print("\nChoose a workflow pattern to explore:\n")
    print("  0️⃣  LLM-Based Coordinator  - Dynamic orchestration (flexible but unpredictable)")
    print("  1️⃣  Sequential Workflow     - Guaranteed order (predictable pipeline)")
    print("  2️⃣  Parallel Workflow       - Concurrent execution (fast & independent)")
    print("  3️⃣  Loop Workflow           - Iterative refinement (quality improvement)")
    print("  4️⃣  Exit\n")
    print("="*80)


async def run_pattern(pattern_choice, retry_config):
    """Run the selected pattern."""

    if pattern_choice == "0":
        print("\n🤖 Running LLM-Based Coordinator...")
        agent = create_llm_coordinator(retry_config)
        prompt = "What are the latest advancements in quantum computing and what do they mean for AI?"

    elif pattern_choice == "1":
        print("\n🚥 Running Sequential Workflow...")
        agent = create_sequential_pipeline(retry_config)
        prompt = "Write a blog post about the benefits of multi-agent systems for software developers"

    elif pattern_choice == "2":
        print("\n🛣️  Running Parallel Workflow...")
        agent = create_parallel_research(retry_config)
        prompt = "Run the daily executive briefing on Tech, Health, and Finance"

    elif pattern_choice == "3":
        print("\n➰ Running Loop Workflow...")
        agent = create_loop_refinement(retry_config)
        prompt = "Write a short story about a lighthouse keeper who discovers a mysterious, glowing map"

    else:
        print("❌ Invalid choice!")
        return

    print(f"📝 Prompt: {prompt}\n")
    print("-"*80)

    runner = InMemoryRunner(agent=agent)
    response = await runner.run_debug(prompt)

    print("-"*80)
    print("\n✅ Workflow completed!\n")


async def main():
    """Main function for interactive demo."""
    print("\n🚀 Welcome to Multi-Agent Systems Demo!")

    # Setup
    try:
        load_api_key()
        print("✅ API key loaded successfully.")
    except Exception as e:
        print(f"\n{e}")
        return

    retry_config = create_retry_config()

    # Interactive loop
    while True:
        print_menu()

        choice = input("Enter your choice (0-4): ").strip()

        if choice == "4":
            print("\n👋 Goodbye!\n")
            break

        if choice in ["0", "1", "2", "3"]:
            try:
                await run_pattern(choice, retry_config)
                input("\n\nPress Enter to continue...")
            except KeyboardInterrupt:
                print("\n\n⏸️  Operation cancelled.\n")
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
        else:
            print("❌ Invalid choice! Please enter 0-4.\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
