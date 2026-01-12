#!/usr/bin/env python3
"""Test script for the LangGraph workflow"""

import sys
import os
sys.path.append('.')

from workflow.graph import graph
from models.patient import PatientData
from langchain_core.messages import HumanMessage

def test_routing():
    """Test the routing functionality"""
    print("Testing routing logic...")

    # Test cases
    test_cases = [
        ("I have chest pain", "emergency"),
        ("I'm feeling anxious", "mental_health"),
        ("I have a headache", "general"),
        ("I think I broke my arm", "emergency"),
        ("I need therapy", "mental_health"),
        ("I have a sore throat", "general")
    ]

    for message, expected_ward in test_cases:
        # Create initial state
        initial_state = {
            "messages": [HumanMessage(content=message)],
            "patient_data": PatientData().model_dump(),
            "current_node": "router",
            "session_id": "test_session"
        }

        # Only test the router node
        from workflow.graph import router_node
        result = router_node(initial_state)

        # Check routing
        actual_ward = result["patient_data"].get("ward")
        status = "PASS" if actual_ward == expected_ward else "FAIL"
        print(f"{status}: '{message}' -> {actual_ward} (expected: {expected_ward})")

    print("\nRouting test completed!")

def test_data_collection():
    """Test data collection flow"""
    print("\nTesting data collection flow...")

    # Test individual ward node logic instead of full graph
    from workflow.graph import emergency_ward_node

    # Initial state after routing
    initial_state = {
        "messages": [HumanMessage(content="I have chest pain")],
        "patient_data": {
            "patient_name": None,
            "patient_age": None,
            "patient_query": "I have chest pain",
            "ward": "emergency"
        },
        "current_node": "emergency_ward",
        "session_id": "test_collection"
    }

    print("Initial state: Missing all fields except query")

    # Test asking for name
    result1 = emergency_ward_node(initial_state)
    ai_messages = [msg for msg in result1["messages"] if msg.__class__.__name__ == 'AIMessage']
    print(f"AI asks: '{ai_messages[-1].content}'")

    # User provides name
    state_with_name = {
        **result1,
        "messages": result1["messages"] + [HumanMessage(content="John Doe")]
    }
    result2 = emergency_ward_node(state_with_name)
    ai_messages = [msg for msg in result2["messages"] if msg.__class__.__name__ == 'AIMessage']
    print(f"AI asks: '{ai_messages[-1].content}'")

    # User provides age
    state_with_age = {
        **result2,
        "messages": result2["messages"] + [HumanMessage(content="35")]
    }
    result3 = emergency_ward_node(state_with_age)
    ai_messages = [msg for msg in result3["messages"] if msg.__class__.__name__ == 'AIMessage']
    print(f"AI responds: '{ai_messages[-1].content}'")

    print(f"Final current_node: {result3['current_node']}")
    print("\nData collection test completed!")

if __name__ == "__main__":
    test_routing()
    test_data_collection()