"""
Script to create home automation agent with intentional flaws.

This script creates a complete agent directory structure:
- agent.py: Agent definition with tools
- integration.evalset.json: Test cases
- test_config.json: Evaluation configuration

The agent has intentional issues for learning purposes:
1. Vague response format (low response_match_score)
2. Missing examples (fails on complex queries)

Run this script to create the agent:
    python create_home_agent.py

Then evaluate it:
    cd home_automation_agent
    adk eval . integration.evalset.json --config_file_path=test_config.json --print_detailed_results
"""

import json
import os
from pathlib import Path


def create_agent_file():
    """Create agent.py with intentional flaws."""
    agent_code = '''"""
Home Automation Agent

A simple agent for controlling smart home devices.
This version has intentional flaws for learning evaluation debugging.

Flaws:
1. Vague response format (causes low response_match_score)
2. Missing location format examples (causes tool parameter errors)
"""

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini


def set_device_status(location: str, device_id: str, status: str) -> dict:
    """
    Control a smart home device.

    Args:
        location: Room name where the device is located
        device_id: Type of device (lights, thermostat, etc.)
        status: Desired status (on, off, or temperature value)

    Returns:
        dict: Success status and message
    """
    return {
        "success": True,
        "message": f"Successfully set the {device_id} in {location} to {status.lower()}.",
    }


# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# Create model
model = Gemini(model="gemini-2.0-flash-exp")

# INTENTIONAL FLAW 1: Vague instruction (causes response mismatch)
root_agent = LlmAgent(
    name="home_automation_assistant",
    model=model,
    tools=[set_device_status],
    instruction="""
    You are a home automation assistant that helps users control smart home devices.

    You can control lights and thermostats in different rooms.
    Be helpful and confirm actions.
    """,  # Missing: Specific response format, location format examples
)
'''

    return agent_code


def create_evalset():
    """Create integration.evalset.json with test cases."""
    evalset = {
        "eval_set_id": "home_automation_integration_suite",
        "eval_cases": [
            # Test 1: Turn on lights (will fail - response format issue)
            {
                "eval_id": "test_turn_on_living_room_lights",
                "conversation": [
                    {
                        "user_content": {
                            "parts": [{"text": "Turn on the living room lights"}]
                        },
                        "final_response": {
                            "parts": [
                                {"text": "The living room lights are now on."}
                            ]
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "set_device_status",
                                    "args": {
                                        "location": "living_room",
                                        "device_id": "lights",
                                        "status": "on",
                                    },
                                }
                            ]
                        },
                    }
                ],
            },
            # Test 2: Turn off lights (will fail - response format issue)
            {
                "eval_id": "test_turn_off_bedroom_lights",
                "conversation": [
                    {
                        "user_content": {
                            "parts": [{"text": "Turn off the bedroom lights"}]
                        },
                        "final_response": {
                            "parts": [{"text": "The bedroom lights are now off."}]
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "set_device_status",
                                    "args": {
                                        "location": "bedroom",
                                        "device_id": "lights",
                                        "status": "off",
                                    },
                                }
                            ]
                        },
                    }
                ],
            },
            # Test 3: Set thermostat (will fail - parameter format)
            {
                "eval_id": "test_set_thermostat_temperature",
                "conversation": [
                    {
                        "user_content": {
                            "parts": [
                                {
                                    "text": "Set the living room thermostat to 72 degrees"
                                }
                            ]
                        },
                        "final_response": {
                            "parts": [
                                {
                                    "text": "The living room thermostat has been set to 72 degrees."
                                }
                            ]
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "set_device_status",
                                    "args": {
                                        "location": "living_room",
                                        "device_id": "thermostat",
                                        "status": "72",
                                    },
                                }
                            ]
                        },
                    }
                ],
            },
            # Test 4: Info query (should pass - no tools needed)
            {
                "eval_id": "test_capability_query",
                "conversation": [
                    {
                        "user_content": {
                            "parts": [{"text": "What devices can you control?"}]
                        },
                        "final_response": {
                            "parts": [
                                {
                                    "text": "I can control lights and thermostats in different rooms of your home."
                                }
                            ]
                        },
                    }
                ],
            },
            # Test 5: Turn on kitchen lights (will likely fail)
            {
                "eval_id": "test_turn_on_kitchen_lights",
                "conversation": [
                    {
                        "user_content": {
                            "parts": [{"text": "Turn on the kitchen lights"}]
                        },
                        "final_response": {
                            "parts": [{"text": "The kitchen lights are now on."}]
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "set_device_status",
                                    "args": {
                                        "location": "kitchen",
                                        "device_id": "lights",
                                        "status": "on",
                                    },
                                }
                            ]
                        },
                    }
                ],
            },
        ],
    }

    return evalset


def create_test_config():
    """Create test_config.json."""
    config = {
        "criteria": {
            "response_match_score": 0.8,
            "tool_trajectory_avg_score": 1.0,
        }
    }

    return config


def create_fixed_agent():
    """Create agent_fixed.py with corrections."""
    fixed_code = '''"""
Home Automation Agent - FIXED VERSION

This version fixes the issues from the original agent.

Fixes:
1. Added specific response format template
2. Added location format examples
3. Improved tool descriptions
"""

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini


def set_device_status(location: str, device_id: str, status: str) -> dict:
    """
    Control a smart home device.

    Args:
        location: Room name (lowercase, no spaces): living_room, bedroom, kitchen
        device_id: Device type: lights, thermostat
        status: Desired status (on, off, or temperature value)

    Returns:
        dict: Success status and message

    Examples:
        set_device_status("living_room", "lights", "on")
        set_device_status("bedroom", "thermostat", "72")
    """
    return {
        "success": True,
        "message": f"Successfully set the {device_id} in {location} to {status.lower()}.",
    }


# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# Create model
model = Gemini(model="gemini-2.0-flash-exp")

# FIXED: Specific instruction with format and examples
root_agent = LlmAgent(
    name="home_automation_assistant",
    model=model,
    tools=[set_device_status],
    instruction="""
    You are a home automation assistant that controls smart home devices.

    IMPORTANT RULES:

    1. Response Format (ALWAYS use this exact format):
       "The {location} {device_id} are now {status}."

       Examples:
       - "The living room lights are now on."
       - "The bedroom lights are now off."
       - "The living room thermostat has been set to 72 degrees."

    2. Location Format (CRITICAL):
       - Use lowercase with underscores for multi-word rooms
       - "living room" → "living_room"
       - "bedroom" → "bedroom" (already one word)
       - "kitchen" → "kitchen"

    3. Device Types:
       - lights
       - thermostat

    4. Status Values:
       - For lights: "on" or "off"
       - For thermostat: temperature number as string (e.g., "72")

    Example Interactions:

    User: "Turn on the living room lights"
    You: Call set_device_status("living_room", "lights", "on")
         Respond: "The living room lights are now on."

    User: "Turn off the bedroom lights"
    You: Call set_device_status("bedroom", "lights", "off")
         Respond: "The bedroom lights are now off."

    User: "Set the living room thermostat to 72 degrees"
    You: Call set_device_status("living_room", "thermostat", "72")
         Respond: "The living room thermostat has been set to 72 degrees."
    """,
)
'''

    return fixed_code


def main():
    """Create the home automation agent directory structure."""
    print("\n" + "=" * 80)
    print("Creating Home Automation Agent")
    print("=" * 80)
    print()

    # Create directory
    agent_dir = Path("home_automation_agent")
    agent_dir.mkdir(exist_ok=True)

    print(f"✅ Created directory: {agent_dir}")
    print()

    # Create agent.py (with flaws)
    agent_path = agent_dir / "agent.py"
    with open(agent_path, "w") as f:
        f.write(create_agent_file())
    print(f"✅ Created: {agent_path}")
    print("   (Contains intentional flaws for learning)")
    print()

    # Create agent_fixed.py (fixed version)
    fixed_path = agent_dir / "agent_fixed.py"
    with open(fixed_path, "w") as f:
        f.write(create_fixed_agent())
    print(f"✅ Created: {fixed_path}")
    print("   (Fixed version for comparison)")
    print()

    # Create __init__.py (required for adk eval)
    init_path = agent_dir / "__init__.py"
    with open(init_path, "w") as f:
        f.write('"""\nHome Automation Agent Package\n"""\n\n')
        f.write("from .agent import root_agent\n\n")
        f.write('__all__ = ["root_agent"]\n')
    print(f"✅ Created: {init_path}")
    print("   (Makes agent directory a Python package)")
    print()

    # Create evalset
    evalset_path = agent_dir / "integration.evalset.json"
    with open(evalset_path, "w") as f:
        json.dump(create_evalset(), f, indent=2)
    print(f"✅ Created: {evalset_path}")
    print("   (5 test cases)")
    print()

    # Create test config
    config_path = agent_dir / "test_config.json"
    with open(config_path, "w") as f:
        json.dump(create_test_config(), f, indent=2)
    print(f"✅ Created: {config_path}")
    print("   (response_match: 0.8, tool_trajectory: 1.0)")
    print()

    # Create .env if it doesn't exist
    env_path = agent_dir / ".env"
    if not env_path.exists():
        with open(env_path, "w") as f:
            f.write("# Copy your GOOGLE_API_KEY here\n")
            f.write("GOOGLE_API_KEY=your_api_key_here\n")
        print(f"⚠️  Created: {env_path}")
        print("   (Remember to add your API key!)")
        print()

    # Print structure
    print("=" * 80)
    print("Directory Structure:")
    print("=" * 80)
    print()
    print("home_automation_agent/")
    print("├── __init__.py                 # Python package marker")
    print("├── agent.py                    # Broken version (for learning)")
    print("├── agent_fixed.py              # Fixed version (reference)")
    print("├── integration.evalset.json    # Test cases")
    print("├── test_config.json            # Evaluation thresholds")
    print("└── .env                        # API key (add yours!)")
    print()

    # Print next steps
    print("=" * 80)
    print("Next Steps:")
    print("=" * 80)
    print()
    print("1. Add your API key:")
    print(f"   $ nano {env_path}")
    print("   (Replace 'your_api_key_here' with your actual key)")
    print()
    print("2. Run evaluation on broken agent:")
    print("   $ cd home_automation_agent")
    print("   $ adk eval . integration.evalset.json \\")
    print("       --config_file_path=test_config.json \\")
    print("       --print_detailed_results")
    print()
    print("3. Observe failures:")
    print("   Expected: Some tests will fail due to:")
    print("   - Vague response format")
    print("   - Parameter format issues")
    print()
    print("4. Fix the agent:")
    print("   - Option A: Manually fix agent.py using examples from Example 4")
    print("   - Option B: Compare with agent_fixed.py to see the solution")
    print()
    print("5. Re-run evaluation:")
    print("   $ adk eval . integration.evalset.json \\")
    print("       --config_file_path=test_config.json \\")
    print("       --print_detailed_results")
    print()
    print("6. Verify improvement:")
    print("   Goal: 5/5 tests passing (100%)")
    print()
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
