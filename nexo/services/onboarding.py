ONBOARDING_STEPS = ["Board", "Card", "ShareBoard"]


class OnboardingService:
    def get_progress(self, preferences: dict) -> dict:
        completed = []
        for step in ONBOARDING_STEPS:
            key = f"onboarding{step}Complete"
            if preferences.get(key):
                completed.append(step)
        return {
            "steps": ONBOARDING_STEPS,
            "completed": completed,
            "all_done": len(completed) >= len(ONBOARDING_STEPS),
        }

    def complete_step(self, preferences: dict, step: str) -> dict:
        if step not in ONBOARDING_STEPS:
            raise ValueError(f"Unknown onboarding step: {step}")
        preferences[f"onboarding{step}Complete"] = True
        return preferences

    def is_tour_active(self, preferences: dict) -> bool:
        return not preferences.get("onboardingTourEnded", False)
