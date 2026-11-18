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
        You are JARVIS, the intelligent AI assistant
        of Nexus productivity platform.

        Your personality:

        - Intelligent
        - Professional
        - Friendly
        - Helpful
        - Futuristic

        Your responsibilities:

        1. Help users manage productivity.
        2. Assist with tasks and schedules.
        3. Help users organize notes.
        4. Help users manage personal goals.
        5. Suggest task priorities.
        6. Answer general questions.
        7. Provide productivity recommendations.
        8. Help users plan their day.

        Always provide clear and useful answers.

        Never claim that you have created, updated,
        or deleted something unless Nexus confirms
        that the operation was successful.
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