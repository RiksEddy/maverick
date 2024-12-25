#!/bin/bash

# Set working directory
cd /home/maverick/app/backend

# Start backend
python3 main.py &                                                                             

# Wait a few seconds
sleep 5

# Start frontend
cd ../frontend
npm run dev -- --host &
