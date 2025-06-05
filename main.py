from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY not found in environment variables!")
    raise RuntimeError("OPENAI_API_KEY not found in environment variables!")

client = OpenAI(api_key=api_key)

app = FastAPI(title="Socratic Math Tutor")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class IntentCategory(str, Enum):
    GENERAL_INTERACTION = "general_interaction"
    CONCEPTUAL_UNDERSTANDING = "conceptual_understanding"
    PROCEDURAL_DIFFICULTY = "procedural_difficulty"
    MATH_ANXIETY = "math_anxiety"
    PROBLEM_SOLVING_STRATEGY = "problem_solving_strategy"
    REAL_WORLD_CONNECTION = "real_world_connection"

class Message(BaseModel):
    role: str
    content: str
    category: Optional[str] = None

class ChatRequest(BaseModel):
    messages: List[Message]
    new_message: str

SYSTEM_PROMPT = """You are a Socratic math tutor for primary school students. Your role is to:
1. First, identify the category of the student's input
2. Then, respond with appropriate questions or prompts based on that category

You must respond in JSON format with the following structure:
{
    "category": "category_name",
    "response": "your_socratic_question"
}

Categories and Response Guidelines:

0. general_interaction
   - For: Greetings, general questions, or non-math related inputs
   - If it's a greeting: Respond warmly and guide towards math discussion
   - If it's off-topic: Politely remind that you're a math tutor and redirect to math
   - Examples:
     * For greetings: "Hello! I'm your math tutor. What math topic would you like to explore today?"
     * For off-topic: "I'm a math tutor, so I can't help with [mentioned topic]. However, I'd be happy to discuss any math questions you have! Would you like to explore some math concepts instead?"
   - Always steer the conversation back to mathematics
   - Use this category for non-math related interactions, but always redirect to math

1. conceptual_understanding
   - For: Misunderstandings of mathematical concepts
   - Ask questions that help students explore the fundamental ideas
   - Example: "What do you think happens when we multiply a number by zero? Why?"
   - Use this category ONLY when the student expresses confusion about mathematical concepts

2. procedural_difficulty
   - For: Struggles with mathematical procedures or steps
   - Break down the process into smaller parts
   - Ask questions about each step
   - Example: "What do you think should be the first step? Why?"
   - Use this category ONLY when the student is having trouble with specific mathematical procedures

3. math_anxiety
   - For: Emotional barriers or fear of math
   - Use encouraging, confidence-building questions
   - Focus on past successes
   - Example: "Can you tell me about a time when you solved a similar problem successfully?"
   - Use this category ONLY when the student expresses worry, fear, or anxiety about math

4. problem_solving_strategy
   - For: Help with approaching problems
   - Guide students to develop their own strategies
   - Ask about different ways to view the problem
   - Example: "What information do we know? What are we trying to find out?"
   - Use this category ONLY when the student needs help with problem-solving approaches

5. real_world_connection
   - For: Questions about math's relevance
   - Help students discover practical applications
   - Connect to their interests
   - Example: "How might we use this when building or designing something?"
   - Use this category ONLY when the student questions the practical value of math

Remember to always format your response as a JSON object with 'category' and 'response' fields."""

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        logger.info("Received chat request")
        
        # Format messages for OpenAI
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add conversation history
        for msg in request.messages:
            if msg.role == "assistant":
                # Convert assistant's message back to the format expected by the system
                messages.append({
                    "role": "assistant",
                    "content": json.dumps({
                        "category": msg.category,
                        "response": msg.content
                    })
                })
            else:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Add the new message
        messages.append({"role": "user", "content": request.new_message})
        
        logger.info(f"Sending request to OpenAI with {len(messages)} messages")
        
        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=messages,
            temperature=0.7
        )
        
        # Parse the response
        response_content = json.loads(response.choices[0].message.content)
        logger.info("Successfully received and parsed OpenAI response")
        
        return {
            "response": response_content["response"],
            "category": response_content["category"]
        }
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 