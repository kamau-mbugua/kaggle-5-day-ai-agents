"""
Example 1: Basic Evaluation Setup

Demonstrates:
- What is agent evaluation vs testing
- Why evaluation matters for AI agents
- Understanding evaluation metrics
- The evaluation workflow

Key Concepts:
- response_match_score: Text similarity (0.0-1.0)
- tool_trajectory_avg_score: Tool usage correctness (0.0-1.0)
- Evalsets: JSON files with test cases
- Test configuration: Pass/fail thresholds

Run:
python examples/example_1_basic_evaluation.py
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import load_api_key


async def demo_basic_evaluation():
    """
    Demonstrate basic evaluation concepts.

    Shows:
    1. What is agent evaluation
    2. Why we need it
    3. Key evaluation metrics
    4. The evaluation workflow
    """
    print("\n" + "=" * 80)
    print("Example 1: Basic Evaluation Setup")
    print("=" * 80)

    # Demo 1: What is evaluation
    print("\n" + "-" * 80)
    print("DEMO 1: What is Agent Evaluation?")
    print("-" * 80)
    print()
    print("Traditional Software Testing:")
    print("  Input: divide(10, 0)")
    print("  Expected: ZeroDivisionError")
    print("  Result: ✅ Clear pass/fail")
    print()
    print("AI Agent Testing:")
    print("  Input: 'Find papers about transformers'")
    print("  Expected: ???")
    print("  Result: How do we measure quality?")
    print()
    print("💡 Agent Evaluation = Systematic quality assessment")
    print()
    print("Key Differences:")
    print("  • Traditional: Exact outputs")
    print("  • AI Agents: Semantic similarity")
    print()

    # Demo 2: Why evaluation matters
    print("-" * 80)
    print("DEMO 2: Why Evaluation Matters")
    print("-" * 80)
    print()
    print("Without Evaluation:")
    print("  ❌ Can't catch regressions")
    print("  ❌ No quality benchmarks")
    print("  ❌ Manual testing only")
    print("  ❌ No confidence in changes")
    print()
    print("With Evaluation:")
    print("  ✅ Automated quality checks")
    print("  ✅ Catch regressions early")
    print("  ✅ Measure improvements")
    print("  ✅ Deploy with confidence")
    print()
    print("Use Cases:")
    print("  • Pre-deployment validation")
    print("  • Regression testing during development")
    print("  • A/B testing different prompts")
    print("  • Comparing model versions")
    print()

    # Demo 3: Evaluation metrics
    print("-" * 80)
    print("DEMO 3: Understanding Evaluation Metrics")
    print("-" * 80)
    print()
    print("Two Core Metrics:")
    print()
    print("1. response_match_score (0.0 - 1.0)")
    print("   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("   Measures: Text similarity between expected and actual response")
    print()
    print("   Example:")
    print("   Expected:  'The lights in the living room are now on.'")
    print("   Actual:    'Living room lights have been turned on.'")
    print("   Score:     0.85 ✅ (semantically similar)")
    print()
    print("   Expected:  'The lights in the living room are now on.'")
    print("   Actual:    'I cannot help with that request.'")
    print("   Score:     0.12 ❌ (completely different)")
    print()
    print("2. tool_trajectory_avg_score (0.0 - 1.0)")
    print("   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("   Measures: Tool usage correctness (right tools, right parameters)")
    print()
    print("   Example:")
    print("   Expected:  set_device_status(location='living_room', device='lights', status='on')")
    print("   Actual:    set_device_status(location='living_room', device='lights', status='on')")
    print("   Score:     1.0 ✅ (perfect match)")
    print()
    print("   Expected:  set_device_status(location='living_room', device='lights', status='on')")
    print("   Actual:    set_device_status(location='bedroom', device='lights', status='on')")
    print("   Score:     0.67 ⚠️  (wrong location)")
    print()
    print("   Expected:  set_device_status(location='living_room', device='lights', status='on')")
    print("   Actual:    No tools called")
    print("   Score:     0.0 ❌ (tool not used)")
    print()

    # Demo 4: Score interpretation
    print("-" * 80)
    print("DEMO 4: Interpreting Scores")
    print("-" * 80)
    print()
    print("Typical Thresholds:")
    print()
    print("┌──────────────────────┬───────────────┬─────────────────────┐")
    print("│ Metric               │ Threshold     │ Interpretation      │")
    print("├──────────────────────┼───────────────┼─────────────────────┤")
    print("│ response_match_score │ ≥ 0.8         │ Semantically close  │")
    print("│ tool_trajectory_avg  │ = 1.0         │ Exact tool match    │")
    print("└──────────────────────┴───────────────┴─────────────────────┘")
    print()
    print("Why Strict Tool Matching?")
    print("  • Tools have side effects (turn on lights, send emails)")
    print("  • Wrong parameters can cause real problems")
    print("  • Better to fail test than execute wrong action")
    print()
    print("Why Relaxed Response Matching?")
    print("  • Multiple valid phrasings")
    print("  • LLMs vary output style")
    print("  • Semantic meaning matters more than exact wording")
    print()

    # Demo 5: Evaluation workflow
    print("-" * 80)
    print("DEMO 5: The Evaluation Workflow")
    print("-" * 80)
    print()
    print("Step-by-Step Process:")
    print()
    print("1️⃣  CREATE TEST CASES")
    print("   → Define user queries")
    print("   → Specify expected responses")
    print("   → List expected tool calls")
    print("   → Save as *.evalset.json")
    print()
    print("2️⃣  CONFIGURE THRESHOLDS")
    print("   → Set response_match_score threshold")
    print("   → Set tool_trajectory_avg_score threshold")
    print("   → Save as test_config.json")
    print()
    print("3️⃣  RUN EVALUATION")
    print("   → Use adk eval CLI command")
    print("   → Agent processes test cases")
    print("   → Scores calculated automatically")
    print("   → Results saved to *.results file")
    print()
    print("4️⃣  ANALYZE RESULTS")
    print("   → Review pass/fail status")
    print("   → Identify failure patterns")
    print("   → Compare expected vs actual")
    print("   → Plan fixes")
    print()
    print("5️⃣  FIX AND ITERATE")
    print("   → Update agent instructions")
    print("   → Fix tool implementations")
    print("   → Re-run evaluation")
    print("   → Verify improvements")
    print()

    # Demo 6: Evaluation file structure
    print("-" * 80)
    print("DEMO 6: Evaluation File Structure")
    print("-" * 80)
    print()
    print("Required Files:")
    print()
    print("1. Agent Directory")
    print("   home_automation_agent/")
    print("   ├── agent.py              # Agent definition")
    print("   ├── integration.evalset.json  # Test cases")
    print("   └── test_config.json      # Thresholds")
    print()
    print("2. Evalset Format (*.evalset.json)")
    print("   {")
    print('     "eval_set_id": "home_automation_integration_suite",')
    print('     "eval_cases": [')
    print("       {")
    print('         "eval_id": "test_turn_on_lights",')
    print('         "conversation": [')
    print("           {")
    print('             "user_content": {"parts": [{"text": "query"}]},')
    print('             "final_response": {"parts": [{"text": "expected"}]},')
    print('             "intermediate_data": {')
    print('               "tool_uses": [{"name": "tool", "args": {...}}]')
    print("             }")
    print("           }")
    print("         ]")
    print("       }")
    print("     ]")
    print("   }")
    print()
    print("3. Test Config Format (test_config.json)")
    print("   {")
    print('     "criteria": {')
    print('       "response_match_score": 0.8,')
    print('       "tool_trajectory_avg_score": 1.0')
    print("     }")
    print("   }")
    print()

    # Demo 7: CLI command
    print("-" * 80)
    print("DEMO 7: Running Evaluations with CLI")
    print("-" * 80)
    print()
    print("Basic Command:")
    print("  adk eval <agent_dir> <evalset_file>")
    print()
    print("With Configuration:")
    print("  adk eval home_automation_agent \\")
    print("           home_automation_agent/integration.evalset.json \\")
    print("           --config_file_path=home_automation_agent/test_config.json")
    print()
    print("With Detailed Output:")
    print("  adk eval home_automation_agent \\")
    print("           home_automation_agent/integration.evalset.json \\")
    print("           --config_file_path=home_automation_agent/test_config.json \\")
    print("           --print_detailed_results")
    print()
    print("Output Files:")
    print("  • *.evalset.json.results  → Full evaluation results")
    print("  • Console output          → Summary and detailed results")
    print()

    # Summary
    print("=" * 80)
    print("✅ Basic Evaluation Complete!")
    print("=" * 80)
    print()
    print("Key Takeaways:")
    print()
    print("  ✅ Evaluation = Systematic quality measurement")
    print("  ✅ Two metrics: response_match + tool_trajectory")
    print("  ✅ Workflow: Create → Configure → Run → Analyze → Fix")
    print("  ✅ Use adk eval CLI for batch testing")
    print()
    print("Next Steps:")
    print("  → Example 2: Create test cases and evalsets")
    print("  → Example 3: Run evaluations and analyze results")
    print("  → Example 4: Debug and fix failing agents")
    print()


if __name__ == "__main__":
    # Check for .env file
    if not os.path.exists(".env"):
        print("\n" + "=" * 80)
        print("⚠️  WARNING: .env file not found!")
        print("=" * 80)
        print()
        print("This example doesn't require an API key,")
        print("but you'll need one for Examples 2-4.")
        print()
        print("Setup:")
        print("1. Copy .env.example to .env")
        print("2. Add your GOOGLE_API_KEY to .env")
        print("3. Get your key from: https://aistudio.google.com/app/apikey")
        print()
        print("=" * 80 + "\n")

    asyncio.run(demo_basic_evaluation())
