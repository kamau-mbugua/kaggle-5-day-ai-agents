# Tool Patterns & Best Practices 🧰

**Based on Kaggle's 5-Day AI Agents Intensive Course - Day 2b**

A comprehensive guide to advanced agent tool patterns including MCP (Model Context Protocol) integration and long-running operations with human-in-the-loop approval.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Pattern 1: MCP Integration](#pattern-1-mcp-integration)
- [Pattern 2: Long-Running Operations](#pattern-2-long-running-operations)
- [Architecture & Concepts](#architecture--concepts)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Advanced Topics](#advanced-topics)
- [Resources](#resources)

## Overview

This project demonstrates two critical patterns for building production-ready AI agents:

### 1. **MCP Integration** 🌐
Connect your agents to external services using the Model Context Protocol - a standardized interface that eliminates custom API integration code.

**Key Benefits:**
- No custom API client code needed
- Use community-built integrations (GitHub, Slack, databases, etc.)
- Connect to multiple MCP servers simultaneously
- Standardized tool interface across all services

### 2. **Long-Running Operations** ⏳
Build agents that can pause execution and wait for human approval before completing critical operations.

**Key Benefits:**
- Human-in-the-loop for critical decisions
- State preservation across pause/resume cycles
- Perfect for financial transactions, bulk operations, irreversible actions
- Compliance checkpoints and approval workflows

## Quick Start

### Prerequisites

```bash
# Python 3.10+
python --version

# Node.js and npx (required for MCP examples)
node --version
npx --version

# Google ADK
pip install google-adk
```

### Installation

```bash
# 1. Navigate to project directory
cd day-2/day-2b

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file with your API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 4. Run interactive demo
python tool_patterns_demo.py
```

### Getting Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key to your `.env` file:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

## Pattern 1: MCP Integration

### What is MCP?

**Model Context Protocol (MCP)** is an open protocol that standardizes how AI applications connect to external data sources and tools. Think of it as a universal adapter for AI agents.

```
┌─────────────────────────────────────┐
│      Your AI Agent (MCP Client)     │
└──────────────┬──────────────────────┘
               │ Standard MCP Protocol
               ├──────────┬──────────┬──────────┐
               ▼          ▼          ▼          ▼
         ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
         │ GitHub  │ │  Slack  │ │Database │ │  Maps   │
         │ Server  │ │ Server  │ │ Server  │ │ Server  │
         └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

### Why Use MCP?

**Before MCP:**
```python
# Custom integration code for EVERY service
class GitHubClient:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.github.com"

    def get_issues(self):
        # 50+ lines of custom API code
        pass

class SlackClient:
    def __init__(self, token):
        # Another custom integration
        pass
```

**With MCP:**
```python
# Single standardized interface
mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
        ),
    )
)

agent = LlmAgent(tools=[mcp_toolset])
# Agent automatically gets all GitHub operations!
```

### MCP Architecture

#### Transport Layer
MCP supports multiple connection types:

1. **stdio (Standard Input/Output)**
   - Local processes communicate via stdin/stdout
   - Perfect for Node.js packages via npx
   - Example: `npx -y @modelcontextprotocol/server-everything`

2. **HTTP/SSE (Server-Sent Events)**
   - Remote servers over HTTP
   - Long-lived connections with streaming
   - Example: `http://mcp-server.example.com`

#### Connection Components

```python
mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",                    # Executor
            args=[                            # Server package
                "-y",                         # Auto-confirm install
                "@modelcontextprotocol/server-everything",
            ],
            tool_filter=["getTinyImage"],     # Selective tools
        ),
        timeout=30,                           # Connection timeout
    )
)
```

### Example: MCP Integration

See `examples/1_mcp_integration.py` for a complete working example.

```python
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Connect to MCP server
mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-everything"],
            tool_filter=["getTinyImage"],
        ),
        timeout=30,
    )
)

# Create agent with MCP tools
agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite"),
    name="image_agent",
    instruction="You are an image generation assistant using MCP tools.",
    tools=[mcp_toolset],  # MCP tools automatically available
)
```

### Popular MCP Servers

| Server | Description | Installation |
|--------|-------------|--------------|
| **@modelcontextprotocol/server-everything** | Demo server with test tools | `npx -y @modelcontextprotocol/server-everything` |
| **@modelcontextprotocol/server-github** | GitHub operations (repos, issues, PRs) | `npx -y @modelcontextprotocol/server-github` |
| **@kaggle/kaggle-mcp** | Kaggle datasets and notebooks | `npx -y @kaggle/kaggle-mcp` |
| **@modelcontextprotocol/server-slack** | Slack messaging integration | `npx -y @modelcontextprotocol/server-slack` |
| **@modelcontextprotocol/server-postgres** | PostgreSQL database operations | `npx -y @modelcontextprotocol/server-postgres` |

Find more at: [modelcontextprotocol.io](https://modelcontextprotocol.io/examples)

### MCP Tool Filtering

You can selectively enable tools from an MCP server:

```python
# Only use specific tools
tool_filter=["getTinyImage", "createFile"]

# Or allow all tools
tool_filter=None  # Default
```

## Pattern 2: Long-Running Operations

### What Are Long-Running Operations?

Operations that need to **pause** agent execution and wait for **human approval** before continuing.

### Use Cases

- **Financial Transactions**: "Transfer $10,000 to vendor" → Pause for approval
- **Bulk Operations**: "Delete 1000 user records" → Confirm before proceeding
- **High-Cost Actions**: "Spin up 50 cloud servers" → Validate resource allocation
- **Irreversible Operations**: "Permanently delete account" → Final confirmation
- **Compliance Checkpoints**: "Export PII data" → Manager approval required

### The Pause/Resume Flow

```
┌──────────────┐
│  User Query  │ "Ship 10 containers to Rotterdam"
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────┐
│ STEP 1: Agent Starts Processing                  │
│ - Agent receives query                            │
│ - Calls place_shipping_order(10, "Rotterdam")    │
│ - Tool detects: 10 > threshold (5)               │
│ - Tool calls: tool_context.request_confirmation()│
│ - Returns: {"status": "pending"}                  │
└──────┬───────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────┐
│ STEP 2: ADK Creates Special Event                │
│ - Event type: "adk_request_confirmation"         │
│ - Contains: hint, payload, approval_id           │
│ - Workflow detects this event                     │
│ - Execution PAUSED ⏸️                             │
└──────┬───────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────┐
│ STEP 3: Human Decision                           │
│ - Display: "⚠️ Large order: 10 containers"       │
│ - Human decides: APPROVE ✅ or REJECT ❌          │
│ - Format decision as FunctionResponse            │
└──────┬───────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────┐
│ STEP 4: Resume Execution                         │
│ - Call run_async() with SAME invocation_id       │
│ - Pass human decision as new_message             │
│ - Tool receives: tool_context.tool_confirmation  │
│ - Tool checks: .confirmed == True or False       │
│ - Returns final result                            │
│ - Execution COMPLETE ✅                           │
└───────────────────────────────────────────────────┘
```

### Implementation: Three Scenarios

#### Scenario 1: Small Orders (Auto-Approve)

```python
def place_shipping_order(
    num_containers: int,
    destination: str,
    tool_context: ToolContext
) -> dict:
    # Auto-approve small orders
    if num_containers <= 5:
        return {
            "status": "approved",
            "order_id": f"ORD-{num_containers}-AUTO",
            "message": f"Order auto-approved: {num_containers} containers"
        }
```

#### Scenario 2: Large Order - First Call (Pause)

```python
    # PAUSE: This is the first call for a large order
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"⚠️ Large order: {num_containers} containers to {destination}. Approve?",
            payload={"num_containers": num_containers, "destination": destination}
        )
        return {
            "status": "pending",
            "message": f"Order requires approval"
        }
```

#### Scenario 3: Large Order - Resumed Call (Continue)

```python
    # CONTINUE: This is the resumed call after human decision
    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "approved",
            "order_id": f"ORD-{num_containers}-HUMAN",
            "message": f"Order approved: {num_containers} containers"
        }
    else:
        return {
            "status": "rejected",
            "message": f"Order rejected by human"
        }
```

### Why Resumability Matters

**Without Resumability:**
```python
# ❌ Agent forgets everything when paused
agent = LlmAgent(...)
runner = InMemoryRunner(agent=agent)
# Pause → Agent loses context → Can't resume
```

**With Resumability:**
```python
# ✅ State preserved across pause/resume
agent = LlmAgent(...)
app = App(
    root_agent=agent,
    resumability_config=ResumabilityConfig(is_resumable=True)
)
runner = Runner(app=app, session_service=InMemorySessionService())
# Pause → State saved → Resume continues seamlessly
```

### Complete Workflow Example

See `examples/2_long_running_operations.py` for full implementation.

```python
async def run_shipping_workflow(runner, session_service, query, auto_approve=True):
    # Step 1: Send initial request
    session_id = f"order_{uuid.uuid4().hex[:8]}"
    await session_service.create_session(
        app_name="shipping_coordinator",
        user_id="test_user",
        session_id=session_id
    )

    events = []
    async for event in runner.run_async(
        user_id="test_user",
        session_id=session_id,
        new_message=query_content
    ):
        events.append(event)

    # Step 2: Check if agent paused
    approval_info = check_for_approval(events)

    # Step 3: Handle approval workflow
    if approval_info:
        # Human makes decision
        decision = auto_approve  # In production: get_human_decision()

        # Step 4: Resume with decision
        async for event in runner.run_async(
            user_id="test_user",
            session_id=session_id,
            new_message=create_approval_response(approval_info, decision),
            invocation_id=approval_info["invocation_id"],  # Same invocation!
        ):
            # Agent continues and completes
            pass
```

## Architecture & Concepts

### Components Overview

```
┌────────────────────────────────────────────────────────────┐
│                         Your Application                    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐  │
│  │                    App (Resumable)                   │  │
│  │  ┌─────────────────────────────────────────────┐   │  │
│  │  │              LlmAgent                        │   │  │
│  │  │  - Gemini model                              │   │  │
│  │  │  - Instructions                              │   │  │
│  │  │  - Tools                                     │   │  │
│  │  └──────────────────┬──────────────────────────┘   │  │
│  │                     │                               │  │
│  │         ┌───────────┼───────────┐                   │  │
│  │         │           │           │                   │  │
│  │         ▼           ▼           ▼                   │  │
│  │   ┌─────────┐ ┌─────────┐ ┌─────────┐             │  │
│  │   │   MCP   │ │Function │ │ Custom  │             │  │
│  │   │ Toolset │ │  Tools  │ │  Tools  │             │  │
│  │   └─────────┘ └─────────┘ └─────────┘             │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐  │
│  │                  Runner                              │  │
│  │  - Orchestrates execution                            │  │
│  │  - Manages sessions                                  │  │
│  │  - Handles pause/resume                              │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐  │
│  │            InMemorySessionService                    │  │
│  │  - Stores session state                              │  │
│  │  - Preserves conversation history                    │  │
│  │  - Maintains tool context                            │  │
│  └─────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

### Key Classes

#### App & ResumabilityConfig

```python
from google.adk.apps.app import App, ResumabilityConfig

app = App(
    name="shipping_coordinator",
    root_agent=agent,
    resumability_config=ResumabilityConfig(is_resumable=True)
)
```

**What it does:**
- Wraps agent with state management
- Enables pause/resume capability
- Preserves conversation history and tool context

#### ToolContext

```python
from google.adk.tools.tool_context import ToolContext

def my_tool(param: str, tool_context: ToolContext) -> dict:
    # First call: tool_confirmation is None
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint="Waiting for approval",
            payload={"param": param}
        )
        return {"status": "pending"}

    # Resumed call: tool_confirmation has human decision
    if tool_context.tool_confirmation.confirmed:
        return {"status": "approved"}
```

**What it provides:**
- `tool_confirmation`: None (first call) or ToolConfirmation (resumed)
- `request_confirmation()`: Method to pause execution
- `.confirmed`: Boolean indicating human decision (True/False)

#### Runner & Sessions

```python
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()
runner = Runner(app=app, session_service=session_service)

# Create session
await session_service.create_session(
    app_name="shipping_coordinator",
    user_id="user_123",
    session_id="session_abc"
)

# Run with session
async for event in runner.run_async(
    user_id="user_123",
    session_id="session_abc",
    new_message=query,
    invocation_id=None  # First call, or previous invocation_id to resume
):
    process(event)
```

### Event Types

#### Standard Events

```python
# Text response from agent
if event.content and event.content.parts:
    for part in event.content.parts:
        if part.text:
            print(f"Agent: {part.text}")

# Function call event
if part.function_call:
    print(f"Calling: {part.function_call.name}")

# Function response
if part.function_response:
    print(f"Result: {part.function_response.response}")
```

#### Special Event: adk_request_confirmation

```python
# Detect pause request
for event in events:
    if event.content and event.content.parts:
        for part in event.content.parts:
            if (part.function_call and
                part.function_call.name == "adk_request_confirmation"):
                # Agent has paused!
                approval_id = part.function_call.id
                invocation_id = event.invocation_id
                # Now wait for human decision
```

## Best Practices

### MCP Integration Best Practices

#### 1. **Tool Filtering**
Only enable the tools you need:

```python
# ✅ Good: Selective tools
tool_filter=["getTinyImage", "uploadFile"]

# ❌ Bad: All tools enabled (security risk)
tool_filter=None
```

#### 2. **Timeout Configuration**
Set appropriate timeouts for server connections:

```python
# ✅ Good: Reasonable timeout
timeout=30  # 30 seconds for connection

# ❌ Bad: Too short (fails often)
timeout=5

# ❌ Bad: Too long (hangs)
timeout=300
```

#### 3. **Error Handling**
Always handle MCP connection failures:

```python
try:
    mcp_toolset = create_mcp_toolset()
except Exception as e:
    print(f"❌ MCP connection failed: {e}")
    print("⚠️  Check: Node.js installed? npx available?")
    # Fallback to alternative tools or graceful degradation
```

#### 4. **Instruction Clarity**
Tell the agent how to use MCP tools:

```python
agent = LlmAgent(
    instruction="""You are an image assistant.

    When users request images:
    1. Use the getTinyImage tool from MCP server
    2. Explain this is a demo tool (16x16 test image)
    3. Let user know when image is generated

    Be friendly and explain what MCP is if asked.
    """,
    tools=[mcp_toolset]
)
```

### Long-Running Operations Best Practices

#### 1. **Clear Thresholds**
Define explicit thresholds for approval:

```python
# ✅ Good: Clear business rule
LARGE_ORDER_THRESHOLD = 5
if num_containers > LARGE_ORDER_THRESHOLD:
    # Request approval

# ❌ Bad: Magic number
if num_containers > 5:  # Why 5? Unclear.
```

#### 2. **Informative Hints**
Provide context in confirmation requests:

```python
# ✅ Good: Detailed hint
tool_context.request_confirmation(
    hint=f"⚠️ Large order: {num_containers} containers to {destination}. "
         f"Cost: ${num_containers * 5000}. Approve?",
    payload={
        "num_containers": num_containers,
        "destination": destination,
        "estimated_cost": num_containers * 5000
    }
)

# ❌ Bad: Vague hint
tool_context.request_confirmation(
    hint="Approve?",
    payload={}
)
```

#### 3. **Payload Completeness**
Include all information needed for human decision:

```python
# ✅ Good: Complete payload
payload={
    "num_containers": num_containers,
    "destination": destination,
    "estimated_cost": cost,
    "delivery_date": date,
    "vendor": vendor_name,
    "requester": user_id
}

# ❌ Bad: Incomplete payload
payload={"num_containers": num_containers}
```

#### 4. **Session Management**
Use meaningful session IDs:

```python
# ✅ Good: Descriptive session ID
session_id = f"order_{uuid.uuid4().hex[:8]}_{timestamp}"

# ✅ Good: User-based session
session_id = f"user_{user_id}_workflow_{uuid.uuid4().hex[:8]}"

# ❌ Bad: Generic session
session_id = str(uuid.uuid4())
```

#### 5. **Error Recovery**
Handle approval workflow failures gracefully:

```python
try:
    approval_info = check_for_approval(events)
    if approval_info:
        # Resume with decision
        async for event in runner.run_async(...):
            pass
    else:
        # No approval needed
        print_agent_response(events)
except Exception as e:
    # Approval workflow failed
    logger.error(f"Approval workflow error: {e}")
    # Notify user, rollback, or retry
```

### Retry Configuration

Always configure retries for transient errors:

```python
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,              # Retry up to 5 times
    exp_base=7,             # Exponential backoff base
    initial_delay=1,        # Start with 1 second delay
    http_status_codes=[429, 500, 503, 504]  # Retry on these codes
)

