from response import (
    success_response,
    error_response,
    jarvis_response
)

print(success_response("Task created successfully"))

print(error_response("Something went wrong"))

print(jarvis_response(
    "Hello! I am JARVIS, your Nexus assistant.",
    intent="greeting"
))