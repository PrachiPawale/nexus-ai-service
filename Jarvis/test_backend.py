from backend_client import nexus_backend

print("Testing Nexus Backend Connection...")

result = nexus_backend.get_dashboard(1)

print("\nBackend Response:")
print(result)

if result["success"]:
    print("\nNexus Backend Connected Successfully!")
else:
    print("\nBackend Connection Failed!")
    print(result.get("message"))