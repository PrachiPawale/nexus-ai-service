from datetime import datetime

class ConversationMemory:

    def __init__(self, max_messages=20):
        self.conversations = {}
        self.max_messages = max_messages

    def add_message(self, session_id, role, message):
        if session_id not in self.conversations:
            self.conversations[session_id] = []

        self.conversations[session_id].append({
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })

        # Keep only the latest messages
        self.conversations[session_id] = (
            self.conversations[session_id][-self.max_messages:]
        )

    def get_history(self, session_id):
        return self.conversations.get(session_id, [])

    def get_context(self, session_id):
        history = self.get_history(session_id)

        return "\n".join(
            f"{item['role']}: {item['message']}"
            for item in history
        )

    def clear_history(self, session_id):
        self.conversations.pop(session_id, None)

    def get_all_sessions(self):
        return list(self.conversations.keys())


conversation_memory = ConversationMemory()