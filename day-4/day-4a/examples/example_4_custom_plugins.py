"""
Example 4: Custom Plugins and Callbacks

Demonstrates:
- Build custom plugins with callbacks
- Track custom metrics (invocation counts, tool usage)
- Implement before/after hooks for agents, tools, and models
- Combine multiple plugins for comprehensive observability

Key Pattern:
class MyPlugin(BasePlugin):
    async def before_agent_callback(self, ...):
        # Custom logic before agent runs

    async def after_tool_callback(self, ...):
        # Custom logic after tool completes

Run:
python examples/example_4_custom_plugins.py
"""

import asyncio
import sys
import os
import logging
from typing import Dict

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.google_llm import Gemini
from google.adk.models.llm_request import LlmRequest
from google.adk.runners import InMemoryRunner
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.tools.google_search_tool import google_search

from utils import (
    load_api_key,
    create_retry_config,
    cleanup_logs,
)


# Custom Plugin 1: Count Invocations
class InvocationCounterPlugin(BasePlugin):
    """
    Custom plugin that counts agent, tool, and LLM invocations.

    Demonstrates:
    - before_agent_callback
    - before_tool_callback
    - before_model_callback
    """

    def __init__(self) -> None:
        super().__init__(name="invocation_counter")
        self.agent_count: int = 0
        self.tool_count: int = 0
        self.llm_request_count: int = 0

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        """Count agent invocations."""
        self.agent_count += 1
        logging.info(
            f"[InvocationCounter] 🤖 Agent '{agent.name}' starting (run #{self.agent_count})"
        )

    async def before_tool_callback(
        self, *, callback_context: CallbackContext
    ) -> None:
        """Count tool invocations."""
        self.tool_count += 1
        tool_name = callback_context.tool_name or "unknown"
        logging.info(
            f"[InvocationCounter] 🔧 Tool '{tool_name}' starting (call #{self.tool_count})"
        )

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> None:
        """Count LLM requests."""
        self.llm_request_count += 1
        logging.info(
            f"[InvocationCounter] 🧠 LLM request #{self.llm_request_count}"
        )

    def get_stats(self) -> Dict[str, int]:
        """Return collected statistics."""
        return {
            "agent_invocations": self.agent_count,
            "tool_calls": self.tool_count,
            "llm_requests": self.llm_request_count,
        }


# Custom Plugin 2: Performance Monitor
class PerformanceMonitorPlugin(BasePlugin):
    """
    Custom plugin that monitors agent performance.

    Demonstrates:
    - after_agent_callback
    - after_tool_callback
    - Measuring execution time
    """

    def __init__(self) -> None:
        super().__init__(name="performance_monitor")
        self.agent_times: list = []
        self.tool_times: list = []

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        """Record start time."""
        import time

        callback_context.custom_data["agent_start_time"] = time.time()

    async def after_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        """Calculate and log agent execution time."""
        import time

        start_time = callback_context.custom_data.get("agent_start_time")
        if start_time:
            duration = time.time() - start_time
            self.agent_times.append(duration)
            logging.info(
                f"[PerformanceMonitor] ⏱️  Agent '{agent.name}' completed in {duration:.2f}s"
            )

    async def before_tool_callback(
        self, *, callback_context: CallbackContext
    ) -> None:
        """Record tool start time."""
        import time

        callback_context.custom_data["tool_start_time"] = time.time()

    async def after_tool_callback(
        self, *, callback_context: CallbackContext
    ) -> None:
        """Calculate and log tool execution time."""
        import time

        start_time = callback_context.custom_data.get("tool_start_time")
        if start_time:
            duration = time.time() - start_time
            self.tool_times.append(duration)
            tool_name = callback_context.tool_name or "unknown"
            logging.info(
                f"[PerformanceMonitor] ⏱️  Tool '{tool_name}' completed in {duration:.2f}s"
            )

    def get_stats(self) -> Dict:
        """Return performance statistics."""
        return {
            "total_agent_calls": len(self.agent_times),
            "avg_agent_time": (
                sum(self.agent_times) / len(self.agent_times)
                if self.agent_times
                else 0
            ),
            "total_tool_calls": len(self.tool_times),
            "avg_tool_time": (
                sum(self.tool_times) / len(self.tool_times) if self.tool_times else 0
            ),
        }


