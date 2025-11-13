# Quick Start Guide - Agent Memory

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
cd day-3/day-3b

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
python memory_management_demo.py
```

### Demo Options

1. **Manual Memory Storage** - add_session_to_memory()
2. **Reactive Memory** - load_memory tool
3. **Proactive Memory** - preload_memory tool
4. **Automated Memory** - Callbacks
5. **Run All** - Full tour

## What Each Example Does

### 1. Manual Memory Storage (`examples/example_1_manual_memory.py`)

**What it demonstrates:**
- Initialize MemoryService alongside SessionService
- Transfer session data to memory manually
- Verify memory contents

**What you'll see:**
```
DEMO 1: Store favorite color in session
User > My favorite color is blue-green.
Agent > [Writes haiku about blue-green]

DEMO 2: Manually save to memory
✅ Session data transferred to memory storage

DEMO 3: Verify memory contents
💾 Memory contains 2 events
```

**Key takeaway:** `add_session_to_memory()` transfers sessions to long-term storage

---

### 2. Reactive Memory Retrieval (`examples/example_2_reactive_memory.py`)

**What it demonstrates:**
- Agent with load_memory tool
- Agent decides when to search memory
- Memory retrieval across sessions

**What you'll see:**
```
DEMO 1: Pre-populate memory
✅ Stored: favorite color, hobby

DEMO 2: Agent with load_memory tool
✅ Agent can search when needed

DEMO 3: Ask about favorite color
User > What is my favorite color?
Agent calls load_memory → Finds "purple" ✅

DEMO 4: Math question
User > What is 2+2?
Agent answers directly (no memory search)
```

**Key takeaway:** Reactive = Agent chooses when to search (efficient)

---

### 3. Proactive Memory Retrieval (`examples/example_3_proactive_memory.py`)

**What it demonstrates:**
- Agent with preload_memory tool
- Automatic memory loading before every turn
- Guaranteed memory context

**What you'll see:**
```
DEMO 1: Pre-populate memory
✅ Stored: name, location, job

DEMO 2: Agent with preload_memory
✅ Memory auto-loads every turn

DEMO 3: Test questions
User > What is my name?
Memory auto-loaded → Agent: "Alex" ✅

User > Where do I live?
Memory auto-loaded → Agent: "Portland, Oregon" ✅

DEMO 4: Math question
User > What is 5 x 7?
Memory auto-loaded (even though not needed)
```

**Key takeaway:** Proactive = Always loads memory (guaranteed context)

---

### 4. Automated Memory with Callbacks (`examples/example_4_automated_memory.py`)

**What it demonstrates:**
- after_agent_callback for automatic storage
- Combining automated storage + retrieval
- Zero-intervention memory management

**What you'll see:**
```
DEMO 1: Create agent with automation
✅ preload_memory (auto retrieval)
✅ after_agent_callback (auto storage)

DEMO 2: First conversation
User > I gifted a toy car to my nephew!
Agent > Great! [responds]
→ Automatically saved to memory ✨

DEMO 3: Second conversation (NEW session)
User > What did I gift my nephew?
→ Memory auto-loaded ✨
Agent > A toy car ✅
→ This conversation also saved ✨

DEMO 4: Comprehensive test
All information recalled across multiple sessions!
```

**Key takeaway:** Callbacks + preload_memory = Complete automation

---

## Quick Test Commands

```bash
# Run individual examples
python examples/example_1_manual_memory.py
python examples/example_2_reactive_memory.py
python examples/example_3_proactive_memory.py
python examples/example_4_automated_memory.py

# Run interactive demo
python memory_management_demo.py
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

### "Agent doesn't retrieve memory"

**Problem:** Missing memory tools or incorrect pattern

**Fix:**
```python
# Reactive: Agent decides
agent = LlmAgent(
    tools=[load_memory],
    instruction="Use load_memory when you need past context"
)

# Proactive: Always loads
agent = LlmAgent(
    tools=[preload_memory]
)
```

## Understanding the Code

### Basic Memory Pattern

