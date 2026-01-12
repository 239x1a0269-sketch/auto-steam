from langgraph.graph import StateGraph
from agent.state import AgentState
from agent.intent import detect_intent
from agent.tools import mock_lead_capture

def chatbot_node(state: AgentState):
    last_user_msg = state["messages"][-1]
    intent = detect_intent(last_user_msg)

    state["intent"] = intent

    if intent == "greeting":
        return {"messages": ["Hi! How can I help you with AutoStream today?"]}

    if intent == "product_inquiry":
        return {
            "messages": [
                "AutoStream offers:\n"
                "- Basic: $29/month (10 videos, 720p)\n"
                "- Pro: $79/month (Unlimited, 4K, AI captions)\n"
                "Which plan are you interested in?"
            ]
        }

    if intent == "high_intent":
        if not state.get("name"):
            return {"messages": ["Great! May I have your name?"]}
        if not state.get("email"):
            return {"messages": ["Thanks! Could you share your email?"]}
        if not state.get("platform"):
            return {"messages": ["Which creator platform do you use? (YouTube, Instagram, etc.)"]}

        mock_lead_capture(state["name"], state["email"], state["platform"])
        return {"messages": ["🎉 You’re all set! Our team will contact you shortly."]}

    return {"messages": ["Can you please clarify your request?"]}

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("chatbot", chatbot_node)
    graph.set_entry_point("chatbot")
    graph.set_finish_point("chatbot")
    return graph.compile()
