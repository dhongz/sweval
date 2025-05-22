import dspy
from typing import Literal

class UserPreferences(dspy.Signature):
    """Update the user's previous preferences based on the list of feedback from previous generations using those preferences. Consider when the quality is false and the topic of the content."""
    list_of_feedback: list[str] = dspy.InputField(desc="list of feedback in markdown containing the topic, the content, and the user rated quality as a boolean")
    prev_preference: str = dspy.InputField(desc="the user's overall preferences")
    user_preference: str = dspy.OutputField(desc="newly updated user preferences")

class ExtractUserPreferences(dspy.Module):
    def __init__(self):
        self.user_preferences = dspy.ChainOfThought(UserPreferences)

    def forward(self, list_of_feedback, prev_preference):
        return self.user_preferences(list_of_feedback=list_of_feedback, prev_preference=prev_preference)

    async def aforward(self, list_of_feedback, prev_preference):
        return await self.user_preferences.acall(list_of_feedback=list_of_feedback, prev_preference=prev_preference)
        
extract_user_preferences = ExtractUserPreferences()