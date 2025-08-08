#!/bin/bash

echo "🛑 Stopping ML Pipeline services..."

# Stop all services
docker-compose down

echo "🧹 Cleaning up..."
docker system prune -f

echo "✅ All services stopped and cleaned up!"
echo ""
echo "📊 To start again:"
echo "   ./start.sh"
echo ""
echo "🗑️ To remove all data:"
echo "   docker-compose down -v" 