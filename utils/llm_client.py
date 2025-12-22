from openai import OpenAI
import time

class GroqClient:
    def __init__(self, api_key, model_name):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )
        self.model_name = model_name

    def generate_response(self, messages, temperature=0.7):
        """
        Generates a response from the Groq API with basic rate limiting.
        """
        try:
            # Fixed delay to prevent rate limits
            time.sleep(2) 
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error communicating with LLM: {str(e)}"
