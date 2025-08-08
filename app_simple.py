from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import logging
import os

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

@app.get("/")
async def root():
    """Root endpoint - serves frontend or API info"""
    if os.path.exists("frontend/index.html"):
        return FileResponse("frontend/index.html")
    else:
        return {
            "message": "ML Pipeline API is running",
            "status": "healthy",
            "model_loaded": False
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": False,
        "message": "Basic API is running (ML models not loaded yet)"
    }

@app.post("/classify", response_model=TextResponse)
async def classify_text(request: TextRequest):
    """Mock text classification for testing"""
    try:
        # Simple mock sentiment analysis
        text = request.text.lower()
        if any(word in text for word in ['love', 'great', 'good', 'excellent', 'amazing']):
            prediction = "POSITIVE"
            confidence = 0.85
        elif any(word in text for word in ['hate', 'terrible', 'bad', 'awful', 'horrible']):
            prediction = "NEGATIVE"
            confidence = 0.80
        else:
            prediction = "NEUTRAL"
            confidence = 0.60
        
        return TextResponse(
            text=request.text,
            prediction=prediction,
            confidence=confidence,
            model_info={
                "model_name": "mock-sentiment-analyzer",
                "task": "sentiment-analysis"
            }
        )
        
    except Exception as e:
        logger.error(f"Error in classification: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
async def generate_text(request: TextRequest):
    """Mock text generation for testing"""
    try:
        return {
            "input_text": request.text,
            "generated_text": f"Mock response to: {request.text}",
            "model_info": {
                "model_name": "mock-text-generator",
                "task": "text-generation"
            }
        }
        
    except Exception as e:
        logger.error(f"Error in text generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model-info")
async def get_model_info():
    """Get information about the loaded models"""
    return {
        "sentiment_model": "mock-sentiment-analyzer",
        "generation_model": "mock-text-generator",
        "models_loaded": False,
        "device": "cpu",
        "status": "Mock mode - real models not loaded"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 