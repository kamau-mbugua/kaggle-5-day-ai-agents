# 🚀 Day 1b: Multi-Agent Systems & Workflow Patterns

Based on the **Kaggle 5-Day AI Agents Intensive Course**

This project demonstrates how to build multi-agent systems using Google's Agent Development Kit (ADK). Learn how to coordinate teams of specialized agents using four powerful workflow patterns.

## 📋 Table of Contents

- [What are Multi-Agent Systems?](#what-are-multi-agent-systems)
- [The Four Workflow Patterns](#the-four-workflow-patterns)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Pattern Details](#pattern-details)
- [Choosing the Right Pattern](#choosing-the-right-pattern)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

## 🤔 What are Multi-Agent Systems?

### The Problem: The "Do-It-All" Agent

Single agents can do a lot, but what happens when tasks get complex? A monolithic agent that tries to do everything becomes:
- Hard to build (long, confusing instructions)
- Hard to debug (which part failed?)
- Hard to maintain (changes affect everything)
- Often unreliable (too much complexity)

### The Solution: A Team of Specialists

Instead of one "do-it-all" agent, build a **multi-agent system** - a team of simple, specialized agents that collaborate:

```
Single Agent:              Multi-Agent System:
┌─────────────┐           ┌─────────┐  ┌─────────┐  ┌─────────┐
│             │           │Research │  │ Writer  │  │ Editor  │
│  Do It All  │    vs     │ Agent   │→ │ Agent   │→ │ Agent   │
│             │           │         │  │         │  │         │
└─────────────┘           └─────────┘  └─────────┘  └─────────┘
  Complex                      Simple, Specialized, Reliable
```

**Benefits:**
- ✅ Easier to build (each agent has one clear job)
- ✅ Easier to test (test each agent separately)
- ✅ Easier to debug (identify which agent failed)
- ✅ More reliable (specialized agents are more focused)
- ✅ More maintainable (change one agent without affecting others)

## 🎯 The Four Workflow Patterns

### Quick Comparison

| Pattern | When to Use | Example | Speed | Predictability |
|---------|-------------|---------|-------|----------------|
| **LLM Coordinator** | Dynamic orchestration needed | Research → Summarize | ⚡⚡ | 🎲 Flexible |
| **Sequential** | Order matters, linear pipeline | Outline → Write → Edit | ⚡ | ✅ Guaranteed |
| **Parallel** | Independent tasks, speed matters | Multi-topic research | ⚡⚡⚡ | ✅ Guaranteed |
| **Loop** | Iterative improvement needed | Writer ↔ Critic refinement | ⚡ | ✅ Guaranteed |

### Visual Overview

```
1. LLM-Based Coordinator (Dynamic)
   ┌────────────┐
   │Coordinator │ (LLM decides what to call)
   │    LLM     │
   └─────┬──────┘
         ├──→ Research Agent
         └──→ Summarizer Agent

2. Sequential Workflow (Linear Pipeline)
   Outline Agent → Writer Agent → Editor Agent

3. Parallel Workflow (Concurrent Execution)
   ┌───────────────────────┐
   │  Tech Researcher      │
   │  Health Researcher    │ → Aggregator Agent
   │  Finance Researcher   │
   └───────────────────────┘
         (run simultaneously)

4. Loop Workflow (Iterative Refinement)
   Initial Writer → ┌→ Critic Agent ──┐
                    └← Refiner Agent ←┘
                       (repeat until approved)
```

## ✅ Prerequisites

1. **Python 3.10 or higher**
   ```bash
   python --version
   ```

2. **Google Gemini API Key**
   - Get your free API key: https://aistudio.google.com/app/apikey
   - No credit card required for the free tier

3. **Google ADK installed**
   ```bash
   pip install google-adk
   ```

## 📁 Project Structure

```
day-1b/
├── README.md                        # This file
├── QUICKSTART.md                    # 5-minute quick start guide
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
│
├── multi_agent_demo.py              # Interactive demo (all patterns)
│
├── examples/                        # Individual pattern examples
│   ├── 0_llm_coordinator.py         # LLM-based orchestration
│   ├── 1_sequential_workflow.py     # Blog post pipeline
│   ├── 2_parallel_workflow.py       # Multi-topic research
│   └── 3_loop_workflow.py           # Story refinement
│
└── multi-agent-system/              # ADK CLI structure (optional)
    ├── __init__.py
    └── agent.py
```

## 🛠️ Setup Instructions

### Step 1: Install Dependencies

```bash
# Navigate to the project directory
cd /path/to/day-1b

# Install required packages
pip install -r requirements.txt
```

### Step 2: Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

Or set it as an environment variable:
```bash
export GOOGLE_API_KEY="your_actual_api_key_here"
```

### Step 3: Verify Installation

```bash
# Check if google-adk is installed
pip show google-adk

# Verify Python version
python --version
```

## 🚀 Usage

### Method 1: Interactive Demo (Recommended)

Run the unified demo to explore all patterns:

```bash
python multi_agent_demo.py
```

This will show an interactive menu:
```
🤖 MULTI-AGENT SYSTEMS & WORKFLOW PATTERNS
============================================================

Choose a workflow pattern to explore:

  0️⃣  LLM-Based Coordinator  - Dynamic orchestration
  1️⃣  Sequential Workflow     - Guaranteed order
  2️⃣  Parallel Workflow       - Concurrent execution
  3️⃣  Loop Workflow           - Iterative refinement
  4️⃣  Exit
```

### Method 2: Run Individual Examples

Each pattern has its own standalone script:

```bash
# LLM-Based Coordinator
python examples/0_llm_coordinator.py

# Sequential Workflow (Blog Creation)
python examples/1_sequential_workflow.py

# Parallel Workflow (Multi-Topic Research)
python examples/2_parallel_workflow.py

# Loop Workflow (Story Refinement)
python examples/3_loop_workflow.py
```

## 📚 Pattern Details

### Pattern 0: LLM-Based Coordinator

**Use when:** You need dynamic, flexible orchestration

**How it works:**
- A coordinator LLM manages sub-agents as tools
- The LLM decides when and how to use each agent
- Flexible but can be unpredictable

**Example:**
```python
coordinator = Agent(
    name="ResearchCoordinator",
    tools=[AgentTool(research_agent), AgentTool(summarizer_agent)],
    instruction="Orchestrate research and summarization workflow"
)
```

**Pros:**
- ✅ Flexible and adaptive
- ✅ Can handle complex decision-making

**Cons:**
- ❌ Less predictable (LLM makes decisions)
- ❌ Harder to debug

---

### Pattern 1: Sequential Workflow

**Use when:** Order matters and tasks build on each other

**How it works:**
- Agents run in a fixed, guaranteed order
- Output of one agent becomes input for the next
- Like an assembly line

**Example:**
```python
pipeline = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[outline_agent, writer_agent, editor_agent]
)
```

**Perfect for:**
- 📝 Blog post creation (Outline → Write → Edit)
- 🔄 Data processing pipelines
- 📊 Report generation

**Pros:**
- ✅ Predictable execution order
- ✅ Easy to understand and debug
- ✅ Clear data flow

**Cons:**
- ❌ Slower (sequential, not parallel)
- ❌ Less flexible

---

### Pattern 2: Parallel Workflow

**Use when:** Tasks are independent and speed matters

**How it works:**
- Multiple agents run simultaneously
- Results are combined after all complete
- Dramatic speed improvements

**Example:**
```python
parallel_team = ParallelAgent(
    name="ResearchTeam",
    sub_agents=[tech_researcher, health_researcher, finance_researcher]
)

# Combine with sequential for aggregation
system = SequentialAgent(
    sub_agents=[parallel_team, aggregator_agent]
)
```

**Perfect for:**
- 📰 Multi-topic research
- 🔍 Independent data collection
- 🧪 Parallel testing

**Pros:**
- ✅ 3x+ faster for independent tasks
- ✅ Efficient resource usage
- ✅ Predictable execution

**Cons:**
- ❌ Only works for independent tasks
- ❌ Requires aggregation step

---

### Pattern 3: Loop Workflow

**Use when:** Iterative improvement and quality refinement are needed

**How it works:**
- Agents run in a cycle
- Review → Refine → Review → Refine
- Continues until approval or max iterations

**Example:**
```python
refinement_loop = LoopAgent(
    name="StoryRefinementLoop",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=2
)
```

**Perfect for:**
- ✍️ Content refinement (Writer ↔ Critic)
- 🧪 Test-fix cycles
- 🎨 Iterative design

**Pros:**
- ✅ Ensures quality through iteration
- ✅ Self-improving systems
- ✅ Controlled refinement cycles

**Cons:**
- ❌ Slower (multiple iterations)
- ❌ Needs exit conditions

---

## 🎯 Choosing the Right Pattern

### Decision Tree

```
Start: What kind of task do you have?

├─ Need adaptive orchestration?
│  └─ YES → LLM-Based Coordinator
│
├─ Tasks must happen in specific order?
│  └─ YES → Sequential Workflow
│
├─ Tasks are independent and speed matters?
│  └─ YES → Parallel Workflow
│
└─ Need iterative improvement cycles?
   └─ YES → Loop Workflow
```

### Real-World Examples

**E-commerce Product Launch:**
```
1. Parallel: Generate product descriptions in multiple languages
2. Sequential: Review → Edit → Publish
3. Loop: A/B test messaging until conversion optimal
```

**Research Paper Writing:**
```
1. LLM Coordinator: Decide research topics based on user query
2. Parallel: Research multiple topics simultaneously
3. Sequential: Outline → Write → Edit → Format
4. Loop: Peer review and revision cycles
```

**Software Development:**
```
1. Sequential: Design → Code → Test
2. Parallel: Run test suites concurrently
3. Loop: Code review and fix cycles
```

## 🐛 Troubleshooting

### Issue: "GOOGLE_API_KEY not found"

**Solution:**
```bash
# Make sure .env exists and has your key
cat .env

# Or set environment variable
export GOOGLE_API_KEY="your_key_here"
```

### Issue: "429 Rate Limit Error"

**Solution:**
- Wait a few seconds between requests
- The retry configuration will automatically handle this
- Consider upgrading your API quota if needed

### Issue: "Module not found: google.adk"

**Solution:**
```bash
pip install --upgrade google-adk
```

### Issue: Agents not running in expected order

**Solution:**
- For LLM Coordinator: Expected behavior (LLM decides order)
- For Sequential/Parallel/Loop: Check that you're using the correct agent type

### Issue: Loop runs forever

**Solution:**
- Check that `max_iterations` is set
- Verify exit conditions are being met
- Check that exit_loop function is properly configured

## 📖 Learning Path

**Beginner:**
1. Start with `examples/1_sequential_workflow.py`
2. Understand how agents pass data using `output_key`
3. Run `multi_agent_demo.py` to see all patterns

**Intermediate:**
1. Experiment with `examples/2_parallel_workflow.py`
2. Try modifying agent instructions
3. Create your own specialized agents

**Advanced:**
1. Combine multiple patterns (e.g., parallel + sequential)
2. Create custom tools and functions
3. Build domain-specific multi-agent systems

## 🎓 Key Concepts

### 1. Agent Specialization
Each agent has ONE clear responsibility:
```python
research_agent = Agent(
    name="ResearchAgent",
    instruction="Your ONLY job is to research..."
)
```

### 2. State Management
Agents share state using `output_key`:
```python
agent1 = Agent(
    instruction="Do research...",
    output_key="research_results"  # Saves output
)

agent2 = Agent(
    instruction="Summarize: {research_results}"  # Uses output
)
```

### 3. Tool Composition
Wrap agents as tools for coordinator patterns:
```python
coordinator = Agent(
    tools=[
        AgentTool(research_agent),  # Agent becomes a tool
        AgentTool(summarizer_agent)
    ]
)
```

### 4. Exit Conditions
Loop agents need clear exit signals:
```python
def exit_loop():
    return {"status": "approved"}

refiner = Agent(
    tools=[FunctionTool(exit_loop)],
    instruction="Call exit_loop when approved"
)
```

## 📚 Resources

### Official Documentation
- [ADK Documentation](https://github.com/google/adk-toolkit)
- [ADK Agents Overview](https://github.com/google/adk-toolkit/blob/main/docs/agents.md)
- [Sequential Agents](https://github.com/google/adk-toolkit/blob/main/docs/sequential-agents.md)
- [Parallel Agents](https://github.com/google/adk-toolkit/blob/main/docs/parallel-agents.md)
- [Loop Agents](https://github.com/google/adk-toolkit/blob/main/docs/loop-agents.md)
- [Gemini API Documentation](https://ai.google.dev/docs)

### Course Materials
- [Kaggle 5-Day Agents Course](https://www.kaggle.com/learn-guide/5-day-gen-ai)
- [Day 1b Notebook](https://www.kaggle.com/code/markishere/day-1-multi-agent-systems)

### Community
- [Kaggle Discord](https://discord.gg/kaggle)
- [Google AI Discord](https://discord.gg/google-ai)

## 🎯 Next Steps

1. **Experiment** - Try all four patterns with different prompts
2. **Customize** - Modify agent instructions and create your own
3. **Combine** - Mix patterns to solve complex problems
4. **Day 2** - Continue to the next notebook for Custom Functions and MCP Tools
5. **Build** - Create your own multi-agent systems for real-world use cases

## 💡 Pro Tips

1. **Start Simple:** Begin with Sequential, it's the easiest to understand
2. **Test Individually:** Test each agent separately before combining
3. **Clear Instructions:** Give each agent specific, clear instructions
4. **State Management:** Use descriptive `output_key` names
5. **Error Handling:** Always configure retry options
6. **Debugging:** Use `run_debug()` to see agent interactions
7. **Performance:** Use Parallel for independent tasks, Sequential for dependent ones

## ✅ Congratulations!

You've mastered multi-agent systems and workflow patterns! 🎉

**Key Takeaways:**
- ✅ Multi-agent systems are easier to build and maintain than monolithic agents
- ✅ Four patterns cover most workflow needs (LLM, Sequential, Parallel, Loop)
- ✅ Choose the right pattern based on your task requirements
- ✅ Combine patterns to solve complex problems

**Ready for more?** Continue to Day 2 to learn about Custom Functions, MCP Tools, and Long-Running Operations!

---

## 📝 License

Copyright 2025 Google LLC

Licensed under the Apache License, Version 2.0
