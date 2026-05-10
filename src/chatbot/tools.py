"""
LLM Tool definitions for chatbot
"""

import json


def get_search_products_tool():
    """Define search_products tool for LLM"""
    return {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search for jewelry products in the database based on customer query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., 'gold rings', 'necklaces under 5000')",
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price filter (optional)",
                    },
                },
                "required": ["query"],
            },
        },
    }


def get_place_order_tool():
    """Define place_order tool for LLM"""
    return {
        "type": "function",
        "function": {
            "name": "place_order",
            "description": "Place an order for a jewelry product",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "integer", "description": "Product ID"},
                    "customer_name": {"type": "string", "description": "Customer name"},
                    "customer_address": {"type": "string", "description": "Delivery address"},
                },
                "required": ["product_id", "customer_name", "customer_address"],
            },
        },
    }


def get_helpline_tool():
    """Define get_helpline tool for LLM"""
    return {
        "type": "function",
        "function": {
            "name": "get_helpline",
            "description": "Get helpline contact information for complex issues",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_type": {
                        "type": "string",
                        "description": "Type of issue (returns, complaints, etc.)",
                    }
                },
                "required": ["issue_type"],
            },
        },
    }


def get_search_knowledge_base_tool():
    """Define search_knowledge_base tool for LLM"""
    return {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Search knowledge base for FAQs and product information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for knowledge base",
                    }
                },
                "required": ["query"],
            },
        },
    }


def get_all_tools():
    """Get all available tools"""
    return [
        get_search_products_tool(),
        get_place_order_tool(),
        get_helpline_tool(),
        get_search_knowledge_base_tool(),
    ]
