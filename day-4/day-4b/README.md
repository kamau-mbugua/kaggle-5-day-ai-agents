# Day 4b - Agent Evaluation

**Master systematic agent testing and quality measurement with Google ADK's evaluation framework**

## Overview

This module teaches you how to systematically test and evaluate AI agents using Google ADK's evaluation framework. Learn to create test cases, run automated evaluations, interpret results, and iteratively improve agent quality.

### What You'll Learn

- **Evaluation Concepts**: Understand evaluation vs testing, key metrics, and systematic quality measurement
- **Test Case Creation**: Design comprehensive evalsets with expected responses and tool trajectories
- **Running Evaluations**: Use `adk eval` CLI for batch testing with configurable thresholds
- **Debugging Failures**: Analyze results, identify root causes, and apply targeted fixes
- **Iterative Improvement**: Achieve 100% pass rates through systematic refinement

### Why Evaluation Matters

Traditional software testing:
```python
divide(10, 0)  # ZeroDivisionError - clear pass/fail
```

AI agent testing:
```python
agent.run("Find papers about transformers")
# Result: ??? - How do we measure quality?
```

**Evaluation provides systematic quality measurement** for AI agents where outputs are not deterministic.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup environment
cp .env.example .env
# Add your GOOGLE_API_KEY to .env

# 3. Run interactive demo
python evaluation_demo.py

# 4. Create practice agent
python create_home_agent.py

# 5. Run evaluation
cd home_automation_agent
adk eval . integration.evalset.json --config_file_path=test_config.json --print_detailed_results
```

## Core Concepts

### Evaluation Metrics

Google ADK provides two primary evaluation metrics:

#### 1. response_match_score (0.0 - 1.0)

**Measures**: Text similarity between expected and actual agent responses

**Calculation**: Semantic similarity using embeddings

**Interpretation**:
- `0.8 - 1.0` ✅ Very similar (semantically equivalent)
- `0.6 - 0.8` 🟡 Similar meaning (acceptable variation)
- `0.3 - 0.6` ⚠️ Partially related (potential issue)
- `0.0 - 0.3` ❌ Completely different (failure)

**Example**:
```python
Expected: "The living room lights are now on."
Actual:   "Living room lights turned on."
Score:    0.92 ✅ (semantically equivalent)

Actual:   "I turned on the lights."
Score:    0.75 🟡 (similar but missing location)

Actual:   "What would you like me to do?"
Score:    0.15 ❌ (completely different)
```

**Why Relaxed Threshold (0.8)?**
- LLMs vary phrasing naturally
- Multiple valid response formats
- Semantic meaning matters more than exact wording

#### 2. tool_trajectory_avg_score (0.0 - 1.0)

**Measures**: Tool usage correctness (right tools, right parameters)

**Calculation**: Exact match of tool names and arguments

**Interpretation**:
- `1.0` ✅ Perfect match (tool + all args correct)
- `0.7` ⚠️ Partial match (some args wrong)
- `0.0` ❌ No match (wrong tool or not called)

**Example**:
```python
Expected: set_device_status(location='living_room', device='lights', status='on')
Actual:   set_device_status(location='living_room', device='lights', status='on')
Score:    1.0 ✅ (exact match)

Actual:   set_device_status(location='bedroom', device='lights', status='on')
Score:    0.67 ⚠️ (1 of 3 args wrong)

Actual:   No tool called
Score:    0.0 ❌ (tool not used)
```

**Why Strict Threshold (1.0)?**
- Tools have real-world side effects
- Wrong parameters cause problems
- Better to fail test than execute wrong action

### Evalset Format

Test cases are stored in `*.evalset.json` files:

```json
{
  "eval_set_id": "home_automation_integration_suite",
  "eval_cases": [
    {
      "eval_id": "test_turn_on_lights",
      "conversation": [
        {
          "user_content": {
            "parts": [{"text": "Turn on the living room lights"}]
          },
          "final_response": {
            "parts": [{"text": "The living room lights are now on."}]
          },
          "intermediate_data": {
            "tool_uses": [
              {
                "name": "set_device_status",
                "args": {
                  "location": "living_room",
                  "device_id": "lights",
                  "status": "on"
                }
              }
            ]
          }
        }
      ]
    }
  ]
}
```

**Key Fields**:
- `eval_id`: Unique test identifier
- `user_content`: User's input query
- `final_response`: Expected agent response
- `intermediate_data.tool_uses`: Expected tool calls (optional)

### Test Configuration

Define pass/fail thresholds in `test_config.json`:

```json
{
  "criteria": {
    "response_match_score": 0.8,
    "tool_trajectory_avg_score": 1.0
  }
}
```

## Evaluation Workflow

### 1. Create Test Cases

```python
from utils import create_eval_case, create_evalset, save_evalset

# Create individual test case
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

# Create evalset with multiple cases
evalset = create_evalset(
    eval_set_id="integration_suite",
    eval_cases=[test_case, ...]
)

# Save to file
save_evalset(evalset, "agent/integration.evalset.json")
```

### 2. Configure Thresholds

```python
from utils import create_test_config, save_test_config

