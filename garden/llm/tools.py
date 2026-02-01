"""
Tool definitions for Claude API.

Each tool corresponds to an action the system can take.
Tools use discrete action types (water_small, water_medium, water_large)
rather than parameterized amounts, matching the ActionType enum.
"""

TOOLS = [
    {
        "name": "water_small",
        "description": "Dispense a small amount of water (~10ml). Use for minor moisture adjustments.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "water_medium",
        "description": "Dispense a medium amount of water (~20ml). Use for moderate dryness.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "water_large",
        "description": "Dispense a large amount of water (~30ml). Use only for very dry soil.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "light_on",
        "description": "Turn on the grow light.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "light_off",
        "description": "Turn off the grow light.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "fan_on",
        "description": "Turn on the ventilation fan. Helps with temperature, humidity, and air circulation.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "fan_off",
        "description": "Turn off the ventilation fan.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "no_action",
        "description": "Do nothing. Use when conditions are acceptable or unclear.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]

# Map tool names to ActionType values
TOOL_TO_ACTION = {
    "water_small": "water_small",
    "water_medium": "water_medium",
    "water_large": "water_large",
    "light_on": "light_on",
    "light_off": "light_off",
    "fan_on": "fan_on",
    "fan_off": "fan_off",
    "no_action": "no_action",
}
