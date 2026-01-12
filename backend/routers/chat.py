from fastapi import APIRouter, HTTPException
from models.patient import ChatMessage, PatientData
from workflow.graph import graph
from database import get_supabase
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
        supabase = get_supabase()
        print(f"DEBUG: Supabase client: {supabase is not None}")

        if supabase:
            data = {
                "session_id": session_id,
                "patient_name": patient_data["patient_name"],
                "patient_age": patient_data["patient_age"],
                "patient_query": patient_data["patient_query"],
                "ward": patient_data["ward"],
                "created_at": "now()"
            }

            print(f"DEBUG: Attempting to insert data: {data}")

            # First check if table exists
            try:
                # Try to select from the table to see if it exists
                test_result = supabase.table("patients").select("*").limit(1).execute()
                print(f"DEBUG: Table exists, current records: {len(test_result.data) if test_result.data else 0}")
            except Exception as table_error:
                print(f"DEBUG: Table check failed: {table_error}")

            # Now try to insert
            result = supabase.table("patients").insert(data).execute()
            print(f"SUCCESS: Patient data stored: {result}")
            print(f"SUCCESS: Inserted data: {result.data if hasattr(result, 'data') else 'No data attribute'}")

            # Verify the insertion by selecting the record
            if result.data and len(result.data) > 0:
                inserted_id = result.data[0].get('session_id')
                verify_result = supabase.table("patients").select("*").eq("session_id", session_id).execute()
                print(f"SUCCESS: Verification - found {len(verify_result.data)} records for session {session_id}")
        else:
            print("ERROR: Supabase client is None")

    except Exception as e:
        print(f"ERROR: Failed to store patient data: {e}")
        import traceback
        print(f"ERROR: Full traceback: {traceback.format_exc()}")