config = create_test_config(
    response_match_threshold=0.8,
    tool_trajectory_threshold=1.0
)

save_test_config(config, "agent/test_config.json")
```

### 3. Run Evaluation

```bash
# Basic evaluation
adk eval <agent_dir> <evalset_file>

# With configuration
adk eval home_automation_agent \
         home_automation_agent/integration.evalset.json \
         --config_file_path=home_automation_agent/test_config.json

# With detailed output
adk eval home_automation_agent \
         home_automation_agent/integration.evalset.json \
         --config_file_path=home_automation_agent/test_config.json \
         --print_detailed_results
```

### 4. Analyze Results

```python
from utils import analyze_results, print_evaluation_summary

# Load and analyze results
analysis = analyze_results("integration.evalset.json.results")

# Print summary
print_evaluation_summary(analysis, test_config)
```

**Results File Structure**:
```json
{
  "eval_set_id": "home_automation_integration_suite",
  "eval_cases": [
    {
      "eval_id": "test_turn_on_lights",
      "pass": true,
      "conversation": [
        {
          "user_content": {...},
          "final_response": {...},
          "intermediate_data": {...},
          "metrics": {
            "response_match_score": 0.92,
            "tool_trajectory_avg_score": 1.0
          }
        }
      ]
    }
  ]
}
```

### 5. Fix and Iterate

Common failure patterns and fixes:

#### Low Response Match Score

**Symptom**: `response_match_score: 0.45`, `tool_trajectory_avg_score: 1.0`

**Root Causes**:
- Agent using different phrasing
- Missing information in response
- Wrong format

**Fix**: Update agent instructions with specific format

```python
# BEFORE (vague)
instruction = "You control smart home devices. Be helpful."

# AFTER (specific)
instruction = """
You are a home automation assistant.

RESPONSE FORMAT (always use):
"The {location} {device} are now {status}."

Example:
User: "Turn on the living room lights"
You: "The living room lights are now on."
"""
```

#### Low Tool Trajectory Score

**Symptom**: `response_match_score: 0.95`, `tool_trajectory_avg_score: 0.33`

**Root Causes**:
- Wrong tool parameters
- Parameter extraction errors
- Tool not called

**Fix**: Improve tool descriptions and parameter formats

```python
def set_device_status(
    location: str,  # Use underscores: 'living_room', 'bed_room'
    device_id: str,  # Device type: 'lights', 'thermostat'
    status: str,     # State: 'on', 'off', or temperature
):
    """
    Control a smart home device.

    Examples:
        set_device_status('living_room', 'lights', 'on')
        set_device_status('bed_room', 'thermostat', '72')
    """
```

#### Both Scores Low

**Symptom**: `response_match_score: 0.25`, `tool_trajectory_avg_score: 0.0`

**Root Causes**:
- Agent didn't understand query
- Missing tools
- Poor instruction quality

**Fix**: Add examples and improve clarity

```python
instruction = """
You control smart home devices.

Example Interactions:

User: "Turn on the living room lights"
You: Call set_device_status('living_room', 'lights', 'on')
     Respond: "The living room lights are now on."

User: "Set bedroom temp to 72"
You: Call set_device_status('bed_room', 'thermostat', '72')
     Respond: "The bedroom thermostat has been set to 72 degrees."
"""
```

## Examples

### Example 1: Basic Evaluation Setup

Learn evaluation concepts, metrics, and workflow:

```bash
python examples/example_1_basic_evaluation.py
```

**Covers**:
- Evaluation vs testing comparison
- Understanding response_match_score and tool_trajectory_avg_score
- Score interpretation guidelines
- Evaluation workflow steps
- File structure requirements

### Example 2: Creating Test Cases

Design comprehensive evalsets:

```bash
python examples/example_2_test_cases.py
```

**Covers**:
- Test case anatomy
- Creating evalsets programmatically
- Writing test configurations
- Test design best practices
- Coverage strategies

**Output**: Creates `demo_agent/` directory with sample evalset and config

### Example 3: Running Evaluations

Execute evaluations with CLI:

```bash
python examples/example_3_running_evaluations.py
```

**Covers**:
- `adk eval` command syntax
- Command options and flags
- Understanding console output
- Reading results files
- Common evaluation scenarios

### Example 4: Analyzing and Fixing Failures

Debug and improve failing agents:

```bash
python examples/example_4_analysis_and_fixes.py
```

**Covers**:
- Reading and analyzing results
- Common failure patterns
- Systematic debugging approach
- Fixing instructions and tools
- Iterative improvement workflow
- Regression prevention

### Example 5: Home Automation Agent

Hands-on practice with real agent:

```bash
# Create the agent
python create_home_agent.py

# Navigate to agent directory
cd home_automation_agent

# Add your API key to .env
nano .env

# Run evaluation
adk eval . integration.evalset.json \
  --config_file_path=test_config.json \
  --print_detailed_results

