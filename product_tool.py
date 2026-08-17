import json
from google import genai


products = {
    "iphone 16": 70000,
    "macbook": 100000,
    "airpods": 20000
}


def get_product_price(product):
    return products.get(product.lower(), "Product not found")


client = genai.Client()

tool = {
    "type": "function",
    "name": "get_product_price",
    "description": "Gets the price of a product from the product database.",
    "parameters": {
        "type": "object",
        "properties": {
            "product": {"type": "string"}
        },
        "required": ["product"]
    }
}

prompt = input("Ask: ")

response = client.interactions.create(
    model="gemini-3.6-flash",
    input=prompt,
    tools=[tool]
)

# Find ALL function calls
function_calls = [
    step for step in response.steps
    if step.type == "function_call"
]

results = []

# Execute every requested function
for call in function_calls:

    if call.name == "get_product_price":

        product = call.arguments["product"]
        price = get_product_price(product)

        print(f"\nDatabase result: {product} = {price}")

        results.append({
            "type": "function_result",
            "name": call.name,
            "call_id": call.id,
            "result": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "product": product,
                        "price": price,
                        "currency": "INR"
                    })
                }
            ]
        })


# Send ALL results back to Gemini
final_response = client.interactions.create(
    model="gemini-3.6-flash",
    previous_interaction_id=response.id,
    input=results
)

print("\nGemini:")
print(final_response.output_text)