import dspy
from dspy.evaluate import Evaluate
import os
import mlflow
import json
import asyncio

from app.services.content_gen import generate_content
from app.services.user_preferences import extract_user_preferences
from app.services.assess import assess_content

from app.services.metric import generated_content_eval, user_preferences_eval, assess_content_eval


# mlflow.dspy.autolog()
# mlflow.set_tracking_uri('http://localhost:5000')

lm = dspy.LM('openai/gpt-4.1-mini', api_key=os.getenv('OPENAI_API_KEY'))
dspy.configure(lm=lm)

data_set = [
    dspy.Example(content="""
            # 7 Instant Wins: A Bite‑Size Listicle

            Metabolic Afterburn – Muscles act like idle GPUs — drawing power even when “off,” adding ~6–10 cal/day per extra pound of lean mass.

            Joint Armor – Stronger surrounding tissue stabilizes knees/hips, slashing injury risk by ~30 %.

            Hormone Tune‑Up – Testosterone + growth hormone surge for up to 24 h post‑session, aiding recovery across all activities.

            Bone Bank Deposits – Loading stimulates osteoblasts; density can climb 1–3 % / yr.

            Mood Elevator – Endorphins + dopamine spike = natural antidepressant.

            Glucose Control – Muscle hoards glycogen, improving insulin sensitivity and shrinking T2D risk window.

            Posture Reset – Deadlifts & rows counteract “keyboard hunch,” freeing the thoracic spine.
            """,
    quality=True
    ).with_inputs("content"),
    dspy.Example(content="""
            # From Couch to 200 lb Deadlift: Dad’s Journey
            My 62‑year‑old father hated gyms. A minor fall changed his mind. Eight weeks later he:

            Picks grandkids up pain‑free

            Sleeps through the night (back pain gone)

            Brags about his “lifter’s calluses” at church

            “Strength isn’t about ego,” he told me, “it’s about options.”
            The barbell became his independence device.
            """,
        quality=True
    ).with_inputs("content"),
    dspy.Example(content="""
            # FAQ: Weight Training for Absolute Beginners
            Q: Will I get bulky?
            A: Muscle gain averages 0.5–1 lb/mo for novices—bulking is intentional, not accidental.

            Q: Cardio vs. lifting—do I need both?
            A: Yes: aerobic for the heart pump, resistance for the hardware it pumps through.

            Q: Best schedule?

            3 × week full‑body or

            4 × week upper/lower split

            Q: Equipment?
            Start with:
            • Adjustable dumbbells
            • Resistance bands
            • Pull‑up bar
            """,
        quality=False
    ).with_inputs("content"),
    dspy.Example(content="""
            # 5‑Minute Primer: Your First Session
            Warm‑up: 5 min brisk walk + dynamic hips

            Circuit (3 rounds)

            Goblet Squat × 10

            Push‑up (incline) × 8

            Dumbbell Row × 10/arm

            Stretch, hydrate, log weights
            """,
        quality=True
    ).with_inputs("content"),
    dspy.Example(content="""
            # The Iron Manifesto
            Strength is democratic.

            Barbells don’t care about age, race, or salary.

            Plates measure effort honestly.

            Progress is quantifiable, unfiltered, and self‑authored.

            In a world of outsourced conveniences, hoisting cold steel is a rebellion—proof we can still opt into hard things for a bigger payoff: autonomy, vitality, grit.

            Pick up something heavy today.
            Your body—and maybe your character—will be heavier‑duty tomorrow.
            """,
        quality=False
    ).with_inputs("content"),
    dspy.Example(content="""
            # What Lifting Did for My Anxiety
            I used to lie awake at night with my mind racing—emails, regrets, what-ifs.
            Then I started lifting.

            The first time I deadlifted 135 lbs, I cried in the car. Not because it was hard, but because for once, my brain shut up. The iron demanded my full presence. And in that, I found peace.

            Lifting didn’t cure my anxiety. But it gave me agency. Structure. Something solid to hold when everything else felt like fog.
            """,
        quality=False
    ).with_inputs("content"),
    dspy.Example(content="""
            # Before and After: 3 Months of Lifting
            Before:

            BP: 138/90

            Squat: bodyweight only

            Mood: Flat. Lethargic.

            Sleep: 5–6 hours (interrupted)

            After (90 Days):

            BP: 121/78

            Squat: 155 lbs

            Mood: Stable. Energized.

            Sleep: 7.5 hours (deep + consistent)

            You can’t always see it on the scale. But the internal changes? Night and day.
            """,
        quality=False
    ).with_inputs("content"),
    dspy.Example(content="""
            # How Lifting Supports Aging Gracefully
            Strength declines 1–2% per year after age 30.
            By 70, most lose over 30% of their original muscle mass.

            But studies show resistance training in older adults:

            Rebuilds lost lean mass

            Reduces fall risk

            Improves cognition (via BDNF release)

            Restores confidence & mobility

            Source: Liu & Latham (2019), Cochrane Review

            Don’t age passively. Fight for your function.
            """,
        quality=True
    ).with_inputs("content"),
    dspy.Example(content="""
            # Lifting for the Lazy: Why It’s the Most Efficient Form of Exercise
            Don’t like running for hours? Great. You don’t need to.

            Strength training is time-efficient:

            3 sessions/week

            40 minutes/session

            Proven results in fat loss, insulin regulation, posture, and even sleep quality

            You don’t need 10,000 steps. You need 3 well-executed sets of squats.
            """,
        quality=True
    ).with_inputs("content"),
    dspy.Example(content="""
            # Machine Learning, Explained Like You’re Five
            Imagine your brain learns what a cat looks like. You see fur, whiskers, and hear a “meow.”

            Machine learning is how computers learn patterns just like that — by being shown examples over and over until they “get it.”

            ML isn’t magic. It’s math + memory + mistakes.
            And the best models just make fewer mistakes over time.
            """,
        quality=False
    ).with_inputs("content"),
    dspy.Example(content="""
            # 10 Real-World Things You Didn’t Know Use ML
            Your Netflix recommendations

            Google Maps traffic predictions

            Email spam filters

            Banking fraud alerts

            Voice assistants (like Siri)

            Self-checkout scanners

            Instagram feed ranking

            Typing autocorrect

            Smart thermostats

            Resume scanners at job portals


            """,
        quality=False
    ).with_inputs("content"),
    dspy.Example(content="""
            # From Model to Money: How ML Actually Drives Business
            A model isn’t valuable unless it solves a real problem.

            ✅ Churn prediction? Saves retention costs.
            ✅ Demand forecasting? Cuts inventory loss.
            ✅ Image moderation? Saves compliance dollars.

            ML is a lever — but only if it’s plugged into operations.
            Otherwise, it’s just a fancy spreadsheet with attitude.
            """,
        quality=True
    ).with_inputs("content"),
    dspy.Example(content="""
            # A Day in the Life of a Machine Learning Engineer
            8:30am: Reviewing overnight model performance
            10:00am: Meeting with product team to discuss model outputs
            11:30am: Feature engineering
            2:00pm: Hyperparameter tuning
            4:00pm: Data pipeline bug
            6:00pm: Re-deploy and monitor

            It’s not just math — it’s plumbing, communication, and iteration.
            """,
        quality=False
    ).with_inputs("content"),
    dspy.Example(content="""
            # The Dirty Truth About Clean Data
                80% of ML time isn’t building models — it’s wrangling data.

                Typos

                Missing values

                Duplicate records

                Inconsistent labels

                Models don’t fail because the math is wrong.
                They fail because the data lies.

                If you want to succeed in ML, learn to clean before you dream.
            """,
        quality=True
    ).with_inputs("content"),
    dspy.Example(content="""
            # Choosing the Right ML Model: A Decision Tree
            Start here:

            Is your data labeled?
            → Yes → Supervised learning
            → No → Unsupervised learning

            Supervised?
            → Classification or regression?
            → Lots of features? Try XGBoost.
            → Need explainability? Try logistic regression.
            → Images? Go CNN.
            → Text? Go transformer.

            Models are tools. Know what you’re building before picking the hammer.
            """,
        quality=True
    ).with_inputs("content"),
]

