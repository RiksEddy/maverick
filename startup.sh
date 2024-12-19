#!/bin/bash

# Set working directory
cd /home/rikseddy/maverick

# Pull latest changes
# git pull

# Start backend
cd app/backend
python3 main.py &                                                                             

# Wait a few seconds
sleep 2

# Start frontend
cd ../frontend
npm run dev -- --host &

# Keep script running (prevents rc.local from ending)
#wait
