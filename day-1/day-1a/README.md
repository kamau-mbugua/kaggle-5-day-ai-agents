# 🚀 Day 1a: Your First AI Agent with Google ADK

Based on the **Kaggle 5-Day AI Agents Intensive Course**

This project demonstrates how to build your first AI agent using Google's Agent Development Kit (ADK). The agent can use tools like Google Search to answer questions with current information.

## 📋 Table of Contents

- [What is an AI Agent?](#what-is-an-ai-agent)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Understanding the Code](#understanding-the-code)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

## 🤔 What is an AI Agent?

A traditional LLM interaction:
```
Prompt → LLM → Text Response
```

An AI Agent can do more:
```
Prompt → Agent → Thought → Action → Observation → Final Answer
```

**Key Difference:** Agents can take actions using tools (like Google Search) to get better answers!

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
day-1a/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── simple_agent.py              # Standalone agent script
└── sample-agent/                # ADK CLI agent structure
    ├── __init__.py
    ├── agent.py                 # Agent definition for ADK CLI
    └── .env.example
```

## 🛠️ Setup Instructions

### Step 1: Install Dependencies

```bash
# Navigate to the project directory
cd /home/kelvin/IdeaProjects/5-Day-AI-Agents-Intensive-Course-with-Google/day-1/day-1a

# Install required packages
pip install -r requirements.txt
```

### Step 2: Configure API Key

#### Option A: Using .env file (Recommended)

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```bash
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

#### Option B: Using environment variable

```bash
export GOOGLE_API_KEY="your_actual_api_key_here"
```

### Step 3: Verify Installation

```bash
# Check if google-adk is installed
pip show google-adk

# Check if adk command is available
adk --version
```

## 🚀 Usage

### Method 1: Run the Simple Agent Script (Recommended for Beginners)

This script provides an interactive way to chat with your agent:

```bash
python simple_agent.py
```

**Features:**
- ✅ Automatic API key loading from `.env`
- ✅ Pre-configured example queries
- ✅ Interactive chat mode
- ✅ Error handling and retry logic

**Example Output:**
```
🚀 Starting AI Agent with Google ADK

✅ Gemini API key loaded successfully.
📋 Configuring retry options...
✅ Retry configuration created.
🤖 Creating AI agent...
✅ Agent created successfully.
⚙️  Creating runner...
✅ Runner created successfully.

================================================================================
Query: What is Agent Development Kit from Google?
================================================================================

User > What is Agent Development Kit from Google?
helpful_assistant > The Agent Development Kit (ADK) from Google is...
```

### Method 2: Using ADK CLI Commands

The `sample-agent` folder is configured to work with ADK CLI tools.

#### 2.1: Configure the sample-agent

```bash
cd sample-agent
cp .env.example .env
# Edit .env and add your API key
```

#### 2.2: Run with ADK CLI

**Option A: Command-line runner**
```bash
adk run
```
Then type your questions interactively.

**Option B: Web UI (Recommended)**
```bash
adk web
```
Then open http://localhost:8000 in your browser.

**Option C: API Server**
```bash
adk api_server
```
Starts a REST API server on port 8000.

### Method 3: Create Your Own Agent

You can create a new agent using the ADK CLI:

```bash
# Create a new agent with your API key
adk create my-custom-agent --model gemini-2.5-flash-lite --api_key $GOOGLE_API_KEY

# Navigate to the new agent directory
cd my-custom-agent

# Run the agent
adk web
```

## 📚 Understanding the Code

### Key Components

#### 1. **Agent Configuration**

```python
root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(model="gemini-2.5-flash-lite"),
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info.",
    tools=[google_search],  # Tools the agent can use
)
```

#### 2. **Retry Configuration**

Handles transient errors like rate limits:

```python
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)
```

#### 3. **Runner**

Orchestrates the conversation between you and the agent:

```python
runner = InMemoryRunner(agent=root_agent)
response = await runner.run_debug("Your question here")
```

### How It Works

1. **User asks a question** → "What's the weather in London?"
2. **Agent analyzes** → Realizes it needs current information
3. **Agent uses tool** → Calls Google Search
4. **Agent observes** → Reviews search results
5. **Agent responds** → Provides answer based on current data

## 🐛 Troubleshooting

### Issue: "GOOGLE_API_KEY not found"

**Solution:**
1. Make sure you created a `.env` file (not `.env.example`)
2. Verify the API key is correct
3. Check that `.env` is in the same directory as the script

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

### Issue: "adk command not found"

**Solution:**
```bash
# Make sure google-adk is installed
pip install google-adk

# If still not working, try reinstalling
pip uninstall google-adk
pip install google-adk
```

### Issue: Agent not using Google Search

**Solution:**
- Check that `google_search` is included in the `tools` list
- Verify the agent's instruction mentions using search
- Try asking questions that require current information

## 📖 Example Queries to Try

### General Knowledge
```
- What is Agent Development Kit from Google?
- Explain how AI agents work
```

### Current Information
```
- What's the weather in [your city]?
- Who won the last FIFA World Cup?
- What new movies are in theaters now?
- What's the current price of Bitcoin?
```

### Research Questions
```
- What are the latest features in Python 3.13?
- Compare React and Vue frameworks
- What are the best practices for API design?
```

## 🔧 Advanced Configuration

### Changing the Model

You can use different Gemini models:

```python
model=Gemini(
    model="gemini-2.5-flash-lite"  # Fast and efficient
    # model="gemini-2.0-flash-exp"  # Experimental features
    # model="gemini-1.5-pro"         # More capable
)
```

### Adding More Tools

ADK provides several built-in tools:

```python
from google.adk.tools import google_search, code_execution

tools=[
    google_search,
    code_execution,  # Execute Python code
]
```

### Custom Instructions

Customize the agent's behavior:

```python
instruction="""
You are a helpful assistant specialized in Python programming.
Use Google Search for current library documentation.
Always provide code examples when explaining concepts.
"""
```

## 📚 Resources

### Official Documentation
- [ADK Documentation](https://github.com/google/adk-toolkit)
- [ADK Quickstart for Python](https://github.com/google/adk-toolkit/blob/main/docs/quickstart-python.md)
- [Gemini API Documentation](https://ai.google.dev/docs)

### Course Materials
- [Kaggle 5-Day Agents Course](https://www.kaggle.com/learn-guide/5-day-gen-ai)
- [Day 1 Notebook](https://www.kaggle.com/code/markishere/day-1-simple-ai-agents)

### Community
- [Kaggle Discord](https://discord.gg/kaggle)
- [Google AI Discord](https://discord.gg/google-ai)

## 🎯 Next Steps

1. **Experiment** - Try different questions and observe how the agent uses tools
2. **Customize** - Modify the agent's instructions and behavior
3. **Day 2** - Continue to the next notebook to learn about multi-agent systems
4. **Build** - Create your own agents for specific use cases

## 📝 License

Copyright 2025 Google LLC

Licensed under the Apache License, Version 2.0

---

## ✅ Congratulations!

You've successfully set up your first AI agent! 🎉

The key takeaway: Your agent doesn't just respond—it **reasons**, **acts**, and **observes** to give better answers.

**Ready for more?** Continue to Day 2 to learn about multi-agent architectures!
