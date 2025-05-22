import dspy
from typing import Literal
from agent.assess import assess_content
from agent.user_preferences import extract_user_preferences
import os

user_preferences = "Prefers detailed, original, and critically rigorous content with comprehensive analysis and well-developed perspectives. Values substantive explanation and critical insight over broad, incomplete, or superficial discussions. Maintains a strong preference for high-quality, in-depth explorations in technical, scientific, and niche entertainment fields, favoring originality and critical depth rather than general pop culture narratives or incomplete content. Continues to seek content that is thoroughly developed, well-written, and intellectually engaging."

lm = dspy.LM('openai/gpt-4.1-mini', api_key=os.getenv('OPENAI_API_KEY'))
dspy.settings.configure(lm=lm)

class InitGeneration(dspy.Signature):
    """Generate five pieces of content of provided type about provided topic in five different styles of delivery"""
    topic: str = dspy.InputField(desc="the topic of the content to generate")
    content_type: str = dspy.InputField(desc="the type  of content to generate")
    content: list[str] = dspy.OutputField(desc="markdown-formatted content")

class InitGroup(dspy.Module):
    def __init__(self):
        self.generate_content = dspy.Predict(InitGeneration)

    def forward(self, topic, content_type):
        return self.generate_content(topic=topic, content_type=content_type)

    async def aforward(self, topic, content_type):
        return await self.generate_content.acall(topic=topic, content_type=content_type)
        

init_group = InitGroup()


def assess_content_eval(example, pred, trace=None):
    return example.quality == pred.quality

async def async_assess_content(example, pred, trace=None):
    quality = await assess_content.acall(content=pred.content)
    return quality.quality == example.quality


def user_preferences_eval(example, pred, trace=None):
    optimized_assess_content = assess_content
    optimized_assess_content.load("optimized_assess_content.json")

    quality = optimized_assess_content(content=example.content, user_preference=pred.user_preference)
    return quality.quality == example.quality

async def async_user_preferences_eval(example, pred, trace=None):
    optimized_assess_content = assess_content
    optimized_assess_content.load("optimized_assess_content.json")

    quality = await optimized_assess_content.acall(content=example.content, user_preference=pred.user_preference)
    return quality.quality == example.quality


def generated_content_eval(example, pred, trace=None):
    optimized_assess_content = assess_content
    optimized_assess_content.load("optimized_assess_content.json")

    quality = optimized_assess_content(content=pred.content, user_preference=user_preferences)
    return quality.quality == example.quality

async def async_generated_content_eval(example, pred, trace=None):
    optimized_assess_content = assess_content
    optimized_assess_content.load("optimized_assess_content.json")

    quality = await optimized_assess_content.acall(content=pred.content, user_preference=user_preferences)
    return quality.quality == example.quality