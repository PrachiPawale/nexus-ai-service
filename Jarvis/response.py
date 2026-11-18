from datetime import datetime


def success_response(message, data=None):
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }


def error_response(message, error=None):
    return {
        "success": False,
        "message": message,
        "error": str(error) if error else None,
        "timestamp": datetime.now().isoformat()
    }


def jarvis_response(message, intent=None, data=None):
    return {
        "success": True,
        "assistant": "JARVIS",
        "response": message,
        "intent": intent,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }