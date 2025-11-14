# Quick Start Guide - Agent Evaluation

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
cd day-4/day-4b

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
python evaluation_demo.py
```

### Demo Options

1. **Basic Evaluation Setup** - Metrics, workflow, and concepts
2. **Creating Test Cases** - Evalsets and configuration
3. **Running Evaluations** - CLI commands and results
4. **Analyzing Failures** - Debug and fix workflow
5. **Create Home Agent** - Hands-on practice
6. **Run All** - Full tour

## What Each Example Does

### 1. Basic Evaluation Setup (`examples/example_1_basic_evaluation.py`)

**What it demonstrates:**
- Evaluation vs traditional testing
- Understanding evaluation metrics
- Score interpretation
- Evaluation workflow

**What you'll see:**
```
DEMO 1: What is Agent Evaluation?
Traditional: divide(10, 0) → ZeroDivisionError ✅
AI Agent: 'Find papers' → ??? (How to measure?)
💡 Evaluation = Systematic quality measurement

DEMO 2: Understanding Evaluation Metrics
1. response_match_score (0.0 - 1.0)
   Measures: Text similarity

   Expected: 'The living room lights are now on.'
   Actual:   'Living room lights turned on.'
   Score:    0.92 ✅ (semantically equivalent)

2. tool_trajectory_avg_score (0.0 - 1.0)
   Measures: Tool usage correctness

   Expected: set_device_status(location='living_room', ...)
   Actual:   set_device_status(location='living_room', ...)
   Score:    1.0 ✅ (perfect match)

Typical Thresholds:
┌──────────────────────┬───────────────┬─────────────────────┐
│ Metric               │ Threshold     │ Interpretation      │
├──────────────────────┼───────────────┼─────────────────────┤
│ response_match_score │ ≥ 0.8         │ Semantically close  │
│ tool_trajectory_avg  │ = 1.0         │ Exact tool match    │
└──────────────────────┴───────────────┴─────────────────────┘
```

**Key takeaway:** Evaluation provides systematic quality measurement

---

### 2. Creating Test Cases (`examples/example_2_test_cases.py`)

**What it demonstrates:**
- Test case structure
- Creating evalsets programmatically
- Writing test configurations
- Test design best practices

**What you'll see:**
```
DEMO 1: Anatomy of a Test Case
Components:
  1. eval_id: Unique identifier
  2. user_content: Input query
  3. final_response: Expected response
  4. intermediate_data: Expected tool calls (optional)

DEMO 2: Create Test Case
test_case = create_eval_case(
    eval_id="test_turn_on_lights",
    user_query="Turn on the living room lights",
    expected_response="The living room lights are now on.",
    expected_tools=[{
        "name": "set_device_status",
        "args": {"location": "living_room", ...}
    }]
)

DEMO 3: Create Evalset
✅ Created evalset with 5 test cases:
  1. test_turn_on_living_room_lights (with tools)
  2. test_turn_off_bedroom_lights (with tools)
  3. test_set_thermostat_temperature (with tools)
  4. test_turn_off_all_kitchen_devices (with tools)
  5. test_capability_query (no tools)

DEMO 4: Best Practices
✅ DO:
  • Use descriptive eval_id names
  • Test one behavior per case
  • Cover positive AND negative cases
  • Use realistic user queries
  • Specify exact expected responses

❌ DON'T:
  • Make tests dependent on each other
  • Test multiple unrelated behaviors
  • Use vague expected responses
```

**Key takeaway:** Well-designed test cases enable reliable evaluation

---

### 3. Running Evaluations (`examples/example_3_running_evaluations.py`)

**What it demonstrates:**
- Using adk eval CLI command
- Command options and flags
- Understanding output
- Interpreting results files

**What you'll see:**
```
DEMO 1: The adk eval CLI Command
Basic:
  adk eval <agent_directory> <evalset_file>

With Configuration:
  adk eval home_automation_agent \
           home_automation_agent/integration.evalset.json \
           --config_file_path=home_automation_agent/test_config.json

With Detailed Output:
  adk eval home_automation_agent \
           home_automation_agent/integration.evalset.json \
           --config_file_path=home_automation_agent/test_config.json \
           --print_detailed_results

