# Quick Start Guide - Tool Patterns & Best Practices

**Get running in 5 minutes!** 🚀

## Prerequisites Check

```bash
# Python 3.10+
python --version

# Node.js and npx (required for MCP examples)
node --version
npx --version

# If missing Node.js:
# macOS: brew install node
# Ubuntu: sudo apt install nodejs npm
# Windows: Download from https://nodejs.org/
```

## Installation

```bash
# 1. Navigate to directory
cd day-2/day-2b

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
python tool_patterns_demo.py
```

### Demo Options

1. **MCP Integration Example** - Connect to external services
2. **Long-Running Operations Example** - Human-in-the-loop approval
3. **Run Both** - Full demonstration
4. **Exit**

## What Each Example Does

### 1. MCP Integration (`examples/1_mcp_integration.py`)

**What it demonstrates:**
- Connect to external MCP (Model Context Protocol) servers
- Use community-built integrations without custom API code
- Agent automatically gets tools from MCP server

**What you'll see:**
```
🌐 MCP INTEGRATION - Connecting to External Services
📦 Setting up MCP connection...
   Server: @modelcontextprotocol/server-everything
   Tool: getTinyImage (demo image generator)
🤖 Creating image agent with MCP integration...
✅ Agent created!

💬 Query: Can you provide a sample tiny image?

✅ Image received from MCP server!
   Format: Base64-encoded
   Size: 16x16 pixels (demo image)
```

**Key takeaway:** No custom API client code needed - just connect to MCP server and agent automatically gets the tools!

### 2. Long-Running Operations (`examples/2_long_running_operations.py`)

**What it demonstrates:**
- Pause agent execution for human approval
- Resume with preserved state
- Perfect for financial transactions, bulk operations, irreversible actions

**What you'll see:**

**Demo 1: Small Order (Auto-Approve)**
```
💬 User > Ship 3 containers to Singapore

🚀 Starting workflow...
✅ No approval needed - order completed immediately
🤖 Agent > Order auto-approved: 3 containers to Singapore
```

**Demo 2: Large Order (Requires Approval)**
```
💬 User > Ship 10 containers to Rotterdam

🚀 Starting workflow...
⏸️  Agent paused - large order requires approval
🤔 Simulating human decision: APPROVE ✅

▶️  Resuming workflow with decision...
🤖 Agent > Order approved: 10 containers to Rotterdam
```

**Demo 3: Large Order (Rejected)**
```
💬 User > Ship 8 containers to Los Angeles

🚀 Starting workflow...
⏸️  Agent paused - large order requires approval
🤔 Simulating human decision: REJECT ❌

▶️  Resuming workflow with decision...
🤖 Agent > Order rejected: 8 containers to Los Angeles
```

**Key takeaway:** Agent can pause, wait for human decision, and resume exactly where it left off!

## Quick Test Commands

```bash
# Run MCP integration only
python examples/1_mcp_integration.py

# Run long-running operations only
python examples/2_long_running_operations.py

# Test workflow utilities
python utils/workflow_helpers.py

# Check if Node.js is working
npx --version
```

## Common Issues

### "npx: command not found"

**Problem:** Node.js not installed

**Fix:**
```bash
# macOS
brew install node

# Ubuntu/Debian
sudo apt update && sudo apt install nodejs npm

# Windows
# Download from: https://nodejs.org/

# Verify
node --version
npx --version
```

### "GOOGLE_API_KEY not found"

**Problem:** Missing or incorrect API key in `.env` file

**Fix:**
1. Visit https://aistudio.google.com/app/apikey
2. Create API key
3. Add to `.env`:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

### "MCP server connection timeout"

**Problem:** Server taking too long to start

**Fix:**
- First run may be slower (npx downloads package)
- Wait 30-60 seconds
- Check internet connection
- Verify npx works: `npx --version`

## Understanding the Code

### MCP Integration Pattern

```python
# 1. Create MCP toolset
mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-everything"],
        ),
    )
)

# 2. Agent automatically gets MCP tools
agent = LlmAgent(
    tools=[mcp_toolset],  # That's it!
    instruction="Use MCP tools to help users"
)
```

