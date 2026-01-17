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
        
        # Save patient consultation data if ward has been determined by AI
        if patient_data.get("ward"):
            asyncio.create_task(save_patient_consultation(
                session_id=session_id,
                patient_name=patient_data.get("patient_name"),
                patient_age=patient_data.get("patient_age"),
                symptoms=patient_data.get("patient_query"),
                suggested_ward=patient_data.get("ward")
            ))
        
        # Save chat conversation to database asynchronously
        asyncio.create_task(save_chat_to_database(session_id, result["messages"]))
        
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

async def save_chat_to_database(session_id: str, messages: list):
    """Save complete chat conversation to Supabase chat_sessions table"""
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(executor, _save_chat_blocking, session_id, messages)
    except Exception as e:
        print(f"[WARNING] Failed to save chat to database: {e}")

async def save_patient_consultation(session_id: str, patient_name: str, patient_age: int, symptoms: str, suggested_ward: str):
    """Save patient consultation details (name, age, symptoms, suggested ward) to database"""
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(executor, _save_consultation_blocking, session_id, patient_name, patient_age, symptoms, suggested_ward)
    except Exception as e:
        print(f"[WARNING] Failed to save consultation: {e}")

def _save_consultation_blocking(session_id: str, patient_name: str, patient_age: int, symptoms: str, suggested_ward: str):
    """Blocking function to save patient consultation data to database"""
    try:
        supabase_admin = get_supabase_admin()
        if not supabase_admin:
            return
        
        # Convert ward enum to string if needed
        ward_value = suggested_ward
        if hasattr(ward_value, 'value'):
            ward_value = ward_value.value
        else:
            ward_value = str(ward_value)
        
        # Prepare consultation data
        consultation_data = {
            "session_id": session_id,
            "patient_name": patient_name,
            "patient_age": patient_age,
            "symptoms": symptoms,
            "suggested_ward": ward_value,
            "status": "consultation_completed"
        }
        
        # Try to update existing consultation, or insert new one
        try:
            # First check if session exists
            existing = supabase_admin.table("chat_sessions").select("id").eq("session_id", session_id).execute()
            
            if existing.data and len(existing.data) > 0:
                # Update existing consultation
                supabase_admin.table("chat_sessions").update(consultation_data).eq("session_id", session_id).execute()
                print(f"[DATABASE] Updated consultation for {patient_name} (Age: {patient_age}) - Ward: {ward_value}")
            else:
                # Insert new consultation
                supabase_admin.table("chat_sessions").insert(consultation_data).execute()
                print(f"[DATABASE] Saved consultation for {patient_name} (Age: {patient_age}) - Suggested Ward: {ward_value}")
        except Exception as db_error:
            print(f"[WARNING] Consultation save failed: {db_error}")
    
    except Exception as e:
        print(f"[ERROR] Failed to save consultation: {e}")

def _save_chat_blocking(session_id: str, messages: list):
    """Blocking function to save chat to database"""
    try:
        supabase_admin = get_supabase_admin()
        if not supabase_admin:
            return
        
        # Convert LangChain messages to serializable format
        conversation_data = []
        for msg in messages:
            if hasattr(msg, 'content') and hasattr(msg, '__class__'):
                msg_type = msg.__class__.__name__
                msg_content = msg.content
                conversation_data.append({
                    "type": msg_type,
                    "content": msg_content
                })
        
        # Prepare data for chat_sessions table
        chat_data = {
            "session_id": session_id,
            "conversation_data": conversation_data,
            "status": "active"
        }
        
        # Try to update existing session, or insert new one
        try:
            # First check if session exists
            existing = supabase_admin.table("chat_sessions").select("id").eq("session_id", session_id).execute()
            
            if existing.data and len(existing.data) > 0:
                # Update existing session
                supabase_admin.table("chat_sessions").update(chat_data).eq("session_id", session_id).execute()
                print(f"[DATABASE] Updated chat session: {session_id}")
            else:
                # Insert new session
                supabase_admin.table("chat_sessions").insert(chat_data).execute()
                print(f"[DATABASE] Saved chat session: {session_id}")
        except Exception as db_error:
            print(f"[WARNING] Database save failed: {db_error}")
    
    except Exception as e:
        print(f"[ERROR] Failed to save chat: {e}")

async def store_patient_data_async(session_id: str, patient_data: Dict[str, Any]):
    """Store patient data asynchronously without blocking chat response"""
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(executor, store_patient_data, session_id, patient_data)
    except Exception:
        pass  # Silent fail - don't disrupt chat experience