# we will create subset of dataset for each task
# recipe samples from ingredients -> 51k (sourced from first 100K samples)
# generate_ingredient_extraction_samples -> 20k (sourced from second 20K samples)
# constraint_generator_samples -> 30k (sourced from third 30K samples)
# recipe_summary_samples -> 10k (sourced from fourth 10K samples)
# generate_qa_pair_samples -> 40k (sourced from fifth 40K samples)

import asyncio
import json
from src.utils.data_generators import generate_recipe_samples, generate_ingredient_extraction_samples, constraint_generator_samples, recipe_summary_samples, generate_qa_pair_samples
from src.utils.io_utils import load_json, save_json, save_jsonl
from tqdm.asyncio import tqdm_asyncio
from tqdm import tqdm

async def create_dataset_subsets():
    # load the datasets
    dataset_with_ingredient_NER = load_json("dataset/recipes_proc_NER_1k_1.json")
    full_dataset = load_json("dataset/recipes_processed.json")[100000:]
    # create subset of dataset for each task
    recipe_generation_dataset = dataset_with_ingredient_NER
    ingredient_extraction_dataset = dataset_with_ingredient_NER[:5000] + full_dataset[:20000]
    constraint_generator_dataset = dataset_with_ingredient_NER[45000:50000] + full_dataset[20000:23000]
    recipe_summary_dataset = dataset_with_ingredient_NER[10000:20000] + full_dataset[32000:42000]
    generate_qa_pair_dataset = dataset_with_ingredient_NER[30000:35000] + full_dataset[62000:65000]
    # save the datasets
    save_json(recipe_generation_dataset, "dataset/processed/recipe_generation_dataset.json")
    save_json(ingredient_extraction_dataset, "dataset/processed/ingredient_extraction_dataset.json")
    save_json(constraint_generator_dataset, "dataset/processed/constraint_generator_dataset.json")
    save_json(recipe_summary_dataset, "dataset/processed/recipe_summary_dataset.json")
    save_json(generate_qa_pair_dataset, "dataset/processed/generate_qa_pair_dataset.json")
    print("============================================ Datasets created successfully =============================================")
    print(f"Recipe Generation Dataset: {len(recipe_generation_dataset)}")
    print(f"Ingredient Extraction Dataset: {len(ingredient_extraction_dataset)}")
    print(f"Constraint Generator Dataset: {len(constraint_generator_dataset)}")
    print(f"Recipe Summary Dataset: {len(recipe_summary_dataset)}")
    print(f"Generate QA Pair Dataset: {len(generate_qa_pair_dataset)}")

