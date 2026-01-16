from fastapi import APIRouter, HTTPException
from models.patient import ChatMessage, PatientData
from workflow.graph import graph
from database import get_supabase, get_supabase_admin
from typing import Dict, Any
import uuid

router = APIRouter()

# In-memory storage for conversation states (in production, use Redis or similar)
conversation_states: Dict[str, Dict[str, Any]] = {}

@router.post("/chat")
async def chat_endpoint(chat_message: ChatMessage) -> Dict[str, str]:
    """Handle chat messages and return AI responses"""
    try:
        session_id = chat_message.session_id

        # Get or create conversation state
        if session_id not in conversation_states:
            conversation_states[session_id] = {
                "messages": [],
                "patient_data": PatientData().model_dump(),
                "current_node": "router",
                "session_id": session_id
            }

        state = conversation_states[session_id]

        # Add user message to state
        from langchain_core.messages import HumanMessage
        human_message = HumanMessage(content=chat_message.message)
        state["messages"].append(human_message)

        # Process through LangGraph
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

        # Store patient data in Supabase if complete
        patient_data = result["patient_data"]
        if all([
            patient_data.get("patient_name"),
            patient_data.get("patient_age"),
            patient_data.get("patient_query"),
            patient_data.get("ward")
        ]):
            store_patient_data(session_id, patient_data)

        return {"response": ai_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

def store_patient_data(session_id: str, patient_data: Dict[str, Any]):
    """Store completed patient data in Supabase"""
    try:
        # Use admin client for inserts to bypass RLS
        supabase_admin = get_supabase_admin()
        supabase = get_supabase()
        
        print(f"DEBUG: Supabase admin client: {supabase_admin is not None}")
        print(f"DEBUG: Supabase anon client: {supabase is not None}")

        if supabase_admin is None:
            print("ERROR: Supabase admin client is None - make sure SUPABASE_SERVICE_ROLE_KEY is set in environment")
            return

        # Convert ward enum to string if it's an enum
        ward_value = patient_data.get("ward")
        if ward_value is None:
            print("ERROR: Ward is None!")
            return
            
        if hasattr(ward_value, 'value'):
            # It's an Enum, get its value
            ward_value = ward_value.value
            print(f"DEBUG: Converted enum ward to string: {ward_value}")
        else:
            # It's already a string
            ward_value = str(ward_value)
            print(f"DEBUG: Ward is already string: {ward_value}")
        
        data = {
            "session_id": session_id,
            "patient_name": patient_data.get("patient_name"),
            "patient_age": patient_data.get("patient_age"),
            "patient_query": patient_data.get("patient_query"),
            "ward": ward_value,
            "created_at": "now()"
        }

        print(f"DEBUG: Final data to insert: {data}")

        # First check if table exists
        try:
            test_result = supabase_admin.table("patients").select("*").limit(1).execute()
            print(f"DEBUG: Table exists, current records: {len(test_result.data) if test_result.data else 0}")
        except Exception as table_error:
            print(f"DEBUG: Table check failed: {table_error}")

        # Now try to insert using admin client (bypasses RLS)
        print(f"DEBUG: Attempting insert with admin client")
        result = supabase_admin.table("patients").insert(data).execute()
        print(f"SUCCESS: Insert result type: {type(result)}")
        print(f"SUCCESS: Insert result: {result}")
        
        if hasattr(result, 'data'):
            print(f"SUCCESS: Inserted data: {result.data}")
            if result.data and len(result.data) > 0:
                print(f"SUCCESS: Record inserted successfully: {result.data[0]}")
                verify_result = supabase_admin.table("patients").select("*").eq("session_id", session_id).execute()
                print(f"SUCCESS: Verification - found {len(verify_result.data)} records for session {session_id}")
        else:
            print(f"SUCCESS: No data attribute in result, but insert likely succeeded")

    except Exception as e:
        print(f"ERROR: Failed to store patient data: {e}")
        import traceback
        print(f"ERROR: Full traceback: {traceback.format_exc()}")