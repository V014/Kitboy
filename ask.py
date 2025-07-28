import google.generativeai as genai

# Configure the API key
genai.configure(api_key="AIzaSyDMgJ_S82PNeMh8GJGs0DFWoQPzQ4ZZvDo")

# Create a generative model
model = genai.GenerativeModel('gemini-1.5-flash')

print("Google AI Chatbot. Type 'quit', 'exit', or 'bye' to end the conversation.")

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