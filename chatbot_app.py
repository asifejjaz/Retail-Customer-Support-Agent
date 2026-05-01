import streamlit as st
import sqlite3
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
DB_PATH = os.path.join(os.path.dirname(__file__), 'jewelry_store.db')

client = OpenAI(
    api_key=API_KEY,
)

# Database Helpers
def search_products(query: str, max_price: float = None) -> str:
    """Searches the jewelry database for products matching the query."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    sql = "SELECT id, name, category, price, stock FROM products WHERE (name LIKE ? OR category LIKE ?)"
    params = [f"%{query}%", f"%{query}%"]
    
    if max_price:
        sql += " AND price <= ?"
        params.append(max_price)
        
    cursor.execute(sql, params)
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return "No products found matching your criteria."
    
    formatted = "Found the following products:\n"
    for r in results:
        formatted += f"- ID: {r[0]}, Name: {r[1]}, Category: {r[2]}, Price: £{r[3]}, Stock: {r[4]}\n"
    return formatted

def place_order(product_id: int, customer_name: str, customer_address: str) -> str:
    """Places an order for a product."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check stock
    cursor.execute("SELECT stock, name FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    
    if not product:
        conn.close()
        return "Error: Product ID not found."
        
    stock, name = product
    if stock <= 0:
        conn.close()
        return f"Sorry, the {name} is currently out of stock."
        
    # Place order
    cursor.execute(
        "INSERT INTO orders (product_id, customer_name, customer_address, status) VALUES (?, ?, ?, ?)",
        (product_id, customer_name, customer_address, "Processing")
    )
    
    # Update stock
    cursor.execute("UPDATE products SET stock = stock - 1 WHERE id = ?", (product_id,))
    
    conn.commit()
    order_id = cursor.lastrowid
    conn.close()
    
    return f"Order successfully placed for {name}! Your Order ID is {order_id}."

def get_helpline(issue_type: str) -> str:
    """Provides contact details for returns or other complex issues."""
    return "For returns or complex inquiries, please contact our helpline at 1-800-NASHAD (1-800-627-423) or email support@nashadjewellers.com."

# Tools schema for OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search the jewelry store database for products.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search term, e.g., 'ring', 'necklace', 'gold', 'diamond'."
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price the user is willing to pay. Omit if not specified."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "place_order",
            "description": "Place an order for a customer. Requires product ID, name, and address.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "integer",
                        "description": "The ID of the product to order."
                    },
                    "customer_name": {
                        "type": "string",
                        "description": "Full name of the customer."
                    },
                    "customer_address": {
                        "type": "string",
                        "description": "Shipping address for the order."
                    }
                },
                "required": ["product_id", "customer_name", "customer_address"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_helpline",
            "description": "Get contact information for store returns or complex issues.",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_type": {
                        "type": "string",
                        "description": "Brief description of the issue, e.g., 'return', 'complaint'."
                    }
                },
                "required": ["issue_type"]
            }
        }
    }
]

# Streamlit App
st.set_page_config(page_title="Nashad Jewellers Assistant", page_icon="💎")

st.title("💎 Nashad Jewellers Assistant")
st.markdown("Welcome to Nashad Jewellers! How can we make your day sparkle?")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a welcoming and highly empathetic customer service assistant for Nashad Jewellers. Introduce yourself briefly when saying hello. Explain that you can help customers search for beautiful jewelry (rings, bracelets, necklaces) and assist them in placing orders. Always match the user's emotional tone and use emojis if the user does to make them feel understood. You can search products, take orders, and refer complex issues or returns to the helpline."}
    ]

# Display chat messages (skip system prompt)
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
                model=MODEL,
                messages=st.session_state.messages,
                tools=tools,
                tool_choice="auto",
            )
            
            response_message = response.choices[0].message
            
            # Check for function calls
            if response_message.tool_calls:
                st.session_state.messages.append(response_message)
                
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    if function_name == "search_products":
                        function_response = search_products(**function_args)
                    elif function_name == "place_order":
                        function_response = place_order(**function_args)
                    elif function_name == "get_helpline":
                        function_response = get_helpline(**function_args)
                    else:
                        function_response = "Unknown function call."
                        
                    st.session_state.messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    })
                
                # Second response after function calls
                second_response = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                )
                final_content = second_response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": final_content})
                message_placeholder.markdown(final_content)
                
            else:
                final_content = response_message.content
                st.session_state.messages.append({"role": "assistant", "content": final_content})
                message_placeholder.markdown(final_content)
                
        except Exception as e:
            if "401" in str(e) or "User not found" in str(e):
                error_msg = "⚠️ **API Key Error:** The OpenRouter API key provided is returning a 'User not found' error. Please verify your key on the OpenRouter dashboard.\n\n*Mock Response: Yes, I can certainly help you find the perfect bracelet today! 😊*"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                message_placeholder.markdown(error_msg)
            else:
                st.error(f"Error communicating with API: {str(e)}")
