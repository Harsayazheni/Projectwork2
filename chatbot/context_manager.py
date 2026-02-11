"""
Context Manager - Extracts and formats prediction data for chatbot
"""

class ContextManager:
    """Manages user context from prediction module"""
    
    def get_skill_gaps(self, skills, ideal):
        """Calculate skill gaps"""
        if not skills or not ideal:
            return []
        
        gaps = []
        for skill, val in skills.items():
            ideal_val = ideal.get(skill, val)
            if val < ideal_val:
                gaps.append({
                    "skill": skill.replace("_", " "),
                    "current": val,
                    "ideal": ideal_val,
                    "gap": ideal_val - val
                })
        
        # Sort by gap (highest first)
        gaps.sort(key=lambda x: x["gap"], reverse=True)
        return gaps
    
    def build_context(self, session):
        """Build formatted context string for AI"""
        if "prediction" not in session:
            return "No career prediction available yet. User is exploring career options."
        
        prediction = session.get("prediction", "Unknown")
        description = session.get("description", "")
        skills = session.get("skills", {})
        ideal = session.get("ideal", {})
        
        # Get top 3 skill gaps
        gaps = self.get_skill_gaps(skills, ideal)
        top_gaps = gaps[:3] if gaps else []
        
        context = f"""
CURRENT USER CONTEXT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Predicted Career: {prediction}
📝 Description: {description}

🎯 USER'S CURRENT SKILLS (out of 10):
"""
        
        for skill, val in skills.items():
            context += f"   • {skill.replace('_', ' ')}: {val}/10\n"
        
        if top_gaps:
            context += f"\n⚠️  TOP 3 SKILL GAPS TO IMPROVE:\n"
            for i, gap in enumerate(top_gaps, 1):
                context += f"   {i}. {gap['skill']}: Currently {gap['current']}/10, Need {gap['ideal']}/10 (Gap: {gap['gap']})\n"
        
        context += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        return context
    
    def get_context_data(self, session):
        """Get context as structured data (for API/debugging)"""
        skills = session.get("skills", {})
        ideal = session.get("ideal", {})
        gaps = self.get_skill_gaps(skills, ideal)
        
        return {
            "prediction": session.get("prediction"),
            "description": session.get("description"),
            "skills": skills,
            "ideal": ideal,
            "skill_gaps": gaps[:3]
        }