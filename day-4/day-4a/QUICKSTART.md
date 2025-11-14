# Quick Start Guide - Agent Observability

**Get running in 5 minutes!** 🚀

## Prerequisites Check

```bash
# Python 3.10+
python --version

# Install Google ADK
pip install google-adk
```

## Installation

```bash
# 1. Navigate to directory
cd day-4/day-4a

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env

# 4. Add your API key to .env
# Get your key from: https://aistudio.google.com/app/apikey
```

Your `.env` file should look like:
```
GOOGLE_API_KEY=AIzaSy...your_actual_key_here
```

## Run the Demo

```bash
python observability_demo.py
```

### Demo Options

1. **Basic Logging Setup** - DEBUG, INFO, WARNING, ERROR levels
2. **Debugging Broken Agents** - symptom → logs → fix workflow
3. **Production Logging** - LoggingPlugin for automated observability
4. **Custom Plugins** - Build your own monitoring tools
5. **Run All** - Full tour

## What Each Example Does

### 1. Basic Logging Setup (`examples/example_1_basic_logging.py`)

**What it demonstrates:**
- Configure logging with different levels
- Understand what each level captures
- When to use each level

**What you'll see:**
```
DEMO 1: DEBUG Level Logging
✅ Captures: Full LLM requests, responses, tool calls, everything

DEMO 2: INFO Level Logging
✅ Captures: Key events, agent starts/completions, major milestones

DEMO 3: WARNING Level Logging
✅ Captures: Potential issues, retries, deprecated features

DEMO 4: ERROR Level Logging
✅ Captures: Exception messages, stack traces, critical failures

Comparison Table:
┌─────────────┬──────────────────────┬─────────────────────┐
│ Level       │ What It Captures     │ When to Use         │
├─────────────┼──────────────────────┼─────────────────────┤
│ DEBUG       │ Everything           │ Development         │
│ INFO        │ Key events           │ Production          │
│ WARNING     │ Potential issues     │ Monitoring          │
│ ERROR       │ Failures             │ Alerting            │
└─────────────┴──────────────────────┴─────────────────────┘
```

**Key takeaway:** DEBUG for development, INFO for production

---

### 2. Debugging Broken Agents (`examples/example_2_debugging_broken_agent.py`)

**What it demonstrates:**
- Intentionally broken agent (type mismatch bug)
- Systematic debugging workflow
- Using DEBUG logs to find root cause
- Fix and verify

**What you'll see:**
```
DEMO 1: Broken Research Paper Finder
Agent returns suspiciously high paper count ❌

DEMO 2: Analyze the Failure
🔍 Examining DEBUG logs...

DEMO 3: Root Cause Analysis
🎯 DEBUGGING WORKFLOW:
  Step 1: Symptom → High count
  Step 2: Logs → Search for count_papers
  Step 3: LLM Request → Function call details
  Step 4: Root Cause → Type mismatch!
          count_papers expects: str
          Agent passes: List[str]
          Result: len() counts characters, not items!
  Step 5: Fix → Change type to List[str]

DEMO 4: Fix and Verify
✅ Fixed agent works correctly!

Common Failure Patterns:
┌─────────────────────────────┬──────────────────────────┐
│ Symptom                     │ Root Cause               │
├─────────────────────────────┼──────────────────────────┤
│ "Cannot help"               │ Missing tool             │
│ Wrong results               │ Type mismatch            │
│ Agent loops                 │ Ambiguous instructions   │
│ Tool not called             │ Poor description         │
└─────────────────────────────┴──────────────────────────┘
```

**Key takeaway:** Symptom → Logs → Root Cause → Fix → Verify

---

### 3. Production Logging (`examples/example_3_production_logging.py`)

**What it demonstrates:**
- ADK's built-in LoggingPlugin
- Zero-config observability
- Structured logging output
- When to use LoggingPlugin vs custom