async def test_assess():
    evaluater = Evaluate(
        devset=data_set,
        metric=assess_content_eval,
        # num_threads=1,
        display_progress=True,
        return_outputs=True,
        return_all_scores=True,
        # display_table=5
    )
    evaluater(assess_content)

    mipro_optimizer = dspy.MIPROv2(
        metric=assess_content_eval,
        auto="medium",
    )
    optimized_assess_content = mipro_optimizer.compile(
        assess_content,
        trainset=data_set,
        max_bootstrapped_demos=4,
        requires_permission_to_run=False,
        minibatch=False
    )

    evaluater(optimized_assess_content, devset=data_set)
    optimized_assess_content.save("optimized_assess_content.json")
    # content = "This is a good content"
    # quality = await assess_content.acall(content=content)
    # return quality

async def test_generated_content():
    optimized_assess_content = assess_content
    optimized_assess_content.load("optimized_assess_content.json")

    optimized_extract_user_preferences = extract_user_preferences
    optimized_extract_user_preferences.load("optimized_user_preferences_two.json")

    optimized_generate_content = generate_content
    optimized_generate_content.load("optimized_generate_content.json")

    user_preferences = "Prefers detailed, original, and critically rigorous content with comprehensive analysis and well-developed perspectives. Values substantive explanation and critical insight over broad, incomplete, or superficial discussions. Maintains a strong preference for high-quality, in-depth explorations in technical, scientific, and niche entertainment fields, favoring originality and critical depth rather than general pop culture narratives or incomplete content. Continues to seek content that is thoroughly developed, well-written, and intellectually engaging."
    action = "start"

    content_gen_examples = []
    assess_examples = []
    user_preference_examples = []

    try:
        with open("content_gen_examples.json", "r") as f:
            saved_examples = json.load(f)
            content_gen_examples = [
                dspy.Example(
                    topic=ex["topic"],
                    content_type=ex["content_type"],
                    content=ex["content"],
                    user_preference=ex["user_preference"],
                    quality=ex["quality"]
                ).with_inputs("topic", "content_type", "user_preference")
                for ex in saved_examples
            ]
            assess_eval_examples = [
                dspy.Example(
                    content=ex["content"],
                    quality=ex["quality"],
                    user_preference=user_preferences
                ).with_inputs("content", "user_preference")
                for ex in saved_examples
            ]
        with open("user_preference_examples.json", "r") as f:
            saved_examples = json.load(f)
            user_preference_examples = [
                dspy.Example(
                    topic=ex["topic"],
                    content=ex["content"],
                    quality=ex["quality"],
                    prev_preference=ex["prev_preference"],
                    user_preference=ex["user_preference"]
                ).with_inputs("topic", "content", "quality", "prev_preference")
                for ex in saved_examples
            ]
        print(f"Loaded {len(content_gen_examples)} content gen examples and {len(assess_examples)} assess examples")
    except FileNotFoundError:
        print("No existing examples found. Starting fresh.")


    while True:
        action = input("Enter the action for content generation (generate/exit): ").lower().strip()
        
        if action == "exit":
            with open("content_gen_examples.json", "w") as f:
                json.dump([
                    {
                        "topic": ex.topic,
                        "content_type": ex.content_type,
                        "content": ex.content,
                        "quality": ex.quality,
                        "user_preference": ex.user_preference
                    }
                    for ex in content_gen_examples
                ], f, indent=2)
            with open("assess_examples.json", "w") as f:
                json.dump([
                    {
                        "content": ex.content,
                        "quality": ex.quality,
                        "user_preference": ex.user_preference
                    }
                    for ex in assess_examples
                ], f, indent=2)

            with open("user_preference_examples.json", "w") as f:
                json.dump([
                    {   
                        "topic": ex.topic,
                        "content": ex.content,
                        "quality": ex.quality,
                        "prev_preference": ex.prev_preference,
                        "user_preference": ex.user_preference
                    }
                    for ex in user_preference_examples
                ], f, indent=2)
            print(f"Saved {len(content_gen_examples)} content gen examples and {len(assess_examples)} assess examples and {len(user_preference_examples)} user preference examples")
            break
        elif action == "generate":
            topic = input("Enter the topic for content generation: ")
            content_type = input("Enter content type: ")
            generate_result = await optimized_generate_content.acall(topic=topic, content_type=content_type, user_preference=user_preferences)
            print(generate_result)

            user_feedback = input("Enter the user feedback (good/bad): ").lower().strip()
            quality = user_feedback == "good"
            ai_predict = await optimized_assess_content.acall(content=generate_result.content, user_preference=user_preferences)

            content_gen_example = dspy.Example(topic=topic, content_type=content_type, content=generate_result.content, quality=quality, user_preference=user_preferences).with_inputs("topic", "content_type", "user_preference")
            content_gen_examples.append(content_gen_example)
            
            assess_example = dspy.Example(content=generate_result.content, quality=ai_predict.quality, user_preference=user_preferences).with_inputs("content", "user_preference")
            assess_examples.append(assess_example)
            
            

            extract_user_preference = await optimized_extract_user_preferences.acall(topic=topic, content=generate_result.content, quality=quality, prev_preference=user_preferences)
            
            user_preference_example = dspy.Example(topic=topic, content=generate_result.content, quality=quality, prev_preference=user_preferences, user_preference=extract_user_preference.user_preference).with_inputs("topic", "content", "quality", "prev_preference")
            user_preferences = extract_user_preference.user_preference
            user_preference_examples.append(user_preference_example)
            print(f"Example added. Total examples: {len(content_gen_examples)}")
        else:
            print("Invalid action. Please enter 'generate' or 'exit'.")


    # ASSESS OPTIMIZE
    evaluater = Evaluate(
        devset=assess_eval_examples,
        metric=assess_content_eval,
        # num_threads=1,
        display_progress=True,
        return_outputs=True,
        return_all_scores=True,
        # display_table=5
    )
    evaluater(optimized_assess_content)
    
    # mipro_optimizer = dspy.MIPROv2(
    #     metric=assess_content_eval,
    #     auto="medium",
    # )
    # optimized_assess_content = mipro_optimizer.compile(
    #     assess_content,
    #     trainset=assess_eval_examples,
    #     max_bootstrapped_demos=8,
    #     requires_permission_to_run=False,
    #     minibatch=False
    # )

    # evaluater(optimized_assess_content)
    # optimized_assess_content.save("optimized_assess_content.json")


