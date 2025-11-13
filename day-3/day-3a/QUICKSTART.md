# Quick Start Guide - Agent Sessions

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
cd day-3/day-3a

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
python session_management_demo.py
```

### Demo Options

1. **Stateful Agent** - Memory with InMemorySessionService
2. **Persistent Sessions** - DatabaseSessionService
3. **Context Compaction** - EventsCompactionConfig
4. **Session State** - Custom tools for structured data
5. **Run All** - Full tour

## What Each Example Does

### 1. Stateful Agent (`examples/1_stateful_agent.py`)

**What it demonstrates:**
- Building agents that remember conversations
- Using InMemorySessionService (temporary storage)
- How sessions maintain context

**What you'll see:**
```
DEMO 1: First Conversation
User > Hi, I'm Sam! What is the capital of United States?
Agent > Hi Sam! The capital is Washington, D.C.

User > What is my name?
Agent > Your name is Sam  ✅ Remembers!

DEMO 2: New Session
User > What is my name?
Agent > I don't know your name  ❌ Fresh start
```

**Key takeaway:** Same session_id = Agent remembers; Different session_id = Fresh start

---

### 2. Persistent Sessions (`examples/2_persistent_sessions.py`)

**What it demonstrates:**
- Upgrading to persistent storage with SQLite
- Conversations that survive application restarts
- Session isolation and privacy

**What you'll see:**
```
DEMO 1: Store information
User > Hi, I'm Sam!
Agent > Nice to meet you, Sam!
💾 Stored in: agent_sessions.db

DEMO 2: After restart
User > What's my name?
Agent > Your name is Sam  ✅ Still remembers!
```

**Key takeaway:** DatabaseSessionService persists data across restarts

---

### 3. Context Compaction (`examples/3_context_compaction.py`)

**What it demonstrates:**
- Automatic history summarization
- Reducing token usage for long conversations
- Configuring compaction interval and overlap

**What you'll see:**
```
Turn 1: AI in healthcare?
Turn 2: Drug discovery developments?
Turn 3: Tell me more about second development
🔄 Compaction triggered! History summarized

Turn 4: Who are the main companies?
✅ Agent maintains context with 70% fewer tokens
```

**Key takeaway:** Compaction reduces costs while maintaining conversation quality

---

### 4. Session State (`examples/4_session_state.py`)

**What it demonstrates:**
- Using session.state for structured data
- Custom tools that read/write state
- State isolation between sessions

**What you'll see:**
```
User > My name is Sam. I'm from Poland.
🔧 Tool: save_userinfo(name="Sam", country="Poland")
💾 State: {"user:name": "Sam", "user:country": "Poland"}

User > What's my name and country?
🔧 Tool: retrieve_userinfo()
Agent > Your name is Sam and you're from Poland ✅
```

**Key takeaway:** State = Structured data; Events = Conversation history

---

## Quick Test Commands

```bash
# Run individual examples
python examples/example_1_stateful_agent.py
python examples/example_2_persistent_sessions.py
python examples/example_3_context_compaction.py
python examples/example_4_session_state.py

# Run interactive demo
python session_management_demo.py
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

### "Database locked"

**Problem:** SQLite database in use by another process

**Fix:**
```bash
# Close any other running instances
# Or delete the database file
rm *.db
```

## Understanding the Code

### Basic Session Pattern

```python
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

# 1. Create agent
agent = Agent(...)

# 2. Create session service
session_service = InMemorySessionService()

# 3. Create runner
runner = Runner(
    agent=agent,
    app_name="my_app",
    session_service=session_service
)

# 4. Run conversation
async for event in runner.run_async(
    user_id="user_123",
    session_id="session_abc",  # Same ID = same conversation
    new_message=query
):
    process(event)
```

### Persistent Storage Pattern

```python
from google.adk.sessions import DatabaseSessionService

# SQLite (simple, local)
session_service = DatabaseSessionService(
    db_url="sqlite:///my_data.db"
)

# PostgreSQL (production)
session_service = DatabaseSessionService(
    db_url="postgresql://user:pass@host/db"
)
```

### Context Compaction Pattern

```python
from google.adk.apps.app import App, EventsCompactionConfig

# Create App with compaction
app = App(
    name="my_app",
    root_agent=agent,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=3,  # Compact every 3 turns
        overlap_size=1          # Keep 1 turn for context
    )
)

# Use App with Runner
runner = Runner(app=app, session_service=session_service)
```

### Session State Pattern

```python
from google.adk.tools.tool_context import ToolContext

def my_tool(tool_context: ToolContext, value: str):
    # Write to state
    tool_context.state["my_key"] = value

    # Read from state
    stored = tool_context.state.get("my_key", "default")

    return {"status": "success", "value": stored}
```

## Key Concepts (2-Minute Summary)

### Session = Container for Conversation

```
Session
├── Events (conversation history)
│   ├── User message
│   ├── Agent response
│   ├── Tool call
│   └── Tool result
└── State (structured data)
    ├── user:name = "Sam"
    └── user:country = "Poland"
```

### InMemory vs Database

| Feature | InMemory | Database |
|---------|----------|----------|
| **Speed** | Fastest | Fast |
| **Persistence** | ❌ Lost on restart | ✅ Permanent |
| **Use Case** | Testing | Production |
| **Setup** | None | DB required |

### Context Compaction

**Problem:** Long conversations = High costs
```
Turn 1:   500 tokens
Turn 5: 2,500 tokens  ❌ Expensive!
```

**Solution:** Automatic summarization
```
Turn 1:   500 tokens
Turn 5:   800 tokens  ✅ 68% savings!
```

### Session State

**Events** = Full conversation (for LLM context)
**State** = Structured data (for tool coordination)

```python
# Events: Conversation flow
"Hi, I'm Sam!" → "Nice to meet you!"

# State: Facts extracted
{"user:name": "Sam"}
```

## Next Steps

1. **Explore Examples**: Read through all 4 example files
2. **Modify & Experiment**: Change compaction intervals, add custom tools
3. **Read Full Documentation**: Check `README.md` for deep dives
4. **Build Your Own**: Apply patterns to your use case

## Project Structure

```
day-3a/
├── examples/
│   ├── 1_stateful_agent.py          # InMemorySessionService
│   ├── 2_persistent_sessions.py     # DatabaseSessionService
│   ├── 3_context_compaction.py      # EventsCompactionConfig
│   └── 4_session_state.py           # Custom tools
├── utils/
│   ├── __init__.py
│   └── session_helpers.py           # Helper functions
├── session_management_demo.py       # Interactive demo
├── requirements.txt                 # Dependencies
├── .env.example                     # API key template
├── README.md                        # Full documentation
└── QUICKSTART.md                    # This file
```

## Resources

- **Full Documentation**: `README.md`
- **Google ADK Docs**: https://ai.google.dev/adk
- **Sessions Guide**: https://ai.google.dev/adk/sessions
- **Get API Key**: https://aistudio.google.com/app/apikey

## Need Help?

1. **Check README.md**: Comprehensive troubleshooting section
2. **Test Components**: Run examples independently
3. **Verify Setup**: Check `.env` file and dependencies
4. **Community**: Google ADK Discord for support

---

**You're all set!** 🎉 Run `python session_management_demo.py` to start exploring session management!
