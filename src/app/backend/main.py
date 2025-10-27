from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AsyncOpenAI
from typing import Optional, List
from .config import config

app = FastAPI(title="Cook Assistant API", version="1.0.0")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AsyncOpenAI client with Modal endpoint
client = AsyncOpenAI(
    api_key=config.MODAL_API_KEY,
    base_url=config.MODAL_BASE_URL
)

class RecipeRequest(BaseModel):
    ingredients: List[str]
    additional_instructions: Optional[str] = None
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = 1024

class RecipeResponse(BaseModel):
    recipe: str
    ingredients_used: List[str]
    model: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[dict]] = None
    temperature: Optional[float] = 1.0

class ChatResponse(BaseModel):
    response: str
    model: str

@app.get("/")
async def root():
    return {
        "message": "Cook Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "/generate-recipe": "POST - Generate a recipe from ingredients",
            "/chat": "POST - Chat with the cooking assistant",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Try to list models to verify connection
        models = await client.models.list()
        model_list = [model.id for model in models.data]
        return {
            "status": "healthy",
            "modal_connection": "connected",
            "available_models": model_list
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

@app.post("/generate-recipe", response_model=RecipeResponse)
async def generate_recipe(request: RecipeRequest):
    """
    Generate a recipe from a list of ingredients.
    """
    try:
        # Get the available model
        models = await client.models.list()
        model_id = models.data[0].id if models.data else "unknown"
        
        # Format ingredients
        ingredients_text = ", ".join(request.ingredients)
        
        # Create the user message
        user_content = f"Generate a recipe using the following ingredients: {ingredients_text}. Include a title and clear steps."
        
        if request.additional_instructions:
            user_content += f" Additional requirements: {request.additional_instructions}"
        
        # Create messages
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that generates recipe samples from a given set of ingredients."
            },
            {
                "role": "user",
                "content": user_content
            }
        ]
        
        # Get completion from Modal endpoint
        response = await client.chat.completions.create(
            model=model_id,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=False,
            seed=config.DEFAULT_SEED
        )
        
        # Extract the recipe
        recipe_text = response.choices[0].message.content
        
        # Remove thinking tags if present
        if "</think>" in recipe_text:
            recipe_text = recipe_text.split("</think>", 1)[-1].lstrip()
        
        return RecipeResponse(
            recipe=recipe_text,
            ingredients_used=request.ingredients,
            model=model_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recipe: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the cooking assistant.
    """
    try:
        # Get the available model
        models = await client.models.list()
        model_id = models.data[0].id if models.data else "unknown"
        
        # Build conversation history
        messages = [
            {
                "role": "system",
                "content": "You are a helpful cooking assistant. You can help with recipes, cooking techniques, ingredient substitutions, and general cooking advice."
            }
        ]
        
        # Add conversation history if provided
        if request.conversation_history:
            messages.extend(request.conversation_history)
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": request.message
        })
        
        # Get completion from Modal endpoint
        response = await client.chat.completions.create(
            model=model_id,
            messages=messages,
            temperature=request.temperature,
            stream=False,
            seed=config.DEFAULT_SEED
        )
        
        # Extract response
        assistant_message = response.choices[0].message.content
        
        # Remove thinking tags if present
        if "</think>" in assistant_message:
            assistant_message = assistant_message.split("</think>", 1)[-1].lstrip()
        
        return ChatResponse(
            response=assistant_message,
            model=model_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