DEMO 2: Understanding Output
┌────────────────────────────────────┐
│ Evaluation Summary                 │
├────────────────────────────────────┤
│ Total Test Cases: 5                │
│ Passed: 3                          │
│ Failed: 2                          │
│ Pass Rate: 60.0%                   │
└────────────────────────────────────┘

DEMO 3: Score Interpretation
response_match_score:
  0.0 - 0.3  ❌ Completely different
  0.3 - 0.6  ⚠️  Partially related
  0.6 - 0.8  🟡 Similar meaning
  0.8 - 1.0  ✅ Very similar

tool_trajectory_avg_score:
  1.0  ✅ Perfect match
  0.7  ⚠️  Partial match
  0.0  ❌ No match
```

**Key takeaway:** adk eval CLI automates batch testing

---

### 4. Analyzing and Fixing Failures (`examples/example_4_analysis_and_fixes.py`)

**What it demonstrates:**
- Analyzing evaluation failures
- Common failure patterns
- Systematic debugging
- Fixing instructions and tools
- Iterative improvement

**What you'll see:**
```
DEMO 1: Common Failure Patterns
Pattern 1: Low Response Match Score
  response_match_score: 0.45
  tool_trajectory_avg_score: 1.0
  Issue: Vague response format
  Fix: Add response template to instructions

Pattern 2: Low Tool Trajectory Score
  response_match_score: 0.95
  tool_trajectory_avg_score: 0.33
  Issue: Wrong tool parameters
  Fix: Improve tool descriptions

Pattern 3: Both Scores Low
  response_match_score: 0.25
  tool_trajectory_avg_score: 0.0
  Issue: Agent doesn't understand
  Fix: Add examples to instructions

DEMO 2: Fixing Agent Instructions
❌ BEFORE:
  instruction = "You control smart home devices. Be helpful."

✅ AFTER:
  instruction = """
  You are a home automation assistant.

  RESPONSE FORMAT (always use):
  "The {location} {device} are now {status}."

  Example:
  User: "Turn on the living room lights"
  You: "The living room lights are now on."
  """

DEMO 3: Iterative Improvement
Iteration 1: 2/5 passed (40%) → Fix vague responses
Iteration 2: 4/5 passed (80%) → Fix parameter format
Iteration 3: 5/5 passed (100%) ✅ → Ready to deploy!
```

**Key takeaway:** Systematic debugging leads to 100% pass rates

---

### 5. Home Automation Agent (Hands-on Practice)

**Create the agent:**
```bash
python create_home_agent.py
```

**What it creates:**
```
home_automation_agent/
├── agent.py                    # Broken version (for learning)
├── agent_fixed.py              # Fixed version (reference)
├── integration.evalset.json    # Test cases
├── test_config.json            # Evaluation thresholds
└── .env                        # API key (add yours!)
```

**Run evaluation:**
```bash
cd home_automation_agent

# Add your API key first
nano .env

# Run evaluation
adk eval . integration.evalset.json \
  --config_file_path=test_config.json \
  --print_detailed_results
```

**Expected Results:**
- Some tests will fail initially
- Identify failures: vague responses, parameter issues
- Fix: Update agent.py (or compare with agent_fixed.py)
- Re-evaluate: Achieve 100% pass rate

**Key takeaway:** Practice makes perfect!

---

## Quick Test Commands

```bash
# Run individual examples
python examples/example_1_basic_evaluation.py
python examples/example_2_test_cases.py
python examples/example_3_running_evaluations.py
python examples/example_4_analysis_and_fixes.py

# Create home automation agent
python create_home_agent.py

# Run interactive demo
python evaluation_demo.py
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

### "Agent not found"

**Problem:** Wrong directory or agent not created

**Fix:**
```bash
# Create agent first
python create_home_agent.py

# Then navigate to agent directory
cd home_automation_agent

# Run evaluation from within agent directory
adk eval . integration.evalset.json --config_file_path=test_config.json
```

### Low Scores Despite Correct Behavior

**Problem:** Agent works but scores are low

**Fix:**
1. Check expected response matches agent style
2. Adjust thresholds if semantically correct
3. Standardize response format in instructions

## Understanding the Code

### Creating Test Cases Pattern

