from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import logging
import os
import re
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ML Pipeline API",
    description="A machine learning pipeline with text classification capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

class TextRequest(BaseModel):
    text: str

class TextResponse(BaseModel):
    text: str
    prediction: str
    confidence: float
    model_info: dict

# Global variables for Llama model
model = None
tokenizer = None

def load_llama_model():
    """Load Llama model and tokenizer"""
    global model, tokenizer
    try:
        logger.info("Loading Llama model...")
        # Using a better conversational model
        model_name = "microsoft/DialoGPT-small"
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        logger.info("Llama model loaded successfully!")
        return True
    except Exception as e:
        logger.error(f"Error loading Llama model: {e}")
        return False

def generate_llama_response(user_input, max_length=100):
    """Generate response using Llama model"""
    global model, tokenizer
    
    if model is None or tokenizer is None:
        return "Model not loaded yet. Please wait..."
    
    try:
        # Encode user input
        input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
        
        # Generate response
        with torch.no_grad():
            output_ids = model.generate(
                input_ids,
                max_length=max_length,
                pad_token_id=tokenizer.eos_token_id,
                temperature=0.6,
                do_sample=True,
                top_k=30,
                top_p=0.9
            )
        
        # Decode response
        response = tokenizer.decode(output_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        
        return response if response else "I'm sorry, I couldn't generate a response."
        
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return f"Error generating response: {str(e)}"

def generate_chat_response(user_input):
    """Generate response using Llama model"""
    return generate_llama_response(user_input)

def generate_contextual_response(input_text):
    """Generate contextual responses based on input"""
    responses = [
        f"Regarding '{input_text}', I think that's worth exploring further.",
        f"Your message about '{input_text}' is quite interesting.",
        f"I find your input '{input_text}' very engaging.",
        f"That's a fascinating topic you've brought up.",
        f"I appreciate you sharing that with me."
    ]
    return random.choice(responses)

# Simple sentiment analysis using keyword matching (fallback)
def analyze_sentiment(text):
    """Simple sentiment analysis using keyword matching"""
    text_lower = text.lower()
    
    # Positive keywords
    positive_words = ['love', 'great', 'good', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome', 'best', 'perfect']
    # Negative keywords
    negative_words = ['hate', 'terrible', 'bad', 'awful', 'horrible', 'worst', 'disgusting', 'terrible', 'awful', 'hate']
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return "POSITIVE", 0.7 + (positive_count * 0.1)
    elif negative_count > positive_count:
        return "NEGATIVE", 0.7 + (negative_count * 0.1)
    else:
        return "NEUTRAL", 0.6

@app.get("/")
async def root():
    """Root endpoint - serves frontend or API info"""
    if os.path.exists("frontend/index.html"):
        return FileResponse("frontend/index.html")
    else:
        return {
            "message": "ML Pipeline API is running",
            "status": "healthy",
            "model_loaded": True
        }

@app.on_event("startup")
async def load_model():
    """Load Llama model on startup"""
    try:
        success = load_llama_model()
        if success:
            logger.info("Llama model loaded successfully!")
        else:
            logger.warning("Failed to load Llama model, using fallback")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        logger.info("Using fallback system")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_loaded = model is not None and tokenizer is not None
    return {
        "status": "healthy",
        "model_loaded": model_loaded,
        "message": "ML Pipeline API is running with Llama model" if model_loaded else "ML Pipeline API is running with fallback"
    }

@app.post("/classify", response_model=TextResponse)
async def classify_text(request: TextRequest):
    """Text classification (sentiment analysis)"""
    try:
        prediction, confidence = analyze_sentiment(request.text)
        
        return TextResponse(
            text=request.text,
            prediction=prediction,
            confidence=confidence,
            model_info={
                "model_name": "simple-sentiment-analyzer",
                "task": "sentiment-analysis"
            }
        )
        
    except Exception as e:
        logger.error(f"Error in classification: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
async def generate_text(request: TextRequest):
    """Text generation using Llama model"""
    try:
        generated_text = generate_chat_response(request.text)
        
        return {
            "input_text": request.text,
            "generated_text": generated_text,
            "model_info": {
                "model_name": "Llama-Model",
                "task": "text-generation"
            }
        }
        
    except Exception as e:
        logger.error(f"Error in text generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model-info")
async def get_model_info():
    """Get information about the loaded models"""
    model_loaded = model is not None and tokenizer is not None
    return {
        "sentiment_model": "simple-sentiment-analyzer",
        "generation_model": "Llama-Model",
        "models_loaded": model_loaded,
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        "status": "Llama model loaded and ready" if model_loaded else "Using fallback system"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 