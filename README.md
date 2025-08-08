# ML Pipeline with Docker and Open Web UI

A complete machine learning pipeline built with FastAPI, Docker, and Open Web UI frontend. This project uses small text-based models from Hugging Face for sentiment analysis and text generation.

## 🚀 Features

- **FastAPI Backend**: RESTful API with sentiment analysis and text generation
- **Small Text Models**: Uses lightweight models from Hugging Face
- **Docker Containerization**: Complete containerized environment
- **Open Web UI Frontend**: Modern web interface for interaction
- **Nginx Reverse Proxy**: Unified access point for all services
- **Health Monitoring**: Built-in health checks and monitoring

## 📋 Prerequisites

- Docker and Docker Compose installed
- At least 4GB RAM available
- Internet connection for model downloads

## 🏗️ Project Structure

```
thermoflask/
├── app.py                    # FastAPI application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Multi-service orchestration
├── docker-compose.prod.yml  # Production configuration
├── nginx.conf              # Nginx reverse proxy config
├── test_api.py             # API testing script
├── start.sh                # Quick start script
├── stop.sh                 # Quick stop script
├── .dockerignore           # Docker ignore file
├── frontend/
│   └── index.html         # Simple web frontend
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Build and Start Services

```bash
# Clone or navigate to the project directory
cd thermoflask

# Quick start (recommended)
./start.sh

# Or manually build and start all services
docker-compose up --build
```

### 2. Access the Application

Once all services are running, you can access:

- **Main Application**: http://localhost
- **API Documentation**: http://localhost/api/docs
- **Health Check**: http://localhost/health
- **Direct API**: http://localhost:8000

### 3. Test the API

```bash
# Run the test script
python test_api.py

# Or test via the web frontend
# Open http://localhost in your browser
```

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

### Text Generation
```bash
POST /generate
Content-Type: application/json

{
    "text": "Hello, how are you?"
}
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

# Run FastAPI locally
uvicorn app:app --reload --host 0.0.0.0 --port 8000

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
- **Sentiment Analysis**: `distilbert-base-uncased-finetuned-sst-2-english`
- **Text Generation**: `microsoft/DialoGPT-small`

To change models, modify the `app.py` file:

```python
# Change model names in the load_model() function
classifier_name = "your-preferred-sentiment-model"
model_name = "your-preferred-generation-model"
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :8000
   lsof -i :80
   
   # Stop conflicting services
   sudo systemctl stop nginx  # if nginx is running locally
   ```

2. **Model Download Issues**
   ```bash
   # Check internet connectivity
   docker-compose exec ml-api ping huggingface.co
   
   # Clear Docker cache
   docker system prune -a
   ```

3. **Memory Issues**
   ```bash
   # Check memory usage
   docker stats
   
   # Increase Docker memory limit in Docker Desktop settings
   ```

4. **Service Not Starting**
   ```bash
   # Check detailed logs
   docker-compose logs ml-api
   
   # Restart with fresh build
   docker-compose down
   docker-compose up --build
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
2. Review the logs using `docker-compose logs`
3. Open an issue on the repository

---

**Note**: The first run may take several minutes as it downloads the ML models from Hugging Face. Subsequent runs will be faster as the models are cached. 