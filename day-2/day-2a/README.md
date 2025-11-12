# 🧰 Day 2a: Agent Tools - Custom Functions & Code Execution

Based on the **Kaggle 5-Day AI Agents Intensive Course**

Learn how to build agents that take intelligent actions with custom tools. Transform Python functions into agent tools, execute code for reliable calculations, and use agents as tools within other agents.

## 📋 Table of Contents

- [Why Do Agents Need Tools?](#why-do-agents-need-tools)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Tool Patterns](#tool-patterns)
- [Complete Tool Types Guide](#complete-tool-types-guide)
- [Best Practices](#best-practices)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

## 🤔 Why Do Agents Need Tools?

### The Problem
Without tools, an agent's knowledge is frozen in time:
- ❌ Can't access today's news or current information
- ❌ Can't check your company's inventory or database
- ❌ Can't take actions on your behalf
- ❌ No connection to the outside world

### The Solution
**Tools transform isolated LLMs into capable agents that can actually help you get things done.**

## ✅ Prerequisites

1. **Python 3.10+**
2. **Google Gemini API Key** - [Get it here](https://aistudio.google.com/app/apikey)
3. **Google ADK**
   ```bash
   pip install google-adk
   ```

## 📁 Project Structure

```
day-2a/
├── README.md                          # Complete documentation
├── QUICKSTART.md                      # 5-minute guide
├── requirements.txt                   # Dependencies
├── .env.example                       # API key template
├── .gitignore
│
├── agent_tools_demo.py                # Interactive demo (all patterns)
│
├── examples/                          # Individual pattern examples
│   ├── 1_custom_function_tools.py     # Currency converter
│   ├── 2_code_execution.py            # Enhanced with calculations
│   └── 3_agent_as_tool.py             # Research coordinator
│
└── tools/                             # Reusable custom tools
    ├── __init__.py
    └── currency_tools.py              # Currency conversion tools
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd /path/to/day-2a
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
cp .env.example .env
# Edit .env and add: GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Run Interactive Demo
```bash
python agent_tools_demo.py
```

Or run individual examples:
```bash
python examples/1_custom_function_tools.py
python examples/2_code_execution.py
python examples/3_agent_as_tool.py
```

## 🎯 Tool Patterns

### Pattern 1: Custom Function Tools

**What:** Turn Python functions into agent tools

**When to use:** Need custom business logic, domain-specific functionality

**Example:** Currency converter with fees and exchange rates

```python
def get_fee_for_payment_method(method: str) -> dict:
    """Looks up transaction fee percentage."""
    fee_database = {
        "platinum credit card": 0.02,
        "bank transfer": 0.01,
    }
    fee = fee_database.get(method.lower())
    if fee:
        return {"status": "success", "fee_percentage": fee}
    return {"status": "error", "error_message": "Method not found"}

agent = LlmAgent(
    name="currency_agent",
    tools=[get_fee_for_payment_method],  # Function becomes tool!
    instruction="Use get_fee_for_payment_method() to find fees..."
)
```

**Key Benefits:**
- ✅ Any Python function becomes a tool instantly
- ✅ Complete control over functionality
- ✅ Easy to test and maintain

---

### Pattern 2: Code Execution

**What:** Use BuiltInCodeExecutor for reliable calculations

**When to use:** Need precise calculations, avoid LLM math errors

**Example:** Enhanced currency converter with Python calculations

```python
# Calculation specialist
calculation_agent = LlmAgent(
    name="CalculationAgent",
    instruction="Generate ONLY Python code for calculations",
    code_executor=BuiltInCodeExecutor(),  # Enables code execution!
)

# Main agent uses calculation specialist
agent = LlmAgent(
    name="enhanced_currency_agent",
    tools=[
        get_fee_for_payment_method,
        get_exchange_rate,
        AgentTool(agent=calculation_agent),  # Use agent as tool!
    ],
    instruction="Use calculation_agent for precise math..."
)
```

**Key Benefits:**
- ✅ No LLM math errors - code is precise
- ✅ Repeatable, auditable calculations
- ✅ Generated code is visible

---

### Pattern 3: Agent as Tool

**What:** Use specialist agents within coordinator agents

**When to use:** Need delegation to domain experts

**Example:** Research coordinator with data analyst and summarizer

```python
# Create specialists
data_analyst = LlmAgent(
    name="DataAnalystAgent",
    instruction="Analyze numerical data and trends..."
)

summarizer = LlmAgent(
    name="SummarizerAgent",
    instruction="Create concise summaries..."
)

# Coordinator uses specialists as tools
coordinator = LlmAgent(
    name="ResearchCoordinator",
    tools=[
        google_search,
        AgentTool(agent=data_analyst),    # Agent as tool!
        AgentTool(agent=summarizer),      # Agent as tool!
    ],
    instruction="Use specialists for analysis and summarization..."
)
```

**Key Benefits:**
- ✅ Reuse specialist agents across systems
- ✅ Clear separation of concerns
- ✅ Coordinator stays in control

---

## 🧰 Complete Tool Types Guide

### Custom Tools
Build your own tools for specific needs

| Type | Description | Example |
|------|-------------|---------|
| **Function Tools** ✅ | Python functions as tools | `get_fee_for_payment_method` |
| **Agent Tools** ✅ | Agents used as tools | `AgentTool(agent=calc_agent)` |
| **Long Running Tools** | For operations that take time | Human-in-loop approvals |
| **MCP Tools** | Model Context Protocol servers | Filesystem, databases |
| **OpenAPI Tools** | Auto-generated from API specs | REST API endpoints |

### Built-in Tools
Pre-built tools ready to use

| Type | Description | Example |
|------|-------------|---------|
| **Gemini Tools** ✅ | Leverage Gemini capabilities | `google_search`, `BuiltInCodeExecutor` |
| **Google Cloud Tools** | Enterprise integration | BigQuery, Spanner |
| **Third-party Tools** | Existing tool ecosystems | Hugging Face, GitHub |

## 🏆 ADK Best Practices

### 1. Dictionary Returns
```python
# Good
return {"status": "success", "data": result}
return {"status": "error", "error_message": "Failed"}

# Bad
return result  # No status indicator
raise Exception("Failed")  # Unstructured error
```

### 2. Clear Docstrings
```python
def get_exchange_rate(base_currency: str, target_currency: str) -> dict:
    """Looks up and returns the exchange rate between two currencies.

    Args:
        base_currency: ISO 4217 code (e.g., "USD")
        target_currency: ISO 4217 code (e.g., "EUR")

    Returns:
        Success: {"status": "success", "rate": 0.93}
        Error: {"status": "error", "error_message": "..."}
    """
```

### 3. Type Hints
```python
def process_data(amount: float, currency: str) -> dict:
    # Type hints enable proper schema generation
    pass
```

### 4. Error Handling
```python
try:
    result = risky_operation()
    return {"status": "success", "data": result}
except Exception as e:
    return {"status": "error", "error_message": str(e)}
```

## 📚 Examples Deep Dive

### Example 1: Custom Function Tools
```bash
python examples/1_custom_function_tools.py
```

**What it does:**
- Currency conversion with fees and exchange rates
- Uses two custom function tools
- Demonstrates ADK best practices

**Key Concepts:**
- Function → Tool transformation
- Dictionary returns with status
- Error handling patterns

---

### Example 2: Code Execution
```bash
python examples/2_code_execution.py
```

**What it does:**
- Enhanced currency converter with precise calculations
- Generates and executes Python code
- Shows generated code and results

**Key Concepts:**
- BuiltInCodeExecutor usage
- Agent as tool pattern
- Code visibility and auditability

---

### Example 3: Agent as Tool
```bash
python examples/3_agent_as_tool.py
```

**What it does:**
- Research coordinator with specialist agents
- Data analyst and summarizer as tools
- Demonstrates delegation pattern

**Key Concepts:**
- AgentTool usage
- Specialist agent design
- Coordinator pattern

---

## 🎯 Agent Tools vs Sub-Agents

### Agent Tools (Delegation)
```
Coordinator Agent
      ├─ calls → Specialist Agent 1
      ├─ gets result ←
      ├─ calls → Specialist Agent 2
      └─ gets result ←
Coordinator stays in control!
```

**Use when:** Need results from specialists to continue workflow

### Sub-Agents (Handoff)
```
Main Agent
  └─ transfers control → Specialist Agent
                         (now handles all input)
```

**Use when:** Transferring user to different specialist (e.g., support tiers)

---

## 🐛 Troubleshooting

### Issue: "GOOGLE_API_KEY not found"
```bash
# Check .env file exists
cat .env

# Set environment variable
export GOOGLE_API_KEY="your_key_here"
```

### Issue: "Module not found: tools"
```bash
# Make sure you're in the project directory
cd /path/to/day-2a

# Run with correct path
python examples/1_custom_function_tools.py
```

### Issue: Tool not being called
**Solution:**
- Check tool is in `tools=[]` list
- Verify instruction references tool by exact function name
- Check docstring is clear for LLM understanding

### Issue: Code execution fails
**Solution:**
- Verify BuiltInCodeExecutor is configured
- Check generated code syntax
- Ensure calculation agent instruction specifies Python-only output

---

## 💡 Pro Tips

1. **Start Simple:** Begin with function tools, then add complexity
2. **Clear Docstrings:** LLMs use them to understand when to use tools
3. **Error Handling:** Always return structured errors with status
4. **Test Individually:** Test each tool separately before combining
5. **Code Execution:** Use for math - LLMs make calculation errors
6. **Agent Tools:** Great for reusing specialists across systems
7. **Type Hints:** Enable proper schema generation

---

## 📖 Learning Path

**Beginner:**
1. Run `agent_tools_demo.py` to see all patterns
2. Study `examples/1_custom_function_tools.py`
3. Understand dictionary returns and docstrings

**Intermediate:**
1. Experiment with `examples/2_code_execution.py`
2. Create your own custom function tools
3. Try combining multiple tool types

**Advanced:**
1. Build specialist agents with `examples/3_agent_as_tool.py`
2. Combine patterns (functions + code execution + agent tools)
3. Create domain-specific multi-tool systems

---

## 📚 Resources

### Official Documentation
- [ADK Documentation](https://github.com/google/adk-toolkit)
- [ADK Tools Guide](https://github.com/google/adk-toolkit/blob/main/docs/tools.md)
- [ADK Function Tools](https://github.com/google/adk-toolkit/blob/main/docs/function-tools.md)
- [Gemini API Docs](https://ai.google.dev/docs)

### Course Materials
- [Kaggle 5-Day Agents Course](https://www.kaggle.com/learn-guide/5-day-gen-ai)
- [Day 2a Notebook](https://www.kaggle.com/code/markishere/day-2-agent-tools)

### Community
- [Kaggle Discord](https://discord.gg/kaggle)
- [Google AI Discord](https://discord.gg/google-ai)

---

## 🎯 Next Steps

1. ✅ Run all examples to see tools in action
2. ✅ Create your own custom function tools
3. ✅ Experiment with code execution
4. ✅ Build specialist agents
5. ✅ Continue to Day 2b for Tool Patterns and MCP Tools

---

## ✅ Congratulations!

You've mastered agent tools! 🎉

**Key Takeaways:**
- ✅ Python functions become tools instantly
- ✅ Code execution provides reliable calculations
- ✅ Agent tools enable specialist delegation
- ✅ Follow ADK best practices for robust tools
- ✅ Combine tool types for powerful agents

**Ready for more?** Continue to Day 2b for advanced tool patterns!

---

## 📝 License

Copyright 2025 Google LLC
Licensed under the Apache License, Version 2.0