model = Gemini(
    model="gemini-2.5-flash-lite",
    retry_options=retry_config
)
```

## Troubleshooting

### MCP Integration Issues

#### Problem: "npx: command not found"

**Cause:** Node.js/npx not installed

**Solution:**
```bash
# Install Node.js
# macOS
brew install node

# Ubuntu/Debian
sudo apt update && sudo apt install nodejs npm

# Windows
# Download from: https://nodejs.org/

# Verify installation
node --version
npx --version
```

#### Problem: "MCP server connection timeout"

**Cause:** Server taking too long to start or network issues

**Solution:**
```python
# Increase timeout
mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(...),
        timeout=60,  # Increase to 60 seconds
    )
)
```

#### Problem: "Tool 'xyz' not found in MCP server"

**Cause:** Tool name mismatch or not available in server

**Solution:**
```python
# 1. Check available tools (remove tool_filter temporarily)
mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(...),
        tool_filter=None,  # Get all tools
    )
)

# 2. Print available tools
print(mcp_toolset.get_available_tools())

# 3. Use correct tool names
tool_filter=["correctToolName"]
```

#### Problem: "RuntimeError: Attempted to exit cancel scope in a different task" on exit

**Cause:** MCP stdio client cleanup race condition (known issue)

**Impact:** This is a harmless cleanup warning that appears when the program exits. It doesn't affect functionality.

**Solution:**
```python
# Already handled in examples with:
# 1. Finally block with cleanup attempt
# 2. Small delay before exit: await asyncio.sleep(0.1)