```python
from utils import create_eval_case, create_evalset, save_evalset

# Create test case
test_case = create_eval_case(
    eval_id="test_turn_on_lights",
    user_query="Turn on the living room lights",
    expected_response="The living room lights are now on.",
    expected_tools=[
        {
            "name": "set_device_status",
            "args": {
                "location": "living_room",
                "device_id": "lights",
                "status": "on"
            }
        }
    ]
)

# Create evalset
evalset = create_evalset(
    eval_set_id="my_test_suite",
    eval_cases=[test_case]
)

# Save to file
save_evalset(evalset, "agent/tests.evalset.json")
```

### Running Evaluation Pattern

```bash
# Basic command
adk eval <agent_dir> <evalset_file>

# With configuration
adk eval <agent_dir> <evalset_file> \
  --config_file_path=<config_file>

# With detailed output
adk eval <agent_dir> <evalset_file> \
  --config_file_path=<config_file> \
  --print_detailed_results
```

### Analyzing Results Pattern

```python
from utils import analyze_results, print_evaluation_summary

# Analyze results file
analysis = analyze_results("integration.evalset.json.results")

# Print summary
print_evaluation_summary(analysis)

# Check specific metrics
print(f"Pass rate: {analysis['passed'] / analysis['total_cases'] * 100:.1f}%")
print(f"Avg response score: {analysis['avg_response_score']:.3f}")
print(f"Avg tool score: {analysis['avg_tool_score']:.3f}")
```

## Key Concepts (2-Minute Summary)

### The Evaluation Problem

```
Traditional Software:
  divide_by_zero() → Clear: ZeroDivisionError

AI Agents:
  "Find papers" → "I cannot help"  ← Why??
```

### The Solution

```
Evaluation = Quality Measurement for AI Agents

Metrics:
  ✅ response_match_score: Text similarity (0.0-1.0)
  ✅ tool_trajectory_avg_score: Tool correctness (0.0-1.0)
```

### The Workflow

```
1. Create Test Cases → evalset.json
2. Configure Thresholds → test_config.json
3. Run Evaluation → adk eval
4. Analyze Results → .results file
5. Fix and Iterate → Until 100% pass rate
```

### Score Thresholds

| Metric | Threshold | Why |
|--------|-----------|-----|
| **response_match** | ≥ 0.8 | Multiple valid phrasings |
| **tool_trajectory** | = 1.0 | Exact match required |

### Debugging Pattern

```
Symptom → Logs → Root Cause → Fix → Verify
```

## Next Steps

1. **Explore Examples**: Run all 5 example files and the demo
2. **Create Your Agent**: Build the home automation agent
3. **Run Evaluation**: Practice with adk eval CLI
4. **Debug Failures**: Achieve 100% pass rate
5. **Read Full Documentation**: Check `README.md` for deep dives
6. **Apply to Projects**: Use evaluation in your own agents

## Project Structure

```
day-4b/
├── examples/
│   ├── example_1_basic_evaluation.py          # Concepts & metrics
│   ├── example_2_test_cases.py                # Creating evalsets
│   ├── example_3_running_evaluations.py       # CLI usage
│   └── example_4_analysis_and_fixes.py        # Debugging
├── utils/
│   ├── __init__.py
│   └── evaluation_helpers.py                   # Helper functions
├── create_home_agent.py                        # Agent generator
├── evaluation_demo.py                          # Interactive demo
├── requirements.txt                            # Dependencies
├── .env.example                                # API key template
├── README.md                                   # Full documentation
└── QUICKSTART.md                               # This file
```

## Resources

- **Full Documentation**: `README.md`
- **Google ADK Docs**: https://ai.google.dev/adk
- **Evaluation Guide**: https://ai.google.dev/adk/evaluation
- **Get API Key**: https://aistudio.google.com/app/apikey
- **Kaggle Course**: https://www.kaggle.com/learn-guide/5-day-genai

## Need Help?

1. **Check README.md**: Comprehensive troubleshooting section
2. **Test Components**: Run examples independently
3. **Verify Setup**: Check `.env` file and dependencies
4. **Community**: Google ADK Discord for support

---

**You're all set!** 🎉 Run `python evaluation_demo.py` to start exploring agent evaluation!
