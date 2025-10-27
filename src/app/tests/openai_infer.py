from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.getenv("MODAL_API_KEY"))
    
    # Set the base URL for the OpenAI-compatible API
    client.base_url = "https://v-ibe--cook-assistant-v1-serve.modal.run/v1"
    
    # Get the available model
    model = client.models.list().data[0]
    model_id = model.id
    print(f"Using model: {model_id}")
    # Create messages with system and user roles
    messages = [
        {"role": "system", "content": "You are a helpful assistant that generates recipe samples from a given set of ingredients."},
    {"role": "user", "content": "Generate a recipe using the following ingredients: eggs, milk, flour, sugar, butter. Include a title and clear steps."},
        
    ]
    
    # Display the conversation history
    print(f"\nConversation History:")
    for message in messages:
        if message["role"] == "user":
            print(f"User: {message['content']}")
        elif message["role"] == "assistant":
            print(f"Assistant: {message['content']}")
    
    # Get the completion from the API
    response = client.chat.completions.create(
        model=model_id,
        messages=messages,
        temperature=1,
        # max_tokens=512,
        stream=False,
        # top_p=0.8,
        seed=48,
        # extra_body={
        #     "min_p":0,
        #     "top_k": 20,
        # }
    )
    
    # Display the new assistant's response
    assistant_message = response.choices[0].message.content
    
    if "</think>" in assistant_message:
            # Split by closing tag and take everything after it
            assistant_message = assistant_message.split("</think>", 1)[-1].lstrip()
    print(f"Assistant: {assistant_message}")

if __name__ == "__main__":
    main()