# This warning can be safely ignored - it occurs during
# async generator cleanup and doesn't indicate a problem
# with your code or the MCP integration.
```

#### Problem: "Permission denied" when running MCP server

**Cause:** Insufficient permissions or security restrictions

**Solution:**
```bash
# macOS: Grant terminal permissions in System Preferences

# Linux: Check script permissions
chmod +x mcp-server-script

# Windows: Run terminal as administrator
```

### Long-Running Operations Issues

#### Problem: "Agent doesn't resume after approval"

**Cause:** Wrong invocation_id or session_id

**Solution:**
```python
# ✅ Save invocation_id from approval event
approval_info = check_for_approval(events)
saved_invocation_id = approval_info["invocation_id"]

# ✅ Use SAME invocation_id when resuming
async for event in runner.run_async(
    user_id="test_user",
    session_id=session_id,  # Same session!
    new_message=approval_response,
    invocation_id=saved_invocation_id  # Same invocation!
):
    pass
```

#### Problem: "tool_context.tool_confirmation is always None"

**Cause:** Not using resumable App or wrong function signature

**Solution:**
```python
# ✅ Correct: Use App with resumability
app = App(
    root_agent=agent,
    resumability_config=ResumabilityConfig(is_resumable=True)
)
runner = Runner(app=app, session_service=session_service)