######################################

    # extract OPTIMIZE
    evaluater = Evaluate(
        devset=user_preference_examples,
        metric=user_preferences_eval,
        # num_threads=1,
        display_progress=True,
        return_outputs=True,
        return_all_scores=True,
        # display_table=5
    )
    evaluater(optimized_extract_user_preferences)
    
    # mipro_optimizer = dspy.MIPROv2(
    #     metric=user_preferences_eval,
    #     auto="medium",
    # )
    # optimized_user_preferences = mipro_optimizer.compile(
    #     optimized_extract_user_preferences,
    #     trainset=user_preference_examples,
    #     max_bootstrapped_demos=4,
    #     requires_permission_to_run=False,
    #     minibatch=False
    # )

    # evaluater(optimized_user_preferences)
    # optimized_user_preferences.save("optimized_user_preferences_two.json")


######################################

    # generate OPTIMIZE
    # evaluater = Evaluate(
    #     devset=content_gen_examples,
    #     metric=generated_content_eval,
    #     # num_threads=1,
    #     display_progress=True,
    #     return_outputs=True,
    #     return_all_scores=True,
    #     # display_table=5
    # )
    # evaluater(optimized_generate_content)
    
    # mipro_optimizer = dspy.MIPROv2(
    #     metric=generated_content_eval,
    #     auto="medium",
    # )
    # optimized_generate_content = mipro_optimizer.compile(
    #     generate_content,
    #     trainset=content_gen_examples,
    #     max_bootstrapped_demos=4,
    #     requires_permission_to_run=False,
    #     minibatch=False
    # )

    # evaluater(optimized_generate_content)
    # optimized_generate_content.save("optimized_generate_content.json")

            

async def main():
    # content = await generate_content.acall(topic="", content_type="blog")
    # print(content)
    # await test_assess()
    await test_generated_content()

if __name__ == "__main__":
    asyncio.run(main())






