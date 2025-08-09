# ML Pipeline with Docker and Open Web UI

A complete machine learning pipeline built with FastAPI, Docker, and Open Web UI frontend. This project uses small text-based models from Hugging Face for sentiment analysis and text generation.

## 🚀 Features

- **FastAPI Backend**: RESTful API with sentiment analysis and text generation
- **LLaMA-family Generation**: Uses the TinyLlama chat model for `/generate`
- **Docker Containerization**: Complete containerized environment
- **Open Web UI Frontend**: Modern web interface for interaction
- **Nginx Reverse Proxy**: Unified access point for all services
- **Health Monitoring**: Built-in health checks and monitoring

## 📋 Prerequisites

- Python 3.9+ (for local, no-Docker run)
- Docker and Docker Compose (for containerized run)
- At least 4–6GB RAM recommended
- Internet connection for first-time model downloads

## 🏗️ Project Structure

```
thermoflask/
├── app.py                    # FastAPI application (TinyLlama for generation)
├── app_simple.py             # Lightweight mock API (no model downloads)
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Multi-service orchestration
├── docker-compose.prod.yml  # Production configuration
├── nginx.conf              # Nginx reverse proxy config
├── test_api.py             # API testing script
├── start.sh                # Quick start script
├── stop.sh                 # Quick stop script
├── frontend/
│   └── index.html         # Simple web frontend
└── README.md              # This file
```

## 🚀 Quick Start

### A) Run Locally (no Docker)

```bash
# 1) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Start the FastAPI app (TinyLlama downloads on first run)
uvicorn app:app --host 0.0.0.0 --port 8000

# 4) Open in browser
open http://localhost:8000/docs  # FastAPI docs
```

- The first run will download the TinyLlama model; this may take a few minutes.
- If you only want a lightweight mock API (no model download), start:

```bash
uvicorn app_simple:app --host 0.0.0.0 --port 8000
```

### B) Run with Docker

```bash
# Quick start (recommended)
./start.sh

# Or manually build and start all services
# If you have the plugin:  docker compose up --build
# If you have the legacy CLI: docker-compose up --build
```

Note: Ensure Docker Desktop is running before executing the commands above.

### Access the Application

Once services are running, you can access:

- **Main Application**: http://localhost
- **API Documentation**: http://localhost/docs or http://localhost/api/docs
- **Health Check**: http://localhost/health
- **Direct API**: http://localhost:8000

### Test the API

```bash
# Ensure the server is running on :8000, then run:
python test_api.py
```

Note: the test script expects a field named `generated_class`, while the API returns `generated_text`. Generation will succeed, but that line shows an error in the script output; it does not affect the service. You can test generation directly (see below).

## 🚀 Quick Commands

### Start/Stop Scripts

```bash
# Quick start
./start.sh

# Quick stop
./stop.sh

# Production mode
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 🔧 Individual Service Commands

### ML API Service

```bash
# Build the ML API image
docker build -t ml-pipeline .

# Run the ML API container
docker run -p 8000:8000 ml-pipeline

# View logs
docker-compose logs ml-api

# Restart the service
docker-compose restart ml-api
```

### Open Web UI

```bash
# Access Open Web UI directly
docker run -p 3000:8080 ghcr.io/open-webui/open-webui:main

# View logs
docker-compose logs open-webui

# Quick stop
./stop.sh
```

### Nginx Proxy

```bash
# Test nginx configuration
docker-compose exec nginx nginx -t

# Reload nginx configuration
docker-compose exec nginx nginx -s reload
```

## 📊 API Endpoints

### Health Check
```bash
GET /health
```

### Text Classification (Sentiment Analysis)
```bash
POST /classify
Content-Type: application/json

{
    "text": "I love this movie!"
}
```

### Text Generation (TinyLlama)
```bash
POST /generate
Content-Type: application/json

{
    "text": "Say hi in a friendly way."
}

# Example curl
curl -s -X POST http://localhost:8000/generate \
  -H 'Content-Type: application/json' \
  -d '{"text":"Say hi in a friendly way."}'
```

### Model Information
```bash
GET /model-info
```

## 🔍 Monitoring and Debugging

### View Service Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs ml-api
docker-compose logs open-webui
docker-compose logs nginx

# Follow logs in real-time
docker-compose logs -f ml-api
```

### Check Service Status

```bash
# List running containers
docker-compose ps

# Check container health
docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
```

### Access Container Shell

```bash
# Access ML API container
docker-compose exec ml-api bash

# Access nginx container
docker-compose exec nginx sh
```

## 🛠️ Development Commands

### Local Development

```bash
# Install dependencies locally
pip install -r requirements.txt

# Run FastAPI locally (TinyLlama)
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Lightweight mock mode (no model download)
uvicorn app_simple:app --reload --host 0.0.0.0 --port 8000

# Test API locally
python test_api.py
```

### Docker Development

```bash
# Rebuild without cache
docker-compose build --no-cache

# Run in detached mode
docker-compose up -d

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 🔧 Configuration

### Environment Variables

You can customize the behavior by setting environment variables:

```bash
# In docker-compose.yml
environment:
  - PYTHONUNBUFFERED=1
  - WEBUI_SECRET_KEY=your-secret-key-here
```

### Model Configuration

The application uses these models by default:
- **Sentiment Analysis**: simple keyword-based analyzer (in-code fallback)
- **Text Generation**: `TinyLlama/TinyLlama-1.1B-Chat-v1.0`

To change the generation model, edit `app.py` in `load_llama_model()`:

```python
# app.py
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # replace with your preferred HF model
```

## 🐛 Troubleshooting

### Common Issues

1. **First run is slow / model download**
   - TinyLlama is downloaded on first startup. Ensure internet connectivity.
   - Subsequent runs use the local cache and are faster.

2. **LibreSSL / urllib3 warning on macOS**
   - You may see `NotOpenSSLWarning` from `urllib3`. This is harmless for local development.

3. **Port Already in Use**
   ```bash
   lsof -i :8000
   lsof -i :80
   ```

4. **Service Not Starting (Docker)**
   ```bash
   docker-compose logs ml-api
   docker-compose down && docker-compose up --build
   ```

### Performance Optimization

```bash
# Use GPU if available (requires nvidia-docker)
# Add to docker-compose.yml:
runtime: nvidia
environment:
  - NVIDIA_VISIBLE_DEVICES=all

# Optimize for production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

## 📈 Scaling

### Horizontal Scaling

```bash
# Scale ML API service
docker-compose up --scale ml-api=3

# Scale with load balancer
docker-compose -f docker-compose.yml -f docker-compose.scale.yml up
```

## 🔒 Security Considerations

1. **Change Default Secrets**: Update `WEBUI_SECRET_KEY` in production
2. **Network Security**: Use internal Docker networks for service communication
3. **API Security**: Implement authentication for production use
4. **Model Security**: Validate input data to prevent injection attacks

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review logs (`docker-compose logs` or the terminal where you ran `uvicorn`)
3. Open an issue on the repository

---

**Note**: The first run may take several minutes as it downloads the TinyLlama model from Hugging Face. Subsequent runs will be faster as the model is cached. 