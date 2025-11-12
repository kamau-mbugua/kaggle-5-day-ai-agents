# ⚡ Quick Start Guide

Get your AI agent running in **5 minutes**!

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

### 3️⃣ Run the Agent

```bash
python simple_agent.py
```

That's it! 🎉

## 💬 Try These Questions

Once the agent starts, try asking:

- "What's the weather in London?"
- "Who won the last World Cup?"
- "What is Google ADK?"

## 🌐 Use the Web UI (Optional)

For a better experience with a graphical interface:

```bash
cd sample-agent
cp .env.example .env
# Edit .env with your API key
adk web
```

Then open http://localhost:8000

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.

## ❓ Issues?

**API Key Error:**
```bash
# Make sure .env exists and has your key
cat .env
```

**Module Not Found:**
```bash
pip install --upgrade google-adk
```

**Need Help?**
Check the [Troubleshooting section](README.md#troubleshooting) in the README.
