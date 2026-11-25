from typing import Dict, List
from openai import OpenAI

def generate_response(openai_key: str, user_message: str, context: str, 
                     conversation_history: List[Dict], model: str = "gpt-4.1-mini") -> str:
    """Generate response using OpenAI with context"""

    # TODO: Define system prompt
    system_prompt = """
    You are a helpful NASA mission intelligence assistant.
    Answer the user's question using the provided NASA context.
    If the context does not contain enough information to answer
    the question, clearly say that you do not have enough information.
    Do not invent facts.
    """
    # TODO: Set context in messages
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "system",
            "content": f"NASA mission context:\n{context}"
        }
    ]
    # TODO: Add chat history
    messages.extend(conversation_history)
    # Add current user question
    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )
    # TODO: Create OpenAI Client
    client = OpenAI(api_key=openai_key)
    # TODO: Send request to OpenAI
    response = client.chat.completions.create(
    model=model,
        messages=messages,
        temperature=0.2
    )
    # TODO: Return response
    return response.choices[0].message.content
    pass