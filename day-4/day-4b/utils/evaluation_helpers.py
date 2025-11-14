"""
Helper functions for agent evaluation examples.

Provides utilities for:
- Loading API keys
- Creating evalsets and test configurations
- Running evaluations
- Analyzing results
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv


def load_api_key() -> str:
    """
    Load Google API key from .env file.

    Returns:
        str: The API key

    Raises:
        ValueError: If GOOGLE_API_KEY is not set
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found in environment variables. "
            "Please create a .env file with your API key."
        )
    return api_key


def create_retry_config():
    """
    Create a retry configuration for API calls.

    Note: Retry configuration is now handled automatically by the SDK.
    This function is kept for backward compatibility.

    Returns:
        None: Retry options are configured automatically
    """
    # Retry configuration is now handled automatically by Google ADK
    return None


def create_evalset(
    eval_set_id: str,
    eval_cases: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Create an evalset structure.

    Args:
        eval_set_id: Unique identifier for the evalset
        eval_cases: List of evaluation cases

    Returns:
        Dict containing the evalset structure
    """
    return {
        "eval_set_id": eval_set_id,
        "eval_cases": eval_cases,
    }


def create_eval_case(
    eval_id: str,
    user_query: str,
    expected_response: str,
    expected_tools: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Create a single evaluation case.

    Args:
        eval_id: Unique identifier for this test case
        user_query: The user's input query
        expected_response: The expected agent response
        expected_tools: Optional list of expected tool calls

    Returns:
        Dict containing the evaluation case
    """
    conversation_turn = {
        "user_content": {"parts": [{"text": user_query}]},
        "final_response": {"parts": [{"text": expected_response}]},
    }

    if expected_tools:
        conversation_turn["intermediate_data"] = {"tool_uses": expected_tools}

    return {"eval_id": eval_id, "conversation": [conversation_turn]}


def save_evalset(evalset: Dict[str, Any], file_path: str) -> None:
    """
    Save evalset to a JSON file.

    Args:
        evalset: The evalset dictionary
        file_path: Path to save the evalset file
    """
    # Ensure directory exists
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(evalset, f, indent=2)


def load_evalset(file_path: str) -> Dict[str, Any]:
    """
    Load evalset from a JSON file.

    Args:
        file_path: Path to the evalset file

    Returns:
        Dict containing the evalset
    """
    with open(file_path, "r") as f:
        return json.load(f)


def create_test_config(
    response_match_threshold: float = 0.8,
    tool_trajectory_threshold: float = 1.0,
) -> Dict[str, Any]:
    """
    Create a test configuration.

    Args:
        response_match_threshold: Minimum score for response matching (0.0-1.0)
        tool_trajectory_threshold: Minimum score for tool trajectory (0.0-1.0)

    Returns:
        Dict containing the test configuration
    """
    return {
        "criteria": {
            "response_match_score": response_match_threshold,
            "tool_trajectory_avg_score": tool_trajectory_threshold,
        }
    }


def save_test_config(config: Dict[str, Any], file_path: str) -> None:
    """
    Save test configuration to a JSON file.

    Args:
        config: The test configuration dictionary
        file_path: Path to save the config file
    """
    # Ensure directory exists
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(config, f, indent=2)


def run_evaluation(
    agent_dir: str,
    evalset_file: str,
    config_file: Optional[str] = None,
    print_detailed: bool = True,
) -> subprocess.CompletedProcess:
    """
    Run evaluation using adk eval CLI.

    Args:
        agent_dir: Path to the agent directory
        evalset_file: Path to the evalset file
        config_file: Optional path to test config file
        print_detailed: Whether to print detailed results

    Returns:
        subprocess.CompletedProcess with evaluation results
    """
    cmd = ["adk", "eval", agent_dir, evalset_file]

    if config_file:
        cmd.extend(["--config_file_path", config_file])

    if print_detailed:
        cmd.append("--print_detailed_results")

    return subprocess.run(cmd, capture_output=True, text=True)


def analyze_results(results_file: str) -> Dict[str, Any]:
    """
    Analyze evaluation results from a results file.

    Args:
        results_file: Path to the results JSON file

    Returns:
        Dict containing analysis of results
    """
    with open(results_file, "r") as f:
        results = json.load(f)

    analysis = {
        "total_cases": len(results.get("eval_cases", [])),
        "passed": 0,
        "failed": 0,
        "failures": [],
        "avg_response_score": 0.0,
        "avg_tool_score": 0.0,
    }

    response_scores = []
    tool_scores = []

    for case in results.get("eval_cases", []):
        eval_id = case.get("eval_id", "unknown")
        passed = case.get("pass", False)

        if passed:
            analysis["passed"] += 1
        else:
            analysis["failed"] += 1
            # Extract failure reason
            metrics = case.get("conversation", [{}])[0].get("metrics", {})
            analysis["failures"].append(
                {
                    "eval_id": eval_id,
                    "response_score": metrics.get("response_match_score", 0.0),
                    "tool_score": metrics.get("tool_trajectory_avg_score", 0.0),
                }
            )

        # Collect scores
        metrics = case.get("conversation", [{}])[0].get("metrics", {})
        response_scores.append(metrics.get("response_match_score", 0.0))
        tool_scores.append(metrics.get("tool_trajectory_avg_score", 0.0))

    # Calculate averages
    if response_scores:
        analysis["avg_response_score"] = sum(response_scores) / len(response_scores)
    if tool_scores:
        analysis["avg_tool_score"] = sum(tool_scores) / len(tool_scores)

    return analysis


def print_evaluation_summary(
    analysis: Dict[str, Any],
    config: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Print a formatted summary of evaluation results.

    Args:
        analysis: Analysis dictionary from analyze_results()
        config: Optional test configuration for threshold display
    """
    print("\n" + "=" * 80)
    print("📊 EVALUATION SUMMARY")
    print("=" * 80)
    print()

    # Overall results
    total = analysis["total_cases"]
    passed = analysis["passed"]
    failed = analysis["failed"]
    pass_rate = (passed / total * 100) if total > 0 else 0

    print(f"Total Test Cases: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Pass Rate: {pass_rate:.1f}%")
    print()

    # Average scores
    print(f"Average Response Match Score: {analysis['avg_response_score']:.3f}")
    print(f"Average Tool Trajectory Score: {analysis['avg_tool_score']:.3f}")
    print()

    # Thresholds (if config provided)
    if config:
        criteria = config.get("criteria", {})
        print("Configured Thresholds:")
        print(f"  response_match_score: {criteria.get('response_match_score', 'N/A')}")
        print(
            f"  tool_trajectory_avg_score: {criteria.get('tool_trajectory_avg_score', 'N/A')}"
        )
        print()

    # Failures detail
    if analysis["failures"]:
        print("Failed Test Cases:")
        for failure in analysis["failures"]:
            print(f"  • {failure['eval_id']}")
            print(f"    Response Score: {failure['response_score']:.3f}")
            print(f"    Tool Score: {failure['tool_score']:.3f}")
        print()

    print("=" * 80)


def format_tool_calls(tool_uses: List[Dict[str, Any]]) -> str:
    """
    Format tool calls for display.

    Args:
        tool_uses: List of tool use dictionaries

    Returns:
        Formatted string representation
    """
    if not tool_uses:
        return "No tools used"

    formatted = []
    for tool in tool_uses:
        name = tool.get("name", "unknown")
        args = tool.get("args", {})
        formatted.append(f"{name}({', '.join(f'{k}={v}' for k, v in args.items())})")

    return "\n".join(formatted)


def calculate_score_color(score: float, threshold: float) -> str:
    """
    Determine color indicator for a score.

    Args:
        score: The actual score
        threshold: The threshold for passing

    Returns:
        String with color indicator (✅, ⚠️, ❌)
    """
    if score >= threshold:
        return "✅"
    elif score >= threshold * 0.8:
        return "⚠️"
    else:
        return "❌"
