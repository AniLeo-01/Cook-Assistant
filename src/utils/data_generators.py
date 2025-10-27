import json
from openai import AsyncOpenAI
from typing import Dict, Any
import os
from src.prompts.dataset_prompts import QA_PAIR_PROMPT, CONSTRAINT_GENERATOR_PROMPT, CONSTRAINT_ADAPTATION_PROMPT, RECIPE_SUMMARY_PROMPT
from dotenv import load_dotenv

load_dotenv()

async def generate(recipe: Dict[str, Any], system_prompt: str, model_name: str):
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = await client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": str(recipe)}
        ],
        temperature=1,
        response_format={"type": "json_object"},

    )
    result = json.loads(response.choices[0].message.content)
    return result

async def generate_recipe_samples(recipe: Dict[str, Any]):
    prompt = f"Generate a recipe using the following ingredients: {', '.join(recipe['cleaned_ingredients'])}. Include a title and clear steps."
    system_prompt = "You are a helpful assistant that generates recipe samples from a given set of ingredients."
    directions = recipe['directions']
    title = recipe['title']
    directions_text = "\n".join(directions)
    return [{"role": "system", "content": system_prompt}, 
    {"role": "user", "content": prompt},
    {"role": "assistant", "content": f"Using the given ingredients, you can cook the following dish: {title}\nHere is how to prepare it:\n{directions_text}"}
    ]

async def generate_ingredient_extraction_samples(recipe: Dict[str, Any]):
    prompt = f"List all the ingredients and quantities for this recipe: \n" + "\n".join(recipe['directions'])
    system_prompt = "You are a helpful assistant that is expert in culinary cuisines"
    ingredients_text = ", ".join(recipe['ingredients'])
    return [{"role": "system", "content": system_prompt},
    {"role": "user", "content": prompt},
    {"role": "assistant", "content": ingredients_text}]

async def constraint_generator_samples(recipe: Dict[str, Any]):
    constraint_result = await generate(recipe, CONSTRAINT_GENERATOR_PROMPT, os.getenv('DATASET_CURATOR_MODEL'))
    constraint_text = constraint_result['constraint']
    adapted_recipe = await generate(constraint_text, CONSTRAINT_ADAPTATION_PROMPT.format(recipe=recipe), os.getenv('DATASET_CURATOR_MODEL'))
    altered_recipe = adapted_recipe['altered recipe']
    ingredients_list = ', '.join(altered_recipe['ingredients'])
    directions_list = '\n'.join(altered_recipe['directions'])
    system_prompt = "You are a helpful assistant that is expert in culinary cuisines, given the following constraint, create a recipe that is adapted to it. Make sure to keep the flavor profile similar to the provided recipe."
    return [{"role": "system", "content": system_prompt},
    {"role": "user", "content": constraint_text},
    {"role": "assistant", "content": f"The ingredients for {altered_recipe['title']} are {ingredients_list} and here's the full recipe for it: \n{directions_list}"}]

async def recipe_summary_samples(recipe: Dict[str, Any]):
    system_prompt = "Summarize the recipe in 1-2 sentences. Focus on the main cooking method and key ingredients."
    summarized_recipe = await generate(recipe, RECIPE_SUMMARY_PROMPT, os.getenv('DATASET_CURATOR_MODEL'))
    return [{"role": "system", "content": system_prompt},
    {"role": "user", "content": str(recipe)},
    {"role": "assistant", "content": summarized_recipe['summary']}]

async def generate_qa_pair_samples(recipe: Dict[str, Any]):
    system_prompt = f"You are a helpful assistant that is expert in culinary cuisines, given the following recipe and question. Make sure to keep the answer in context of the recipe.\n# Recipe: {recipe}"
    qa_pair = await generate(recipe, QA_PAIR_PROMPT, os.getenv('DATASET_CURATOR_MODEL'))
    question, answer = qa_pair['question'], qa_pair['answer']
    return [{"role": "system", "content": system_prompt},
    {"role": "user", "content": question},
    {"role": "assistant", "content": answer}]




# async def main():
#     recipe = {
#         "title": "No-Bake Nut Cookies",
#         "ingredients": [
#             "1 c. firmly packed brown sugar",
#             "1/2 c. evaporated milk",
#             "1/2 tsp. vanilla",
#             "1/2 c. broken nuts (pecans)",
#             "2 Tbsp. butter or margarine",
#             "3 1/2 c. bite size shredded rice biscuits"
#         ],
#         "directions": [
#             "In a heavy 2-quart saucepan, mix brown sugar, nuts, evaporated milk and butter or margarine.",
#             "Stir over medium heat until mixture bubbles all over top.",
#             "Boil and stir 5 minutes more. Take off heat.",
#             "Stir in vanilla and cereal; mix well.",
#             "Using 2 teaspoons, drop and shape into 30 clusters on wax paper.",
#             "Let stand until firm, about 30 minutes."
#         ],
#         "cleaned_ingredients": [
#             "firmly packed brown sugar",
#             "evaporated milk",
#             "vanilla",
#             "broken nuts (pecans)",
#             "butter or margarine",
#             "shredded rice biscuits"
#         ]
#     }
    
#     print("=== Recipe Samples ===")
#     result = await generate_recipe_samples(recipe)
#     print(result)
    
#     print("\n=== Ingredient Extraction Samples ===")
#     result = await generate_ingredient_extraction_samples(recipe)
#     print(result)
    
#     print("\n=== Constraint Generator Samples ===")
#     result = await constraint_generator_samples(recipe)
#     print(result)
    
#     print("\n=== Recipe Summary Samples ===")
#     result = await recipe_summary_samples(recipe)
#     print(result)
    
#     print("\n=== QA Pair Samples ===")
#     result = await generate_qa_pair_samples(recipe)
#     print(result)

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())