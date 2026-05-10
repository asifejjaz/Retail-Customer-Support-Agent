"""
Main Streamlit chatbot application
"""

import streamlit as st
import os
import json
from pathlib import Path

# Add project root to path for imports
import sys

# Add root directory to path (three levels up from app.py)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.settings import get_config
from src.database.db import DatabaseManager
from src.utils.helpers import extract_price_from_query
from src.chatbot.tools import get_all_tools
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load configuration
config = get_config()

# Initialize clients and managers
client = OpenAI(api_key=config.OPENAI_API_KEY)

# Database path
db_path = os.path.join(config.DB_PATH, config.DB_NAME)
db_manager = DatabaseManager(db_path)


def display_product_grid(products):
    """Display products in a grid layout with 3 items per row"""
    if not products:
        return

    # Create rows of 3 columns each
    for i in range(0, len(products), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(products):
                product = products[i + j]
                with cols[j]:
                    if product["image_url"]:
                        st.image(product["image_url"], width=150, caption=product["name"])
                    st.write(f"**£{product['price']}**")
                    st.write(f"Category: {product['category']}")
                    st.write(f"Stock: {product['stock']}")
                    if st.button(
                        f"View Details - ID: {product['id']}",
                        key=f"view_{product['id']}",
                    ):
                        st.markdown(f"[Buy Now]({product['product_url']})")
                        st.write(f"Description: {product['description']}")


def search_products_action(query: str, max_price: float = None) -> str:
    """Search for products and return formatted response"""
    products = db_manager.search_products(query, max_price, limit=9)

    if not products:
        return "No products found matching that description."

    return "GRID_DISPLAY:" + json.dumps(products)


def main():
    """Main chatbot application"""
    st.set_page_config(page_title=config.APP_TITLE, page_icon=config.APP_ICON)

    st.title(config.APP_TITLE)
    st.markdown("Welcome to Nashad Jewellers! How can we make your day sparkle?")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": "You are a welcoming and highly empathetic customer service assistant for Nashad Jewellers. Introduce yourself briefly when saying hello. Explain that you can help customers search for beautiful jewelry (rings, bracelets, necklaces) and assist them in placing orders. Always match the user's emotional tone. IMPORTANT: Only use emojis in your responses if the user has used emojis in their message; otherwise, your default mode must be completely emoji-free. When products are searched, they will be displayed in a grid automatically - do not describe individual products or use any image syntax. You can search products, take orders, and refer complex issues or returns to the helpline. CRITICAL: For any user query related to finding, browsing, or inquiring about jewelry products (e.g., 'show me rings', 'gold necklaces under 5000'), ALWAYS use the search_products function. Extract the relevant search terms from the query as the 'query' parameter (e.g., 'gold rings'). If a price limit is mentioned (e.g., 'under 10000'), use it as 'max_price'. If the query is too vague, use a broad term like 'jewelry' or ask for clarification in your response before searching. Never refuse to help with product searches; always attempt to search using the tools available.",
            }
        ]

    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask me about our jewelry..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            try:
                response = client.chat.completions.create(
                    model=config.OPENAI_MODEL,
                    messages=st.session_state.messages,
                    tools=get_all_tools(),
                    tool_choice="auto",
                )

                response_message = response.choices[0].message

                # Handle tool calls
                if response_message.tool_calls:
                    tool_calls_dict = [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in response_message.tool_calls
                    ]
                    st.session_state.messages.append(
                        {
                            "role": response_message.role,
                            "content": response_message.content,
                            "tool_calls": tool_calls_dict,
                        }
                    )

                    for tool_call in tool_calls_dict:
                        function_name = tool_call["function"]["name"]
                        function_args = json.loads(tool_call["function"]["arguments"])

                        if function_name == "search_products":
                            function_response = search_products_action(**function_args)
                            if function_response.startswith("GRID_DISPLAY:"):
                                grid_data = function_response.split("GRID_DISPLAY:", 1)[
                                    1
                                ]
                                try:
                                    products = json.loads(grid_data)
                                    display_product_grid(products)
                                    function_response = f"Found {len(products)} products matching your search. They're displayed in the grid above."
                                except json.JSONDecodeError:
                                    pass

                        st.session_state.messages.append(
                            {
                                "tool_call_id": tool_call["id"],
                                "role": "tool",
                                "name": function_name,
                                "content": function_response,
                            }
                        )

                    # Get final response
                    second_response = client.chat.completions.create(
                        model=config.OPENAI_MODEL,
                        messages=st.session_state.messages,
                    )
                    final_content = second_response.choices[0].message.content
                    st.session_state.messages.append(
                        {"role": "assistant", "content": final_content}
                    )
                    message_placeholder.markdown(final_content)

                else:
                    final_content = response_message.content
                    st.session_state.messages.append(
                        {"role": "assistant", "content": final_content}
                    )
                    message_placeholder.markdown(final_content)

            except Exception as e:
                st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
