#!/bin/bash

echo "🚀 Starting Perplexity Clone Frontend"
echo "====================================="

# Check if we're in the right directory
if [ ! -d "src/frontend" ]; then
    echo "❌ Error: src/frontend directory not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

echo "✅ Frontend directory found"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed!"
    echo "Please install Node.js 18+ to continue."
    exit 1
fi

echo "✅ Node.js found: $(node --version)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed!"
    echo "Please install npm to continue."
    exit 1
fi

echo "✅ npm found: $(npm --version)"

# Navigate to frontend directory and start
echo ""
echo "🔧 Starting development server..."
echo "Frontend will be available at: http://localhost:3000"
echo "Press Ctrl+C to stop the server"
echo ""

cd src/frontend && npm run dev
