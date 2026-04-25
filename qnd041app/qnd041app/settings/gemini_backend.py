import google.generativeai as genai


class GeminiBackend:
    def __init__(self, config):
        self.model_id = config.get("MODEL_ID", "gemini-1.5-flash")
        self.api_key = config.get("API_KEY")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_id)

    def complete(self, prompt, **kwargs):
        response = self.model.generate_content(prompt)
        return response.text