async def process_dataset_with_generator(recipes, generator_func, task_name, max_concurrent=10):
    """
    Process a dataset concurrently with a generator function and show progress.
    
    Args:
        recipes: List of recipe dictionaries
        generator_func: Async function to generate instruction samples
        task_name: Name of the task for progress bar
        max_concurrent: Maximum concurrent tasks
    
    Returns:
        List of generated instruction samples
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_with_semaphore(recipe):
        async with semaphore:
            try:
                return await generator_func(recipe)
            except Exception as e:
                print(f"\nError processing recipe in {task_name}: {e}")
                return None
    
    # Create tasks with progress bar
    tasks = [process_with_semaphore(recipe) for recipe in recipes]
    results = []
    
    # Use tqdm.asyncio.gather for progress tracking
    for coro in tqdm_asyncio.as_completed(tasks, desc=task_name, total=len(tasks)):
        result = await coro
        if result is not None:
            results.append(result)
    
    return results

async def create_instruction_tuned_dataset():
    """
    Create instruction tuned dataset by processing all subset datasets concurrently.
    Each dataset is processed with its corresponding generator function.
    """
    print("Loading datasets...")
    # load the datasets
    recipe_generation_dataset = load_json("dataset/processed/recipe_generation_dataset.json")
    ingredient_extraction_dataset = load_json("dataset/processed/ingredient_extraction_dataset.json")
    constraint_generator_dataset = load_json("dataset/processed/constraint_generator_dataset.json")
    recipe_summary_dataset = load_json("dataset/processed/recipe_summary_dataset.json")
    generate_qa_pair_dataset = load_json("dataset/processed/generate_qa_pair_dataset.json")
    
    print(f"\nDataset sizes:")
    print(f"  Recipe Generation: {len(recipe_generation_dataset)}")
    print(f"  Ingredient Extraction: {len(ingredient_extraction_dataset)}")
    print(f"  Constraint Generator: {len(constraint_generator_dataset)}")
    print(f"  Recipe Summary: {len(recipe_summary_dataset)}")
    print(f"  QA Pair Generation: {len(generate_qa_pair_dataset)}")
    print(f"\nTotal recipes to process: {len(recipe_generation_dataset) + len(ingredient_extraction_dataset) + len(constraint_generator_dataset) + len(recipe_summary_dataset) + len(generate_qa_pair_dataset)}")
    
    print("\n" + "="*80)
    print("Processing datasets concurrently with progress bars...")
    print("="*80 + "\n")
    
    # Process all datasets concurrently with their respective generator functions
    results = await asyncio.gather(
        process_dataset_with_generator(
            recipe_generation_dataset, 
            generate_recipe_samples, 
            "Recipe Generation",
            max_concurrent=50
        ),
        process_dataset_with_generator(
            ingredient_extraction_dataset, 
            generate_ingredient_extraction_samples, 
            "Ingredient Extraction",
            max_concurrent=50
        ),
        process_dataset_with_generator(
            constraint_generator_dataset, 
            constraint_generator_samples, 
            "Constraint Generator",
            max_concurrent=30  # Lower concurrency for API-heavy tasks
        ),
        process_dataset_with_generator(
            recipe_summary_dataset, 
            recipe_summary_samples, 
            "Recipe Summary",
            max_concurrent=30  # Lower concurrency for API-heavy tasks
        ),
        process_dataset_with_generator(
            generate_qa_pair_dataset, 
            generate_qa_pair_samples, 
            "QA Pair Generation",
            max_concurrent=30  # Lower concurrency for API-heavy tasks
        )
    )
    
    # Unpack results
    recipe_gen_results, ingredient_ext_results, constraint_gen_results, recipe_sum_results, qa_pair_results = results
    
    # Merge all results into final dataset
    print("\n" + "="*80)
    print("Merging datasets...")
    final_dataset = (
        recipe_gen_results + 
        ingredient_ext_results + 
        constraint_gen_results + 
        recipe_sum_results + 
        qa_pair_results
    )
    
    print(f"Total samples in final dataset: {len(final_dataset)}")
    
    # Save the final conversational dataset
    output_path = "dataset/processed/instruction_tuned_dataset.json"
    print(f"\nSaving final dataset to {output_path}...")
    save_json(final_dataset, output_path)
    
    print("\n" + "="*80)
    print("✓ Instruction tuned dataset created successfully!")
    print("="*80)
    print(f"\nFinal Dataset Statistics:")
    print(f"  Recipe Generation samples: {len(recipe_gen_results)}")
    print(f"  Ingredient Extraction samples: {len(ingredient_ext_results)}")
    print(f"  Constraint Generator samples: {len(constraint_gen_results)}")
    print(f"  Recipe Summary samples: {len(recipe_sum_results)}")
    print(f"  QA Pair Generation samples: {len(qa_pair_results)}")
    print(f"  Total samples: {len(final_dataset)}")
    print(f"\nDataset saved to: {output_path}")
    
    return final_dataset



async def convert_conversations():
    """
    Convert a list of conversations (each conversation is a list of message dicts)
    into a list of dicts with the key 'conversations' -> list[ {role, content}, ... ].
    """
    with open('Cook-Assistant/dataset/processed/instruction_tuned_dataset.json', 'r') as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Input must be a list of conversations.")
    for i, convo in enumerate(data):
        if not isinstance(convo, list):
            raise ValueError(f"Conversation at index {i} must be a list of message dicts.")
        for j, msg in enumerate(convo):
            if not isinstance(msg, dict):
                raise ValueError(f"Message at conversation {i}, index {j} must be a dict.")
            if "role" not in msg or "content" not in msg:
                raise ValueError(f"Message at conversation {i}, index {j} must have 'role' and 'content' keys.")
    save_jsonl(data, "dataset/processed/instruction_tuned_dataset_processed.jsonl")
    return [{"conversations": convo} for convo in data]



if __name__ == "__main__":
    asyncio.run(create_dataset_subsets())
    # Run the dataset creation pipeline
    asyncio.run(create_instruction_tuned_dataset())
    asyncio.run(convert_conversations())
