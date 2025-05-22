import dspy
from typing import Literal
import os

lm = dspy.LM('openai/gpt-4.1-mini', api_key=os.getenv('OPENAI_API_KEY'))
dspy.settings.configure(lm=lm)

class Assess(dspy.Signature):
    """Using the user's preferences, discern if the content is good or bad."""
    content: str = dspy.InputField(desc="the content to assess")
    user_preference: str = dspy.InputField(desc="the user's overall preferences")
    quality: bool = dspy.OutputField(desc="is the content good")

class AssessContent(dspy.Module):
    def __init__(self):
        self.assess_content = dspy.ChainOfThought(Assess)

    def forward(self, content, user_preference):
        return self.assess_content(content=content, user_preference=user_preference)

    async def aforward(self, content, user_preference):
        return await self.assess_content.acall(content=content, user_preference=user_preference)

assess_content = AssessContent()