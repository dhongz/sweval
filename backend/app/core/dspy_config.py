import dspy
import os

lm = dspy.LM('openai/gpt-4.1-mini', api_key=os.getenv('OPENAI_API_KEY'))
dspy.settings.configure(lm=lm)