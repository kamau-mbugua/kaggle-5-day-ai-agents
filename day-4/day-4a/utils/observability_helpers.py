"""
Helper functions for observability examples.

Functions:
- load_api_key(): Load Google API key from environment
- create_retry_config(): Create retry configuration
- setup_logging(): Configure logging with specified level
- cleanup_logs(): Remove old log files
- run_agent_with_logging(): Run agent and capture logs
- print_log_summary(): Display log file summary
"""

import os
import logging
from typing import Optional
from dotenv import load_dotenv
from google.genai import types
from google.adk.runners import InMemoryRunner


def load_api_key() -> str:
    """
    Load Google API key from .env file.

    Returns:
        str: The API key

    Raises:
        ValueError: If API key is not found
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found. Please create a .env file with your API key.\n"
            "Get your key from: https://aistudio.google.com/app/apikey"
        )

    return api_key


def create_retry_config() -> types.HttpRetryOptions:
    """
    Create HTTP retry configuration for API calls.

    Returns:
        HttpRetryOptions: Configured retry options with 5 attempts
    """
    return types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],
    )


def setup_logging(
    log_file: str = "agent.log",
    level: int = logging.INFO,
    format_string: Optional[str] = None,
) -> None:
    """
    Configure logging with specified level and format.

    Args:
        log_file: Path to log file
        level: Logging level (logging.DEBUG, INFO, WARNING, ERROR)
        format_string: Custom format string (optional)

    Example:
        setup_logging("debug.log", logging.DEBUG)
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Remove existing handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Configure logging
    logging.basicConfig(
        filename=log_file,
        level=level,
        format=format_string,
        force=True,
    )

    print(f"✅ Logging configured: {log_file} (Level: {logging.getLevelName(level)})")


def cleanup_logs(*log_files: str) -> None:
    """
    Remove old log files.

    Args:
        *log_files: Variable number of log file paths to remove

    Example:
        cleanup_logs("agent.log", "debug.log", "web.log")
    """
    removed_count = 0
    for log_file in log_files:
        if os.path.exists(log_file):
            os.remove(log_file)
            print(f"🧹 Cleaned up {log_file}")
            removed_count += 1

    if removed_count == 0:
        print("✓ No log files to clean up")
    else:
        print(f"✅ Cleaned up {removed_count} log file(s)")


async def run_agent_with_logging(
    runner: InMemoryRunner,
    query: str,
    user_id: str = "demo_user",
) -> str:
    """
    Run agent and display response with logging.

    Args:
        runner: InMemoryRunner instance
        query: User query
        user_id: User identifier

    Returns:
        str: Agent response

    Example:
        response = await run_agent_with_logging(runner, "Hello!")
    """
    print(f"\n{'=' * 80}")
    print(f"User > {query}")
    print("=" * 80)

    response_text = ""

    try:
        response = await runner.run_debug(query, user_id=user_id)
        response_text = response
        print(f"\nAgent > {response}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        logging.error(f"Agent execution failed: {e}", exc_info=True)
        response_text = f"ERROR: {str(e)}"

    print("=" * 80)

    return response_text


def print_log_summary(log_file: str, max_lines: int = 50) -> None:
    """
    Display summary of log file contents.

    Args:
        log_file: Path to log file
        max_lines: Maximum lines to display

    Example:
        print_log_summary("agent.log", max_lines=30)
    """
    print(f"\n{'=' * 80}")
    print(f"📋 Log Summary: {log_file}")
    print("=" * 80)

    if not os.path.exists(log_file):
        print(f"❌ Log file not found: {log_file}")
        return

    try:
        with open(log_file, "r") as f:
            lines = f.readlines()

        total_lines = len(lines)
        print(f"\nTotal log entries: {total_lines}")

        if total_lines == 0:
            print("(Empty log file)")
            return

        # Count by log level
        debug_count = sum(1 for line in lines if "DEBUG" in line)
        info_count = sum(1 for line in lines if "INFO" in line)
        warning_count = sum(1 for line in lines if "WARNING" in line)
        error_count = sum(1 for line in lines if "ERROR" in line)

        print(f"\nLog Level Distribution:")
        print(f"  DEBUG:   {debug_count}")
        print(f"  INFO:    {info_count}")
        print(f"  WARNING: {warning_count}")
        print(f"  ERROR:   {error_count}")

        # Show sample of logs
        print(f"\n--- First {min(max_lines, total_lines)} lines ---\n")
        for line in lines[:max_lines]:
            print(line.rstrip())

        if total_lines > max_lines:
            print(f"\n... and {total_lines - max_lines} more lines")

    except Exception as e:
        print(f"❌ Error reading log file: {e}")

    print("=" * 80)


def print_debugging_tips():
    """Print helpful debugging tips for observability."""
    print("\n" + "=" * 80)
    print("🔍 Debugging Tips")
    print("=" * 80)
    print()
    print("When debugging agent issues:")
    print()
    print("  1. Start with symptom → Look at final error/behavior")
    print("  2. Check logs → Search for ERROR or WARNING entries")
    print("  3. Find root cause → Trace back through DEBUG logs")
    print("  4. Fix and verify → Test with same input")
    print()
    print("Key things to look for in logs:")
    print()
    print("  • LLM Request: System instructions, available tools")
    print("  • LLM Response: Model output, function calls")
    print("  • Tool Calls: Arguments passed, results returned")
    print("  • Errors: Exception messages, stack traces")
    print()
    print("Log Levels:")
    print()
    print("  DEBUG   → Detailed diagnostic info (development)")
    print("  INFO    → General informational messages")
    print("  WARNING → Warning messages (potential issues)")
    print("  ERROR   → Error messages (failures)")
    print()
    print("=" * 80)
