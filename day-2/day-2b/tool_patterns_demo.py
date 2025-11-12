"""
Tool Patterns - Interactive Demo
Based on the Kaggle 5-Day Agents Course - Day 2b

Explore advanced tool patterns:
1. MCP Integration - Connect to external services
2. Long-Running Operations - Pause for human approval

Note: MCP examples require Node.js and npx to be installed.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("\n" + "="*80)
print("🧰 TOOL PATTERNS & BEST PRACTICES - Interactive Demo")
print("="*80)
print("\nThis demo showcases advanced agent tool patterns:")
print("\n1️⃣  MCP Integration")
print("   - Connect to external services via Model Context Protocol")
print("   - Use community-built integrations")
print("   - No custom API client code needed")
print("   - Requires: Node.js and npx installed")
print("\n2️⃣  Long-Running Operations")
print("   - Pause agent execution for human approval")
print("   - Resume with saved state")
print("   - Perfect for financial transactions, bulk operations")
print("\n" + "="*80)
print("\n📋 Choose which pattern to explore:\n")
print("   1. MCP Integration Example")
print("   2. Long-Running Operations Example")
print("   3. Run Both (Full Demo)")
print("   4. Exit\n")
print("="*80)

choice = input("\nEnter your choice (1-4): ").strip()

if choice == "1":
    print("\n🌐 Running MCP Integration Example...")
    print("="*80 + "\n")
    os.system("python examples/1_mcp_integration.py")

elif choice == "2":
    print("\n⏳ Running Long-Running Operations Example...")
    print("="*80 + "\n")
    os.system("python examples/2_long_running_operations.py")

elif choice == "3":
    print("\n🎯 Running Full Demo (Both Patterns)...")
    print("\n" + "="*80)
    print("PART 1: MCP Integration")
    print("="*80 + "\n")
    os.system("python examples/1_mcp_integration.py")

    input("\n\n⏸️  Press Enter to continue to Part 2...")

    print("\n" + "="*80)
    print("PART 2: Long-Running Operations")
    print("="*80 + "\n")
    os.system("python examples/2_long_running_operations.py")

elif choice == "4":
    print("\n👋 Goodbye!\n")
else:
    print("\n❌ Invalid choice. Please run again and select 1-4.\n")
