"""
Long-Running Operations - Human-in-the-Loop Approval
Based on the Kaggle 5-Day Agents Course - Day 2b

This demonstrates how to build agents that can pause execution and wait for
human approval before completing critical operations.

Key Concepts:
- Tools can pause execution using ToolContext.request_confirmation()
- Agent workflow detects pause via adk_request_confirmation event
- Resume with same invocation_id to continue where it paused
- State is maintained across pause/resume cycle

Use Cases:
- Financial transactions requiring approval
- Bulk operations (delete 1000 records)
- High-cost actions (spin up 50 servers)
- Irreversible operations (permanently delete account)
- Compliance checkpoints
"""

import os
import asyncio
import uuid
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.apps.app import App, ResumabilityConfig
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types

# Import workflow utilities
from utils import check_for_approval, print_agent_response, create_approval_response


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


# Configuration
LARGE_ORDER_THRESHOLD = 5


def place_shipping_order(
    num_containers: int, destination: str, tool_context: ToolContext
) -> dict:
    """
    Places a shipping order with approval for large orders.

    This demonstrates the three scenarios in a long-running operation:

    SCENARIO 1: Small orders (≤5 containers)
        - Auto-approve immediately
        - Return approved status
        - No pause needed

    SCENARIO 2: Large order - FIRST CALL (Pause)
        - Detect it's first call: tool_context.tool_confirmation is None
        - Call request_confirmation() to pause
        - Return pending status
        - ADK creates adk_request_confirmation event
        - Workflow detects this and waits for human decision

    SCENARIO 3: Large order - RESUMED CALL (Continue)
        - Detect it's resuming: tool_context.tool_confirmation is not None
        - Check human decision: .confirmed is True or False
        - Return approved or rejected status
        - Workflow displays final result

    Args:
        num_containers: Number of containers to ship
        destination: Shipping destination
        tool_context: ADK-provided context for pause/resume

    Returns:
        Dictionary with order status and details
    """

    # SCENARIO 1: Small orders auto-approve
    if num_containers <= LARGE_ORDER_THRESHOLD:
        return {
            "status": "approved",
            "order_id": f"ORD-{num_containers}-AUTO",
            "num_containers": num_containers,
            "destination": destination,
            "message": f"Order auto-approved: {num_containers} containers to {destination}",
        }

    # SCENARIO 2: Large order - FIRST CALL - Pause here
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"⚠️ Large order: {num_containers} containers to {destination}. Approve?",
            payload={"num_containers": num_containers, "destination": destination},
        )
        return {
            "status": "pending",
            "message": f"Order for {num_containers} containers requires approval",
        }

    # SCENARIO 3: Large order - RESUMED CALL - Continue here
    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "approved",
            "order_id": f"ORD-{num_containers}-HUMAN",
            "num_containers": num_containers,
            "destination": destination,
            "message": f"Order approved: {num_containers} containers to {destination}",
        }
    else:
        return {
            "status": "rejected",
            "message": f"Order rejected: {num_containers} containers to {destination}",
        }