# ✅ Correct: Include tool_context parameter
def my_tool(param: str, tool_context: ToolContext) -> dict:
    if not tool_context.tool_confirmation:
        # First call
        pass
    else:
        # Resumed call
        pass
```

#### Problem: "Session not found when resuming"

**Cause:** Session expired or not created properly

**Solution:**
```python
# ✅ Create session before first call
await session_service.create_session(
    app_name="my_app",
    user_id="user_123",
    session_id="session_abc"
)

# ✅ Use same session_id throughout workflow
# First call
async for event in runner.run_async(
    session_id="session_abc",  # Same ID
    ...
):
    pass

# Resume call
async for event in runner.run_async(
    session_id="session_abc",  # Same ID
    ...
):
    pass
```

#### Problem: "Events not captured correctly"

**Cause:** Not collecting all events before checking for approval

**Solution:**
```python
# ✅ Collect ALL events first
events = []
async for event in runner.run_async(...):
    events.append(event)

# ✅ Then check for approval
approval_info = check_for_approval(events)

# ❌ Wrong: Check during iteration
async for event in runner.run_async(...):
    if check_for_approval([event]):  # Incomplete!
        pass
```

### Corrupted Virtual Environment

#### Problem: "IndentationError: expected an indented block" in anyio library

**Cause:** Virtual environment corruption (often after installation issues)

**Symptoms:**
- Error in `anyio/_backends/_asyncio.py` line 459
- IndentationError with stray character `c`
- Happens when running any async code

**Solution:**
```bash
# Rebuild virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Verify fix
python examples/2_long_running_operations.py
```

### General Debugging Tips

#### Enable Verbose Logging

```python
# For MCP integration
import logging
logging.basicConfig(level=logging.DEBUG)

