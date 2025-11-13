# Agent Memory - Memory Management Part 2 🧠

**Based on Kaggle's 5-Day AI Agents Intensive Course - Day 3b**

Master long-term memory management for AI agents with persistent knowledge storage, intelligent retrieval patterns, and automated memory workflows.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [Pattern 1: Manual Memory Storage](#pattern-1-manual-memory-storage)
- [Pattern 2: Reactive Memory Retrieval](#pattern-2-reactive-memory-retrieval)
- [Pattern 3: Proactive Memory Retrieval](#pattern-3-proactive-memory-retrieval)
- [Pattern 4: Automated Memory with Callbacks](#pattern-4-automated-memory-with-callbacks)
- [Architecture](#architecture)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

## Overview

In Day 3a, you learned about **Sessions** - short-term memory for single conversations. Now you'll add **Memory** - a searchable, long-term knowledge store that persists across multiple conversations.

### The Distinction

| Aspect | Session (Day 3a) | Memory (Day 3b) |
|--------|------------------|-----------------|
| **Scope** | Single conversation | All conversations |
| **Duration** | Temporary (one chat) | Persistent (lifetime) |
| **Purpose** | Conversation context | Knowledge base |
| **Analogy** | Application state | Database |

Think of it this way:
- **Session**: "What did you say 10 minutes ago in THIS conversation?"
- **Memory**: "What preferences have you mentioned across ALL conversations?"

### What You'll Learn

✅ Initialize MemoryService and integrate with agents
✅ Transfer session data to long-term storage
✅ Retrieve memories with reactive and proactive patterns
✅ Automate memory management with callbacks
✅ Understand memory consolidation (conceptual)

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
cd day-3/day-3b

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 4. Run interactive demo
python memory_management_demo.py
```

### Getting Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy to `.env`:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

## Core Concepts

### Sessions vs Memory

```python
# Without Memory - Conversation 1
>>> "My favorite color is blue"
Agent: "Got it!"

# Conversation 2 (different session)
>>> "What's my favorite color?"
Agent: "I don't know"  # ❌ Forgot! (Sessions don't share data)
```

```python
# With Memory - Conversation 1
>>> "My favorite color is blue"
Agent: "Got it!"
→ Saved to memory ✅

# Conversation 2 (different session)
>>> "What's my favorite color?"
Agent: "Your favorite color is blue"  # ✅ Remembers! (Memory persists)
```

### Three-Step Memory Workflow

```
1. Initialize → Create MemoryService + provide to Runner
2. Ingest     → Transfer sessions to memory (add_session_to_memory)
3. Retrieve   → Search memories (search_memory, load_memory, preload_memory)
```

### Memory Architecture

```
┌────────────────────────────────────────────────────────┐
│                    Application                          │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Runner                               │  │
│  │  Orchestrates agent + services                    │  │
│  └───────┬──────────────────────────┬────────────────┘  │
│          │                          │                    │
│          ▼                          ▼                    │
│  ┌───────────────┐        ┌───────────────────────┐    │
│  │ SessionService│        │   MemoryService       │    │
│  │  (short-term) │        │   (long-term)         │    │
│  └───────┬───────┘        └──────────┬────────────┘    │
│          │                           │                   │
│          ▼                           ▼                   │
│    Conversation                  Knowledge               │
│    Events                        Base                    │
│    (temporary)                   (persistent)            │
└────────────────────────────────────────────────────────┘
```

## Pattern 1: Manual Memory Storage

### InMemoryMemoryService

The simplest memory service for learning and development.

**Implementation:**
- Stores raw conversation events
- Keyword-based search
- In-memory storage (resets on restart)
- Perfect for prototyping

**Limitations:**
- No consolidation (stores everything)
- Simple keyword matching
- Not persistent

See `examples/example_1_manual_memory.py` for complete example.

### Basic Usage

```python
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner

# Create memory service
memory_service = InMemoryMemoryService()

# Add to runner (alongside session service)
runner = Runner(
    agent=agent,
    app_name="MyApp",
    session_service=session_service,
    memory_service=memory_service,  # Memory now available!
)

# Have a conversation (stored in session)
await runner.run_async(
    user_id="user_123",
    session_id="session_1",
    new_message=types.Content(...)
)

# Transfer session to memory
session = await session_service.get_session(
    app_name="MyApp",
    user_id="user_123",
    session_id="session_1"
)

# Key method: Manual save to memory
await memory_service.add_session_to_memory(session)
```

### When to Use Manual Storage

✅ Learning and experimentation
✅ Fine-grained control over what gets saved
✅ Selective memory storage (filter sensitive data)
❌ Production systems (use automated callbacks instead)

## Pattern 2: Reactive Memory Retrieval

### load_memory Tool

Agent **decides when** to search memory.

**How it works:**
1. User asks a question
2. Agent evaluates: "Do I need past context?"
3. If yes → Agent calls `load_memory` tool
4. Memory service returns relevant memories
5. Agent uses memories to answer

**Advantages:**
- More efficient (only searches when needed)
- Saves tokens and latency
- Agent controls memory access

**Disadvantages:**
- Agent might forget to search
- Requires smart agent reasoning

See `examples/example_2_reactive_memory.py` for complete example.

### Implementation

```python
from google.adk.tools import load_memory

# Create agent with load_memory tool
agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite"),
    name="ReactiveAgent",
    instruction="Answer questions. Use load_memory if you need past context.",
    tools=[load_memory],  # Agent chooses when to use!
)

# Create runner
runner = Runner(
    agent=agent,
    app_name="MyApp",
    session_service=session_service,
    memory_service=memory_service,
)

# Test: Memory-required question
>>> "What is my favorite color?"
# Agent calls load_memory → retrieves "blue" → answers correctly

# Test: No memory needed
>>> "What is 2+2?"
# Agent answers directly without searching memory
```

### When to Use Reactive

✅ Smart agents with good reasoning
✅ Token efficiency is priority
✅ Mixed queries (some need memory, some don't)
❌ Critical applications where forgetting is unacceptable

## Pattern 3: Proactive Memory Retrieval

### preload_memory Tool

Memory **automatically loaded** before every turn.

**How it works:**
1. Before agent processes query
2. `preload_memory` automatically searches memory
3. Memories loaded into system instructions
4. Agent always has full context
5. No risk of forgetting

**Advantages:**
- Guaranteed memory access
- No forgetting
- Simpler agent instructions

**Disadvantages:**
- Less efficient (searches every turn)
- Higher token usage
- Searches even when not needed

See `examples/example_3_proactive_memory.py` for complete example.

### Implementation

```python
from google.adk.tools import preload_memory

# Create agent with preload_memory
agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite"),
    name="ProactiveAgent",
    instruction="Answer questions using available information.",
    tools=[preload_memory],  # Automatic loading!
)

# Create runner
runner = Runner(
    agent=agent,
    app_name="MyApp",
    session_service=session_service,
    memory_service=memory_service,
)

# Every query automatically loads memory first
>>> "What is my name?"
# Memory auto-loaded → answer from context ✅

>>> "What is 5+5?"
# Memory auto-loaded (even though not needed)
```

### When to Use Proactive

✅ Critical memory access required
✅ Simple agents (less reasoning needed)
✅ User profile/preferences always needed
❌ High-volume applications (token costs)

### Comparison Table

| Aspect | load_memory (Reactive) | preload_memory (Proactive) |
|--------|------------------------|----------------------------|
| **Trigger** | Agent decides | Every turn (automatic) |
| **Efficiency** | High (selective search) | Lower (always searches) |
| **Reliability** | Depends on agent | Guaranteed |
| **Token Usage** | Minimal | Higher |
| **Use Case** | Smart agents | Critical memory |

## Pattern 4: Automated Memory with Callbacks

### The Automation Problem

Manual memory storage has issues:
- Forgetting to call `add_session_to_memory()`
- Inconsistent saving across conversations
- Not scalable for production

**Solution: Callbacks**

### What are Callbacks?

Callbacks are functions that ADK **automatically calls** at specific execution stages.

Think of them as checkpoints in your agent's lifecycle:

```
User message
    ↓
before_agent_callback ⚡
    ↓
Agent processing
    ↓
after_agent_callback ⚡  ← We use this!
    ↓
Response
```

Available callback types:
- `before_agent_callback` → Before agent starts
- `after_agent_callback` → After agent completes turn
- `before_tool_callback` / `after_tool_callback` → Around tools
- `before_model_callback` / `after_model_callback` → Around LLM calls

See `examples/example_4_automated_memory.py` for complete example.

### Implementation

```python
# Step 1: Define callback function
async def auto_save_to_memory(callback_context):
    """Automatically save session after each agent turn."""
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )

# Step 2: Create agent with callback + preload_memory
agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite"),
    name="AutomatedAgent",
    instruction="Answer questions and remember conversations.",
    tools=[preload_memory],  # Automatic retrieval
    after_agent_callback=auto_save_to_memory,  # Automatic storage!
)

# Step 3: Create runner
runner = Runner(
    agent=agent,
    app_name="MyApp",
    session_service=session_service,
    memory_service=memory_service,
)

# Result: Zero-intervention memory management!
>>> "I love pizza"
Agent: "Great to know!"
→ Automatically saved to memory ✅

>>> "What food do I love?"  # Different session
→ Memory automatically loaded ✅
Agent: "You love pizza!"
→ This conversation also saved ✅
```

### Complete Automation

Combining `preload_memory` + `after_agent_callback`:

```
Automatic Storage ✅
    ↓
Automatic Retrieval ✅
    ↓
Zero Manual Work 🎉
```

### When to Save to Memory

| Timing | Implementation | Best For |
|--------|---------------|----------|
| After every turn | `after_agent_callback` | Real-time updates |
| End of conversation | Manual call on session end | Batch processing |
| Periodic intervals | Timer-based job | Long conversations |

## Architecture

### MemoryService Options

| Feature | InMemoryMemoryService | VertexAiMemoryBankService |
|---------|----------------------|---------------------------|
| **Storage** | In-memory (temporary) | Cloud (persistent) |
| **Search** | Keyword matching | Semantic (meaning-based) |
| **Consolidation** | None (raw storage) | LLM-powered extraction |
| **Production Ready** | ❌ No | ✅ Yes |
| **Use Case** | Learning, testing | Production apps |

### Memory Consolidation (Conceptual)

**The Problem:**
Raw session storage includes:
- Every user message
- Every agent response
- Every tool call
- All conversational noise

**Example:**
```
User: "My favorite color is blue. Actually, maybe blue-green. Yes, blue-green."
Agent: "Noted!"
User: "Thanks!"
Agent: "You're welcome!"

→ Stores 4 messages (redundant, verbose)
```

**The Solution: Consolidation**
LLM extracts key facts:

```
Extracted Memory: "User's favorite color: blue-green"

→ Stores 1 concise fact
```

**Benefits:**
- Less storage
- Faster retrieval
- More accurate answers
- Reduced token usage

**How it Works (Managed Services):**

```
1. Raw Session Events
   ↓
2. LLM analyzes conversation
   ↓
3. Extracts key facts
   ↓
4. Stores concise memories
   ↓
5. Merges with existing (deduplication)
```

**Implementation Note:**
- `InMemoryMemoryService`: No consolidation
- `VertexAiMemoryBankService`: Automatic consolidation (Day 5)

## Best Practices

### Memory Storage

**✅ DO:**
- Use automated callbacks in production
- Save conversations after completion
- Filter sensitive data before storage
- Implement periodic cleanup for old memories

**❌ DON'T:**
- Store passwords or API keys
- Forget error handling in callbacks
- Save every single message manually
- Mix sessions and memories (keep separate)

### Memory Retrieval

**✅ DO:**
- Use `load_memory` for smart agents
- Use `preload_memory` for critical contexts
- Test both patterns for your use case
- Monitor token usage

**❌ DON'T:**
- Rely on agent memory without tools
- Assume memories always exist
- Forget to handle empty search results
- Mix retrieval patterns randomly

### Production Considerations

**✅ DO:**
- Use managed memory services (Vertex AI)
- Implement monitoring and logging
- Test memory accuracy regularly
- Plan for memory cleanup/archival

**❌ DON'T:**
- Use InMemoryMemoryService in production
- Store unlimited memories without limits
- Ignore memory search performance
- Skip security reviews for stored data

## Troubleshooting

### Issue: "Memory not found"

**Cause:** Memory wasn't saved or query doesn't match

**Solution:**
```python
# 1. Verify memory was saved
await memory_service.add_session_to_memory(session)

# 2. Check memory contents
search_response = await memory_service.search_memory(
    app_name="MyApp",
    user_id="user_123",
    query=""  # Empty query returns all memories
)
print(f"Total memories: {len(search_response.memories)}")

# 3. Test search query
search_response = await memory_service.search_memory(
    app_name="MyApp",
    user_id="user_123",
    query="favorite color"
)
```

### Issue: "Agent doesn't use load_memory tool"

**Cause:** Agent doesn't understand when to search

**Solution:**
```python
# Improve agent instructions
agent = LlmAgent(
    instruction="""
    Answer user questions.

    IMPORTANT: Use the load_memory tool when:
    - User asks about their preferences
    - User asks "what did I say"
    - User references past conversations
    """,
    tools=[load_memory],
)

# Or use preload_memory instead
agent = LlmAgent(
    instruction="Answer using available context.",
    tools=[preload_memory],  # Automatic, no decision needed
)
```

### Issue: "Callback not executing"

**Cause:** Callback errors silently fail

**Solution:**
```python
# Add error handling to callback
async def auto_save_to_memory(callback_context):
    try:
        await callback_context._invocation_context.memory_service.add_session_to_memory(
            callback_context._invocation_context.session
        )
    except Exception as e:
        print(f"Memory save error: {e}")
        # Log to monitoring system
```

### Issue: "Search returns no results"

**Cause:** Keyword mismatch with InMemoryMemoryService

**Solution:**
```python
# InMemoryMemoryService uses exact keyword matching
# Stored: "My favorite color is blue"

# ✅ Works
search_memory(query="favorite color")  # Keywords match!

# ❌ Fails
search_memory(query="preferred hue")  # Keywords don't match

# Solution: Use semantic search (Vertex AI Memory Bank)
# Or store with multiple phrasings
```

## Resources

### Official Documentation

- **Google ADK**: https://ai.google.dev/adk
- **Memory Guide**: https://ai.google.dev/adk/memory
- **Callbacks**: https://ai.google.dev/adk/callbacks
- **Vertex AI Memory Bank**: https://cloud.google.com/vertex-ai/docs/memory-bank

### Course Materials

- **Kaggle Course**: [5-Day AI Agents Intensive](https://www.kaggle.com/learn-guide/5-day-genai)
- **Day 3a**: Sessions (prerequisite for this module)
- **Day 3b Notebook**: Memory Management Part 2

### Community

- **Google ADK Discord**: Join for community support
- **GitHub Issues**: Report bugs or request features
- **Stack Overflow**: Tag `google-adk` for questions

---

## Next Steps

### Continue Learning

**Day 4**: Observability and Evaluation
- Monitor agent performance
- Implement logging and tracing
- Evaluate agent quality
- Debug production issues

### Build Your Own

Apply what you've learned:
- Personal assistant with long-term memory
- Customer support with user profiles
- Research agent with knowledge accumulation
- Multi-user chatbot with isolated memories

### Experiment

Try these modifications:
1. Combine both memory tools (load + preload)
2. Create conditional callbacks (save only important conversations)
3. Implement memory search UI
4. Build memory analytics dashboard

---

**Happy Agent Building!** 🤖

Built with ❤️ using [Google ADK](https://ai.google.dev/adk) and [Gemini](https://ai.google.dev/gemini-api)
