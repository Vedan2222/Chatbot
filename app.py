from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS  # Required for CORS handling
from langchain_community.llms import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

# Replace with your OpenAI API Key
OPENAI_API_KEY = "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"

# Function to connect to PostgreSQL
def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="chatbot_db",  # Change if needed
        user="postgres",  # Replace with your PostgreSQL username
        password="vrp103@gmail.com"  # Replace with your PostgreSQL password
    )

# Summarize supplier data using LangChain and OpenAI
def summarize_supplier_data(supplier_data):
    llm = OpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY)
    prompt = f"Summarize the following supplier data:\n{supplier_data}"
    return llm(prompt)

# Query database to retrieve product and supplier information
def query_database(user_query):
    conn = connect_db()
    cursor = conn.cursor()

    # Handling query for fetching all products under a specific brand
    if "products" in user_query and "brand" in user_query:
        brand_name = user_query.split("brand")[-1].strip()
        cursor.execute("""
            SELECT name, price, category FROM products WHERE brand ILIKE %s
        """, (f"%{brand_name}%",))
        results = cursor.fetchall()
        if not results:
            return f"No products found under brand {brand_name}."
        response = [f"Product: {name}, Price: ${price}, Category: {category}" for name, price, category in results]
        return response
    
    # Handling query for fetching all products without brand filter
    if "show me all products" in user_query:
        cursor.execute("""
            SELECT name, price, category FROM products
        """)
        results = cursor.fetchall()
        if not results:
            return "No products found."
        response = [f"Product: {name}, Price: ${price}, Category: {category}" for name, price, category in results]
        return response

    
    # Handling query for fetching details of a specific product
    if "details of product" in user_query:
        product_name = user_query.split("product")[-1].strip()
        cursor.execute("""
            SELECT name, price, description FROM products WHERE name ILIKE %s
        """, (f"%{product_name}%",))
        results = cursor.fetchall()
        if not results:
            return f"No details found for product {product_name}."
        response = [f"Product: {name}, Price: ${price}, Description: {description}" for name, price, description in results]
        return response
    
    if "give me details of" in user_query:
        product_name = user_query.split("details of")[-1].strip()
        cursor.execute("""
            SELECT name, brand, price, category, description FROM products WHERE name ILIKE %s
        """, (f"%{product_name}%",))
        results = cursor.fetchall()
        if not results:
            return f"No product found with name {product_name}."
        name, brand, price, category, description = results[0]
        response = {
            "Product Name": name,
            "Brand": brand,
            "Price": f"${price}",
            "Category": category,
            "Description": description
        }
        return response

    if "supplier" in user_query and "product" in user_query:
        product_name = user_query.split("product")[-1].strip()
        cursor.execute("""
            SELECT s.name FROM suppliers s
            JOIN products p ON s.id = p.supplier_id
            WHERE p.name ILIKE %s
        """, (f"%{product_name}%",))
        results = cursor.fetchall()
        if not results:
            return f"No supplier found for product {product_name}."
        response = [f"Supplier: {supplier}" for supplier in results]
        return response

    cursor.close()
    conn.close()
    return "Sorry, I couldn't understand your query."

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("query", "")
    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    # Convert the query to lowercase to make the process case-insensitive
    user_query = user_query.lower()

    # Query the database
    db_response = query_database(user_query)
    
    # Optionally summarize or enhance the response using LangChain if required
    if isinstance(db_response, list):
        response_text = "\n".join(db_response)
    else:
        # Enhance the response using LangChain's OpenAI model
        llm = OpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY)
        response_text = llm(f"Enhance this response: {db_response}")
    
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)
