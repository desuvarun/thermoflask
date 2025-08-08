#!/usr/bin/env python3
"""
Test script for the ML Pipeline API
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_classify():
    """Test the text classification endpoint"""
    print("\nTesting text classification...")
    test_texts = [
        "I love this movie!",
        "This is terrible.",
        "The weather is nice today."
    ]
    
    for text in test_texts:
        try:
            response = requests.post(
                f"{BASE_URL}/classify",
                json={"text": text}
            )
            print(f"Text: {text}")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Prediction: {result['prediction']}")
                print(f"Confidence: {result['confidence']:.3f}")
            else:
                print(f"Error: {response.text}")
            print("-" * 50)
        except Exception as e:
            print(f"Error: {e}")

def test_generate():
    """Test the text generation endpoint"""
    print("\nTesting text generation...")
    test_text = "Hello, how are you?"
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate",
            json={"text": test_text}
        )
        print(f"Input: {test_text}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Generated class: {result['generated_class']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def test_model_info():
    """Test the model info endpoint"""
    print("\nTesting model info...")
    try:
        response = requests.get(f"{BASE_URL}/model-info")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Models loaded: {result['models_loaded']}")
            print(f"Device: {result['device']}")
            print(f"Sentiment model: {result['sentiment_model']}")
            print(f"Generation model: {result['generation_model']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def wait_for_service():
    """Wait for the service to be ready"""
    print("Waiting for service to be ready...")
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("Service is ready!")
                return True
        except:
            pass
        print(f"Attempt {attempt + 1}/{max_attempts} - waiting...")
        time.sleep(2)
    
    print("Service failed to start within expected time")
    return False

if __name__ == "__main__":
    print("ML Pipeline API Test Suite")
    print("=" * 50)
    
    if not wait_for_service():
        print("Exiting due to service unavailability")
        exit(1)
    
    test_health()
    test_classify()
    test_generate()
    test_model_info()
    
    print("\nTest suite completed!") 