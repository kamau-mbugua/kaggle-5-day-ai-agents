"""
MCP Integration - Connecting to External Services
Based on the Kaggle 5-Day Agents Course - Day 2b

This demonstrates how to connect your agent to external MCP (Model Context Protocol)
servers without writing custom integration code.

Key Concepts:
- MCP provides standardized interfaces to external services
- Use community-built integrations (GitHub, Slack, databases, etc.)
- Connect to multiple MCP servers in one agent
- No custom API client code needed

Requirements:
- Node.js and npx must be installed for stdio MCP servers
"""

import os
import asyncio
import base64
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from google.genai import types


def load_api_key():
    """Load the Google API key from environment variables."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "❌ GOOGLE_API_KEY not found. Please create a .env file with your API key.\n"
            "Get your API key from: https://aistudio.google.com/app/apikey"
        )

    os.environ["GOOGLE_API_KEY"] = api_key
    return api_key


def create_retry_config():
    """Create retry configuration for handling transient errors."""
    return types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504]
    )


def create_mcp_toolset():
    """
    Create MCP Toolset connection to the Everything MCP Server.

    The Everything MCP Server is a demo server that provides test tools
    including getTinyImage (returns a 16x16 pixel test image).

    In production, you would connect to real MCP servers like:
    - GitHub MCP Server (for repository operations)
    - Slack MCP Server (for messaging)
    - Database MCP Servers (for data access)
    - Google Maps MCP Server (for location services)

    Requirements:
        - Node.js and npx must be installed
        - The server package will be auto-installed via npx

    Returns:
        McpToolset: Configured connection to MCP server
    """

    print("📦 Setting up MCP connection...")
    print("   Server: @modelcontextprotocol/server-everything")
    print("   Tool: getTinyImage (demo image generator)")
    print("   ℹ️  Note: This requires Node.js and npx to be installed\n")

    mcp_toolset = McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",  # Use Node Package eXecute
                args=[
                    "-y",  # Auto-confirm installation
                    "@modelcontextprotocol/server-everything",
                ],
                tool_filter=["getTinyImage"],  # Only use this tool
            ),
            timeout=30,  # 30 second connection timeout
        )
    )

    print("✅ MCP Toolset created!\n")
    return mcp_toolset


def create_image_agent(retry_config, mcp_toolset):
    """
    Create an agent that uses MCP tools.

    The agent has access to the getTinyImage tool from the MCP server
    and can use it to generate test images.

    Args:
        retry_config: Retry configuration for the model
        mcp_toolset: MCP toolset with server connection

    Returns:
        LlmAgent: Agent with MCP tool integration
    """

    agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="image_agent",
        instruction="""You are an image generation assistant using MCP tools.

        When users request images:
        1. Use the getTinyImage tool from the MCP server
        2. Explain that this is a demo tool that generates a 16x16 test image
        3. Let the user know the image has been generated

        Be friendly and explain what MCP is if asked.
        """,
        tools=[mcp_toolset],
    )

    return agent


async def demo_mcp_integration():
    """Demonstrate MCP integration with an agent."""

    print("\n" + "="*80)
    print("🌐 MCP INTEGRATION - Connecting to External Services")
    print("="*80 + "\n")

    # Setup
    load_api_key()
    retry_config = create_retry_config()

    # Create MCP connection
    try:
        mcp_toolset = create_mcp_toolset()
    except Exception as e:
        print(f"\n❌ Error creating MCP toolset: {e}")
        print("\n⚠️  Make sure Node.js and npx are installed:")
        print("   - Check: npx --version")
        print("   - Install Node.js from: https://nodejs.org/")
        return

    # Create agent
    print("🤖 Creating image agent with MCP integration...")
    agent = create_image_agent(retry_config, mcp_toolset)
    print("✅ Agent created!\n")

    # Create runner
    runner = InMemoryRunner(agent=agent)

    # Test query
    query = "Can you provide a sample tiny image?"

    print(f"💬 Query: {query}\n")
    print("-"*80)

    try:
        response = await runner.run_debug(query, verbose=False)

        print("-"*80)

        # Try to extract and display the image
        print("\n📊 Checking for images in response...")
        images_found = False

        for event in response:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "function_response") and part.function_response:
                        for item in part.function_response.response.get("content", []):
                            if item.get("type") == "image":
                                images_found = True
                                print("✅ Image received from MCP server!")
                                print(f"   Format: Base64-encoded")
                                print(f"   Size: 16x16 pixels (demo image)")

                                # Show first few characters of base64 data
                                img_data = item["data"]
                                print(f"   Data preview: {img_data[:50]}...")

        if not images_found:
            print("ℹ️  No images found in response (agent may have responded with text only)")

    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        print("\nℹ️  Common issues:")
        print("   - Node.js/npx not installed")
        print("   - Network connection problems")
        print("   - MCP server installation failed")
    finally:
        # Cleanup MCP connection
        try:
            if hasattr(mcp_toolset, 'cleanup') and callable(mcp_toolset.cleanup):
                await mcp_toolset.cleanup()
        except Exception as cleanup_error:
            # Suppress cleanup errors to avoid obscuring the main error
            pass

    print("\n" + "="*80)
    print("💡 Key Takeaways:")
    print("="*80)
    print("1. MCP provides standardized interfaces to external services")
    print("2. No custom API client code needed")
    print("3. Use community-built integrations")
    print("4. Same pattern works for GitHub, Slack, databases, etc.")
    print("5. Easily scale by adding more MCP servers")
    print("="*80 + "\n")


async def main():
    """Main function."""
    try:
        await demo_mcp_integration()

        print("\n" + "="*80)
        print("🎯 About MCP Servers")
        print("="*80)
        print("\nMCP Architecture:")
        print("  Your Agent (MCP Client)")
        print("       ↓")
        print("  Standard MCP Protocol")
        print("       ↓")
        print("  ┌─────────┬──────────┬─────────┐")
        print("  │ GitHub  │  Slack   │  Maps   │")
        print("  │ Server  │  Server  │ Server  │")
        print("  └─────────┴──────────┴─────────┘")
        print("\n📚 More MCP Servers:")
        print("  • GitHub MCP - Repository operations")
        print("  • Kaggle MCP - Dataset/notebook operations")
        print("  • Slack MCP - Messaging integration")
        print("  • Database MCP - SQL operations")
        print("  • Find more: modelcontextprotocol.io/examples")
        print("="*80 + "\n")

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        # Give async cleanup tasks time to complete
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())
