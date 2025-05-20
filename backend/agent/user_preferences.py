import dspy
from typing import Literal

class UserPreferences(dspy.Signature):
    """Update the user's previous preferences based on the content and it's perceived quality. Consider when the quality is false and the topic of the content."""
    topic: str = dspy.InputField(desc="the topic of the content")
    content: str = dspy.InputField(desc="content to extract the user's preferences from")
    quality: bool = dspy.InputField(desc="the perceived quality of the content")
    prev_preference: str = dspy.InputField(desc="the user's overall preferences")
    user_preference: str = dspy.OutputField(desc="newly updated user preferences")

class ExtractUserPreferences(dspy.Module):
    def __init__(self):
        self.user_preferences = dspy.ChainOfThought(UserPreferences)

    def forward(self, topic, content, quality, prev_preference):
        return self.user_preferences(topic=topic, content=content, quality=quality, prev_preference=prev_preference)

    async def aforward(self, topic, content, quality, prev_preference):
        return await self.user_preferences.acall(topic=topic, content=content, quality=quality, prev_preference=prev_preference)
        

extract_user_preferences = ExtractUserPreferences()