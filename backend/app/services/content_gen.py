import dspy
from typing import Literal
import os

lm = dspy.LM('openai/gpt-4.1-mini', api_key=os.getenv('OPENAI_API_KEY'))
dspy.settings.configure(lm=lm)

class ContentGeneration(dspy.Signature):
    """Generate content of provided type about provided topic"""
    user_preference: str = dspy.InputField(desc="the user's overall preferences")
    topic: str = dspy.InputField(desc="the topic of the content to generate")
    content_type: str = dspy.InputField(desc="the type  of content to generate")
    content: str = dspy.OutputField(desc="markdown-formatted content")

class GenerateContent(dspy.Module):
    def __init__(self):
        self.generate_content = dspy.ChainOfThought(ContentGeneration)

    def forward(self, topic, content_type, user_preference):
        return self.generate_content(topic=topic, content_type=content_type, user_preference=user_preference)
    
    async def aforward(self, topic, content_type, user_preference):
        return await self.generate_content.acall(topic=topic, content_type=content_type, user_preference=user_preference)
        

generate_content = GenerateContent()