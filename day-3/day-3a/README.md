# Agent Sessions - Memory Management Part 1 🧠

**Based on Kaggle's 5-Day AI Agents Intensive Course - Day 3a**

Master the art of building stateful AI agents that remember conversations, persist data, and manage context efficiently.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [Pattern 1: Stateful Agents](#pattern-1-stateful-agents)
- [Pattern 2: Persistent Sessions](#pattern-2-persistent-sessions)
- [Pattern 3: Context Compaction](#pattern-3-context-compaction)
- [Pattern 4: Session State](#pattern-4-session-state)
- [Architecture](#architecture)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

## Overview

Large Language Models are inherently **stateless** - they only process the information you provide in a single API call. This creates a fundamental problem: how do you have meaningful, contextual conversations?

**Solution: Sessions**

Sessions provide short-term memory management for AI agents, enabling them to:
- Remember conversation history
- Maintain context across multiple turns
- Store structured data for workflow management
- Optimize long conversations with automatic summarization

### What You'll Learn

✅ Build stateful agents that remember conversations
✅ Persist sessions across application restarts
✅ Optimize long conversations with context compaction
✅ Manage structured data with session state
✅ Choose the right session service for your needs

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
cd day-3/day-3a

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 4. Run interactive demo
python session_management_demo.py
```

### Getting Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy to `.env`:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

## Core Concepts

### The Statelessness Problem

```python
# Without sessions - Agent forgets everything
>>> "Hi, I'm Sam!"
Agent: "Nice to meet you!"
>>> "What's my name?"
Agent: "I don't know your name"  # ❌ Forgot!
```

```python
# With sessions - Agent remembers
>>> "Hi, I'm Sam!"
Agent: "Nice to meet you, Sam!"
>>> "What's my name?"
Agent: "Your name is Sam"  # ✅ Remembers!
```

### Session Anatomy

A **Session** consists of two key components:

#### 1. **Session Events** (`session.events`)
The chronological conversation history:

```
Events = [
    UserMessage("Hi, I'm Sam!"),
    AgentResponse("Nice to meet you, Sam!"),
    ToolCall("save_name", {"name": "Sam"}),
    ToolResponse({"status": "saved"}),
    UserMessage("What's my name?"),
    AgentResponse("Your name is Sam")
]
```

#### 2. **Session State** (`session.state`)
Structured key-value data:

```python
state = {
    "user:name": "Sam",
    "user:country": "Poland",
    "workflow:step": 3,
    "temp:calculation": 42
}
```

### Session Architecture

```
┌────────────────────────────────────────────────────┐
│                    Application                      │
│                                                      │
│  ┌────────────────────────────────────────────┐   │
│  │              Runner                         │   │
│  │  (Orchestrates conversation flow)           │   │
│  └──────────────┬─────────────────────────────┘   │
│                 │                                   │
│                 ▼                                   │
│  ┌────────────────────────────────────────────┐   │
│  │          SessionService                     │   │
│  │  - InMemorySessionService (temporary)       │   │
│  │  - DatabaseSessionService (persistent)      │   │
│  │  - Agent Engine Sessions (cloud)            │   │
│  └──────────────┬─────────────────────────────┘   │
│                 │                                   │
│                 ▼                                   │
│       ┌─────────────────────┐                      │
│       │      Session        │                      │
│       │  ┌──────────────┐  │                      │
│       │  │   Events     │  │  Conversation        │
│       │  │  (history)   │  │  history             │
│       │  └──────────────┘  │                      │
│       │  ┌──────────────┐  │                      │
│       │  │    State     │  │  Structured          │
│       │  │  (key-value) │  │  data                │
│       │  └──────────────┘  │                      │
│       └─────────────────────┘                      │
└────────────────────────────────────────────────────┘
```

## Pattern 1: Stateful Agents

### InMemorySessionService

The simplest session service - stores conversations in RAM (temporary).

**Perfect for:**
- Development and testing
- Quick prototypes
- Demos and tutorials

**Limitations:**
- Lost on application restart
- Not suitable for production
- No persistence

### Implementation

See `examples/1_stateful_agent.py` for complete example.

```python
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

# Create agent
agent = Agent(
    model=Gemini(model="gemini-2.5-flash-lite"),
    name="chatbot",
    description="A stateful chatbot"
)

# Set up temporary session storage
session_service = InMemorySessionService()

# Create runner
runner = Runner(
    agent=agent,
    app_name="my_app",
    session_service=session_service
)

# Have a conversation
async for event in runner.run_async(
    user_id="user_123",
    session_id="session_abc",
    new_message=types.Content(
        role="user",
        parts=[types.Part(text="Hi, I'm Sam!")]
    )
):
    # Process events
    pass
```

### Key Insights

✅ **Same session_id** = Agent remembers conversation
✅ **Different session_id** = Fresh start, no memory
✅ **Automatic history** = Runner maintains context
⚠️ **Temporary storage** = Lost on restart

## Pattern 2: Persistent Sessions

### DatabaseSessionService

Upgrades to persistent storage using a database (SQLite, PostgreSQL, etc.).

**Perfect for:**
- Production applications
- Long-running conversations
- Multi-user systems
- Applications requiring data persistence

**Benefits:**
- Survives application restarts
- Supports multiple users
- Scalable storage
- Production-ready

### Implementation

See `examples/2_persistent_sessions.py` for complete example.

```python
from google.adk.sessions import DatabaseSessionService

# SQLite (simple, local file)
db_url = "sqlite:///my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

# PostgreSQL (production)
# db_url = "postgresql://user:pass@localhost/dbname"
# session_service = DatabaseSessionService(db_url=db_url)

# Use with Runner
runner = Runner(
    agent=agent,
    app_name="my_app",
    session_service=session_service
)
```

### Database Schema

The DatabaseSessionService automatically creates tables:

```sql
CREATE TABLE sessions (
    app_name TEXT,
    user_id TEXT,
    session_id TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    state JSON,
    PRIMARY KEY (app_name, user_id, session_id)
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    app_name TEXT,
    session_id TEXT,
    author TEXT,
    content JSON,
    timestamp TIMESTAMP
);
```

### Session Isolation

Sessions are isolated by three keys:

1. **app_name** - Different applications
2. **user_id** - Different users
3. **session_id** - Different conversations

```python
# User A, Session 1
runner.run_async(
    user_id="user_a",
    session_id="session_1",
    ...
)

# User A, Session 2 (isolated from Session 1)
runner.run_async(
    user_id="user_a",
    session_id="session_2",
    ...
)

# User B, Session 1 (isolated from User A)
runner.run_async(
    user_id="user_b",
    session_id="session_1",
    ...
)
```

## Pattern 3: Context Compaction

### The Long Conversation Problem

As conversations grow, token usage explodes:

```
Turn 1:   500 tokens
Turn 2: 1,000 tokens (includes Turn 1)
Turn 3: 1,500 tokens (includes Turn 1 + 2)
Turn 4: 2,000 tokens (includes Turn 1 + 2 + 3)
...
Turn 10: 5,000 tokens ❌ Expensive!
```

### EventsCompactionConfig

Automatic history summarization to reduce token usage.

**How it works:**
1. Agent has a normal conversation
2. After N turns, old history is automatically summarized
3. Summary replaces detailed history
4. Recent turns are kept for context

See `examples/3_context_compaction.py` for complete example.

```python
from google.adk.apps.app import App, EventsCompactionConfig

# Create App with compaction
app = App(
    name="my_app",
    root_agent=agent,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=3,  # Compact every 3 turns
        overlap_size=1,         # Keep 1 turn for context
    ),
)

# Use with Runner
runner = Runner(
    app=app,  # Pass App, not Agent
    session_service=session_service
)
```

### Compaction Example

**Before Compaction:**
```
Turn 1: "What's the capital of France?" → "Paris"
Turn 2: "What about Germany?" → "Berlin"
Turn 3: "And Italy?" → "Rome"
Turn 4: "Tell me about the first one" → ...
```

**After Compaction (at Turn 4):**
```
[Summary]: User asked about capitals of France (Paris), Germany (Berlin)
Turn 3: "And Italy?" → "Rome"  [kept for overlap]
Turn 4: "Tell me about the first one" → "Paris is the capital of France..."
```

### Token Savings

```
Without Compaction (Turn 10): ~5,000 tokens
With Compaction (Turn 10):    ~1,500 tokens
Savings: 70% ✅
```

## Pattern 4: Session State

### Session State vs Events

| Aspect | Events | State |
|--------|--------|-------|
| **Content** | Full conversation history | Structured key-value data |
| **Purpose** | LLM context | Data sharing between tools |
| **Format** | Messages, tool calls | Dictionary |
| **Size** | Large (grows over time) | Small (fixed keys) |
| **Use For** | Conversation context | User preferences, workflow data |

### Custom Tools for State Management

See `examples/4_session_state.py` for complete example.

```python
from google.adk.tools.tool_context import ToolContext

def save_userinfo(
    tool_context: ToolContext,
    user_name: str,
    country: str
) -> dict:
    """Save user information to session state."""
    # Write to state
    tool_context.state["user:name"] = user_name
    tool_context.state["user:country"] = country

    return {"status": "success"}


def retrieve_userinfo(tool_context: ToolContext) -> dict:
    """Retrieve user information from session state."""
    # Read from state
    user_name = tool_context.state.get("user:name", "Unknown")
    country = tool_context.state.get("user:country", "Unknown")

    return {
        "status": "success",
        "user_name": user_name,
        "country": country
    }
```

### State Key Naming Conventions

Use descriptive prefixes for organization:

```python
# User-specific data
tool_context.state["user:name"] = "Sam"
tool_context.state["user:preferences"] = {...}

# Application-level data
tool_context.state["app:config"] = {...}
tool_context.state["app:version"] = "1.0"

# Temporary workflow data
tool_context.state["temp:calculation"] = 42
tool_context.state["temp:step"] = 3
```

## Architecture

### SessionService Comparison

| Feature | InMemory | Database | Agent Engine |
|---------|----------|----------|--------------|
| **Persistence** | ❌ Temporary | ✅ Permanent | ✅ Permanent |
| **Scalability** | Low | Medium | High |
| **Setup** | None | Database required | GCP required |
| **Cost** | Free | DB costs | GCP costs |
| **Best For** | Testing | Self-hosted | Enterprise |

### Choosing the Right Service

```
Development/Testing
    │
    └─> InMemorySessionService

Small to Medium Apps (Self-hosted)
    │
    └─> DatabaseSessionService (SQLite/PostgreSQL)

Enterprise/Production (GCP)
    │
    └─> Agent Engine Sessions
```

## Best Practices

### Session Management

**✅ DO:**
- Use meaningful session IDs (e.g., `user_123_chat_2025_01`)
- Implement session cleanup for old conversations
- Set appropriate compaction intervals
- Use DatabaseSessionService for production

**❌ DON'T:**
- Share session_id between different users
- Store sensitive data in plain text
- Keep infinite session history without compaction
- Use InMemorySessionService in production

### State Management

**✅ DO:**
- Use descriptive key prefixes (`user:`, `app:`, `temp:`)
- Store only essential structured data
- Document what data your tools store
- Clean up temporary data when done

**❌ DON'T:**
- Store full conversation history in state
- Use state for data that belongs in events
- Create overly complex state structures
- Store unserializable objects

### Context Compaction

**✅ DO:**
- Set `compaction_interval` based on conversation length
- Keep `overlap_size` of 1-2 for context
- Test compaction with your specific use case
- Monitor token usage before/after

**❌ DON'T:**
- Set interval too low (loses context)
- Set interval too high (no savings)
- Forget to test that agent still works after compaction

## Troubleshooting

### Issue: "Session not found"

**Cause:** Session hasn't been created yet

**Solution:**
```python
# Always create session before use
session = await session_service.create_session(
    app_name="my_app",
    user_id="user_123",
    session_id="session_abc"
)
```

### Issue: "Agent forgets conversation"

**Causes:**
1. Using different session_id
2. Using InMemorySessionService and restarted app
3. Database connection lost

**Solutions:**
```python
# 1. Verify same session_id
print(f"Using session: {session_id}")

# 2. Use DatabaseSessionService for persistence
session_service = DatabaseSessionService(db_url="sqlite:///data.db")

# 3. Check database connection
try:
    session = await session_service.get_session(...)
except Exception as e:
    print(f"Database error: {e}")
```

### Issue: "Compaction not triggering"

**Cause:** Not enough conversation turns

**Solution:**
```python
# Verify compaction_interval
events_compaction_config=EventsCompactionConfig(
    compaction_interval=3,  # Triggers after 3 turns
    overlap_size=1
)

# Check if you've had enough turns
# Compaction triggers AFTER the Nth turn
```

### Issue: "State not persisting"

**Causes:**
1. Not using DatabaseSessionService
2. State not being written correctly

**Solutions:**
```python
# 1. Use persistent storage
session_service = DatabaseSessionService(db_url="sqlite:///data.db")

# 2. Verify state writes in tools
def my_tool(tool_context: ToolContext):
    tool_context.state["key"] = "value"
    # Verify write
    print(f"State after write: {tool_context.state}")
```

## Resources

### Official Documentation

- **Google ADK**: https://ai.google.dev/adk
- **Sessions Guide**: https://ai.google.dev/adk/sessions
- **Context Compaction**: https://ai.google.dev/adk/compaction
- **Session State**: https://ai.google.dev/adk/session-state

### Course Materials

- **Kaggle Course**: [5-Day AI Agents Intensive](https://www.kaggle.com/learn-guide/5-day-genai)
- **Day 3a Notebook**: Memory Management Part 1 - Sessions

### Community

- **Google ADK Discord**: Join for community support
- **GitHub Issues**: Report bugs or request features
- **Stack Overflow**: Tag `google-adk` for questions

---

## Next Steps

### Continue Learning

**Day 3b** (Coming Soon): Memory Management Part 2
- Long-term memory systems
- Automatic memory extraction
- Memory-driven personalization
- Cross-session knowledge

### Build Your Own

Apply what you've learned:
- Customer support chatbot with history
- Personal assistant with preferences
- Multi-turn research agent
- Workflow automation with state

---

**Happy Agent Building!** 🤖

Built with ❤️ using [Google ADK](https://ai.google.dev/adk) and [Gemini](https://ai.google.dev/gemini-api)