# Custom Plugin 3: Tool Usage Tracker
class ToolUsageTrackerPlugin(BasePlugin):
    """
    Custom plugin that tracks which tools are used and how often.

    Demonstrates:
    - Collecting custom metrics
    - Tool-specific analytics
    """

    def __init__(self) -> None:
        super().__init__(name="tool_usage_tracker")
        self.tool_usage: Dict[str, int] = {}

    async def before_tool_callback(
        self, *, callback_context: CallbackContext
    ) -> None:
        """Track tool usage."""
        tool_name = callback_context.tool_name or "unknown"
        self.tool_usage[tool_name] = self.tool_usage.get(tool_name, 0) + 1
        logging.info(
            f"[ToolUsageTracker] 📊 Tool '{tool_name}' used {self.tool_usage[tool_name]} time(s)"
        )

    def get_stats(self) -> Dict[str, int]:
        """Return tool usage statistics."""
        return self.tool_usage.copy()


async def demo_custom_plugins():
    """
    Demonstrate custom plugins and callbacks.

    Shows:
    1. Build custom plugins from scratch
    2. Implement different callback types
    3. Collect custom metrics
    4. Combine multiple plugins
    """
    print("\n" + "=" * 80)
    print("Example 4: Custom Plugins and Callbacks")
    print("=" * 80)

    # Setup
    load_api_key()
    retry_config = create_retry_config()

    cleanup_logs("custom_plugins.log")
    logging.basicConfig(
        filename="custom_plugins.log",
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        force=True,
    )

    # Demo 1: Understanding plugins
    print("\n" + "-" * 80)
    print("DEMO 1: What are Plugins and Callbacks?")
    print("-" * 80)
    print()
    print("Plugin = Collection of callbacks")
    print("Callback = Function that runs at specific points")
    print()
    print("Available callbacks:")
    print("  • before_agent_callback  → Before agent starts")
    print("  • after_agent_callback   → After agent completes")
    print("  • before_tool_callback   → Before tool runs")
    print("  • after_tool_callback    → After tool completes")
    print("  • before_model_callback  → Before LLM call")
    print("  • after_model_callback   → After LLM responds")
    print("  • on_model_error_callback → When LLM errors occur")
    print()

    # Demo 2: Create custom plugins
    print("-" * 80)
    print("DEMO 2: Create Custom Plugins")
    print("-" * 80)
    print()
    print("Creating 3 custom plugins:")
    print("  1. InvocationCounterPlugin   → Counts invocations")
    print("  2. PerformanceMonitorPlugin  → Tracks execution time")
    print("  3. ToolUsageTrackerPlugin    → Monitors tool usage")
    print()

    # Initialize plugins
    counter_plugin = InvocationCounterPlugin()
    performance_plugin = PerformanceMonitorPlugin()
    tool_tracker_plugin = ToolUsageTrackerPlugin()

    print("✅ Plugins created")
    print()

    # Demo 3: Agent with multiple plugins
    print("-" * 80)
    print("DEMO 3: Agent with Multiple Plugins")
    print("-" * 80)
    print()

    search_agent = LlmAgent(
        name="search_assistant",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="Use google_search to find information. Be concise.",
        tools=[google_search],
    )

    # Create runner with ALL plugins
    runner = InMemoryRunner(
        agent=search_agent,
        plugins=[
            counter_plugin,
            performance_plugin,
            tool_tracker_plugin,
        ],  # Multiple plugins!
    )

    print("✅ Runner configured with 3 custom plugins")
    print()
    print("What happens now:")
    print("  • Every event triggers ALL relevant callbacks")
    print("  • Plugins run independently")
    print("  • Each plugin collects its own metrics")
    print()

    # Demo 4: Run agent and observe plugins
    print("-" * 80)
    print("DEMO 4: Watch Plugins in Action")
    print("-" * 80)
    print()

    queries = [
        "What is artificial intelligence?",
        "Find recent Python tutorials",
        "Search for machine learning papers",
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n🔹 Query {i}: {query}")
        response = await runner.run_debug(query)
        print(f"Response: {response[:100]}...")

    print()
    print("✅ All queries processed with plugin monitoring")
    print()

    # Demo 5: Display collected metrics
    print("-" * 80)
    print("DEMO 5: Collected Metrics")
    print("-" * 80)
    print()

    print("📊 InvocationCounterPlugin Stats:")
    counter_stats = counter_plugin.get_stats()
    for key, value in counter_stats.items():
        print(f"  • {key}: {value}")
    print()

    print("⏱️  PerformanceMonitorPlugin Stats:")
    perf_stats = performance_plugin.get_stats()
    for key, value in perf_stats.items():
        if "time" in key:
            print(f"  • {key}: {value:.3f}s")
        else:
            print(f"  • {key}: {value}")
    print()

    print("🔧 ToolUsageTrackerPlugin Stats:")
    tool_stats = tool_tracker_plugin.get_stats()
    for tool_name, count in tool_stats.items():
        print(f"  • {tool_name}: {count} calls")
    print()

    # Demo 6: Plugin use cases
    print("-" * 80)
    print("DEMO 6: Custom Plugin Use Cases")
    print("-" * 80)
    print()
    print("When to build custom plugins:")
    print()
    print("  ✅ Custom metrics tracking")
    print("     Example: Business KPIs, user engagement")
    print()
    print("  ✅ External system integration")
    print("     Example: Send logs to Datadog, New Relic")
    print()
    print("  ✅ Security and compliance")
    print("     Example: Audit trails, PII detection")
    print()
    print("  ✅ Performance monitoring")
    print("     Example: Latency tracking, bottleneck detection")
    print()
    print("  ✅ Custom alerting")
    print("     Example: Slack notifications on errors")
    print()

    # Demo 7: Plugin lifecycle
    print("-" * 80)
    print("DEMO 7: Plugin Lifecycle")
    print("-" * 80)
    print()
    print("Execution flow with plugins:")
    print()
    print("  User query")
    print("     ↓")
    print("  before_agent_callback ⚡  (all plugins)")
    print("     ↓")
    print("  Agent processing")
    print("     ↓")
    print("  before_model_callback ⚡  (all plugins)")
    print("     ↓")
    print("  LLM call")
    print("     ↓")
    print("  after_model_callback ⚡  (all plugins)")
    print("     ↓")
    print("  before_tool_callback ⚡  (all plugins)")
    print("     ↓")
    print("  Tool execution")
    print("     ↓")
    print("  after_tool_callback ⚡  (all plugins)")
    print("     ↓")
    print("  after_agent_callback ⚡  (all plugins)")
    print("     ↓")
    print("  Response")
    print()

    # Summary
    print("=" * 80)
    print("✅ Custom Plugins Complete!")
    print("=" * 80)
    print()
    print("Key Takeaways:")
    print()
    print("  ✅ Plugins = Collection of callbacks")
    print("  ✅ Callbacks = Hooks into agent lifecycle")
    print("  ✅ Multiple plugins work independently")
    print("  ✅ Build custom metrics and integrations")
    print()
    print("Plugin Decision Matrix:")
    print()
    print("┌────────────────────────────┬─────────────────────────────┐")
    print("│ Use LoggingPlugin When     │ Use Custom Plugin When      │")
    print("├────────────────────────────┼─────────────────────────────┤")
    print("│ Standard logs needed       │ Custom metrics needed       │")
    print("│ Quick setup                │ External integration        │")
    print("│ Development debugging      │ Business KPIs               │")
    print("│ General observability      │ Special formatting          │")
    print("└────────────────────────────┴─────────────────────────────┘")
    print()
    print("Day 4a Complete! 🎉")
    print("You've mastered agent observability!")
    print()


if __name__ == "__main__":
    asyncio.run(demo_custom_plugins())