# For agent debugging
response = await runner.run_debug(query, verbose=True)
```

#### Test Components Independently

```bash
# Test MCP server directly
npx -y @modelcontextprotocol/server-everything

# Test tool function independently
result = place_shipping_order(10, "Singapore", mock_context)
print(result)

# Test event parsing
approval_info = check_for_approval(sample_events)
print(approval_info)
```

#### Check Event Structure

```python
# Print all events for debugging
for i, event in enumerate(events):
    print(f"\n=== Event {i} ===")
    print(f"Role: {event.content.role if event.content else 'N/A'}")
    if event.content and event.content.parts:
        for part in event.content.parts:
            if part.text:
                print(f"Text: {part.text}")
            if part.function_call:
                print(f"Function call: {part.function_call.name}")
            if part.function_response:
                print(f"Function response: {part.function_response.response}")
```

## Advanced Topics

### Multiple MCP Servers

Connect to multiple MCP servers simultaneously:

```python
# Create multiple toolsets
github_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
        )
    )
)

kaggle_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@kaggle/kaggle-mcp"],
        )
    )
)

# Agent gets tools from both servers
agent = LlmAgent(
    tools=[github_tools, kaggle_tools],
    instruction="""You can:
    - Manage GitHub repositories using github_tools
    - Access Kaggle datasets using kaggle_tools
    """
)
```

### Nested Approvals

Handle multiple approval checkpoints:

```python
def complex_operation(tool_context: ToolContext) -> dict:
    # Checkpoint 1: Data validation
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint="Checkpoint 1: Data validated. Proceed to processing?",
            payload={"checkpoint": 1, "data_size": 1000}
        )
        return {"status": "pending", "checkpoint": 1}

    # After checkpoint 1 approval
    if tool_context.tool_confirmation.payload.get("checkpoint") == 1:
        # Process data...
        # Checkpoint 2: Final confirmation
        tool_context.request_confirmation(
            hint="Checkpoint 2: Processing complete. Commit changes?",
            payload={"checkpoint": 2, "changes": 500}
        )
        return {"status": "pending", "checkpoint": 2}

    # After checkpoint 2 approval
    if tool_context.tool_confirmation.confirmed:
        return {"status": "approved", "message": "All checkpoints passed"}