**What you'll see:**
```
DEMO 1: Understanding LoggingPlugin
Automatically captures:
  🚀 User messages and responses
  ⏱️  Timing data
  🧠 LLM requests/responses
  🔧 Tool calls/results
  ✅ Complete execution traces

DEMO 2: Agent with LoggingPlugin
runner = InMemoryRunner(
    agent=agent,
    plugins=[LoggingPlugin()]  # This line!
)

DEMO 3: Watch LoggingPlugin in Action
[logging_plugin] 🚀 USER MESSAGE RECEIVED
[logging_plugin] 🧠 LLM REQUEST
[logging_plugin] 🧠 LLM RESPONSE
[logging_plugin] 🔧 TOOL STARTING
[logging_plugin] 🔧 TOOL COMPLETED
[logging_plugin] ✅ INVOCATION COMPLETED

Decision Matrix:
┌─────────────────────────────┬──────────────────────────┐
│ Use LoggingPlugin When      │ Use Custom Plugin When   │
├─────────────────────────────┼──────────────────────────┤
│ Standard observability      │ Custom metrics needed    │
│ Quick setup                 │ External integration     │
│ Debugging issues            │ Special formatting       │
│ Audit trails                │ Selective logging        │
└─────────────────────────────┴──────────────────────────┘
```

**Key takeaway:** LoggingPlugin = zero-config production observability

---

### 4. Custom Plugins (`examples/example_4_custom_plugins.py`)

**What it demonstrates:**
- Build custom plugins from scratch
- Implement different callback types
- Collect custom metrics
- Combine multiple plugins

**What you'll see:**
```
DEMO 1: What are Plugins?
Plugin = Collection of Callbacks
Callbacks = Hooks into agent lifecycle

Available callbacks:
  • before_agent_callback
  • after_agent_callback
  • before_tool_callback
  • after_tool_callback
  • before_model_callback
  • after_model_callback

DEMO 2: Create 3 Custom Plugins
  1. InvocationCounterPlugin   → Counts calls
  2. PerformanceMonitorPlugin  → Tracks time
  3. ToolUsageTrackerPlugin    → Monitors tools

DEMO 3: Multiple Plugins Together
runner = InMemoryRunner(
    agent=agent,
    plugins=[counter, performance, tracker]
)

DEMO 4: Collected Metrics
📊 InvocationCounterPlugin:
  • agent_invocations: 3
  • tool_calls: 6
  • llm_requests: 9

⏱️  PerformanceMonitorPlugin:
  • avg_agent_time: 2.3s
  • avg_tool_time: 0.8s

🔧 ToolUsageTrackerPlugin:
  • google_search: 6 calls

Plugin Lifecycle:
  User query
     ↓
  before_agent_callback ⚡
     ↓
  Agent processing
     ↓
  before_tool_callback ⚡
     ↓
  Tool execution
     ↓
  after_tool_callback ⚡
     ↓
  after_agent_callback ⚡
     ↓
  Response
```

**Key takeaway:** Custom plugins for specialized monitoring needs

---

## Quick Test Commands

```bash
# Run individual examples
python examples/example_1_basic_logging.py
python examples/example_2_debugging_broken_agent.py
python examples/example_3_production_logging.py
python examples/example_4_custom_plugins.py

# Run interactive demo
python observability_demo.py
```

## Common Issues

### "GOOGLE_API_KEY not found"

**Problem:** Missing or incorrect API key in `.env` file

**Fix:**
1. Visit https://aistudio.google.com/app/apikey
2. Create API key
3. Add to `.env`:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

### "Module not found"

**Problem:** Dependencies not installed

**Fix:**
```bash
pip install -r requirements.txt
```

### "No logs generated"

**Problem:** Logging not configured

**Fix:**
```python
import logging

logging.basicConfig(
    filename="agent.log",
    level=logging.DEBUG,
    force=True,  # Override existing config
)
```

## Understanding the Code

### Basic Logging Pattern

```python
import logging

# Configure logging level
logging.basicConfig(
    filename="agent.log",
    level=logging.DEBUG,  # or INFO, WARNING, ERROR
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Run agent
# Logs are automatically written to agent.log
```

