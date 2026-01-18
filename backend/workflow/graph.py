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
    """Use LLM to classify symptoms into General, Emergency, or Mental_health (with timeout)"""

    # If LLM is not available, fall back to keyword-based classification
    if llm is None:
        return classify_symptom_with_keywords(symptom)

    # Try quick keyword-based check first (faster fallback)
    quick_result = classify_symptom_with_keywords(symptom)
    if quick_result in ["Emergency", "Mental_health"]:
        # If keyword-based check finds emergency/mental health, trust it (faster)
        return quick_result

    prompt = (
        "You are a helpful Medical Assistant. Classify the symptoms below into one of the categories:\n\n"
        "- General\n"
        "- Emergency\n"
        "- Mental_health\n\n"
        f"Symptom: {symptom}\n\n"
        "Respond only with one word: General, Emergency, or Mental_health"
    )

    try:
        # Call LLM with minimal overhead
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
        # If LLM fails, fall back to keyword-based (much faster)
        return classify_symptom_with_keywords(symptom)

class ConversationState(TypedDict):
    messages: list
    patient_data: PatientData
    current_node: str
    session_id: str
    router_greeting_shown: bool

def router_node(state: ConversationState) -> ConversationState:
    """Route to initial ward for information collection and generate first response"""
    messages = state["messages"]
    
    # Only show greeting if we haven't shown it yet
    if not state.get("router_greeting_shown", False) and len(messages) > 0:
        last_message = messages[-1]
        
        if isinstance(last_message, HumanMessage):
            # For initial routing, always go to general ward first
            # The ward logic will handle the actual classification later
            ward = Ward.GENERAL
            next_node = "general_ward"

            # Initialize patient data
            patient_data = state["patient_data"].copy()
            patient_data["ward"] = ward

            # Generate initial greeting response
            initial_response = AIMessage(content="Hello! I'm the hospital AI receptionist. May I please have your full name?")

            return {
                **state,
                "patient_data": patient_data,
                "messages": messages + [initial_response],
                "current_node": next_node,
                "router_greeting_shown": True
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
    
    # Count how many user messages we have to know which response we're processing
    user_message_count = len([msg for msg in messages if not isinstance(msg, AIMessage)])

    # Get the last user message
    last_user_message = None
    for msg in reversed(messages):
        if hasattr(msg, 'content') and not isinstance(msg, AIMessage):
            last_user_message = msg.content
            break

    # Check if the message is a polite greeting/closing (thank you, goodbye, etc.)
    if last_user_message:
        polite_keywords = ["thank you", "thanks", "thank", "goodbye", "bye", "take care", "nice day", "have a nice day", "see you", "appreciate it", "appreciate"]
        last_message_lower = last_user_message.lower().strip()
        
        if any(keyword in last_message_lower for keyword in polite_keywords):
            # Generate a nice closing response
            patient_name = patient_data.get("patient_name")
            closing_responses = [
                f"You're welcome, {patient_name}! Thank you for visiting our hospital. Have a nice day and take care!",
                f"Thank you for your trust, {patient_name}. Wishing you good health. Have a wonderful day!",
                f"You're most welcome, {patient_name}! Take care and get well soon. Have a great day!",
                f"Thank you for choosing our hospital, {patient_name}. Wishing you a speedy recovery. Have a nice day!",
            ]
            
            closing_message = closing_responses[0] if patient_name else "You're welcome! Thank you for visiting our hospital. Have a nice day and take care!"
            ai_message = AIMessage(content=closing_message)
            
            return {
                **state,
                "patient_data": patient_data,
                "messages": messages + [ai_message],
                "current_node": "complete"
            }

    # Determine what information we have and what we need next
    has_name = patient_data.get("patient_name") is not None and patient_data.get("patient_name").strip() != ""
    has_valid_age = patient_data.get("patient_age") is not None
    has_symptoms = patient_data.get("patient_query") is not None and patient_data.get("patient_query").strip() != ""

    # Only process the user message if the router greeting has been shown
    # This prevents processing the first user message twice
    if state.get("router_greeting_shown", False) and last_user_message:
        # Process the last user message to populate missing fields (in order: name -> age -> symptoms)
        if user_message_count == 1 and not has_name:
            # Don't process yet - this is the first message and router greeting was just shown
            pass
        elif not has_name:
            # First response should be the name (second user message, first AI response was greeting)
            patient_data["patient_name"] = last_user_message.strip()
            has_name = True
        elif has_name and not has_valid_age:
            # Second response should be the age
            age_input = last_user_message.strip()
            if age_input.isdigit():
                age = int(age_input)
                # Reasonable age validation (1-120 years)
                if 1 <= age <= 120:
                    patient_data["patient_age"] = age
                    has_valid_age = True
        elif has_name and has_valid_age and not has_symptoms:
            # Third response should be the symptoms
            patient_data["patient_query"] = last_user_message.strip()
            has_symptoms = True

    # Determine the next question based on what we're missing
    if not has_name:
        # First step - ask for name
        question = "Hello! I'm the hospital AI receptionist. May I please have your full name?"
    elif not has_valid_age:
        # Second step - ask for age
        question = f"Thank you, {patient_data.get('patient_name')}. Could you please tell me your age? (Please enter a number between 1-120)"
    elif not has_symptoms:
        # Third step - ask for symptoms
        question = "Thank you. Could you please describe your symptoms so I can help route you to the appropriate department?"
    else:
        # All information collected - classify and complete
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
        success_message = AIMessage(content=f"Thank you for providing your information, {patient_data.get('patient_name')}. Based on your symptoms, you'll be shifted to the {ward_display}. A healthcare professional will assist you shortly.")

        return {
            **state,
            "patient_data": patient_data,
            "messages": messages + [success_message],
            "current_node": "complete"
        }

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