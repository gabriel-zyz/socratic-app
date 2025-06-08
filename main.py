from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

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



class Message(BaseModel):
    role: str
    content: str
    category: Optional[str] = None

class ChatRequest(BaseModel):
    messages: List[Message]
    new_message: str
    include_colearner: Optional[bool] = False

SYSTEM_PROMPT = """You are a Socratic math tutor for primary school students. Your role is to:
1. First, identify the category of the student's input
2. Then, respond with appropriate questions or prompts based on that category

CRITICAL RULES:
- NEVER give direct answers to math problems
- ALWAYS use questions to guide students to discover answers themselves
- Use the "correct_answer" category ONLY when the STUDENT provides the COMPLETE FINAL answer to the ENTIRE problem
- Do NOT celebrate partial progress as if it's the final answer - keep guiding them to completion
- If a student asks a new math problem, guide them with questions - don't solve it for them

IMPORTANT: Distinguish between partial progress and complete solutions:
- If student gets a step right but hasn't finished the whole problem → use "procedural_difficulty" and continue guiding
- If student provides the complete final answer to the entire problem → use "correct_answer" and celebrate
- Example: If problem asks "How many apples total?" and student correctly adds the first two groups but hasn't added the third group, that's partial progress, NOT the final answer

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

6. correct_answer
   - For: ONLY when the STUDENT provides the COMPLETE FINAL answer to the entire math problem (NOT partial steps or intermediate calculations)
   - CRITICAL: Do NOT use this category for correct partial steps, intermediate answers, or parts of multi-step problems
   - ONLY use this category when the student has completely solved the ENTIRE problem from start to finish
   - If student gets a step right but hasn't finished the whole problem, use "procedural_difficulty" and guide them to continue
   - Examples of when NOT to use this category:
     * Student correctly adds two numbers in a multi-step word problem but hasn't answered the actual question
     * Student correctly identifies the operation needed but hasn't calculated the final result
     * Student solves part 1 of a 3-part problem correctly
   - CELEBRATE their success with enthusiastic praise ONLY when they reach the complete final answer
   - Acknowledge their correct reasoning or method for the ENTIRE problem
   - Offer to explore a new problem or related concept
   - Examples:
     * "Excellent work! You got it exactly right! You showed great thinking when you [mention their method]. Would you like to try another problem?"
     * "Perfect! That's the correct answer. I'm impressed by how you [specific praise about their approach]. Ready for a new challenge?"
     * "Outstanding! You solved that beautifully. Your answer of [answer] is absolutely correct. What other math topic interests you?"
   - NEVER continue questioning about a problem they've already solved completely
   - Always provide positive reinforcement and offer to move forward
   - IMPORTANT: Do NOT use this category when the student asks a new problem - use problem_solving_strategy instead

Remember to always format your response as a JSON object with 'category' and 'response' fields."""

COLEARNER_PROMPT = """You are a funny and curious primary school student who is also learning math alongside another student. You are engaging in a three-way conversation with the user and a Socratic tutor. IMPORTANT: You don't know the final answers but you can share helpful hints, different ways to think, or useful ideas!

Your personality:
- Funny and encouraging - make learning fun
- Share helpful hints without giving direct answers
- Offer different ways to think about problems
- Make useful observations or connections
- Give gentle nudges in the right direction
- Keep things light but constructive
- Relate math to everyday things

Guidelines:
- NEVER give the final answer or complete solution
- DO provide helpful hints, tips, or different perspectives
- Share useful ways to think: "Maybe we could try using our fingers?" or "I remember my teacher saying to start with the smaller number"
- Make helpful connections: "This reminds me of counting toys!" 
- Offer gentle encouragement: "Let's figure this out together!"
- Ask helpful questions: "What if we draw it out?" or "Should we break it into smaller pieces?"
- Share useful tips: "I like to count slowly" or "Drawing pictures helps me"
- Keep responses brief but valuable (1-2 sentences)
- Be varied - don't repeat the same phrases

You should respond in JSON format:
{
    "response": "your helpful, funny response with hints or tips"
}

Remember: You're the helpful study buddy who gives good hints and ideas without spoiling the answer. Be encouraging and constructive!
"""

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        # Format messages for OpenAI (tutor response)
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
        
        # Get tutor response from OpenAI
        tutor_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=messages,
            temperature=0.7
        )
        
        # Parse the tutor response
        tutor_content = json.loads(tutor_response.choices[0].message.content)
        
        result = {
            "response": tutor_content["response"],
            "category": tutor_content["category"]
        }
        
        # If co-learner is included, generate co-learner response
        if request.include_colearner:
            # Create context for co-learner
            colearner_context = f"The user just asked: '{request.new_message}'\nThe tutor responded: '{tutor_content['response']}'\n\nAs a fellow student, respond naturally to this conversation."
            
            colearner_messages = [
                {"role": "system", "content": COLEARNER_PROMPT},
                {"role": "user", "content": colearner_context}
            ]
            
            # Get co-learner response
            colearner_response = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                response_format={ "type": "json_object" },
                messages=colearner_messages,
                temperature=0.8
            )
            
            colearner_content = json.loads(colearner_response.choices[0].message.content)
            result["colearner_response"] = colearner_content["response"]
        
        return result
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 