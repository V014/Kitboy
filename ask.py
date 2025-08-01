import os
from dotenv import load_dotenv
import google.generativeai as genai

class AskKitboy:
    # Create function that handles prompts
    @staticmethod
    def prompt(prompt):
        # Load API key from .env
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            return "API key not found. Please set it in the .env file."

        genai.configure(api_key=api_key)

        # Create a generative model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        while True:
            # Check for exit commands
            if prompt.lower() in ["quit", "exit", "bye"]:
                break

            try:
                # Generate content
                response = model.generate_content(prompt)

                # Print the response
                return (f"{response.text}")

            except Exception as e:
                return (f"An error occurred: {e}")