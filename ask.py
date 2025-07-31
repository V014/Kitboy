import google.generativeai as genai

class AskKitboy:
    # Create function that handles prompts
    @staticmethod
    def prompt(prompt):

        # Configure the API key
        genai.configure(api_key="AIzaSyDMgJ_S82PNeMh8GJGs0DFWoQPzQ4ZZvDo")

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