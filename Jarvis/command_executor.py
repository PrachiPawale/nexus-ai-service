from backend_client import nexus_backend


class CommandExecutor:

    def __init__(self):
        self.user_id = 1

    def execute(self, command):

        if not command.get("success"):
            return {
                "success": False,
                "message": command.get("message")
            }

        module = command.get("module")
        action = command.get("action")
        content = command.get("content", "").strip()

        if action == "list":
            return self.list_records(module)

        elif action == "create":
            return self.create_record(module, content)

        return {
            "success": False,
            "message": f"{action} operation is not implemented yet."
        }

    # LIST OPERATIONS

    def list_records(self, module):

        operations = {
            "task": nexus_backend.get_tasks,
            "note": nexus_backend.get_notes,
            "goal": nexus_backend.get_goals,
            "calendar": nexus_backend.get_events
        }

        if module not in operations:
            return {
                "success": False,
                "message": "Unknown Nexus module."
            }

        result = operations[module](self.user_id)

        return self.handle_result(
            result,
            f"Here are your {module} records."
        )

    # CREATE OPERATIONS

    def create_record(self, module, content):

        if not content:
            return {
                "success": False,
                "message": "Please provide details to create a record."
            }

        if module == "task":

            data = {
                "user_id": self.user_id,
                "title": content,
                "status": "pending",
                "priority": "medium"
            }

            result = nexus_backend.create_task(data)

        elif module == "note":

            data = {
                "user_id": self.user_id,
                "title": "JARVIS Note",
                "content": content
            }

            result = nexus_backend.create_note(data)

        elif module == "goal":

            data = {
                "user_id": self.user_id,
                "title": content,
                "description": "",
                "progress": 0
            }

            result = nexus_backend.create_goal(data)

        elif module == "calendar":

            return {
                "success": False,
                "message": (
                    "Calendar creation requires a meeting date "
                    "and start time. We'll implement date extraction next."
                )
            }

        else:
            return {
                "success": False,
                "message": "Unknown Nexus module."
            }

        return self.handle_result(
            result,
            f"Your {module} was created successfully."
        )

    # COMMON RESPONSE HANDLER

    def handle_result(self, result, message):

        if not result.get("success"):
            return {
                "success": False,
                "message": "The Nexus operation failed.",
                "error": result.get("error")
                         or result.get("message")
            }

        return {
            "success": True,
            "message": message,
            "data": result.get("data")
        }


command_executor = CommandExecutor()


def execute_command(command):
    return command_executor.execute(command)