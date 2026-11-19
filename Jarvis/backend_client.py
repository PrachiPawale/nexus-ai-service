import requests
from config import settings


class NexusBackendClient:

    def __init__(self):
        self.base_url = settings.BACKEND_URL.rstrip("/")
        self.timeout = 15

    def request(self, method, endpoint, data=None, params=None):

        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )

            response.raise_for_status()

            if response.status_code == 204 or not response.content:
                return {
                    "success": True,
                    "data": None
                }

            return {
                "success": True,
                "data": response.json()
            }

        except requests.exceptions.HTTPError:

            try:
                error_data = response.json()
            except ValueError:
                error_data = response.text

            return {
                "success": False,
                "message": "Backend request failed",
                "status_code": response.status_code,
                "error": error_data
            }

        except requests.exceptions.ConnectionError:

            return {
                "success": False,
                "message": "Cannot connect to Nexus backend. Check whether Node.js server is running."
            }

        except requests.exceptions.Timeout:

            return {
                "success": False,
                "message": "Nexus backend request timed out."
            }

        except requests.exceptions.RequestException as e:

            return {
                "success": False,
                "message": "Unexpected backend communication error.",
                "error": str(e)
            }

    # TASK OPERATIONS

    def get_tasks(self, user_id):
        return self.request(
            "GET", "/api/tasks",
            params={"user_id": user_id}
        )

    def get_task(self, task_id, user_id):
        return self.request(
            "GET", f"/api/tasks/{task_id}",
            params={"user_id": user_id}
        )

    def create_task(self, task_data):
        return self.request("POST", "/api/tasks", data=task_data)

    def update_task(self, task_id, task_data):
        return self.request("PUT", f"/api/tasks/{task_id}", data=task_data)

    def delete_task(self, task_id, user_id):
        return self.request(
            "DELETE", f"/api/tasks/{task_id}",
            params={"user_id": user_id}
        )

    # NOTE OPERATIONS

    def get_notes(self, user_id):
        return self.request(
            "GET", "/api/notes",
            params={"user_id": user_id}
        )

    def get_note(self, note_id, user_id):
        return self.request(
            "GET", f"/api/notes/{note_id}",
            params={"user_id": user_id}
        )

    def create_note(self, note_data):
        return self.request("POST", "/api/notes", data=note_data)

    def update_note(self, note_id, note_data):
        return self.request("PUT", f"/api/notes/{note_id}", data=note_data)

    def delete_note(self, note_id, user_id):
        return self.request(
            "DELETE", f"/api/notes/{note_id}",
            params={"user_id": user_id}
        )

    # GOAL OPERATIONS

    def get_goals(self, user_id):
        return self.request(
            "GET", "/api/goals",
            params={"user_id": user_id}
        )

    def get_goal(self, goal_id, user_id):
        return self.request(
            "GET", f"/api/goals/{goal_id}",
            params={"user_id": user_id}
        )

    def create_goal(self, goal_data):
        return self.request("POST", "/api/goals", data=goal_data)

    def update_goal(self, goal_id, goal_data):
        return self.request("PUT", f"/api/goals/{goal_id}", data=goal_data)

    def delete_goal(self, goal_id, user_id):
        return self.request(
            "DELETE", f"/api/goals/{goal_id}",
            params={"user_id": user_id}
        )

    # CALENDAR OPERATIONS

    def get_events(self, user_id):
        return self.request(
            "GET", "/api/calendar",
            params={"user_id": user_id}
        )

    def get_event(self, event_id, user_id):
        return self.request(
            "GET", f"/api/calendar/{event_id}",
            params={"user_id": user_id}
        )

    def create_event(self, event_data):
        return self.request("POST", "/api/calendar", data=event_data)

    def update_event(self, event_id, event_data):
        return self.request("PUT", f"/api/calendar/{event_id}", data=event_data)

    def delete_event(self, event_id, user_id):
        return self.request(
            "DELETE", f"/api/calendar/{event_id}",
            params={"user_id": user_id}
        )

    # DASHBOARD

    def get_dashboard(self, user_id):
        return self.request(
            "GET", f"/api/dashboard/{user_id}"
        )


nexus_backend = NexusBackendClient()