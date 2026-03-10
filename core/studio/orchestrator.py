class StudioOrchestrator:
    def build_episode_brief(self, governor_state):
        topic = governor_state.get("next_priority") or governor_state.get("active_arc")
        return {
            "topic": topic,
            "campaign": governor_state.get("active_campaign"),
            "era": governor_state.get("active_era"),
            "season": governor_state.get("active_season"),
            "arc": governor_state.get("active_arc")
        }
