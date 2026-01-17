from fastapi import APIRouter, HTTPException
from models.patient import ChatMessage, PatientData
from workflow.graph import graph
from database import get_supabase, get_supabase_admin
from typing import Dict, Any
import uuid
import asyncio
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()

# In-memory storage for conversation states (in production, use Redis or similar)
conversation_states: Dict[str, Dict[str, Any]] = {}

# Thread pool for non-blocking database operations
executor = ThreadPoolExecutor(max_workers=3)

@router.post("/chat")
async def chat_endpoint(chat_message: ChatMessage) -> Dict[str, str]:
    """Handle chat messages and return AI responses (optimized for speed)"""
    try:
        session_id = chat_message.session_id

        # Get or create conversation state
        if session_id not in conversation_states:
            conversation_states[session_id] = {
                "messages": [],
                "patient_data": PatientData().model_dump(),
                "current_node": "router",
                "session_id": session_id,
                "router_greeting_shown": False
            }

        state = conversation_states[session_id]

        # Add user message to state
        from langchain_core.messages import HumanMessage
        human_message = HumanMessage(content=chat_message.message)
        state["messages"].append(human_message)

        # Process through LangGraph (this is the main slow operation)
        result = graph.invoke(state)

        # Update stored state
        conversation_states[session_id] = result

        # Get AI response - look for the last message that's not the human message
        from langchain_core.messages import AIMessage
        ai_messages = [msg for msg in result["messages"] if isinstance(msg, AIMessage)]
        if ai_messages:
            ai_response = ai_messages[-1].content
        else:
            # Fallback: get the last message that's not from the user
            all_messages = result["messages"]
            for msg in reversed(all_messages):
                if hasattr(msg, 'content') and msg != human_message:
                    ai_response = msg.content
                    break
            else:
                ai_response = "I'm sorry, I couldn't process your request."

        # Get patient data for potential storage
        patient_data = result["patient_data"]
        
        # Store patient data asynchronously (non-blocking) if complete
        if all([
            patient_data.get("patient_name"),
            patient_data.get("patient_age"),
            patient_data.get("patient_query"),
            patient_data.get("ward")
        ]):
            # Run storage in background to avoid blocking response
            asyncio.create_task(store_patient_data_async(session_id, patient_data))

        return {"response": ai_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

def store_patient_data(session_id: str, patient_data: Dict[str, Any]):
    """Store completed patient data in Supabase (blocking)"""
    try:
        # Use admin client for inserts to bypass RLS
        supabase_admin = get_supabase_admin()
        
        if supabase_admin is None:
            return

        # Convert ward enum to string if it's an enum
        ward_value = patient_data.get("ward")
        if ward_value is None:
            return
            
        if hasattr(ward_value, 'value'):
            ward_value = ward_value.value
        else:
            ward_value = str(ward_value)
        
        data = {
            "session_id": session_id,
            "patient_name": patient_data.get("patient_name"),
            "patient_age": patient_data.get("patient_age"),
            "patient_query": patient_data.get("patient_query"),
            "ward": ward_value,
            "created_at": "now()"
        }

        # Insert data (with basic error handling)
        try:
            result = supabase_admin.table("patients").insert(data).execute()
        except Exception as insert_error:
            pass  # Silent fail for background task

    except Exception as e:
        pass  # Silent fail for background storage

async def store_patient_data_async(session_id: str, patient_data: Dict[str, Any]):
    """Store patient data asynchronously without blocking chat response"""
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(executor, store_patient_data, session_id, patient_data)
    except Exception:
        pass  # Silent fail - don't disrupt chat experience