# Compare with fixed version
# See agent_fixed.py for solution
```

**The Agent**:
- Controls smart home devices (lights, thermostats)
- Has intentional flaws for learning
- Includes 5 test cases
- Provides fixed version for comparison

**Expected Results**:
- Initial evaluation: Some tests fail
- Identify: Vague responses, parameter issues
- Fix: Update instructions and tool descriptions
- Re-evaluate: Achieve 100% pass rate

## Test Case Design Best Practices

### ✅ DO

1. **Use Descriptive IDs**
   ```python
   ✅ eval_id="test_turn_on_living_room_lights"
   ❌ eval_id="test1"
   ```

2. **Test One Behavior Per Case**
   ```python
   ✅ Separate tests for 'turn on' and 'turn off'
   ❌ Combined test for multiple unrelated actions
   ```

3. **Cover Positive AND Negative Cases**
   ```python
   ✅ Test valid inputs AND error scenarios
   ❌ Only test happy path
   ```

4. **Use Realistic Queries**
   ```python
   ✅ "Turn on the living room lights"
   ❌ "execute set_device_status()"
   ```

5. **Specify Exact Responses**
   ```python
   ✅ "The living room lights are now on."
   ❌ "ok" or "success"
   ```

6. **Include All Tool Parameters**
   ```python
   ✅ All required args specified
   ❌ Missing location or device_id
   ```

### ❌ DON'T

- Make tests dependent on each other
- Test multiple unrelated behaviors in one case
- Use vague expected responses
- Forget to test error cases
- Hardcode API keys or secrets in evalsets

### Test Coverage Matrix

| Category | Examples |
|----------|----------|
| Happy Path | Valid inputs, expected tool calls |
| Edge Cases | Empty inputs, extreme values |
| Error Handling | Invalid locations, unknown devices |
| Multi-step | Complex queries requiring reasoning |
| Ambiguous | Vague instructions needing clarification |
| Tool Selection | Right tool from multiple options |

## Organizing Evalsets

For larger projects:

```
agent_directory/
├── agent.py
├── test_config.json              # Shared configuration
├── integration.evalset.json      # End-to-end tests
├── unit.evalset.json             # Individual tool tests
├── regression.evalset.json       # Bug prevention tests
└── performance.evalset.json      # Speed/efficiency tests
```

Run specific suites:
```bash
# Run integration tests
adk eval agent integration.evalset.json --config_file_path=test_config.json

# Run regression tests
adk eval agent regression.evalset.json --config_file_path=test_config.json
```

## Troubleshooting

### Low Scores Despite Correct Behavior

**Problem**: Agent works correctly but scores are low

**Solutions**:
1. Check expected response phrasing matches agent style
2. Adjust thresholds if semantically correct:
   ```json
   {
     "criteria": {
       "response_match_score": 0.7  // Lowered from 0.8
     }
   }
   ```
3. Standardize response format in agent instructions

### Tool Parameters Not Matching

**Problem**: `tool_trajectory_avg_score` is 0.67 or lower

**Common Causes**:
- Inconsistent parameter formatting (spaces vs underscores)
- Missing parameters
- Wrong data types (string vs number)

**Solution**:
1. Review tool descriptions for clarity
2. Add examples to instructions
3. Ensure consistent parameter formats

### Tests Pass Locally, Fail in CI/CD

**Causes**:
- Different Python/package versions
- Missing environment variables
- API rate limiting

**Solutions**:
1. Pin package versions in `requirements.txt`
2. Set environment variables in CI/CD
3. Add retry logic or delays between tests

### Agent Refuses to Help

**Problem**: "I cannot help with that request" responses

**Causes**:
- Tool not available to agent
- Unclear capability description
- Overly restrictive safety instructions

**Solutions**:
1. Verify tools are passed to agent
2. Improve tool descriptions
3. Add capability examples to instructions

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Agent Evaluation

on: [push, pull_request]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run evaluation
        env:
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
        run: |
          cd home_automation_agent
          adk eval . integration.evalset.json \
            --config_file_path=test_config.json

      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: evaluation-results
          path: home_automation_agent/*.results
```

## Resources

- **Google ADK Documentation**: https://ai.google.dev/adk
- **Evaluation Guide**: https://ai.google.dev/adk/evaluation
- **Get API Key**: https://aistudio.google.com/app/apikey
- **Kaggle Course**: https://www.kaggle.com/learn-guide/5-day-genai

## What's Next?

After mastering agent evaluation:

1. **Day 5 - Advanced Topics**: Explore advanced agent patterns and production deployment
2. **Build Your Own Agent**: Apply evaluation to your projects
3. **CI/CD Integration**: Automate evaluation in your deployment pipeline
4. **A/B Testing**: Compare different agent versions systematically

## Summary

- ✅ Evaluation = Systematic quality measurement for AI agents
- ✅ Two metrics: `response_match_score` + `tool_trajectory_avg_score`
- ✅ Workflow: Create → Configure → Run → Analyze → Fix
- ✅ Use `adk eval` CLI for batch testing
- ✅ Iterate until 100% pass rate
- ✅ Prevent regressions with comprehensive test suites

Happy agent testing! 🧪