def create_shipping_agent(retry_config):
    """
    Create a shipping coordinator agent with pausable tool.

    The agent uses the place_shipping_order tool which can pause
    for human approval on large orders.

    Args:
        retry_config: Retry configuration for the model

    Returns:
        LlmAgent: Agent with long-running tool
    """

    agent = LlmAgent(
        name="shipping_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a shipping coordinator assistant.

        When users request to ship containers:
        1. Use the place_shipping_order tool with number and destination
        2. If status is 'pending', inform user that approval is required
        3. After receiving final result, provide clear summary:
           - Order status (approved/rejected)
           - Order ID (if available)
           - Number of containers and destination
        4. Keep responses concise but informative
        """,
        tools=[FunctionTool(func=place_shipping_order)],
    )

    return agent


def create_resumable_app(agent):
    """
    Wrap agent in a resumable App.

    WHY THIS IS NEEDED:
    - Regular agents are stateless - no memory between calls
    - When tool pauses, agent forgets what it was doing
    - App with resumability saves state when paused
    - State includes: conversation history, tool parameters, pause location

    When resuming:
    - App loads saved state
    - Agent continues exactly where it paused
    - As if no time passed

    Args:
        agent: The shipping agent

    Returns:
        App: Resumable app wrapping the agent
    """

    app = App(
        name="shipping_coordinator",
        root_agent=agent,
        resumability_config=ResumabilityConfig(is_resumable=True),
    )

    return app


async def run_shipping_workflow(
    runner,
    session_service,
    query: str,
    auto_approve: bool = True
):
    """
    Run a shipping workflow with approval handling.

    This function orchestrates the entire pause/resume flow:

    STEP 1: Send initial request
        - Call run_async() with user query
        - Collect all events
        - Agent calls place_shipping_order tool

    STEP 2: Detect pause
        - Check events for adk_request_confirmation
        - If found: Tool paused, approval needed
        - Save invocation_id for resuming

    STEP 3: Handle approval
        - Get human decision (simulated here with auto_approve)
        - Format decision as FunctionResponse
        - Call run_async() AGAIN with same invocation_id
        - Agent resumes and completes

    Args:
        runner: Runner with resumable app
        session_service: Session service for state management
        query: User's shipping request
        auto_approve: Simulate human decision (True=approve, False=reject)
    """

    print(f"\n{'='*80}")
    print(f"💬 User > {query}\n")

    # Generate unique session ID
    session_id = f"order_{uuid.uuid4().hex[:8]}"

    # Create session for this workflow
    await session_service.create_session(
        app_name="shipping_coordinator",
        user_id="test_user",
        session_id=session_id
    )

    query_content = types.Content(role="user", parts=[types.Part(text=query)])
    events = []

    # STEP 1: Send initial request
    print("🚀 Starting workflow...\n")
    async for event in runner.run_async(
        user_id="test_user",
        session_id=session_id,
        new_message=query_content
    ):
        events.append(event)

    # STEP 2: Check if agent paused for approval
    approval_info = check_for_approval(events)

    # STEP 3: Handle approval workflow
    if approval_info:
        print(f"⏸️  Agent paused - large order requires approval")
        print(f"🤔 Simulating human decision: {'APPROVE ✅' if auto_approve else 'REJECT ❌'}\n")

        # Resume with approval decision
        print("▶️  Resuming workflow with decision...\n")
        async for event in runner.run_async(
            user_id="test_user",
            session_id=session_id,
            new_message=create_approval_response(approval_info, auto_approve),
            invocation_id=approval_info["invocation_id"],  # Critical: resume same execution
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"🤖 Agent > {part.text}")

    else:
        # No approval needed - small order completed immediately
        print("✅ No approval needed - order completed immediately\n")
        print_agent_response(events)

    print(f"{'='*80}\n")


async def demo_long_running_operations():
    """Demonstrate long-running operations with approval."""

    print("\n" + "="*80)
    print("⏳ LONG-RUNNING OPERATIONS - Human-in-the-Loop Approval")
    print("="*80 + "\n")

    # Setup
    load_api_key()
    retry_config = create_retry_config()

    # Create components
    print("🔧 Setting up components...")
    agent = create_shipping_agent(retry_config)
    app = create_resumable_app(agent)
    session_service = InMemorySessionService()
    runner = Runner(app=app, session_service=session_service)
    print("✅ Components ready!\n")

    print("📋 Configuration:")
    print(f"   • Large order threshold: >{LARGE_ORDER_THRESHOLD} containers")
    print(f"   • Small orders: Auto-approve")
    print(f"   • Large orders: Pause and request approval\n")

    # Demo 1: Small order (no approval needed)
    print("\n" + "="*80)
    print("DEMO 1: Small Order (Auto-Approve)")
    print("="*80)
    await run_shipping_workflow(
        runner,
        session_service,
        "Ship 3 containers to Singapore"
    )

    # Demo 2: Large order with approval
    print("\n" + "="*80)
    print("DEMO 2: Large Order (Approved)")
    print("="*80)
    await run_shipping_workflow(
        runner,
        session_service,
        "Ship 10 containers to Rotterdam",
        auto_approve=True
    )

    # Demo 3: Large order rejected
    print("\n" + "="*80)
    print("DEMO 3: Large Order (Rejected)")
    print("="*80)
    await run_shipping_workflow(
        runner,
        session_service,
        "Ship 8 containers to Los Angeles",
        auto_approve=False
    )

    print("\n" + "="*80)
    print("💡 Key Takeaways:")
    print("="*80)
    print("1. Tools can pause using ToolContext.request_confirmation()")
    print("2. Workflow detects pause via adk_request_confirmation event")
    print("3. Resume with same invocation_id to continue")
    print("4. State is preserved across pause/resume")
    print("5. Perfect for financial, bulk, or irreversible operations")
    print("="*80 + "\n")


async def main():
    """Main function."""
    try:
        await demo_long_running_operations()

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
