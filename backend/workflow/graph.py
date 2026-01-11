from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from models.patient import PatientData, Ward
import re
import os

# Initialize Gemini LLM for classification (only if API key is available)
llm = None
if os.getenv("GOOGLE_API_KEY"):
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.2,
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        print("[SUCCESS] LLM initialized with Google Gemini")
    except Exception as e:
        print(f"[ERROR] Failed to initialize LLM: {e}")
        llm = None
else:
    print("[INFO] GOOGLE_API_KEY not found - using keyword-based classification")

def classify_symptom_with_keywords(symptom: str) -> str:
    """Fallback keyword-based classification"""
    content = symptom.lower()

    # Emergency keywords
    emergency_keywords = [
        "emergency", "urgent", "heart attack", "stroke", "bleeding",
        "chest pain", "difficulty breathing", "unconscious",
        "severe pain", "accident", "injury", "broke", "broken",
        "fracture", "sprain", "cut", "wound", "burn", "fever",
        "high temperature", "collapse", "fall", "crash"
    ]

    # Mental health keywords
    mental_health_keywords = [
        "depression", "anxiety", "anxious", "suicide", "mental health",
        "therapy", "counseling", "stress", "panic attack", "panic",
        "mood disorder", "psychological", "psychiatric", "mental",
        "depressed", "sad", "worried", "nervous", "overwhelmed"
    ]

    if any(keyword in content for keyword in emergency_keywords):
        return "Emergency"
    elif any(keyword in content for keyword in mental_health_keywords):
        return "Mental_health"
    else:
        return "General"

def classify_symptom_with_llm(symptom: str) -> str:
    """Use LLM to classify symptoms into General, Emergency, or Mental_health"""

    # If LLM is not available, fall back to keyword-based classification
    if llm is None:
        return classify_symptom_with_keywords(symptom)

    prompt = (
        "You are a helpful Medical Assistant. Classify the symptoms below into one of the categories:\n\n"
        "- General\n"
        "- Emergency\n"
        "- Mental_health\n\n"
        f"Symptom: {symptom}\n\n"
        "Respond only with one word: General, Emergency, or Mental_health\n\n"
        "Example: Input: I have fever, Output: General"
    )

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        category = response.content.strip()

        # Normalize the response
        category_lower = category.lower()
        if "general" in category_lower:
            return "General"
        elif "emergency" in category_lower:
            return "Emergency"
        elif "mental" in category_lower:
            return "Mental_health"
        else:
            return "General"  # Default fallback

    except Exception as e:
        print(f"LLM classification failed: {e}")
        return classify_symptom_with_keywords(symptom)  # Fallback to keyword-based

class ConversationState(TypedDict):
    messages: list
    patient_data: PatientData
    current_node: str
    session_id: str

def router_node(state: ConversationState) -> ConversationState:
    """Route to initial ward for information collection"""
    messages = state["messages"]
    last_message = messages[-1]

    if isinstance(last_message, HumanMessage):
        # For initial routing, always go to general ward first
        # The ward logic will handle the actual classification later
        ward = Ward.GENERAL
        next_node = "general_ward"

        # Initialize patient data
        patient_data = state["patient_data"].copy()
        patient_data["ward"] = ward

        return {
            **state,
            "patient_data": patient_data,
            "current_node": next_node
        }

    return state

def general_ward_node(state: ConversationState) -> ConversationState:
    return handle_ward_logic(state, "general")

def emergency_ward_node(state: ConversationState) -> ConversationState:
    return handle_ward_logic(state, "emergency")

def mental_health_ward_node(state: ConversationState) -> ConversationState:
    return handle_ward_logic(state, "mental_health")

