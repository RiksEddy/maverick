#!/bin/bash

# Set working directory
cd ~/maverick

# Pull latest changes
git pull

# Start backend
cd app/backend
python3 main.py &                                                                             

# Wait a second
sleep 1

# Start frontend
cd ../frontend
npm run dev -- --host &
