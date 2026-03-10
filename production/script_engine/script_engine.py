from narrative.personality_engine.personality_engine import PersonalityEngine

class ScriptEngine:
    def __init__(self):
        self.personality = PersonalityEngine()

    def generate(self, brief):
        core = (
            f"Campaign: {brief['campaign']}\n"
            f"Era: {brief['era']}\n"
            f"Season: {brief['season']}\n"
            f"Arc: {brief['arc']}\n\n"
            f"Episode Focus: {brief['topic']}\n"
            "Researchers recently uncovered evidence that challenges known exploration routes."
        )
        return {"topic": brief["topic"], "body": self.personality.wrap(core), "summary": f"An investigation into {brief['topic']}."}