def handle_ward_logic(state: ConversationState, ward_type: str) -> ConversationState:
    """Common logic for all ward nodes - collect patient information in name -> age -> symptoms order"""
    patient_data = state["patient_data"].copy()
    messages = state["messages"]

    # Count AI messages to know what step we're in
    ai_message_count = len([msg for msg in messages if isinstance(msg, AIMessage)])

    # Process user responses based on conversation step
    last_user_message = None
    for msg in reversed(messages):
        if hasattr(msg, 'content') and not isinstance(msg, AIMessage):
            last_user_message = msg.content
            break

    # Track the effective conversation step (accounts for validation failures)
    effective_step = ai_message_count

    # Adjust effective step if we have missing required information
    if not patient_data.get("patient_name") and ai_message_count >= 1:
        effective_step = 1  # Still waiting for name
    elif not patient_data.get("patient_age") and ai_message_count >= 2:
        effective_step = 2  # Still waiting for valid age
    elif not patient_data.get("patient_query") and ai_message_count >= 3:
        effective_step = 3  # Still waiting for symptoms

    if ai_message_count > 0 and last_user_message:
        # Process user response based on effective conversation step
        if effective_step == 1:
            # User provided name
            patient_data["patient_name"] = last_user_message.strip()
        elif effective_step == 2:
            # User provided age - validate it
            age_input = last_user_message.strip()
            if age_input.isdigit():
                age = int(age_input)
                # Reasonable age validation (1-120 years)
                if 1 <= age <= 120:
                    patient_data["patient_age"] = age
                # No print statements needed in production
            # Invalid input is handled by not storing it
        elif effective_step == 3:
            # User provided symptoms
            patient_data["patient_query"] = last_user_message.strip()

    # Determine next question based on effective conversation step
    if effective_step == 0:
        # First interaction - ask for name
        question = "Hello! I'm the hospital AI receptionist. May I please have your full name?"
    elif effective_step == 1:
        # After getting name, ask for age
        question = "Thank you. Could you please tell me your age?"
    elif effective_step == 2:
        # Check if we have valid age, if not, ask again
        if not patient_data.get("patient_age"):
            question = "I'm sorry, please enter a valid age using only numbers (between 1-120)."
        else:
            # Age is valid, ask for symptoms
            question = "Thank you. Could you please describe your symptoms so I can help route you to the appropriate department?"
    elif effective_step == 3:
        # User provided symptoms, now classify and complete
        # All information collected, classify symptoms and route to ward
        if patient_data.get("patient_name") and patient_data.get("patient_age") and patient_data.get("patient_query"):
            # Classify symptoms and determine ward
            symptoms = patient_data["patient_query"]
            ward = classify_symptom_with_llm(symptoms)

            # Map classification to ward enum
            if ward == "Emergency":
                final_ward = Ward.EMERGENCY
                ward_display = "Emergency Department"
            elif ward == "Mental_health":
                final_ward = Ward.MENTAL_HEALTH
                ward_display = "Mental Health Services"
            else:
                final_ward = Ward.GENERAL
                ward_display = "General Ward"

            # Update patient data with final ward
            patient_data["ward"] = final_ward

            # Trigger webhook and complete
            trigger_webhook(patient_data)
            success_message = AIMessage(content=f"Thank you for providing your information. Based on your symptoms, you'll be shifted to the {ward_display}. A healthcare professional will assist you shortly.")

            return {
                **state,
                "patient_data": patient_data,
                "messages": messages + [success_message],
                "current_node": "complete"
            }
        else:
            # Check what's missing and ask appropriately
            if not patient_data.get("patient_age"):
                question = "I'm sorry, please enter a valid age using only numbers (between 1-120)."
            else:
                question = "Could you please describe your symptoms?"

    ai_message = AIMessage(content=question)
    return {
        **state,
        "patient_data": patient_data,
        "messages": messages + [ai_message],
        "current_node": f"{ward_type}_ward"  # Stay in the same ward node
    }

def get_question_for_field(field: str, ward_type: str) -> str:
    """Generate appropriate question based on missing field and ward type"""
    ward_messages = {
        "general": "General Ward",
        "emergency": "Emergency Department",
        "mental_health": "Mental Health Services"
    }

    ward_name = ward_messages.get(ward_type, "Hospital")

    questions = {
        "patient_name": f"I understand you're contacting the {ward_name}. May I please have your full name?",
        "patient_age": "Could you please tell me your age?",
        "patient_query": f"What specific symptoms or concerns are you experiencing that brought you to the {ward_name}?"
    }

    return questions.get(field, "Could you please provide that information?")

def trigger_webhook(patient_data: PatientData):
    """Send patient data to webhook endpoint"""
    import httpx
    import os

    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        payload = {
            "patient_name": patient_data["patient_name"],
            "patient_age": patient_data["patient_age"],
            "patient_query": patient_data["patient_query"],
            "ward": patient_data["ward"]
        }

        try:
            response = httpx.post(webhook_url, json=payload, timeout=10.0)
            print(f"Webhook triggered successfully: {response.status_code}")
        except Exception as e:
            print(f"Webhook failed: {e}")
    else:
        print("No webhook URL configured")

def get_next_node(state: ConversationState) -> str:
    """Determine the next node based on current state"""
    current_node = state["current_node"]
    if current_node == END:
        return END
    return current_node

# Build the graph
def build_graph():
    workflow = StateGraph(ConversationState)

    # Add nodes
    workflow.add_node("router", router_node)
    workflow.add_node("general_ward", general_ward_node)
    workflow.add_node("emergency_ward", emergency_ward_node)
    workflow.add_node("mental_health_ward", mental_health_ward_node)

    # Add edges
    workflow.set_entry_point("router")

    # Router routes to ward nodes
    workflow.add_conditional_edges(
        "router",
        lambda x: x["current_node"],
        {
            "general_ward": "general_ward",
            "emergency_ward": "emergency_ward",
            "mental_health_ward": "mental_health_ward"
        }
    )

    # Ward nodes return to a final node that handles completion
    workflow.add_node("complete", lambda x: x)  # Simple passthrough node

    # All ward nodes lead to the complete node when done
    for ward in ["general_ward", "emergency_ward", "mental_health_ward"]:
        workflow.add_edge(ward, "complete")

    # Set complete as a final node
    workflow.set_finish_point("complete")

    return workflow.compile()

# Global graph instance
graph = build_graph()