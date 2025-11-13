"""
Helper functions for managing sessions and conversations.

This module provides reusable utilities for:
- Running conversational sessions
- Loading API keys
- Configuring retry options
"""

import os
from typing import Union, List
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.genai import types


def load_api_key() -> None:
    """
    Load Google API key from environment variables.

    Looks for GOOGLE_API_KEY in:
    1. Environment variables
    2. .env file in current directory

    Raises:
        ValueError: If API key is not found
    """
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found! Please:\n"
            "1. Copy .env.example to .env\n"
            "2. Add your API key to .env\n"
            "3. Get your key from: https://aistudio.google.com/app/apikey"
        )

    print("✅ API key loaded successfully")


def create_retry_config() -> types.HttpRetryOptions:
    """
    Create production-ready retry configuration for Gemini API calls.

    Returns:
        HttpRetryOptions configured for:
        - 5 retry attempts
        - Exponential backoff
        - Rate limit and server error handling
    """
    return types.HttpRetryOptions(
        attempts=5,  # Maximum retry attempts
        exp_base=7,  # Delay multiplier for exponential backoff
        initial_delay=1,  # Start with 1 second delay
        http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
    )


async def run_session(
    runner_instance: Runner,
    user_queries: Union[List[str], str, None] = None,
    session_name: str = "default",
    user_id: str = "default",
    model_name: str = "gemini-2.5-flash-lite",
) -> None:
    """
    Manage a complete conversation session with automatic history maintenance.

    This function handles:
    - Session creation or retrieval
    - Query processing with streaming responses
    - Conversation history management

    Args:
        runner_instance: The Runner managing the agent
        user_queries: Single query (str) or list of queries to process.
                     None to just show session info.
        session_name: Unique identifier for this session
        user_id: User identifier (default: "default")
        model_name: Name of the model for display (default: "gemini-2.5-flash-lite")

    Example:
        >>> await run_session(runner, "What is the capital of France?", "geography-session")
        >>> await run_session(runner, ["Hello!", "What's my name?"], "user-intro-session")
    """
    print(f"\n{'='*80}")
    print(f"📋 Session: {session_name}")
    print(f"{'='*80}")

    # Get session service from runner
    session_service = runner_instance.session_service

    # Get app name from the Runner
    app_name = runner_instance.app_name

    # Attempt to create a new session or retrieve an existing one
    try:
        session = await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_name
        )
        print(f"✅ Created new session")
    except Exception:
        session = await session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_name
        )
        print(f"♻️  Retrieved existing session")

    # Process queries if provided
    if user_queries:
        # Convert single query to list for uniform processing
        if isinstance(user_queries, str):
            user_queries = [user_queries]

        # Process each query in the list sequentially
        for query in user_queries:
            print(f"\n💬 User > {query}")
            print(f"{'-'*80}")

            # Convert the query string to the ADK Content format
            query_content = types.Content(
                role="user",
                parts=[types.Part(text=query)]
            )

            # Stream the agent's response asynchronously
            response_parts = []
            async for event in runner_instance.run_async(
                user_id=user_id,
                session_id=session.id,
                new_message=query_content
            ):
                # Check if the event contains valid content
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        # Filter out empty or "None" responses
                        if part.text and part.text.strip() and part.text != "None":
                            response_parts.append(part.text)

            # Print complete response
            if response_parts:
                full_response = " ".join(response_parts)
                print(f"🤖 {model_name} >\n{full_response}")
            else:
                print(f"🤖 {model_name} > (No text response)")

            print(f"{'-'*80}")
    else:
        print("\nℹ️  No queries provided - session ready for interaction")

    print(f"{'='*80}\n")


if __name__ == "__main__":
    print("✅ Session helper functions loaded successfully")
