# Agent Observability 🔍

**Based on Kaggle's 5-Day AI Agents Intensive Course - Day 4a**

Master agent observability through logging, tracing, debugging, and production monitoring. Learn to identify failures, track performance, and build reliable AI systems.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [Pattern 1: Basic Logging Setup](#pattern-1-basic-logging-setup)
- [Pattern 2: Debugging Broken Agents](#pattern-2-debugging-broken-agents)
- [Pattern 3: Production Logging](#pattern-3-production-logging)
- [Pattern 4: Custom Plugins](#pattern-4-custom-plugins)
- [Architecture](#architecture)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

## Overview

### The Observability Challenge

Traditional software fails predictably:
```python
divide_by_zero()  # Clear error: ZeroDivisionError
```

AI agents fail mysteriously:
```python
User: "Find quantum computing papers"
Agent: "I cannot help with that request."
You: 😭 WHY?? Is it the prompt? Missing tools? API error?
```

### The Solution

**Agent observability** provides X-ray vision into your agent's decision-making process:

- ✅ See exact prompts sent to the LLM
- ✅ Watch which tools are available
- ✅ Track how models respond
- ✅ Identify where failures occur

### Three Pillars of Observability

| Pillar | What It Is | Example |
|--------|------------|---------|
| **Logs** | Record of single events | "Agent started at 10:15:30" |
| **Traces** | Connected story of events | "User query → LLM call → Tool use → Response" |
| **Metrics** | Summary statistics | "Average response time: 2.3s" |

### What You'll Learn

✅ Configure logging with different levels (DEBUG, INFO, WARNING, ERROR)
✅ Debug broken agents with systematic workflows
✅ Implement production observability with LoggingPlugin
✅ Build custom plugins for specialized monitoring

## Quick Start

### Prerequisites

```bash
# Python 3.10+
python --version

# Google ADK
pip install google-adk
```

### Installation

```bash
# 1. Navigate to directory
cd day-4/day-4a

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 4. Run interactive demo
python observability_demo.py
```

### Getting Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy to `.env`:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

## Core Concepts

### Logging Levels

Python's logging module provides hierarchical levels:

```
DEBUG    → Everything (verbose, for development)
INFO     → Key events (standard production)
WARNING  → Potential issues (monitor closely)
ERROR    → Failures (requires attention)
```

**Level Hierarchy:**
```
DEBUG includes: DEBUG + INFO + WARNING + ERROR
INFO includes:  INFO + WARNING + ERROR
WARNING includes: WARNING + ERROR
ERROR includes: ERROR only
```

### The Debugging Pattern

```
1. Symptom    → What went wrong?
2. Logs       → Check DEBUG logs
3. Root Cause → Trace execution flow
4. Fix        → Apply correction
5. Verify     → Test with same input
```

### Plugin Architecture

```
Plugin = Collection of Callbacks

Callbacks = Hooks into agent lifecycle:
  • before_agent_callback
  • after_agent_callback
  • before_tool_callback
  • after_tool_callback
  • before_model_callback
  • after_model_callback
  • on_model_error_callback
```

## Pattern 1: Basic Logging Setup

### Understanding Log Levels

**DEBUG Level** (Most Verbose)
```python
import logging

logging.basicConfig(level=logging.DEBUG)

# Captures:
# - Full LLM requests (system instructions, tools)
# - Complete LLM responses
# - Tool call arguments and results
# - Internal state transitions
```

**Use Case:** Development, debugging, troubleshooting

**INFO Level** (Standard)
```python
logging.basicConfig(level=logging.INFO)

# Captures:
# - Agent starts and completions
# - Tool invocations
# - Major events and milestones
# - High-level execution flow
```

**Use Case:** Production monitoring, general observability

**WARNING Level**
```python
logging.basicConfig(level=logging.WARNING)

# Captures:
# - Potential issues (slow responses, retries)
# - Deprecated features
# - Non-critical errors
```

**Use Case:** Monitoring for potential problems

**ERROR Level** (Least Verbose)
```python
logging.basicConfig(level=logging.ERROR)

# Captures:
# - Exception messages
# - Stack traces
# - Critical failures
```

**Use Case:** Alerting, incident response

See `examples/example_1_basic_logging.py` for complete example.

### Configuration Best Practices

**Development:**
```python
import logging

logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
```

**Production:**
```python
logging.basicConfig(
    filename="production.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
```

**Custom Format:**
```python
logging.basicConfig(
    filename="custom.log",
    level=logging.INFO,
    format="[%(levelname)s] %(filename)s:%(lineno)s - %(message)s",
)
```

## Pattern 2: Debugging Broken Agents

### The Systematic Debugging Workflow

**Step 1: Observe the Symptom**
```
User: "Find quantum computing papers"
Agent: Returns suspiciously high count (e.g., 5000 papers)

Symptom: Unexpected behavior
```

**Step 2: Enable DEBUG Logging**
```python
import logging

logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,  # Capture everything!
)
```

**Step 3: Examine Logs**
```python
# Look for key patterns:
# - "LLM Request" → What was sent to the model?
# - "LLM Response" → What did the model return?
# - "Tool Call" → What arguments were passed?
# - "Tool Result" → What was returned?
```

**Step 4: Identify Root Cause**
```python
# Common issues:
# ❌ Missing tools in tools list
# ❌ Type mismatches in function arguments
# ❌ Ambiguous instructions
# ❌ Poor tool descriptions
```

**Step 5: Fix and Verify**
```python
# Apply fix → Test → Check logs again
```

See `examples/example_2_debugging_broken_agent.py` for complete workflow.

### Example: Type Mismatch Bug

**Broken Code:**
```python
def count_papers(papers: str):  # Should be List[str]!
    return len(papers)  # Counts characters, not list items!

# Result: len("paper1,paper2,paper3") = 21 (wrong!)
```

**DEBUG Logs Show:**
```
DEBUG - LLM Response: function_call: count_papers
DEBUG - Arguments: {'papers': ['paper1', 'paper2', 'paper3']}
DEBUG - Tool Result: 21  # ❌ Wrong! Should be 3
```

**Root Cause:** Type annotation says `str`, but agent passes `List[str]`

**Fixed Code:**
```python
def count_papers(papers: List[str]):  # Correct type!
    return len(papers)  # Counts list items

# Result: len(['paper1', 'paper2', 'paper3']) = 3 (correct!)
```

### Common Failure Patterns

| Symptom | Root Cause | How to Find in Logs |
|---------|-----------|---------------------|
| "Cannot help" | Missing tool | LLM Request shows `tools: []` |
| Wrong results | Type mismatch | Tool arguments don't match signature |
| Agent loops | Ambiguous instructions | Multiple LLM calls with same context |
| Tool not called | Poor description | LLM doesn't recognize when to use tool |
| Timeout | Infinite recursion | Repeated agent calls without progress |

## Pattern 3: Production Logging

### ADK's Built-in LoggingPlugin

**What It Captures Automatically:**
- 🚀 User messages and agent responses
- ⏱️ Timing data for performance analysis
- 🧠 LLM requests and responses
- 🔧 Tool calls and results
- ✅ Complete execution traces

**Zero Configuration Required!**

### Implementation

```python
from google.adk.runners import InMemoryRunner
from google.adk.plugins.logging_plugin import LoggingPlugin

# Create runner with LoggingPlugin
runner = InMemoryRunner(
    agent=agent,
    plugins=[LoggingPlugin()],  # That's it!
)

# Everything is logged automatically
response = await runner.run_debug("Your query here")
```

See `examples/example_3_production_logging.py` for complete example.

### LoggingPlugin Output Format

```
[logging_plugin] 🚀 USER MESSAGE RECEIVED
   Invocation ID: e-abc123...
   Session ID: session_xyz
   User ID: user_001
   Root Agent: my_agent
   User Content: "Find papers on AI"

[logging_plugin] 🧠 LLM REQUEST
   Model: gemini-2.5-flash-lite
   System Instruction: "You are a research assistant..."
   Available Tools: ['google_search', 'count_papers']

[logging_plugin] 🧠 LLM RESPONSE
   Content: function_call: google_search
   Token Usage - Input: 242, Output: 21

[logging_plugin] 🔧 TOOL STARTING
   Tool Name: google_search
   Arguments: {'query': 'AI papers'}

[logging_plugin] 🔧 TOOL COMPLETED
   Tool Name: google_search
   Result: [list of papers...]

[logging_plugin] ✅ INVOCATION COMPLETED
   Final Agent: my_agent
   Total Time: 2.3s
```

### When to Use LoggingPlugin

**✅ Use LoggingPlugin When:**
- Standard observability needs
- Quick production setup
- Debugging issues
- Audit trails
- Performance monitoring

**❌ Use Custom Plugin When:**
- Custom metrics tracking (business KPIs)
- External system integration (Datadog, New Relic)
- Special formatting requirements
- Selective event logging
- Security/compliance needs

## Pattern 4: Custom Plugins

### Building Custom Plugins

**Plugin Structure:**
```python
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.base_agent import BaseAgent

class MyPlugin(BasePlugin):
    def __init__(self):
        super().__init__(name="my_plugin")
        self.data = {}  # Store custom metrics

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ):
        # Custom logic before agent runs
        pass

    async def after_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ):
        # Custom logic after agent completes
        pass
```

### Example: Invocation Counter Plugin

```python
class InvocationCounterPlugin(BasePlugin):
    def __init__(self):
        super().__init__(name="invocation_counter")
        self.agent_count = 0
        self.tool_count = 0
        self.llm_count = 0

    async def before_agent_callback(self, *, agent, callback_context):
        self.agent_count += 1
        logging.info(f"Agent run #{self.agent_count}")

    async def before_tool_callback(self, *, callback_context):
        self.tool_count += 1
        logging.info(f"Tool call #{self.tool_count}")

    async def before_model_callback(self, *, callback_context, llm_request):
        self.llm_count += 1
        logging.info(f"LLM request #{self.llm_count}")

    def get_stats(self):
        return {
            "agents": self.agent_count,
            "tools": self.tool_count,
            "llm_calls": self.llm_count,
        }
```

### Example: Performance Monitor Plugin

```python
import time

class PerformanceMonitorPlugin(BasePlugin):
    def __init__(self):
        super().__init__(name="performance_monitor")
        self.agent_times = []

    async def before_agent_callback(self, *, agent, callback_context):
        callback_context.custom_data["start_time"] = time.time()

    async def after_agent_callback(self, *, agent, callback_context):
        start = callback_context.custom_data.get("start_time")
        if start:
            duration = time.time() - start
            self.agent_times.append(duration)
            logging.info(f"Agent completed in {duration:.2f}s")

    def get_stats(self):
        return {
            "total_calls": len(self.agent_times),
            "avg_time": sum(self.agent_times) / len(self.agent_times),
            "max_time": max(self.agent_times),
            "min_time": min(self.agent_times),
        }
```

See `examples/example_4_custom_plugins.py` for complete implementations.

### Plugin Lifecycle

```
User Query
    ↓
before_agent_callback ⚡  (all plugins)
    ↓
Agent Processing
    ↓
before_model_callback ⚡  (all plugins)
    ↓
LLM Call
    ↓
after_model_callback ⚡  (all plugins)
    ↓
before_tool_callback ⚡  (all plugins)
    ↓
Tool Execution
    ↓
after_tool_callback ⚡  (all plugins)
    ↓
after_agent_callback ⚡  (all plugins)
    ↓
Response
```

### Using Multiple Plugins

```python
from google.adk.runners import InMemoryRunner

# Create multiple plugins
counter = InvocationCounterPlugin()
performance = PerformanceMonitorPlugin()
tool_tracker = ToolUsageTrackerPlugin()

# Add all to runner
runner = InMemoryRunner(
    agent=agent,
    plugins=[
        counter,
        performance,
        tool_tracker,
    ],  # All plugins work independently!
)

# Run agent
response = await runner.run_debug("Your query")

# Get metrics from each plugin
print(counter.get_stats())
print(performance.get_stats())
print(tool_tracker.get_stats())
```

## Architecture

### Observability Stack

```
┌─────────────────────────────────────────────────────┐
│                   Application                        │
│                                                       │
│  ┌────────────────────────────────────────────────┐ │
│  │              Runner                             │ │
│  │  (Orchestrates agent + plugins)                 │ │
│  └───────┬────────────────────────┬────────────────┘ │
│          │                        │                   │
│          ▼                        ▼                   │
│  ┌───────────────┐      ┌─────────────────────┐    │
│  │     Agent     │      │      Plugins        │    │
│  │  (LlmAgent)   │      │  - LoggingPlugin    │    │
│  │               │      │  - Custom Plugins   │    │
│  └───────┬───────┘      └──────────┬──────────┘    │
│          │                         │                 │
│          ▼                         ▼                 │
│    Tools & LLM              Callbacks               │
│                             (Hooks)                  │
└─────────────────────────────────────────────────────┘
          │                         │
          ▼                         ▼
    Execution Flow            Log Files
                              Metrics
                              Traces
```

### Callback Types

| Callback | When It Runs | Use Case |
|----------|--------------|----------|
| `before_agent_callback` | Before agent starts | Count invocations, log start time |
| `after_agent_callback` | After agent completes | Calculate duration, collect metrics |
| `before_tool_callback` | Before tool executes | Log tool arguments, validate inputs |
| `after_tool_callback` | After tool completes | Log results, track tool usage |
| `before_model_callback` | Before LLM call | Log prompts, count tokens |
| `after_model_callback` | After LLM responds | Log responses, track latency |
| `on_model_error_callback` | When LLM errors | Handle retries, alert on failures |

## Best Practices

### Development

**✅ DO:**
- Use DEBUG level to see everything
- Enable DEBUG logs when debugging issues
- Check logs after every significant change
- Test with same inputs after fixes

**❌ DON'T:**
- Commit DEBUG logs to production
- Log sensitive data (passwords, API keys)
- Ignore WARNING messages
- Skip log analysis when issues occur

### Production

**✅ DO:**
- Use INFO level for standard monitoring
- Use LoggingPlugin for quick setup
- Monitor WARNING and ERROR levels
- Implement log rotation
- Set up alerts for ERROR levels
- Track metrics over time

**❌ DON'T:**
- Use DEBUG level (too verbose, performance impact)
- Log every single event
- Ignore storage limits
- Skip performance monitoring
- Forget about log retention policies

### Custom Plugins

**✅ DO:**
- Keep plugins focused (single responsibility)
- Handle errors gracefully in callbacks
- Document what metrics you're tracking
- Test plugins independently
- Use meaningful plugin names

**❌ DON'T:**
- Block agent execution in callbacks
- Throw exceptions from callbacks
- Perform heavy computation in callbacks
- Mix concerns (one plugin = one purpose)
- Forget to clean up resources

## Troubleshooting

### Issue: "No logs generated"

**Cause:** Logging not configured or wrong log file path

**Solution:**
```python
import logging
import os

# Ensure logging is configured
logging.basicConfig(
    filename="agent.log",
    level=logging.DEBUG,
    force=True,  # Override existing config
)

# Verify file is created
assert os.path.exists("agent.log"), "Log file not created"
```

### Issue: "Logs too verbose in production"

**Cause:** Using DEBUG level in production

**Solution:**
```python
# Development
logging.basicConfig(level=logging.DEBUG)

# Production
logging.basicConfig(level=logging.INFO)  # Less verbose
```

### Issue: "Can't find root cause in logs"

**Cause:** Not searching for the right keywords

**Solution:**
```bash
# Search for errors
grep -i "error" agent.log

# Search for specific tool
grep -i "count_papers" agent.log

# Search for LLM requests
grep -i "llm request" agent.log

# Search for function calls
grep -i "function_call" agent.log
```

### Issue: "Plugin callbacks not executing"

**Cause:** Plugin not added to runner or callback errors

**Solution:**
```python
# Ensure plugin is added
runner = InMemoryRunner(
    agent=agent,
    plugins=[my_plugin],  # Plugin must be in list!
)

# Add error handling to callbacks
async def before_agent_callback(self, *, agent, callback_context):
    try:
        # Your logic here
        pass
    except Exception as e:
        logging.error(f"Plugin error: {e}")
```

### Issue: "LoggingPlugin output not visible"

**Cause:** Output goes to stdout, not captured

**Solution:**
```python
# LoggingPlugin prints to stdout by default
# To capture, redirect stdout or use custom logging configuration

import sys
import logging

# Redirect stdout to file
sys.stdout = open("output.log", "w")

# Or configure root logger
logging.basicConfig(level=logging.INFO)
```

## Resources

### Official Documentation

- **Google ADK**: https://ai.google.dev/adk
- **Observability Guide**: https://ai.google.dev/adk/observability
- **Plugins Documentation**: https://ai.google.dev/adk/plugins
- **Logging Best Practices**: https://docs.python.org/3/howto/logging.html

### Course Materials

- **Kaggle Course**: [5-Day AI Agents Intensive](https://www.kaggle.com/learn-guide/5-day-genai)
- **Day 4a Notebook**: Agent Observability

### Community

- **Google ADK Discord**: Join for community support
- **GitHub Issues**: Report bugs or request features
- **Stack Overflow**: Tag `google-adk` for questions

---

## Next Steps

### Continue Learning

**Day 4b**: Agent Evaluation
- Measure agent performance
- Implement quality metrics
- Test accuracy and reliability
- Build evaluation frameworks

### Build Your Own

Apply what you've learned:
- Add observability to existing agents
- Build custom monitoring dashboard
- Create alerting system for errors
- Implement performance tracking

### Experiment

Try these modifications:
1. Build plugin that sends alerts to Slack
2. Create dashboard visualizing metrics
3. Implement cost tracking plugin
4. Build security audit plugin

---

**Happy Agent Building!** 🤖

Built with ❤️ using [Google ADK](https://ai.google.dev/adk) and [Gemini](https://ai.google.dev/gemini-api)
