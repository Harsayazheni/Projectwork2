"""
Chatbot Module - AI Career Assistant
"""

from flask import Blueprint, render_template, request, session, jsonify
from chatbot.context_manager import ContextManager
from chatbot.chatbot_logic import get_career_guidance

# Create Blueprint for chatbot module
chatbot_bp = Blueprint(
    'chatbot',
    __name__,
    template_folder='templates',
    static_folder='static'
)

# Initialize context manager
context_manager = ContextManager()

@chatbot_bp.route("/")
def chatbot():
    """Render chatbot interface"""
    if "prediction" not in session:
        return render_template(
            "chatbot.html",
            error=True,
            error_message="Please complete career prediction first to use the AI assistant."
        )
    
    return render_template(
        "chatbot.html",
        error=False,
        prediction=session.get("prediction")
    )

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    """Handle chatbot messages"""
    try:
        data = request.json
        user_message = data.get("message", "").strip()
        
        if not user_message:
            return jsonify({"success": False, "error": "Empty message"})
        
        # Get context from prediction module via session
        context = context_manager.build_context(session)
        
        # Get AI response
        bot_reply = get_career_guidance(user_message, context)
        
        return jsonify({
            "success": True,
            "response": bot_reply
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error: {str(e)}"
        })

@chatbot_bp.route("/context", methods=["GET"])
def get_context():
    """API endpoint to get current user context (for debugging)"""
    context_data = context_manager.get_context_data(session)
    return jsonify(context_data)