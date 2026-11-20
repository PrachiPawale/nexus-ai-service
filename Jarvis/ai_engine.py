from openai import OpenAI
from google import genai

from config import settings


class AIEngine:

    def __init__(self):

        self.provider = settings.AI_PROVIDER.lower()

        self.model = settings.AI_MODEL

        self.client = None

        # Initialize Gemini
        if self.provider == "gemini":

            if settings.GEMINI_API_KEY:

                self.client = genai.Client(
    api_key=settings.GEMINI_API_KEY,

    http_options={
        "timeout": 30000
    }
)

        # Initialize OpenAI
        elif self.provider == "openai":

            if settings.AI_API_KEY:

                self.client = OpenAI(
                    api_key=settings.AI_API_KEY
                )

    # JARVIS System Instructions
    def get_instructions(self):

        return """
        You are JARVIS, the intelligent AI assistant of Nexus.

    Personality:
    - Intelligent, professional, friendly and futuristic.
    - Communicate naturally and confidently.

    Responsibilities:
    - Answer general questions.
    - Help manage tasks, schedules, notes and goals.
    - Provide productivity suggestions.
    - Help users organize their day.

    Response rules:
    - Answer directly.
    - Keep simple answers short.
    - Avoid unnecessary explanations.
    - Use detailed explanations only when needed.
    - Never invent Nexus operations.
    - Never claim an operation succeeded unless Nexus confirms it.
    """

    # Generate AI Response
    def generate_response(self, prompt, context=None):

        if not prompt or not prompt.strip():

            return {
                "success": False,
                "message": "Please enter a valid message."
            }

        if not self.client:

            return {
                "success": False,
                "message": "AI provider is not configured.",
                "provider": self.provider
            }

        try:

            instructions = self.get_instructions()

            if context:

                prompt = f"""
                Previous conversation:
                {context}

                Current user message:
                {prompt}
                """

            # GEMINI
            if self.provider == "gemini":

                response = self.client.models.generate_content(

                    model=self.model,

                    contents=prompt,

                    config={
                        "system_instruction": instructions,
                        "temperature": 0.7
                    }
                )

                answer = response.text

            # OPENAI
            elif self.provider == "openai":

                response = self.client.responses.create(

                    model=self.model,

                    instructions=instructions,

                    input=prompt
                )

                answer = response.output_text

            else:

                return {
                    "success": False,
                    "message": "Unsupported AI provider."
                }

            if not answer:

                return {
                    "success": False,
                    "message": "AI returned an empty response."
                }

            return {
                "success": True,
                "provider": self.provider,
                "model": self.model,
                "response": answer
            }

        except Exception as e:

            error_message = str(e)

            if "503" in error_message:
                message = "JARVIS is temporarily busy. Please try again shortly."

            elif "429" in error_message:
                message = "AI usage limit reached. Please check your API quota."

            elif "401" in error_message or "403" in error_message:
                message = "AI authentication failed. Please check your API key."

            else:
                message = "Unable to generate AI response."

        return {
        "success": False,
        "message": message,
        "error": error_message,
        "provider": self.provider
    }


# Initialize AI Engine
ai_engine = AIEngine()


# Public Function
def generate_response(prompt, context=None):

    return ai_engine.generate_response(
        prompt,
        context
    )