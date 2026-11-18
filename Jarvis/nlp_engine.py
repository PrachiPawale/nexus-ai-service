import re
from datetime import datetime, timedelta


class NexusNLP:

    def process_command(self, text: str):

        command = text.lower().strip()

        result = {
            "success": True,
            "original_text": text,
            "intent": "unknown",
            "module": "unknown",
            "entities": {},
            "response": ""
        }

        # -------------------------
        # MODULE DETECTION
        # -------------------------

        if re.search(r"\b(tasks?|todos?|to-dos?)\b", command):
            module = "task"

        elif re.search(r"\b(notes?)\b", command):
            module = "note"

        elif re.search(r"\b(goals?)\b", command):
            module = "goal"

        elif re.search(
            r"\b(calendar|meeting|meetings|event|events|schedule)\b",
            command
        ):
            module = "calendar"

        else:
            module = "unknown"

        result["module"] = module

        # -------------------------
        # INTENT DETECTION
        # -------------------------

        if re.search(
            r"\b(create|add|make|write|set|book|schedule)\b",
            command
        ):
            intent = "create"

        elif re.search(
            r"\b(show|list|view|display|find|what|which|upcoming)\b",
            command
        ):
            intent = "show"

        elif re.search(
            r"\b(update|edit|change|modify|complete|finish|mark)\b",
            command
        ):
            intent = "update"

        elif re.search(
            r"\b(delete|remove|erase|cancel)\b",
            command
        ):
            intent = "delete"

        else:
            intent = "unknown"

        result["intent"] = intent

        # -------------------------
        # EXTRACT NUMBER
        # -------------------------

        number_match = re.search(
            r"\b(?:task|note|goal|event|meeting)\s+(\d+)\b",
            command
        )

        if number_match:
            result["entities"]["number"] = int(
                number_match.group(1)
            )

        # -------------------------
        # EXTRACT PROGRESS
        # -------------------------

        progress_match = re.search(
            r"\b(\d{1,3})\s*(?:percent|%)\b",
            command
        )

        if progress_match:
            progress = int(progress_match.group(1))

            if 0 <= progress <= 100:
                result["entities"]["progress"] = progress

        # -------------------------
        # EXTRACT DATE
        # -------------------------

        if "day after tomorrow" in command:
            target_date = datetime.now() + timedelta(days=2)

            result["entities"]["date"] = (
                target_date.strftime("%Y-%m-%d")
            )

        elif "tomorrow" in command:
            target_date = datetime.now() + timedelta(days=1)

            result["entities"]["date"] = (
                target_date.strftime("%Y-%m-%d")
            )

        elif "today" in command:
            result["entities"]["date"] = (
                datetime.now().strftime("%Y-%m-%d")
            )

        # -------------------------
        # RESPONSE
        # -------------------------

        if module == "unknown":
            response = "I could not identify the requested module."

        elif intent == "unknown":
            response = "I understood the module but not the action."

        else:
            response = f"I understood your request. Module: {module}. Action: {intent}."

        result["response"] = response

        return result


jarvis_nlp = NexusNLP()