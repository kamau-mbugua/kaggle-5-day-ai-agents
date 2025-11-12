# ⚡ Quick Start Guide - Multi-Agent Systems

Get your multi-agent system running in **5 minutes**!

## 🎯 Prerequisites

- Python 3.10+
- Google Gemini API Key ([Get it here](https://aistudio.google.com/app/apikey))

## 🚀 3 Steps to Run

### 1️⃣ Install Dependencies

```bash
pip install google-adk python-dotenv
```

### 2️⃣ Set Up API Key

```bash
# Copy the environment template
cp .env.example .env

# Edit .env and add your API key
# GOOGLE_API_KEY=your_actual_key_here
```

Or set it directly:
```bash
export GOOGLE_API_KEY="your_actual_key_here"
```

### 3️⃣ Run the Interactive Demo

```bash
python multi_agent_demo.py
```

That's it! 🎉

## 💬 What You'll See

The interactive menu will appear:

```
🤖 MULTI-AGENT SYSTEMS & WORKFLOW PATTERNS
======================================================================

Choose a workflow pattern to explore:

  0️⃣  LLM-Based Coordinator  - Dynamic orchestration
  1️⃣  Sequential Workflow     - Guaranteed order (Blog Creation)
  2️⃣  Parallel Workflow       - Concurrent execution (Multi-Research)
  3️⃣  Loop Workflow           - Iterative refinement (Story Writing)
  4️⃣  Exit

======================================================================
Enter your choice (0-4):
```

## 🎯 Try Each Pattern

### Pattern 0: LLM Coordinator
- Ask: "What are the latest advancements in quantum computing?"
- Watch the coordinator dynamically orchestrate research and summarization

### Pattern 1: Sequential Workflow
- Create a blog post about multi-agent systems
- See how Outline → Writer → Editor work in sequence

### Pattern 2: Parallel Workflow
- Run a daily briefing on Tech, Health, and Finance
- Watch three researchers work simultaneously

### Pattern 3: Loop Workflow
- Write a short story that gets iteratively refined
- See the Critic ↔ Refiner loop improve quality

## 🎓 Run Individual Examples

Instead of the interactive demo, you can run specific patterns:

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

## 🏗️ Pattern Comparison

| Pattern | Speed | Predictability | Best For |
|---------|-------|----------------|----------|
| LLM Coordinator | ⚡⚡ | 🎲 Flexible | Dynamic tasks |
| Sequential | ⚡ | ✅ Guaranteed | Linear pipelines |
| Parallel | ⚡⚡⚡ | ✅ Guaranteed | Independent tasks |
| Loop | ⚡ | ✅ Guaranteed | Iterative refinement |

## ❓ Common Issues

**API Key Error:**
```bash
# Make sure .env exists and has your key
cat .env
```

**Module Not Found:**
```bash
pip install --upgrade google-adk
```

**Rate Limits:**
- Wait a few seconds between requests
- Retry config handles this automatically

## 📚 Full Documentation

See [README.md](README.md) for:
- Complete pattern explanations
- Detailed architecture diagrams
- Advanced usage examples
- Troubleshooting guide
- Best practices

## 🎯 Next Steps

1. ✅ Try all four patterns
2. ✅ Read the [README.md](README.md) for deep dives
3. ✅ Modify examples to create your own agents
4. ✅ Continue to Day 2 for advanced topics

## 💡 Quick Tips

- **Start with Sequential** - Easiest to understand
- **Use Parallel for speed** - When tasks are independent
- **Use Loop for quality** - When refinement is needed
- **Debug with run_debug()** - See agent interactions

Happy coding! 🚀
