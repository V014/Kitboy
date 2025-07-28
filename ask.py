import google.generativeai as genai
import os

# Configure the API key
# genai.configure(api_key="API_KEY_HERE")
genai.configure(api_key=os.read("assets/api/api_config.txt").strip())

# Create a generative model
model = genai.GenerativeModel('gemini-1.5-flash')

while True:
    # Get prompt from user
    prompt = input("You: ")

    # Check for exit commands
    if prompt.lower() in ["quit", "exit", "bye"]:
        break

    try:
        # Generate content
        response = model.generate_content(prompt)

        # Print the response
        print(f"AI: {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

print("Conversation ended.")