```python
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner

# 1. Create memory service
memory_service = InMemoryMemoryService()

# 2. Create runner with BOTH services
runner = Runner(
    agent=agent,
    app_name="my_app",
    session_service=session_service,
    memory_service=memory_service,  # Add memory!
)

# 3. Have conversation (stored in session)
await runner.run_async(...)

# 4. Transfer to memory
session = await session_service.get_session(...)
await memory_service.add_session_to_memory(session)
```

### Reactive Pattern (load_memory)

```python
from google.adk.tools import load_memory

agent = LlmAgent(
    tools=[load_memory],  # Agent chooses when to search
    instruction="Use load_memory if you need past context"
)

# Agent decides: "Do I need memory?" → Searches if yes
```

### Proactive Pattern (preload_memory)

```python
from google.adk.tools import preload_memory

agent = LlmAgent(
    tools=[preload_memory],  # Always loads memory
    instruction="Answer using available information"
)

# Memory automatically loaded before every turn
```

### Automated Pattern (Callbacks)

```python
# Define callback
async def auto_save_to_memory(callback_context):
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )

# Create agent with callback
agent = LlmAgent(
    tools=[preload_memory],  # Auto-retrieval
    after_agent_callback=auto_save_to_memory,  # Auto-storage!
)

# Result: Zero manual memory management!
```

## Key Concepts (2-Minute Summary)

### Session vs Memory

```
Session = Short-term memory (single conversation)
Memory  = Long-term knowledge (all conversations)

Think:
Session = "What did you say 10 minutes ago?"
Memory  = "What are your preferences from last week?"
```

### Three-Step Workflow

```
1. Initialize → Create MemoryService
2. Ingest     → add_session_to_memory()
3. Retrieve   → load_memory or preload_memory
```

### Reactive vs Proactive

| Aspect | load_memory | preload_memory |
|--------|-------------|----------------|
| **When** | Agent decides | Every turn |
| **Efficiency** | High | Lower |
| **Reliability** | Might forget | Guaranteed |
| **Use Case** | Smart agents | Critical memory |

### Memory Consolidation

**Problem:** Raw sessions = verbose, redundant data

**Solution:** LLM extracts key facts

```
Before: "My favorite color is blue. No, blue-green!" (2 messages)
After:  "User's favorite color: blue-green" (1 fact)
```

**Implementation:**
- InMemoryMemoryService: No consolidation
- VertexAiMemoryBankService: Automatic (Day 5)

### Automation Benefits

```
Manual:
✓ Have conversation
✓ Save to memory (manual)
✓ Add retrieval tools (manual)

Automated:
✓ Have conversation
✅ Auto-saved (callback)
✅ Auto-retrieved (preload_memory)
```

## Next Steps

1. **Explore Examples**: Read through all 4 example files
2. **Modify & Experiment**: Change patterns, add custom logic
3. **Read Full Documentation**: Check `README.md` for deep dives
4. **Build Your Own**: Apply patterns to your use case

## Project Structure

```
day-3b/
├── examples/
│   ├── example_1_manual_memory.py          # Manual storage
│   ├── example_2_reactive_memory.py        # load_memory
│   ├── example_3_proactive_memory.py       # preload_memory
│   └── example_4_automated_memory.py       # Callbacks
├── utils/
│   ├── __init__.py
│   └── memory_helpers.py                   # Helper functions
├── memory_management_demo.py               # Interactive demo
├── requirements.txt                        # Dependencies
├── .env.example                            # API key template
├── README.md                               # Full documentation
└── QUICKSTART.md                           # This file
```

## Resources

- **Full Documentation**: `README.md`
- **Google ADK Docs**: https://ai.google.dev/adk
- **Memory Guide**: https://ai.google.dev/adk/memory
- **Get API Key**: https://aistudio.google.com/app/apikey

## Need Help?

1. **Check README.md**: Comprehensive troubleshooting section
2. **Test Components**: Run examples independently
3. **Verify Setup**: Check `.env` file and dependencies
4. **Community**: Google ADK Discord for support

---

**You're all set!** 🎉 Run `python memory_management_demo.py` to start exploring memory management!