### Long-Running Operations Pattern

```python
def place_order(num_items: int, tool_context: ToolContext) -> dict:
    # Small orders: Auto-approve
    if num_items <= 5:
        return {"status": "approved"}

    # Large orders: First call - PAUSE
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"Large order: {num_items} items. Approve?"
        )
        return {"status": "pending"}

    # Large orders: Resumed call - CONTINUE
    if tool_context.tool_confirmation.confirmed:
        return {"status": "approved"}
    else:
        return {"status": "rejected"}
```

### Workflow Helper Functions

```python
from utils import check_for_approval, create_approval_response

# Check if agent paused
approval_info = check_for_approval(events)

if approval_info:
    # Agent paused - get human decision
    decision = True  # or False

    # Resume with decision
    async for event in runner.run_async(
        new_message=create_approval_response(approval_info, decision),
        invocation_id=approval_info["invocation_id"]
    ):
        pass
```

## Key Concepts (2-Minute Summary)

### MCP (Model Context Protocol)

**Problem:** Building custom API integrations for every service is time-consuming

**Solution:** MCP provides standardized interface - connect once, use any MCP server

```
Your Agent → MCP Protocol → [GitHub | Slack | Database | Maps]
```

**Benefits:**
- No custom API client code
- Use community-built integrations
- Connect to multiple services simultaneously

### Long-Running Operations

**Problem:** Some operations need human approval before executing

**Solution:** Agent can pause, wait for approval, and resume with preserved state

```
Start → Detect large order → PAUSE ⏸️ → Human decides → RESUME ▶️ → Complete
```

**Benefits:**
- Human-in-the-loop for critical decisions
- State preserved across pause/resume
- Perfect for financial, bulk, or irreversible operations

### Resumability

**Without Resumability:**
```python
agent = LlmAgent(...)
# Pause → Agent forgets everything ❌
```

**With Resumability:**
```python
app = App(
    root_agent=agent,
    resumability_config=ResumabilityConfig(is_resumable=True)
)
# Pause → State saved → Resume continues ✅
```

## Next Steps

1. **Explore Examples**: Read through `examples/1_mcp_integration.py` and `examples/2_long_running_operations.py`

2. **Try Different MCP Servers**:
   ```bash
   # GitHub operations
   npx -y @modelcontextprotocol/server-github

   # Kaggle datasets
   npx -y @kaggle/kaggle-mcp

   # Slack messaging
   npx -y @modelcontextprotocol/server-slack
   ```

3. **Modify Examples**:
   - Change approval thresholds
   - Add custom approval logic
   - Connect to different MCP servers
   - Create nested approval checkpoints

4. **Read Full Documentation**: Check `README.md` for:
   - Detailed architecture explanations
   - Advanced patterns
   - Best practices
   - Troubleshooting guide

## Project Structure

```
day-2b/
├── examples/
│   ├── 1_mcp_integration.py          # MCP server connection
│   └── 2_long_running_operations.py  # Approval workflows
├── utils/
│   ├── __init__.py
│   └── workflow_helpers.py           # Helper functions
├── tool_patterns_demo.py             # Interactive demo
├── requirements.txt                  # Dependencies
├── .env.example                      # API key template
├── README.md                         # Full documentation
└── QUICKSTART.md                     # This file
```

## Resources

- **Full Documentation**: `README.md`
- **Google ADK Docs**: https://ai.google.dev/adk
- **MCP Protocol**: https://modelcontextprotocol.io
- **MCP Servers**: https://modelcontextprotocol.io/examples
- **Get API Key**: https://aistudio.google.com/app/apikey

## Need Help?

1. **Check README.md**: Comprehensive troubleshooting section
2. **Test Components**: Run examples independently
3. **Enable Logging**: Set `verbose=True` in examples
4. **Community**: Google ADK Discord, MCP Discord

---

**You're all set!** 🎉 Run `python tool_patterns_demo.py` to start exploring advanced agent patterns!
