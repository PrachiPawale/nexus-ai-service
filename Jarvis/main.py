from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import jarvis_nlp  # Import the JarvisNLP instance from nlp_engine.py
from ai_engine import generate_response

from command_executor import execute_command

from fastapi.middleware.cors import CORSMiddleware

from response import (
    success_response,
    error_response,
    jarvis_response
)

from conversation_memory import conversation_memory

app = FastAPI(
    title="Nexus JARVIS",
    description="AI-powered natural language service for Nexus",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CommandRequest(BaseModel):
    text: str

class ChatRequest(BaseModel):
    text: str
    session_id: str = "default"

@app.get("/")
def root():
    return {
        "message": "Nexus JARVIS is running",
        "version": "2.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "jarvis"
    }


@app.post("/process-command")
def process_command(request: CommandRequest):

    try:
        if not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Command cannot be empty"
            )

        # Step 1: Understand the command
        nlp_result = jarvis_nlp.process_command(request.text)

        # Step 2: Execute the command
        execution_result = execute_command(nlp_result)

        return {
            "success": execution_result.get("success"),
            "input": request.text,
            "intent": nlp_result,
            "response": execution_result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )  
        
# JARVIS AI Chat Endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        if not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty"
            )

        session_id = request.session_id

        # Get previous conversation context
        context = conversation_memory.get_context(session_id)

        # Save current user message
        conversation_memory.add_message(
            session_id,
            "user",
            request.text
        )

        # Generate AI response
        result = generate_response(
            prompt=request.text,
            context=context
        )

        if not result.get("success"):
            return error_response(
                result.get("message", "Unable to generate response"),
                result.get("error")
            )

        answer = result.get("response")

        # Save JARVIS response
        conversation_memory.add_message(
            session_id,
            "assistant",
            answer
        )

        return jarvis_response(
            message=answer,
            intent="conversation",
            data={
                "session_id": session_id,
                "provider": result.get("provider"),
                "model": result.get("model")
            }
        )

    except HTTPException:
        raise

    except Exception as e:
        return error_response(
            "An unexpected error occurred",
            e
        )
        
@app.get("/conversation/{session_id}")
def get_conversation(session_id: str):
    try:
        history = conversation_memory.get_history(session_id)

        return success_response(
            "Conversation history retrieved successfully",
            data={
                "session_id": session_id,
                "history": history,
                "total_messages": len(history)
            }
        )

    except Exception as e:
        return error_response(
            "Unable to retrieve conversation history",
            e
        )
        
@app.delete("/conversation/{session_id}")
def delete_conversation(session_id: str):
    try:
        conversation_memory.clear_history(session_id)

        return success_response(
            "Conversation history cleared successfully",
            data={
                "session_id": session_id
            }
        )

    except Exception as e:
        return error_response(
            "Unable to clear conversation history",
            e
        )