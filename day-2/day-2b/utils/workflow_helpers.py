"""
Workflow Helper Functions for Long-Running Operations

These functions help process events, detect approval requests,
and handle the pause/resume flow in long-running agent operations.
"""

from google.genai import types


def check_for_approval(events):
    """
    Check if events contain an approval request (adk_request_confirmation).

    This function loops through all events looking for the special
    adk_request_confirmation event that signals the agent has paused
    and is waiting for human approval.

    Args:
        events: List of events from agent execution

    Returns:
        dict: Contains 'approval_id' and 'invocation_id' if approval needed
        None: If no approval request found

    Example:
        approval_info = check_for_approval(events)
        if approval_info:
            print(f"Pausing at invocation {approval_info['invocation_id']}")
    """
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if (
                    part.function_call
                    and part.function_call.name == "adk_request_confirmation"
                ):
                    return {
                        "approval_id": part.function_call.id,
                        "invocation_id": event.invocation_id,
                    }
    return None


def print_agent_response(events):
    """
    Extract and print agent's text responses from events.

    Args:
        events: List of events from agent execution

    Example:
        print_agent_response(events)
        # Output: Agent > Order completed successfully!
    """
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"Agent > {part.text}")


def create_approval_response(approval_info, approved):
    """
    Create an approval response message to resume the agent.

    Takes the approval information and human decision (True/False)
    and creates a properly formatted FunctionResponse that ADK
    understands for resuming execution.

    Args:
        approval_info: Dict with 'approval_id' from check_for_approval()
        approved: Boolean - True to approve, False to reject

    Returns:
        types.Content: Formatted response ready to send back to agent

    Example:
        approval_info = check_for_approval(events)
        response = create_approval_response(approval_info, True)
        # Pass this response when resuming with run_async()
    """
    confirmation_response = types.FunctionResponse(
        id=approval_info["approval_id"],
        name="adk_request_confirmation",
        response={"confirmed": approved},
    )
    return types.Content(
        role="user", parts=[types.Part(function_response=confirmation_response)]
    )


def extract_image_from_events(events):
    """
    Extract base64-encoded images from MCP tool responses.

    Args:
        events: List of events from agent execution

    Returns:
        list: List of base64-encoded image data strings

    Example:
        images = extract_image_from_events(events)
        for img_data in images:
            display(Image(data=base64.b64decode(img_data)))
    """
    images = []
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "function_response") and part.function_response:
                    for item in part.function_response.response.get("content", []):
                        if item.get("type") == "image":
                            images.append(item["data"])
    return images


# Test functions if run directly
if __name__ == "__main__":
    print("Workflow Helper Functions")
    print("=" * 50)
    print("\nAvailable functions:")
    print("  • check_for_approval(events) - Detect approval requests")
    print("  • print_agent_response(events) - Display agent text")
    print("  • create_approval_response(info, approved) - Format approval")
    print("  • extract_image_from_events(events) - Get images from MCP tools")
