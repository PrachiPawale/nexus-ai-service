from nlp_engine import jarvis_nlp


commands = [
    "Create a task to finish Nexus documentation",
    "Show my upcoming meetings",
    "Update goal 1 progress to 75 percent",
    "Delete task 3",
    "Schedule a meeting tomorrow",
    "Create a note about my project"
]


for command in commands:

    print("\nUser:", command)

    result = jarvis_nlp.process_command(command)

    print("JARVIS:", result)