from conversation_memory import conversation_memory

session = "test-session-1"

conversation_memory.add_message(
    session,
    "user",
    "My name is Alex."
)

conversation_memory.add_message(
    session,
    "assistant",
    "Nice to meet you, Alex!"
)

conversation_memory.add_message(
    session,
    "user",
    "What is my name?"
)

print("Conversation History:")
print(conversation_memory.get_history(session))

print("\nAI Context:")
print(conversation_memory.get_context(session))