CONSTRAINT_ADAPTATION_PROMPT = """# Goal
You are an expert for designing prompts for creating dataset for culinary cuisines and nutrition. Given the recipe details, create scenarios for adapting to ingredient constraints for allergy and other reasons, and recreate the recipe to that. Make sure to keep the flavor profile similar to the provided recipe.

# Recipe
{recipe}

# Output
The alternative ingredients and the recipe steps in JSON format

# JSON Output format
{{
"altered recipe": <altered recipe>,
"altered ingredients": [<list of altered ingredients (only keep the ingredients)>]
}}"""

CONSTRAINT_GENERATOR_PROMPT = """# Goal
You are an expert for designing prompts for creating dataset for culinary cuisines and nutrition. Given the recipe details, create scenarios for adapting to ingredient constraints for allergy and other reasons, 

# Input
{{
    "title": "No-Bake Nut Cookies",
    "ingredients": [
      "1 c. firmly packed brown sugar",
      "1/2 c. evaporated milk",
      "1/2 tsp. vanilla",
      "1/2 c. broken nuts (pecans)",
      "2 Tbsp. butter or margarine",
      "3 1/2 c. bite size shredded rice biscuits"
    ],
    "directions": [
      "In a heavy 2-quart saucan, mix brown sugar, nuts, evaporated milk and butter or margarine.",
      "Stir over medium heat until mixture bubbles all over top.",
      "Boil and stir 5 minutes more. Take off heat.",
      "Stir in vanilla and cereal; mix well.",
      "Using 2 teaspoons, drop and shape into 30 clusters on wax paper.",
      "Let stand until firm, about 30 minutes."
    ]
}}

# Output
Make this recipe nut-free but keep flavor profile similar.

# JSON Output format
{{
"constraint": <recipe constraint>
}}"""

QA_PAIR_PROMPT = """# Goal
You are an expert for designing prompts for creating dataset for culinary cuisines and nutrition. Given the recipe details, create question-answer pairs. Make sure to keep the question and answer in context of the recipe (can be related to the ingredients, directions, allergens, etc.).
Make sure the answer is brief, friendly in tone and easy to understand.
# JSON Output format
{{
"question": <recipe question>,
"answer": <answer relevant to the recipe>
}}"""

RECIPE_SUMMARY_PROMPT = """# Goal
You are an expert for designing prompts for creating dataset for culinary cuisines and nutrition. Given the recipe details, summarize the recipe in 1-2 sentences. Focus on the main cooking method and key ingredients.

# JSON Output format
{{
"summary": <recipe summary>
}}"""
