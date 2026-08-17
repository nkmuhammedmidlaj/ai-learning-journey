import json
from google import genai


def calculate(a, b):
    return a * b


client = genai.Client()

tool = {
    "type": "function",
    "name": "calculate",
    "description": "Multiplies two numbers.",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"}
        },
        "required": ["a", "b"]
    }
}

prompt = input("Ask: ")

response = client.interactions.create(
    model="gemini-3.6-flash",
    input=prompt,
    tools=[tool]
)

# Get Gemini's function call
function_call = next(
    step for step in response.steps
    if step.type == "function_call"
)

# Execute the Python function
if function_call.name == "calculate":

    args = function_call.arguments

    result = calculate(
        args["a"],
        args["b"]
    )

    print("\nPython calculated:", result)

    # Send the result back to Gemini
    final_response = client.interactions.create(
        model="gemini-3.6-flash",
        previous_interaction_id=response.id,
        input=[
            {
                "type": "function_result",
                "name": function_call.name,
                "call_id": function_call.id,
                "result": [
                    {
                        "type": "text",
                        "text": json.dumps(result)
                    }
                ]
            }
        ]
    )

    print("\nGemini:")
    print(final_response.output_text)