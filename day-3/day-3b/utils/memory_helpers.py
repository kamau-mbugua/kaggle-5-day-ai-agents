"""
Helper functions for memory management examples.

Functions:
- load_api_key(): Load Google API key from environment
- create_retry_config(): Create retry configuration
- run_session(): Run a complete session with queries
- display_memory_contents(): Display all memories in memory service
- display_search_results(): Display search results in formatted way
"""

import os
from typing import Union, List
from dotenv import load_dotenv
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import BaseSessionService
from google.adk.memory import BaseMemoryService


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


async def run_session(
    runner_instance: Runner,
    user_queries: Union[List[str], str, None] = None,
    session_id: str = "default",
    user_id: str = "default",
    app_name: str = "MemoryDemoApp",
    session_service: BaseSessionService = None,
) -> None:
    """
    Run a complete conversation session with one or more queries.

    Args:
        runner_instance: The Runner instance to use
        user_queries: Single query string or list of queries
        session_id: Unique identifier for the session
        user_id: User identifier
        app_name: Application name
        session_service: Session service instance

    Example:
        await run_session(
            runner,
            ["Hi, I'm Sam", "What's my name?"],
            session_id="test-123"
        )
    """
    print(f"\n### Session: {session_id}")

    # Create or retrieve session
    if session_service:
        try:
            session = await session_service.create_session(
                app_name=app_name, user_id=user_id, session_id=session_id
            )
        except:
            session = await session_service.get_session(
                app_name=app_name, user_id=user_id, session_id=session_id
            )

    # Convert single query to list
    if isinstance(user_queries, str):
        user_queries = [user_queries]

    # Process each query
    if user_queries:
        for query in user_queries:
            print(f"\nUser > {query}")
            query_content = types.Content(role="user", parts=[types.Part(text=query)])

            # Stream agent response
            async for event in runner_instance.run_async(
                user_id=user_id, session_id=session_id, new_message=query_content
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    text = event.content.parts[0].text
                    if text and text != "None":
                        print(f"Agent > {text}")


async def display_memory_contents(
    memory_service: BaseMemoryService,
    app_name: str,
    user_id: str,
    max_display: int = 10,
) -> None:
    """
    Display all memories stored in the memory service.

    Args:
        memory_service: Memory service instance
        app_name: Application name
        user_id: User identifier
        max_display: Maximum number of memories to display

    Example:
        await display_memory_contents(memory_service, "MyApp", "user123")
    """
    # Search with empty query to get all memories
    search_response = await memory_service.search_memory(
        app_name=app_name, user_id=user_id, query=""
    )

    print(f"\n💾 Memory Contents:")
    print(f"  Total memories: {len(search_response.memories)}")
    print()

    if not search_response.memories:
        print("  (No memories stored yet)")
        return

    for i, memory in enumerate(search_response.memories[:max_display]):
        if memory.content and memory.content.parts:
            text = memory.content.parts[0].text[:80]
            print(f"  [{i+1}] {memory.author}: {text}...")

    if len(search_response.memories) > max_display:
        print(f"\n  ... and {len(search_response.memories) - max_display} more")


async def display_search_results(
    memory_service: BaseMemoryService,
    app_name: str,
    user_id: str,
    query: str,
    max_display: int = 5,
) -> None:
    """
    Search memory and display results in formatted way.

    Args:
        memory_service: Memory service instance
        app_name: Application name
        user_id: User identifier
        query: Search query
        max_display: Maximum results to display

    Example:
        await display_search_results(
            memory_service,
            "MyApp",
            "user123",
            "favorite color"
        )
    """
    search_response = await memory_service.search_memory(
        app_name=app_name, user_id=user_id, query=query
    )

    print(f'\n🔍 Search Results for: "{query}"')
    print(f"  Found {len(search_response.memories)} relevant memories")
    print()

    if not search_response.memories:
        print("  (No matching memories found)")
        return

    for i, memory in enumerate(search_response.memories[:max_display]):
        if memory.content and memory.content.parts:
            text = memory.content.parts[0].text[:100]
            print(f"  [{i+1}] {memory.author}: {text}...")

    if len(search_response.memories) > max_display:
        print(f"\n  ... and {len(search_response.memories) - max_display} more results")
