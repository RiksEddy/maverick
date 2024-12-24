#!/bin/bash

# Set working directory
cd /home/maverick

# Pull latest changes
git pull

# Start backend
cd app/backend
python3 main.py &                                                                             

# Wait a second
sleep 5

# Start frontend
cd ../frontend
npm run dev -- --host &
