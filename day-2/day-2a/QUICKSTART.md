# ⚡ Quick Start Guide - Agent Tools

Get your agent tools running in **5 minutes**!

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
python agent_tools_demo.py
```

That's it! 🎉

## 💬 What You'll See

The interactive menu will appear:

```
🧰 AGENT TOOLS - Interactive Demo
======================================================================

Choose a tool pattern to explore:

  1️⃣  Custom Function Tools    - Currency converter with custom tools
  2️⃣  Code Execution           - Enhanced converter with calculations
  3️⃣  Agent as Tool            - Research coordinator with specialists
  4️⃣  Exit

======================================================================
Enter your choice (1-4):
```

## 🎯 Try Each Pattern

### Pattern 1: Custom Function Tools
- Convert currency with fees and exchange rates
- See how Python functions become agent tools
- Learn ADK best practices

### Pattern 2: Code Execution
- Enhanced currency converter with precise calculations
- Watch Python code generation and execution
- Understand why code is better than LLM math

### Pattern 3: Agent as Tool
- Research coordinator with specialist agents
- See delegation pattern in action
- Learn difference between Agent Tools and Sub-Agents

## 🎓 Run Individual Examples

Instead of the interactive demo, you can run specific patterns:

```bash
# Pattern 1: Custom Function Tools
python examples/1_custom_function_tools.py

# Pattern 2: Code Execution
python examples/2_code_execution.py

# Pattern 3: Agent as Tool
python examples/3_agent_as_tool.py
```

## 🏗️ Pattern Comparison

| Pattern | Use Case | Key Benefit |
|---------|----------|-------------|
| Custom Functions | Business logic | Complete control |
| Code Execution | Calculations | Precision & reliability |
| Agent as Tool | Delegation | Reusable specialists |

## ❓ Common Issues

**API Key Error:**
```bash
# Make sure .env exists and has your key
cat .env
```

**Module Not Found:**
```bash
# Make sure you're in the correct directory
cd /path/to/day-2a
python examples/1_custom_function_tools.py
```

**Tool Not Being Called:**
- Check tool is in `tools=[]` list
- Verify instruction references tool by function name
- Check docstring is clear

## 📚 Full Documentation

See [README.md](README.md) for:
- Complete tool types guide
- Detailed best practices
- Advanced patterns
- Troubleshooting guide

## 🎯 Next Steps

1. ✅ Try all three patterns
2. ✅ Read the [README.md](README.md) for details
3. ✅ Create your own custom tools
4. ✅ Continue to Day 2b for advanced patterns

## 💡 Quick Tips

- **Docstrings Matter:** LLMs use them to understand tools
- **Return Dictionaries:** Always use {"status": "success/error"}
- **Type Hints:** Enable proper schema generation
- **Code for Math:** LLMs make calculation errors
- **Test Tools:** Test functions separately before using in agents

Happy coding! 🚀
