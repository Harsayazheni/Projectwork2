"""
OPUS Career Management Platform - Main Entry Point
"""

from flask import Flask, render_template
import os
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "opus_secret_key_change")

    # -------------------------------------------------
    # ✅ SINGLE, EXPLICIT HOME ROUTE
    # -------------------------------------------------
    @app.route("/")
    def home():
        # Reuse existing homepage UI
        return render_template("home.html")

    # -------------------------------------------------
    # Register Blueprints (ALL PREFIXED)
    # -------------------------------------------------

    # Career Prediction (NO LONGER OWNS "/")
    from prediction.app import prediction_bp
    app.register_blueprint(prediction_bp, url_prefix="/prediction")

    # Chatbot
    from chatbot.app import chatbot_bp
    app.register_blueprint(chatbot_bp, url_prefix="/chatbot")

    # Resume Match
    from resume_match.app import resume_bp
    app.register_blueprint(resume_bp, url_prefix="/resume")

    # Fake Job Detector
    from fakejobdetector.app import fakejob_bp
    app.register_blueprint(fakejob_bp, url_prefix="/fakejob")

    # Roadmap Generator (already prefixed internally)
    from roadmap_generator.app import roadmap_bp
    app.register_blueprint(roadmap_bp)

    # -------------------------------------------------
    # Health Check
    # -------------------------------------------------
    @app.route("/health")
    def health():
        return {"status": "OK"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