```

### Custom Approval UI

Integrate with custom approval systems:

```python
async def get_human_approval(approval_info: dict) -> bool:
    """
    Send approval request to custom system.
    Could be: Slack message, email, web dashboard, etc.
    """
    hint = approval_info["hint"]
    payload = approval_info["payload"]

    # Example: Send to Slack
    slack_client = SlackClient(token=os.getenv("SLACK_TOKEN"))
    message = slack_client.send_approval_request(
        channel="#approvals",
        hint=hint,
        payload=payload,
        buttons=["Approve", "Reject"]
    )

    # Wait for human response (webhook, polling, etc.)
    response = await slack_client.wait_for_response(message.id, timeout=3600)

    return response.action == "Approve"
```

### Conditional Approval Logic

Different approval flows based on context:

```python
def smart_approval(amount: float, user_role: str, tool_context: ToolContext) -> dict:
    # Manager: Auto-approve up to $10,000
    if user_role == "manager" and amount <= 10000:
        return {"status": "approved", "reason": "manager_auto_approved"}

    # Executive: Auto-approve up to $50,000
    if user_role == "executive" and amount <= 50000:
        return {"status": "approved", "reason": "executive_auto_approved"}

    # Everyone else: Require approval
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"⚠️ Approval needed: ${amount} (user: {user_role})",
            payload={"amount": amount, "user_role": user_role}
        )
        return {"status": "pending"}

    # Process approval decision
    if tool_context.tool_confirmation.confirmed:
        return {"status": "approved", "reason": "human_approved"}
    else:
        return {"status": "rejected", "reason": "human_rejected"}