### Debugging Pattern

```python
# 1. Symptom: Agent behaves unexpectedly

# 2. Enable DEBUG logging
logging.basicConfig(level=logging.DEBUG)

# 3. Run agent and check logs
# 4. Find root cause in logs
# 5. Apply fix
# 6. Verify with same input
```

### Production Pattern (LoggingPlugin)

```python
from google.adk.runners import InMemoryRunner
from google.adk.plugins.logging_plugin import LoggingPlugin

# Add LoggingPlugin to runner
runner = InMemoryRunner(
    agent=agent,
    plugins=[LoggingPlugin()],  # Automatic observability!
)

# Everything is logged automatically
response = await runner.run_debug("Your query")
```

### Custom Plugin Pattern

```python
from google.adk.plugins.base_plugin import BasePlugin

class MyPlugin(BasePlugin):
    def __init__(self):
        super().__init__(name="my_plugin")
        self.metrics = {}

    async def before_agent_callback(self, *, agent, callback_context):
        # Custom logic before agent runs
        pass

    async def after_agent_callback(self, *, agent, callback_context):
        # Custom logic after agent completes
        pass

# Use plugin
runner = InMemoryRunner(
    agent=agent,
    plugins=[MyPlugin()],
)
```

## Key Concepts (2-Minute Summary)

### The Observability Problem

```
Traditional Software:
  divide_by_zero() → Clear: ZeroDivisionError

AI Agents:
  "Find papers" → "I cannot help"  ← Why??
```

### The Solution

```
Observability = X-ray Vision for Agents

See:
  ✅ Exact prompts sent to LLM
  ✅ Available tools
  ✅ Model responses
  ✅ Where failures occur
```

### Three Pillars

| Pillar | What | Example |
|--------|------|---------|
| **Logs** | Single events | "Agent started" |
| **Traces** | Connected story | "Query → LLM → Tool → Response" |
| **Metrics** | Statistics | "Avg time: 2.3s" |

### Log Levels

```
DEBUG    → Everything (development)
INFO     → Key events (production)
WARNING  → Issues (monitoring)
ERROR    → Failures (alerting)
```

### Debugging Workflow

```
1. Symptom    → What went wrong?
2. Logs       → Check DEBUG logs
3. Root Cause → Trace execution
4. Fix        → Apply correction
5. Verify     → Test again
```

### Plugin Types

```
LoggingPlugin → Built-in, zero-config
Custom Plugin → Build your own for special needs
```

## Next Steps

1. **Explore Examples**: Run all 4 example files
2. **Modify & Experiment**: Add your own logging, build custom plugins
3. **Read Full Documentation**: Check `README.md` for deep dives
4. **Build Your Own**: Apply observability to your agents

## Project Structure

```
day-4a/
├── examples/
│   ├── example_1_basic_logging.py          # Log levels
│   ├── example_2_debugging_broken_agent.py # Debug workflow
│   ├── example_3_production_logging.py     # LoggingPlugin
│   └── example_4_custom_plugins.py         # Custom plugins
├── utils/
│   ├── __init__.py
│   └── observability_helpers.py            # Helper functions
├── observability_demo.py                   # Interactive demo
├── requirements.txt                        # Dependencies
├── .env.example                            # API key template
├── README.md                               # Full documentation
└── QUICKSTART.md                           # This file
```

## Resources

- **Full Documentation**: `README.md`
- **Google ADK Docs**: https://ai.google.dev/adk
- **Observability Guide**: https://ai.google.dev/adk/observability
- **Get API Key**: https://aistudio.google.com/app/apikey

## Need Help?

1. **Check README.md**: Comprehensive troubleshooting section
2. **Test Components**: Run examples independently
3. **Verify Setup**: Check `.env` file and dependencies
4. **Community**: Google ADK Discord for support

---

**You're all set!** 🎉 Run `python observability_demo.py` to start exploring agent observability!
