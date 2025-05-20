import dspy
from typing import Literal
from agent.assess import assess_content
from agent.user_preferences import extract_user_preferences


user_preferences = "Prefers detailed, original, and critically rigorous content with comprehensive analysis and well-developed perspectives. Values substantive explanation and critical insight over broad, incomplete, or superficial discussions. Maintains a strong preference for high-quality, in-depth explorations in technical, scientific, and niche entertainment fields, favoring originality and critical depth rather than general pop culture narratives or incomplete content. Continues to seek content that is thoroughly developed, well-written, and intellectually engaging."

def assess_content_eval(example, pred, trace=None):
    return example.quality == pred.quality


async def async_assess_content(example, pred, trace=None):
    quality = await assess_content.acall(content=pred.content)
    return quality.quality == example.quality

def user_preferences_eval(example, pred, trace=None):
    optimized_assess_content = assess_content
    optimized_assess_content.load("optimized_assess_content.json")

    # optimized_user_preferences = extract_user_preferences
    # optimized_user_preferences.load("optimized_user_preferences.json")

    # preference = optimized_user_preferences(content=example.content, quality=example.quality, prev_preference=example.prev_preference)
    quality = optimized_assess_content(content=example.content, user_preference=pred.user_preference)
    return quality.quality == example.quality

def generated_content_eval(example, pred, trace=None):
    optimized_assess_content = assess_content
    optimized_assess_content.load("optimized_assess_content.json")

    quality = optimized_assess_content(content=pred.content, user_preference=user_preferences)
    return quality.quality == example.quality