```

### Approval Audit Trail

Log all approval decisions for compliance:

```python
import json
from datetime import datetime

def log_approval_decision(approval_info: dict, decision: bool, user_id: str):
    """Log approval decisions for audit trail."""
    audit_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "invocation_id": approval_info["invocation_id"],
        "hint": approval_info["hint"],
        "payload": approval_info["payload"],
        "decision": "APPROVED" if decision else "REJECTED",
        "decided_by": user_id,
    }

    # Save to audit log
    with open("approvals_audit.jsonl", "a") as f:
        f.write(json.dumps(audit_entry) + "\n")

    print(f"✅ Audit logged: {audit_entry}")
```

## Resources

### Official Documentation

- **Google ADK**: [Google AI Developer Kit](https://ai.google.dev/adk)
- **Gemini Models**: [Gemini API Documentation](https://ai.google.dev/gemini-api)
- **MCP Protocol**: [Model Context Protocol](https://modelcontextprotocol.io)
- **MCP Servers**: [MCP Examples](https://modelcontextprotocol.io/examples)

### MCP Server Repositories

- **Everything Server**: [@modelcontextprotocol/server-everything](https://github.com/modelcontextprotocol/servers/tree/main/src/everything)
- **GitHub Server**: [@modelcontextprotocol/server-github](https://github.com/modelcontextprotocol/servers/tree/main/src/github)
- **Kaggle Server**: [@kaggle/kaggle-mcp](https://github.com/Kaggle/kaggle-mcp)
- **Slack Server**: [@modelcontextprotocol/server-slack](https://github.com/modelcontextprotocol/servers/tree/main/src/slack)

### Course Materials

- **Kaggle Course**: [5-Day AI Agents Intensive](https://www.kaggle.com/learn-guide/5-day-genai)
- **Day 2b Notebook**: Tool Patterns and Best Practices

### Community

- **ADK Discord**: [Google ADK Community](https://discord.gg/google-adk)
- **MCP Community**: [MCP Protocol Discord](https://discord.gg/mcp)
- **Stack Overflow**: Tag `google-adk` or `model-context-protocol`

### Video Tutorials

- **MCP Introduction**: [Understanding Model Context Protocol](https://youtube.com/watch?v=mcp-intro)
- **Long-Running Operations**: [Building Approval Workflows](https://youtube.com/watch?v=approval-workflows)

---

## Quick Reference

### MCP Setup Checklist

- [ ] Node.js and npx installed (`node --version`, `npx --version`)
- [ ] Google API key in `.env` file
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] MCP server package identified (e.g., `@modelcontextprotocol/server-github`)
- [ ] Tool filter configured (selective tools for security)
- [ ] Timeout set appropriately (30-60 seconds)
- [ ] Error handling implemented (connection failures)
- [ ] Agent instructions updated (how to use MCP tools)

### Long-Running Operations Checklist

- [ ] ToolContext parameter added to function signature
- [ ] Clear threshold defined (when to request approval)
- [ ] Informative hint created (context for human decision)
- [ ] Complete payload included (all decision-making data)
- [ ] App wrapped with ResumabilityConfig
- [ ] Session service configured (InMemorySessionService)
- [ ] Session created before workflow start
- [ ] Events collected and checked for approval request
- [ ] Resume with same invocation_id and session_id
- [ ] Approval response formatted correctly (FunctionResponse)

### Common Commands

```bash
# Run interactive demo
python tool_patterns_demo.py

# Run MCP example
python examples/1_mcp_integration.py

# Run long-running example
python examples/2_long_running_operations.py

# Check Node.js setup
node --version && npx --version

# Test MCP server directly
npx -y @modelcontextprotocol/server-everything

# View workflow helpers
python -c "from utils import check_for_approval; help(check_for_approval)"
```

---

**Ready to build production-ready AI agents?** Start with the [Quick Start](#quick-start) section and explore the examples! 🚀
