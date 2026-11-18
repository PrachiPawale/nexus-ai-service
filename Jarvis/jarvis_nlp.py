import re


class JarvisNLP:

    def __init__(self):
        self.modules = [
            "task",
            "note",
            "goal",
            "calendar"
        ]

    # Identify the action
    def detect_action(self, text):

        text = text.lower()

        actions = {
            "create": ["create", "add", "make", "schedule", "new"],
            "update": ["update", "edit", "change", "modify"],
            "delete": ["delete", "remove", "cancel"],
            "list": ["show", "list", "display", "view", "get"],
            "complete": ["complete", "finish", "done", "mark as completed"]
        }

        for action, keywords in actions.items():
            for keyword in keywords:
                if re.search(r"\b" + re.escape(keyword) + r"\b", text):
                    return action

        return "unknown"

    # Identify the module
    def detect_module(self, text):

        text = text.lower()

        # Goals first to avoid confusing goal updates with note updates
        modules = {
            "goal": ["goal", "goals", "target", "targets"],
            "task": ["task", "tasks", "todo", "to-do"],
            "note": ["note", "notes", "memo", "memos"],
            "calendar": [
                "calendar",
                "event",
                "events",
                "meeting",
                "meetings",
                "appointment",
                "appointments"
            ]
        }

        for module, keywords in modules.items():
            for keyword in keywords:
                if re.search(r"\b" + re.escape(keyword) + r"\b", text):
                    return module

        return "unknown"

    # Extract content from command
    def extract_content(self, text):

        patterns = [
            r"\b(?:about|called|named|titled)\s+(.+)",
            r"\bto\s+(.+)",
            r"\bthat\s+(.+)"
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                return match.group(1).strip()

        return text.strip()

    # Main command processor
    def process_command(self, command):

        if not command or not command.strip():
            return {
                "success": False,
                "message": "Please provide a command."
            }

        command = command.strip()

        action = self.detect_action(command)
        module = self.detect_module(command)
        content = self.extract_content(command)

        if module == "unknown":
            return {
                "success": False,
                "message": "I could not identify the Nexus module.",
                "input": command
            }

        if action == "unknown":
            return {
                "success": False,
                "message": "I could not identify the requested action.",
                "module": module
            }

        return {
            "success": True,
            "module": module,
            "action": action,
            "content": content,
            "original_command": command,
            "message": f"JARVIS identified a {action} request for {module}."
        }


# Initialize NLP engine
jarvis = JarvisNLP()


# Function called by main.py
def process_command(command):

    return jarvis.process_command(command)